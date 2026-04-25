"""RCA auto-diagnosis agent."""

__all__ = ["build_agent"]


def __getattr__(name: str):
    # Lazy import so test modules can import sub-packages (e.g. rca_agent.config)
    # without forcing the whole agent stack (and deepagents) to load.
    if name == "build_agent":
        from rca_agent.agent import build_agent

        return build_agent
    raise AttributeError(f"module 'rca_agent' has no attribute {name!r}")
