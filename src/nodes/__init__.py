# ./src/nodes/__init__.py

"""Public API for the nodes package.

This module re-exports `TriageNodes` as the sole intended entry point
for accessing pipeline node methods.

Example:
    Importing from the package directly:
    ```
    from src.nodes import TriageNodes
    from src.llm import GroqClient
    from src.logger import AppLogger

    nodes = TriageNodes(llm=GroqClient(), logger=AppLogger("triage"))
    graph.add_node("preprocess", nodes.preprocess)
    graph.add_node("classify", nodes.classify)
    ```
"""

from src.nodes.triage_nodes import TriageNodes

__all__ = [
    "TriageNodes",
]
