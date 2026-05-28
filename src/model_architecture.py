"""AI model architecture diagrams.

Returns Mermaid flowchart diagrams showing the internal architecture
of each registered AI model.
"""

from __future__ import annotations

from src.models import AIModel

_DIAGRAMS: dict[str, str] = {

"supplier-risk-agent": """graph TD
    subgraph input_layer["Input sources"]
        D1["Supplier Performance Summary<br/><small>data product</small>"]
        D2["Contract Spend History<br/><small>data product</small>"]
        D3["External risk signals<br/><small>news, geopolitical</small>"]
    end
    subgraph agent_orchestration["LangGraph orchestration"]
        direction TB
        ROUTER["Router<br/><small>classifies incoming signal type</small>"]
        subgraph scanning["Signal scanning"]
            SCAN["Scanner agent<br/><small>Claude 3.5 Haiku</small><br/><small>High volume, low cost</small>"]
        end
        subgraph analysis["Risk analysis"]
            SYNTH["Synthesis agent<br/><small>Claude 3.5 Sonnet</small><br/><small>Deep reasoning</small>"]
        end
        subgraph controls["Governance controls"]
            CONF["Confidence check"]
            TRACE["Source traceability"]
            ESC["Escalation rules"]
        end
    end
    subgraph output_layer["Outputs"]
        REC["Risk assessment + recommendations"]
        DASH["Dashboard alert"]
        HUM["Human review queue"]
    end
    D1 --> ROUTER
    D2 --> ROUTER
    D3 --> ROUTER
    ROUTER --> SCAN
    SCAN -->|"risk signal detected"| SYNTH
    SCAN -->|"no risk"| DISCARD["Discard<br/><small>logged</small>"]
    SYNTH --> CONF
    CONF -->|"confidence >= 80%"| TRACE
    CONF -->|"confidence < 80%"| ESC
    TRACE --> REC
    TRACE --> DASH
    ESC --> HUM
    style input_layer fill:#E6F1FB,stroke:#185FA5
    style agent_orchestration fill:#FAFAFA,stroke:#5F5E5A
    style scanning fill:#F1EFE8,stroke:#5F5E5A
    style analysis fill:#EEEDFE,stroke:#534AB7
    style controls fill:#FAEEDA,stroke:#854F0B
    style output_layer fill:#E1F5EE,stroke:#0F6E56""",

"contract-insights-assistant": """graph TD
    subgraph input["Input"]
        D1["Contract Spend History<br/><small>data product</small>"]
        Q["User query<br/><small>natural language</small>"]
    end
    subgraph processing["Processing pipeline"]
        direction TB
        CTX["Context assembly<br/><small>retrieve relevant contracts,<br/>spend records, terms</small>"]
        LLM["Claude 3.5 Haiku<br/><small>analyse, summarise,<br/>surface insights</small>"]
        VAL["Output validation<br/><small>check for hallucination,<br/>verify against source</small>"]
    end
    subgraph output["Output"]
        INS["Contract insight report"]
        SRC["Source references"]
    end
    D1 --> CTX
    Q --> CTX
    CTX --> LLM
    LLM --> VAL
    VAL -->|"validated"| INS
    VAL -->|"sources attached"| SRC
    VAL -->|"validation failed"| REJ["Rejected<br/><small>flagged for review</small>"]
    style input fill:#E6F1FB,stroke:#185FA5
    style processing fill:#EEEDFE,stroke:#534AB7
    style output fill:#E1F5EE,stroke:#0F6E56""",

"logistics-disruption-agent": """graph TD
    subgraph input["Input sources"]
        D1["Logistics Delay Events<br/><small>data product</small>"]
        D2["Inventory Availability Snapshot<br/><small>data product</small>"]
        W["Weather API<br/><small>Met.no</small>"]
        V["Vessel AIS<br/><small>tracking</small>"]
    end
    subgraph agent["LangGraph orchestration"]
        direction TB
        MON["Monitor agent<br/><small>Claude 3.5 Haiku</small><br/><small>event classification</small>"]
        PRED["Prediction agent<br/><small>Claude 3.5 Sonnet</small><br/><small>disruption probability,<br/>delay estimation</small>"]
        CONT["Contingency agent<br/><small>Claude 3.5 Sonnet</small><br/><small>alternative routing,<br/>resource reallocation</small>"]
        subgraph safety["Safety gate"]
            CHECK["Safety-critical check"]
        end
    end
    subgraph output["Outputs"]
        ALERT["Disruption alert"]
        PLAN["Contingency plan"]
        ESC["Safety escalation<br/><small>human required</small>"]
    end
    D1 --> MON
    W --> MON
    V --> MON
    MON -->|"disruption likely"| PRED
    PRED --> CONT
    D2 --> CONT
    CONT --> CHECK
    CHECK -->|"not safety-critical"| ALERT
    CHECK -->|"not safety-critical"| PLAN
    CHECK -->|"safety-critical"| ESC
    style input fill:#E6F1FB,stroke:#185FA5
    style agent fill:#FAFAFA,stroke:#5F5E5A
    style safety fill:#FAECE7,stroke:#993C1D
    style output fill:#E1F5EE,stroke:#0F6E56""",

"inventory-planning-assistant": """graph TD
    subgraph input["Input"]
        D1["Inventory Availability Snapshot<br/><small>data product</small>"]
    end
    subgraph feature_eng["Feature engineering"]
        F1["Consumption history<br/><small>rolling averages</small>"]
        F2["Seasonal patterns<br/><small>monthly, quarterly</small>"]
        F3["Lead time features<br/><small>supplier delivery</small>"]
        F4["Criticality weighting<br/><small>spare part class</small>"]
    end
    subgraph model["Model"]
        XGB["XGBoost<br/><small>demand forecast</small>"]
        RULES["Business rules<br/><small>safety stock floors,<br/>reorder constraints</small>"]
    end
    subgraph output["Output"]
        FORE["Demand forecast"]
        REC["Reorder recommendations"]
        ALERT["Low stock alerts"]
    end
    D1 --> F1
    D1 --> F2
    D1 --> F3
    D1 --> F4
    F1 --> XGB
    F2 --> XGB
    F3 --> XGB
    F4 --> XGB
    XGB --> RULES
    RULES --> FORE
    RULES --> REC
    RULES --> ALERT
    style input fill:#E6F1FB,stroke:#185FA5
    style feature_eng fill:#F1EFE8,stroke:#5F5E5A
    style model fill:#EEEDFE,stroke:#534AB7
    style output fill:#E1F5EE,stroke:#0F6E56""",

"maintenance-planning-agent": """graph TD
    subgraph input["Input sources"]
        D1["Maintenance Work Order History<br/><small>data product</small>"]
        IOT["IoT sensor readings<br/><small>vibration, temperature, pressure</small>"]
        INSP["Inspection records"]
    end
    subgraph feature["Feature extraction"]
        TS["Time-series features<br/><small>sensor trends, rolling stats</small>"]
        WO["Work order features<br/><small>failure codes, intervals, costs</small>"]
        EQ["Equipment profile<br/><small>age, class, criticality</small>"]
    end
    subgraph ensemble["Ensemble model"]
        LSTM["LSTM<br/><small>temporal patterns in sensor data</small>"]
        RF["Random Forest<br/><small>failure probability from work order history</small>"]
        COMB["Ensemble combiner<br/><small>weighted average</small>"]
    end
    subgraph safety_gate["Safety gate — ALL outputs reviewed"]
        REV["Mandatory human review<br/><small>for safety-critical equipment</small>"]
    end
    subgraph output["Output"]
        PRED["Failure prediction"]
        PRIO["Backlog prioritisation"]
        FLAG["Regulatory maintenance flag"]
    end
    D1 --> WO
    IOT --> TS
    INSP --> EQ
    TS --> LSTM
    WO --> RF
    EQ --> RF
    LSTM --> COMB
    RF --> COMB
    COMB --> REV
    REV --> PRED
    REV --> PRIO
    REV --> FLAG
    style input fill:#E6F1FB,stroke:#185FA5
    style feature fill:#F1EFE8,stroke:#5F5E5A
    style ensemble fill:#EEEDFE,stroke:#534AB7
    style safety_gate fill:#FAECE7,stroke:#993C1D,stroke-width:2px
    style output fill:#E1F5EE,stroke:#0F6E56""",

"procurement-anomaly-detector": """graph TD
    subgraph input["Input"]
        D1["Supplier Performance Summary<br/><small>data product</small>"]
        D2["Contract Spend History<br/><small>data product</small>"]
    end
    subgraph preprocessing["Preprocessing"]
        JOIN["Join supplier + spend records"]
        FEAT["Feature extraction<br/><small>spend deviation, frequency,<br/>vendor patterns, timing</small>"]
    end
    subgraph model["Detection model"]
        ISO["Isolation Forest<br/><small>unsupervised anomaly scoring</small>"]
        FILT["Rule-based filters<br/><small>duplicate POs, round-number invoices,<br/>split orders</small>"]
    end
    subgraph output["Output"]
        SCORE["Anomaly score"]
        FLAG["Flagged transactions"]
        RPT["Investigation report"]
    end
    D1 --> JOIN
    D2 --> JOIN
    JOIN --> FEAT
    FEAT --> ISO
    FEAT --> FILT
    ISO --> SCORE
    FILT --> FLAG
    SCORE --> RPT
    FLAG --> RPT
    style input fill:#E6F1FB,stroke:#185FA5
    style preprocessing fill:#F1EFE8,stroke:#5F5E5A
    style model fill:#EEEDFE,stroke:#534AB7
    style output fill:#E1F5EE,stroke:#0F6E56""",
}


def generate_model_architecture(model: AIModel) -> str | None:
    """Return a Mermaid diagram for the given AI model, or None if not available."""
    return _DIAGRAMS.get(model.id)


def architecture_caption(model: AIModel) -> str:
    """Return an auto-generated summary caption for the architecture."""
    n_inputs = len(model.input_data_products)
    if model.model_type == "Agent":
        # Count sub-models based on framework hint
        n_submodels = 3 if model.id == "logistics-disruption-agent" else 2
        return (
            f"Multi-model agent using {model.framework or 'LangGraph'} orchestration "
            f"with {n_submodels} sub-models. Input from {n_inputs} data product(s)."
        )
    elif model.model_type == "NLP model":
        return (
            f"Single-model pipeline using {model.base_model or 'LLM'}. "
            f"Input from {n_inputs} data product(s)."
        )
    else:
        return (
            f"Non-generative model using {model.base_model or 'traditional ML'}. "
            f"Input from {n_inputs} data product(s). No LLM token consumption."
        )


__all__ = ["generate_model_architecture", "architecture_caption"]
