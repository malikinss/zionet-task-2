# ./src/data/samples.py

"""Sample application data for testing the processing pipeline.

This module provides a dict of example job applications covering
different candidate profiles, intended for use in manual runs,
demos, and integration tests.

Example:
    Iterating over all samples:
    ```
    from src.data.samples import APPLICATIONS
    from src import run

    for title, application in APPLICATIONS.items():
        run(application=application, title=title)
    ```
"""

APPLICATIONS: dict[str, dict] = {
    "Strong candidate — John Doe": {
        "name": "  john doe  ",
        "email": "  John.Doe@Gmail.COM  ",
        "position": "Senior Python Developer",
        "experience_years": "5",
        "skills": ["Python", "FastAPI", " PostgreSQL ", "Docker"],
        "cover_letter": (
            "I have 5 years of experience building scalable APIs"
            " with Python and FastAPI. I led a team of 3 engineers "
            "at my last company."
        ),
    },

    "Weak candidate — Jane Smith": {
        "name": "jane smith",
        "email": "JANE@MAIL.COM",
        "position": "Senior Python Developer",
        "experience_years": "1",
        "skills": ["Excel", "Word"],
        "cover_letter": "I want to learn programming.",
    }
}
"""Sample job applications keyed by descriptive title.

Each entry maps a human-readable candidate label to a raw application
dict matching the expected `raw_input` schema. Values are intentionally
unclean to exercise the preprocessing node.
"""
