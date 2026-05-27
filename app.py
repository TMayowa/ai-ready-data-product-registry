"""AI-Ready Data Product Registry — Streamlit application.

Demonstrates how enterprise data products can be structured, documented,
and governed for safe AI-agent consumption.
"""

from __future__ import annotations

import json
import os
import pandas as pd
import streamlit as st
import streamlit_mermaid as st_mermaid

from src.contract_validator import ai_consumer_summary, validate_contract
from src.lineage import generate_mermaid
from src.models import DataProduct
from src.readiness_score import (
    gaps,
    overall_score,
    readiness_status,
    score_all_dimensions,
    WEIGHTS,
)

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI-Ready Data Product Registry",
    layout="wide",
)

# ── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.title("Data Product Registry")
    st.caption(
        "A portfolio project demonstrating AI-ready data product governance."
    )
    st.divider()
    with st.expander("About"):
        st.markdown(
            "This app uses fully synthetic data. It does not contain "
            "real company data, proprietary architecture, or confidential "
            "material."
        )
    st.markdown(
        "[View on GitHub](https://github.com/TMayowa/ai-ready-data-product-registry)"
    )

# ── Title ───────────────────────────────────────────────────────────────────
st.title("AI-Ready Data Product Registry")
st.caption(
    "Demonstrating how enterprise data products can be structured, "
    "documented, and governed for safe AI consumption."
)

# ── Data loading ────────────────────────────────────────────────────────────
DATA_PATH = os.path.join(
    os.path.dirname(__file__), "data", "data_products.json"
)


@st.cache_data
def load_products() -> list[DataProduct] | None:
    """Load and parse data products from JSON. Returns None on failure."""
    if not os.path.isfile(DATA_PATH):
        return None
    try:
        with open(DATA_PATH, encoding="utf-8") as f:
            raw = json.load(f)
    except json.JSONDecodeError:
        return None
    if not raw:
        return None
    try:
        return [DataProduct.model_validate(r) for r in raw]
    except Exception:
        return None


products = load_products()

if products is None:
    st.error(
        "Could not load data products. Make sure `data/data_products.json` "
        "exists and contains valid data. Run `python generate_data.py` to "
        "regenerate."
    )
    st.stop()

# Precompute scores
product_map = {p.name: p for p in products}
product_scores = {p.name: overall_score(p) for p in products}
product_statuses = {p.name: readiness_status(s) for s, p in zip(product_scores.values(), products)}

# ── Tabs ────────────────────────────────────────────────────────────────────
tabs = st.tabs([
    "Catalogue",
    "Readiness Scores",
    "Data Contracts",
    "AI Consumer View",
    "Lineage",
])

# ════════════════════════════════════════════════════════════════════════════
# Tab 1 — Catalogue
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    # Summary metrics
    avg_score = sum(product_scores.values()) / len(product_scores)
    ready_count = sum(
        1 for s in product_statuses.values() if s in ("Ready", "Conditionally ready")
    )
    # Highest risk domain: domain with lowest average score
    domain_scores: dict[str, list[float]] = {}
    for p in products:
        domain_scores.setdefault(p.domain, []).append(overall_score(p))
    domain_avgs = {d: sum(v) / len(v) for d, v in domain_scores.items()}
    highest_risk_domain = min(domain_avgs, key=domain_avgs.get)  # type: ignore[arg-type]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Data Products", len(products))
    c2.metric("Average Readiness Score", f"{avg_score:.1f}")
    c3.metric("Products Ready for AI", ready_count)
    c4.metric("Highest Risk Domain", highest_risk_domain)

    st.divider()

    # Product overview table
    df_data = []
    for p in products:
        sc = overall_score(p)
        sts = readiness_status(sc)
        color = "green" if sts == "Ready" else "orange" if sts == "Conditionally ready" else "red"
        df_data.append({
            "Product": p.name,
            "Domain": p.domain,
            "Classification": p.classification,
            "Refresh": p.refresh_frequency,
            "Readiness Score": f"{sc:.1f}",
            "Status": f"<span style='color:{color};font-weight:bold'>{sts}</span>",
        })

    df = pd.DataFrame(df_data)
    st.markdown("### Product Catalogue")
    st.write(
        df[["Product", "Domain", "Classification", "Refresh", "Status"]].to_html(
            index=False, escape=False
        ),
        unsafe_allow_html=True,
    )

    st.divider()

    # Product detail
    selected_name = st.selectbox("Select a data product for details", list(product_map.keys()))
    p = product_map[selected_name]

    col_left, col_right = st.columns(2)
    with col_left:
        st.markdown("#### Core Metadata")
        st.markdown(f"**ID:** {p.id}")
        st.markdown(f"**Domain:** {p.domain}")
        st.markdown(f"**Classification:** {p.classification}")
        st.markdown(f"**Refresh Frequency:** {p.refresh_frequency}")
        st.markdown(f"**Source Systems:** {', '.join(p.source_systems)}")
        st.markdown(f"**Description:** {p.description}")
        st.markdown(f"**Created:** {p.created_date}")
        st.markdown(f"**Last Updated:** {p.last_updated}")
        if p.documentation_url:
            st.markdown(f"**Docs:** [{p.documentation_url}]({p.documentation_url})")
        st.markdown("#### Known Limitations")
        for lim in p.known_limitations:
            st.markdown(f"- {lim}")

    with col_right:
        st.markdown("#### Ownership")
        st.markdown(f"**Business Owner:** {p.business_owner}")
        st.markdown(f"**Technical Owner:** {p.technical_owner}")
        st.markdown(f"**Data Steward:** {p.data_steward}")
        st.markdown("#### Readiness")
        sc = product_scores[p.name]
        sts = product_statuses[p.name]
        st.metric("Overall Score", f"{sc:.1f}", delta=sts, delta_color="off")
        st.markdown(f"**Status:** {sts}")

# ════════════════════════════════════════════════════════════════════════════
# Tab 2 — Readiness Scores
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    sel = st.selectbox("Select a data product", list(product_map.keys()), key="readiness_select")
    p = product_map[sel]
    sc = overall_score(p)
    sts = readiness_status(sc)

    color_hex = "#28a745" if sc >= 80 else "#ffc107" if sc >= 50 else "#dc3545"
    st.markdown(
        f"<h2 style='text-align:center;color:{color_hex}'>Overall Score: {sc:.1f}</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<p style='text-align:center'><span style='color:{color_hex};font-weight:bold;font-size:1.2em'>{sts}</span></p>",
        unsafe_allow_html=True,
    )

    st.divider()

    dim_scores = score_all_dimensions(p)
    dim_display = {
        "ownership": "Ownership",
        "documentation": "Documentation",
        "lineage": "Lineage",
        "quality": "Quality",
        "access_rules": "Access Rules",
        "ai_usage_policy": "AI Usage Policy",
        "freshness": "Freshness",
        "human_escalation": "Human Escalation",
    }

    # 2x4 grid
    row1_cols = st.columns(4)
    row2_cols = st.columns(4)
    all_cols = row1_cols + row2_cols

    dim_keys = list(WEIGHTS.keys())
    for idx, dim in enumerate(dim_keys):
        val = dim_scores[dim]
        delta_color = "normal" if val >= 70 else "inverse" if val < 50 else "off"
        with all_cols[idx]:
            st.metric(
                label=dim_display[dim],
                value=f"{val}/100",
                delta=f"{WEIGHTS[dim]*100:.0f}% weight",
                delta_color=delta_color,
            )

    st.divider()

    st.markdown("### Improvement Gaps")
    gap_list = gaps(p)
    if gap_list:
        for g in gap_list:
            st.markdown(f"- {g}")
    else:
        st.success("No gaps identified — all dimensions are fully addressed.")

# ════════════════════════════════════════════════════════════════════════════
# Tab 3 — Data Contracts
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    sel = st.selectbox("Select a data product", list(product_map.keys()), key="contract_select")
    p = product_map[sel]
    dc = p.data_contract

    st.markdown("### Contract Details")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Contract Version:** {dc.contract_version}")
        st.markdown(f"**Last Reviewed:** {dc.last_reviewed}")
        st.markdown(f"**Freshness SLA:** {dc.freshness_sla}")
        st.markdown(f"**Escalation Contact:** {dc.escalation_contact}")
        st.markdown("**Consumers:**")
        for c in dc.consumers:
            st.markdown(f"- {c}")
    with c2:
        st.markdown("**AI Consumers:**")
        for c in dc.ai_consumers:
            st.markdown(f"- {c}")
        st.markdown("**Required Metadata Fields:**")
        for fld in dc.required_metadata_fields:
            st.markdown(f"- `{fld}`")

    st.divider()

    st.markdown("### Quality Rules")
    rules_df = pd.DataFrame([
        {
            "Field": r.field_name,
            "Rule": r.rule_description,
            "Threshold": r.threshold,
            "Severity": r.severity.upper(),
        }
        for r in dc.quality_rules
    ])
    st.table(rules_df)

    st.divider()

    st.markdown("### Validation Result")
    vr = validate_contract(dc)

    risk_color = "green" if vr.risk_level == "low" else "orange" if vr.risk_level == "medium" else "red"
    valid_icon = ":white_check_mark:" if vr.is_valid else ":x:"

    st.markdown(f"**Contract Valid:** {valid_icon}")
    risk_badge_color = {
        "low": "#28a745",
        "medium": "#ffc107",
        "high": "#dc3545",
    }
    st.markdown(
        f"**Risk Level:** <span style='color:{risk_badge_color[vr.risk_level]};font-weight:bold'>{vr.risk_level.upper()}</span>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"**AI Consumption Allowed:** {'Yes' if vr.ai_consumption_allowed else 'No'}"
    )

    if vr.missing_fields:
        st.markdown("**Missing Fields:**")
        for mf in vr.missing_fields:
            st.markdown(f"- {mf}")

    if vr.ai_consumption_conditions:
        st.markdown("**AI Consumption Conditions:**")
        for c in vr.ai_consumption_conditions:
            st.markdown(f"- {c}")

    if vr.warnings:
        st.markdown("**Warnings:**")
        for w in vr.warnings:
            st.markdown(f"- :warning: {w}")

# ════════════════════════════════════════════════════════════════════════════
# Tab 4 — AI Consumer View
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    st.markdown("### Can an AI agent use this data product?")
    sel = st.selectbox("Select a data product", list(product_map.keys()), key="ai_select")
    p = product_map[sel]
    summary = ai_consumer_summary(p)

    status_color = {
        "Approved": "#28a745",
        "Conditional": "#ffc107",
        "Blocked": "#dc3545",
    }
    st.markdown(
        f"<h2 style='text-align:center;color:{status_color[summary['status']]}'>{summary['status']}</h2>",
        unsafe_allow_html=True,
    )

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### Permitted Actions")
        for action in summary["permitted_actions"]:
            st.markdown(f":white_check_mark: {action}")

    with col_r:
        st.markdown("#### Prohibited Actions")
        for action in summary["prohibited_actions"]:
            st.markdown(f":no_entry: {action}")

    st.divider()

    if summary["conditions"]:
        st.markdown("#### Conditions for Use")
        for cond in summary["conditions"]:
            st.info(cond)

    st.markdown("#### Human Approval Required For")
    if summary["required_human_approval_for"]:
        for idx, trigger in enumerate(summary["required_human_approval_for"], 1):
            st.markdown(f"{idx}. {trigger}")
    else:
        st.markdown("*None specified*")

    st.divider()

    st.markdown(f"**Max Autonomy Level:** `{p.data_contract.ai_usage_policy.max_autonomy_level}`")

    if p.data_contract.ai_usage_policy.max_autonomy_level == "read-only":
        st.warning(
            "This data product is approved for read-only AI consumption. "
            "AI agents may analyse and summarise but must not take actions "
            "or generate recommendations without explicit human approval."
        )

# ════════════════════════════════════════════════════════════════════════════
# Tab 5 — Lineage
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    sel = st.selectbox("Select a data product", list(product_map.keys()), key="lineage_select")
    p = product_map[sel]

    st.markdown("### Data Lineage")
    mermaid_code = generate_mermaid(p)
    try:
        st_mermaid.st_mermaid(mermaid_code, height=500)
    except Exception:
        st.code(mermaid_code, language="mermaid")

    st.divider()

    st.markdown("### Lineage Nodes")
    node_df = pd.DataFrame([
        {"System": n.system_name, "Layer": n.layer, "Description": n.description}
        for n in p.lineage
    ])
    st.table(node_df)
