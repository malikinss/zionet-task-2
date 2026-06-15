# ./src/llm/__init__.py

"""Public API for the llm package.

This module re-exports `GroqClient` as the sole intended entry point
for LLM interactions across the application.

Example:
    Importing from the package directly:
    ```
    from src.llm import GroqClient

    client = GroqClient()
    reply = client.complete(
        system="You are a helpful assistant.",
        user="What is the capital of France?"
    )
    print(reply)  # "Paris"
    ```
"""

from src.llm.groq_client import GroqClient

__all__ = ["GroqClient"]
