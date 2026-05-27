"""Synthetic AI model generator for the AI-Ready Data & AI Governance Platform.

Generates 6 AI models with evaluations, OKRs, and governance metadata.
"""

import json
import os

from faker import Faker

from src.models import AIModel, ModelEvaluation, ModelOKR

fake = Faker(["no_NO"])


def _eval(eid, date, eval_type, dataset, score, passed, notes, evaluator):
    return ModelEvaluation(
        eval_id=eid, eval_date=date, eval_type=eval_type,
        dataset_used=dataset, score=score, passed=passed,
        notes=notes, evaluated_by=evaluator,
    )


def _okr(objective, key_results, status, quarter, progress_pct):
    return ModelOKR(
        objective=objective, key_results=key_results,
        status=status, quarter=quarter, progress_pct=progress_pct,
    )


def _generate_models() -> list[AIModel]:
    ev1, ev2, ev3 = fake.name(), fake.name(), fake.name()
    ev4, ev5, ev6 = fake.name(), fake.name(), fake.name()

    models: list[AIModel] = []

    # 1. Supplier Risk Agent
    models.append(AIModel(
        id="supplier-risk-agent",
        name="Supplier Risk Agent",
        model_type="Agent",
        description=(
            "Monitors supplier performance data, market signals, and geopolitical risk indicators "
            "to identify suppliers at risk of delivery failure, financial distress, or compliance issues. "
            "Generates risk assessments and recommended mitigation actions for category managers. "
            "Designed to reduce time-to-insight for supplier risk events from days to minutes."
        ),
        version="1.3.0",
        status="Production",
        model_owner=fake.name(),
        governance_lead=fake.name(),
        owning_team="Supply Chain AI & Analytics",
        domain="Procurement",
        governance_status="Approved",
        risk_classification="Medium",
        last_governance_review="2026-01-15",
        next_review_due="2026-07-15",
        base_model="Claude 3.5 Sonnet",
        framework="LangGraph",
        infrastructure="Azure OpenAI + LangGraph on AKS",
        api_endpoint="/api/v2/ai-models/supplier-risk-agent",
        api_key_required=True,
        api_rate_limit="100 requests/hour",
        input_data_products=["DP-001", "DP-002"],
        output_data_products=[],
        required_data_freshness="< 24 hours",
        minimum_data_quality_score=75,
        business_processes=["Procure-to-Pay", "Supplier qualification", "Category management"],
        process_step="Supplier monitoring & risk assessment",
        evaluations=[
            _eval("EVAL-001", "2026-03-10", "accuracy", "Supplier backtest Q1-2025",
                  87.0, True, "Correctly identified 87% of known supplier risk events in backtesting.", ev1),
            _eval("EVAL-002", "2026-03-11", "governance_compliance", "Governance audit sample",
                  92.0, True, "All recommendations include source traceability and confidence scores.", ev2),
            _eval("EVAL-003", "2026-04-02", "data_quality_sensitivity", "Stale data simulation",
                  71.0, False, "Performance degrades when supplier data freshness exceeds 48 hours.", ev3),
        ],
        okrs=[
            _okr("Reduce supplier risk response time",
                 ["Decrease avg time from risk event to action from 5 days to 1 day",
                  "Flag 90% of high-risk suppliers before delivery failure occurs",
                  "Achieve 85%+ user satisfaction in category manager survey"],
                 "On track", "Q2 2026", 65),
            _okr("Improve supplier risk coverage",
                 ["Monitor 100% of tier-1 suppliers continuously",
                  "Expand coverage to 60% of tier-2 suppliers",
                  "Integrate 3 new external risk signal sources"],
                 "At risk", "Q2 2026", 40),
        ],
        total_requests_last_30_days=4200,
        avg_latency_ms=3400,
        error_rate_pct=2.1,
        users_with_access=12,
        max_autonomy_level="recommend",
        human_oversight_required=[
            "All risk classifications above 'medium'",
            "Recommendations affecting contracts above NOK 5M",
            "New supplier risk events involving single-source suppliers",
        ],
        allowed_actions=["summarisation", "trend detection", "risk flagging", "recommendation drafting"],
        prohibited_actions=["autonomous supplier decisions", "contractual commitments", "safety-critical actions"],
        escalation_rules=[
            "Escalate to category manager if risk score > 80",
            "Escalate to procurement director if single-source supplier at risk",
        ],
        created_date="2023-11-01",
        last_updated="2026-04-15",
    ))

    # 2. Contract Insights Assistant
    models.append(AIModel(
        id="contract-insights-assistant",
        name="Contract Insights Assistant",
        model_type="NLP model",
        description=(
            "Analyses contract spend patterns, utilisation rates, and commercial terms to surface insights "
            "for contract managers. Identifies under-utilised framework agreements, spend leakage outside "
            "contracted terms, and approaching renewal deadlines. Designed to support proactive contract "
            "management rather than reactive reporting."
        ),
        version="2.0.1",
        status="Production",
        model_owner=fake.name(),
        governance_lead=fake.name(),
        owning_team="Contract Management Technology",
        domain="Contract Management",
        governance_status="Approved",
        risk_classification="Medium",
        last_governance_review="2026-02-01",
        next_review_due="2026-08-01",
        base_model="Claude 3.5 Haiku",
        framework="LangChain",
        infrastructure="Azure OpenAI on AKS",
        api_endpoint="/api/v2/ai-models/contract-insights-assistant",
        api_key_required=True,
        api_rate_limit="200 requests/hour",
        input_data_products=["DP-002"],
        output_data_products=[],
        required_data_freshness="< 7 days",
        minimum_data_quality_score=70,
        business_processes=["Procure-to-Pay", "Contract management", "Spend analysis"],
        process_step="Contract analysis & renewal planning",
        evaluations=[
            _eval("EVAL-004", "2026-01-20", "accuracy", "Manual review baseline Q4-2025",
                  82.0, True, "Correctly classified 82% of spend anomalies against manual review baseline.", ev4),
            _eval("EVAL-005", "2026-01-21", "latency", "Load test 500 concurrent queries",
                  94.0, True, "Average response under 2 seconds for standard queries.", ev5),
        ],
        okrs=[
            _okr("Improve contract utilisation visibility",
                 ["Surface insights for 100% of framework agreements above NOK 10M",
                  "Reduce unidentified spend leakage by 30%",
                  "Generate monthly utilisation reports for top 50 contracts"],
                 "Achieved", "Q1 2026", 100),
        ],
        total_requests_last_30_days=2100,
        avg_latency_ms=1800,
        error_rate_pct=1.3,
        users_with_access=8,
        max_autonomy_level="read-only",
        human_oversight_required=[
            "Anomalies flagged on contracts above NOK 10M",
            "Recommendations involving new vendors not in master",
        ],
        allowed_actions=["spend pattern analysis", "anomaly detection", "contract utilisation reporting"],
        prohibited_actions=["contract amendments", "payment authorisations", "vendor selection decisions"],
        escalation_rules=["Escalate anomalies above NOK 10M to contract director"],
        created_date="2024-03-01",
        last_updated="2026-02-20",
    ))

    # 3. Logistics Disruption Agent
    models.append(AIModel(
        id="logistics-disruption-agent",
        name="Logistics Disruption Agent",
        model_type="Agent",
        description=(
            "Monitors vessel movements, weather forecasts, port congestion, and operational delay events "
            "to predict and alert on logistics disruptions for offshore operations. Provides disruption "
            "probability scores, estimated delay duration, and recommended contingency actions for "
            "logistics coordinators. Integrates weather and vessel AIS data to provide early warning "
            "of potential delivery failures."
        ),
        version="0.8.2",
        status="Staging",
        model_owner=fake.name(),
        governance_lead=fake.name(),
        owning_team="Offshore Logistics Technology",
        domain="Offshore Logistics",
        governance_status="Under review",
        risk_classification="High",
        last_governance_review="2026-03-01",
        next_review_due="2026-06-01",
        base_model="Claude 3.5 Sonnet",
        framework="LangGraph",
        infrastructure="Azure OpenAI + LangGraph on AKS (staging)",
        api_endpoint="/api/v2/ai-models/logistics-disruption-agent",
        api_key_required=True,
        api_rate_limit="50 requests/hour",
        input_data_products=["DP-003", "DP-004"],
        output_data_products=[],
        required_data_freshness="< 2 hours",
        minimum_data_quality_score=80,
        business_processes=["Offshore logistics planning", "Vessel scheduling", "Emergency response coordination"],
        process_step="Disruption detection & contingency planning",
        evaluations=[
            _eval("EVAL-006", "2026-04-05", "accuracy", "Historical disruption backtest 2024",
                  76.0, False, "Below 80% target — struggles with multi-factor cascading delays.", ev1),
            _eval("EVAL-007", "2026-04-06", "robustness", "Vessel data gap simulation",
                  83.0, True, "Handles vessel data gaps gracefully with fallback heuristics.", ev2),
            _eval("EVAL-008", "2026-04-10", "governance_compliance", "Governance audit staging",
                  68.0, False, "Missing: escalation path for safety-critical delay scenarios not yet defined.", ev6),
        ],
        okrs=[
            _okr("Achieve production readiness for offshore logistics disruption prediction",
                 ["Complete 3 staging environment validation cycles",
                  "Achieve governance board approval",
                  "Demonstrate 80%+ prediction accuracy on historical disruption data"],
                 "At risk", "Q2 2026", 45),
        ],
        total_requests_last_30_days=890,
        avg_latency_ms=5200,
        error_rate_pct=4.7,
        users_with_access=5,
        max_autonomy_level="recommend",
        human_oversight_required=[
            "All disruption alerts involving personnel transfer operations",
            "Delays exceeding 48 hours",
            "Weather severity above orange threshold",
        ],
        allowed_actions=["delay pattern analysis", "ETA prediction", "disruption alerting"],
        prohibited_actions=["vessel rerouting decisions", "safety-critical operational changes", "crew scheduling modifications"],
        escalation_rules=[
            "Escalate to logistics manager if disruption probability > 70%",
            "Escalate to safety coordinator if personnel transfer at risk",
        ],
        created_date="2025-01-15",
        last_updated="2026-04-10",
    ))

    # 4. Inventory Planning Assistant
    models.append(AIModel(
        id="inventory-planning-assistant",
        name="Inventory Planning Assistant",
        model_type="Recommendation engine",
        description=(
            "Forecasts material consumption patterns and recommends optimal reorder points, safety stock "
            "levels, and procurement timing for warehouse and materials planners. Designed to reduce "
            "stockout events for critical spare parts while minimising excess inventory carrying costs "
            "across onshore and offshore storage locations."
        ),
        version="3.1.0",
        status="Production",
        model_owner=fake.name(),
        governance_lead=fake.name(),
        owning_team="Materials Management & Planning",
        domain="Materials Management",
        governance_status="Approved",
        risk_classification="Low",
        last_governance_review="2026-01-20",
        next_review_due="2026-07-20",
        base_model="XGBoost + heuristic rules",
        framework="scikit-learn",
        infrastructure="Azure ML (CPU cluster)",
        api_endpoint="/api/v2/ai-models/inventory-planning-assistant",
        api_key_required=True,
        api_rate_limit="500 requests/hour",
        input_data_products=["DP-004"],
        output_data_products=[],
        required_data_freshness="< 24 hours",
        minimum_data_quality_score=75,
        business_processes=["Materials management", "Procurement planning", "Warehouse operations"],
        process_step="Demand forecasting & reorder planning",
        evaluations=[
            _eval("EVAL-009", "2026-02-14", "accuracy", "Top 200 materials 6-month backtest",
                  91.0, True, "91% forecast accuracy on top 200 materials over 6-month backtest.", ev3),
            _eval("EVAL-010", "2026-02-15", "fairness", "Onshore vs offshore location analysis",
                  88.0, True, "No significant bias across onshore vs offshore locations.", ev4),
        ],
        okrs=[
            _okr("Reduce critical spare part stockouts",
                 ["Reduce stockout events for critical spares by 40%",
                  "Achieve 90%+ forecast accuracy for top 200 materials",
                  "Decrease average reorder lead time by 2 days"],
                 "On track", "Q2 2026", 72),
        ],
        total_requests_last_30_days=12300,
        avg_latency_ms=450,
        error_rate_pct=0.8,
        users_with_access=38,
        max_autonomy_level="recommend",
        human_oversight_required=[
            "Critical spare part below safety stock",
            "Forecast deviation above 30%",
            "New material not in master data",
        ],
        allowed_actions=["stock level forecasting", "reorder recommendations", "consumption trend analysis"],
        prohibited_actions=["automatic purchase order creation", "safety stock overrides", "warehouse allocation changes"],
        escalation_rules=["Escalate critical stockout risk to materials manager within 4 hours"],
        created_date="2023-06-01",
        last_updated="2026-03-01",
    ))

    # 5. Maintenance Planning Agent
    models.append(AIModel(
        id="maintenance-planning-agent",
        name="Maintenance Planning Agent",
        model_type="Predictive model",
        description=(
            "Analyses maintenance work order history, IoT sensor readings, and equipment failure patterns "
            "to predict upcoming maintenance needs and prioritise the maintenance backlog. Designed to "
            "support shift from reactive to predictive maintenance for offshore assets, reducing unplanned "
            "downtime and improving safety compliance."
        ),
        version="2.2.0",
        status="Production",
        model_owner=fake.name(),
        governance_lead=fake.name(),
        owning_team="Asset Integrity & Reliability Engineering",
        domain="Operations",
        governance_status="Restricted",
        risk_classification="Critical",
        last_governance_review="2026-02-10",
        next_review_due="2026-05-10",
        base_model="Custom LSTM + Random Forest ensemble",
        framework="PyTorch + scikit-learn",
        infrastructure="On-premise GPU cluster (NVIDIA A100)",
        api_endpoint="/api/v2/ai-models/maintenance-planning-agent",
        api_key_required=True,
        api_rate_limit="50 requests/hour",
        input_data_products=["DP-005"],
        output_data_products=[],
        required_data_freshness="< 24 hours",
        minimum_data_quality_score=80,
        business_processes=["Asset maintenance", "Reliability engineering", "Safety compliance"],
        process_step="Predictive maintenance & backlog prioritisation",
        evaluations=[
            _eval("EVAL-011", "2026-03-05", "accuracy", "7-day prediction horizon backtest 2025",
                  79.0, False, "Below 80% target for 7-day advance prediction — performs better at 3-day horizon (88%).", ev5),
            _eval("EVAL-012", "2026-03-06", "governance_compliance", "Safety audit Q1 2026",
                  95.0, True, "Fully compliant — all outputs flagged for human review on safety-critical equipment.", ev6),
            _eval("EVAL-013", "2026-03-07", "data_quality_sensitivity", "Low IoT coverage simulation",
                  64.0, False, "Significant accuracy drop when IoT sensor coverage is below 50% for an asset.", ev1),
        ],
        okrs=[
            _okr("Reduce unplanned offshore equipment downtime",
                 ["Predict 70% of equipment failures 7+ days in advance",
                  "Reduce unplanned downtime events by 25%",
                  "Maintain zero missed regulatory maintenance deadlines"],
                 "On track", "Q2 2026", 58),
        ],
        total_requests_last_30_days=890,
        avg_latency_ms=2800,
        error_rate_pct=1.9,
        users_with_access=8,
        max_autonomy_level="read-only",
        human_oversight_required=[
            "ALL predictions for safety-critical equipment",
            "Any recommendation to defer scheduled maintenance",
            "Predictions involving regulatory inspection timelines",
            "Anomaly alerts on equipment with less than 2 years of sensor data",
        ],
        allowed_actions=["failure pattern analysis", "predictive maintenance indicators", "maintenance backlog prioritisation"],
        prohibited_actions=[
            "maintenance schedule changes on safety-critical equipment",
            "inspection interval modifications",
            "compliance record alterations",
        ],
        escalation_rules=[
            "Escalate predicted failures within 7 days to maintenance engineer",
            "Escalate safety-critical equipment anomalies to reliability director within 1 hour",
        ],
        created_date="2023-09-01",
        last_updated="2026-03-20",
    ))

    # 6. Procurement Anomaly Detector
    models.append(AIModel(
        id="procurement-anomaly-detector",
        name="Procurement Anomaly Detector",
        model_type="Anomaly detector",
        description=(
            "Scans purchase orders, invoices, and contract terms to detect anomalous transactions "
            "that may indicate maverick spending, duplicate payments, pricing errors, or potential "
            "compliance issues. Designed to complement manual audit processes by surfacing high-priority "
            "items for investigation."
        ),
        version="0.3.1",
        status="Development",
        model_owner=fake.name(),
        governance_lead=fake.name(),
        owning_team="Procurement Compliance & Audit",
        domain="Cross-domain",
        governance_status="Draft",
        risk_classification="Medium",
        last_governance_review="2026-04-15",
        next_review_due="2026-07-15",
        base_model="Isolation Forest + rule-based filters",
        framework="scikit-learn",
        infrastructure="Azure ML (CPU cluster)",
        api_endpoint="/api/v2/ai-models/procurement-anomaly-detector",
        api_key_required=True,
        api_rate_limit="200 requests/hour",
        input_data_products=["DP-001", "DP-002"],
        output_data_products=[],
        required_data_freshness="< 7 days",
        minimum_data_quality_score=70,
        business_processes=["Procure-to-Pay", "Internal audit", "Compliance monitoring"],
        process_step="Transaction monitoring & audit support",
        evaluations=[
            _eval("EVAL-014", "2026-04-20", "accuracy", "Known anomaly backtest 2023-2025",
                  68.0, False, "High false positive rate — 32% of flagged transactions were normal on manual review.", ev2),
        ],
        okrs=[
            _okr("Validate anomaly detection approach on historical procurement data",
                 ["Achieve 75%+ precision on known anomaly backtest",
                  "Complete stakeholder review with procurement compliance team",
                  "Define production deployment plan with data platform team"],
                 "Behind", "Q2 2026", 25),
        ],
        total_requests_last_30_days=120,
        avg_latency_ms=1200,
        error_rate_pct=8.3,
        users_with_access=3,
        max_autonomy_level="read-only",
        human_oversight_required=[
            "All flagged transactions above NOK 500k",
            "Any anomaly involving new vendors",
        ],
        allowed_actions=["anomaly detection", "transaction flagging", "audit report generation"],
        prohibited_actions=["automatic transaction blocking", "vendor blacklisting", "payment holds"],
        escalation_rules=["All anomaly flags must be reviewed by a compliance officer before any action"],
        created_date="2025-09-01",
        last_updated="2026-04-20",
    ))

    return models


def main() -> None:
    models = _generate_models()
    output = [m.model_dump(mode="json") for m in models]
    project_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(project_dir, "data", "ai_models.json")

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(models)} AI models to {output_path}\n")
    print(f"{'Model':<35} {'Status':<12} {'Gov':<14} {'Risk':<10} {'Evals':>6} {'Latest':>7}")
    print("-" * 90)
    for m in models:
        latest = m.evaluations[-1].score if m.evaluations else 0
        print(f"  {m.name:<33} {m.status:<12} {m.governance_status:<14} {m.risk_classification:<10} {len(m.evaluations):>6} {latest:>7.1f}")


if __name__ == "__main__":
    main()
