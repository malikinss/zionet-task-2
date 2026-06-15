# ./src/logger/__init__.py

"""Public API for the logger package.

This module re-exports `AppLogger` as the sole intended entry point
for logging across the application.

Example:
    Importing from the package directly:
    ```
    from src.logger import AppLogger

    log = AppLogger("my_app")
    log.node("[LLM]").start("Invoking model")
    log.node("[TOOL]").info("Running calculator")
    ```
"""

from src.logger.app_logger import AppLogger

__all__ = ["AppLogger"]
