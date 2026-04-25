from pathlib import Path

from rca_agent.agent import build_rca_agent
from rca_agent.config import AgentRuntimeConfig


def test_build_rca_agent_wires_model_tools_and_prompt(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills" / "sample"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("sample skill", encoding="utf-8")

    captured = {}

    def fake_factory(**kwargs):
        captured.update(kwargs)
        return {"ok": True}

    config = AgentRuntimeConfig(model="openai:gpt-4o", skills_dir=tmp_path / "skills")
    agent = build_rca_agent(config, factory=fake_factory)

    assert agent == {"ok": True}
    assert captured["model"] == "openai:gpt-4o"
    assert captured["tools"] == []
    assert "sample skill" in captured["system_prompt"]
