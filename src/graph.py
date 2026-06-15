# ./src/graph.py

"""`LangGraph` state graph builder for the application processing pipeline.

This module defines and compiles the StateGraph that connects the
preprocessing, classification, and routing nodes into a complete
application processing pipeline.

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
from src.nodes.preprocess import preprocess_node
from src.nodes.classify import classify_node
from src.nodes.route import (
    router_node, shortlist_node, reject_node, escalate_node
)


def build_graph() -> CompiledStateGraph:
    """Builds and compiles the application processing `StateGraph`.

    Registers all pipeline nodes, sets the entry point to
    `"preprocess"`, connects preprocessing and classification with
    a direct edge, routes from classification to one of three terminal
    nodes via `router_node`, and connects all terminal nodes to `END`.

    Returns:
        A compiled `LangGraph` application ready to invoke.

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
    graph = StateGraph(ApplicationState)
    graph.add_node("preprocess", preprocess_node)
    graph.add_node("classify", classify_node)
    graph.add_node("shortlist", shortlist_node)
    graph.add_node("reject", reject_node)
    graph.add_node("escalate", escalate_node)
    graph.set_entry_point("preprocess")
    graph.add_edge("preprocess", "classify")
    graph.add_conditional_edges(
        "classify",
        router_node,
        {
            "shortlist": "shortlist",
            "reject": "reject",
            "escalate": "escalate",
        }
    )
    graph.add_edge("shortlist", END)
    graph.add_edge("reject", END)
    graph.add_edge("escalate", END)
    return graph.compile()
