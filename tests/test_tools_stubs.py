from __future__ import annotations

import pytest

from rca_agent.tools import ALL_TOOLS
from rca_agent.tools.base import stub_response


def test_stub_response_shape():
    payload = stub_response("foo", a=1, b="x")
    assert payload["status"] == "stub"
    assert payload["tool"] == "foo"
    assert payload["args"] == {"a": 1, "b": "x"}
    assert "implementation pending" in payload["note"].lower()


# Each tool must accept its declared args (we exercise minimal valid input)
# and return a structured stub payload — never raise.
TOOL_CALLS: dict[str, dict] = {
    "run_shell": {"cmd": "echo hi"},
    "search_logs": {"query": "ERROR"},
    "fetch_logs": {"source": "stdout"},
    "query_metrics": {"promql": "up"},
    "search_runbook": {"query": "5xx spike"},
    "search_kb": {"query": "5xx spike"},
}


@pytest.mark.parametrize("tool_name,kwargs", list(TOOL_CALLS.items()))
def test_each_stub_returns_stub_payload(tool_name, kwargs):
    by_name = {t.name: t for t in ALL_TOOLS}
    assert tool_name in by_name, f"tool not registered: {tool_name}"
    tool = by_name[tool_name]
    result = tool.invoke(kwargs)
    assert isinstance(result, dict), f"{tool_name} did not return a dict: {result!r}"
    assert result["status"] == "stub", f"{tool_name} did not return a stub payload"
    assert result["tool"] == tool_name
