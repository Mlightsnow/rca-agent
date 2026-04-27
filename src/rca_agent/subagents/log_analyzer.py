"""log_analyzer subagent: narrows in on suspicious log lines."""
from __future__ import annotations

from rca_agent.prompts import load_prompt
from rca_agent.subagents.registry import build_subagent
from rca_agent.tools import fetch_logs, search_logs

log_analyzer = build_subagent(
    name="log_analyzer",
    description=(
        "Use when you need to find specific log lines, error patterns, or "
        "request traces in the application logs."
    ),
    prompt=load_prompt("subagents/log_analyzer"),
    tools=[search_logs, fetch_logs],
)
