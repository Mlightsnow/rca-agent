"""metric_analyzer subagent: investigates metric anomalies."""
from __future__ import annotations

from rca_agent.prompts import load_prompt
from rca_agent.subagents.registry import build_subagent
from rca_agent.tools import query_metrics

metric_analyzer = build_subagent(
    name="metric_analyzer",
    description=(
        "Use when you need to investigate time-series metrics — latency, "
        "error rate, saturation, traffic — for an incident window."
    ),
    prompt=load_prompt("subagents/metric_analyzer"),
    tools=[query_metrics],
)
