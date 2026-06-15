# ./src/nodes/preprocess.py

"""Preprocessing node for the application processing pipeline.

This module provides the `preprocess_node` function that validates and
normalizes raw application input into a cleaned dict ready for
downstream nodes.

Example:
    Using the node in a graph:
    ```
    from src.nodes.preprocess import preprocess_node

    result = preprocess_node(state)
    print(result["cleaned"]["name"])      # "Jane Doe"
    print(result["cleaned"]["skills"])    # ["python", "sql"]
    ```
"""

from src.types.state import ApplicationState
from src.logger import AppLogger

log = AppLogger("preprocess")
"""Module-level logger for the preprocessing node."""


def preprocess_node(state: ApplicationState) -> dict:
    """Cleans and normalizes raw application data.

    Reads raw_input from state and produces a cleaned dict with
    normalized name casing, lowercased email and skills, a parsed
    integer experience value, and stripped whitespace throughout.

    Args:
        state: The current application state. Must have a populated
            `raw_input` field. Missing keys default to empty strings,
            empty lists, or zero as appropriate.

    Returns:
        A dict with a single key `"cleaned"` containing the
        normalized application data with keys `name`, `email`,
        `position`, `experience_years`, `skills`,
        and `cover_letter`.

    Example:
    ```
    result = preprocess_node({
        "raw_input": {
            "name": "jane doe",
            "email": "Jane@Example.COM",
            "position": "Engineer",
            "experience_years": "5",
            "skills": [" Python ", "SQL"],
            "cover_letter": "  I am excited to apply.  ",
        },
        "cleaned": {},
        "classification": None,
        "decision": "",
    })
    result["cleaned"]["name"]   # "Jane Doe"
    result["cleaned"]["email"]  # "jane@example.com"
    result["cleaned"]["skills"] # ["python", "sql"]
    ```
    """
    logger = log.node("[PREPROCESS]")
    logger.start("Cleaning application data")

    raw = state["raw_input"]

    cleaned = {
        "name": raw.get("name", "").strip().title(),
        "email": raw.get("email", "").strip().lower(),
        "position": raw.get("position", "").strip(),
        "experience_years": int(raw.get("experience_years", 0)),
        "skills": [s.strip().lower() for s in raw.get("skills", [])],
        "cover_letter": raw.get("cover_letter", "").strip(),
    }

    logger.done(f"{cleaned['name']} → {cleaned['position']}")

    return {"cleaned": cleaned}
