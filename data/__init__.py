# ./src/data/__init__.py

"""Public API for the data package.

This module re-exports `APPLICATIONS` as the sole intended entry point
for accessing sample application data.

Example:
    Importing from the package directly:
    ```
        from data import APPLICATIONS
        from src import run

        for title, application in APPLICATIONS.items():
            run(application=application, title=title)
    ```
"""

from data.samples import APPLICATIONS

__all__ = [
    "APPLICATIONS"
]
