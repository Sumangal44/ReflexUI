"""Capabilities define hooks that can plug into the agent's pipeline."""

from abc import ABC
from dataclasses import dataclass

from flexai.message import Message, AIMessage


@dataclass(frozen=True)
class Capability(ABC):
    """Abstract base class for defining cognitive capabilities of an agent.

    Provides hooks to modify the agent's behavior at different stages of
    the conversation pipeline, allowing for customization of prompts,
    messages, and responses.
    """

    async def modify_prompt(self, prompt: str) -> str:
        """Modify the system prompt before it's sent to the LLM.

        Args:
            prompt: The current system prompt.

        Returns:
            The modified system prompt.
        """
        return prompt

    async def modify_messages(self, messages: list[Message]) -> list[Message]:
        """Modify the conversation messages before sending them to the LLM.

        This method can be used to add, remove, or alter messages in the
        conversation history before they are processed by the language model.

        Args:
            messages: The current conversation messages.

        Returns:
            The modified list of messages.
        """
        return messages

    async def modify_response(
        self, messages: list[Message], response: AIMessage
    ) -> AIMessage:
        """Modify the AI-generated response before sending it to the user.

        This method allows for post-processing of the AI's response, which
        can include filtering, reformatting, or augmenting the content.

        Args:
            messages: The current conversation messages.
            response: The AI-generated response.

        Returns:
            The modified AI response.
        """
        return response
