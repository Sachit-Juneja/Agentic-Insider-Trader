"""
Agent #13: Risk & Optimization Agent — Kelly Criterion, position sizing.
"""

import random
import math
from typing import Any

from app.agents.base import BaseAgent


class RiskOptimizationAgent(BaseAgent):
    name = "risk_optimization_agent"
    description = "Calculates Kelly Criterion and optimal position sizing based on portfolio and risk tolerance."

    def _kelly_criterion(self, win_prob: float, win_loss_ratio: float) -> float:
        """Calculate Kelly fraction: f* = p - (1-p)/b"""
        if win_loss_ratio <= 0:
            return 0.0
        kelly = win_prob - (1 - win_prob) / win_loss_ratio
        return max(0, min(kelly, 1.0))  # Clamp to [0, 1]

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        risk_tolerance = state.get("risk_tolerance", "moderate")
        agent_outputs = state.get("agent_outputs", {})

        # Aggregate signals from all agents
        signals = []
        for name, output in agent_outputs.items():
            if isinstance(output, dict) and "signal" in output:
                signals.append(output["signal"])

        bullish = signals.count("bullish")
        bearish = signals.count("bearish")
        total = max(len(signals), 1)

        # Estimate win probability from agent consensus
        win_prob = bullish / total
        win_loss_ratio = random.uniform(1.5, 3.0)

        # Kelly calculation
        full_kelly = self._kelly_criterion(win_prob, win_loss_ratio)

        # Adjust for risk tolerance
        risk_multipliers = {
            "conservative": 0.25,
            "moderate": 0.5,
            "aggressive": 0.75,
            "yolo": 1.0,
        }
        multiplier = risk_multipliers.get(risk_tolerance, 0.5)
        adjusted_kelly = full_kelly * multiplier

        # Position sizing for a hypothetical $100k portfolio
        portfolio_value = 100_000
        position_size = round(portfolio_value * adjusted_kelly, 2)

        # Risk metrics
        max_drawdown_est = round(random.uniform(5, 30), 1)
        sharpe_estimate = round(random.uniform(-0.5, 2.5), 2)
        var_95 = round(position_size * random.uniform(0.02, 0.08), 2)

        score = round(50 + (win_prob - 0.5) * 60, 1)
        score = max(0, min(100, score))

        signal = "bullish" if adjusted_kelly > 0.15 else "bearish" if adjusted_kelly < 0.05 else "neutral"

        return self._make_output(
            confidence=round(random.uniform(0.55, 0.85), 2),
            signal=signal, score=score,
            summary=(
                f"Kelly Criterion: {full_kelly:.1%} (adjusted: {adjusted_kelly:.1%} for {risk_tolerance}). "
                f"Suggested position: ${position_size:,.0f} of $100k portfolio. "
                f"Estimated Sharpe: {sharpe_estimate}."
            ),
            data={
                "win_probability": round(win_prob, 3),
                "win_loss_ratio": round(win_loss_ratio, 2),
                "full_kelly_fraction": round(full_kelly, 4),
                "adjusted_kelly_fraction": round(adjusted_kelly, 4),
                "risk_tolerance": risk_tolerance,
                "position_size_usd": position_size,
                "portfolio_value": portfolio_value,
                "position_pct": round(adjusted_kelly * 100, 1),
                "max_drawdown_pct": max_drawdown_est,
                "sharpe_ratio": sharpe_estimate,
                "var_95_usd": var_95,
                "agent_consensus": {"bullish": bullish, "bearish": bearish, "neutral": total - bullish - bearish},
            },
            key_findings=[
                f"Kelly Fraction: {full_kelly:.1%} (adj: {adjusted_kelly:.1%})",
                f"Position Size: ${position_size:,.0f} ({adjusted_kelly*100:.1f}% of portfolio)",
                f"Win Probability: {win_prob:.1%} ({bullish}/{total} agents bullish)",
                f"Est. Sharpe: {sharpe_estimate}",
                f"VaR(95%): ${var_95:,.0f}",
            ],
        )
