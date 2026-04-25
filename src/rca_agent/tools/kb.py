"""Knowledge-base / runbook search tools (stubs)."""
from __future__ import annotations

from typing import Any

from rca_agent.tools.base import rca_tool, stub_response


@rca_tool
def search_runbook(query: str) -> dict[str, Any]:
    """Search the runbook collection for relevant SOPs.

    Args:
        query: Free-form search query.

    Returns:
        Structured runbook hits. Currently a stub.
    """
    return stub_response("search_runbook", query=query)


@rca_tool
def search_kb(query: str) -> dict[str, Any]:
    """Search the broader incident / knowledge base.

    Args:
        query: Free-form search query.

    Returns:
        Structured KB hits. Currently a stub.
    """
    return stub_response("search_kb", query=query)
