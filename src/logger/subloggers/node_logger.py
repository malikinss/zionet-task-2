# ./src/logger/subloggers/node_logger.py

"""Structured logger for graph node lifecycle events.

This module provides `NodeLogger`, a thin wrapper around `Logger` that
formats node-specific events such as start, completion, info messages,
errors, and human input prompts with consistent colorized prefixes.

Example:
    Basic usage:
    ```
    from src.logger.subloggers.logger import Logger
    from src.logger.subloggers.node_logger import NodeLogger

    log = NodeLogger(core=Logger("graph"))
    log.start("Processing input")
    log.info("Calling LLM")
    log.done("Response received")
    ```

    With a custom prefix:
    ```
    log = NodeLogger(core=Logger("graph"), prefix="[LLM]")
    log.start("Invoking model")
    ```
"""

from typing import Optional
from src.logger.subloggers.logger import Logger
from src.logger.subloggers.colors import CYAN, YELLOW, GREEN, RED, PINK, BOLD


class NodeLogger:
    """A structured logger for graph node lifecycle events.

    Wraps a `Logger` instance and emits consistently formatted,
    colorized messages for the key stages of a node execution.
    The prefix label can be overridden at instantiation time.

    Attributes:
        PREFIX: Label prepended to every message emitted by this logger.

    Example:
    ```
    core = Logger("graph")
    log = NodeLogger(core)
    log.start("Fetching data")
    log.info("Cache miss, querying API")
    log.done("Data ready")
    ```
    """

    PREFIX: str = "[NODE]"
    """Default label prepended to every message emitted by this logger."""

    def __init__(self, core: Logger, prefix: Optional[str] = None):
        """Initializes the node logger with an underlying `Logger`
        and optional prefix.

        Args:
            core: A `Logger` instance used for all output.
            prefix: Optional override for `PREFIX`. If provided, replaces
                the class-level default for this instance.

        Example:
        ```
        log = NodeLogger(core=Logger("graph"))
        log = NodeLogger(core=Logger("graph"), prefix="[LLM]")
        ```
        """
        self._core = core
        if prefix:
            self.PREFIX = prefix

    def start(self, msg: str, separator: bool = True):
        """Logs the beginning of a node execution.

        Optionally emits a separator before the start message.

        Args:
            msg: Description of what the node is starting.
            separator: Whether to print a separator line before the
                message. Defaults to `True`.

        Example:
        ```
        log.start("Processing user input")
        # ============================================================
        # [NODE] Starting: Processing user input
        ```
        """
        if separator:
            self._core.separator()
        self._log(f"Starting: {self._core.colorize(msg, CYAN)}")

    def done(self, msg: str, separator: bool = True):
        """Logs the successful completion of a node execution.

        Optionally emits a separator and a blank line after the message.

        Args:
            msg: Description of what the node completed.
            separator: Whether to print a separator line after the
                message. Defaults to `True`.

        Example:
        ```
        log.done("Response received")
        # [NODE] Done: Response received
        # ============================================================
        ```
        """
        self._log(f"Done: {self._core.colorize(msg, GREEN)}")
        if separator:
            self._core.separator()
        print()

    def info(self, msg: str):
        """Logs an informational message in yellow at `INFO` level.

        Args:
            msg: Message text to log.

        Example:
        ```
        log.info("Waiting for tool result")
        # [NODE] Waiting for tool result
        ```
        """
        self._log(self._core.colorize(msg, YELLOW))

    def error(self, msg: str):
        """Logs an error message in red at `ERROR` level with the node prefix.

        Args:
            msg: Error message text.

        Example:
        ```
        log.error("Tool execution failed")
        # [NODE] Tool execution failed
        ```
        """
        self._core.error(f"{self.prefix} {self._core.colorize(msg, RED)}")

    def human_input(self, msg: str):
        """Logs a human input prompt with a warning emoji in yellow.

        Args:
            msg: Message text describing the expected human input.

        Example:
        ```
        log.human_input("Waiting for user confirmation")
        # [NODE] Waiting for user confirmation
        ```
        """
        self._log(f"{self._core.colorize(msg, YELLOW)}")

    def _log(self, msg: str):
        """Logs an info-level message with the colorized node prefix.

        Args:
            msg: Message text to log.

        Example:
        ```
        self._log("Thinking...")
        # [NODE] Thinking...
        ```
        """
        self._core.info(f"{self.prefix} {msg}")

    @property
    def prefix(self) -> str:
        """Returns the colorized node prefix string.

        Renders `PREFIX` in bold pink using the underlying Logger's
        colorize method.

        Returns:
            A bold pink ANSI-colored string of `PREFIX`.

        Example:
        ```
        print(log.prefix)  # \x1b[95m\x1b[1m[NODE]\x1b[0m
        ```
        """
        return self._core.colorize(self.PREFIX, PINK, BOLD)
