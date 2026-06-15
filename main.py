# ./main.py

"""Entry point for running all sample applications through the pipeline.

This script loads environment variables and processes every entry in
`APPLICATIONS`, streaming each one through the full preprocessing,
classification, and routing pipeline.

Example:
    Running directly:
    ```
    $ python main.py
    ```
"""

from dotenv import load_dotenv
from src.agent import run
from data.samples import APPLICATIONS

load_dotenv()


def main():
    """Processes all sample applications through the pipeline.

    Iterates over `APPLICATIONS` and calls run for each entry, using
    the dict key as the display title.

    Example:
    ```
    main()
    # [MAIN] Starting: Strong candidate — John Doe
    # ...
    # [MAIN] Starting: Weak candidate — Jane Smith
    # ...
    ```
    """
    for title, sample in APPLICATIONS.items():
        run(sample, title)


if __name__ == "__main__":
    main()
