"""Pydantic v2 data models for an enterprise data product registry.

Defines the core entities for governed, documented data products with
clear ownership, quality rules, lineage, and AI usage policies.
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
    """Top-level model representing a governed, documented data product
    that can be assessed for AI-readiness."""

    model_config = ConfigDict(extra="forbid")

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


__all__ = [
    "QualityRule",
    "LineageNode",
    "AIUsagePolicy",
    "DataContract",
    "DataProduct",
    "LineageLayer",
    "AutonomyLevel",
    "Domain",
    "Classification",
    "RefreshFrequency",
]
