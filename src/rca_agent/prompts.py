from __future__ import annotations

from .skills import SkillDefinition

BASE_PROMPT = """\
你是一个自动根因诊断（RCA）助手。
目标：快速定位问题根因，输出可执行的验证步骤和修复建议。
约束：
1. 信息不足时先澄清。
2. 结论必须区分“已验证”与“推测”。
3. 输出结构化：现象 / 假设 / 验证 / 根因 / 修复。
"""


def compose_system_prompt(base_prompt: str, skills: list[SkillDefinition]) -> str:
    """Compose system prompt with currently loaded skills."""
    if not skills:
        return base_prompt.strip()

    rendered_skills = "\n\n".join(
        f"[Skill: {skill.name}]\n{skill.content.strip()}" for skill in skills
    )
    return f"{base_prompt.strip()}\n\n可用技能:\n{rendered_skills}".strip()
