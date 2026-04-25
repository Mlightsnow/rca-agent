---
name: example_skill
description: |
  Placeholder skill pack. Demonstrates the SKILL.md integration seam for
  deepagents' SkillsMiddleware. Replace this with a real diagnostic
  checklist (e.g. "noisy-neighbor triage", "OOM triage").
---

# Example skill (placeholder)

This pack is intentionally empty. It exists so the
`hypothesis_validator` subagent has a `skills=[...]` reference to wire up,
proving the integration works end-to-end.

When you author a real skill pack here, put:

- a short, action-oriented title and description in the YAML frontmatter,
- a numbered checklist of diagnostic steps in the body,
- any helper files (queries, scripts) alongside this `SKILL.md`.
