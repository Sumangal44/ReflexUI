"""Base class to define agent tools."""

import inspect
from dataclasses import dataclass
from typing import Callable

# Convert Python types to JSON schema types.
TYPE_MAP = {
    "str": "string",
    "int": "number",
    "float": "number",
    "bool": "boolean",
    "list": "array",
    "dict": "object",
}


@dataclass(frozen=True)
class Tool:
    """A tool is a function that can be called by an agent."""

    # The name of the tool.
    name: str

    # A description of how the tool works - this should be detailed
    description: str

    # The function parameters and their types.
    params: tuple[tuple[str, str], ...]

    # The return type of the function.
    return_type: str

    # The function to call.
    fn: Callable

    @classmethod
    def from_function(cls, func: Callable) -> "Tool":
        """Create a tool from a function.

        Args:
            func: The function to convert to a tool.

        Returns:
            A new tool instance.
        """
        signature = inspect.signature(func)
        params = tuple(
            (
                (
                    name,
                    (
                        param.annotation.__name__
                        if hasattr(param.annotation, "__name__")
                        else "No annotation"
                    ),
                )
            )
            for name, param in signature.parameters.items()
        )
        return_type = (
            signature.return_annotation.__name__
            if hasattr(signature.return_annotation, "__name__")
            else "No annotation"
        )
        description = inspect.getdoc(func) or "No description"
        return cls(
            name=func.__name__,
            description=description,
            params=params,
            return_type=return_type,
            fn=func,
        )


def send_message(message: str) -> None:
    """Send a final message to the user. This should be done after all internal processing is completed.

    Args:
        message: The message to send to the user.
    """
    pass
