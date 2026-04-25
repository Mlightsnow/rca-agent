"""Helpers for building deepagents `SubAgent` dicts.

This is the **only** module that imports the `SubAgent` shape from
deepagents. Per the plan, if deepagents renames a field, only this file
changes. Every concrete subagent in `rca_agent/subagents/*.py` calls
`build_subagent(...)` to produce its registry entry.
"""
from __future__ import annotations

from typing import Any

from deepagents import SubAgent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

REQUIRED_KEYS = ("name", "description", "system_prompt")


def build_subagent(
    *,
    name: str,
    description: str,
    prompt: str,
    tools: list[BaseTool] | None = None,
    model: str | BaseChatModel | None = None,
    skills: list[str] | None = None,
) -> SubAgent:
    """Return a `SubAgent` TypedDict ready for `create_deep_agent`.

    Args:
        name: Stable identifier; used by the `task` tool to dispatch.
        description: One-sentence action-oriented summary of when to use it.
        prompt: The subagent's system prompt (free-form Markdown is fine).
        tools: Optional subset of tools available to this subagent. If
            omitted, the subagent inherits the parent agent's tool list.
        model: Optional model override (string or `BaseChatModel`). If
            omitted, inherits the parent's model.
        skills: Optional list of paths to `SKILL.md` directories to mount
            via deepagents' SkillsMiddleware.
    """
    sa: dict[str, Any] = {
        "name": name,
        "description": description,
        "system_prompt": prompt,
    }
    if tools is not None:
        sa["tools"] = tools
    if model is not None:
        sa["model"] = model
    if skills:
        sa["skills"] = skills
    return sa  # type: ignore[return-value]
