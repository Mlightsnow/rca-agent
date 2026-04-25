from __future__ import annotations

import pytest

from rca_agent.config import ConfigError, Settings, get_settings


def test_defaults(monkeypatch):
    # Wipe any inherited env so we test pure defaults.
    for k in ("RCA_PROVIDER", "RCA_MODEL", "RCA_MODEL_BASE_URL",
              "RCA_MODEL_API_KEY", "RCA_MODEL_TEMPERATURE", "RCA_LOG_LEVEL"):
        monkeypatch.delenv(k, raising=False)

    s = Settings()
    assert s.provider == "litellm"
    assert s.model is None
    assert s.model_base_url is None
    assert s.model_api_key is None
    assert s.model_temperature == 0.0
    assert s.log_level == "INFO"


def test_env_overrides(monkeypatch):
    monkeypatch.setenv("RCA_PROVIDER", "fake")
    monkeypatch.setenv("RCA_MODEL", "fake-model")
    monkeypatch.setenv("RCA_MODEL_BASE_URL", "http://x:4000")
    monkeypatch.setenv("RCA_MODEL_API_KEY", "secret")
    monkeypatch.setenv("RCA_MODEL_TEMPERATURE", "0.3")
    monkeypatch.setenv("RCA_LOG_LEVEL", "DEBUG")

    s = Settings()
    assert s.provider == "fake"
    assert s.model == "fake-model"
    assert s.model_base_url == "http://x:4000"
    assert s.model_api_key == "secret"
    assert s.model_temperature == pytest.approx(0.3)
    assert s.log_level == "DEBUG"


def test_get_settings_is_cached(env_fake):
    a = get_settings()
    b = get_settings()
    assert a is b


def test_require_for_litellm_validates(monkeypatch):
    monkeypatch.setenv("RCA_PROVIDER", "litellm")
    monkeypatch.delenv("RCA_MODEL", raising=False)
    monkeypatch.delenv("RCA_MODEL_BASE_URL", raising=False)
    s = Settings()
    with pytest.raises(ConfigError):
        s.require_for_runtime()


def test_require_for_litellm_passes(monkeypatch):
    monkeypatch.setenv("RCA_PROVIDER", "litellm")
    monkeypatch.setenv("RCA_MODEL", "gpt-4o")
    monkeypatch.setenv("RCA_MODEL_BASE_URL", "http://localhost:4000")
    s = Settings()
    s.require_for_runtime()  # should not raise


def test_require_for_fake_does_not_need_model(monkeypatch):
    monkeypatch.setenv("RCA_PROVIDER", "fake")
    monkeypatch.delenv("RCA_MODEL", raising=False)
    s = Settings()
    s.require_for_runtime()  # fake provider needs nothing
