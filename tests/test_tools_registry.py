from __future__ import annotations

from langchain_core.tools import BaseTool

from rca_agent.tools import ALL_TOOLS


def test_registry_non_empty():
    assert len(ALL_TOOLS) > 0


def test_each_tool_is_basetool():
    for t in ALL_TOOLS:
        assert isinstance(t, BaseTool), f"{t!r} is not a BaseTool"


def test_unique_tool_names():
    names = [t.name for t in ALL_TOOLS]
    assert len(names) == len(set(names)), f"duplicate tool names: {names}"


def test_each_tool_has_description_and_schema():
    for t in ALL_TOOLS:
        assert t.description, f"{t.name}: missing description"
        # LangChain tools expose a JSON schema for arguments.
        schema = t.args_schema
        assert schema is not None, f"{t.name}: missing args_schema"


def test_expected_tools_present():
    names = {t.name for t in ALL_TOOLS}
    expected = {
        "run_shell",
        "search_logs",
        "fetch_logs",
        "query_metrics",
        "search_runbook",
        "search_kb",
    }
    assert expected.issubset(names), (
        f"missing expected tools: {expected - names}"
    )
