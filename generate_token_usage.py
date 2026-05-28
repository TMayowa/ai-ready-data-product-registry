"""Token usage generator for the AI-Ready Data & AI Governance Platform.

Generates 6 months of realistic token consumption data (Dec 2025 - May 2026)
for each generative AI model.
"""

import json
import os
import random

from src.models import ModelTokenConsumption, SubModelUsage, TokenUsage

MONTHS = ["2025-12", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05"]

# Approximate token pricing (per million tokens)
HAIKU_INPUT_PER_M = 0.25
HAIKU_OUTPUT_PER_M = 1.25
SONNET_INPUT_PER_M = 3.00
SONNET_OUTPUT_PER_M = 15.00


def _vary(base: int, pct: float = 0.08) -> int:
    """Add ±pct% random variance to a base value."""
    delta = int(base * pct)
    return max(0, base + random.randint(-delta, delta))


def _haiku_cost(input_t: int, output_t: int) -> float:
    return round(input_t / 1_000_000 * HAIKU_INPUT_PER_M + output_t / 1_000_000 * HAIKU_OUTPUT_PER_M, 4)


def _sonnet_cost(input_t: int, output_t: int) -> float:
    return round(input_t / 1_000_000 * SONNET_INPUT_PER_M + output_t / 1_000_000 * SONNET_OUTPUT_PER_M, 4)


def _zero_usage() -> list[TokenUsage]:
    return [TokenUsage(month=m, input_tokens=0, output_tokens=0,
                       total_tokens=0, cost_usd=0.0, requests=0) for m in MONTHS]


def _generate_all() -> list[ModelTokenConsumption]:
    results: list[ModelTokenConsumption] = []

    # ── 1. Supplier Risk Agent (multi-model) ──────────────────────────────
    # Haiku scanner: gradually increasing trend
    haiku_bases_in = [190_000, 195_000, 200_000, 205_000, 210_000, 218_000]
    haiku_bases_out = [44_000, 45_000, 47_000, 48_000, 50_000, 52_000]
    haiku_req = [3800, 3900, 4000, 4050, 4100, 4200]

    haiku_usage = [
        TokenUsage(
            month=MONTHS[i],
            input_tokens=_vary(haiku_bases_in[i]),
            output_tokens=_vary(haiku_bases_out[i]),
            total_tokens=_vary(haiku_bases_in[i]) + _vary(haiku_bases_out[i]),
            cost_usd=_haiku_cost(_vary(haiku_bases_in[i]), _vary(haiku_bases_out[i])),
            requests=_vary(haiku_req[i]),
        ) for i in range(6)
    ]
    for u in haiku_usage:
        u.total_tokens = u.input_tokens + u.output_tokens
        u.cost_usd = _haiku_cost(u.input_tokens, u.output_tokens)

    # Sonnet synthesiser: stable with slight increase
    sonnet_bases_in = [65_000, 67_000, 70_000, 72_000, 73_000, 75_000]
    sonnet_bases_out = [28_000, 29_000, 31_000, 33_000, 34_000, 35_000]
    sonnet_req = [420, 430, 450, 460, 465, 480]

    sonnet_usage = [
        TokenUsage(
            month=MONTHS[i],
            input_tokens=_vary(sonnet_bases_in[i]),
            output_tokens=_vary(sonnet_bases_out[i]),
            total_tokens=0,
            cost_usd=0.0,
            requests=_vary(sonnet_req[i]),
        ) for i in range(6)
    ]
    for u in sonnet_usage:
        u.total_tokens = u.input_tokens + u.output_tokens
        u.cost_usd = _sonnet_cost(u.input_tokens, u.output_tokens)

    # Aggregate totals
    sra_total = [
        TokenUsage(
            month=MONTHS[i],
            input_tokens=haiku_usage[i].input_tokens + sonnet_usage[i].input_tokens,
            output_tokens=haiku_usage[i].output_tokens + sonnet_usage[i].output_tokens,
            total_tokens=haiku_usage[i].total_tokens + sonnet_usage[i].total_tokens,
            cost_usd=round(haiku_usage[i].cost_usd + sonnet_usage[i].cost_usd, 4),
            requests=haiku_usage[i].requests,
        ) for i in range(6)
    ]
    last_total = sra_total[-1].total_tokens
    monthly_budget = 150.0
    utilisation = round(sra_total[-1].cost_usd / monthly_budget * 100, 1)

    results.append(ModelTokenConsumption(
        model_id="supplier-risk-agent",
        is_multi_model=True,
        total_monthly_usage=sra_total,
        sub_model_breakdown=[
            SubModelUsage(sub_model_name="Claude 3.5 Haiku", role="Signal scanning & filtering", monthly_usage=haiku_usage),
            SubModelUsage(sub_model_name="Claude 3.5 Sonnet", role="Risk synthesis & recommendation", monthly_usage=sonnet_usage),
        ],
        avg_tokens_per_request=1400,
        avg_cost_per_request_usd=0.012,
        monthly_budget_usd=monthly_budget,
        budget_utilisation_pct=utilisation,
    ))

    # ── 2. Contract Insights Assistant (single Haiku) ────────────────────
    # Spike in March 2026 (contract renewal season)
    cia_in = [95_000, 100_000, 108_000, 145_000, 105_000, 100_000]
    cia_out = [22_000, 24_000, 26_000, 35_000, 25_000, 23_000]
    cia_req = [1800, 1900, 2000, 2600, 2000, 1950]

    cia_usage = [
        TokenUsage(
            month=MONTHS[i],
            input_tokens=_vary(cia_in[i]),
            output_tokens=_vary(cia_out[i]),
            total_tokens=0, cost_usd=0.0,
            requests=_vary(cia_req[i]),
        ) for i in range(6)
    ]
    for u in cia_usage:
        u.total_tokens = u.input_tokens + u.output_tokens
        u.cost_usd = _haiku_cost(u.input_tokens, u.output_tokens)

    cia_budget = 50.0
    cia_util = round(cia_usage[-1].cost_usd / cia_budget * 100, 1)

    results.append(ModelTokenConsumption(
        model_id="contract-insights-assistant",
        is_multi_model=False,
        total_monthly_usage=cia_usage,
        sub_model_breakdown=[],
        avg_tokens_per_request=850,
        avg_cost_per_request_usd=0.004,
        monthly_budget_usd=cia_budget,
        budget_utilisation_pct=cia_util,
    ))

    # ── 3. Logistics Disruption Agent (multi-model, staging, ramping up) ─
    lda_hk_in = [40_000, 45_000, 50_000, 55_000, 62_000, 68_000]
    lda_hk_out = [12_000, 14_000, 16_000, 17_000, 19_000, 21_000]
    lda_sn_in = [22_000, 26_000, 30_000, 34_000, 38_000, 43_000]
    lda_sn_out = [8_000, 10_000, 12_000, 14_000, 16_000, 18_000]
    lda_req = [200, 250, 320, 400, 500, 600]

    lda_hk_usage = [
        TokenUsage(
            month=MONTHS[i],
            input_tokens=_vary(lda_hk_in[i]),
            output_tokens=_vary(lda_hk_out[i]),
            total_tokens=0, cost_usd=0.0,
            requests=_vary(lda_req[i]),
        ) for i in range(6)
    ]
    for u in lda_hk_usage:
        u.total_tokens = u.input_tokens + u.output_tokens
        u.cost_usd = _haiku_cost(u.input_tokens, u.output_tokens)

    lda_sn_usage = [
        TokenUsage(
            month=MONTHS[i],
            input_tokens=_vary(lda_sn_in[i]),
            output_tokens=_vary(lda_sn_out[i]),
            total_tokens=0, cost_usd=0.0,
            requests=_vary(lda_req[i] // 2),
        ) for i in range(6)
    ]
    for u in lda_sn_usage:
        u.total_tokens = u.input_tokens + u.output_tokens
        u.cost_usd = _sonnet_cost(u.input_tokens, u.output_tokens)

    lda_total = [
        TokenUsage(
            month=MONTHS[i],
            input_tokens=lda_hk_usage[i].input_tokens + lda_sn_usage[i].input_tokens,
            output_tokens=lda_hk_usage[i].output_tokens + lda_sn_usage[i].output_tokens,
            total_tokens=lda_hk_usage[i].total_tokens + lda_sn_usage[i].total_tokens,
            cost_usd=round(lda_hk_usage[i].cost_usd + lda_sn_usage[i].cost_usd, 4),
            requests=lda_req[i],
        ) for i in range(6)
    ]
    lda_budget = 80.0
    lda_util = round(lda_total[-1].cost_usd / lda_budget * 100, 1)

    results.append(ModelTokenConsumption(
        model_id="logistics-disruption-agent",
        is_multi_model=True,
        total_monthly_usage=lda_total,
        sub_model_breakdown=[
            SubModelUsage(sub_model_name="Claude 3.5 Haiku", role="Event monitoring & classification", monthly_usage=lda_hk_usage),
            SubModelUsage(sub_model_name="Claude 3.5 Sonnet", role="Disruption prediction & contingency", monthly_usage=lda_sn_usage),
        ],
        avg_tokens_per_request=1800,
        avg_cost_per_request_usd=0.015,
        monthly_budget_usd=lda_budget,
        budget_utilisation_pct=lda_util,
    ))

    # ── 4. Inventory Planning Assistant (non-generative — XGBoost) ───────
    results.append(ModelTokenConsumption(
        model_id="inventory-planning-assistant",
        is_multi_model=False,
        total_monthly_usage=_zero_usage(),
        sub_model_breakdown=[],
        avg_tokens_per_request=0,
        avg_cost_per_request_usd=0.0,
        monthly_budget_usd=None,
        budget_utilisation_pct=None,
    ))

    # ── 5. Maintenance Planning Agent (non-generative — LSTM + RF) ───────
    results.append(ModelTokenConsumption(
        model_id="maintenance-planning-agent",
        is_multi_model=False,
        total_monthly_usage=_zero_usage(),
        sub_model_breakdown=[],
        avg_tokens_per_request=0,
        avg_cost_per_request_usd=0.0,
        monthly_budget_usd=None,
        budget_utilisation_pct=None,
    ))

    # ── 6. Procurement Anomaly Detector (non-generative — Isolation Forest)
    results.append(ModelTokenConsumption(
        model_id="procurement-anomaly-detector",
        is_multi_model=False,
        total_monthly_usage=_zero_usage(),
        sub_model_breakdown=[],
        avg_tokens_per_request=0,
        avg_cost_per_request_usd=0.0,
        monthly_budget_usd=None,
        budget_utilisation_pct=None,
    ))

    return results


def main() -> None:
    data = _generate_all()
    project_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(project_dir, "data", "token_usage.json")

    with open(path, "w", encoding="utf-8") as f:
        json.dump([d.model_dump(mode="json") for d in data], f, indent=2)

    print(f"Saved {len(data)} token consumption profiles to {path}\n")
    print(f"{'Model':<35} {'Generative':<12} {'Tokens (May)':<15} {'Cost (May)':<12} {'Budget util':<12}")
    print("-" * 90)
    for d in data:
        last = d.total_monthly_usage[-1]
        gen = "Yes" if d.avg_tokens_per_request > 0 else "No"
        util = f"{d.budget_utilisation_pct}%" if d.budget_utilisation_pct is not None else "N/A"
        print(f"  {d.model_id:<33} {gen:<12} {last.total_tokens:>12,}   ${last.cost_usd:<10.3f} {util:<12}")


if __name__ == "__main__":
    main()
