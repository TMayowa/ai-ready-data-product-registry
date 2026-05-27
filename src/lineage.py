"""Mermaid lineage diagram generator.

Produces a color-coded Mermaid flowchart from a DataProduct's lineage nodes.
Uses simple letter-based node IDs (A, B, C...) for Mermaid compatibility.
"""

from __future__ import annotations

from src.models import DataProduct

# Layer → Mermaid fill/stroke style
LAYER_STYLES: dict[str, str] = {
    "source":   "fill:#E6F1FB,stroke:#185FA5,color:#042C53",
    "raw":      "fill:#F1EFE8,stroke:#5F5E5A,color:#2C2C2A",
    "cleaned":  "fill:#FAEEDA,stroke:#854F0B,color:#412402",
    "product":  "fill:#E1F5EE,stroke:#0F6E56,stroke-width:3px,color:#04342C",
    "consumer": "fill:#EEEDFE,stroke:#534AB7,color:#26215C",
}

_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def generate_mermaid(product: DataProduct) -> str:
    """Generate a Mermaid graph TD flowchart showing data lineage.

    Uses simple letter node IDs (A, B, C...) to avoid Mermaid parsing issues.
    Consumer nodes branch from the last non-consumer node.
    """
    lines: list[str] = ["graph TD"]
    node_ids: list[str] = []

    # Declare nodes with letter IDs
    for i, node in enumerate(product.lineage):
        nid = _LETTERS[i] if i < len(_LETTERS) else f"N{i}"
        node_ids.append(nid)
        label = f"{node.system_name}<br/><small>{node.layer}</small>"
        lines.append(f'    {nid}["{label}"]')

    # Build edges
    non_consumer = [i for i, n in enumerate(product.lineage) if n.layer != "consumer"]
    consumers = [i for i, n in enumerate(product.lineage) if n.layer == "consumer"]

    for j in range(len(non_consumer) - 1):
        lines.append(f"    {node_ids[non_consumer[j]]} --> {node_ids[non_consumer[j + 1]]}")

    if consumers and non_consumer:
        parent = node_ids[non_consumer[-1]]
        for ci in consumers:
            lines.append(f"    {parent} --> {node_ids[ci]}")

    # Apply layer styles
    for i, node in enumerate(product.lineage):
        style = LAYER_STYLES.get(node.layer, "fill:#FFFFFF,stroke:#000000")
        lines.append(f"    style {node_ids[i]} {style}")

    return "\n".join(lines)


__all__ = ["generate_mermaid", "LAYER_STYLES"]
