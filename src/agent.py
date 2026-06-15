# ./src/agent.py

"""Agent entry point for streaming application processing.

This module provides the run function that builds the processing graph
and streams an application dict through it, logging each completed
node.

Example:
    Processing an application:
    ```
    from src.agent import run

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

from src.graph import build_graph
from src.logger import AppLogger

log = AppLogger("agent")
"""Module-level logger for the agent entry point."""

PREFIX: str = "[MAIN]"
"""Log prefix identifying messages from the agent entry point."""


def run(application: dict, title: str) -> None:
    """Builds the graph and streams an application through the pipeline.

    Constructs the processing graph, streams the application dict
    through it, and logs each completed node. Logs a start message
    before streaming and a done message after all nodes complete.

    Args:
        application: Raw application data dict passed as `raw_input`
            to the graph. Expected keys include `name`, `email`,
            `position`, `experience_years`, `skills`, and
            `cover_letter`.
        title: Human-readable label for the run, used in start and
            done log messages.

    Example:
    ```
    run(
        application={"name": "Jane Doe", "position": "Engineer", ...},
        title="Jane Doe — Engineer"
    )
    # [MAIN] Starting: Jane Doe — Engineer
    # [MAIN] Node 'preprocess' completed
    # [MAIN] Node 'classify' completed
    # [MAIN] Node 'shortlist' completed
    # [MAIN] Done: Jane Doe — Engineer
    ```
    """
    logger = log.node(PREFIX)
    logger.start(title)
    graph = build_graph()
    for event in graph.stream({"raw_input": application}):
        for node_name in event:
            logger.info(f"Node '{node_name}' completed")
    logger.done(title, separator=False)
