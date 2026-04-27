"""Model factory.

Resolves a model spec (string or pre-built `BaseChatModel`) to a concrete
LangChain chat model. The default provider is ``litellm`` — a self-hosted
LiteLLM proxy that exposes an OpenAI-compatible REST endpoint, so we
integrate via ``langchain_openai.ChatOpenAI`` pointed at the proxy URL.

This is the *only* module that knows about provider strings. Callers pass
in a string + provider; everything else stays provider-agnostic.
"""
from __future__ import annotations

from typing import Any

from langchain_core.language_models.chat_models import BaseChatModel

from rca_agent.models.fakes import ToolCallingFakeChatModel


def get_model(
    spec: str | BaseChatModel | None = None,
    provider: str | None = None,
    *,
    base_url: str | None = None,
    api_key: str | None = None,
    temperature: float | None = None,
    **extra: Any,
) -> BaseChatModel:
    """Resolve a model spec to a `BaseChatModel`.

    Args:
        spec: Either a model name (string) or a pre-built `BaseChatModel`.
        provider: One of ``litellm`` (default), ``fake``, ``anthropic``,
            ``openai``. ``litellm`` routes through a self-hosted proxy.
        base_url: For ``litellm``, the proxy URL.
        api_key: For ``litellm``, the proxy API key.
        temperature: Sampling temperature.
        **extra: Forwarded to the underlying model constructor.

    Returns:
        A `BaseChatModel` ready to be passed to deepagents.
    """
    if isinstance(spec, BaseChatModel):
        return spec

    provider = (provider or "litellm").lower()

    if provider == "fake":
        # FakeListChatModel needs at least one canned response. The agent
        # loop test injects its own; this default is only used when callers
        # request the fake provider without supplying responses. We use the
        # tool-aware variant so deepagents' bind_tools() call doesn't blow
        # up the loop.
        responses = extra.pop("responses", ["[fake] ok"])
        return ToolCallingFakeChatModel(responses=responses)

    if provider == "litellm":
        if not isinstance(spec, str) or not spec:
            raise ValueError(
                "Provider 'litellm' requires a model name (string) as `spec`."
            )
        # LiteLLM exposes an OpenAI-compatible API; ChatOpenAI is the cleanest
        # LangChain integration. base_url + api_key point at the proxy.
        from langchain_openai import ChatOpenAI

        kwargs: dict[str, Any] = {"model": spec}
        if base_url is not None:
            kwargs["base_url"] = base_url
        if api_key is not None:
            kwargs["api_key"] = api_key
        if temperature is not None:
            kwargs["temperature"] = temperature
        kwargs.update(extra)
        return ChatOpenAI(**kwargs)

    if provider in {"anthropic", "openai"}:
        if not isinstance(spec, str) or not spec:
            raise ValueError(
                f"Provider '{provider}' requires a model name (string) as `spec`."
            )
        from langchain.chat_models import init_chat_model

        kwargs = dict(extra)
        if temperature is not None:
            kwargs["temperature"] = temperature
        return init_chat_model(spec, model_provider=provider, **kwargs)

    raise ValueError(f"Unknown provider: {provider!r}")
