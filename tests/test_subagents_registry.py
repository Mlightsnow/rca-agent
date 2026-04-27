from __future__ import annotations

from rca_agent.subagents import ALL_SUBAGENTS
from rca_agent.subagents.registry import REQUIRED_KEYS
from rca_agent.tools import ALL_TOOLS


def test_registry_non_empty():
    assert len(ALL_SUBAGENTS) >= 3


def test_each_subagent_has_required_keys():
    for sa in ALL_SUBAGENTS:
        for key in REQUIRED_KEYS:
            assert key in sa, f"subagent missing {key}: {sa}"
            assert sa[key], f"subagent has empty {key}: {sa}"


def test_subagent_names_unique():
    names = [sa["name"] for sa in ALL_SUBAGENTS]
    assert len(names) == len(set(names))


def test_expected_subagents_present():
    names = {sa["name"] for sa in ALL_SUBAGENTS}
    assert {"log_analyzer", "metric_analyzer", "hypothesis_validator"} <= names


def test_subagent_tools_resolve_to_real_tools():
    valid_names = {t.name for t in ALL_TOOLS}
    for sa in ALL_SUBAGENTS:
        for tool in sa.get("tools", []):
            # Tools may be either a BaseTool instance or a callable; both
            # carry a .name attribute via @tool / @rca_tool.
            assert getattr(tool, "name", None) in valid_names, (
                f"subagent {sa['name']!r} references unknown tool {tool!r}"
            )


def test_hypothesis_validator_wires_skill_pack():
    by_name = {sa["name"]: sa for sa in ALL_SUBAGENTS}
    sa = by_name["hypothesis_validator"]
    skills = sa.get("skills") or []
    assert len(skills) >= 1, "hypothesis_validator should reference at least one SKILL.md pack"
