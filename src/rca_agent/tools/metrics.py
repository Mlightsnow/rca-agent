"""Metric query tool (stub)."""
from __future__ import annotations

from typing import Any

from rca_agent.tools.base import rca_tool, stub_response


@rca_tool
def query_metrics(promql: str, range: str = "15m") -> dict[str, Any]:
    """Run a PromQL-style query against the metrics backend.

    Args:
        promql: The PromQL expression.
        range: Lookback window (e.g. "15m", "1h"). Default 15m.

    Returns:
        Structured time-series payload. Currently a stub.
    """
    return stub_response("query_metrics", promql=promql, range=range)
