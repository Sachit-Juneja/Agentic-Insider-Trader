"""
Agent #7: Dark Pool Monitor — estimates institutional block trades and off-exchange routing volumes.
"""

import random
from typing import Any

from app.agents.base import BaseAgent


class DarkPoolAgent(BaseAgent):
    name = "dark_pool_monitor"
    description = "Estimates institutional block trades and off-exchange routing volumes."

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")

        # Mock dark pool data
        dark_pool_pct = round(random.uniform(30, 55), 1)  # % of total volume
        total_volume = random.randint(5_000_000, 100_000_000)
        dark_pool_volume = int(total_volume * dark_pool_pct / 100)
        lit_volume = total_volume - dark_pool_volume

        # Block trades (institutional)
        block_trades = []
        num_blocks = random.randint(3, 8)
        for _ in range(num_blocks):
            size = random.randint(10_000, 500_000)
            block_trades.append({
                "shares": size,
                "estimated_value_usd": size * random.uniform(50, 500),
                "exchange": random.choice(["FINRA ADF", "IEX", "MEMX", "NYSE Arca"]),
                "side_estimate": random.choice(["buy", "buy", "sell"]),  # bias buy
            })

        net_buy_blocks = sum(1 for b in block_trades if b["side_estimate"] == "buy")
        net_sell_blocks = len(block_trades) - net_buy_blocks
        institutional_bias = "accumulation" if net_buy_blocks > net_sell_blocks else "distribution"

        # Short volume
        short_volume_pct = round(random.uniform(15, 45), 1)
        short_exempt_volume = round(random.uniform(1, 8), 1)

        if institutional_bias == "accumulation" and dark_pool_pct > 40:
            signal = "bullish"
            score = random.uniform(60, 78)
        elif institutional_bias == "distribution" and short_volume_pct > 35:
            signal = "bearish"
            score = random.uniform(25, 38)
        else:
            signal = "neutral"
            score = random.uniform(42, 58)

        return self._make_output(
            confidence=round(random.uniform(0.4, 0.7), 2),
            signal=signal,
            score=round(score, 1),
            summary=(
                f"Dark pool volume: {dark_pool_pct}% of total ({dark_pool_volume:,} shares). "
                f"Institutional bias: {institutional_bias.upper()}. "
                f"{num_blocks} block trades detected. Short volume: {short_volume_pct}%."
            ),
            data={
                "dark_pool_pct": dark_pool_pct,
                "dark_pool_volume": dark_pool_volume,
                "lit_volume": lit_volume,
                "total_volume": total_volume,
                "block_trades": block_trades,
                "institutional_bias": institutional_bias,
                "short_volume_pct": short_volume_pct,
                "short_exempt_volume_pct": short_exempt_volume,
                "net_buy_blocks": net_buy_blocks,
                "net_sell_blocks": net_sell_blocks,
            },
            key_findings=[
                f"Dark Pool: {dark_pool_pct}% off-exchange volume",
                f"Institutional Bias: {'🏦 ACCUMULATION' if institutional_bias == 'accumulation' else '📉 DISTRIBUTION'}",
                f"Block Trades: {num_blocks} detected ({net_buy_blocks} buy / {net_sell_blocks} sell)",
                f"Short Volume: {short_volume_pct}%",
            ],
        )
