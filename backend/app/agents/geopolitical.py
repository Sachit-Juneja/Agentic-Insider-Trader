"""
Agent #3: Geopolitical Risk Agent — scans for global events, tariffs, supply chain shocks.
"""

import random
from typing import Any

from app.agents.base import BaseAgent


# Mock geopolitical events database
MOCK_EVENTS = [
    {"event": "US-China trade tensions escalation", "impact": "high", "sectors": ["tech", "semiconductors", "manufacturing"]},
    {"event": "Middle East oil supply disruption fears", "impact": "high", "sectors": ["energy", "airlines", "transportation"]},
    {"event": "EU carbon border tax implementation", "impact": "medium", "sectors": ["industrials", "materials", "utilities"]},
    {"event": "Taiwan strait military exercises", "impact": "critical", "sectors": ["semiconductors", "defense", "tech"]},
    {"event": "Russia sanctions expansion", "impact": "medium", "sectors": ["energy", "financials", "commodities"]},
    {"event": "OPEC+ production cut announcement", "impact": "high", "sectors": ["energy", "transportation", "chemicals"]},
    {"event": "Global shipping route disruptions", "impact": "medium", "sectors": ["retail", "manufacturing", "logistics"]},
    {"event": "US defense spending bill passed", "impact": "medium", "sectors": ["defense", "aerospace", "cybersecurity"]},
    {"event": "Emerging market currency crisis fears", "impact": "low", "sectors": ["financials", "consumer goods"]},
    {"event": "AI regulation framework proposed in EU", "impact": "medium", "sectors": ["tech", "AI", "cloud"]},
]


class GeopoliticalAgent(BaseAgent):
    name = "geopolitical_agent"
    description = "Scans for global events, tariffs, supply chain shocks, and defense sector catalysts."

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")

        # Select 3-5 random events
        num_events = random.randint(3, 5)
        active_events = random.sample(MOCK_EVENTS, min(num_events, len(MOCK_EVENTS)))

        # Score the risk level
        impact_scores = {"critical": 30, "high": 20, "medium": 10, "low": 5}
        total_risk = sum(impact_scores.get(e["impact"], 5) for e in active_events)
        risk_normalized = min(total_risk / 100, 1.0)

        # Determine signal
        if risk_normalized > 0.7:
            signal = "bearish"
            score = random.uniform(20, 35)
        elif risk_normalized > 0.4:
            signal = "neutral"
            score = random.uniform(40, 55)
        else:
            signal = "bullish"
            score = random.uniform(60, 75)

        llm_analysis = self._llm_call(
            system_prompt="You are a geopolitical risk analyst. Assess the impact of current events on equity markets in 2-3 sentences.",
            user_prompt=(
                f"Ticker: {ticker}\n"
                f"Active geopolitical events:\n" +
                "\n".join([f"- {e['event']} (Impact: {e['impact']}, Sectors: {', '.join(e['sectors'])})" for e in active_events]) +
                f"\nOverall risk score: {risk_normalized:.2f}/1.0"
            ),
        )

        return self._make_output(
            confidence=round(random.uniform(0.4, 0.7), 2),
            signal=signal,
            score=round(score, 1),
            summary=llm_analysis,
            data={
                "active_events": active_events,
                "risk_score": round(risk_normalized, 3),
                "event_count": len(active_events),
            },
            key_findings=[
                f"Geopolitical risk level: {'HIGH' if risk_normalized > 0.6 else 'MODERATE' if risk_normalized > 0.3 else 'LOW'}",
                f"{len(active_events)} active events detected",
            ] + [e["event"] for e in active_events[:3]],
        )
