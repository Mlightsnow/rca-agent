"""Runtime configuration for rca-agent.

All settings are read from the process environment (or a `.env` file).
A single `get_settings()` accessor returns the cached `Settings` instance.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

Provider = Literal["litellm", "fake", "anthropic", "openai"]


class ConfigError(RuntimeError):
    """Raised when required runtime configuration is missing."""


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="RCA_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    provider: Provider = "litellm"
    model: str | None = None
    model_base_url: str | None = None
    model_api_key: str | None = None
    model_temperature: float = 0.0
    log_level: str = "INFO"

    def require_for_runtime(self) -> None:
        """Validate that the settings are sufficient to actually build an agent.

        We don't validate at construction time because tests and tooling may
        construct partial settings; we validate at the seam where it matters.
        """
        if self.provider == "fake":
            return
        if self.provider == "litellm":
            missing = [
                name
                for name, val in (
                    ("RCA_MODEL", self.model),
                    ("RCA_MODEL_BASE_URL", self.model_base_url),
                )
                if not val
            ]
            if missing:
                raise ConfigError(
                    f"Provider 'litellm' requires {', '.join(missing)} to be set."
                )
            return
        # anthropic / openai: just need a model name.
        if not self.model:
            raise ConfigError(
                f"Provider '{self.provider}' requires RCA_MODEL to be set."
            )


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
