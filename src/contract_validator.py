"""Data contract validation engine.

Checks whether a DataContract is complete enough for production use
and for safe AI-agent consumption.
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict

from src.models import DataContract, DataProduct


class ValidationResult(BaseModel):
    """Result of validating a data contract."""

    model_config = ConfigDict(extra="forbid")

    is_valid: bool
    missing_fields: list[str]
    warnings: list[str]
    ai_consumption_allowed: bool
    ai_consumption_conditions: list[str]
    risk_level: Literal["low", "medium", "high"]


def validate_contract(contract: DataContract) -> ValidationResult:
    """Check completeness of a DataContract.

    A field is 'missing' if empty/None/empty-list.

    Required for basic validity:
    - contract_version
    - consumers (at least 1)
    - quality_rules (at least 1)
    - freshness_sla
    - escalation_contact

    Additionally required for AI consumption:
    - ai_consumers (at least 1)
    - ai_usage_policy.permitted_uses (at least 1)
    - ai_usage_policy.prohibited_uses (at least 1)
    - ai_usage_policy.human_review_triggers (at least 1)
    - ai_usage_policy.max_autonomy_level != "full-autonomous"
    - required_metadata_fields (at least 3)

    Risk level:
    - high: missing any basic validity field
    - medium: valid but missing AI consumption fields
    - low: all fields complete

    Warnings (non-blocking):
    - contract not reviewed in last 6 months
    - fewer than 3 quality rules
    - no prohibited AI uses defined
    """
    missing: list[str] = []
    ai_missing: list[str] = []
    warnings: list[str] = []

    # Basic validity checks
    if not contract.contract_version:
        missing.append("contract_version")
    if not contract.consumers:
        missing.append("consumers (at least 1 required)")
    if not contract.quality_rules:
        missing.append("quality_rules (at least 1 required)")
    if not contract.freshness_sla:
        missing.append("freshness_sla")
    if not contract.escalation_contact:
        missing.append("escalation_contact")

    # AI consumption checks
    if not contract.ai_consumers:
        ai_missing.append("ai_consumers (at least 1 required)")
    if not contract.ai_usage_policy.permitted_uses:
        ai_missing.append("ai_usage_policy.permitted_uses (at least 1 required)")
    if not contract.ai_usage_policy.prohibited_uses:
        ai_missing.append("ai_usage_policy.prohibited_uses (at least 1 required)")
    if not contract.ai_usage_policy.human_review_triggers:
        ai_missing.append("ai_usage_policy.human_review_triggers (at least 1 required)")
    if contract.ai_usage_policy.max_autonomy_level == "full-autonomous":
        ai_missing.append("max_autonomy_level must not be 'full-autonomous'")
    if len(contract.required_metadata_fields) < 3:
        ai_missing.append("required_metadata_fields (at least 3 required)")

    # Warnings (non-blocking)
    try:
        last_reviewed = datetime.fromisoformat(contract.last_reviewed)
        six_months_ago = datetime.now(tz=UTC) - timedelta(days=183)
        if last_reviewed.replace(tzinfo=UTC) < six_months_ago:
            warnings.append("Contract not reviewed in last 6 months")
    except (ValueError, TypeError):
        warnings.append("Unable to parse last_reviewed date")

    if len(contract.quality_rules) < 3:
        warnings.append(f"Only {len(contract.quality_rules)} quality rule(s) defined (minimum 3 recommended)")
    if not contract.ai_usage_policy.prohibited_uses:
        warnings.append("No prohibited AI uses defined")

    # Determine risk level
    is_valid = len(missing) == 0
    ai_allowed = is_valid and len(ai_missing) == 0

    if missing:
        risk_level = "high"
    elif ai_missing:
        risk_level = "medium"
    else:
        risk_level = "low"

    return ValidationResult(
        is_valid=is_valid,
        missing_fields=missing + ai_missing,
        warnings=warnings,
        ai_consumption_allowed=ai_allowed,
        ai_consumption_conditions=ai_missing if not ai_allowed else [],
        risk_level=risk_level,
    )


def ai_consumer_summary(product: DataProduct) -> dict:
    """Return a dict summarising whether an AI agent can consume this product.

    Returns:
        {
            "can_consume": bool,
            "status": "Approved" | "Conditional" | "Blocked",
            "permitted_actions": [...],
            "prohibited_actions": [...],
            "conditions": [...],
            "required_human_approval_for": [...]
        }
    """
    vr = validate_contract(product.data_contract)
    policy = product.data_contract.ai_usage_policy

    can_consume = vr.ai_consumption_allowed or vr.risk_level == "medium"

    if vr.ai_consumption_allowed:
        status = "Approved"
    elif vr.risk_level == "medium" and vr.is_valid:
        status = "Conditional"
    else:
        status = "Blocked"

    return {
        "can_consume": can_consume,
        "status": status,
        "permitted_actions": list(policy.permitted_uses),
        "prohibited_actions": list(policy.prohibited_uses),
        "conditions": vr.missing_fields,
        "required_human_approval_for": list(policy.human_review_triggers),
    }


__all__ = ["ValidationResult", "validate_contract", "ai_consumer_summary"]
