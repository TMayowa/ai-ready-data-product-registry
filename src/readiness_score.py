"""AI-readiness scoring engine.

Scores a DataProduct across 8 weighted dimensions (0-100 scale) and
produces an overall weighted total with a human-readable status.
"""

from __future__ import annotations

from src.models import DataProduct

# Weights for each dimension (must sum to 100%)
WEIGHTS: dict[str, float] = {
    "ownership": 0.15,
    "documentation": 0.10,
    "lineage": 0.15,
    "quality": 0.15,
    "access_rules": 0.10,
    "ai_usage_policy": 0.15,
    "freshness": 0.10,
    "human_escalation": 0.10,
}


def score_dimension(product: DataProduct, dimension: str) -> int:
    """Return a 0-100 score for a single dimension."""
    _dim = dimension.lower()

    if _dim == "ownership":
        score = 0
        if product.business_owner:
            score += 40
        if product.technical_owner:
            score += 30
        if product.data_steward:
            score += 30
        return score

    if _dim == "documentation":
        score = 0
        if product.description and len(product.description) > 50:
            score += 40
        if product.documentation_url is not None:
            score += 30
        if product.known_limitations:
            score += 30
        return score

    if _dim == "lineage":
        score = 0
        if len(product.lineage) >= 3:
            score += 40
        layers = {n.layer for n in product.lineage}
        if "source" in layers and "product" in layers:
            score += 30
        if "consumer" in layers:
            score += 30
        return score

    if _dim == "quality":
        rules = product.data_contract.quality_rules
        score = 0
        if len(rules) >= 1:
            score += 30
        if any(r.severity == "critical" for r in rules):
            score += 30
        if len(rules) >= 3:
            score += 40
        return score

    if _dim == "access_rules":
        score = 0
        if product.classification and product.classification != "Public":
            score += 50
        if len(product.data_contract.required_metadata_fields) >= 3:
            score += 50
        return score

    if _dim == "ai_usage_policy":
        policy = product.data_contract.ai_usage_policy
        score = 0
        if len(policy.permitted_uses) >= 2:
            score += 25
        if len(policy.prohibited_uses) >= 1:
            score += 25
        if len(policy.human_review_triggers) >= 1:
            score += 25
        if policy.max_autonomy_level != "full-autonomous":
            score += 25
        return score

    if _dim == "freshness":
        score = 0
        if product.refresh_frequency:
            score += 50
        if product.data_contract.freshness_sla:
            score += 50
        return score

    if _dim == "human_escalation":
        score = 0
        if len(product.data_contract.ai_usage_policy.human_review_triggers) >= 2:
            score += 50
        if product.data_contract.escalation_contact:
            score += 50
        return score

    raise ValueError(f"Unknown dimension: {dimension}")


def score_all_dimensions(product: DataProduct) -> dict[str, int]:
    """Return {"ownership": 85, "documentation": 60, ...} for all 8 dimensions."""
    dims = list(WEIGHTS.keys())
    return {d: score_dimension(product, d) for d in dims}


def overall_score(product: DataProduct) -> float:
    """Return weighted 0-100 overall score, rounded to 1 decimal."""
    dim_scores = score_all_dimensions(product)
    total = sum(WEIGHTS[d] * dim_scores[d] for d in dim_scores)
    return round(total, 1)


def readiness_status(score: float) -> str:
    """Return 'Ready', 'Conditionally ready', or 'Not ready'.

    - >= 80: Ready
    - >= 50: Conditionally ready
    -  < 50: Not ready
    """
    if score >= 80:
        return "Ready"
    if score >= 50:
        return "Conditionally ready"
    return "Not ready"


def gaps(product: DataProduct) -> list[str]:
    """Return human-readable list of gaps for improvement."""
    issues: list[str] = []

    # Ownership
    if not product.business_owner:
        issues.append("Missing business owner")
    if not product.technical_owner:
        issues.append("Missing technical owner")
    if not product.data_steward:
        issues.append("Missing data steward")

    # Documentation
    if not product.description or len(product.description) <= 50:
        issues.append("Description is too short (must exceed 50 characters)")
    if product.documentation_url is None:
        issues.append("Missing documentation URL")
    if not product.known_limitations:
        issues.append("No known limitations documented")

    # Lineage
    if len(product.lineage) < 3:
        issues.append(f"Lineage has only {len(product.lineage)} nodes (minimum 3 recommended)")
    layers = {n.layer for n in product.lineage}
    if "source" not in layers or "product" not in layers:
        issues.append("Lineage missing source or product layer")
    if "consumer" not in layers:
        issues.append("No consumer layer in lineage")

    # Quality
    rules = product.data_contract.quality_rules
    if not rules:
        issues.append("No quality rules defined")
    elif len(rules) < 3:
        issues.append(f"Only {len(rules)} quality rule(s) defined (minimum 3 recommended)")
    if not any(r.severity == "critical" for r in rules):
        issues.append("No critical-severity quality rules")

    # Access rules
    if product.classification == "Public":
        issues.append("Classification is 'Public' — consider restricting access")
    if len(product.data_contract.required_metadata_fields) < 3:
        issues.append("Fewer than 3 required metadata fields")

    # AI usage policy
    policy = product.data_contract.ai_usage_policy
    if len(policy.permitted_uses) < 2:
        issues.append("Fewer than 2 permitted AI uses defined")
    if not policy.prohibited_uses:
        issues.append("No prohibited AI uses defined")
    if not policy.human_review_triggers:
        issues.append("No human review triggers defined")
    if policy.max_autonomy_level == "full-autonomous":
        issues.append("Full autonomous access enabled — consider restricting autonomy")

    # Freshness
    if not product.refresh_frequency:
        issues.append("No refresh frequency set")
    if not product.data_contract.freshness_sla:
        issues.append("No freshness SLA defined")

    # Human escalation
    if len(policy.human_review_triggers) < 2:
        issues.append("Fewer than 2 human review triggers")
    if not product.data_contract.escalation_contact:
        issues.append("No escalation contact defined")

    return issues


__all__ = [
    "WEIGHTS",
    "score_dimension",
    "score_all_dimensions",
    "overall_score",
    "readiness_status",
    "gaps",
]
