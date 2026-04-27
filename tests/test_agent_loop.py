"""Smoke test for the full agent loop.

Proves that custom prompt + custom tools + custom model + custom subagents
all wire into deepagents successfully and the resulting graph can be
invoked with a user message and produce a final assistant message.

Uses `FakeListChatModel` so it runs offline without any API key.
"""
from __future__ import annotations

import pytest
from langchain_core.messages import AIMessage

from rca_agent import build_agent
from rca_agent.models.fakes import ToolCallingFakeChatModel


@pytest.fixture
def fake_loop_model() -> ToolCallingFakeChatModel:
    # FakeListChatModel cycles its responses; supplying a few covers the
    # scenario where the graph asks the model more than once before stopping.
    return ToolCallingFakeChatModel(
        responses=[
            "I will investigate. Tentative root cause: unknown — tools are stubs.",
            "Final answer: insufficient data; tools returned stub responses.",
            "ok",
        ]
    )


def test_build_agent_returns_invocable_graph(fake_loop_model, env_fake):
    agent = build_agent(model=fake_loop_model)
    # deepagents returns a CompiledStateGraph. Don't assert the exact type —
    # just that it has the LangGraph-style invocation surface.
    assert hasattr(agent, "invoke"), "agent must expose .invoke"
    assert hasattr(agent, "stream"), "agent must expose .stream"


def test_agent_loop_produces_final_message(fake_loop_model, env_fake):
    agent = build_agent(model=fake_loop_model)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "Service X 5xx spike at 10:00"}]}
    )
    msgs = result["messages"]
    assert msgs, "agent returned no messages"
    # The trailing message is the assistant's final answer.
    last = msgs[-1]
    assert isinstance(last, AIMessage), f"last message not AIMessage: {type(last)}"
    assert last.content, "final assistant message has empty content"


def test_agent_user_input_is_preserved(fake_loop_model, env_fake):
    agent = build_agent(model=fake_loop_model)
    result = agent.invoke(
        {"messages": [{"role": "user", "content": "hello world"}]}
    )
    # Find the user message in the trace.
    user_contents = [
        m.content
        for m in result["messages"]
        if getattr(m, "type", None) == "human"
    ]
    assert "hello world" in user_contents
