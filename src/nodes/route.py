# ./src/nodes/route.py

"""Routing nodes for the application processing pipeline.

This module provides the router node that reads the classification
category and returns it as a routing key, along with the three
terminal nodes that handle shortlisting, rejection, and escalation.

Example:
    Using the nodes in a graph:
    ```
    from src.nodes.route import (
        router_node, shortlist_node, reject_node, escalate_node
    )

    route = router_node(state)   # "shortlist" | "reject" | "escalate"
    ```
"""

from src.types.state import ApplicationState
from src.types.classification import ApplicationClassification
from src.logger import AppLogger

log = AppLogger("route")
"""Module-level logger shared across all routing nodes."""


def _get_classification(state: ApplicationState) -> ApplicationClassification:
    """Retrieves the classification from state, raising if absent.

    Args:
        state: The current application state.

    Returns:
        The ApplicationClassification stored in state.

    Raises:
        ValueError: If `state["classification"]` is None.

    Example:
    ```
    c = _get_classification(state)
    print(c.category)  # "shortlist"
    ```
    """
    c = state["classification"]
    if c is None:
        raise ValueError("Classification is missing from state")
    return c


def router_node(state: ApplicationState) -> str:
    """Reads the classification category and returns it as a routing key.

    Args:
        state: The current application state with a populated
            `classification` field.

    Returns:
        The category string from the classification: one of
        `"shortlist"`, `"reject"`, or `"escalate"`.

    Raises:
        ValueError: If classification is missing from state.

    Example:
    ```
    route = router_node(state)
    print(route)  # "shortlist"
    ```
    """
    logger = log.node("[ROUTER]")
    c = _get_classification(state)
    logger.info(f"Routing to: {c.category.upper()}")
    return c.category


def shortlist_node(state: ApplicationState) -> dict:
    """Handles shortlisted applications by logging interview scheduling.

    Args:
        state: The current application state with populated
            `classification` and `cleaned` fields.

    Returns:
        A dict with `"decision"` set to `"shortlist"`.

    Raises:
        ValueError: If classification is missing from state.

    Example:
    ```
    result = shortlist_node(state)
    print(result["decision"])  # "shortlist"
    ```
    """
    logger = log.node("[SHORTLIST]")
    c = _get_classification(state)
    logger.start(f"Scheduling interview for: {state['cleaned']['name']}")
    logger.info(f"Score: {c.score}/100 | Urgency: {c.urgency}")
    logger.done(c.reasoning)
    return {"decision": "shortlist"}


def reject_node(state: ApplicationState) -> dict:
    """Handles rejected applications with an interactive confirmation prompt.

    Prompts the user to confirm the rejection. If confirmed, records
    the decision as `"reject"`; otherwise escalates to human review.

    Args:
        state: The current application state with populated
            `classification` and `cleaned` fields.

    Returns:
        A dict with `"decision"` set to `"reject"` if the user
        confirms, or `"escalate"` if the user cancels.

    Raises:
        ValueError: If classification is missing from state.

    Example:
    ```
    # User types "yes":
    result = reject_node(state)
    print(result["decision"])  # "reject"

    # User types anything else:
    result = reject_node(state)
    print(result["decision"])  # "escalate"
    ```
    """
    logger = log.node("[REJECT]")
    c = _get_classification(state)
    name = state["cleaned"]["name"]

    logger.start(f"About to send rejection to: {name}")
    logger.info(f"Score: {c.score}/100 | Reason: {c.reasoning}")
    logger.human_input(
        "Send rejection letter?"
        " Type 'yes' to confirm, anything else to escalate"
    )

    answer = input("  >>> ").strip().lower()

    if answer == "yes":
        logger.done(f"Rejection confirmed for: {name}")
        return {"decision": "reject"}
    else:
        log.node("[ESCALATE]").info(
            "Rejection cancelled — escalating to human review"
        )
        return {"decision": "escalate"}


def escalate_node(state: ApplicationState) -> dict:
    """Handles applications flagged for human review.

    Logs the candidate name, score, and missing information, then
    records the decision as `"escalate"`.

    Args:
        state: The current application state with populated
            `classification` and `cleaned` fields.

    Returns:
        A dict with `"decision"` set to `"escalate"`.

    Raises:
        ValueError: If classification is missing from state.

    Example:
    ```
    result = escalate_node(state)
    print(result["decision"])  # "escalate"
    ```
    """
    logger = log.node("[ESCALATE]")
    c = _get_classification(state)
    logger.start(
        f"Flagging for human review: {state['cleaned']['name']}"
    )
    logger.info(f"Score: {c.score}/100")
    logger.done(f"Missing info: {c.missing_info}")
    return {"decision": "escalate"}
