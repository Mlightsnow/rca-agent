from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class SkillDefinition:
    name: str
    content: str


def load_skills(skills_dir: Path) -> list[SkillDefinition]:
    """Load markdown skills from local directory.

    Expected layout:
      skills/<skill_name>/SKILL.md
    """
    if not skills_dir.exists():
        return []

    skills: list[SkillDefinition] = []
    for skill_file in sorted(skills_dir.glob("*/SKILL.md")):
        skills.append(
            SkillDefinition(
                name=skill_file.parent.name,
                content=skill_file.read_text(encoding="utf-8"),
            )
        )
    return skills
