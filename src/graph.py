# ./src/graph.py

"""`LangGraph` state graph builder for the application processing pipeline.

This module defines and compiles the `StateGraph` that connects the
preprocessing, classification, and routing nodes into a complete
application processing pipeline using a `TriageNodes` instance for
dependency injection.

Example:
    Building and invoking the graph:
    ```
    from src.graph import build_graph

    app = build_graph()
    result = app.invoke({
        "raw_input": {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "position": "Engineer",
            "experience_years": 5,
            "skills": ["Python", "SQL"],
            "cover_letter": "I am excited to apply.",
        },
        "cleaned": {},
        "classification": None,
        "decision": "",
    })
    print(result["decision"])  # "shortlist"
    ```
"""

from langgraph.graph import StateGraph, END
from langgraph.graph.state import CompiledStateGraph
from src.types.state import ApplicationState
from src.nodes import TriageNodes
from src.llm import GroqClient
from src.logger import AppLogger


def build_graph() -> CompiledStateGraph:
    """Builds and compiles the application processing StateGraph.

    Instantiates `TriageNodes` with a shared GroqClient and `AppLogger`,
    registers all pipeline nodes, sets the entry point to
    `"preprocess"`, connects preprocessing and classification with
    a direct edge, routes from classification to one of three terminal
    nodes via nodes.router, and connects all terminal nodes to END.

    Returns:
        A compiled LangGraph application ready to invoke.

    Example:
    ```
    app = build_graph()
    result = app.invoke({
        "raw_input": {"name": "Jane Doe", ...},
        "cleaned": {},
        "classification": None,
        "decision": "",
    })
    print(result["decision"])  # "shortlist" | "reject" | "escalate"
    ```
    """
    nodes = _create_nodes()
    graph = StateGraph(ApplicationState)
    _build_edges(graph, nodes)
    return graph.compile()


def _create_nodes() -> TriageNodes:
    """Instantiates `TriageNodes` with a shared `GroqClient` and `AppLogger`.

    Returns:
        A `TriageNodes` instance ready to be registered in the graph.

    Example:
    ```
    nodes = _create_nodes()
    graph.add_node("preprocess", nodes.preprocess)
    """
    return TriageNodes(
        llm=GroqClient(),
        logger=AppLogger("triage")
    )


def _build_edges(graph: StateGraph, nodes: TriageNodes) -> None:
    """Registers all nodes and edges on the graph.

    Sets up the node list, entry point, direct edges, conditional
    routing, and terminal edges in a single call.

    Args:
        graph: The StateGraph instance to configure.
        nodes: The TriageNodes instance providing node methods.

    Example:
    ```
    graph = StateGraph(ApplicationState)
    _build_edges(graph, nodes)
    ```
    """
    _set_nodes(graph, nodes)
    graph.set_entry_point("preprocess")
    graph.add_edge("preprocess", "classify")
    graph.add_conditional_edges(
        "classify",
        nodes.router,
        {
            "shortlist": "shortlist",
            "reject": "reject",
            "escalate": "escalate",
        }
    )
    _set_end_edges(graph)


def _set_nodes(graph: StateGraph, nodes: TriageNodes) -> None:
    """Registers all `TriageNodes` methods as named nodes on the graph.

    Uses each method's `__name__` as the node name, so the registered
    names match the method names: `"preprocess"`, `"classify"`,
    `"shortlist"`, `"reject"`, and `"escalate"`.

    Args:
        graph: The `StateGraph` instance to register nodes on.
        nodes: The `TriageNodes` instance providing node methods.

    Example:
    ```
    _set_nodes(graph, nodes)
    # equivalent to:
    # graph.add_node("preprocess", nodes.preprocess)
    # graph.add_node("classify", nodes.classify)
    # ...
    ```
    """
    for fn in [
        nodes.preprocess,
        nodes.classify,
        nodes.shortlist,
        nodes.reject,
        nodes.escalate,
    ]:
        graph.add_node(fn.__name__, fn)


def _set_end_edges(graph: StateGraph) -> None:
    """Connects all terminal nodes to END.

    Args:
        graph: The `StateGraph` instance to add terminal edges to.

    Example:
    ```
    _set_end_edges(graph)
    # equivalent to:
    # graph.add_edge("shortlist", END)
    # graph.add_edge("reject", END)
    # graph.add_edge("escalate", END)
    ```
    """
    for name in ["shortlist", "reject", "escalate"]:
        graph.add_edge(name, END)
