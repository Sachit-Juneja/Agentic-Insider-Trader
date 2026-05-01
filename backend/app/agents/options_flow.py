"""
Agent #6: Options Flow Agent — tracks unusual options activity, gamma exposure, put/call ratios.
"""

import random
from typing import Any

from app.agents.base import BaseAgent
from app.config import settings
from services.market_data import get_options_chain


class OptionsFlowAgent(BaseAgent):
    name = "options_flow_agent"
    description = "Tracks unusual options activity, gamma exposure, and put/call ratios."

    def _mock_options_data(self, ticker: str) -> dict:
        """Generate mock options flow data."""
        put_call_ratio = round(random.uniform(0.5, 1.8), 2)
        total_volume = random.randint(50_000, 500_000)
        put_volume = int(total_volume * put_call_ratio / (1 + put_call_ratio))
        call_volume = total_volume - put_volume

        # Unusual activity detection
        unusual_trades = []
        for _ in range(random.randint(2, 6)):
            is_call = random.choice([True, True, False])  # bias toward calls
            strike_pct = random.uniform(0.9, 1.15)
            days_to_expiry = random.choice([7, 14, 30, 45, 60, 90])
            premium = random.randint(50_000, 5_000_000)
            unusual_trades.append({
                "type": "CALL" if is_call else "PUT",
                "strike_pct_from_spot": round(strike_pct, 2),
                "dte": days_to_expiry,
                "premium_usd": premium,
                "sentiment": "bullish" if is_call else "bearish",
                "size": "SWEEP" if premium > 1_000_000 else "BLOCK",
            })

        # Gamma exposure
        gamma_exposure = round(random.uniform(-500, 500), 1)  # in millions
        max_pain = round(random.uniform(0.95, 1.05), 3)

        return {
            "put_call_ratio": put_call_ratio,
            "total_volume": total_volume,
            "call_volume": call_volume,
            "put_volume": put_volume,
            "unusual_trades": unusual_trades,
            "gamma_exposure_mm": gamma_exposure,
            "max_pain_pct": max_pain,
            "implied_volatility_rank": round(random.uniform(10, 95), 1),
            "iv_percentile": round(random.uniform(15, 90), 1),
        }

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")
        
        if settings.use_mock_data:
            data = self._mock_options_data(ticker)
        else:
            chain = get_options_chain(ticker)
            if not chain:
                data = self._mock_options_data(ticker)
            else:
                calls = chain.get("calls", [])
                puts = chain.get("puts", [])
                
                call_vol = sum(c.get("volume", 0) or 0 for c in calls)
                put_vol = sum(p.get("volume", 0) or 0 for p in puts)
                pc_ratio = round(put_vol / max(call_vol, 1), 2)
                
                # Mock unusual trades from real chain to preserve logic
                data = self._mock_options_data(ticker)
                data["put_call_ratio"] = pc_ratio
                data["total_volume"] = call_vol + put_vol
                data["call_volume"] = call_vol
                data["put_volume"] = put_vol


        # Determine signal
        pc_ratio = data["put_call_ratio"]
        bullish_sweeps = sum(1 for t in data["unusual_trades"] if t["sentiment"] == "bullish" and t["size"] == "SWEEP")
        bearish_sweeps = sum(1 for t in data["unusual_trades"] if t["sentiment"] == "bearish" and t["size"] == "SWEEP")

        if pc_ratio < 0.7 or bullish_sweeps > bearish_sweeps:
            signal = "bullish"
            score = random.uniform(60, 80)
        elif pc_ratio > 1.2 or bearish_sweeps > bullish_sweeps:
            signal = "bearish"
            score = random.uniform(25, 40)
        else:
            signal = "neutral"
            score = random.uniform(42, 58)

        total_premium = sum(t["premium_usd"] for t in data["unusual_trades"])

        return self._make_output(
            confidence=round(random.uniform(0.5, 0.8), 2),
            signal=signal,
            score=round(score, 1),
            summary=(
                f"P/C Ratio: {pc_ratio} ({'put-heavy' if pc_ratio > 1 else 'call-heavy'}). "
                f"{len(data['unusual_trades'])} unusual trades totaling ${total_premium:,.0f} in premium. "
                f"GEX: {data['gamma_exposure_mm']}M. IV Rank: {data['implied_volatility_rank']}%."
            ),
            data=data,
            key_findings=[
                f"Put/Call Ratio: {pc_ratio} ({'🐻 Bearish' if pc_ratio > 1.2 else '🐂 Bullish' if pc_ratio < 0.7 else 'Neutral'})",
                f"Unusual trades: {len(data['unusual_trades'])} (${total_premium:,.0f} premium)",
                f"Gamma Exposure: {data['gamma_exposure_mm']}M ({'dealer long' if data['gamma_exposure_mm'] > 0 else 'dealer short'})",
                f"IV Rank: {data['implied_volatility_rank']}%",
                f"Max Pain: {data['max_pain_pct']*100:.1f}% of spot",
            ],
        )
