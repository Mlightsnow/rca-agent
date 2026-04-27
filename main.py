"""Entry point: `python main.py "incident description"`.

Keeps the CLI deliberately thin — argparse, build the agent, invoke it
once, print the final assistant message. All real wiring lives in
`rca_agent.agent.build_agent`.
"""
from __future__ import annotations

import argparse
import sys

from langchain_core.messages import AIMessage


def _final_text(messages: list) -> str:
    for msg in reversed(messages):
        if isinstance(msg, AIMessage) and msg.content:
            return msg.content if isinstance(msg.content, str) else str(msg.content)
    return ""


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="rca-agent",
        description="Run the RCA auto-diagnosis agent on a single incident.",
    )
    parser.add_argument("incident", help="Free-form incident description")
    args = parser.parse_args(argv)

    # Late import: avoids loading deepagents (and its model client) for `--help`.
    from rca_agent import build_agent

    agent = build_agent()
    result = agent.invoke(
        {"messages": [{"role": "user", "content": args.incident}]}
    )
    print(_final_text(result["messages"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
