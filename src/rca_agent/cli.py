from __future__ import annotations

from .agent import build_rca_agent
from .config import AgentRuntimeConfig


def main() -> None:
    """Local-only CLI loop (no sandbox/container for MVP)."""
    config = AgentRuntimeConfig()
    agent = build_rca_agent(config)

    print("RCA Agent MVP started. Type 'exit' to quit.")
    while True:
        user_input = input("\n> ").strip()
        if user_input.lower() in {"exit", "quit"}:
            print("bye")
            break

        result = agent.invoke(
            {"messages": [{"role": "user", "content": user_input}]}
        )
        print(result)


if __name__ == "__main__":
    main()
