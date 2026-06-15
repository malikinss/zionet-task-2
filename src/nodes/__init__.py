# ./src/nodes/__init__.py

"""Public API for the nodes package.

This module re-exports the node functions intended for use by the
graph builder, providing a single stable import point for all
pipeline nodes.

Example:
    Importing from the package directly:
    ```
        from src.nodes import classify_node, preprocess_node, escalate_node

        graph.add_node("preprocess", preprocess_node)
        graph.add_node("classify", classify_node)
        graph.add_node("escalate", escalate_node)
    ```
"""

from src.nodes.classify import classify_node
from src.nodes.preprocess import preprocess_node
from src.nodes.route import escalate_node

__all__ = [
    "classify_node", "preprocess_node", "escalate_node"
]
