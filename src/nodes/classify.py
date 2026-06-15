# ./src/nodes/classify.py

"""Classification node for the application processing pipeline.

This module provides the classify_node function and supporting helpers
that send cleaned application data to the LLM, parse the structured
classification response, and return it as an `ApplicationClassification`.

Example:
    Using the node in a graph:
    ```
    from src.nodes.classify import classify_node

    result = classify_node(state)
    print(result["classification"].category)  # "shortlist"
    print(result["classification"].score)      # 87
    ```
"""

from src.types.state import ApplicationState
from src.types.classification import ApplicationClassification
from src.prompts import CLASSIFIER_PROMPT
from src.llm import GroqClient
from src.logger import AppLogger

PREFIX: str = "[CLASSIFY]"
"""Log prefix identifying messages from the classification node."""

log = AppLogger("classify")
"""Module-level logger for the classification node."""


def classify_node(state: ApplicationState) -> dict:
    """Classifies a cleaned application using the LLM.

    Sends the cleaned application data to the LLM with `CLASSIFIER_PROMPT`
    as the system message, parses the `JSON` response into an
    `ApplicationClassification`, and returns it under the
    `"classification"` key.

    Args:
        state: The current application state. Must have a populated
            `cleaned` field with `position`, `name`,
            `experience_years`, `skills`, and `cover_letter`.

    Returns:
        A dict with a single key `"classification"` containing the
        parsed ApplicationClassification instance.

    Example:
    ```
    result = classify_node(state)
    print(result["classification"].category)  # "shortlist"
    print(result["classification"].urgency)   # "high"
    ```
    """
    logger = log.node(PREFIX)
    logger.start("Analyzing application with LLM")

    client = GroqClient()
    cleaned = state["cleaned"]

    raw_json = client.complete(
        system=CLASSIFIER_PROMPT,
        user=_get_user_message(cleaned),
    )
    raw_json = _extract_from_snippet(raw_json)
    classification = ApplicationClassification.model_validate_json(raw_json)

    logger.done(f"{classification.category} (score={classification.score})")

    return {"classification": classification}


def _extract_from_snippet(raw: str, language: str = "json") -> str:
    """Strips markdown code fence wrappers from a string.

    Removes leading and trailing triple-backtick fences, including an
    optional language tag, and strips surrounding whitespace.

    Args:
        raw: Raw string that may be wrapped in a markdown code fence.
        language: Language tag following the opening fence. Defaults
            to `"json"`.

    Returns:
        The unwrapped and stripped content string.

    Example:
    ```
    _extract_from_snippet("```json\\n{...}\\n```")  # "{...}"
    _extract_from_snippet("{...}")                   # "{...}"
    ```
    """
    fence = "```"
    return (
        raw
        .strip()
        .removeprefix(f"{fence}{language}")
        .removeprefix(fence)
        .removesuffix(fence)
        .strip()
    )


def _get_user_message(data: dict) -> str:
    """Formats cleaned application data into a user message string for the LLM.

    Args:
        data: Cleaned application dict with keys `position`, `name`,
            `experience_years`, `skills`, and `cover_letter`.

    Returns:
        A formatted multi-line string summarizing the application.

    Example:
    ```
    _get_user_message({
        "position": "Engineer",
        "name": "Jane Doe",
        "experience_years": 5,
        "skills": ["Python", "SQL"],
        "cover_letter": "I am excited to apply..."
    })
    # "Position: Engineer\\nCandidate: Jane Doe\\n..."
    ```
    """
    return (
        f"Position: {data['position']}\n"
        f"Candidate: {data['name']}\n"
        f"Experience: {data['experience_years']} years\n"
        f"Skills: {', '.join(data['skills'])}\n"
        f"Cover Letter: {data['cover_letter']}\n"
    )
