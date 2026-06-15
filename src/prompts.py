# ./src/prompts.py

"""System prompt definitions for the application processing pipeline.

This module contains prompt strings injected into LLM calls to
establish the model's role, output format, and routing rules.

Example:
    Using the classifier prompt in an LLM call:
    ```
    from src.prompts import CLASSIFIER_PROMPT
    from src.llm import GroqClient

    client = GroqClient()
    reply = client.complete(
        system=CLASSIFIER_PROMPT, user=application_text
    )
    ```
"""

CLASSIFIER_PROMPT = """
You are an expert HR recruiter reviewing job applications.

Analyze the application and return a JSON object with these exact fields:
- category: one of "shortlist", "reject", "escalate"
- urgency: one of "high", "medium", "low"
- missing_info: list of strings (what information is missing)
- reasoning: string (explain your decision)
- score: integer 0-100 (overall candidate score)

Routing rules:
- shortlist: score >= 70, strong match for the role
- escalate: score 40-69, OR missing critical info, needs human review
- reject: score < 40, clearly not a fit

Return ONLY valid JSON, no extra text.
"""
"""System prompt for the HR classifier LLM call.

Instructs the model to act as an HR recruiter, evaluate a job
application, and return a structured `JSON` object following the
`ApplicationClassification` schema. Defines score thresholds for
each routing category.
"""
