"""Tool authoring helpers.

`rca_tool` is a thin wrapper around `langchain_core.tools.tool` so that every
RCA tool has a uniform shape (typed args, JSON-serializable dict return,
explicit description from the docstring).

`stub_response` is the canonical "I'm not implemented yet" payload — used by
every stub tool so the agent loop can keep reasoning instead of crashing.
"""
from __future__ import annotations

from typing import Any

from langchain_core.tools import tool as _lc_tool


def stub_response(name: str, **kwargs: Any) -> dict[str, Any]:
    """Return the canonical stub payload for a not-yet-implemented tool."""
    return {
        "status": "stub",
        "tool": name,
        "args": kwargs,
        "note": "implementation pending — wire up the real backend in tools/",
    }


# Re-export LangChain's @tool decorator under a project-local name so we own
# the import surface. Future cross-cutting concerns (auditing, rate limiting,
# tracing) can be layered here without touching individual tool modules.
rca_tool = _lc_tool

__all__ = ["rca_tool", "stub_response"]
