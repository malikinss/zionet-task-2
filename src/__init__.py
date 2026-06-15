# ./src/__init__.py

"""Public API for the src package.

This module re-exports the `run` function as the sole intended entry
point for processing applications through the pipeline.

Example:
    Importing from the package directly:
    ```
    from src import run

    run(
        application={
            "name": "Jane Doe",
            "email": "jane@example.com",
            "position": "Engineer",
            "experience_years": 5,
            "skills": ["Python", "SQL"],
            "cover_letter": "I am excited to apply.",
        },
        title="Jane Doe — Engineer"
    )
    ```
"""

from src.agent import run

__all__ = [
    "run"
]
