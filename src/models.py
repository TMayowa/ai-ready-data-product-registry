"""Pydantic v2 data models for the AI-Ready Data & AI Governance Platform.

Contains models for: data products, AI models, users, API keys, and approval requests.
"""

from __future__ import annotations

from enum import Enum
from typing import Literal

from pydantic import BaseModel, ConfigDict


class QualityRule(BaseModel):
    """A data quality rule applied to a specific field in a data product."""

    model_config = ConfigDict(extra="forbid")

    field_name: str
    rule_description: str
    threshold: str
    severity: Literal["critical", "warning", "info"]


class LineageLayer(str, Enum):
    SOURCE = "source"
    RAW = "raw"
    CLEANED = "cleaned"
    PRODUCT = "product"
    CONSUMER = "consumer"


class LineageNode(BaseModel):
    """A node in a data product's lineage graph."""

    model_config = ConfigDict(extra="forbid")

    system_name: str
    layer: Literal["source", "raw", "cleaned", "product", "consumer"]
    description: str


class AutonomyLevel(str, Enum):
    READ_ONLY = "read-only"
    RECOMMEND = "recommend"
    ACT_WITH_APPROVAL = "act-with-approval"
    FULL_AUTONOMOUS = "full-autonomous"


class AIUsagePolicy(BaseModel):
    """Policy defining how AI agents may (and may not) use a data product."""

    model_config = ConfigDict(extra="forbid")

    permitted_uses: list[str]
    prohibited_uses: list[str]
    human_review_triggers: list[str]
    max_autonomy_level: Literal["read-only", "recommend", "act-with-approval", "full-autonomous"]


class DataContract(BaseModel):
    """A data contract specifying metadata, quality rules, freshness SLA,
    consumer lists, and AI usage policy for a data product."""

    model_config = ConfigDict(extra="forbid")

    contract_version: str
    last_reviewed: str
    consumers: list[str]
    ai_consumers: list[str]
    required_metadata_fields: list[str]
    quality_rules: list[QualityRule]
    freshness_sla: str
    ai_usage_policy: AIUsagePolicy
    escalation_contact: str


class Domain(str, Enum):
    PROCUREMENT = "Procurement"
    CONTRACT_MANAGEMENT = "Contract Management"
    OFFSHORE_LOGISTICS = "Offshore Logistics"
    MATERIALS_MANAGEMENT = "Materials Management"
    OPERATIONS = "Operations"


class Classification(str, Enum):
    PUBLIC = "Public"
    INTERNAL = "Internal"
    CONFIDENTIAL = "Confidential"
    RESTRICTED = "Restricted"


class RefreshFrequency(str, Enum):
    REAL_TIME = "Real-time"
    HOURLY = "Hourly"
    DAILY = "Daily"
    WEEKLY = "Weekly"
    MONTHLY = "Monthly"


class DataProduct(BaseModel):
    """Top-level model for a governed, documented, AI-ready data product."""

    model_config = ConfigDict(extra="ignore")

    # Core fields (v1)
    id: str
    name: str
    domain: Literal["Procurement", "Contract Management", "Offshore Logistics", "Materials Management", "Operations"]
    description: str
    business_owner: str
    technical_owner: str
    data_steward: str
    source_systems: list[str]
    classification: Literal["Public", "Internal", "Confidential", "Restricted"]
    refresh_frequency: Literal["Real-time", "Hourly", "Daily", "Weekly", "Monthly"]
    documentation_url: str | None = None
    lineage: list[LineageNode]
    data_contract: DataContract
    known_limitations: list[str]
    created_date: str
    last_updated: str

    # Extended metadata (v2)
    record_count: int | None = None
    size_mb: float | None = None
    schema_fields: list[dict] | None = None
    update_frequency_actual: str | None = None
    tags: list[str] = []
    related_products: list[str] = []
    domain_owner_team: str | None = None
    governance_status: Literal["Draft", "Under review", "Approved", "Deprecated"] = "Approved"
    data_sensitivity: str | None = None
    retention_policy: str | None = None

    # Usage and sharing metrics (v2)
    total_consumers: int = 0
    ai_consumers_count: int = 0
    api_calls_last_30_days: int = 0
    unique_users_last_30_days: int = 0
    data_shares_external: int = 0
    data_shares_internal: int = 0
    last_accessed: str | None = None
    popularity_rank: int | None = None

    # API access (v2)
    api_endpoint: str | None = None
    api_key_required: bool = True
    api_rate_limit: str | None = None
    api_documentation_url: str | None = None


# ── AI Model Registry ─────────────────────────────────────────────────────


class ModelEvaluation(BaseModel):
    """A single evaluation run for an AI model."""

    model_config = ConfigDict(extra="forbid")

    eval_id: str
    eval_date: str
    eval_type: Literal["accuracy", "fairness", "robustness", "latency", "governance_compliance", "data_quality_sensitivity"]
    dataset_used: str
    score: float
    passed: bool
    notes: str
    evaluated_by: str


class ModelOKR(BaseModel):
    """An OKR tied to an AI model's operational goals."""

    model_config = ConfigDict(extra="forbid")

    objective: str
    key_results: list[str]
    status: Literal["On track", "At risk", "Behind", "Achieved"]
    quarter: str
    progress_pct: int


class AIModel(BaseModel):
    """An AI model or agent registered in the governance platform."""

    model_config = ConfigDict(extra="ignore")

    id: str
    name: str
    model_type: Literal["Agent", "Predictive model", "Classification model", "NLP model", "Recommendation engine", "Anomaly detector"]
    description: str
    version: str
    status: Literal["Development", "Staging", "Production", "Deprecated", "Under review"]

    # Ownership and governance
    model_owner: str
    governance_lead: str
    owning_team: str
    domain: Literal["Procurement", "Contract Management", "Offshore Logistics", "Materials Management", "Operations", "Cross-domain"]
    governance_status: Literal["Draft", "Under review", "Approved", "Restricted", "Suspended"]
    risk_classification: Literal["Low", "Medium", "High", "Critical"]
    last_governance_review: str
    next_review_due: str

    # Technical details
    base_model: str | None = None
    framework: str | None = None
    infrastructure: str | None = None
    api_endpoint: str | None = None
    api_key_required: bool = True
    api_rate_limit: str | None = None

    # Data dependencies
    input_data_products: list[str]
    output_data_products: list[str] = []
    required_data_freshness: str | None = None
    minimum_data_quality_score: int | None = None

    # Process integration
    business_processes: list[str]
    process_step: str | None = None

    # Performance and usage
    evaluations: list[ModelEvaluation]
    okrs: list[ModelOKR]
    total_requests_last_30_days: int = 0
    avg_latency_ms: int | None = None
    error_rate_pct: float | None = None
    users_with_access: int = 0

    # Autonomy and controls
    max_autonomy_level: Literal["read-only", "recommend", "act-with-approval", "full-autonomous"]
    human_oversight_required: list[str]
    allowed_actions: list[str]
    prohibited_actions: list[str]
    escalation_rules: list[str]

    created_date: str
    last_updated: str


# ── Governance Models ─────────────────────────────────────────────────────


class User(BaseModel):
    """A platform user with a role and access level."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    email: str
    role: Literal[
        "Data Product Owner", "Data Steward", "AI Model Owner",
        "Governance Lead", "Data Consumer", "AI Consumer",
        "Platform Admin", "Domain Lead"
    ]
    department: str
    domain: str | None = None
    access_level: Literal["Viewer", "Contributor", "Approver", "Admin"]
    can_approve_data_products: bool = False
    can_approve_ai_models: bool = False
    can_generate_api_keys: bool = False
    active: bool = True


class APIKey(BaseModel):
    """An API key issued for a data product or AI model."""

    model_config = ConfigDict(extra="forbid")

    key_id: str
    masked_key: str
    resource_type: Literal["data_product", "ai_model"]
    resource_id: str
    issued_to: str
    issued_by: str
    issued_date: str
    expires_date: str
    status: Literal["Active", "Expired", "Revoked"]
    rate_limit: str
    scope: Literal["read", "read-write", "admin"]
    last_used: str | None = None


class ApprovalRequest(BaseModel):
    """A governance approval request for access or model deployment."""

    model_config = ConfigDict(extra="forbid")

    request_id: str
    request_type: Literal["Data product access", "AI model deployment", "API key generation", "Governance review", "Model promotion"]
    resource_id: str
    resource_name: str
    requested_by: str
    requested_date: str
    status: Literal["Pending", "Approved", "Rejected", "Escalated"]
    reviewed_by: str | None = None
    review_date: str | None = None
    review_notes: str | None = None
    approval_level_required: Literal["Domain Lead", "Governance Lead", "Platform Admin"]


__all__ = [
    "QualityRule", "LineageNode", "AIUsagePolicy", "DataContract", "DataProduct",
    "LineageLayer", "AutonomyLevel", "Domain", "Classification", "RefreshFrequency",
    "ModelEvaluation", "ModelOKR", "AIModel",
    "User", "APIKey", "ApprovalRequest",
]
