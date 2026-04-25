from __future__ import annotations

from typing import Any, Callable

from .config import AgentRuntimeConfig
from .models import resolve_model
from .prompts import BASE_PROMPT, compose_system_prompt
from .skills import load_skills
from .tools import build_toolset

DeepAgentFactory = Callable[..., Any]


def _default_factory(**kwargs: Any) -> Any:
    from deepagents import create_deep_agent

    return create_deep_agent(**kwargs)


def build_rca_agent(
    config: AgentRuntimeConfig,
    factory: DeepAgentFactory | None = None,
) -> Any:
    """Build a deepagents-powered RCA agent loop with custom extension points."""
    model_spec = resolve_model(config.model)
    skills = load_skills(config.skills_dir)
    system_prompt = compose_system_prompt(config.system_prompt or BASE_PROMPT, skills)

    creator = factory or _default_factory
    return creator(
        model=model_spec.name,
        tools=build_toolset(),
        system_prompt=system_prompt,
    )
