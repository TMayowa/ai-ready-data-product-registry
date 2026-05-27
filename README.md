# AI-Ready Data Product Registry & Readiness Validator

A Streamlit application demonstrating how enterprise data products can be structured, documented, and governed so they are safe for analytics and AI-agent consumption.

## Why this matters

AI agents and LLM-based systems increasingly need to consume enterprise data. But consuming raw, ungoverned data creates risks: hallucinations built on stale data, autonomous actions taken without authorisation, recommendations with no traceable source. Data products need clear ownership, quality rules, lineage, access controls, and explicit AI usage policies before agents can be trusted to act on them.

This project demonstrates what that governance layer looks like in practice.

## Features

- **Data product catalogue** — Browse 5 sample data products across procurement, logistics, contract management, materials, and operations
- **AI-readiness scoring** — Score each product across 8 dimensions (ownership, documentation, lineage, quality, access, AI policy, freshness, escalation) with a 0-100 composite score
- **Data contract validation** — Check whether a data contract is complete enough for production use and AI consumption
- **AI consumer view** — Answer the question: "Can an AI agent use this data product, and under what conditions?"
- **Lineage visualisation** — Trace data flow from source systems through transformation layers to consumer applications and AI agents

## Tech stack

- Python 3.10+
- Streamlit
- Pydantic v2 (data validation and contract schemas)
- Faker (synthetic data generation)
- Mermaid (lineage diagrams)

## Run locally

```bash
git clone https://github.com/TMayowa/ai-ready-data-product-registry.git
cd ai-ready-data-product-registry
pip install -r requirements.txt
python generate_data.py
streamlit run app.py
```

## Project structure

```
ai-ready-data-product-registry/
├── app.py                    # Streamlit application
├── generate_data.py          # Synthetic data generator
├── requirements.txt
├── README.md
├── data/
│   └── data_products.json    # Generated sample data
├── src/
│   ├── __init__.py
│   ├── models.py             # Pydantic data models
│   ├── readiness_score.py    # AI-readiness scoring engine
│   ├── contract_validator.py # Data contract validation
│   └── lineage.py            # Mermaid lineage generator
└── screenshots/
```

## Sample data products

| Product | Domain | Classification | AI autonomy level |
|---------|--------|---------------|-------------------|
| Supplier Performance Summary | Procurement | Internal | Recommend |
| Contract Spend History | Contract Management | Confidential | Read-only |
| Logistics Delay Events | Offshore Logistics | Internal | Recommend |
| Inventory Availability Snapshot | Materials Management | Internal | Recommend |
| Maintenance Work Order History | Operations | Restricted | Read-only |

## What this demonstrates

- Defining data products as governed, documented assets with clear ownership and consumer contracts
- Scoring enterprise data for AI-readiness across multiple governance dimensions
- Validating data contracts for completeness before AI agents are permitted to consume
- Modelling permitted, prohibited, and conditional AI usage rules per data product
- Mapping data lineage from source systems through transformation layers to AI consumers

## Disclaimer

This project uses fully synthetic data generated for portfolio and demonstration purposes. It does not contain real company data, proprietary architecture, internal system names, operational records, supplier information, or confidential material. Data product structures are inspired by industrial energy-sector patterns but are entirely fictional.

## How to use this

1. Run the app: `streamlit run app.py`
2. Explore the 5 tabs: Catalogue, Readiness Scores, Data Contracts, AI Consumer View, Lineage
3. Select different data products in each tab to see their governance details
4. The Readiness Scores tab shows a weighted 0-100 composite score with dimension-level breakdowns
5. The AI Consumer View tab tells you whether an AI agent can consume each product and under what conditions
