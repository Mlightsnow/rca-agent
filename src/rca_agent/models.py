from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class ModelSpec:
    """Abstraction for future model-provider customization."""

    name: str


def resolve_model(model_name: str) -> ModelSpec:
    """Resolve model config.

    For MVP, this returns only model name. Later versions can inject
    provider-specific clients or auth strategies.
    """
    return ModelSpec(name=model_name)
