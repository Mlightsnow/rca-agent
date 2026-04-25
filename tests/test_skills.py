from pathlib import Path

from rca_agent.skills import load_skills


def test_load_skills_reads_skill_markdown(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skills" / "demo"
    skill_dir.mkdir(parents=True)
    (skill_dir / "SKILL.md").write_text("# demo", encoding="utf-8")

    skills = load_skills(tmp_path / "skills")

    assert len(skills) == 1
    assert skills[0].name == "demo"
    assert "# demo" in skills[0].content
