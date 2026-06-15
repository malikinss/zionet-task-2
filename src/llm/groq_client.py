# ./src/llm/groq_client.py

"""Groq LLM client for simple single-turn completions.

This module provides a lightweight `GroqClient` that sends a system
and user message pair to the Groq chat completions API and returns
the response as a plain string.

Example:
    Basic usage:
    ```
        from src.llm.groq_client import GroqClient

        client = GroqClient()
        reply = client.complete(
            system="You are a helpful assistant.",
            user="What is the capital of France?"
        )
        print(reply)  # "Paris"
    ```
"""

import os
from typing import Optional
from groq import Groq

MODEL: str = os.getenv("MODEL_NAME", "llama-3.3-70b-versatile")
"""Active Groq model name, resolved from the `MODEL_NAME` env var.

Falls back to `"llama-3.3-70b-versatile"` if the variable is not set.
"""

API_KEY: Optional[str] = os.getenv("GROQ_API_KEY")
"""Groq API key read from the `GROQ_API_KEY` environment variable."""


class GroqClient:
    """A lightweight Groq client for single-turn chat completions.

    Sends a system and user message pair to the Groq API and returns
    the assistant's reply as a plain string.

    Attributes:
        _client: Authenticated `Groq` client instance.

    Example:
    ```
    client = GroqClient()
    reply = client.complete(
        system="You are a concise assistant.",
        user="Name the planets in the solar system."
    )
    print(reply)
    ```
    """

    def __init__(self):
        """Initializes the Groq client using the module-level `API_KEY`.

        Example:
        ```
        client = GroqClient()
        ```
        """
        self._client = Groq(api_key=API_KEY)

    def complete(self, system: str, user: str) -> str:
        """Sends a system and user message to the Groq API and returns
        the reply.

        Args:
            system: System prompt establishing the assistant's behavior.
            user: User message to send to the model.

        Returns:
            The assistant's reply as a plain string, or an empty string
            if the response content is `None`.

        Example:
        ```
        client.complete(
            system="You are a helpful assistant.",
            user="What is 2 + 2?"
        )
        # "4"
        ```
        """
        response = self._client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return response.choices[0].message.content or ""
