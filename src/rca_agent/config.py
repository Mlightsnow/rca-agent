from dataclasses import dataclass, field
from pathlib import Path


@dataclass(slots=True)
class AgentRuntimeConfig:
    """Runtime knobs for building and running the RCA MVP agent."""

    model: str = "openai:gpt-4o-mini"
    system_prompt: str = "You are an RCA (Root Cause Analysis) assistant."
    skills_dir: Path = Path("skills")
    enable_planning: bool = True
    metadata: dict[str, str] = field(default_factory=dict)
