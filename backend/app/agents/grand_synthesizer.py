"""
Agent #14: Grand Synthesizer — resolves conflicts, outputs final score (0-100), Buy/Sell/Hold.
"""

import random
from typing import Any

from app.agents.base import BaseAgent


# Agent weights for final scoring
AGENT_WEIGHTS = {
    "technical_analyst": 0.15,
    "fundamental_agent": 0.15,
    "insider_trading_agent": 0.12,
    "options_flow_agent": 0.10,
    "dark_pool_monitor": 0.08,
    "macro_agent": 0.08,
    "market_regime_agent": 0.08,
    "sector_comparator": 0.06,
    "media_sentiment_agent": 0.06,
    "social_scraper": 0.04,
    "geopolitical_agent": 0.05,
    "risk_optimization_agent": 0.03,
}


class GrandSynthesizerAgent(BaseAgent):
    name = "grand_synthesizer"
    description = "The judge. Resolves conflicts, outputs final 0-100 score and Buy/Sell/Hold rating."

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")
        agent_outputs = state.get("agent_outputs", {})

        # Weighted score calculation
        weighted_score = 0.0
        total_weight = 0.0
        agent_scores = {}
        conflicts = []
        signals_list = []

        for agent_name, weight in AGENT_WEIGHTS.items():
            output = agent_outputs.get(agent_name, {})
            if isinstance(output, dict) and "score" in output:
                score = output["score"]
                signal = output.get("signal", "neutral")
                confidence = output.get("confidence", 0.5)

                effective_weight = weight * confidence
                weighted_score += score * effective_weight
                total_weight += effective_weight
                agent_scores[agent_name] = {"score": score, "signal": signal, "weight": weight, "confidence": confidence}
                signals_list.append(signal)

        final_score = round(weighted_score / max(total_weight, 0.01), 1)
        final_score = max(0, min(100, final_score))

        # Detect conflicts
        bullish_agents = [n for n, s in agent_scores.items() if s["signal"] == "bullish"]
        bearish_agents = [n for n, s in agent_scores.items() if s["signal"] == "bearish"]
        if bullish_agents and bearish_agents:
            conflicts.append(f"Conflict: {len(bullish_agents)} bullish vs {len(bearish_agents)} bearish agents")

        # Determine rating
        if final_score >= 75:
            rating = "STRONG BUY"
        elif final_score >= 60:
            rating = "BUY"
        elif final_score >= 40:
            rating = "HOLD"
        elif final_score >= 25:
            rating = "SELL"
        else:
            rating = "STRONG SELL"

        avg_confidence = sum(s.get("confidence", 0.5) for s in agent_scores.values()) / max(len(agent_scores), 1)

        # LLM synthesis
        llm_summary = self._llm_call(
            system_prompt="You are the Grand Synthesizer AI. Give a 3-4 sentence executive summary synthesizing all agent findings into a coherent investment thesis.",
            user_prompt=(
                f"Ticker: {ticker} | Final Score: {final_score}/100 | Rating: {rating}\n"
                f"Bullish agents ({len(bullish_agents)}): {', '.join(bullish_agents[:5])}\n"
                f"Bearish agents ({len(bearish_agents)}): {', '.join(bearish_agents[:5])}\n"
                f"Conflicts: {'; '.join(conflicts) if conflicts else 'None'}\n"
                f"Hold period: {state.get('hold_period', '3m')}"
            ),
        )

        return {
            "agent_outputs": {
                self.name: {
                    "agent_name": self.name,
                    "confidence": round(avg_confidence, 2),
                    "signal": "bullish" if final_score >= 60 else "bearish" if final_score < 40 else "neutral",
                    "score": final_score,
                    "summary": llm_summary,
                    "data": {"agent_scores": agent_scores, "conflicts": conflicts},
                    "key_findings": [
                        f"Final Score: {final_score}/100",
                        f"Rating: {rating}",
                        f"Consensus: {len(bullish_agents)} bullish / {len(bearish_agents)} bearish",
                        f"Confidence: {avg_confidence:.0%}",
                    ],
                }
            },
            "final_score": final_score,
            "final_rating": rating,
            "final_summary": llm_summary,
        }
