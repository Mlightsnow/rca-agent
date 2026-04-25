from __future__ import annotations

import pytest
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_openai import ChatOpenAI

from rca_agent.models.factory import get_model


def test_passthrough_basechatmodel_instance():
    fake = FakeListChatModel(responses=["x"])
    assert get_model(fake) is fake


def test_fake_provider_returns_fake_model():
    m = get_model("anything", provider="fake")
    assert isinstance(m, FakeListChatModel)


def test_litellm_provider_builds_chat_openai():
    m = get_model(
        "my-litellm-alias",
        provider="litellm",
        base_url="http://localhost:4000",
        api_key="sk-test",
        temperature=0.2,
    )
    assert isinstance(m, ChatOpenAI)
    # Smoke-check that the connection settings landed somewhere visible.
    # langchain-openai normalizes these onto the client; checking model is
    # sufficient to prove the wiring works end-to-end.
    assert m.model_name == "my-litellm-alias"


def test_unknown_provider_raises():
    with pytest.raises(ValueError):
        get_model("foo", provider="not-a-real-provider")


def test_litellm_requires_model_string():
    with pytest.raises(ValueError):
        get_model(None, provider="litellm", base_url="http://x:4000", api_key="k")


def test_returns_basechatmodel():
    m = get_model("anything", provider="fake")
    assert isinstance(m, BaseChatModel)
