"""Log search / fetch tools (stubs)."""
from __future__ import annotations

from typing import Any

from rca_agent.tools.base import rca_tool, stub_response


@rca_tool
def search_logs(query: str, since: str | None = None) -> dict[str, Any]:
    """Search application logs for matching lines.

    Args:
        query: Free-form search query (keywords, regex, structured selector).
        since: Optional ISO-8601 timestamp; only return lines at or after this.

    Returns:
        Structured search hits. Currently a stub.
    """
    return stub_response("search_logs", query=query, since=since)


@rca_tool
def fetch_logs(source: str, lines: int = 200) -> dict[str, Any]:
    """Fetch the most recent log lines from a named source.

    Args:
        source: Logical source name (e.g. "api-server", "worker.stdout").
        lines: Number of lines to return (default 200).

    Returns:
        Structured log payload. Currently a stub.
    """
    return stub_response("fetch_logs", source=source, lines=lines)
