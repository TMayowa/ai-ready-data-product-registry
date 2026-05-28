# Product Requirements Document
## AI-Ready Data Product Registry & Governance Platform

**Version:** 2.1
**Owner:** Mayowa Togun
**Last updated:** 2026-05-28
**Status:** Portfolio prototype — synthetic data only

---

## 1. Executive Summary

The AI-Ready Data Product Registry is a governance platform that combines a data product catalogue, an AI model registry, and a data mesh assessment framework. It demonstrates how an enterprise can structure, document, and govern both data products and AI models so they are safe for human and AI-agent consumption in industrial environments.

The product addresses a specific gap in enterprise AI deployment: organisations have data catalogues (like Collibra) and they have AI/ML platforms (like Azure ML, Databricks), but they rarely connect the two with explicit governance contracts that say *"AI agent X is permitted to consume data product Y under conditions Z."* This platform shows what that connection looks like in practice.

This is a portfolio project built with fully synthetic data. It is not a production system. Its purpose is to demonstrate product management, AI governance, and data governance thinking at a level appropriate for senior PM, governance lead, or AI strategy roles in industrial sectors (energy, manufacturing, logistics).

---

## 2. Problem Statement

### The trigger
AI agents and LLM-based systems are increasingly being deployed inside enterprises to consume operational data. They generate recommendations, flag risks, surface insights, and in some cases take autonomous actions. The business value is real. The governance risk is also real.

### What goes wrong without governance
1. **Hallucinations on stale or low-quality data.** An LLM cheerfully summarises a supplier risk report from data that is three weeks out of date. The category manager acts on it.
2. **Autonomous actions without authority.** An agent triggers a purchase order because nobody defined an explicit "no-autonomous-procurement" rule.
3. **Untraceable recommendations.** A reliability engineer cannot trace why the maintenance AI flagged a specific pump as failure-prone, because the data lineage is incomplete.
4. **Cross-domain leakage.** A logistics AI starts using procurement data without the procurement domain owners knowing.
5. **No clear escalation paths.** When the AI is wrong, nobody knows who to escalate to.

### The underlying problem
Data products and AI models are governed separately, by different teams, with different vocabularies, different review cycles, and different approval gates. The connections between them — *"this AI model depends on this data product, with these quality requirements, and these autonomy constraints"* — are usually tribal knowledge sitting in confluence pages and slack threads.

### Who feels this pain
- **Domain leads** (procurement, operations, logistics) trying to ensure AI deployed in their domain does not embarrass or expose the business
- **Governance leads** trying to enforce policy across a mesh of decentralised data products and AI models
- **Data product owners** who do not know which AI models depend on their product
- **AI model owners** who do not know which data products they can safely consume
- **Compliance and audit teams** who need a single source of truth for AI-data interactions

---

## 3. Goals and Non-Goals

### Goals
1. Demonstrate a unified governance view across data products and AI models
2. Make AI-readiness scoring transparent and auditable
3. Show realistic governance gaps, not a glossy "everything is perfect" demo
4. Make data mesh principles concrete and assessable
5. Provide a portfolio artefact that demonstrates product, AI, and data governance skills

### Non-Goals
- Not a production data catalogue (no real data ingestion, no live API)
- Not a replacement for Collibra, Alation, or any commercial catalogue
- Not an AI model serving platform (no model deployment, no inference)
- Not a real authentication system (users and approvals are display-only)
- Not domain-specific to one industry, though examples use industrial-energy patterns

---

## 4. Target Users and Personas

### Primary personas

**Domain Lead — Procurement** (decision-maker)
- Owns procurement data products and AI models in their domain
- Approves data access requests and AI model deployments
- Needs to see governance health at a glance and act on pending approvals
- Cares about: governance status, risk classification, pending approvals

**Governance Lead** (policy enforcer)
- Owns cross-domain policy
- Approves high-risk AI models and API key requests
- Needs visibility into mesh principles, federated governance status
- Cares about: governance health scores, escalations, audit traceability

**Data Product Owner** (asset owner)
- Owns a specific data product end-to-end
- Maintains the data contract, quality rules, lineage
- Needs to know who consumes their product and whether quality meets AI requirements
- Cares about: readiness scores, gaps, AI consumer dependencies, sharing metrics

**AI Model Owner** (ML/AI builder)
- Owns one or more AI models or agents
- Tracks evaluations, OKRs, and model lifecycle
- Needs to know if their input data products meet quality requirements
- Cares about: model evaluations, data dependencies, governance status, autonomy level

### Secondary personas

**Data Consumer / AI Consumer** (read-only user)
- Browses the catalogue to find data products or AI models to use
- Requests API keys for specific resources
- Cares about: discoverability, AI consumption permissions, conditions of use

**Platform Admin** (platform owner)
- Operates the platform, sees everything
- Cares about: aggregate metrics, system health, user roles

---

## 5. User Stories

### Catalogue and discovery
- As a Domain Lead, I want to browse all data products in my domain so I know what I am responsible for governing
- As a Data Consumer, I want to search and filter data products by classification, refresh frequency, and governance status so I can find what I need
- As anyone, I want to see usage metrics (API calls, unique users) so I understand which products are valuable

### AI model registry
- As an AI Model Owner, I want to see all registered AI models so I avoid duplicating work
- As a Governance Lead, I want to filter AI models by risk classification so I can prioritise reviews
- As a Domain Lead, I want to see the OKRs and evaluation history of AI models in my domain so I can assess their health

### Readiness and quality
- As a Data Product Owner, I want a clear score telling me how AI-ready my product is and which dimensions need improvement
- As an AI Model Owner, I want to know if my input data products meet my minimum quality requirements before I deploy
- As a Governance Lead, I want to compare two data products side by side so I can identify systemic governance gaps

### Contracts and consumption
- As a Data Consumer, I want to know if I can use a data product for AI agent consumption and under what conditions
- As an AI Model Owner, I want to see which contracts bind my model
- As anyone, I want to inspect a contract as JSON so I can verify its structure programmatically

### Lineage and architecture
- As anyone, I want to see how data flows from source systems through transformations to AI consumers
- As a Governance Lead, I want to see the full data mesh architecture so I can identify cross-domain dependencies
- As a Domain Lead, I want to see how my domain's data flows into business processes

### Token consumption (generative AI)
- As a Cost Owner, I want to see monthly token consumption per generative AI model so I can manage budgets
- As an AI Model Owner, I want to see input vs output token trends and budget utilisation
- As anyone, I want to see sub-model breakdown for multi-model agents so I understand cost drivers

### Governance and access
- As a Platform Admin, I want to see all users and their approval permissions
- As a Governance Lead, I want to see pending approval requests prominently so nothing falls through the cracks
- As a Data Consumer, I want to request a new API key through a clear workflow

---

## 6. Functional Requirements

The application is structured as an 8-tab Streamlit interface. Each tab is described as a feature area.

### Tab 1 — Data Catalogue

**Purpose:** Browse and inspect data products.

**Inputs:** 5 synthetic data products loaded from `data/data_products.json`

**Capabilities:**
- Summary metrics: total products, average readiness score, products ready for AI, most-accessed product
- Catalogue table with: product name, domain, classification, governance status badge, refresh frequency, readiness score, status badge, total consumers
- Product detail view (split into two columns):
  - **Left:** ID, domain, classification, governance status, refresh frequency, actual update lag, source systems, description, created/updated dates, documentation URL, record count, size MB, data sensitivity, retention policy, known limitations, tags
  - **Right:** Business owner, technical owner, data steward (with warning if missing), domain owner team, readiness score (large coloured number), readiness status badge, usage metrics (API calls, unique users, internal/external shares, last accessed), API access details (endpoint, rate limit, docs link)
- Schema fields table (if defined) showing column name, type, nullability, description
- "View as JSON" expander showing the full product as formatted JSON
- "Data product schema" expander showing the Pydantic JSON schema

**Acceptance criteria:**
- All 5 products appear in catalogue
- Selecting a product updates the detail view
- Products with missing data steward show a warning icon
- JSON view is valid and complete

---

### Tab 2 — AI Model Registry

**Purpose:** Browse and inspect AI models.

**Inputs:** 6 synthetic AI models loaded from `data/ai_models.json`

**Capabilities:**
- Summary metrics: total models, in production, under review, average latest evaluation score
- Model table with: name, type, status badge, governance status badge, risk classification badge, domain, autonomy level, evals passed/total
- Model detail view:
  - Header: model name and version, description paragraph
  - **Ownership & Governance column:** model owner, governance lead, owning team, status/governance/risk badges, last/next review dates
  - **Technical column:** base model, framework, infrastructure, autonomy level, API endpoint
  - **Usage column:** requests (30d), users, latency, error rate, allowed actions list, prohibited actions list, human oversight requirements
- Data Dependencies section: for each input data product, show its readiness score and whether it meets the model's minimum quality requirement
- OKRs section: each OKR with objective, status badge, progress bar, quarter, and key results
- Evaluations section: latest evaluation summary + full table (date, type, score, passed/failed, notes, evaluator)
- "View as JSON" expander

**Acceptance criteria:**
- All 6 models appear in registry
- Selected model shows all sections
- Data dependency warnings appear when score < minimum requirement
- OKR progress bars match progress_pct values

---

### Tab 3 — Readiness Scores

**Purpose:** Score data products on AI-readiness across 8 dimensions and surface gaps.

**Scoring dimensions and weights:**
1. Ownership (15%) — business owner, technical owner, data steward populated
2. Documentation (10%) — description length, docs URL, known limitations
3. Lineage (15%) — node count, layer coverage, consumer presence
4. Quality (15%) — number of quality rules, critical severity rules
5. Access rules (10%) — classification set, required metadata fields
6. AI usage policy (15%) — permitted/prohibited uses, human review triggers, max autonomy
7. Freshness (10%) — refresh frequency and SLA defined
8. Human escalation (10%) — review triggers count, escalation contact set

**Capabilities:**
- Single-product view or two-product comparison via checkbox
- Overall score as large coloured number (green ≥80, amber ≥50, red <50)
- Readiness status badge (Ready / Conditionally ready / Not ready)
- 8 dimension metric cards in 2x4 grid with weight as delta
- Gaps list with all unmet criteria
- Impact on AI consumers section: for each dependent model, show whether the current score meets its minimum requirement

**Acceptance criteria:**
- Scoring is deterministic from product data
- Side-by-side comparison shows both products with identical structure
- Gap descriptions are actionable

---

### Tab 4 — Data Contracts

**Purpose:** View and validate data contracts.

**Capabilities:**
- Contract details (two columns): version, last reviewed, freshness SLA, escalation contact, consumers, AI consumers, required metadata fields, AI models bound by this contract
- Quality rules table: field, rule description, threshold, severity (uppercase)
- Validation result: validity flag, risk level badge (low/medium/high), AI consumption allowed flag, list of missing fields, warnings
- "View contract as JSON" expander

**Validation logic:**
- Basic validity requires: contract_version, ≥1 consumer, ≥1 quality rule, freshness_sla, escalation_contact
- AI consumption additionally requires: ≥1 ai_consumer, ≥1 permitted_use, ≥1 prohibited_use, ≥1 human_review_trigger, autonomy != "full-autonomous", ≥3 required_metadata_fields
- Risk level: high if any basic field missing, medium if AI fields missing, low if all complete
- Warnings (non-blocking): contract not reviewed in 6 months, fewer than 3 quality rules, no prohibited AI uses

**Acceptance criteria:**
- Contracts with missing data steward/escalation contact show "Not defined" warnings
- Validation result is consistent across reloads
- Risk badge colour matches risk level

---

### Tab 5 — AI Consumption

**Purpose:** Answer "Can an AI agent use this data product?" and show token consumption.

**Capabilities:**
- Status indicator (Approved / Conditional / Blocked) shown as a large coloured heading
- Permitted actions list (green checkmarks) and prohibited actions list (red stop signs) side by side
- Conditions for use (if any) as info boxes
- Human approval required for: numbered list
- Max autonomy level badge with warning box if read-only
- AI Models Consuming This Product: per model, name + status badge + whether data quality meets requirement

**Token consumption section:**
- Platform-wide summary metrics: total tokens (latest month), total cost USD, most expensive model, avg cost per request
- Per-model area chart showing input vs output tokens over 6 months
- Budget metrics: monthly budget, current month cost, utilisation %
- Budget warnings: amber if >80%, red if >95%
- For multi-model agents: sub-model breakdown bar chart + table with role, tokens, cost
- Non-generative models (XGBoost, LSTM, Isolation Forest): show info message explaining token tracking does not apply

**Acceptance criteria:**
- Status correctly reflects contract validation
- Token charts render for generative models
- Non-generative models display correct info message

---

### Tab 6 — Lineage

**Purpose:** Visualise data flow as Mermaid diagrams.

**Capabilities:**
- View selector with three options:
  1. **Product lineage** — per-product flow from source through transformations to consumers
  2. **Data mesh architecture** — full mesh showing platform + 5 domains + cross-domain AI flows
  3. **Process maps** — Procure-to-Pay or Maintenance & Reliability process diagram
- Empty-state info messages until a view and option are selected
- Below each lineage diagram: table of lineage nodes with system name, layer, description

**Acceptance criteria:**
- Empty state appears on first open of the tab
- Lineage diagrams render for all 5 data products
- Mesh diagram shows all 5 domains and their AI model consumers

---

### Tab 7 — Governance

**Purpose:** Show users, API keys, approval requests, and governance health.

**Capabilities:**
- Governance Health: 4 metric cards (Domain Ownership, Data as Product, Self-Serve Platform, Federated Governance) each with score and identified gaps
- Data mesh architecture diagram in an expander
- Users table: name, role, department, domain, access level, approval permissions
- API Keys: active/expired counts, keys table (key, resource, issued to, status, scope, expires, last used)
- Active key details: expandable per-key view with issuer, issuee, dates
- "Request New API Key" form: resource dropdown, scope dropdown, justification text area, submit button
- Approval Requests: warning banner for pending requests, full table with type, resource, requester, date, status, reviewer

**Acceptance criteria:**
- Pending approval count matches global banner
- API key form submission shows success message and approval guidance
- Governance health scores reflect actual product/model state

---

### Tab 8 — Process Maps

**Purpose:** Show business process flows annotated with data products and AI models.

**Capabilities:**
- Process selector: Procure-to-Pay (8 steps) or Maintenance & Reliability (7 steps)
- Empty state prompt until selection
- Mermaid diagram showing process steps with data product and AI model contributions (dashed arrows)
- Coverage summary: count of data products, AI models, status breakdown
- Data product step table
- AI model step table
- Legend explaining node colours and arrow conventions

**Acceptance criteria:**
- Both processes render correctly
- Coverage summary counts match the diagram

---

### Sidebar (always visible)

- Title: "Data & AI Governance Platform"
- Caption: "Demonstrating enterprise data product and AI model governance for industrial environments."
- "About this platform" expander explaining the project, synthetic data, and what it demonstrates
- "Platform stats" expander with 4 metrics (data products, AI models, users, active API keys)
- GitHub link

### Global banner (above tabs)

- App title and caption
- 4 metric cards: data products, AI models with "in production" delta, average readiness score, pending approvals with attention indicator

### Footer (below tabs)

- Caption: "A portfolio project built to showcase product management, AI, and data governance knowledge. Built with synthetic data by Mayowa Togun."

---

## 7. Data Model

The platform uses Pydantic v2 models for all entities.

### Core models
- **`DataProduct`** — id, name, domain, description, ownership trio (business/technical/steward), source systems, classification, refresh frequency, lineage, data contract, known limitations, dates, plus 18 extended metadata fields (record count, schema, tags, usage metrics, API access, governance status, data sensitivity, retention policy)
- **`DataContract`** — version, last reviewed, consumers, AI consumers, required metadata fields, quality rules, freshness SLA, AI usage policy, escalation contact
- **`AIUsagePolicy`** — permitted/prohibited uses, human review triggers, max autonomy level
- **`QualityRule`** — field, description, threshold, severity (critical/warning/info)
- **`LineageNode`** — system name, layer (source/raw/cleaned/product/consumer), description

### AI model registry
- **`AIModel`** — id, name, type, description, version, status, ownership, governance, risk, technical details, data dependencies (minimum quality score), business processes, evaluations, OKRs, usage stats, autonomy controls, allowed/prohibited actions, human oversight, escalation rules
- **`ModelEvaluation`** — eval id, date, type (accuracy/fairness/robustness/latency/governance/sensitivity), dataset, score, passed flag, notes, evaluator
- **`ModelOKR`** — objective, key results, status, quarter, progress percentage

### Governance
- **`User`** — id, name, email, role, department, domain, access level, approval permissions, active flag
- **`APIKey`** — key id, masked key, resource type/id, issued to/by, dates, status, rate limit, scope, last used
- **`ApprovalRequest`** — request id, type, resource, requester, date, status, reviewer, review notes, approval level required

### Token consumption (generative models only)
- **`ModelTokenConsumption`** — model id, multi-model flag, total monthly usage, sub-model breakdown, avg tokens/request, avg cost/request, monthly budget, utilisation %
- **`TokenUsage`** — month, input/output/total tokens, cost USD, requests
- **`SubModelUsage`** — sub-model name, role, monthly usage list

All models use Pydantic v2 with explicit Literal types for enums and validation through `model_validate()`.

---

## 8. Architecture and Technology

### Stack
- **Language:** Python 3.10+
- **Framework:** Streamlit (UI), Pydantic v2 (data validation)
- **Visualisation:** Mermaid (via CDN, no extra dependency)
- **Synthetic data:** Faker (Norwegian locale for owner/steward names)
- **Charts:** Streamlit native (st.area_chart, st.bar_chart, st.metric)

### File organisation
```
ai-ready-data-product-registry/
├── app.py                      # Main Streamlit application (8 tabs)
├── generate_data.py            # Synthetic data product generator
├── generate_ai_models.py       # Synthetic AI model generator
├── generate_users.py           # Synthetic users, API keys, approvals
├── generate_token_usage.py     # Synthetic token usage data
├── requirements.txt
├── PRD.md                      # This document
├── README.md
├── data/                       # Generated JSON data files
│   ├── data_products.json
│   ├── ai_models.json
│   ├── users.json
│   ├── api_keys.json
│   ├── approval_requests.json
│   └── token_usage.json
└── src/
    ├── models.py               # All Pydantic models
    ├── readiness_score.py      # 8-dimension scoring engine
    ├── contract_validator.py   # Contract validation logic
    ├── lineage.py              # Mermaid lineage generator
    ├── data_mesh.py            # Data mesh diagram + assessment
    ├── model_architecture.py   # AI model architecture diagrams
    └── process_maps.py         # Business process maps
```

### Data flow
1. Generator scripts produce JSON files in `data/`
2. `app.py` loads all JSON at startup via cached functions
3. Pydantic models validate every record on load
4. UI components query in-memory dicts (no live recomputation except scoring)
5. Mermaid diagrams render client-side via CDN JavaScript

### Dependencies (intentional minimum)
- `streamlit>=1.30.0`
- `pydantic>=2.0.0`
- `faker>=20.0.0`
- `pandas>=2.0.0`

No external chart libraries (Plotly, matplotlib). No SQLite or database. No authentication framework. No deployment infrastructure.

---

## 9. Domain Model

The platform models a data mesh with 5 domains, each owning data products and AI models.

| Domain | Data Product | AI Model(s) |
|--------|--------------|-------------|
| Procurement | Supplier Performance Summary | Supplier Risk Agent, Procurement Anomaly Detector (cross-domain) |
| Contract Management | Contract Spend History | Contract Insights Assistant |
| Offshore Logistics | Logistics Delay Events | Logistics Disruption Agent |
| Materials Management | Inventory Availability Snapshot | Inventory Planning Assistant |
| Operations | Maintenance Work Order History | Maintenance Planning Agent |

### Deliberate imperfections (for realism)
- Supplier Performance Summary — missing documentation URL
- Contract Spend History — empty data steward, contract reviewed 8 months ago, only 2 quality rules
- Logistics Delay Events — root cause coding has 15% unclassified rate
- Inventory Availability Snapshot — empty data steward, empty escalation contact, empty freshness SLA, only 2 human review triggers, governance status Draft
- Maintenance Work Order History — lineage missing transformation (cleaned) layer

Scores range from 82 to 100 to demonstrate that real catalogues are never perfect.

---

## 10. Success Metrics (for the portfolio project)

This project is a demonstration artefact. Success is measured by what it communicates to a hiring manager or stakeholder.

### Demonstration goals
- A reviewer can understand the data mesh concept from the lineage tab alone
- A reviewer can articulate the difference between "data product readiness" and "AI model governance" after browsing for 5 minutes
- A reviewer recognises the imperfections as deliberate product thinking, not bugs
- A reviewer can describe how token consumption ties to budget and operational cost

### Implementation quality signals
- All 8 tabs load without errors on first open
- All Mermaid diagrams render correctly
- All Pydantic validation passes on synthetic data
- README reads as a serious portfolio piece, not a tutorial walkthrough

---

## 11. Constraints and Assumptions

### Constraints
- Synthetic data only; no real company data, system names, or operational records
- Single-user demo; no concurrent access patterns considered
- No persistent state changes; form submissions show success messages but do not write back
- No external API integrations; all data is local JSON
- No CI/CD; local execution only

### Assumptions
- Reviewer has Python 3.10+ installed
- Reviewer can run `pip install -r requirements.txt`
- Reviewer is familiar with Streamlit basics
- Reviewer is comfortable interpreting a data mesh

---

## 12. Out of Scope

Explicitly out of scope for this version:

- Real authentication or RBAC enforcement
- Actual API key generation, storage, or rotation
- Live data ingestion from real source systems
- Real AI model invocation
- Database backend (data is JSON files)
- Multi-tenancy
- Audit logging beyond the displayed approval history
- Mobile-responsive layout
- Localisation beyond English
- Real-time updates between users

---

## 13. Future Considerations

If this prototype were to evolve into something more substantial, plausible next steps would be:

### Near-term (still as a portfolio artefact)
- Add a "Governance scorecard" PDF export per domain
- Add a search/filter bar across the catalogue
- Add a model comparison view (similar to product comparison)
- Add automated PRD/contract generation for new products

### Medium-term (toward a real product)
- Backed by a real database (Postgres or DuckDB)
- Real user authentication via SSO
- Webhook integration with real data catalogues (Collibra, Atlan, Datahub)
- Real approval workflows with email notifications
- Real-time token consumption from LLM provider APIs

### Long-term (productisation)
- Connector framework for real data sources (SAP, S3, Snowflake)
- Policy-as-code engine for AI usage policies
- Continuous evaluation pipeline for registered AI models
- Mesh-level cost allocation and chargeback

These are speculative directions, not commitments.

---

## 14. Open Questions

- Should governance status (Draft / Under review / Approved) be reviewable in-app, or remain read-only?
- Is "Maturity level" (Managed / Measured / Optimising) the right framing for domain assessment, or would something simpler work better for non-data-mesh-literate reviewers?
- Should the AI consumption tab consolidate with the AI Model Registry tab, or remain separate?
- Is there value in showing failed Pydantic validation errors as warnings, rather than silently skipping?

---

## 15. Glossary

- **Data product** — A governed, documented dataset with explicit ownership, contract, and consumers
- **Data contract** — A formal specification of a data product's quality rules, consumers, AI usage policy, and SLAs
- **AI-readiness score** — A 0-100 weighted score across 8 governance dimensions indicating whether a data product is suitable for AI consumption
- **Data mesh** — A decentralised data architecture where domain teams own their data products, supported by a federated governance layer
- **Federated governance** — Governance policies set centrally but enforced per domain
- **Max autonomy level** — The highest level of action an AI model is permitted to take with a data product (read-only / recommend / act-with-approval / full-autonomous)
- **Human review triggers** — Conditions under which a human must review an AI output before action
- **OKR** — Objective and Key Results; a goal-setting framework used for AI model lifecycle goals
- **Sub-model** — A constituent LLM within a multi-model agent (e.g. a Haiku scanner + Sonnet synthesiser inside a LangGraph agent)

---

## 16. References

- Data mesh — Zhamak Dehghani, *Data Mesh: Delivering Data-Driven Value at Scale* (O'Reilly, 2022)
- Pydantic v2 documentation — https://docs.pydantic.dev
- Streamlit documentation — https://docs.streamlit.io
- Mermaid documentation — https://mermaid.js.org

---

**Document end.**

*Prepared by Mayowa Togun as part of the AI-Ready Data Product Registry portfolio project.*
