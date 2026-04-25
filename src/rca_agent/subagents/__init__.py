"""Subagent registry.

`ALL_SUBAGENTS` is the list passed to `create_deep_agent(subagents=...)`.
Adding a new subagent = drop a new module here and append to the list.
"""
from __future__ import annotations

from deepagents import SubAgent

from rca_agent.subagents.hypothesis_validator import hypothesis_validator
from rca_agent.subagents.log_analyzer import log_analyzer
from rca_agent.subagents.metric_analyzer import metric_analyzer

ALL_SUBAGENTS: list[SubAgent] = [
    log_analyzer,
    metric_analyzer,
    hypothesis_validator,
]

__all__ = [
    "ALL_SUBAGENTS",
    "log_analyzer",
    "metric_analyzer",
    "hypothesis_validator",
]
