"""Synthetic data generator for the AI-Ready Data & AI Governance Platform.

Generates 5 realistic data products with deliberate imperfections to demonstrate
realistic governance gaps. Validates through Pydantic models before saving.
"""

import json
import os
from datetime import UTC, datetime

from faker import Faker

from src.models import (
    AIUsagePolicy,
    DataContract,
    DataProduct,
    LineageNode,
    QualityRule,
)
from src.readiness_score import overall_score, gaps

fake = Faker(["no_NO"])  # Norwegian locale for realistic names


def _random_date(start_year: int, end_year: int) -> str:
    """Return an ISO-format date string between start_year and end_year."""
    start = datetime(start_year, 1, 1, tzinfo=UTC)
    end = datetime(end_year, 12, 31, tzinfo=UTC)
    return fake.date_between(start, end).isoformat()


def _generate_products() -> list[DataProduct]:
    """Build and return 5 validated DataProduct instances with realistic imperfections."""

    business_owners = [fake.name() for _ in range(5)]
    technical_owners = [fake.name() for _ in range(5)]
    data_stewards = [fake.name() for _ in range(5)]

    products: list[DataProduct] = []

    # ── 1. Supplier Performance Summary ──────────────────────────────────
    # IMPERFECTION: documentation_url is None (gap: "Missing documentation URL")
    products.append(
        DataProduct(
            id="DP-001",
            name="Supplier Performance Summary",
            domain="Procurement",
            description=(
                "Aggregated supplier performance data including delivery precision, "
                "quality compliance, safety record, and responsiveness metrics. "
                "Enables trend analysis, benchmarking across supplier tiers, and "
                "early risk flagging for procurement managers and AI agents."
            ),
            business_owner=business_owners[0],
            technical_owner=technical_owners[0],
            data_steward=data_stewards[0],
            source_systems=["SAP S/4HANA", "Supplier Portal"],
            classification="Internal",
            refresh_frequency="Daily",
            documentation_url=None,  # GAP: missing documentation URL
            lineage=[
                LineageNode(
                    system_name="SAP ERP",
                    layer="source",
                    description="Core ERP system holding supplier master data and transaction records.",
                ),
                LineageNode(
                    system_name="Raw supplier transactions",
                    layer="raw",
                    description="Unprocessed supplier delivery and quality data from SAP S/4HANA.",
                ),
                LineageNode(
                    system_name="Cleaned supplier metrics",
                    layer="cleaned",
                    description="Standardised supplier scores with deduplication and outlier removal.",
                ),
                LineageNode(
                    system_name="Supplier Performance Summary",
                    layer="product",
                    description="Final aggregated product with KPI dashboards and trend indicators.",
                ),
                LineageNode(
                    system_name="Power BI dashboard",
                    layer="consumer",
                    description="Visual reporting layer for procurement analysts and managers.",
                ),
                LineageNode(
                    system_name="Supplier Risk Agent",
                    layer="consumer",
                    description="AI agent consuming performance data for risk assessment and recommendations.",
                ),
            ],
            data_contract=DataContract(
                contract_version="v2.1",
                last_reviewed=_random_date(2025, 2026),
                consumers=["Procurement Management", "Category Managers"],
                ai_consumers=["Supplier Risk Agent"],
                required_metadata_fields=[
                    "supplier_id",
                    "evaluation_period",
                    "evaluation_type",
                    "assessor_id",
                ],
                quality_rules=[
                    QualityRule(
                        field_name="supplier_id",
                        rule_description="Supplier identifier must be present for every record",
                        threshold="not null",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="performance_score",
                        rule_description="Score must fall within the valid range",
                        threshold="between 0 and 100",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="last_evaluation_date",
                        rule_description="Evaluation date must be current",
                        threshold="within 12 months",
                        severity="warning",
                    ),
                ],
                freshness_sla="24 hours from source system load",
                ai_usage_policy=AIUsagePolicy(
                    permitted_uses=[
                        "summarisation",
                        "trend detection",
                        "risk flagging",
                        "recommendation drafting",
                    ],
                    prohibited_uses=[
                        "autonomous supplier decisions",
                        "contractual commitments",
                        "safety-critical actions",
                    ],
                    human_review_triggers=[
                        "confidence below 80%",
                        "source freshness exceeds SLA",
                        "involves restricted suppliers",
                        "recommendation affects contract value above NOK 5M",
                    ],
                    max_autonomy_level="recommend",
                ),
                escalation_contact="procurement.governance@energycomp.com",
            ),
            known_limitations=[
                "does not include sub-tier supplier data",
                "performance scores lag by 1 business day",
            ],
            created_date=_random_date(2023, 2024),
            last_updated=_random_date(2025, 2026),
            # Extended metadata
            record_count=12400,
            size_mb=45.2,
            update_frequency_actual="Last refreshed 18 hours ago",
            tags=["procurement", "supplier", "performance", "kpi", "risk"],
            related_products=["DP-002"],
            domain_owner_team="Procurement Performance & Analytics",
            governance_status="Approved",
            total_consumers=34,
            ai_consumers_count=3,
            api_calls_last_30_days=8420,
            unique_users_last_30_days=28,
            data_shares_internal=12,
            data_shares_external=2,
            last_accessed="2026-05-27",
            popularity_rank=2,
            api_endpoint="/api/v2/data-products/supplier-performance-summary",
            api_key_required=True,
            api_rate_limit="1000 requests/hour",
            api_documentation_url="https://data-platform.internal/docs/supplier-performance-summary",
            schema_fields=[
                {"name": "supplier_id", "type": "VARCHAR(20)", "nullable": False, "description": "Unique supplier identifier"},
                {"name": "supplier_name", "type": "VARCHAR(200)", "nullable": False, "description": "Legal supplier name"},
                {"name": "performance_score", "type": "DECIMAL(5,2)", "nullable": False, "description": "Overall performance score 0-100"},
                {"name": "last_evaluation_date", "type": "DATE", "nullable": False, "description": "Date of last formal evaluation"},
                {"name": "region", "type": "VARCHAR(50)", "nullable": True, "description": "Supplier primary operating region"},
                {"name": "category", "type": "VARCHAR(100)", "nullable": True, "description": "Procurement category"},
                {"name": "risk_rating", "type": "VARCHAR(10)", "nullable": True, "description": "Risk rating: Low/Medium/High/Critical"},
                {"name": "contract_count", "type": "INTEGER", "nullable": True, "description": "Number of active contracts"},
            ],
        )
    )

    # ── 2. Contract Spend History ───────────────────────────────────────
    # IMPERFECTIONS: data_steward empty, contract reviewed 8 months ago, only 2 quality rules
    products.append(
        DataProduct(
            id="DP-002",
            name="Contract Spend History",
            domain="Contract Management",
            description=(
                "Historical spend data across all active contracts including "
                "commitment tracking, actual vs. forecast comparisons, and "
                "vendor-level spend aggregation. Supports spend pattern analysis "
                "and anomaly detection by human analysts and AI assistants."
            ),
            business_owner=business_owners[1],
            technical_owner=technical_owners[1],
            data_steward="",  # GAP: no data steward assigned
            source_systems=["SAP S/4HANA", "Contract Management Platform"],
            classification="Confidential",
            refresh_frequency="Weekly",
            documentation_url=None,  # GAP: no documentation URL
            lineage=[
                LineageNode(
                    system_name="SAP ERP + Contract Platform",
                    layer="source",
                    description="ERP and contract management systems producing transaction records.",
                ),
                LineageNode(
                    system_name="Raw contract transactions",
                    layer="raw",
                    description="Unprocessed spend entries from SAP and the contract platform.",
                ),
                LineageNode(
                    system_name="Cleaned spend records",
                    layer="cleaned",
                    description="Validated, currency-normalised spend entries with vendor mapping.",
                ),
                LineageNode(
                    system_name="Contract Spend History",
                    layer="product",
                    description="Aggregated spend product with contract-level and vendor-level views.",
                ),
                LineageNode(
                    system_name="Finance reporting",
                    layer="consumer",
                    description="Standard financial reporting and budget tracking dashboards.",
                ),
                LineageNode(
                    system_name="Contract Insights Assistant",
                    layer="consumer",
                    description="AI assistant for spend pattern analysis and utilisation reporting.",
                ),
            ],
            data_contract=DataContract(
                contract_version="v1.4",
                last_reviewed="2025-09-15",  # GAP: reviewed 8 months ago, outside 6-month policy
                consumers=["Contract Management", "Finance Department"],
                ai_consumers=["Contract Insights Assistant"],
                required_metadata_fields=[
                    "contract_id",
                    "spend_amount",
                    "currency_code",
                    "vendor_id",
                    "transaction_date",
                ],
                quality_rules=[
                    QualityRule(
                        field_name="contract_id",
                        rule_description="Every record must be linked to a valid contract",
                        threshold="not null",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="spend_amount",
                        rule_description="Amount must be non-negative",
                        threshold=">= 0",
                        severity="critical",
                    ),
                    # GAP: only 2 quality rules (minimum 3 recommended)
                ],
                freshness_sla="7 days from source system load",
                ai_usage_policy=AIUsagePolicy(
                    permitted_uses=[
                        "spend pattern analysis",
                        "anomaly detection",
                        "contract utilisation reporting",
                    ],
                    prohibited_uses=[
                        "contract amendments",
                        "payment authorisations",
                        "vendor selection decisions",
                    ],
                    human_review_triggers=[
                        "anomaly flagged on contracts above NOK 10M",
                        "spend deviates more than 25% from forecast",
                        "involves new vendors not in master",
                    ],
                    max_autonomy_level="read-only",
                ),
                escalation_contact="contract.governance@energycomp.com",
            ),
            known_limitations=[
                "historical data before 2020 may have inconsistent currency conversion",
                "multi-year framework agreements not fully decomposed",
            ],
            created_date=_random_date(2023, 2024),
            last_updated=_random_date(2025, 2026),
            # Extended metadata
            record_count=87000,
            size_mb=312.7,
            tags=["contracts", "spend", "finance", "procurement", "vendor"],
            related_products=["DP-001", "DP-004"],
            domain_owner_team="Contract Management & Commercial",
            governance_status="Under review",
            data_sensitivity="Contains commercially sensitive contract values and vendor pricing",
            total_consumers=18,
            ai_consumers_count=1,
            api_calls_last_30_days=2100,
            unique_users_last_30_days=12,
            data_shares_internal=6,
            data_shares_external=0,
            last_accessed="2026-05-26",
            popularity_rank=4,
            api_endpoint="/api/v2/data-products/contract-spend-history",
            api_key_required=True,
            api_rate_limit="500 requests/hour",
            api_documentation_url="https://data-platform.internal/docs/contract-spend-history",
        )
    )

    # ── 3. Logistics Delay Events ───────────────────────────────────────
    products.append(
        DataProduct(
            id="DP-003",
            name="Logistics Delay Events",
            domain="Offshore Logistics",
            description=(
                "Real-time and historical logistics delay events for offshore "
                "operations including vessel delays, weather-related disruptions, "
                "and root cause data. Supports operations dashboards and AI-driven "
                "delay pattern analysis and ETA prediction."
            ),
            business_owner=business_owners[2],
            technical_owner=technical_owners[2],
            data_steward=data_stewards[2],
            source_systems=["Logistics Management System", "Vessel Tracking", "Weather API"],
            classification="Internal",
            refresh_frequency="Hourly",
            documentation_url=None,
            lineage=[
                LineageNode(
                    system_name="Logistics System + Vessel AIS + Met.no Weather",
                    layer="source",
                    description="Combined data from logistics systems, vessel transponders, and weather service.",
                ),
                LineageNode(
                    system_name="Raw delay events",
                    layer="raw",
                    description="Unprocessed delay event records with vessel positions and weather data.",
                ),
                LineageNode(
                    system_name="Enriched delay events (weather, root cause)",
                    layer="cleaned",
                    description="Delay events enriched with weather context and initial root cause coding.",
                ),
                LineageNode(
                    system_name="Logistics Delay Events",
                    layer="product",
                    description="Final product with delay KPIs, trend analysis, and disruption indicators.",
                ),
                LineageNode(
                    system_name="Operations dashboard",
                    layer="consumer",
                    description="Real-time logistics monitoring for operations centre.",
                ),
                LineageNode(
                    system_name="Logistics Disruption Agent",
                    layer="consumer",
                    description="AI agent for delay pattern analysis, root cause clustering, and ETA prediction.",
                ),
            ],
            data_contract=DataContract(
                contract_version="v1.3",
                last_reviewed=_random_date(2025, 2026),
                consumers=["Offshore Operations", "Supply Chain"],
                ai_consumers=["Logistics Disruption Agent"],
                required_metadata_fields=[
                    "event_id",
                    "vessel_id",
                    "delay_minutes",
                    "root_cause_code",
                    "weather_severity",
                ],
                quality_rules=[
                    QualityRule(
                        field_name="event_id",
                        rule_description="Every delay event must have a unique identifier",
                        threshold="not null",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="delay_minutes",
                        rule_description="Delay duration must be non-negative",
                        threshold=">= 0",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="root_cause_code",
                        rule_description="Root cause must belong to approved taxonomy",
                        threshold="in approved taxonomy",
                        severity="warning",
                    ),
                    QualityRule(
                        field_name="vessel_id",
                        rule_description="Vessel must exist in fleet register",
                        threshold="maps to fleet register",
                        severity="critical",
                    ),
                ],
                freshness_sla="2 hours from source system load",
                ai_usage_policy=AIUsagePolicy(
                    permitted_uses=[
                        "delay pattern analysis",
                        "root cause clustering",
                        "ETA prediction",
                        "disruption alerting",
                    ],
                    prohibited_uses=[
                        "vessel rerouting decisions",
                        "safety-critical operational changes",
                        "crew scheduling modifications",
                    ],
                    human_review_triggers=[
                        "delay exceeds 48 hours",
                        "involves personnel transfer operations",
                        "weather severity above threshold",
                        "multiple cascading delays detected",
                    ],
                    max_autonomy_level="recommend",
                ),
                escalation_contact="logistics.ops@energycomp.com",
            ),
            known_limitations=[
                "weather correlation is best-effort and may lag 2 hours",
                "root cause coding depends on manual operator input — approximately 15% of events have unclassified root cause",
            ],
            created_date=_random_date(2023, 2024),
            last_updated=_random_date(2025, 2026),
            # Extended metadata
            record_count=34200,
            size_mb=28.9,
            tags=["logistics", "offshore", "delays", "operations", "vessel", "weather"],
            related_products=["DP-004"],
            domain_owner_team="Offshore Logistics & Supply Chain",
            governance_status="Approved",
            total_consumers=22,
            ai_consumers_count=2,
            api_calls_last_30_days=5600,
            unique_users_last_30_days=19,
            data_shares_internal=8,
            data_shares_external=1,
            last_accessed="2026-05-27",
            popularity_rank=3,
            api_endpoint="/api/v2/data-products/logistics-delay-events",
            api_key_required=True,
            api_rate_limit="2000 requests/hour",
            api_documentation_url="https://data-platform.internal/docs/logistics-delay-events",
        )
    )

    # ── 4. Inventory Availability Snapshot ──────────────────────────────
    # IMPERFECTIONS: data_steward empty, escalation_contact empty, freshness_sla empty
    products.append(
        DataProduct(
            id="DP-004",
            name="Inventory Availability Snapshot",
            domain="Materials Management",
            description=(
                "Daily snapshot of inventory positions across all warehouses "
                "including stock quantities, reorder points, and critical item "
                "flags. Enables stock-level forecasting, consumption trend "
                "analysis, and planning support."
            ),
            business_owner=business_owners[3],
            technical_owner=technical_owners[3],
            data_steward="",  # GAP: no data steward assigned
            source_systems=["SAP MM", "Warehouse Management System"],
            classification="Internal",
            refresh_frequency="Daily",
            documentation_url=None,  # GAP: no documentation URL
            lineage=[
                LineageNode(
                    system_name="SAP MM + WMS",
                    layer="source",
                    description="Material master and warehouse management systems as data sources.",
                ),
                LineageNode(
                    system_name="Raw stock movements",
                    layer="raw",
                    description="Unprocessed material movements and stock adjustments.",
                ),
                LineageNode(
                    system_name="Cleaned inventory positions",
                    layer="cleaned",
                    description="Validated inventory records with warehouse reconciliation.",
                ),
                LineageNode(
                    system_name="Inventory Availability Snapshot",
                    layer="product",
                    description="Daily snapshot product with stock KPIs and trend indicators.",
                ),
                LineageNode(
                    system_name="Planning dashboard",
                    layer="consumer",
                    description="Operational planning dashboard for materials planners.",
                ),
                LineageNode(
                    system_name="Inventory Planning Assistant",
                    layer="consumer",
                    description="AI agent for stock forecasting and reorder recommendations.",
                ),
            ],
            data_contract=DataContract(
                contract_version="v1.2",
                last_reviewed=_random_date(2025, 2026),
                consumers=["Materials Management", "Planning"],
                ai_consumers=["Inventory Planning Assistant"],
                required_metadata_fields=[
                    "material_id",
                    "stock_quantity",
                    "location_code",
                    "reorder_point",
                ],
                quality_rules=[
                    QualityRule(
                        field_name="material_id",
                        rule_description="Every record must have a valid material identifier",
                        threshold="not null",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="stock_quantity",
                        rule_description="Quantity must be non-negative",
                        threshold=">= 0",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="location_code",
                        rule_description="Warehouse code must be in the approved list",
                        threshold="in approved warehouse list",
                        severity="warning",
                    ),
                    QualityRule(
                        field_name="reorder_point",
                        rule_description="Reorder point must be defined for critical items",
                        threshold="defined for critical items",
                        severity="warning",
                    ),
                ],
                freshness_sla="",  # GAP: no freshness SLA defined
                ai_usage_policy=AIUsagePolicy(
                    permitted_uses=[
                        "stock level forecasting",
                        "reorder recommendations",
                        "consumption trend analysis",
                    ],
                    prohibited_uses=[
                        "automatic purchase order creation",
                        "safety stock overrides",
                        "warehouse allocation changes",
                    ],
                    human_review_triggers=[
                        "critical spare part below safety stock",
                        "forecast deviation above 30%",
                    ],
                    max_autonomy_level="recommend",
                ),
                escalation_contact="",  # GAP: no escalation contact
            ),
            known_limitations=[
                "does not capture in-transit inventory in real time",
                "consignment stock not fully reflected",
            ],
            created_date=_random_date(2023, 2024),
            last_updated=_random_date(2025, 2026),
            # Extended metadata
            record_count=156000,
            size_mb=89.4,
            tags=["inventory", "materials", "warehouse", "stock", "planning"],
            related_products=["DP-003"],
            domain_owner_team="Materials Management & Warehousing",
            governance_status="Draft",
            total_consumers=41,
            ai_consumers_count=2,
            api_calls_last_30_days=12300,
            unique_users_last_30_days=38,
            data_shares_internal=15,
            data_shares_external=0,
            last_accessed="2026-05-25",
            popularity_rank=1,
            api_endpoint="/api/v2/data-products/inventory-availability-snapshot",
            api_key_required=True,
            api_rate_limit="2000 requests/hour",
            api_documentation_url="https://data-platform.internal/docs/inventory-availability-snapshot",
        )
    )

    # ── 5. Maintenance Work Order History ───────────────────────────────
    # IMPERFECTION: lineage missing 'cleaned' layer (source -> raw -> product)
    products.append(
        DataProduct(
            id="DP-005",
            name="Maintenance Work Order History",
            domain="Operations",
            description=(
                "Historical maintenance work orders with equipment linkage, "
                "failure coding, IoT sensor context, and completion details. "
                "Supports reliability dashboards, predictive maintenance "
                "indicators, and backlog prioritisation."
            ),
            business_owner=business_owners[4],
            technical_owner=technical_owners[4],
            data_steward=data_stewards[4],
            source_systems=["SAP PM", "Inspection Database", "IoT Sensor Platform"],
            classification="Restricted",
            refresh_frequency="Daily",
            documentation_url="https://docs.internal.energycomp.com/data/maintenance-history",
            lineage=[
                LineageNode(
                    system_name="SAP PM + Inspections + IoT Sensors",
                    layer="source",
                    description="Maintenance, inspection, and IoT sensor systems as data sources.",
                ),
                LineageNode(
                    system_name="Raw work orders",
                    layer="raw",
                    description="Unprocessed maintenance work order records.",
                ),
                # NOTE: 'cleaned' layer intentionally missing — gap in lineage documentation
                LineageNode(
                    system_name="Maintenance Work Order History",
                    layer="product",
                    description="Final product with reliability indicators and predictive maintenance features.",
                ),
                LineageNode(
                    system_name="Reliability dashboard",
                    layer="consumer",
                    description="Operational reliability monitoring for maintenance engineers.",
                ),
                LineageNode(
                    system_name="Maintenance Planning Agent",
                    layer="consumer",
                    description="AI agent for pattern analysis, predictive indicators, and backlog prioritisation.",
                ),
            ],
            data_contract=DataContract(
                contract_version="v2.0",
                last_reviewed=_random_date(2025, 2026),
                consumers=["Maintenance Engineering", "Operations"],
                ai_consumers=["Maintenance Planning Agent"],
                required_metadata_fields=[
                    "work_order_id",
                    "equipment_id",
                    "failure_code",
                    "completion_date",
                    "creation_date",
                ],
                quality_rules=[
                    QualityRule(
                        field_name="work_order_id",
                        rule_description="Every work order must have a unique identifier",
                        threshold="not null",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="equipment_id",
                        rule_description="Equipment must exist in the asset register",
                        threshold="maps to asset register",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="failure_code",
                        rule_description="Failure code must belong to approved taxonomy",
                        threshold="in approved taxonomy",
                        severity="critical",
                    ),
                    QualityRule(
                        field_name="completion_date",
                        rule_description="Completion date must not precede creation date",
                        threshold="not before creation_date",
                        severity="critical",
                    ),
                ],
                freshness_sla="24 hours from source system load",
                ai_usage_policy=AIUsagePolicy(
                    permitted_uses=[
                        "failure pattern analysis",
                        "predictive maintenance indicators",
                        "maintenance backlog prioritisation",
                    ],
                    prohibited_uses=[
                        "maintenance schedule changes on safety-critical equipment",
                        "inspection interval modifications",
                        "compliance record alterations",
                    ],
                    human_review_triggers=[
                        "involves safety-critical equipment class",
                        "predicted failure within 7 days",
                        "work order cost above NOK 2M",
                        "regulatory inspection linked",
                    ],
                    max_autonomy_level="read-only",
                ),
                escalation_contact="maintenance.governance@energycomp.com",
            ),
            known_limitations=[
                "IoT sensor coverage is 60% of monitored assets",
                "historical work orders before 2019 have incomplete failure coding",
                "lineage documentation incomplete — transformation layer not documented",
            ],
            created_date=_random_date(2023, 2024),
            last_updated=_random_date(2025, 2026),
            # Extended metadata
            record_count=245000,
            size_mb=567.3,
            tags=["maintenance", "operations", "safety", "reliability", "equipment", "iot"],
            related_products=[],
            domain_owner_team="Asset Integrity & Reliability Engineering",
            governance_status="Approved",
            data_sensitivity="Contains safety-critical equipment maintenance records subject to regulatory audit",
            retention_policy="10 years per offshore safety regulatory requirement",
            total_consumers=15,
            ai_consumers_count=1,
            api_calls_last_30_days=890,
            unique_users_last_30_days=8,
            data_shares_internal=3,
            data_shares_external=0,
            last_accessed="2026-05-26",
            popularity_rank=5,
            api_endpoint="/api/v2/data-products/maintenance-work-order-history",
            api_key_required=True,
            api_rate_limit="500 requests/hour",
            api_documentation_url="https://data-platform.internal/docs/maintenance-work-order-history",
        )
    )

    return products


def main() -> None:
    """Generate synthetic data products and save to data/data_products.json."""
    products = _generate_products()

    output = [p.model_dump(mode="json") for p in products]
    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_dir, "data", "data_products.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(products)} data products to {output_path}\n")
    print(f"{'Product':<40} {'Domain':<25} {'Gov Status':<15} {'Score':>6} {'Gaps':>5}")
    print("-" * 100)
    for p in products:
        sc = overall_score(p)
        gap_count = len(gaps(p))
        print(f"  {p.name:<38} {p.domain:<25} {p.governance_status:<15} {sc:>6.1f} {gap_count:>5}")


if __name__ == "__main__":
    main()
