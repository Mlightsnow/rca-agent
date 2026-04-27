"""Shell command tool (stub).

Real implementation will call `subprocess.run` on the host (no sandbox in
this MVP). For now it returns the canonical stub payload so the agent can
reason about the missing capability.
"""
from __future__ import annotations

from typing import Any

from rca_agent.tools.base import rca_tool, stub_response


@rca_tool
def run_shell(cmd: str, timeout: int = 30) -> dict[str, Any]:
    """Run a read-only diagnostic shell command on the host.

    Args:
        cmd: The shell command to execute.
        timeout: Hard timeout in seconds (default 30).

    Returns:
        Structured result with stdout/stderr/return_code. Currently a stub.
    """
    return stub_response("run_shell", cmd=cmd, timeout=timeout)
