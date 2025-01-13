from __future__ import annotations
import os
from dataclasses import dataclass, field
from typing import Any, AsyncGenerator, Type, Sequence

# Try to import the anthropic library.
try:
    from anthropic import AsyncAnthropic  # type: ignore
    from anthropic.types import ToolUseBlock  # type: ignore
    from pydantic import BaseModel  # type: ignore
except ImportError:
    raise ImportError(
        "The anthropic library is required for the AnthropicClient. "
        "Please install it using `pip install anthropic`."
    )
from flexai.llm.client import Client
from flexai.message import (
    AIMessage,
    Message,
    UserMessage,
    ToolCall,
    ToolResult,
    MessageContent,
    TextBlock,
)
from flexai.tool import Tool, TYPE_MAP


ANTHROPIC_BETA_HEADERS = [
    "max-tokens-3-5-sonnet-2024-07-15",
    "prompt-caching-2024-07-31",
]


def get_tool_call(tool_use: ToolUseBlock) -> ToolCall:
    """Get the tool call from a tool use block.

    Args:
        tool_use: The tool use block to get the call from.

    Returns:
        The tool call from the tool use block.
    """
    return ToolCall(
        id=tool_use.id,
        name=tool_use.name,
        input=tool_use.input,
    )


@dataclass(frozen=True)
class AnthropicClient(Client):
    """Client for interacting with the Anthropic language model."""

    # The client to use for interacting with the model.
    client: AsyncAnthropic = AsyncAnthropic()

    # The model to use for generating responses.
    model: str = os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620")

    # The maximum number of tokens to generate in a response.
    max_tokens: int = 8192

    # Whether to cache messages or not.
    cache_messages: bool = True

    # Extra headers to include in the request.
    extra_headers: dict = field(
        default_factory=lambda: {"anthropic-beta": ",".join(ANTHROPIC_BETA_HEADERS)}
    )

    async def get_chat_response(
        self,
        messages: list[Message],
        system: str = "",
        tools: list[Tool] | None = None,
        force_tool: bool = True,
    ) -> AIMessage:
        # Send the messages to the model and get the response.
        response = await self.client.beta.prompt_caching.messages.create(
            **self._get_params(messages, system, tools, force_tool)
        )

        # Parse out the tool uses from the response.
        tool_uses = [
            get_tool_call(message)
            for message in response.content
            if isinstance(message, ToolUseBlock)
        ]

        # Get the content to return.
        content_to_return = tool_uses or "\n".join(
            [message.text for message in response.content]
        )
        return AIMessage(
            content=content_to_return,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
        )

    async def stream_chat_response(  # type: ignore
        self,
        messages: list[Message],
        system: str = "",
        tools: list[Tool] | None = None,
    ) -> AsyncGenerator[AIMessage, None]:
        async with self.client.messages.stream(
            **self._get_params(messages, system, tools)
        ) as stream:
            async for text in stream.text_stream:
                yield AIMessage(content=text)  # type: ignore

    def _add_cache_control(self, params: dict) -> dict:
        """Add cache control to the params.

        Args:
            params: The params to add cache control to.

        Returns:
            The params with cache control added.
        """
        if not self.cache_messages:
            return params

        cache_control = {
            "cache_control": {
                "type": "ephemeral",
            }
        }

        # Cache the system message.
        params["system"] = [
            {
                "type": "text",
                "text": params["system"],
                **cache_control,
            }
        ]

        # Cache tool definitions.
        if "tools" in params and len(params["tools"]) > 0:
            params["tools"][-1].update(**cache_control)

        # Cache the last two user messages.
        user_idxs = [
            idx
            for idx, message in enumerate(params["messages"])
            if message["role"] == "user"
        ]
        for idx in user_idxs[-2:]:
            message = params["messages"][idx]
            if isinstance(message["content"], str):
                message["content"] = [{"type": "text", "text": message["content"]}]
            message["content"][-1].update(**cache_control)

        return params

    def _get_params(
        self, messages: list[Message], system: str, tools: list[Tool] | None, force_tool: bool = True
    ) -> dict:
        """Get the common params to send to the model.

        Args:
            messages: The messages to send to the model.
            system: The system message to send to the model.
            tools: The tools to send to the model.
            force_tool: Whether to force the model to use the tools.

        Returns:
            The common params to send to the model.
        """
        kwargs = {
            "max_tokens": self.max_tokens,
            "messages": self.format_content(messages),
            "model": self.model,
            "system": self.format_content(system),
            "extra_headers": self.extra_headers,
        }

        # If tools are provided, force the model to use them (for now).
        if tools:
            kwargs["tools"] = [self.format_tool(tool) for tool in tools]
            if force_tool:
                kwargs["tool_choice"] = {"type": "any"}
        else:
            kwargs["tools"] = []

        # Add cache control to the params.
        params = self._add_cache_control(kwargs)
        return params

    async def get_structured_response(
        self,
        messages: list[Message],
        model: Type[BaseModel],
        system: str = "",
        tools: list[Tool] | None = None,
    ) -> BaseModel:
        """Get the structured response from the chat model.

        Args:
            messages: The messages to send to the model.
            model: The model to use for the response.
            system: Optional system message to set the behavior of the AI.
            tools: Tools to use in the response.

        Returns:
            The structured response from the model.

        Raises:
            ValueError: If the response is not a string.
        """
        schema = model.schema()  # type: ignore
        system = f"""{system}
Return your answer according to the 'properties' of the following schema:
{schema}
Return only the JSON object with the properties filled in.
Do not include anything in your response other than the JSON object.
Do not begin your response with ```json or end it with ```.
"""
        response = await self.get_chat_response(messages, system=system, tools=tools, force_tool=False)
        response.content = str(response.content)
        content = response.content
        try:
            if not isinstance(content, str):
                raise ValueError("The response is not a string.")
            return model.parse_raw(content)  # type: ignore
        except Exception as e:
            # Try again, printing the exception.
            messages = messages + [
                response,
                UserMessage(
                    content=f"There was an error while parsing. Make sure to only include the JSON. Error: {e}"
                ),
            ]
            return await self.get_structured_response(
                messages, model=model, system=system, tools=tools
            )

    @staticmethod
    def format_tool(tool: Tool) -> dict:
        """Convert the tool to a description.

        Args:
            tool: The tool to format.

        Returns:
            A dictionary describing the tool.
        """
        input_schema = {
            "type": "object",
            "properties": {},
        }
        for param_name, param_type in tool.params:
            param_type = TYPE_MAP.get(str(param_type), param_type)
            input_schema["properties"][param_name] = {
                "type": param_type,
            }

        description = {
            "name": tool.name,
            "description": tool.description,
            "input_schema": input_schema,
        }
        return description

    @classmethod
    def format_content(
        cls,
        value: str
        | Message
        | MessageContent
        | Sequence[MessageContent]
        | Sequence[Message],
    ) -> Any:
        """Format the message content for the Anthropic model.

        Args:
            value: The value to format.

        Returns:
            The formatted message content.

        Raises:
            ValueError: If the message content type is unknown.
        """
        # Base types.
        if isinstance(value, str):
            return value
        if isinstance(value, list):
            return [cls.format_content(v) for v in value]

        # Anthropic message format.
        if isinstance(value, Message):
            return {"role": value.role, "content": cls.format_content(value.content)}

        # Message content types.
        if isinstance(value, TextBlock):
            return {
                "type": "text",
                "text": value.text,
            }
        if isinstance(value, ToolCall):
            return {
                "type": "tool_use",
                "id": value.id,
                "name": value.name,
                "input": value.input,
            }
        if isinstance(value, ToolResult):
            return {
                "type": "tool_result",
                "tool_use_id": value.tool_call_id,
                "content": str(value.result),
                "is_error": value.is_error,
            }

        raise ValueError(f"Unknown message content type: {value}")

    @classmethod
    def load_content(
        cls, content: str | list[dict[str, Any]]
    ) -> str | list[MessageContent]:
        """Load the message content from the Anthropic model to dataclasses.

        Args:
            content: The content to load.

        Returns:
            The loaded message content
        """
        # If it's a string, return it.
        if isinstance(content, str):
            return content

        # If it's a list of dictionaries, parse them.
        assert isinstance(content, list)
        parsed_content: list[MessageContent] = []

        for entry in content:
            match entry.pop("type"):
                case "text":
                    parsed_content.append(TextBlock(**entry))
                case "tool_use":
                    parsed_content.append(ToolCall(**entry))
                case "tool_result":
                    parsed_content.append(
                        ToolResult(
                            tool_call_id=entry.pop("tool_use_id"),
                            result=entry.pop("content"),
                            **entry,
                        )
                    )

        return parsed_content
