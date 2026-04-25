from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Any


@dataclass(slots=True)
class ToolSpec:
    """Declarative tool definition for future extensibility."""

    name: str
    description: str
    handler: Callable[..., Any] | None = None


def build_toolset() -> list[Callable[..., Any]]:
    """Build actual deepagents-compatible callables.

    MVP intentionally returns an empty list while preserving extension points.
    """
    return []
