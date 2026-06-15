# ./src/types/__init__.py

"""Public API for the types package.

This module re-exports all types intended for use by other packages,
providing a single stable import point for state and classification
models.

Example:
    Importing from the package directly:
    ```
    from src.types import ApplicationClassification, ApplicationState

    state: ApplicationState = {
        "raw_input": {"name": "Jane Doe"},
        "cleaned": {},
        "classification": None,
        "decision": "",
    }
    ```
"""

from src.types.classification import ApplicationClassification
from src.types.state import ApplicationState

__all__ = [
    "ApplicationClassification",
    "ApplicationState"
]
