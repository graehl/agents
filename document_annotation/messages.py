"""Authored user/assistant messages forming the fixed annotation context."""

from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class FixedMessage:
    role: Literal["user", "assistant"]
    content: str

    def __post_init__(self) -> None:
        if self.role not in ("user", "assistant"):
            raise ValueError("fixed message role must be user or assistant")
        if not isinstance(self.content, str) or not self.content:
            raise ValueError("fixed message content must be a nonempty string")

    def response_item(self) -> dict[str, Any]:
        return {
            "type": "message",
            "role": self.role,
            "content": [
                {
                    "type": "input_text" if self.role == "user" else "output_text",
                    "text": self.content,
                }
            ],
        }
