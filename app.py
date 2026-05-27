"""AI-Ready Data & AI Governance Platform — Streamlit application (v2).

8-tab governance platform combining data product catalogue, AI model registry,
readiness scoring, contract validation, lineage visualisation, and governance workflows.
"""

from __future__ import annotations

import json
import os

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from src.contract_validator import ai_consumer_summary, validate_contract
from src.data_mesh import domain_summary, generate_mesh_diagram, mesh_principles_status
from src.lineage import generate_mermaid
from src.models import AIModel, APIKey, ApprovalRequest, DataProduct, User
from src.process_maps import (
    generate_maintenance_process_map,
    generate_p2p_process_map,
    get_process_list,
)
from src.readiness_score import (
    WEIGHTS,
    gaps,
    overall_score,
    readiness_status,
    score_all_dimensions,
)

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI-Ready Data Product Registry",
    layout="wide",
    page_icon="🏗️",
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# ── Helpers ───────────────────────────────────────────────────────────────────

def badge(text: str, bg: str, fg: str) -> str:
    return (
        f'<span style="background:{bg};color:{fg};padding:2px 10px;'
        f'border-radius:4px;font-size:12px;font-weight:500">{text}</span>'
    )


STATUS_COLORS: dict[str, tuple[str, str]] = {
    "Approved": ("#E1F5EE", "#0F6E56"),
    "Production": ("#E1F5EE", "#0F6E56"),
    "Ready": ("#E1F5EE", "#0F6E56"),
    "Active": ("#E1F5EE", "#0F6E56"),
    "Achieved": ("#E1F5EE", "#0F6E56"),
    "On track": ("#E1F5EE", "#0F6E56"),
    "Under review": ("#FAEEDA", "#854F0B"),
    "Staging": ("#FAEEDA", "#854F0B"),
    "Conditional": ("#FAEEDA", "#854F0B"),
    "Conditionally ready": ("#FAEEDA", "#854F0B"),
    "At risk": ("#FAEEDA", "#854F0B"),
    "Escalated": ("#FAEEDA", "#854F0B"),
    "Draft": ("#F1EFE8", "#5F5E5A"),
    "Development": ("#F1EFE8", "#5F5E5A"),
    "Pending": ("#F1EFE8", "#5F5E5A"),
    "Behind": ("#F1EFE8", "#5F5E5A"),
    "Rejected": ("#FCEBEB", "#A32D2D"),
    "Deprecated": ("#FCEBEB", "#A32D2D"),
    "Blocked": ("#FCEBEB", "#A32D2D"),
    "Expired": ("#FCEBEB", "#A32D2D"),
    "Not ready": ("#FCEBEB", "#A32D2D"),
    "Restricted": ("#FAECE7", "#993C1D"),
    "Critical": ("#FAECE7", "#993C1D"),
    "High": ("#FAECE7", "#993C1D"),
    "Suspended": ("#FAECE7", "#993C1D"),
    "Confidential": ("#EEEDFE", "#534AB7"),
}


def sbadge(status: str) -> str:
    bg, fg = STATUS_COLORS.get(status, ("#F1EFE8", "#5F5E5A"))
    return badge(status, bg, fg)


def render_mermaid(code: str, height: int = 520) -> None:
    """Render a Mermaid diagram via the CDN (no extra dependencies required)."""
    html = f"""
    <div style="background:#fff;padding:16px;border-radius:8px;overflow:auto">
      <pre class="mermaid">{code}</pre>
    </div>
    <script type="module">
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{startOnLoad:true,theme:'neutral',flowchart:{{useMaxWidth:true,htmlLabels:true}}}});
    </script>
    """
    components.html(html, height=height, scrolling=True)


# ── Data loading ──────────────────────────────────────────────────────────────

@st.cache_data
def load_products() -> list[DataProduct]:
    p = os.path.join(BASE_DIR, "data", "data_products.json")
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [DataProduct.model_validate(r) for r in json.load(f)]


@st.cache_data
def load_ai_models() -> list[AIModel]:
    p = os.path.join(BASE_DIR, "data", "ai_models.json")
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [AIModel.model_validate(r) for r in json.load(f)]


@st.cache_data
def load_users() -> list[User]:
    p = os.path.join(BASE_DIR, "data", "users.json")
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [User.model_validate(r) for r in json.load(f)]


@st.cache_data
def load_api_keys() -> list[APIKey]:
    p = os.path.join(BASE_DIR, "data", "api_keys.json")
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [APIKey.model_validate(r) for r in json.load(f)]


@st.cache_data
def load_approval_requests() -> list[ApprovalRequest]:
    p = os.path.join(BASE_DIR, "data", "approval_requests.json")
    if not os.path.isfile(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [ApprovalRequest.model_validate(r) for r in json.load(f)]


products = load_products()
ai_models = load_ai_models()
users = load_users()
api_keys = load_api_keys()
approval_requests = load_approval_requests()

if not products:
    st.error("Could not load data products. Run `python generate_data.py` first.")
    st.stop()

# Precompute
product_map = {p.name: p for p in products}
product_id_map = {p.id: p for p in products}
product_scores = {p.name: overall_score(p) for p in products}
product_statuses = {p.name: readiness_status(product_scores[p.name]) for p in products}
model_map = {m.name: m for m in ai_models}
model_id_map = {m.id: m for m in ai_models}
user_map = {u.id: u for u in users}

# ── Sidebar ───────────────────────────────────────────────────────────────────

with st.sidebar:
    st.title("Data & AI Governance Platform")
    st.caption(
        "Enterprise data products and AI models — governed, documented, "
        "ready for safe consumption."
    )
    st.divider()
    with st.expander("About this platform"):
        st.markdown(
            "A portfolio project using **fully synthetic data**. "
            "Demonstrates how a Collibra-style data catalogue and AI model registry "
            "can be combined with data mesh principles and governance workflows."
        )
    with st.expander("Platform stats"):
        active_keys = sum(1 for k in api_keys if k.status == "Active")
        st.metric("Data Products", len(products))
        st.metric("AI Models", len(ai_models))
        st.metric("Users", len(users))
        st.metric("Active API Keys", active_keys)
    st.markdown(
        "[View on GitHub](https://github.com/TMayowa/ai-ready-data-product-registry)"
    )

# ── Global banner ─────────────────────────────────────────────────────────────

st.title("AI-Ready Data Product Registry")
st.caption(
    "Demonstrating how enterprise data products and AI models can be structured, "
    "documented, and governed for safe AI consumption."
)

avg_score = sum(product_scores.values()) / len(product_scores)
in_prod = sum(1 for m in ai_models if m.status == "Production")
pending_count = sum(1 for r in approval_requests if r.status == "Pending")

g1, g2, g3, g4 = st.columns(4)
g1.metric("Data Products", len(products))
g2.metric("AI Models", len(ai_models), f"{in_prod} in Production")
g3.metric("Avg Readiness Score", f"{avg_score:.1f}")
g4.metric(
    "Pending Approvals", pending_count,
    delta="⚠ Needs attention" if pending_count > 0 else "All clear",
    delta_color="inverse" if pending_count > 0 else "off",
)
st.divider()

# ── Tabs ──────────────────────────────────────────────────────────────────────

tabs = st.tabs([
    "📦 Data Catalogue",
    "🤖 AI Model Registry",
    "📊 Readiness Scores",
    "📋 Data Contracts",
    "🔍 AI Consumption",
    "🔗 Lineage",
    "🏗️ Governance",
    "🗺️ Process Maps",
])

# ════════════════════════════════════════════════════════════════════════════
# TAB 1 — Data Catalogue
# ════════════════════════════════════════════════════════════════════════════
with tabs[0]:
    ready_count = sum(1 for s in product_statuses.values() if s in ("Ready", "Conditionally ready"))
    domain_avgs: dict[str, list[float]] = {}
    for p in products:
        domain_avgs.setdefault(p.domain, []).append(product_scores[p.name])
    highest_risk = min(domain_avgs, key=lambda d: sum(domain_avgs[d]) / len(domain_avgs[d]))
    most_accessed = max(products, key=lambda p: p.api_calls_last_30_days)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Products", len(products))
    c2.metric("Avg Readiness Score", f"{avg_score:.1f}")
    c3.metric("Ready for AI", ready_count)
    c4.metric("Most Accessed", most_accessed.name.split()[0] + "…")

    st.divider()
    st.markdown("### Product Catalogue")

    rows = []
    for p in products:
        sc = product_scores[p.name]
        sts = product_statuses[p.name]
        rows.append({
            "Product": p.name,
            "Domain": p.domain,
            "Classification": p.classification,
            "Gov Status": sbadge(p.governance_status),
            "Refresh": p.refresh_frequency,
            "Score": f"{sc:.1f}",
            "Readiness": sbadge(sts),
            "Consumers": str(p.total_consumers),
        })
    df = pd.DataFrame(rows)
    st.write(df.to_html(index=False, escape=False), unsafe_allow_html=True)

    st.divider()
    sel = st.selectbox("Select a product for full details", list(product_map.keys()), key="cat_sel")
    p = product_map[sel]
    sc = product_scores[p.name]
    sts = product_statuses[p.name]

    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### Core Metadata")
        st.markdown(f"**ID:** `{p.id}`")
        st.markdown(f"**Domain:** {p.domain}")
        st.markdown(f"**Classification:** {sbadge(p.classification)}", unsafe_allow_html=True)
        st.markdown(f"**Governance:** {sbadge(p.governance_status)}", unsafe_allow_html=True)
        st.markdown(f"**Refresh:** {p.refresh_frequency}")
        if p.update_frequency_actual:
            st.markdown(f"**Actual:** _{p.update_frequency_actual}_")
        st.markdown(f"**Sources:** {', '.join(p.source_systems)}")
        st.markdown(f"**Description:** {p.description}")
        st.markdown(f"**Created:** {p.created_date} | **Updated:** {p.last_updated}")
        if p.documentation_url:
            st.markdown(f"**Docs:** [{p.documentation_url}]({p.documentation_url})")
        if p.record_count:
            st.markdown(f"**Records:** ~{p.record_count:,} | **Size:** {p.size_mb} MB")
        if p.data_sensitivity:
            st.warning(f"**Sensitivity:** {p.data_sensitivity}")
        if p.retention_policy:
            st.markdown(f"**Retention:** {p.retention_policy}")
        st.markdown("**Known Limitations:**")
        for lim in p.known_limitations:
            st.markdown(f"- {lim}")
        if p.tags:
            tags_html = " ".join(badge(t, "#E6F1FB", "#185FA5") for t in p.tags)
            st.markdown(f"**Tags:** {tags_html}", unsafe_allow_html=True)

    with col_r:
        st.markdown("#### Ownership")
        st.markdown(f"**Business Owner:** {p.business_owner}")
        st.markdown(f"**Technical Owner:** {p.technical_owner}")
        st.markdown(f"**Data Steward:** {p.data_steward if p.data_steward else '⚠️ _Not assigned_'}")
        if p.domain_owner_team:
            st.markdown(f"**Domain Team:** {p.domain_owner_team}")
        st.divider()
        st.markdown("#### Readiness")
        color = "#28a745" if sc >= 80 else "#ffc107" if sc >= 50 else "#dc3545"
        st.markdown(f"<h3 style='color:{color}'>{sc:.1f}</h3>", unsafe_allow_html=True)
        st.markdown(sbadge(sts), unsafe_allow_html=True)
        st.divider()
        st.markdown("#### Usage Metrics")
        u1, u2 = st.columns(2)
        u1.metric("API Calls (30d)", f"{p.api_calls_last_30_days:,}")
        u2.metric("Unique Users (30d)", p.unique_users_last_30_days)
        u3, u4 = st.columns(2)
        u3.metric("Internal Shares", p.data_shares_internal)
        u4.metric("External Shares", p.data_shares_external)
        if p.last_accessed:
            st.caption(f"Last accessed: {p.last_accessed}")
        st.divider()
        st.markdown("#### API Access")
        st.markdown(f"**Endpoint:** `{p.api_endpoint}`")
        st.markdown(f"**Rate Limit:** {p.api_rate_limit}")
        if p.api_documentation_url:
            st.markdown(f"[API Docs]({p.api_documentation_url})")

    if p.schema_fields:
        st.divider()
        st.markdown("#### Schema")
        st.dataframe(pd.DataFrame(p.schema_fields), use_container_width=True)

    st.divider()
    with st.expander("📄 View as JSON"):
        st.json(p.model_dump(mode="json"))
    with st.expander("📎 Data product schema"):
        st.json(DataProduct.model_json_schema())

# ════════════════════════════════════════════════════════════════════════════
# TAB 2 — AI Model Registry
# ════════════════════════════════════════════════════════════════════════════
with tabs[1]:
    if not ai_models:
        st.info("No AI models. Run `python generate_ai_models.py` first.")
    else:
        prod_models = sum(1 for m in ai_models if m.status == "Production")
        review_models = sum(1 for m in ai_models if m.governance_status == "Under review")
        latest_scores = [m.evaluations[-1].score for m in ai_models if m.evaluations]
        avg_eval = sum(latest_scores) / len(latest_scores) if latest_scores else 0

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Total Models", len(ai_models))
        m2.metric("In Production", prod_models)
        m3.metric("Under Review", review_models)
        m4.metric("Avg Latest Eval", f"{avg_eval:.1f}")

        st.divider()
        rows = []
        for m in ai_models:
            latest = m.evaluations[-1].score if m.evaluations else "-"
            n_evals = len(m.evaluations)
            n_passed = sum(1 for e in m.evaluations if e.passed)
            rows.append({
                "Model": m.name,
                "Type": m.model_type,
                "Status": sbadge(m.status),
                "Governance": sbadge(m.governance_status),
                "Risk": sbadge(m.risk_classification),
                "Domain": m.domain,
                "Autonomy": m.max_autonomy_level,
                "Evals": f"{n_passed}/{n_evals} passed",
            })
        mdf = pd.DataFrame(rows)
        st.write(mdf.to_html(index=False, escape=False), unsafe_allow_html=True)

        st.divider()
        sel_m = st.selectbox("Select a model for full details", list(model_map.keys()), key="ai_sel")
        m = model_map[sel_m]
        st.markdown(f"**{m.name}** — v{m.version}")
        st.markdown(m.description)

        col_left, col_right = st.columns(2)
        with col_left:
            st.markdown("#### Ownership & Governance")
            st.markdown(f"**Model Owner:** {m.model_owner}")
            st.markdown(f"**Governance Lead:** {m.governance_lead}")
            st.markdown(f"**Team:** {m.owning_team}")
            st.markdown(f"**Status:** {sbadge(m.status)}", unsafe_allow_html=True)
            st.markdown(f"**Governance:** {sbadge(m.governance_status)}", unsafe_allow_html=True)
            st.markdown(f"**Risk:** {sbadge(m.risk_classification)}", unsafe_allow_html=True)
            st.markdown(f"**Last Review:** {m.last_governance_review} | **Next:** {m.next_review_due}")
            st.markdown("#### Technical")
            st.markdown(f"**Base Model:** {m.base_model or 'N/A'}")
            st.markdown(f"**Framework:** {m.framework or 'N/A'}")
            st.markdown(f"**Infrastructure:** {m.infrastructure or 'N/A'}")
            st.markdown(f"**Autonomy:** `{m.max_autonomy_level}`")
            if m.api_endpoint:
                st.markdown(f"**Endpoint:** `{m.api_endpoint}`")

        with col_right:
            st.markdown("#### Usage")
            s1, s2 = st.columns(2)
            s1.metric("Requests (30d)", f"{m.total_requests_last_30_days:,}")
            s2.metric("Users", m.users_with_access)
            if m.avg_latency_ms:
                s3, s4 = st.columns(2)
                s3.metric("Latency", f"{m.avg_latency_ms}ms")
                s4.metric("Error Rate", f"{m.error_rate_pct}%")
            st.markdown("#### Allowed Actions")
            for a in m.allowed_actions:
                st.markdown(f"✅ {a}")
            st.markdown("#### Prohibited Actions")
            for a in m.prohibited_actions:
                st.markdown(f"🚫 {a}")
            st.markdown("#### Human Oversight")
            for h in m.human_oversight_required:
                st.markdown(f"- {h}")

        st.divider()
        st.markdown("#### Data Dependencies")
        for dp_id in m.input_data_products:
            dp = product_id_map.get(dp_id)
            if dp:
                dp_score = product_scores[dp.name]
                min_score = m.minimum_data_quality_score or 0
                ok = dp_score >= min_score
                st.markdown(
                    f"{'\u2705' if ok else '⚠️'} **{dp.name}** — Score: **{dp_score:.1f}** "
                    f"{'(meets min)' if ok else f'(below required {min_score})'}"
                )

        st.divider()
        st.markdown("#### OKRs")
        for okr in m.okrs:
            with st.container():
                oc, os_ = st.columns([3, 1])
                oc.markdown(f"**{okr.objective}**")
                os_.markdown(sbadge(okr.status), unsafe_allow_html=True)
                st.progress(okr.progress_pct / 100)
                st.caption(f"{okr.progress_pct}% · {okr.quarter}")
                for kr in okr.key_results:
                    st.markdown(f"  - {kr}")

        st.divider()
        st.markdown("#### Evaluations")
        if m.evaluations:
            le = m.evaluations[-1]
            st.markdown(
                f"**Latest:** {'\u2705' if le.passed else '\u274c'} "
                f"{le.eval_type} — Score **{le.score:.0f}** ({le.eval_date})"
            )
            eval_df = pd.DataFrame([
                {"Date": e.eval_date, "Type": e.eval_type, "Score": e.score,
                 "Passed": "✅" if e.passed else "❌", "Notes": e.notes, "By": e.evaluated_by}
                for e in m.evaluations
            ])
            st.dataframe(eval_df, use_container_width=True)

        with st.expander("📄 View as JSON"):
            st.json(m.model_dump(mode="json"))

# ════════════════════════════════════════════════════════════════════════════
# TAB 3 — Readiness Scores
# ════════════════════════════════════════════════════════════════════════════
with tabs[2]:
    compare_mode = st.checkbox("Compare two products side by side")

    if compare_mode:
        ca, cb = st.columns(2)
        with ca:
            sel_a = st.selectbox("Product A", list(product_map.keys()), key="cmp_a")
        with cb:
            sel_b = st.selectbox("Product B", list(product_map.keys()), key="cmp_b",
                                 index=min(1, len(product_map) - 1))
        show_list = [(sel_a, ca), (sel_b, cb)]
    else:
        sel = st.selectbox("Select a product", list(product_map.keys()), key="read_sel")
        show_list = [(sel, st)]

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

    for pname, container in show_list:
        p = product_map[pname]
        sc = overall_score(p)
        sts = readiness_status(sc)
        color = "#28a745" if sc >= 80 else "#ffc107" if sc >= 50 else "#dc3545"
        with container:
            if compare_mode:
                st.markdown(f"### {p.name}")
            st.markdown(
                f"<h2 style='text-align:center;color:{color}'>Overall: {sc:.1f}</h2>",
                unsafe_allow_html=True,
            )
            st.markdown(f"<p style='text-align:center'>{sbadge(sts)}</p>", unsafe_allow_html=True)
            st.divider()
            dim_scores = score_all_dimensions(p)
            row1 = st.columns(4)
            row2 = st.columns(4)
            for i, dim in enumerate(list(WEIGHTS.keys())):
                val = dim_scores[dim]
                dc = "normal" if val >= 70 else "inverse" if val < 50 else "off"
                with (row1 + row2)[i]:
                    st.metric(dim_display[dim], f"{val}/100",
                              delta=f"{WEIGHTS[dim]*100:.0f}% weight", delta_color=dc)
            st.divider()
            gap_list = gaps(p)
            if gap_list:
                st.markdown("**Gaps:**")
                for g in gap_list:
                    st.markdown(f"- {g}")
            else:
                st.success("No gaps — all dimensions fully addressed.")
            # AI consumer impact
            dependent = [m for m in ai_models if p.id in m.input_data_products]
            if dependent:
                st.divider()
                st.markdown("**Impact on AI consumers:**")
                for m in dependent:
                    min_q = m.minimum_data_quality_score or 0
                    ok = sc >= min_q
                    st.markdown(
                        f"{'\u2705' if ok else '⚠️'} **{m.name}** requires {min_q} — "
                        f"current {sc:.1f} ({'OK' if ok else 'BELOW REQUIREMENT'})"
                    )

# ════════════════════════════════════════════════════════════════════════════
# TAB 4 — Data Contracts
# ════════════════════════════════════════════════════════════════════════════
with tabs[3]:
    sel = st.selectbox("Select a product", list(product_map.keys()), key="con_sel")
    p = product_map[sel]
    dc = p.data_contract

    st.markdown("### Contract Details")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"**Version:** {dc.contract_version}")
        st.markdown(f"**Last Reviewed:** {dc.last_reviewed}")
        st.markdown(f"**Freshness SLA:** {dc.freshness_sla or '⚠️ _Not defined_'}")
        st.markdown(f"**Escalation Contact:** {dc.escalation_contact or '⚠️ _Not defined_'}")
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
        bound = [m for m in ai_models if p.id in m.input_data_products]
        if bound:
            st.markdown("**AI Models bound by this contract:**")
            for m in bound:
                st.markdown(f"- {m.name} ({sbadge(m.status)})", unsafe_allow_html=True)

    st.divider()
    st.markdown("### Quality Rules")
    if dc.quality_rules:
        rules_df = pd.DataFrame([
            {"Field": r.field_name, "Rule": r.rule_description,
             "Threshold": r.threshold, "Severity": r.severity.upper()}
            for r in dc.quality_rules
        ])
        st.table(rules_df)
    else:
        st.warning("No quality rules defined.")

    st.divider()
    st.markdown("### Validation Result")
    vr = validate_contract(dc)
    st.markdown(f"**Valid:** {'\u2705' if vr.is_valid else '\u274c'}")
    st.markdown(f"**Risk Level:** {sbadge(vr.risk_level.capitalize())}", unsafe_allow_html=True)
    st.markdown(f"**AI Consumption:** {'Allowed' if vr.ai_consumption_allowed else 'Not allowed'}")
    if vr.missing_fields:
        st.markdown("**Missing Fields:**")
        for mf in vr.missing_fields:
            st.markdown(f"- {mf}")
    if vr.warnings:
        for w in vr.warnings:
            st.warning(w)

    st.divider()
    with st.expander("📄 View contract as JSON"):
        st.json(dc.model_dump(mode="json"))

# ════════════════════════════════════════════════════════════════════════════
# TAB 5 — AI Consumption
# ════════════════════════════════════════════════════════════════════════════
with tabs[4]:
    st.markdown("### Can an AI agent use this data product?")
    sel = st.selectbox("Select a product", list(product_map.keys()), key="ai_con_sel")
    p = product_map[sel]
    summary = ai_consumer_summary(p)
    sc_color = STATUS_COLORS.get(summary["status"], ("#F1EFE8", "#5F5E5A"))
    st.markdown(
        f"<h2 style='text-align:center;color:{sc_color[1]}'>{summary['status']}</h2>",
        unsafe_allow_html=True,
    )
    col_l, col_r = st.columns(2)
    with col_l:
        st.markdown("#### Permitted Actions")
        for a in summary["permitted_actions"]:
            st.markdown(f"✅ {a}")
    with col_r:
        st.markdown("#### Prohibited Actions")
        for a in summary["prohibited_actions"]:
            st.markdown(f"🚫 {a}")
    st.divider()
    if summary["conditions"]:
        st.markdown("#### Conditions for Use")
        for cond in summary["conditions"]:
            st.info(cond)
    st.markdown("#### Human Approval Required For")
    if summary["required_human_approval_for"]:
        for i, t in enumerate(summary["required_human_approval_for"], 1):
            st.markdown(f"{i}. {t}")
    else:
        st.markdown("_None specified_")
    st.divider()
    autonomy = p.data_contract.ai_usage_policy.max_autonomy_level
    st.markdown(f"**Max Autonomy Level:** {sbadge(autonomy)}", unsafe_allow_html=True)
    if autonomy == "read-only":
        st.warning(
            "This data product is approved for **read-only** AI consumption. "
            "AI agents may analyse and summarise but must not take actions without human approval."
        )
    consuming = [m for m in ai_models if p.id in m.input_data_products]
    if consuming:
        st.divider()
        st.markdown("#### AI Models Consuming This Product")
        for m in consuming:
            sc2 = product_scores[p.name]
            min_q = m.minimum_data_quality_score or 0
            ok = sc2 >= min_q
            mc1, mc2, mc3 = st.columns([3, 2, 2])
            mc1.markdown(f"**{m.name}**")
            mc2.markdown(sbadge(m.status), unsafe_allow_html=True)
            mc3.markdown("✅ Meets quality req." if ok else f"⚠️ Below required {min_q}")

# ════════════════════════════════════════════════════════════════════════════
# TAB 6 — Lineage
# ════════════════════════════════════════════════════════════════════════════
with tabs[5]:
    view_type = st.selectbox(
        "View",
        ["Product lineage", "Data mesh architecture", "Process maps"],
        key="lineage_view",
    )
    if view_type == "Product lineage":
        sel = st.selectbox("Select a product", list(product_map.keys()), key="lin_sel")
        p = product_map[sel]
        st.markdown(f"### Lineage: {p.name}")
        render_mermaid(generate_mermaid(p))
        st.divider()
        st.table(pd.DataFrame(
            [{"System": n.system_name, "Layer": n.layer, "Description": n.description}
             for n in p.lineage]
        ))
    elif view_type == "Data mesh architecture":
        st.markdown("### Data Mesh Architecture")
        render_mermaid(generate_mesh_diagram(), height=700)
    else:
        proc = st.selectbox("Select a process", ["Procure-to-Pay", "Maintenance & Reliability"], key="lin_proc")
        if proc == "Procure-to-Pay":
            render_mermaid(generate_p2p_process_map(), height=600)
        else:
            render_mermaid(generate_maintenance_process_map(), height=600)

# ════════════════════════════════════════════════════════════════════════════
# TAB 7 — Governance
# ════════════════════════════════════════════════════════════════════════════
with tabs[6]:
    # Governance health
    if products and users:
        mesh = mesh_principles_status(products, ai_models, users)
        st.markdown("### Governance Health")
        h1, h2, h3, h4 = st.columns(4)
        for col, (key, label) in zip(
            [h1, h2, h3, h4],
            [("domain_ownership", "Domain Ownership"),
             ("data_as_product", "Data as Product"),
             ("self_serve_platform", "Self-Serve Platform"),
             ("federated_governance", "Federated Governance")],
        ):
            col.metric(label, f"{mesh[key]['score']}/100")
            if mesh[key]["gaps"]:
                for g in mesh[key]["gaps"]:
                    col.caption(f"⚠ {g}")

    st.divider()
    with st.expander("🗺️ Data mesh architecture diagram"):
        render_mermaid(generate_mesh_diagram(), height=700)

    st.divider()
    st.markdown("### Users")
    if users:
        user_rows = []
        for u in users:
            perms = ", ".join(
                filter(None, [
                    "Data" if u.can_approve_data_products else "",
                    "AI" if u.can_approve_ai_models else "",
                    "API Keys" if u.can_generate_api_keys else "",
                ])
            )
            user_rows.append({
                "Name": u.name, "Role": u.role, "Department": u.department,
                "Domain": u.domain or "—", "Access": u.access_level,
                "Can Approve": perms or "—",
            })
        st.write(pd.DataFrame(user_rows).to_html(index=False, escape=False), unsafe_allow_html=True)
    else:
        st.info("No user data. Run `python generate_users.py` first.")

    st.divider()
    st.markdown("### API Keys")
    if api_keys:
        ak, ek = st.columns(2)
        ak.metric("Active", sum(1 for k in api_keys if k.status == "Active"))
        ek.metric("Expired / Revoked", sum(1 for k in api_keys if k.status != "Active"))
        key_rows = []
        for k in api_keys:
            name = user_map[k.issued_to].name if k.issued_to in user_map else k.issued_to
            key_rows.append({
                "Key": k.masked_key, "Resource": k.resource_id,
                "Issued To": name, "Status": sbadge(k.status),
                "Scope": k.scope, "Expires": k.expires_date, "Last Used": k.last_used or "—",
            })
        st.write(pd.DataFrame(key_rows).to_html(index=False, escape=False), unsafe_allow_html=True)

        active_k = [k for k in api_keys if k.status == "Active"]
        if active_k:
            st.markdown("#### Active Key Details")
            for k in active_k:
                issued_to = user_map[k.issued_to].name if k.issued_to in user_map else k.issued_to
                issued_by = user_map[k.issued_by].name if k.issued_by in user_map else k.issued_by
                with st.expander(f"{k.masked_key} — {k.resource_id}"):
                    st.markdown(f"**Key:** `{k.masked_key}`  |  **Scope:** {k.scope}  |  **Rate:** {k.rate_limit}")
                    st.markdown(f"**Issued to:** {issued_to}  |  **By:** {issued_by}")
                    st.markdown(f"**Issued:** {k.issued_date}  |  **Expires:** {k.expires_date}  |  **Last used:** {k.last_used or 'Never'}")

        st.divider()
        st.markdown("#### Request New API Key")
        with st.form("api_key_form"):
            resource_options = (
                [f"Data product: {p.name}" for p in products] +
                [f"AI model: {m.name}" for m in ai_models]
            )
            st.selectbox("Resource", resource_options)
            st.selectbox("Scope", ["read", "read-write"])
            st.text_area("Business justification")
            if st.form_submit_button("Submit Request"):
                st.success("API key request submitted for governance approval.")
                st.info("Requires Governance Lead or Platform Admin approval. Avg: 2 business days.")

    st.divider()
    st.markdown("### Approval Requests")
    if approval_requests:
        pending_reqs = [r for r in approval_requests if r.status == "Pending"]
        if pending_reqs:
            st.warning(f"⚠️ {len(pending_reqs)} pending request(s) require attention")
            for r in pending_reqs:
                req_by = user_map[r.requested_by].name if r.requested_by in user_map else r.requested_by
                st.markdown(f"- **{r.resource_name}** — by {req_by} on {r.requested_date} (needs: {r.approval_level_required})")

        st.divider()
        req_rows = []
        for r in approval_requests:
            req_by = user_map.get(r.requested_by)
            rev_by = user_map.get(r.reviewed_by or "")
            req_rows.append({
                "Type": r.request_type,
                "Resource": r.resource_name[:45] + ("…" if len(r.resource_name) > 45 else ""),
                "Requested By": req_by.name if req_by else r.requested_by,
                "Date": r.requested_date,
                "Status": sbadge(r.status),
                "Reviewed By": rev_by.name if rev_by else "—",
            })
        st.write(pd.DataFrame(req_rows).to_html(index=False, escape=False), unsafe_allow_html=True)
    else:
        st.info("No approval requests. Run `python generate_users.py` first.")

# ════════════════════════════════════════════════════════════════════════════
# TAB 8 — Process Maps
# ════════════════════════════════════════════════════════════════════════════
with tabs[7]:
    proc_sel = st.selectbox(
        "Select a process",
        ["Procure-to-Pay", "Maintenance & Reliability"],
        key="proc_sel",
    )
    if proc_sel == "Procure-to-Pay":
        st.markdown("### Procure-to-Pay Process Map")
        render_mermaid(generate_p2p_process_map(products, ai_models), height=600)
        st.divider()
        p2p_model_statuses = [model_map[n].status for n in ["Inventory Planning Assistant", "Supplier Risk Agent", "Contract Insights Assistant", "Procurement Anomaly Detector"] if n in model_map]
        summary_parts = [f"{sum(1 for s in p2p_model_statuses if s == sv)} {sv}" for sv in ["Production", "Staging", "Development"] if any(s == sv for s in p2p_model_statuses)]
        st.markdown(f"**3 data products** and **4 AI models** involved. Models: {' | '.join(summary_parts)}")
        st.table(pd.DataFrame([
            {"Data Product": "Inventory Availability Snapshot", "Step": "Need identification", "Role": "Stock level context"},
            {"Data Product": "Supplier Performance Summary", "Step": "Supplier selection / Review", "Role": "Performance scores"},
            {"Data Product": "Contract Spend History", "Step": "Purchase order / Invoice", "Role": "Contract & spend data"},
        ]))
        st.markdown("_🟩 Data products (teal) | 🟣 AI models (purple) | Dashed arrows = non-blocking contribution_")
    else:
        st.markdown("### Maintenance & Reliability Process Map")
        render_mermaid(generate_maintenance_process_map(products, ai_models), height=550)
        st.divider()
        mpa = model_map.get("Maintenance Planning Agent")
        st.markdown(
            f"**1 data product** (Maintenance Work Order History) and **1 AI model** "
            f"(Maintenance Planning Agent — {mpa.status if mpa else 'N/A'})."
        )
        st.markdown("⚠️ All AI outputs for safety-critical equipment require human review before action.")

# ── Footer ────────────────────────────────────────────────────────────────────────────
st.divider()
st.caption(
    "This platform uses fully synthetic data for portfolio demonstration purposes. "
    "Built by Mayowa Togun. "
    "[View source on GitHub](https://github.com/TMayowa/ai-ready-data-product-registry)"
)
