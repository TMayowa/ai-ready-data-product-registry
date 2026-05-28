"""AI model architecture diagrams.

Returns Mermaid flowchart diagrams showing the internal architecture
of each registered AI model.
"""

from __future__ import annotations

from src.models import AIModel

_DIAGRAMS: dict[str, str] = {

"supplier-risk-agent": """graph TD
    subgraph input_layer["Input sources"]
        D1["Supplier Performance Summary"]
        D2["Contract Spend History"]
        D3["External risk signals"]
    end
    subgraph agent_orchestration["LangGraph orchestration"]
        direction TB
        ROUTER["Router<br/>classifies signal type"]
        DISCARD["Discard - logged"]
        subgraph scanning["Signal scanning"]
            SCAN["Scanner agent<br/>Claude 3.5 Haiku<br/>High volume, low cost"]
        end
        subgraph analysis["Risk analysis"]
            SYNTH["Synthesis agent<br/>Claude 3.5 Sonnet<br/>Deep reasoning"]
        end
        subgraph controls["Governance controls"]
            CONF["Confidence check"]
            TRACE["Source traceability"]
            ESC["Escalation rules"]
        end
    end
    subgraph output_layer["Outputs"]
        REC["Risk assessment and recommendations"]
        DASH["Dashboard alert"]
        HUM["Human review queue"]
    end
    D1 --> ROUTER
    D2 --> ROUTER
    D3 --> ROUTER
    ROUTER --> SCAN
    SCAN -->|risk signal| SYNTH
    SCAN -->|no risk| DISCARD
    SYNTH --> CONF
    CONF -->|high confidence| TRACE
    CONF -->|low confidence| ESC
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
        D1["Contract Spend History"]
        Q["User query"]
    end
    subgraph processing["Processing pipeline"]
        direction TB
        CTX["Context assembly<br/>retrieve relevant contracts,<br/>spend records, terms"]
        LLM["Claude 3.5 Haiku<br/>analyse, summarise,<br/>surface insights"]
        VAL["Output validation<br/>check for hallucination,<br/>verify against source"]
        REJ["Rejected - flagged for review"]
    end
    subgraph output["Output"]
        INS["Contract insight report"]
        SRC["Source references"]
    end
    D1 --> CTX
    Q --> CTX
    CTX --> LLM
    LLM --> VAL
    VAL -->|validated| INS
    VAL -->|sources attached| SRC
    VAL -->|validation failed| REJ
    style input fill:#E6F1FB,stroke:#185FA5
    style processing fill:#EEEDFE,stroke:#534AB7
    style output fill:#E1F5EE,stroke:#0F6E56""",

"logistics-disruption-agent": """graph TD
    subgraph input["Input sources"]
        D1["Logistics Delay Events"]
        D2["Inventory Availability Snapshot"]
        W["Weather API - Met.no"]
        V["Vessel AIS tracking"]
    end
    subgraph agent["LangGraph orchestration"]
        direction TB
        MON["Monitor agent<br/>Claude 3.5 Haiku<br/>event classification"]
        PRED["Prediction agent<br/>Claude 3.5 Sonnet<br/>disruption probability"]
        CONT["Contingency agent<br/>Claude 3.5 Sonnet<br/>alternative routing"]
        subgraph safety["Safety gate"]
            CHECK["Safety-critical check"]
        end
    end
    subgraph output["Outputs"]
        ALERT["Disruption alert"]
        PLAN["Contingency plan"]
        ESC["Safety escalation - human required"]
    end
    D1 --> MON
    W --> MON
    V --> MON
    MON -->|disruption likely| PRED
    PRED --> CONT
    D2 --> CONT
    CONT --> CHECK
    CHECK -->|standard| ALERT
    CHECK -->|standard| PLAN
    CHECK -->|safety critical| ESC
    style input fill:#E6F1FB,stroke:#185FA5
    style agent fill:#FAFAFA,stroke:#5F5E5A
    style safety fill:#FAECE7,stroke:#993C1D
    style output fill:#E1F5EE,stroke:#0F6E56""",

"inventory-planning-assistant": """graph TD
    subgraph input["Input"]
        D1["Inventory Availability Snapshot"]
    end
    subgraph feature_eng["Feature engineering"]
        F1["Consumption history<br/>rolling averages"]
        F2["Seasonal patterns<br/>monthly, quarterly"]
        F3["Lead time features<br/>supplier delivery"]
        F4["Criticality weighting<br/>spare part class"]
    end
    subgraph model["Model"]
        XGB["XGBoost<br/>demand forecast"]
        RULES["Business rules<br/>safety stock, reorder constraints"]
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
        D1["Maintenance Work Order History"]
        IOT["IoT sensor readings<br/>vibration, temperature, pressure"]
        INSP["Inspection records"]
    end
    subgraph feature["Feature extraction"]
        TS["Time-series features<br/>sensor trends, rolling stats"]
        WO["Work order features<br/>failure codes, intervals, costs"]
        EQ["Equipment profile<br/>age, class, criticality"]
    end
    subgraph ensemble["Ensemble model"]
        LSTM["LSTM<br/>temporal patterns in sensor data"]
        RF["Random Forest<br/>failure probability from work order history"]
        COMB["Ensemble combiner<br/>weighted average"]
    end
    subgraph safety_gate["Safety gate - ALL outputs reviewed"]
        REV["Mandatory human review<br/>for safety-critical equipment"]
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
        D1["Supplier Performance Summary"]
        D2["Contract Spend History"]
    end
    subgraph preprocessing["Preprocessing"]
        JOIN["Join supplier and spend records"]
        FEAT["Feature extraction<br/>spend deviation, frequency,<br/>vendor patterns, timing"]
    end
    subgraph model["Detection model"]
        ISO["Isolation Forest<br/>unsupervised anomaly scoring"]
        FILT["Rule-based filters<br/>duplicate POs, round-number invoices"]
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
