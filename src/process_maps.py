"""Business process flow maps showing where data products and AI models are used."""

from __future__ import annotations


def generate_p2p_process_map(data_products: list = None, ai_models: list = None) -> str:
    """Generate a Procure-to-Pay process map as a Mermaid flowchart."""
    return """graph LR
    subgraph p2p["Procure-to-Pay Process"]
        direction LR
        S1["Need<br/>identification"] --> S2["Requisition"]
        S2 --> S3["Supplier<br/>selection"]
        S3 --> S4["Purchase<br/>order"]
        S4 --> S5["Goods<br/>receipt"]
        S5 --> S6["Invoice<br/>processing"]
        S6 --> S7["Payment"]
        S7 --> S8["Supplier performance<br/>review"]
    end

    subgraph dp["Data Products"]
        DP1["Inventory Availability<br/>Snapshot"]
        DP2["Supplier Performance<br/>Summary"]
        DP3["Contract Spend<br/>History"]
    end

    subgraph ai["AI Models"]
        AI1["Inventory Planning<br/>Assistant"]
        AI2["Supplier Risk<br/>Agent"]
        AI3["Contract Insights<br/>Assistant"]
        AI4["Procurement Anomaly<br/>Detector"]
    end

    DP1 -.->|stock levels| S1
    DP2 -.->|performance scores| S3
    DP3 -.->|contract terms| S4
    DP3 -.->|spend patterns| S6
    DP2 -.->|performance data| S8

    AI1 -.->|reorder recommendations| S1
    AI2 -.->|risk assessment| S3
    AI3 -.->|utilisation insights| S4
    AI4 -.->|anomaly flags| S6
    AI2 -.->|risk monitoring| S8

    style S1 fill:#F1EFE8,stroke:#5F5E5A
    style S2 fill:#F1EFE8,stroke:#5F5E5A
    style S3 fill:#F1EFE8,stroke:#5F5E5A
    style S4 fill:#F1EFE8,stroke:#5F5E5A
    style S5 fill:#F1EFE8,stroke:#5F5E5A
    style S6 fill:#F1EFE8,stroke:#5F5E5A
    style S7 fill:#F1EFE8,stroke:#5F5E5A
    style S8 fill:#F1EFE8,stroke:#5F5E5A
    style DP1 fill:#E1F5EE,stroke:#0F6E56
    style DP2 fill:#E1F5EE,stroke:#0F6E56
    style DP3 fill:#E1F5EE,stroke:#0F6E56
    style AI1 fill:#EEEDFE,stroke:#534AB7
    style AI2 fill:#EEEDFE,stroke:#534AB7
    style AI3 fill:#EEEDFE,stroke:#534AB7
    style AI4 fill:#EEEDFE,stroke:#534AB7"""


def generate_maintenance_process_map(data_products: list = None, ai_models: list = None) -> str:
    """Generate a Maintenance & Reliability process map as a Mermaid flowchart."""
    return """graph LR
    subgraph maint["Maintenance and Reliability Process"]
        direction LR
        M1["Asset<br/>monitoring"] --> M2["Anomaly<br/>detection"]
        M2 --> M3["Work order<br/>creation"]
        M3 --> M4["Planning and<br/>scheduling"]
        M4 --> M5["Execution"]
        M5 --> M6["Completion and<br/>reporting"]
        M6 --> M7["Reliability<br/>analysis"]
    end

    subgraph dp2["Data Products"]
        MW["Maintenance Work Order<br/>History"]
    end

    subgraph ai2["AI Models"]
        MPA["Maintenance Planning<br/>Agent"]
    end

    MW -.->|failure history| M2
    MW -.->|work order data| M4
    MW -.->|completion records| M7

    MPA -.->|predictive indicators| M1
    MPA -.->|backlog prioritisation| M4
    MPA -.->|pattern analysis| M7

    style M1 fill:#F1EFE8,stroke:#5F5E5A
    style M2 fill:#F1EFE8,stroke:#5F5E5A
    style M3 fill:#F1EFE8,stroke:#5F5E5A
    style M4 fill:#F1EFE8,stroke:#5F5E5A
    style M5 fill:#F1EFE8,stroke:#5F5E5A
    style M6 fill:#F1EFE8,stroke:#5F5E5A
    style M7 fill:#F1EFE8,stroke:#5F5E5A
    style MW fill:#E1F5EE,stroke:#0F6E56
    style MPA fill:#EEEDFE,stroke:#534AB7"""


def get_process_list() -> list[dict]:
    """Return metadata for available process maps."""
    return [
        {
            "id": "p2p",
            "name": "Procure-to-Pay",
            "steps": 8,
            "data_products_involved": 3,
            "ai_models_involved": 4,
            "description": "End-to-end purchasing process from need identification to supplier review.",
        },
        {
            "id": "maintenance",
            "name": "Maintenance & Reliability",
            "steps": 7,
            "data_products_involved": 1,
            "ai_models_involved": 1,
            "description": "Asset maintenance lifecycle from monitoring to reliability analysis.",
        },
    ]


__all__ = [
    "generate_p2p_process_map",
    "generate_maintenance_process_map",
    "get_process_list",
]
