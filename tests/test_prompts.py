from rca_agent.prompts import compose_system_prompt
from rca_agent.skills import SkillDefinition


def test_compose_system_prompt_with_skills() -> None:
    prompt = compose_system_prompt(
        "base",
        [SkillDefinition(name="x", content="do x")],
    )

    assert "base" in prompt
    assert "Skill: x" in prompt
    assert "do x" in prompt
