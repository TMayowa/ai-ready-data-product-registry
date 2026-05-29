# AI-Ready Data Product Registry — Prompt Engineering & Build Log

> **Purpose:** This document records every prompt used to build the AI-Ready Data Product Registry & Governance Platform. It demonstrates how AI-assisted development (Warp AI, Claude) was used as a deliberate engineering tool with structured, incremental prompting to produce a production-quality portfolio project in under 8 hours.
>
> **Why this matters:** The AI-Ready Data Product Owner role requires understanding how AI tools can be applied to real workflows. This build log is itself evidence of that skill — using AI as a coding partner with clear specifications, validation checkpoints, and human judgment at every step.

---

## Build methodology

**Approach:** Incremental prompt engineering with verification gates
**Tools used:** Warp AI (terminal-based AI coding assistant), Claude (architecture planning, data design, documentation)
**Total prompts:** 14 build prompts + 4 enhancement patches
**Total build time:** ~8 hours across 2 sessions
**Human decisions at each step:** Architecture choices, domain-specific data design, governance logic, industrial realism review

**Key principle:** Each prompt produces a working, testable increment. No prompt assumes the previous one succeeded — every step starts with verification. This mirrors how I approach product delivery: ship small, validate early, iterate.

---

## Phase 1 — Foundation (Prompts 1–5)

### Prompt 1: Project scaffold

**What it does:** Creates the folder structure, empty modules, and dependency file.
**Why this comes first:** Establishes the contract between all future prompts — file paths, module names, and import structure. Every later prompt references this layout.

```
Create a Python project with this exact structure:

ai-ready-data-product-registry/
├── app.py                    # Streamlit entry point (empty for now, just st.title)
├── requirements.txt          # streamlit, pydantic, faker, pandas, streamlit-mermaid
├── README.md                 # placeholder with project name
├── data/
│   └── .gitkeep
├── src/
│   ├── __init__.py
│   ├── models.py             # empty, will hold Pydantic models
│   ├── readiness_score.py    # empty
│   ├── contract_validator.py # empty
│   └── lineage.py            # empty
├── screenshots/
│   └── .gitkeep
└── .gitignore                # Python defaults + .streamlit/

In requirements.txt include:
streamlit>=1.30.0
pydantic>=2.0.0
faker>=20.0.0
pandas>=2.0.0
streamlit-mermaid>=0.2.0

Initialize a git repo. Do NOT install anything yet.
```

**Verification:** `ls -R` shows full tree. `cat requirements.txt` has all 5 packages.

---

### Prompt 2: Pydantic data models

**What it does:** Defines the core data structures — QualityRule, LineageNode, AIUsagePolicy, DataContract, and DataProduct.
**Why Pydantic:** Enforces validation at the data layer. Every data product must conform to the schema before it enters the system. This mirrors how real data catalogues enforce metadata standards.
**Design decision:** The DataProduct model has 5 nested models because a data product in an enterprise context is not a flat record — it has quality rules, lineage chains, contracts, and AI usage policies that each have their own structure.

```
In ai-ready-data-product-registry/src/models.py, create Pydantic v2 models
for an enterprise data product registry.

Create these models:

1. QualityRule
   - field_name: str
   - rule_description: str
   - threshold: str (e.g. "not null", "between 0 and 100", "within 24h SLA")
   - severity: Literal["critical", "warning", "info"]

2. LineageNode
   - system_name: str
   - layer: Literal["source", "raw", "cleaned", "product", "consumer"]
   - description: str

3. AIUsagePolicy
   - permitted_uses: list[str]
   - prohibited_uses: list[str]
   - human_review_triggers: list[str]
   - max_autonomy_level: Literal["read-only", "recommend", "act-with-approval",
     "full-autonomous"]

4. DataContract
   - contract_version: str
   - last_reviewed: str
   - consumers: list[str]
   - ai_consumers: list[str]
   - required_metadata_fields: list[str]
   - quality_rules: list[QualityRule]
   - freshness_sla: str
   - ai_usage_policy: AIUsagePolicy
   - escalation_contact: str

5. DataProduct (the main model)
   - id: str
   - name: str
   - domain: Literal["Procurement", "Contract Management",
     "Offshore Logistics", "Materials Management", "Operations"]
   - description: str
   - business_owner: str
   - technical_owner: str
   - data_steward: str
   - source_systems: list[str]
   - classification: Literal["Public", "Internal", "Confidential", "Restricted"]
   - refresh_frequency: Literal["Real-time", "Hourly", "Daily", "Weekly", "Monthly"]
   - documentation_url: str | None = None
   - lineage: list[LineageNode]
   - data_contract: DataContract
   - known_limitations: list[str]
   - created_date: str
   - last_updated: str

Use Pydantic v2 syntax (model_config, no class Config).
Add a docstring to each model.
```

**Verification:** `python -c "from src.models import DataProduct; print('OK')"` prints OK.

---

### Prompt 3: Synthetic data generation

**What it does:** Generates 5 realistic data products with hand-crafted domain content and saves to JSON.
**Critical design decision:** The domain-specific content (quality rules, AI policies, lineage chains, human-review triggers) was specified manually in the prompt, not generated randomly. Random generation produces generic data that would not demonstrate industrial domain knowledge. Each product reflects real energy-sector patterns: SAP source systems, offshore logistics terminology, safety-critical classifications, Norwegian operational context.
**Length note:** This is the longest prompt because domain realism is the differentiator. A reviewer at Aker BP will judge the quality of the governance metadata, not the code.

```
Create a file ai-ready-data-product-registry/generate_data.py that generates
5 realistic sample data products and saves them to data/data_products.json.

Use Faker for names/dates and hand-craft the domain-specific content to be
realistic for an industrial energy company.

The 5 data products:

1. Supplier Performance Summary
   - Domain: Procurement
   - Sources: SAP S/4HANA, Supplier Portal
   - Classification: Internal
   - Refresh: Daily
   - Lineage: SAP ERP → Raw supplier transactions → Cleaned supplier metrics
     → Supplier Performance Summary → [Power BI dashboard, Supplier Risk Agent]
   - Quality rules: supplier_id not null (critical), performance_score
     between 0-100 (critical), last_evaluation_date within 12 months (warning)
   - AI permitted: summarisation, trend detection, risk flagging,
     recommendation drafting
   - AI prohibited: autonomous supplier decisions, contractual commitments,
     safety-critical actions
   - Human review: confidence below 80%, source freshness exceeds SLA,
     involves restricted suppliers, recommendation affects contract value
     above NOK 5M
   - Max autonomy: recommend
   - Known limitations: does not include sub-tier supplier data,
     performance scores lag by 1 business day

2. Contract Spend History
   - Domain: Contract Management
   - Sources: SAP S/4HANA, Contract Management Platform
   - Classification: Confidential
   - Refresh: Weekly
   - Lineage: SAP ERP + Contract Platform → Raw contract transactions
     → Cleaned spend records → Contract Spend History
     → [Finance reporting, Contract Insights Assistant]
   - Quality rules: contract_id not null (critical), spend_amount >= 0
     (critical), currency_code in approved list (warning), vendor maps
     to supplier master (critical)
   - AI permitted: spend pattern analysis, anomaly detection,
     contract utilisation reporting
   - AI prohibited: contract amendments, payment authorisations,
     vendor selection decisions
   - Human review: anomaly flagged on contracts above NOK 10M,
     spend deviates more than 25% from forecast,
     involves new vendors not in master
   - Max autonomy: read-only

3. Logistics Delay Events
   - Domain: Offshore Logistics
   - Sources: Logistics Management System, Vessel Tracking, Weather API
   - Classification: Internal
   - Refresh: Hourly
   - Lineage: Logistics System + Vessel AIS + Met.no Weather
     → Raw delay events → Enriched delay events (weather, root cause)
     → Logistics Delay Events
     → [Operations dashboard, Logistics Disruption Agent]
   - Quality rules: event_id not null (critical), delay_minutes >= 0
     (critical), root_cause_code in approved taxonomy (warning),
     vessel_id maps to fleet register (critical)
   - AI permitted: delay pattern analysis, root cause clustering,
     ETA prediction, disruption alerting
   - AI prohibited: vessel rerouting decisions, safety-critical
     operational changes, crew scheduling modifications
   - Human review: delay exceeds 48 hours, involves personnel transfer
     operations, weather severity above threshold,
     multiple cascading delays detected
   - Max autonomy: recommend

4. Inventory Availability Snapshot
   - Domain: Materials Management
   - Sources: SAP MM, Warehouse Management System
   - Classification: Internal
   - Refresh: Daily
   - Lineage: SAP MM + WMS → Raw stock movements
     → Cleaned inventory positions → Inventory Availability Snapshot
     → [Planning dashboard, Inventory Planning Assistant]
   - Quality rules: material_id not null (critical),
     stock_quantity >= 0 (critical), location_code in approved
     warehouse list (warning), reorder_point defined for
     critical items (warning)
   - AI permitted: stock level forecasting, reorder recommendations,
     consumption trend analysis
   - AI prohibited: automatic purchase order creation,
     safety stock overrides, warehouse allocation changes
   - Max autonomy: recommend

5. Maintenance Work Order History
   - Domain: Operations
   - Sources: SAP PM, Inspection Database, IoT Sensor Platform
   - Classification: Restricted
   - Refresh: Daily
   - Lineage: SAP PM + Inspections + IoT Sensors → Raw work orders
     → Enriched work orders (failure codes, sensor context)
     → Maintenance Work Order History
     → [Reliability dashboard, Maintenance Planning Agent]
   - Quality rules: work_order_id not null (critical),
     equipment_id maps to asset register (critical),
     failure_code in approved taxonomy (critical),
     completion_date not before creation_date (critical)
   - AI permitted: failure pattern analysis, predictive maintenance
     indicators, maintenance backlog prioritisation
   - AI prohibited: maintenance schedule changes on safety-critical
     equipment, inspection interval modifications,
     compliance record alterations
   - Max autonomy: read-only

Use Faker to generate realistic names for owners and stewards
(Norwegian-sounding names preferred).
Use realistic dates (created in 2023-2024, last updated in 2025-2026).
Generate proper contract versions (e.g. "v2.1", "v1.4").

Import the Pydantic models from src.models and validate all data
through them before saving.
Save as data/data_products.json with indent=2.
Print a summary: product name, domain, classification,
number of quality rules, readiness dimensions filled.
```

**Verification:** `python generate_data.py` outputs 5 products. `cat data/data_products.json | python -m json.tool | head -30` shows valid JSON.

---

### Prompt 4: Readiness scoring engine

**What it does:** Scores each data product across 8 governance dimensions on a 0–100 scale.
**Design decision:** The 8 dimensions (ownership, documentation, lineage, quality, access rules, AI usage policy, freshness, human escalation) were chosen to match the governance capabilities described in the Aker BP job description. Each dimension has specific, auditable scoring criteria — not subjective ratings.
**Why weighted:** Not all dimensions matter equally. Ownership, lineage, quality, and AI usage policy are weighted at 15% each because they are the dimensions most likely to cause AI failures if missing. Freshness and human escalation are at 10% because they are important but less foundational.

```
In ai-ready-data-product-registry/src/readiness_score.py, create the
AI-readiness scoring engine.

Score a DataProduct across 8 dimensions on a 0-100 scale,
then produce a weighted total.

Dimensions and scoring logic:

1. Ownership (weight: 15%)
   - business_owner exists and non-empty: +40
   - technical_owner exists and non-empty: +30
   - data_steward exists and non-empty: +30

2. Documentation (weight: 10%)
   - description exists and is > 50 chars: +40
   - documentation_url is not None: +30
   - known_limitations list is non-empty: +30

3. Lineage (weight: 15%)
   - lineage list has >= 3 nodes: +40
   - lineage covers at least "source" and "product" layers: +30
   - lineage includes a "consumer" layer: +30

4. Quality (weight: 15%)
   - has at least 1 quality rule: +30
   - has at least 1 "critical" severity rule: +30
   - has >= 3 quality rules total: +40

5. Access rules (weight: 10%)
   - classification is set and not "Public": +50
   - data_contract.required_metadata_fields has >= 3 fields: +50

6. AI usage policy (weight: 15%)
   - permitted_uses has >= 2 entries: +25
   - prohibited_uses has >= 1 entry: +25
   - human_review_triggers has >= 1 trigger: +25
   - max_autonomy_level is not "full-autonomous": +25

7. Freshness (weight: 10%)
   - refresh_frequency is set: +50
   - data_contract.freshness_sla is set and non-empty: +50

8. Human escalation (weight: 10%)
   - human_review_triggers has >= 2 triggers: +50
   - data_contract.escalation_contact is set and non-empty: +50

Create these functions:

def score_dimension(product: DataProduct, dimension: str) -> int:
def score_all_dimensions(product: DataProduct) -> dict:
def overall_score(product: DataProduct) -> float:
def readiness_status(score: float) -> str:
    # >= 80: Ready, >= 50: Conditionally ready, < 50: Not ready
def gaps(product: DataProduct) -> list[str]:
    # Human-readable list of gaps
```

**Verification:** `python -c "from src.readiness_score import overall_score; print('OK')"` prints OK.

---

### Prompt 5: Contract validator

**What it does:** Validates whether a data contract is complete enough for production use and specifically for AI consumption.
**Design decision:** Separating "basic validity" from "AI consumption readiness" is deliberate. A data product can have a valid contract for human consumers but still not be ready for AI agents. The AI-specific requirements (permitted uses, prohibited uses, human review triggers, autonomy level, metadata field count) represent the additional governance layer that AI consumption demands. This distinction is central to the Aker BP role.

```
In ai-ready-data-product-registry/src/contract_validator.py, create
the data contract validation engine.

Create a Pydantic model:

class ValidationResult(BaseModel):
    is_valid: bool
    missing_fields: list[str]
    warnings: list[str]
    ai_consumption_allowed: bool
    ai_consumption_conditions: list[str]
    risk_level: Literal["low", "medium", "high"]

Create these functions:

def validate_contract(contract: DataContract) -> ValidationResult:
    """
    Required for basic validity:
    - contract_version, consumers (>= 1), quality_rules (>= 1),
      freshness_sla, escalation_contact

    Additionally required for AI consumption:
    - ai_consumers (>= 1), permitted_uses (>= 1),
      prohibited_uses (>= 1), human_review_triggers (>= 1),
      max_autonomy_level != "full-autonomous",
      required_metadata_fields (>= 3)

    Risk level:
    - high: missing basic validity fields
    - medium: valid but missing AI consumption fields
    - low: all fields complete

    Warnings: contract not reviewed in 6 months,
    fewer than 3 quality rules, no prohibited AI uses
    """

def ai_consumer_summary(product: DataProduct) -> dict:
    """Returns can_consume, status, permitted/prohibited actions,
    conditions, required human approval."""
```

**Verification:** `python -c "from src.contract_validator import validate_contract; print('OK')"` prints OK.

---

## Phase 2 — Visualisation (Prompts 6–8)

### Prompt 6: Lineage diagram generator

**What it does:** Generates Mermaid flowchart code from a data product's lineage chain.
**Design decision:** Nodes are styled by layer (source = blue, raw = gray, cleaned = amber, product = teal with bold border, consumer = purple). This visual language makes it immediately clear where data originates, where it is transformed, and where it is consumed. The product node is visually emphasised because that is the governed asset.

```
In ai-ready-data-product-registry/src/lineage.py, create a function
that generates a Mermaid diagram string from a DataProduct's lineage.

def generate_mermaid(product: DataProduct) -> str:
    """
    Generate a Mermaid flowchart (top-down).
    Rules:
    - Use 'graph TD'
    - Simple alphanumeric IDs (A, B, C, D, E, F...)
    - Labels: "System Name<br/><small>layer</small>"
    - Connect in order, branch for multiple consumers
    - Style by layer:
        source: fill:#E6F1FB, stroke:#185FA5
        raw: fill:#F1EFE8, stroke:#5F5E5A
        cleaned: fill:#FAEEDA, stroke:#854F0B
        product: fill:#E1F5EE, stroke:#0F6E56, stroke-width:3px
        consumer: fill:#EEEDFE, stroke:#534AB7
    """
```

**Verification:** `python -c "from src.lineage import generate_mermaid; print('OK')"` prints OK.

---

### Prompt 7: Lineage rendering fix

**What it does:** Replaces broken streamlit-mermaid with a reliable CDN-based Mermaid renderer.
**Why this was needed:** The streamlit-mermaid package had rendering issues. The fix uses Mermaid JS loaded from CDN inside a Streamlit HTML component. This is a more reliable approach for portfolio demos.

```
The Mermaid lineage diagrams in app.py are not rendering properly.
Replace st_mermaid() calls with a CDN-based fallback:

import streamlit.components.v1 as components

def render_mermaid(mermaid_code: str, height: int = 500):
    html_content = f"""
    <div style="background: white; padding: 20px; border-radius: 8px;">
        <pre class="mermaid">
        {mermaid_code}
        </pre>
    </div>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs';
        mermaid.initialize({{ startOnLoad: true, theme: 'neutral',
            flowchart: {{ useMaxWidth: true, htmlLabels: true }} }});
    </script>
    """
    components.html(html_content, height=height, scrolling=True)

Fix src/lineage.py node IDs to be simple alphanumeric.
Remove streamlit-mermaid from requirements.txt.
```

**Verification:** All 5 data products render visible, properly colored lineage diagrams.

---

### Prompt 8: Streamlit app — initial build

**What it does:** Wires all modules into a 5-tab Streamlit application.
**Design decision:** Tabs were chosen over sidebar navigation because the content is parallel (catalogue, scores, contracts, AI view, lineage), not hierarchical. Each tab is self-contained — a reviewer can jump to any tab and understand it without context from other tabs.

```
Build the full Streamlit app in app.py.
Load data from data/data_products.json.

5 tabs:
1. Catalogue — grid of products, metadata, ownership
2. Readiness scores — dimension breakdown, gaps
3. Data contracts — structured view, validation
4. AI consumer view — can an agent use this product?
5. Lineage — Mermaid diagrams

Use st.set_page_config(page_title="AI-Ready Data Product Registry",
layout="wide").
Use native Streamlit components. Minimal custom CSS.
Import from all src/ modules.
Handle missing data gracefully.
```

**Verification:** `streamlit run app.py`. All 5 tabs load with correct data.

---

## Phase 3 — Enhancement (Prompts 9–14)

### Prompt 9: Realistic data imperfections

**What it does:** Replaces perfect-score data with deliberately imperfect products.
**Why this matters:** An Aker BP reviewer who sees five perfect 100-score data products will dismiss the project as a toy demo. Real industrial data has gaps: missing stewards, stale contract reviews, incomplete lineage, no escalation contacts. The imperfections were designed to be realistic and specific — "Contract not reviewed in 6+ months" and "No data steward assigned" are real governance problems in enterprise environments. The scores now range from 78 to 93, with each product having 1–3 specific, named gaps.

```
Expand the data models and introduce realistic imperfections.

Add extended metadata fields to DataProduct: record_count, size_mb,
schema_fields, tags, related_products, governance_status,
retention_policy, usage metrics (total_consumers,
api_calls_last_30_days, unique_users_last_30_days, shares),
api access info (endpoint, rate_limit, key_required).

Introduce deliberate imperfections:
- Product 1 (Supplier Performance): 92-95 score, missing docs URL
- Product 2 (Contract Spend): 85-88 score, no steward, stale contract
- Product 3 (Logistics Delays): 88-91 score, weak quality rules
- Product 4 (Inventory): 78-82 score, no steward, no escalation, no SLA
- Product 5 (Maintenance): 86-90 score, incomplete lineage
```

**Verification:** `python generate_data.py` shows mixed scores. No product scores 100.

---

### Prompt 10: AI model registry

**What it does:** Adds 6 AI models spanning agents, predictive models, NLP, recommendation engines, and anomaly detectors.
**Design decision:** Each model has OKRs (demonstrating product ownership thinking), evaluation history with pass/fail results (demonstrating model governance), and explicit data product dependencies with quality floor requirements (demonstrating the connection between data governance and AI governance). The models are at different lifecycle stages — Production, Staging, Development — to show the full governance lifecycle. The Maintenance Planning Agent is classified as "Critical" risk with read-only autonomy because it touches safety-critical equipment, which is realistic for offshore energy operations.

```
Create src/models.py additions for ModelEvaluation, ModelOKR, AIModel.
Create generate_ai_models.py with 6 models:

1. Supplier Risk Agent — LangGraph multi-agent, Production, Approved
2. Contract Insights Assistant — single LLM NLP, Production, Approved
3. Logistics Disruption Agent — LangGraph agent, Staging, Under review
4. Inventory Planning Assistant — XGBoost, Production, Approved
5. Maintenance Planning Agent — LSTM+RF, Production, Restricted (safety)
6. Procurement Anomaly Detector — Isolation Forest, Development, Draft

Each has: description, OKRs with status, evaluations with scores,
data product dependencies, ownership, governance classification,
allowed/prohibited actions, human oversight rules.
```

**Verification:** `python generate_ai_models.py` creates 6 models. Mixed statuses and governance states.

---

### Prompt 11: Users and approval workflows

**What it does:** Adds 10 dummy users with roles, 8 API keys, and 6 approval requests.
**Design decision:** The user roles map to a real governance structure: Platform Admin, Domain Leads, Data Product Owners, Data Stewards, AI Model Owners, Governance Leads, and Consumers. The approval requests include Pending, Approved, Rejected, and Escalated statuses to show the full workflow. This demonstrates understanding that governance is not just documentation — it is people, roles, and decision chains.

```
Create User, APIKey, ApprovalRequest models.
Create generate_users.py:
- 10 users (Norwegian names, Faker nb_NO locale)
- 8 API keys (5 for data products, 3 for AI models)
- 6 approval requests (mixed statuses including escalated)

Roles: Platform Admin, Domain Lead, Data Product Owner,
Data Steward, AI Model Owner, Governance Lead,
Data Consumer, AI Consumer.
```

**Verification:** `python generate_users.py` creates users.json, api_keys.json, approval_requests.json.

---

### Prompt 12: Data mesh architecture

**What it does:** Generates a data mesh architecture diagram and domain maturity assessment.
**Why this is important:** The Aker BP job description references distributed data ownership and federated governance — core data mesh principles. This module visualises the 4 mesh principles (domain ownership, data as a product, self-serve platform, federated governance) and scores the registry against them. It connects the tactical work (individual data products) to the strategic architecture.

```
Create src/data_mesh.py:
- generate_mesh_diagram(): Mermaid diagram showing 5 domains,
  central platform, data product and AI model connections
- domain_summary(): domain maturity assessment
- mesh_principles_status(): score the 4 data mesh principles
```

**Verification:** Valid Mermaid output. Domain summaries include maturity levels.

---

### Prompt 13: Process maps

**What it does:** Generates Procure-to-Pay and Maintenance process flow diagrams showing where data products and AI models are active.
**Why this matters:** This is the bridge between the governance layer and the operational reality. A Procure-to-Pay process map with data products and AI models mapped to specific steps proves understanding of where these tools sit in real business workflows — not just how to build them, but where they create value.

```
Create src/process_maps.py:
- generate_p2p_process_map(): 8-step P2P flow with data product
  and AI model connections at each step
- generate_maintenance_process_map(): 7-step maintenance flow
- get_process_list(): metadata for available maps
```

**Verification:** Valid Mermaid output for both process maps.

---

### Prompt 14: Full app rebuild with 8 tabs

**What it does:** Integrates all new modules into a comprehensive 8-tab application.
**Tabs:** Data catalogue, AI model registry, Readiness scores, Data contracts, AI consumption, Lineage (with mesh and process map views), Governance, Process maps.
**Design decision:** The app was rebuilt rather than patched because the addition of AI models, users, and governance workflows changed the information architecture. A patch approach would have produced inconsistent UX.

```
Rebuild app.py with 8 tabs integrating all modules:
1. Data catalogue — extended metadata, usage metrics, JSON viewer
2. AI model registry — OKRs, evaluations, dependencies
3. Readiness scores — dimension breakdown, AI impact
4. Data contracts — validation, JSON view
5. AI consumption — consumer summary, model requirements
6. Lineage — product lineage, mesh diagram, process maps
7. Governance — users, API keys, approvals, mesh health
8. Process maps — P2P and Maintenance with model coverage
```

**Verification:** All 8 tabs load with full data.

---

## Phase 4 — Enhancement patches (Patches A–D)

### Patch A: Token consumption charts

**What it does:** Adds 6 months of token usage data and consumption charts for generative AI models.
**Design decision:** Only the 3 generative models (Supplier Risk Agent, Contract Insights Assistant, Logistics Disruption Agent) show token charts. The 3 traditional ML models (XGBoost, LSTM, Isolation Forest) display an info message explaining token tracking does not apply. This distinction demonstrates understanding of the operational cost differences between generative and non-generative AI. For multi-model agents, sub-model breakdowns show Haiku doing high-volume cheap scanning and Sonnet doing expensive reasoning — a real architectural cost pattern.

```
Create TokenUsage, SubModelUsage, ModelTokenConsumption models.
Create generate_token_usage.py with 6 months of data (Dec 2025 - May 2026).

Generative models get realistic token profiles:
- Supplier Risk Agent: multi-model, Haiku scanner + Sonnet synthesiser
- Contract Insights: single model, Haiku only, seasonal spike
- Logistics Disruption: multi-model, staging volume (lower)

Non-generative models: all zeros with info message.

Cost rates: Haiku ($0.25/$1.25 per M tokens), Sonnet ($3/$15 per M tokens).
Budget utilisation tracking with warnings at 80% and 95%.

Add charts to AI consumption tab: line charts for token trends,
stacked bars for sub-model breakdown, budget metrics.
```

---

### Patch B: AI model architecture diagrams

**What it does:** Adds a viewable architecture diagram for each AI model.
**Design decision:** Each model type gets a distinct visual style. LangGraph agents show orchestration flows with scanner/synthesiser separation and governance gates. Traditional ML models show feature engineering pipelines. The Maintenance Planning Agent diagram has a prominent red "safety gate" node because all outputs require mandatory human review on safety-critical equipment. The architecture diagrams make the AI models tangible — a reviewer can see exactly how data flows through each model and where governance controls are applied.

```
Create src/model_architecture.py:
- 6 unique Mermaid architecture diagrams
- Agents: multi-step LangGraph flows with governance gates
- Single LLMs: context → model → validation pipelines
- Traditional ML: feature engineering → model → output pipelines
- Safety-critical models: prominent safety gate nodes

Add to AI model registry tab as a section between description and OKRs.
Auto-generate caption describing model type and dependencies.
```

---

### Patch C: UI improvements

**What it does:** Adds custom CSS for consistent styling, reusable badge components, card layouts, and visual spacing.
**Design decision:** All visual changes only — no logic modifications. CSS classes replace inline styles for consistency. st.container(border=True) creates card layouts. Badges use a 7-colour system (green, amber, gray, red, coral, purple, blue) mapped to governance and lifecycle statuses.

```
Add global CSS: metric card styling, tab spacing, badge classes.
Create badge() and render_badges() helper functions.
Replace all inline badge HTML with CSS class approach.
Add st.container(border=True) card layouts.
Consistent st.divider() spacing between sections.
Visual-only changes — no business logic modifications.
```

---

### Patch D: About text update

**What it does:** Updates the sidebar About section and footer.
**Positioning:** "A portfolio project built to showcase product management, AI, and data governance knowledge."

```
Update sidebar About expander with portfolio positioning.
Update footer caption.
List demonstrated skills: data product ownership, AI model governance,
data mesh architecture, readiness scoring, process mapping,
token monitoring, governance workflows.
```

---

## Prompt engineering principles applied

**1. Incremental delivery:** Each prompt produces a testable increment with a verification checkpoint. No prompt depends on assumptions about previous outputs.

**2. Separation of concerns:** Data models, business logic, visualisation, and UI are in separate prompts and separate files. This makes debugging straightforward and allows any module to be replaced independently.

**3. Domain specificity over generic generation:** Quality rules, AI policies, lineage chains, and human-review triggers were hand-specified in prompts, not randomly generated. The domain realism is the product — the code is the delivery mechanism.

**4. Deliberate imperfection:** Perfect data was replaced with realistic gaps because the goal is to demonstrate governance thinking, not data quality. An 85-score product with named gaps is more credible than a 100-score product with none.

**5. Human judgment at every gate:** Warp generated the code. I made the architecture decisions, chose the governance dimensions, designed the data mesh structure, specified the process maps, and reviewed every output against industrial realism. The AI was the tool. The product thinking was mine.

---

## What this project demonstrates

| Skill area | Evidence in this project |
|---|---|
| Data product ownership | 5 governed products with metadata, contracts, quality rules, lineage |
| AI model governance | 6 models with OKRs, evaluations, risk classification, autonomy controls |
| Data mesh architecture | 5-domain mesh with federated governance assessment |
| AI-readiness assessment | 8-dimension scoring framework with weighted composite |
| Data contracts | Structured contracts with AI-specific validation |
| Process integration | P2P and Maintenance process maps with model coverage |
| Governance workflows | Users, roles, approvals, API keys, escalation chains |
| AI cost management | Token consumption tracking with sub-model breakdown |
| Industrial domain knowledge | Energy-sector terminology, safety classifications, Norwegian operational context |
| AI-assisted development | Structured prompt engineering with incremental delivery |
