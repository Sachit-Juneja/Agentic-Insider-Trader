"""
Agent #4: Market Regime Agent — classifies current market state using VIX and SPY trends.
"""

import random
from typing import Any

from app.agents.base import BaseAgent


class MarketRegimeAgent(BaseAgent):
    name = "market_regime_agent"
    description = "Classifies current market state (High-Vol Bear, Low-Vol Bull, etc.) based on VIX and SPY trends."

    REGIMES = {
        "low_vol_bull": {"label": "Low-Vol Bull 🐂", "description": "Calm uptrend — ideal for long positions", "bias": "bullish"},
        "high_vol_bull": {"label": "High-Vol Bull ⚡🐂", "description": "Volatile uptrend — momentum plays with tight stops", "bias": "bullish"},
        "low_vol_bear": {"label": "Low-Vol Bear 🐻", "description": "Grinding lower — slow bleed, avoid catching knives", "bias": "bearish"},
        "high_vol_bear": {"label": "High-Vol Bear 💀🐻", "description": "Panic selling — extreme fear, potential snapback", "bias": "bearish"},
        "transition": {"label": "Regime Transition ⚠️", "description": "Market shifting between states — elevated uncertainty", "bias": "neutral"},
    }

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        # Mock VIX and SPY data
        vix_current = round(random.uniform(12, 40), 1)
        vix_20d_avg = round(random.uniform(14, 30), 1)
        spy_return_20d = round(random.uniform(-8, 8), 2)
        spy_return_60d = round(random.uniform(-15, 15), 2)
        spy_above_200ma = random.choice([True, True, True, False])  # bias toward True

        # Classify regime
        if vix_current < 20 and spy_return_20d > 0:
            regime_key = "low_vol_bull"
        elif vix_current >= 20 and spy_return_20d > 0:
            regime_key = "high_vol_bull"
        elif vix_current < 20 and spy_return_20d <= 0:
            regime_key = "low_vol_bear"
        elif vix_current >= 30 and spy_return_20d < -3:
            regime_key = "high_vol_bear"
        else:
            regime_key = "transition"

        regime = self.REGIMES[regime_key]

        # Score based on regime favorability for longs
        regime_scores = {
            "low_vol_bull": random.uniform(70, 85),
            "high_vol_bull": random.uniform(55, 70),
            "transition": random.uniform(40, 55),
            "low_vol_bear": random.uniform(25, 40),
            "high_vol_bear": random.uniform(15, 30),
        }
        score = regime_scores[regime_key]

        return self._make_output(
            confidence=round(random.uniform(0.6, 0.9), 2),
            signal=regime["bias"],
            score=round(score, 1),
            summary=f"Current regime: {regime['label']}. {regime['description']}. VIX at {vix_current}.",
            data={
                "regime": regime_key,
                "regime_label": regime["label"],
                "vix_current": vix_current,
                "vix_20d_avg": vix_20d_avg,
                "spy_return_20d": spy_return_20d,
                "spy_return_60d": spy_return_60d,
                "spy_above_200ma": spy_above_200ma,
            },
            key_findings=[
                f"Market Regime: {regime['label']}",
                f"VIX: {vix_current} (20d avg: {vix_20d_avg})",
                f"SPY 20d return: {spy_return_20d}%",
                f"SPY {'above' if spy_above_200ma else 'below'} 200-day MA",
            ],
        )
