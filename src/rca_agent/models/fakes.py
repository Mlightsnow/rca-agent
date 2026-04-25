"""Fake chat models for offline smoke testing.

`FakeListChatModel` from langchain-core does not implement `bind_tools`.
deepagents (and any tool-calling agent) calls `bind_tools` before
invocation, so we ship a tiny subclass that no-ops the binding.

Use this instead of `FakeListChatModel` directly whenever the agent loop
will be invoked.
"""
from __future__ import annotations

from typing import Any

from langchain_core.language_models.fake_chat_models import FakeListChatModel
from langchain_core.runnables import Runnable


class ToolCallingFakeChatModel(FakeListChatModel):
    """`FakeListChatModel` that accepts (and ignores) tool bindings."""

    def bind_tools(self, tools: Any, **_: Any) -> "Runnable":  # type: ignore[override]
        return self
