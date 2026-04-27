"""Tool registry.

`ALL_TOOLS` is the single list of LangChain tools that the agent will be
built with. Adding a new tool = drop a new module here and append to the
list below.
"""
from __future__ import annotations

from langchain_core.tools import BaseTool

from rca_agent.tools.kb import search_kb, search_runbook
from rca_agent.tools.logs import fetch_logs, search_logs
from rca_agent.tools.metrics import query_metrics
from rca_agent.tools.shell import run_shell

ALL_TOOLS: list[BaseTool] = [
    run_shell,
    search_logs,
    fetch_logs,
    query_metrics,
    search_runbook,
    search_kb,
]

__all__ = [
    "ALL_TOOLS",
    "run_shell",
    "search_logs",
    "fetch_logs",
    "query_metrics",
    "search_runbook",
    "search_kb",
]
