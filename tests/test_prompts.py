from __future__ import annotations

import pytest

from rca_agent.prompts import load_prompt


def test_loads_top_level_system_prompt():
    text = load_prompt("system")
    assert text.strip(), "system prompt must be non-empty"
    # Sanity-check that it contains some RCA-flavored content.
    assert "Root Cause Analysis" in text or "RCA" in text


@pytest.mark.parametrize(
    "name",
    ["subagents/log_analyzer", "subagents/metric_analyzer", "subagents/hypothesis_validator"],
)
def test_loads_subagent_prompts(name: str):
    text = load_prompt(name)
    assert text.strip()


def test_missing_prompt_raises():
    with pytest.raises(FileNotFoundError):
        load_prompt("does_not_exist")
