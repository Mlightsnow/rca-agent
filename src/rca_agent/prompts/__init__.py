"""Markdown prompt loader.

Prompts live as `.md` files alongside this package and are loaded via
`importlib.resources` so they ship correctly inside an installed wheel.

Usage:

    from rca_agent.prompts import load_prompt
    text = load_prompt("system")
    text = load_prompt("subagents/log_analyzer")
"""
from __future__ import annotations

from importlib.resources import files

_PROMPT_ROOT = files(__package__)


def load_prompt(name: str) -> str:
    """Load a prompt by relative name (without `.md` extension).

    Raises FileNotFoundError if the prompt does not exist.
    """
    rel = f"{name}.md"
    target = _PROMPT_ROOT.joinpath(rel)
    if not target.is_file():
        raise FileNotFoundError(f"Prompt not found: {rel}")
    return target.read_text(encoding="utf-8")
