# ./src/types/classification.py

"""Pydantic model for application classification results.

This module defines the structured output produced by the classifier
node, capturing the category decision, urgency level, missing
information, reasoning, and a numeric score.

Example:
    Constructing a classification result:
    ```
    from src.types.classification import ApplicationClassification

    result = ApplicationClassification(
        category="shortlist",
        urgency="high",
        missing_info=[],
        reasoning="Strong experience and relevant skills.",
        score=87
    )
    print(result.category)  # "shortlist"
    print(result.score)     # 87
    ```
"""

from typing import Literal
from pydantic import BaseModel


class ApplicationClassification(BaseModel):
    """Structured classification result for a processed application.

    Attributes:
        category: Routing decision for the application. One of
            `"shortlist"`, `"reject"`, or `"escalate"`.
        urgency: Priority level for handling the application. One of
            `"high"`, `"medium"`, or `"low"`.
        missing_info: List of fields or documents absent from the
            application that are required for a full assessment.
        reasoning: Human-readable explanation of the classification
            decision.
        score: Numeric quality score for the application, from 0
            (poorest) to 100 (strongest).

    Example:
    ```
    result = ApplicationClassification(
        category="escalate",
        urgency="medium",
        missing_info=["cover_letter", "references"],
        reasoning="Relevant experience but incomplete submission.",
        score=62
    )
    print(result.missing_info)  # ["cover_letter", "references"]
    ```
    """

    category: Literal["shortlist", "reject", "escalate"]
    urgency: Literal["high", "medium", "low"]
    missing_info: list[str]
    reasoning: str
    score: int  # 0-100
