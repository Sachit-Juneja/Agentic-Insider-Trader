"""
Agent #1: User Proxy — parses the request, validates the ticker, dispatches the swarm.
"""

from typing import Any

from app.agents.base import BaseAgent


class UserProxyAgent(BaseAgent):
    name = "user_proxy"
    description = "Parses and validates the analysis request before dispatching the agent swarm."

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "").upper().strip()
        hold_period = state.get("hold_period", "3m")
        risk_tolerance = state.get("risk_tolerance", "moderate")

        # Validate ticker format
        if not ticker or len(ticker) > 10:
            raise ValueError(f"Invalid ticker: '{ticker}'")

        # Map hold periods to days for downstream agents
        period_map = {
            "1d": 1, "1w": 7, "1m": 30, "3m": 90,
            "6m": 180, "1y": 365,
        }
        hold_days = period_map.get(hold_period, 90)

        summary = (
            f"Analysis request validated: {ticker} | "
            f"Hold period: {hold_period} ({hold_days} days) | "
            f"Risk tolerance: {risk_tolerance}"
        )

        return self._make_output(
            confidence=1.0,
            signal="neutral",
            score=50.0,
            summary=summary,
            data={
                "ticker": ticker,
                "hold_period": hold_period,
                "hold_days": hold_days,
                "risk_tolerance": risk_tolerance,
            },
            key_findings=[
                f"Ticker validated: {ticker}",
                f"Analysis window: {hold_days} days",
                f"Risk profile: {risk_tolerance}",
            ],
        )
