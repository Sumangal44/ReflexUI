"""Module for interacting with different language models."""

from .client import Client as Client

# Import the default client if available.
try:
    from .anthropic_client import AnthropicClient as DefaultClient
except ImportError:

    def DefaultClient() -> Client | None:
        """Return a default client.

        Returns:
            None since no default client is available.
        """
        return None
