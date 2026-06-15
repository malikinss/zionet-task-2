# ./src/types/state.py

"""State definition for the application processing pipeline.

This module defines the ApplicationState `TypedDict` used as the shared
state object passed between nodes in the processing graph.

Example:
    Initializing a state dict:
    ```
    from src.types.state import ApplicationState

    state: ApplicationState = {
        "raw_input": {"name": "Jane Doe", "score": "85"},
        "cleaned": {},
        "classification": None,
        "decision": "",
    }
    ```
"""

from typing import Any, Optional
from typing_extensions import TypedDict
from src.types.classification import ApplicationClassification


class ApplicationState(TypedDict):
    """Shared state passed between nodes in the application processing graph.

    Attributes:
        raw_input: Unprocessed input data as received from the source,
            prior to any validation or cleaning.
        cleaned: Validated and normalized version of raw_input, produced
            by the cleaning node.
        classification: Classification result produced by the classifier
            node, or None if classification has not yet occurred.
        decision: Final routing decision string produced by the decision
            node, e.g. `"shortlist"`, `"reject"`, or `"escalate"`.

    Example:
    ```
    state: ApplicationState = {
        "raw_input": {"name": "Jane Doe", "experience": "5 years"},
        "cleaned": {"name": "Jane Doe", "experience_years": 5},
        "classification": ApplicationClassification(
            category="shortlist",
            urgency="high",
            missing_info=[],
            reasoning="Strong profile.",
            score=90
        ),
        "decision": "shortlist",
    }
    ```
    """

    raw_input: dict[str, Any]
    cleaned: dict[str, Any]
    classification: Optional[ApplicationClassification]
    decision: str
