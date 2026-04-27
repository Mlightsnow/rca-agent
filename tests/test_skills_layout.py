from __future__ import annotations

from pathlib import Path

import pytest

from rca_agent.skills import all_skill_paths, skill_path


def test_example_skill_resolvable():
    p = Path(skill_path("example_skill"))
    assert p.is_dir()
    assert (p / "SKILL.md").is_file()


def test_skill_md_has_frontmatter_and_body():
    text = (Path(skill_path("example_skill")) / "SKILL.md").read_text()
    # YAML frontmatter delimited by ---
    assert text.lstrip().startswith("---"), "SKILL.md should start with YAML frontmatter"
    parts = text.split("---", 2)
    assert len(parts) >= 3, "SKILL.md needs frontmatter delimiters"
    frontmatter, body = parts[1], parts[2]
    assert "name:" in frontmatter
    assert "description:" in frontmatter
    assert body.strip(), "SKILL.md body must be non-empty"


def test_all_skill_paths_includes_example():
    paths = all_skill_paths()
    assert any(p.endswith("example_skill") for p in paths)


def test_missing_skill_raises():
    with pytest.raises(FileNotFoundError):
        skill_path("nope_does_not_exist")
