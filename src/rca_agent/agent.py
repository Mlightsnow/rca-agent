"""Agent assembly — the only file that imports `deepagents`.

`build_agent()` composes prompt + tools + model + subagents + skill packs
into a compiled deepagents graph. Callers can override anything via the
`extra_*` hooks; production deployments inject real tool implementations
through `extra_tools` instead of editing the registry.
"""
from __future__ import annotations

from typing import Any

from deepagents import SubAgent, create_deep_agent
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.tools import BaseTool

from rca_agent.config import get_settings
from rca_agent.models import get_model
from rca_agent.prompts import load_prompt
from rca_agent.skills import all_skill_paths
from rca_agent.subagents import ALL_SUBAGENTS
from rca_agent.tools import ALL_TOOLS


def build_agent(
    *,
    model: str | BaseChatModel | None = None,
    extra_tools: list[BaseTool] | None = None,
    extra_subagents: list[SubAgent] | None = None,
    extra_skills: list[str] | None = None,
    system_prompt: str | None = None,
) -> Any:
    """Build the RCA deep agent.

    Args:
        model: Override for the chat model. Accepts either a string spec
            (forwarded to `get_model`) or a pre-built `BaseChatModel`.
        extra_tools: Additional tools appended to `ALL_TOOLS`.
        extra_subagents: Additional subagents appended to `ALL_SUBAGENTS`.
        extra_skills: Additional SKILL.md directory paths appended to the
            top-level skill list (in addition to packs auto-discovered
            under `rca_agent/skills/`).
        system_prompt: Override for the top-level system prompt; default
            loads `prompts/system.md`.

    Returns:
        A compiled deepagents/LangGraph object — call `.invoke({"messages":
        [...]})` (or `.stream`, `.ainvoke`, `.astream`) to run the loop.
    """
    settings = get_settings()
    settings.require_for_runtime()

    if isinstance(model, BaseChatModel):
        resolved_model: BaseChatModel = model
    else:
        resolved_model = get_model(
            model or settings.model,
            settings.provider,
            base_url=settings.model_base_url,
            api_key=settings.model_api_key,
            temperature=settings.model_temperature,
        )

    tools: list[BaseTool] = list(ALL_TOOLS) + list(extra_tools or [])
    subagents: list[SubAgent] = list(ALL_SUBAGENTS) + list(extra_subagents or [])
    skills: list[str] = all_skill_paths() + list(extra_skills or [])

    return create_deep_agent(
        model=resolved_model,
        tools=tools,
        system_prompt=system_prompt or load_prompt("system"),
        subagents=subagents,
        skills=skills,
    )
