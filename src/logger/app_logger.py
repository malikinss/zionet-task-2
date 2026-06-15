# ./src/logger/app_logger.py

"""Application-level logger providing access to named node loggers.

This module provides AppLogger, a single entry point that lazily
instantiates and caches NodeLogger instances keyed by prefix, all
sharing one underlying Logger core.

Example:
    Basic usage::

        from src.logger.app_logger import AppLogger

        log = AppLogger("my_app")
        log.node("[LLM]").start("Invoking model")
        log.node("[TOOL]").info("Running calculator")
        log.node("[LLM]").done("Response received")
"""

from src.logger.subloggers import Logger, NodeLogger


class AppLogger:
    """A composite logger exposing named `NodeLogger` instances.

    Lazily instantiates `NodeLogger` instances on first access by
    prefix, caching them for reuse. All node loggers share a single
    underlying Logger core.

    Attributes:
        _core: Shared Logger instance used by all node loggers.
        _nodes: Cache mapping prefix strings to `NodeLogger` instances.

    Example:
    ```
    log = AppLogger("pipeline")
    log.node("[LLM]").start("Calling model")
    log.node("[TOOL]").info("Fetching weather")
    log.node("[LLM]").done("Final answer ready")
    ```
    """

    def __init__(self, name: str = "app"):
        """Initializes the `AppLogger` with a named core `Logger`.

        Args:
            name: Name passed to the underlying `Logger`. Defaults to
                `"app"`.

        Example:
        ```
        log = AppLogger()
        log = AppLogger("worker")
        ```
        """
        self._core = Logger(name)
        self._nodes: dict[str, NodeLogger] = {}

    def node(self, prefix: str) -> NodeLogger:
        """Returns a `NodeLogger` for the given prefix, creating it if needed.

        Caches the `NodeLogger` instance so the same object is returned
        on subsequent calls with the same prefix.

        Args:
            prefix: Label used as the node identifier, e.g. `"[LLM]"`
                or `"[TOOL]"`.

        Returns:
            A `NodeLogger` instance associated with the given prefix.

        Example:
        ```
        log.node("[LLM]").start("Invoking model")
        log.node("[TOOL]").info("Running calculator")
        log.node("[LLM]") is log.node("[LLM]")  # True
        ```
        """
        if prefix not in self._nodes:
            self._nodes[prefix] = NodeLogger(self._core, prefix)
        return self._nodes[prefix]
