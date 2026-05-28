# Data & Governance Portfolio Lab

##Background and the idea behind this
I built this as a non-conventional way to show my knowledge and what I have worked with in my current and previous roles. It is difficult to show knowledge and contribution as a product manager especially in a highly regulated environment. This static/mock up app was built by me using THE FOLLOWING
- A detailed documentation of my knowledge
- Chatgpt to structure the knowledge
- A detailed documentation of prompts
- Claude opus 4.7 to enhance the prompt and select the stack - python and streamlit in this case
- Warp as the developer terminal and environment
- Three different AI models working on different aspects - Deepseek V4, Claude 4.6 sonnet & Claude 4.7 Opus

# Mock up app & product description
This platform demonstrates how enterprise data products and AI models can be structured, documented, and governed so they are safe for analytics and AI-agent consumption in industrial environments.
A Streamlit application demonstrating how enterprise data products and AI models can be structured, documented, and governed for safe consumption in industrial environments. Inspired by platforms like Collibra, combined with AI model governance and data mesh architecture principles.

## Why this matters

AI agents and LLM-based systems increasingly need to consume enterprise data. But consuming raw, ungoverned data creates risks: hallucinations built on stale data, autonomous actions taken without authorisation, recommendations with no traceable source. Data products need clear ownership, quality rules, lineage, access controls, and explicit AI usage policies before agents can be trusted to act on them.

Beyond data governance, organisations deploying AI models need visibility into model performance, data dependencies, ownership, and the approval chains that control access. This platform demonstrates how data product governance and AI model governance connect — because an AI model is only as trustworthy as the data products it consumes.

## Features

### Data product catalogue
- Browse 5 enterprise data products across procurement, logistics, contract management, materials, and operations
- View full metadata, schema, ownership, usage metrics, governance status, and sharing statistics
- Realistic imperfections — not every product scores perfectly, showing real governance gaps
- Inspect raw JSON data and schema definitions

### AI model registry
- Browse 6 AI models spanning agents, predictive models, NLP models, and anomaly detectors
- View model descriptions, OKRs, evaluation history, and data dependencies
- See which data products each model consumes and whether they meet quality requirements
- Models span the full lifecycle: Development → Staging → Production

### AI-readiness scoring
- Score each data product across 8 governance dimensions (ownership, documentation, lineage, quality, access, AI policy, freshness, escalation)
- Compare products side by side
- See impact on dependent AI models when readiness scores are insufficient

### Data contracts & validation
- Validate contract completeness for production and AI consumption
- View contracts as structured data or raw JSON
- See which AI models are bound by each contract

### AI consumption view
- Answer: "Can an AI agent use this data product, and under what conditions?"
- Show permitted/prohibited actions, autonomy levels, and human oversight requirements
- Cross-reference with registered AI models consuming the product

### Data mesh architecture
- Visualise domain ownership, federated governance, and cross-domain data flows
- Assess the 4 data mesh principles: domain ownership, data as product, self-serve platform, federated governance

### Governance & access
- User directory with roles and approval permissions
- API key management with scoped access and simulated request workflow
- Approval workflow tracking (pending, approved, rejected, escalated)
- Governance health assessment across all 4 mesh principles

### Process maps
- Procure-to-Pay process map showing where data products and AI models are active
- Maintenance & Reliability process map
- Model coverage summary per process

## Tech stack

- Python 3.10+
- Streamlit
- Pydantic v2 (data validation and schemas)
- Faker (synthetic data generation)
- Mermaid via CDN (architecture and lineage diagrams — no extra dependency)

## Run locally

```bash
git clone https://github.com/TMayowa/ai-ready-data-product-registry.git
cd ai-ready-data-product-registry
pip install -r requirements.txt
python generate_data.py
python generate_ai_models.py
python generate_users.py
python -m streamlit run app.py
```

## Project structure

```
ai-ready-data-product-registry/
├── app.py                      # Streamlit application (8 tabs)
├── generate_data.py            # Synthetic data product generator
├── generate_ai_models.py       # Synthetic AI model generator
├── generate_users.py           # Synthetic users, API keys, approvals
├── requirements.txt
├── data/
│   ├── data_products.json        (5 products, realistic imperfections)
│   ├── ai_models.json            (6 models, mixed statuses)
│   ├── users.json                (10 users, mixed roles)
│   ├── api_keys.json             (8 keys, mixed statuses)
│   └── approval_requests.json    (6 requests, mixed statuses)
├── src/
│   ├── models.py                 # All Pydantic models
│   ├── readiness_score.py        # AI-readiness scoring engine
│   ├── contract_validator.py     # Data contract validation
│   ├── lineage.py                # Mermaid lineage generator
│   ├── data_mesh.py              # Data mesh architecture and principles
│   └── process_maps.py           # Business process flow maps
└── screenshots/
```

## Data mesh architecture

This platform models a data mesh with 5 domains:

| Domain | Data Products | AI Models | Maturity |
|--------|--------------|-----------|----------|
| Procurement | Supplier Performance Summary | Supplier Risk Agent, Procurement Anomaly Detector | Measured |
| Contract Management | Contract Spend History | Contract Insights Assistant | Managed |
| Offshore Logistics | Logistics Delay Events | Logistics Disruption Agent | Managed |
| Materials Management | Inventory Availability Snapshot | Inventory Planning Assistant | Managed |
| Operations | Maintenance Work Order History | Maintenance Planning Agent | Measured |

## Sample data products

| Product | Domain | Classification | AI autonomy level | Gov Status |
|---------|--------|---------------|-------------------|------------|
| Supplier Performance Summary | Procurement | Internal | Recommend | Approved |
| Contract Spend History | Contract Management | Confidential | Read-only | Under review |
| Logistics Delay Events | Offshore Logistics | Internal | Recommend | Approved |
| Inventory Availability Snapshot | Materials Management | Internal | Recommend | Draft |
| Maintenance Work Order History | Operations | Restricted | Read-only | Approved |

## What this demonstrates

- Defining data products as governed, documented assets with clear ownership and consumer contracts
- Scoring enterprise data for AI-readiness across multiple governance dimensions
- Validating data contracts for completeness before AI agents are permitted to consume
- Modelling permitted, prohibited, and conditional AI usage rules per data product
- Mapping data lineage from source systems through transformation layers to AI consumers
- Registering AI models with evaluations, OKRs, and data dependency tracking
- Implementing approval workflows and API key governance
- Assessing data mesh maturity across 4 principles

## Disclaimer

This project uses fully synthetic data generated for portfolio and demonstration purposes. It does not contain real company data, proprietary architecture, internal system names, operational records, supplier information, or confidential material. Data product and AI model structures are inspired by industrial energy-sector patterns but are entirely fictional.

---
Built by Mayowa Togun | [GitHub](https://github.com/TMayowa)
