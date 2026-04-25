"""hypothesis_validator subagent: confirms or refutes a candidate root cause.

This is also where we exercise the SKILL.md integration seam — the example
skill pack is mounted via `skills=[...]` so deepagents' SkillsMiddleware
makes its checklist available to the subagent.
"""
from __future__ import annotations

from rca_agent.prompts import load_prompt
from rca_agent.skills import skill_path
from rca_agent.subagents.registry import build_subagent
from rca_agent.tools import run_shell, search_kb

hypothesis_validator = build_subagent(
    name="hypothesis_validator",
    description=(
        "Use when you have a candidate root cause and need to design and "
        "run targeted read-only checks that either confirm or refute it."
    ),
    prompt=load_prompt("subagents/hypothesis_validator"),
    tools=[run_shell, search_kb],
    skills=[skill_path("example_skill")],
)
