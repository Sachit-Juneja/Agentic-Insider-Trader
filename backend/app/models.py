"""
Pydantic models for the API and agent swarm state.
"""

from __future__ import annotations

import operator
from enum import Enum
from typing import Annotated, Any, Optional
from pydantic import BaseModel, Field
from typing_extensions import TypedDict


# ─── API Request/Response Models ──────────────────────────────────────────────


class RiskTolerance(str, Enum):
    CONSERVATIVE = "conservative"
    MODERATE = "moderate"
    AGGRESSIVE = "aggressive"
    YOLO = "yolo"


class AnalysisRequest(BaseModel):
    """Incoming analysis request from the frontend."""
    ticker: str = Field(..., description="Stock ticker symbol (e.g., AAPL)", max_length=10)
    hold_period: str = Field(default="3m", description="Holding period: 1d, 1w, 1m, 3m, 6m, 1y")
    risk_tolerance: RiskTolerance = Field(default=RiskTolerance.MODERATE)


class AgentStatusEnum(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETE = "complete"
    ERROR = "error"


class AgentStatus(BaseModel):
    """Status of an individual agent during execution."""
    agent_name: str
    status: AgentStatusEnum = AgentStatusEnum.PENDING
    summary: str = ""
    confidence: float = 0.0
    execution_time_ms: float = 0.0


class FinalRating(str, Enum):
    STRONG_BUY = "STRONG BUY"
    BUY = "BUY"
    HOLD = "HOLD"
    SELL = "SELL"
    STRONG_SELL = "STRONG SELL"


class AnalysisReport(BaseModel):
    """Final synthesized analysis report."""
    ticker: str
    hold_period: str
    final_score: float = Field(ge=0, le=100)
    rating: FinalRating
    confidence: float = Field(ge=0, le=1)
    summary: str
    agent_results: dict[str, Any] = {}
    risk_metrics: dict[str, Any] = {}
    chart_data: dict[str, Any] = {}
    timestamp: str = ""


# ─── Agent Output Models ─────────────────────────────────────────────────────


class AgentOutput(BaseModel):
    """Standardized output from any agent."""
    agent_name: str
    confidence: float = Field(ge=0, le=1, default=0.5)
    signal: str = "neutral"  # bullish, bearish, neutral
    score: float = Field(ge=0, le=100, default=50.0)
    summary: str = ""
    data: dict[str, Any] = {}
    key_findings: list[str] = []


# ─── LangGraph Swarm State ───────────────────────────────────────────────────


def merge_agent_outputs(left: dict, right: dict) -> dict:
    """Reducer to merge agent outputs into a single dict."""
    merged = left.copy()
    merged.update(right)
    return merged


class SwarmState(TypedDict):
    """The shared state object passed through the LangGraph pipeline."""
    # Input
    ticker: str
    hold_period: str
    risk_tolerance: str

    # Agent outputs — merged via reducer
    agent_outputs: Annotated[dict[str, Any], merge_agent_outputs]

    # Agent status tracking for SSE streaming
    agent_statuses: Annotated[list[dict], operator.add]

    # Synthesis
    final_score: float
    final_rating: str
    final_summary: str

    # Report
    report: dict[str, Any]

    # Metadata
    errors: Annotated[list[str], operator.add]
