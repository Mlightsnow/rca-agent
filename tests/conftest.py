"""Shared pytest fixtures.

Tests run fully offline. The default model is a tool-aware fake derived
from `FakeListChatModel` — it yields canned responses without touching any
network or API key, and accepts `bind_tools(...)` so it can be used inside
the deepagents loop (which always binds tools to the model).
"""
from __future__ import annotations

import pytest

from rca_agent.models.fakes import ToolCallingFakeChatModel


@pytest.fixture
def fake_model() -> ToolCallingFakeChatModel:
    """A tool-aware fake with one canned reply."""
    return ToolCallingFakeChatModel(responses=["Acknowledged. Investigating."])


@pytest.fixture(autouse=True)
def _isolate_settings_cache(monkeypatch):
    """Ensure each test sees a fresh Settings object.

    `get_settings()` is lru_cached; without resetting it, env-var changes in
    one test would leak into another.
    """
    from rca_agent import config

    config.get_settings.cache_clear()
    yield
    config.get_settings.cache_clear()


@pytest.fixture
def env_fake(monkeypatch):
    """Set the env to use the fake provider with a placeholder model."""
    monkeypatch.setenv("RCA_PROVIDER", "fake")
    monkeypatch.setenv("RCA_MODEL", "fake-model")
    monkeypatch.delenv("RCA_MODEL_BASE_URL", raising=False)
    monkeypatch.delenv("RCA_MODEL_API_KEY", raising=False)
    return monkeypatch
