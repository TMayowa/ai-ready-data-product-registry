"""Data mesh architecture diagrams and domain analysis.

Provides Mermaid diagrams, domain summaries, and mesh principles assessment.
"""

from __future__ import annotations

from src.readiness_score import overall_score


def generate_mesh_diagram() -> str:
    """Return a Mermaid graph TB showing the full data mesh architecture."""
    return """graph TB
    subgraph platform["Self-Serve Data Platform"]
        GOV["Federated Governance<br/><small>Standards, Policies, Quality Gates</small>"]
        CAT["Data Catalogue<br/><small>Discovery, Metadata, Lineage</small>"]
        AI_REG["AI Model Registry<br/><small>Models, Evaluations, Controls</small>"]
    end

    subgraph procurement_domain["Procurement Domain"]
        SP["Supplier Performance<br/>Summary"]
        SRA["Supplier Risk<br/>Agent"]
        PAD["Procurement Anomaly<br/>Detector"]
    end

    subgraph contract_domain["Contract Management Domain"]
        CS["Contract Spend<br/>History"]
        CIA["Contract Insights<br/>Assistant"]
    end

    subgraph logistics_domain["Offshore Logistics Domain"]
        LD["Logistics Delay<br/>Events"]
        LDA["Logistics Disruption<br/>Agent"]
    end

    subgraph materials_domain["Materials Management Domain"]
        IA["Inventory Availability<br/>Snapshot"]
        IPA["Inventory Planning<br/>Assistant"]
    end

    subgraph operations_domain["Operations Domain"]
        MW["Maintenance Work Order<br/>History"]
        MPA["Maintenance Planning<br/>Agent"]
    end

    GOV -.-> procurement_domain
    GOV -.-> contract_domain
    GOV -.-> logistics_domain
    GOV -.-> materials_domain
    GOV -.-> operations_domain

    SP --> SRA
    SP --> PAD
    CS --> CIA
    CS --> PAD
    LD --> LDA
    IA --> IPA
    IA --> LDA
    MW --> MPA

    style platform fill:#E6F1FB,stroke:#185FA5,color:#042C53
    style procurement_domain fill:#FAEEDA,stroke:#854F0B,color:#412402
    style contract_domain fill:#EEEDFE,stroke:#534AB7,color:#26215C
    style logistics_domain fill:#E1F5EE,stroke:#0F6E56,color:#04342C
    style materials_domain fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A
    style operations_domain fill:#FAECE7,stroke:#993C1D,color:#4A1B0C"""


def domain_summary(data_products: list, ai_models: list) -> list[dict]:
    """Return a summary for each domain showing products, models, avg readiness, and maturity."""
    domain_order = [
        "Procurement", "Contract Management", "Offshore Logistics",
        "Materials Management", "Operations"
    ]
    summaries = []
    for domain in domain_order:
        prods = [p for p in data_products if p.domain == domain]
        models = [m for m in ai_models if m.domain == domain]
        if not prods:
            continue
        scores = [overall_score(p) for p in prods]
        avg = sum(scores) / len(scores) if scores else 0
        all_approved = all(p.governance_status == "Approved" for p in prods)
        most_approved = sum(1 for p in prods if p.governance_status == "Approved") >= len(prods) * 0.5
        if avg >= 90 and all_approved:
            maturity = "Optimising"
        elif avg >= 75 and most_approved:
            maturity = "Measured"
        else:
            maturity = "Managed"
        domain_owner_team = prods[0].domain_owner_team if prods else None
        summaries.append({
            "domain": domain,
            "domain_owner": domain_owner_team or f"{domain} Team",
            "data_products": [p.name for p in prods],
            "ai_models": [m.name for m in models],
            "avg_readiness_score": round(avg, 1),
            "governance_principle": "Domain-owned, federated governance",
            "maturity_level": maturity,
        })
    return summaries


def mesh_principles_status(data_products: list, ai_models: list, users: list) -> dict:
    """Assess how well the 4 data mesh principles are implemented."""

    # 1. Domain ownership
    with_team = sum(1 for p in data_products if p.domain_owner_team)
    domain_score = int((with_team / max(len(data_products), 1)) * 100)
    domain_gaps = []
    if with_team < len(data_products):
        domain_gaps.append(f"{len(data_products) - with_team} products missing domain owner team")
    with_steward = sum(1 for p in data_products if p.data_steward)
    if with_steward < len(data_products):
        domain_gaps.append(f"{len(data_products) - with_steward} products missing data steward")

    # 2. Data as a product
    with_contract = sum(1 for p in data_products if p.data_contract.contract_version)
    with_api = sum(1 for p in data_products if p.api_endpoint)
    with_docs = sum(1 for p in data_products if p.documentation_url)
    product_score = int(((with_contract + with_api + with_docs) / (3 * max(len(data_products), 1))) * 100)
    product_gaps = []
    if with_docs < len(data_products):
        product_gaps.append(f"{len(data_products) - with_docs} products missing documentation URL")
    approved_count = sum(1 for p in data_products if p.governance_status == "Approved")
    if approved_count < len(data_products):
        product_gaps.append(f"{len(data_products) - approved_count} products not yet Approved")

    # 3. Self-serve platform
    api_count = sum(1 for p in data_products if p.api_endpoint)
    key_users = len(set(k for k in ["USR-008", "USR-009", "USR-010"] if any(u.id in ["USR-008","USR-009","USR-010"] for u in users)))
    platform_score = min(100, int((api_count / max(len(data_products), 1)) * 70 + (len(users) / 10) * 30))
    platform_gaps = []
    platform_gaps.append(f"No automated data quality monitoring — gaps detected manually only")
    platform_gaps.append(f"No self-service data access portal — API key requests require manual approval")

    # 4. Federated governance
    with_policy = sum(1 for p in data_products if p.data_contract.ai_usage_policy.prohibited_uses)
    approvers = sum(1 for u in users if u.can_approve_data_products or u.can_approve_ai_models)
    governance_score = int(((with_policy / max(len(data_products), 1)) * 60 + (approvers / max(len(users), 1)) * 40) * 100)
    governance_score = min(governance_score, 95)
    governance_gaps = []
    freshness_missing = sum(1 for p in data_products if not p.data_contract.freshness_sla)
    if freshness_missing:
        governance_gaps.append(f"{freshness_missing} contracts missing freshness SLA")
    escalation_missing = sum(1 for p in data_products if not p.data_contract.escalation_contact)
    if escalation_missing:
        governance_gaps.append(f"{escalation_missing} contracts missing escalation contact")

    return {
        "domain_ownership": {
            "score": domain_score,
            "evidence": f"{with_team}/{len(data_products)} products have named domain owner teams",
            "gaps": domain_gaps,
        },
        "data_as_product": {
            "score": product_score,
            "evidence": f"{with_contract}/{len(data_products)} have contracts, {with_api}/{len(data_products)} have APIs, {with_docs}/{len(data_products)} have docs",
            "gaps": product_gaps,
        },
        "self_serve_platform": {
            "score": platform_score,
            "evidence": f"API endpoints defined for {api_count}/{len(data_products)} products",
            "gaps": platform_gaps,
        },
        "federated_governance": {
            "score": governance_score,
            "evidence": f"{with_policy}/{len(data_products)} contracts have AI usage policies, {approvers} users with approval rights",
            "gaps": governance_gaps,
        },
    }


__all__ = ["generate_mesh_diagram", "domain_summary", "mesh_principles_status"]
