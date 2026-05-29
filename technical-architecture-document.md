# AI-Ready Data Product Registry — Technical Architecture & Design Document

> **Author:** Mayowa Togun
> **Version:** 2.1
> **Last updated:** May 2026
> **Status:** Portfolio project — fully synthetic data

---

## 1. Executive summary

This platform demonstrates how enterprise data products and AI models can be structured, documented, and governed so they are safe for analytics and AI-agent consumption in industrial environments.

It was built to answer a question that every organisation deploying AI at scale must face: **How do you make enterprise data trustworthy enough for AI agents to act on, and how do you govern the AI models that consume it?**

The platform combines data product catalogue management (inspired by tools like Collibra and Alation) with AI model governance, readiness scoring, and operational monitoring. It models a realistic industrial energy company with 5 data product domains, 6 AI models at different lifecycle stages, 10 governance users, and end-to-end approval workflows.

---

## 2. Problem statement

### The data trust gap

Enterprise data is created for human consumers. Reports, dashboards, and spreadsheets are designed for people who can apply judgment, ask follow-up questions, and recognise when something looks wrong. AI agents cannot do this. They consume data at face value. If the data is stale, incomplete, poorly documented, or lacks clear ownership, an AI agent will still act on it — and the organisation bears the consequence.

### What AI agents need before they can be trusted

Before an AI agent should consume enterprise data, the data product must have:

- **Clear ownership:** A named business owner, technical owner, and data steward who are accountable for the product's quality and availability.
- **Documentation:** Consumer-facing descriptions, schema definitions, and known limitations that allow an agent (or its developers) to understand what the data represents and what it does not.
- **Lineage:** A traceable path from source systems through transformation layers to the data product, so that any output can be traced back to its origin.
- **Quality rules:** Defined, measurable quality expectations with severity levels (critical, warning, info) and thresholds that can be monitored automatically.
- **Access controls:** Classification levels, permitted and prohibited uses, and explicit rules about what AI agents are and are not allowed to do with the data.
- **Human escalation paths:** Defined triggers for when AI outputs must be reviewed by a human before action is taken — based on confidence levels, data freshness, value thresholds, or safety implications.
- **Freshness guarantees:** Stated refresh frequencies and SLAs so consumers know how current the data is.

This platform scores data products across all 8 of these dimensions and makes the assessment visible, auditable, and actionable.

### The AI model governance gap

The data product side is necessary but not sufficient. The AI models that consume data products also need governance:

- **Performance tracking:** Regular evaluations across accuracy, fairness, robustness, latency, governance compliance, and data quality sensitivity.
- **OKRs:** Business objectives tied to measurable key results, so the model's value is tracked like any other product.
- **Data dependency management:** Explicit mapping of which data products a model consumes, with quality floor requirements that flag when a dependency degrades.
- **Autonomy controls:** Clear definitions of what a model is allowed to do autonomously versus what requires human approval.
- **Lifecycle governance:** Approval workflows for model promotion (Development → Staging → Production), API key issuance, and access management.

This platform models all of this.

---

## 3. Architecture overview

### 3.1 System architecture

```
┌──────────────────────────────────────────────────────────────┐
│                    Streamlit application                      │
│                                                              │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │   Data    │ │    AI    │ │Readiness │ │   Data   │       │
│  │Catalogue │ │  Model   │ │  Scores  │ │Contracts │       │
│  │   Tab    │ │Registry  │ │   Tab    │ │   Tab    │       │
│  │          │ │   Tab    │ │          │ │          │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
│       │             │             │             │             │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │    AI    │ │ Lineage  │ │Governance│ │ Process  │       │
│  │Consumpt. │ │  & Mesh  │ │   Tab    │ │  Maps    │       │
│  │   Tab    │ │   Tab    │ │          │ │   Tab    │       │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘       │
│       │             │             │             │             │
├───────┴─────────────┴─────────────┴─────────────┴────────────┤
│                     Application logic                         │
│                                                              │
│  readiness_score.py  contract_validator.py  lineage.py       │
│  data_mesh.py        process_maps.py        model_arch.py    │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                     Data models (Pydantic v2)                 │
│                                                              │
│  DataProduct    AIModel       User          APIKey           │
│  DataContract   ModelOKR      ApprovalReq   TokenUsage       │
│  QualityRule    ModelEval     LineageNode   AIUsagePolicy     │
│                                                              │
├──────────────────────────────────────────────────────────────┤
│                     Data layer (JSON files)                   │
│                                                              │
│  data_products.json    ai_models.json     users.json         │
│  api_keys.json         approval_requests.json                │
│  token_usage.json                                            │
└──────────────────────────────────────────────────────────────┘
```

### 3.2 Technology choices

| Component | Technology | Rationale |
|---|---|---|
| UI framework | Streamlit | Rapid prototyping, built-in charting, native data display components. Appropriate for a governance dashboard that is data-heavy and interaction-light. |
| Data validation | Pydantic v2 | Schema enforcement at the data layer. Every record is validated before entering the system. Mirrors how real data catalogues enforce metadata standards. |
| Synthetic data | Faker (nb_NO locale) | Realistic Norwegian names, dates, and identifiers. Domain-specific content hand-crafted for industrial realism. |
| Diagram rendering | Mermaid JS (CDN) | Renders flowcharts, architecture diagrams, and process maps in the browser. No server-side image generation required. |
| Charting | Streamlit native (Pandas) | st.line_chart, st.bar_chart, st.area_chart backed by Pandas DataFrames. Sufficient for token consumption trends and metric displays. |
| Storage | JSON files | Appropriate for a portfolio demo with 5 data products and 6 AI models. A production system would use a database, but JSON keeps the project self-contained and easy to inspect. |

### 3.3 File structure

```
ai-ready-data-product-registry/
│
├── app.py                          # Streamlit entry point (8 tabs)
│
├── generate_data.py                # Data product generator (5 products)
├── generate_ai_models.py           # AI model generator (6 models)
├── generate_users.py               # User, API key, approval generator
├── generate_token_usage.py         # Token consumption data generator
│
├── requirements.txt                # Python dependencies
├── README.md                       # Project documentation
│
├── data/                           # Generated synthetic data
│   ├── data_products.json          # 5 enterprise data products
│   ├── ai_models.json              # 6 AI models
│   ├── users.json                  # 10 governance users
│   ├── api_keys.json               # 8 API keys
│   ├── approval_requests.json      # 6 approval requests
│   └── token_usage.json            # 6 months token consumption
│
├── src/                            # Application logic modules
│   ├── __init__.py
│   ├── models.py                   # All Pydantic data models
│   ├── readiness_score.py          # 8-dimension AI-readiness scoring
│   ├── contract_validator.py       # Data contract validation engine
│   ├── lineage.py                  # Mermaid lineage diagram generator
│   ├── data_mesh.py                # Data mesh architecture and assessment
│   ├── process_maps.py             # Business process flow diagrams
│   └── model_architecture.py       # AI model architecture diagrams
│
└── screenshots/                    # UI screenshots for documentation
```

---

## 4. Data model design

### 4.1 Data product model

The DataProduct is the central entity. It represents a governed, documented dataset that is treated as a product with defined consumers, quality expectations, and usage rules.

**Core identity fields:**
- `id`, `name`, `domain`, `description`, `tags`
- `governance_status`: Draft → Under review → Approved → Deprecated
- `classification`: Public, Internal, Confidential, Restricted

**Ownership fields:**
- `business_owner`: Accountable for the product's business value and prioritisation
- `technical_owner`: Accountable for the product's technical health and availability
- `data_steward`: Accountable for data quality, metadata accuracy, and governance compliance
- `domain_owner_team`: The team that owns the domain this product belongs to

**Lineage:** An ordered list of LineageNode objects, each with a system name, layer (source → raw → cleaned → product → consumer), and description. The lineage chain traces data from origin to consumption.

**Data contract:** A nested DataContract object containing:
- Consumer lists (human and AI)
- Quality rules with field-level thresholds and severity
- Freshness SLA
- AI usage policy (permitted uses, prohibited uses, human review triggers, max autonomy level)
- Escalation contact
- Contract version and review date

**Usage metrics:**
- `total_consumers`, `ai_consumers_count`, `api_calls_last_30_days`
- `unique_users_last_30_days`, `data_shares_internal`, `data_shares_external`
- `popularity_rank`, `last_accessed`

**API access:**
- `api_endpoint`, `api_key_required`, `api_rate_limit`, `api_documentation_url`

### 4.2 AI model model

The AIModel represents a registered AI model or agent with governance metadata, performance tracking, and data dependencies.

**Core identity:** `id`, `name`, `model_type`, `description`, `version`, `status`, `domain`

**Model types supported:**
- Agent (multi-model orchestration, e.g. LangGraph)
- Predictive model (time-series, regression)
- Classification model
- NLP model (single LLM)
- Recommendation engine
- Anomaly detector

**Ownership and governance:**
- `model_owner`, `governance_lead`, `owning_team`
- `governance_status`: Draft → Under review → Approved → Restricted → Suspended
- `risk_classification`: Low, Medium, High, Critical
- `last_governance_review`, `next_review_due`

**Data dependencies:**
- `input_data_products`: IDs of data products this model consumes
- `output_data_products`: IDs of data products this model produces or enriches
- `required_data_freshness`, `minimum_data_quality_score`

**Performance tracking:**
- `evaluations`: List of ModelEvaluation objects (eval type, score, passed/failed, notes)
- `okrs`: List of ModelOKR objects (objective, key results, status, progress)
- `total_requests_last_30_days`, `avg_latency_ms`, `error_rate_pct`

**Autonomy controls:**
- `max_autonomy_level`: read-only, recommend, act-with-approval, full-autonomous
- `human_oversight_required`, `allowed_actions`, `prohibited_actions`, `escalation_rules`

### 4.3 Governance entities

**User:** Platform users with roles (Data Product Owner, Data Steward, AI Model Owner, Governance Lead, Domain Lead, Platform Admin, Data Consumer, AI Consumer), access levels (Viewer, Contributor, Approver, Admin), and approval permissions.

**APIKey:** Scoped access tokens for data products and AI models with issued/expiry dates, rate limits, and status tracking.

**ApprovalRequest:** Governance workflow records for data product access, AI model deployment, API key generation, and governance reviews. Statuses: Pending, Approved, Rejected, Escalated.

---

## 5. AI-readiness scoring framework

### 5.1 Design rationale

The scoring framework was designed to answer one question: **Is this data product ready for AI agents to consume safely?**

It assesses 8 dimensions. Each dimension scores 0–100 independently, then contributes to a weighted composite score.

### 5.2 Dimensions and weights

| Dimension | Weight | What it measures |
|---|---|---|
| Ownership | 15% | Are business owner, technical owner, and data steward assigned? |
| Documentation | 10% | Does the product have a description, documentation URL, and stated limitations? |
| Lineage | 15% | Can the data be traced from source to consumer through at least 3 layers? |
| Quality | 15% | Are quality rules defined, including critical-severity rules? |
| Access rules | 10% | Is classification set and are metadata fields defined for consumer contracts? |
| AI usage policy | 15% | Are permitted uses, prohibited uses, review triggers, and autonomy level defined? |
| Freshness | 10% | Are refresh frequency and freshness SLA defined? |
| Human escalation | 10% | Are escalation triggers and an escalation contact defined? |

### 5.3 Scoring logic

Each dimension has binary sub-checks that sum to 100:

**Example — Ownership (15% weight):**
- Business owner exists and is non-empty: +40 points
- Technical owner exists and is non-empty: +30 points
- Data steward exists and is non-empty: +30 points

A product with all three owners scores 100 on ownership. A product missing a data steward scores 70.

### 5.4 Composite score and status

- **Overall score** = weighted sum of all 8 dimension scores, rounded to 1 decimal
- **Ready** (≥ 80): Data product can be consumed by AI agents under the defined contract
- **Conditionally ready** (≥ 50): Data product has gaps that should be addressed before AI consumption
- **Not ready** (< 50): Data product should not be consumed by AI agents

### 5.5 Gap detection

The `gaps()` function returns human-readable strings identifying specific missing elements:
- "No data steward assigned"
- "Missing documentation URL"
- "Contract not reviewed in the last 6 months"
- "No escalation contact defined"
- "Incomplete lineage — missing transformation layer"

These are designed to be actionable — each gap maps to a specific fix.

### 5.6 Sample scores (current synthetic data)

| Product | Overall | Status | Key gaps |
|---|---|---|---|
| Supplier Performance Summary | 92–95 | Ready | Missing documentation URL |
| Logistics Delay Events | 88–91 | Ready | Weak quality rule severity, no retention policy |
| Maintenance Work Order History | 86–90 | Ready | Incomplete lineage (missing cleaned layer) |
| Contract Spend History | 85–88 | Conditionally ready | No steward, stale contract review |
| Inventory Availability Snapshot | 78–82 | Conditionally ready | No steward, no escalation contact, no freshness SLA |

---

## 6. Data mesh architecture

### 6.1 Mesh principles modelled

This platform models the 4 data mesh principles:

**1. Domain ownership:** Each of the 5 domains (Procurement, Contract Management, Offshore Logistics, Materials Management, Operations) owns its data products. Ownership is assigned at the product level (business owner, technical owner, steward) and at the domain level (domain owner team, domain lead).

**2. Data as a product:** Data products are treated with product discipline: documented, versioned, measured for adoption, scored for quality, and governed through contracts. Usage metrics (API calls, unique users, sharing) treat data products as assets with consumers, not just tables in a database.

**3. Self-serve data platform:** The registry itself serves as the platform layer: a catalogue for discovery, a readiness scorer for quality assessment, a contract validator for governance compliance, and an API key system for access management.

**4. Federated computational governance:** Governance is distributed to domains (each domain has a Domain Lead who can approve) but coordinated centrally through the Governance Lead and Platform Admin roles. Governance policies (scoring criteria, contract requirements, AI usage rules) are platform-level standards; their application is domain-level responsibility.

### 6.2 Domain maturity assessment

Each domain is assessed for maturity:
- **Optimising:** Average readiness ≥ 90, all products Approved
- **Measured:** Average readiness ≥ 75, most products Approved
- **Managed:** Below measured threshold

### 6.3 Cross-domain data flows

The data mesh diagram visualises cross-domain dependencies. For example:
- The Procurement Anomaly Detector (Cross-domain) consumes from both Procurement (Supplier Performance Summary) and Contract Management (Contract Spend History)
- The Logistics Disruption Agent consumes from both Offshore Logistics (Logistics Delay Events) and Materials Management (Inventory Availability Snapshot)

These cross-domain flows are where governance coordination matters most, because no single domain owns the full data chain.

---

## 7. AI model governance design

### 7.1 Lifecycle stages

```
Development → Staging → Production → Deprecated
                ↓
           Under review (governance gate)
                ↓
           Approved / Restricted / Suspended
```

Each transition requires governance approval. The platform models this through ApprovalRequest entities with approval level requirements (Domain Lead, Governance Lead, Platform Admin).

### 7.2 Risk classification

| Level | Criteria | Governance requirements |
|---|---|---|
| Low | No safety implications, read-only, low financial impact | Domain Lead approval |
| Medium | Recommendations that influence decisions, moderate financial impact | Domain Lead + Governance Lead approval |
| High | Safety-adjacent, high financial impact, external-facing | Governance Lead + Platform Admin approval |
| Critical | Safety-critical equipment, regulatory compliance, personnel safety | Full governance board review, mandatory human oversight on all outputs |

### 7.3 Autonomy controls

Each model has a defined maximum autonomy level:
- **Read-only:** Can analyse and report but not generate recommendations
- **Recommend:** Can generate recommendations but a human must approve before action
- **Act-with-approval:** Can prepare actions but requires explicit human approval to execute
- **Full-autonomous:** Can act without human approval (not used for any model in this platform)

### 7.4 Data dependency management

Each AI model declares which data products it consumes and what minimum readiness score it requires. The platform surfaces mismatches:
- "Dependency risk: Inventory Availability Snapshot readiness is 78, below the Logistics Disruption Agent's minimum of 80"

This creates a feedback loop: improving a data product's governance directly enables AI models that depend on it.

### 7.5 Evaluation framework

Models are evaluated across 6 types:
- **Accuracy:** Does the model produce correct outputs against a known baseline?
- **Fairness:** Are outputs equitable across relevant dimensions (location, category)?
- **Robustness:** Does the model handle edge cases, data gaps, and adversarial inputs?
- **Latency:** Does the model meet response time requirements?
- **Governance compliance:** Does the model trace outputs to sources, include confidence scores, and flag for human review when required?
- **Data quality sensitivity:** How does model performance degrade when input data quality drops?

Each evaluation has a score, pass/fail status, notes, and the name of the evaluator.

### 7.6 Token consumption monitoring

Generative AI models (those using LLMs) have token consumption tracking:
- Monthly input/output token volumes
- Cost calculation using model-specific pricing
- Sub-model breakdown for multi-model agents (e.g. Haiku for scanning, Sonnet for synthesis)
- Budget utilisation percentage with threshold warnings (80% approaching, 95% critical)

Non-generative models (XGBoost, LSTM, Isolation Forest) are explicitly excluded from token tracking with explanatory messaging.

---

## 8. Process integration

### 8.1 Procure-to-Pay process map

The P2P process has 8 steps. Data products and AI models are mapped to specific steps:

| Process step | Data products used | AI models active |
|---|---|---|
| Need identification | Inventory Availability Snapshot | Inventory Planning Assistant |
| Requisition | — | — |
| Supplier selection | Supplier Performance Summary | Supplier Risk Agent |
| Purchase order | Contract Spend History | Contract Insights Assistant |
| Goods receipt | — | — |
| Invoice processing | Contract Spend History | Procurement Anomaly Detector |
| Payment | — | — |
| Supplier performance review | Supplier Performance Summary | Supplier Risk Agent |

### 8.2 Maintenance & Reliability process map

| Process step | Data products used | AI models active |
|---|---|---|
| Asset monitoring | Maintenance Work Order History | Maintenance Planning Agent |
| Anomaly detection | Maintenance Work Order History | Maintenance Planning Agent |
| Work order creation | — | — |
| Planning & scheduling | Maintenance Work Order History | Maintenance Planning Agent |
| Execution | — | — |
| Completion & reporting | Maintenance Work Order History | — |
| Reliability analysis | Maintenance Work Order History | Maintenance Planning Agent |

### 8.3 Model coverage metrics

Each process map includes a coverage summary:
- Number of data products involved
- Number of AI models involved
- Model lifecycle status distribution (how many are Production vs Staging vs Development)

---

## 9. Governance workflow design

### 9.1 Role hierarchy

```
Platform Admin
    ├── Can approve: everything
    ├── Can generate: API keys
    └── Access level: Admin

Governance Lead
    ├── Can approve: data products, AI models
    ├── Can generate: API keys
    └── Access level: Approver

Domain Lead (per domain)
    ├── Can approve: data products and AI models in their domain
    └── Access level: Approver

Data Product Owner
    ├── Can approve: data products they own
    └── Access level: Contributor

AI Model Owner
    ├── Can approve: AI models they own
    └── Access level: Contributor

Data Steward
    └── Access level: Contributor

Data Consumer / AI Consumer
    └── Access level: Viewer
```

### 9.2 Approval workflow

```
Request submitted
    │
    ▼
Routed to required approver (based on risk level)
    │
    ├── Low risk → Domain Lead
    ├── Medium risk → Domain Lead + Governance Lead
    ├── High risk → Governance Lead + Platform Admin
    └── Critical risk → Full governance board
    │
    ▼
Review decision
    │
    ├── Approved → Access granted / Model promoted / Key issued
    ├── Rejected → Notes provided, requester notified
    └── Escalated → Routed to higher authority
```

### 9.3 API key scoping

| Scope | Permissions |
|---|---|
| Read | Query data product or AI model outputs |
| Read-write | Query and submit data or trigger model runs |
| Admin | Full access including configuration changes |

API keys have expiry dates, rate limits, and usage tracking (last used date). Expired and revoked keys are retained for audit purposes.

---

## 10. Design decisions and tradeoffs

| Decision | Rationale | Tradeoff |
|---|---|---|
| JSON storage instead of database | Self-contained, inspectable, no infrastructure dependencies | Does not scale beyond demo size; no concurrent write safety |
| Pydantic validation at data generation | Catches schema violations before they enter the system | Slightly slower generation; adds code complexity |
| Deliberate data imperfections | Demonstrates governance gap detection; builds credibility with reviewers | Some products appear "worse" which could confuse casual viewers |
| 8-dimension scoring with fixed weights | Auditable, explainable, deterministic | Weights may not match every organisation's priorities; not ML-based |
| Separate AI model registry | Shows the connection between data governance and AI governance | Adds complexity; some reviewers may only care about data products |
| Token consumption for generative models only | Honest differentiation between LLM and traditional ML costs | Non-generative models have less visible operational detail |
| Mermaid for all diagrams | Renders in browser, version-controllable in Git, no image dependencies | Less visual control than D3 or custom SVG; limited layout options |
| Norwegian-sounding synthetic names | Builds cultural context for a Norwegian energy company setting | Minor detail, but signals attention to the operating environment |

---

## 11. What a production version would need

This is a portfolio demonstration. A production deployment would require:

- **Database backend:** PostgreSQL or similar for data products, models, users, and audit logs
- **Authentication and authorisation:** SSO integration, role-based access control, session management
- **Real catalogue integration:** Collibra, Microsoft Purview, or Alation API connections for live metadata sync
- **CI/CD for AI models:** Integration with MLflow, Weights & Biases, or Azure ML for model versioning and evaluation pipelines
- **Real-time monitoring:** Prometheus/Grafana for uptime, latency, and error rate dashboards
- **Event-driven governance:** Automated alerts when readiness scores drop, contracts expire, or evaluations fail
- **Audit logging:** Immutable log of all governance decisions, access events, and model deployments
- **Multi-tenancy:** Separate domain workspaces with cross-domain visibility for governance leads
- **API layer:** REST or GraphQL API for programmatic access to the catalogue and governance functions

---

## 12. Disclaimer

This project uses fully synthetic data generated for portfolio and demonstration purposes. It does not contain real company data, proprietary architecture, internal system names, operational records, supplier information, or confidential material. All data product structures, AI model configurations, user profiles, and governance workflows are entirely fictional. Domain patterns are inspired by industrial energy-sector environments but do not represent any specific organisation's systems or data.
