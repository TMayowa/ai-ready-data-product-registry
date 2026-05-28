"""AI model architecture diagrams.

Returns Mermaid flowchart diagrams showing the internal architecture
of each registered AI model.
"""

from __future__ import annotations

from src.models import AIModel

_DIAGRAMS: dict[str, str] = {

"supplier-risk-agent": """graph TD
    D1[Supplier Performance Summary] --> ROUTER
    D2[Contract Spend History] --> ROUTER
    D3[External risk signals] --> ROUTER
    ROUTER[Router] --> SCAN
    SCAN[Scanner - Claude 3.5 Haiku] -->|risk signal| SYNTH
    SCAN -->|no risk| DISC[Discard]
    SYNTH[Synthesiser - Claude 3.5 Sonnet] --> CONF[Confidence check]
    CONF -->|high confidence| TRACE[Source traceability]
    CONF -->|low confidence| ESC[Escalation rules]
    TRACE --> REC[Risk assessment]
    TRACE --> DASH[Dashboard alert]
    ESC --> HUM[Human review queue]
    style D1 fill:#E6F1FB,stroke:#185FA5
    style D2 fill:#E6F1FB,stroke:#185FA5
    style D3 fill:#E6F1FB,stroke:#185FA5
    style SCAN fill:#F1EFE8,stroke:#5F5E5A
    style SYNTH fill:#EEEDFE,stroke:#534AB7
    style CONF fill:#FAEEDA,stroke:#854F0B
    style TRACE fill:#FAEEDA,stroke:#854F0B
    style ESC fill:#FAEEDA,stroke:#854F0B
    style REC fill:#E1F5EE,stroke:#0F6E56
    style DASH fill:#E1F5EE,stroke:#0F6E56
    style HUM fill:#FAECE7,stroke:#993C1D""",

"contract-insights-assistant": """graph TD
    D1[Contract Spend History] --> CTX
    Q[User query] --> CTX
    CTX[Context assembly] --> LLM
    LLM[Claude 3.5 Haiku] --> VAL
    VAL[Output validation] -->|validated| INS[Contract insight report]
    VAL -->|sources attached| SRC[Source references]
    VAL -->|failed| REJ[Rejected - flagged for review]
    style D1 fill:#E6F1FB,stroke:#185FA5
    style Q fill:#E6F1FB,stroke:#185FA5
    style CTX fill:#EEEDFE,stroke:#534AB7
    style LLM fill:#EEEDFE,stroke:#534AB7
    style VAL fill:#EEEDFE,stroke:#534AB7
    style INS fill:#E1F5EE,stroke:#0F6E56
    style SRC fill:#E1F5EE,stroke:#0F6E56
    style REJ fill:#FAECE7,stroke:#993C1D""",

"logistics-disruption-agent": """graph TD
    D1[Logistics Delay Events] --> MON
    D2[Inventory Availability Snapshot] --> CONT
    W[Weather API] --> MON
    V[Vessel AIS] --> MON
    MON[Monitor - Claude 3.5 Haiku] -->|disruption likely| PRED
    PRED[Prediction - Claude 3.5 Sonnet] --> CONT
    CONT[Contingency - Claude 3.5 Sonnet] --> CHECK
    CHECK[Safety-critical check] -->|standard| ALERT[Disruption alert]
    CHECK -->|standard| PLAN[Contingency plan]
    CHECK -->|safety critical| ESC[Safety escalation]
    style D1 fill:#E6F1FB,stroke:#185FA5
    style D2 fill:#E6F1FB,stroke:#185FA5
    style W fill:#E6F1FB,stroke:#185FA5
    style V fill:#E6F1FB,stroke:#185FA5
    style MON fill:#F1EFE8,stroke:#5F5E5A
    style PRED fill:#EEEDFE,stroke:#534AB7
    style CONT fill:#EEEDFE,stroke:#534AB7
    style CHECK fill:#FAECE7,stroke:#993C1D
    style ALERT fill:#E1F5EE,stroke:#0F6E56
    style PLAN fill:#E1F5EE,stroke:#0F6E56
    style ESC fill:#FAECE7,stroke:#993C1D""",

"inventory-planning-assistant": """graph TD
    D1[Inventory Availability Snapshot] --> F1
    D1 --> F2
    D1 --> F3
    D1 --> F4
    F1[Consumption history] --> XGB
    F2[Seasonal patterns] --> XGB
    F3[Lead time features] --> XGB
    F4[Criticality weighting] --> XGB
    XGB[XGBoost demand forecast] --> RULES
    RULES[Business rules] --> FORE[Demand forecast]
    RULES --> REC[Reorder recommendations]
    RULES --> ALERT[Low stock alerts]
    style D1 fill:#E6F1FB,stroke:#185FA5
    style F1 fill:#F1EFE8,stroke:#5F5E5A
    style F2 fill:#F1EFE8,stroke:#5F5E5A
    style F3 fill:#F1EFE8,stroke:#5F5E5A
    style F4 fill:#F1EFE8,stroke:#5F5E5A
    style XGB fill:#EEEDFE,stroke:#534AB7
    style RULES fill:#EEEDFE,stroke:#534AB7
    style FORE fill:#E1F5EE,stroke:#0F6E56
    style REC fill:#E1F5EE,stroke:#0F6E56
    style ALERT fill:#E1F5EE,stroke:#0F6E56""",

"maintenance-planning-agent": """graph TD
    D1[Maintenance Work Order History] --> WO
    IOT[IoT sensor readings] --> TS
    INSP[Inspection records] --> EQ
    TS[Time-series features] --> LSTM
    WO[Work order features] --> RF
    EQ[Equipment profile] --> RF
    LSTM[LSTM temporal model] --> COMB
    RF[Random Forest] --> COMB
    COMB[Ensemble combiner] --> REV
    REV[Mandatory human review] --> PRED[Failure prediction]
    REV --> PRIO[Backlog prioritisation]
    REV --> FLAG[Regulatory flag]
    style D1 fill:#E6F1FB,stroke:#185FA5
    style IOT fill:#E6F1FB,stroke:#185FA5
    style INSP fill:#E6F1FB,stroke:#185FA5
    style TS fill:#F1EFE8,stroke:#5F5E5A
    style WO fill:#F1EFE8,stroke:#5F5E5A
    style EQ fill:#F1EFE8,stroke:#5F5E5A
    style LSTM fill:#EEEDFE,stroke:#534AB7
    style RF fill:#EEEDFE,stroke:#534AB7
    style COMB fill:#EEEDFE,stroke:#534AB7
    style REV fill:#FAECE7,stroke:#993C1D,stroke-width:2px
    style PRED fill:#E1F5EE,stroke:#0F6E56
    style PRIO fill:#E1F5EE,stroke:#0F6E56
    style FLAG fill:#E1F5EE,stroke:#0F6E56""",

"procurement-anomaly-detector": """graph TD
    D1[Supplier Performance Summary] --> JOIN
    D2[Contract Spend History] --> JOIN
    JOIN[Join supplier and spend records] --> FEAT
    FEAT[Feature extraction] --> ISO
    FEAT --> FILT
    ISO[Isolation Forest] --> SCORE[Anomaly score]
    FILT[Rule-based filters] --> FLAG[Flagged transactions]
    SCORE --> RPT[Investigation report]
    FLAG --> RPT
    style D1 fill:#E6F1FB,stroke:#185FA5
    style D2 fill:#E6F1FB,stroke:#185FA5
    style JOIN fill:#F1EFE8,stroke:#5F5E5A
    style FEAT fill:#F1EFE8,stroke:#5F5E5A
    style ISO fill:#EEEDFE,stroke:#534AB7
    style FILT fill:#EEEDFE,stroke:#534AB7
    style RPT fill:#E1F5EE,stroke:#0F6E56""",
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
