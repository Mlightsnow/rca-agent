"""SKILL.md packs for deepagents' SkillsMiddleware.

Skills are *directories* containing a `SKILL.md` file (plus optional
helpers). deepagents discovers them at runtime via filesystem paths, so we
expose a small helper to resolve a pack name to an absolute path that
works from an installed wheel just as well as from a checkout.
"""
from __future__ import annotations

from importlib.resources import as_file, files
from pathlib import Path

_SKILLS_ROOT = files(__package__)


def skill_path(name: str) -> str:
    """Return the absolute filesystem path of a SKILL.md pack directory."""
    pack = _SKILLS_ROOT.joinpath(name)
    if not pack.is_dir():
        raise FileNotFoundError(f"Skill pack not found: {name}")
    # `as_file` materializes a Traversable to a concrete filesystem path
    # (a no-op for an editable install / checkout, copies into a temp dir
    # for zipped wheels). We use the context only to obtain the path; the
    # underlying files persist for the duration of the package import.
    with as_file(pack) as p:
        return str(Path(p).resolve())


def all_skill_paths() -> list[str]:
    """Return absolute paths for every SKILL.md pack in this directory."""
    out: list[str] = []
    for entry in _SKILLS_ROOT.iterdir():
        if entry.is_dir() and entry.joinpath("SKILL.md").is_file():
            out.append(skill_path(entry.name))
    return out


__all__ = ["skill_path", "all_skill_paths"]
