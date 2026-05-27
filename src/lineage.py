"""Mermaid lineage diagram generator.

Produces a color-coded Mermaid flowchart from a DataProduct's lineage nodes.
"""

from __future__ import annotations

import re

from src.models import DataProduct

# Layer → Mermaid style map
LAYER_STYLES: dict[str, str] = {
    "source":   "fill:#E6F1FB,stroke:#185FA5",
    "raw":      "fill:#F1EFE8,stroke:#5F5E5A",
    "cleaned":  "fill:#FAEEDA,stroke:#854F0B",
    "product":  "fill:#E1F5EE,stroke:#0F6E56,stroke-width:2px",
    "consumer": "fill:#EEEDFE,stroke:#534AB7",
}


def _sanitise_id(name: str, index: int) -> str:
    """Create a safe Mermaid node ID by replacing non-alphanumeric chars."""
    clean = re.sub(r"[^a-zA-Z0-9]", "_", name)
    return f"{clean}_{index}"


def generate_mermaid(product: DataProduct) -> str:
    """Generate a Mermaid flowchart (top-down) showing the data lineage.

    Rules:
    - Use 'graph TD' (top-down)
    - Each LineageNode becomes a node, ID derived from system_name (sanitised)
    - Nodes are connected in order (lineage[0] --> lineage[1] --> ...)
    - Style nodes by layer
    - If there are multiple consumers, they branch from the product node
    """
    lines: list[str] = ["graph TD"]
    node_ids: list[str] = []

    # Build nodes and connections
    for i, node in enumerate(product.lineage):
        nid = _sanitise_id(node.system_name, i)
        node_ids.append(nid)
        label = f'{node.system_name}<br/><small>{node.layer}</small>'
        lines.append(f'    {nid}["{label}"]')

    # Build edges
    # Non-consumer nodes connect linearly
    # Consumer nodes all branch from the last non-consumer node
    non_consumer_indices = [
        i for i, n in enumerate(product.lineage) if n.layer != "consumer"
    ]
    consumer_indices = [
        i for i, n in enumerate(product.lineage) if n.layer == "consumer"
    ]

    # Linear chain for non-consumer nodes
    for j in range(len(non_consumer_indices) - 1):
        src_idx = non_consumer_indices[j]
        dst_idx = non_consumer_indices[j + 1]
        lines.append(f"    {node_ids[src_idx]} --> {node_ids[dst_idx]}")

    # Branch consumers from the last non-consumer node
    if consumer_indices:
        branch_parent = node_ids[non_consumer_indices[-1]]
        for ci in consumer_indices:
            lines.append(f"    {branch_parent} --> {node_ids[ci]}")

    # Style nodes
    for i, node in enumerate(product.lineage):
        style = LAYER_STYLES.get(node.layer, "fill:#FFFFFF,stroke:#000000")
        lines.append(f"    style {node_ids[i]} {style}")

    return "\n".join(lines)


__all__ = ["generate_mermaid"]
