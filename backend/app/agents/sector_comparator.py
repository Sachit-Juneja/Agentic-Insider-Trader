"""
Agent #9: Sector Comparator — benches the target stock against its top 3 industry peers.
"""

import random
from typing import Any

from app.agents.base import BaseAgent


# Sector peer mapping
SECTOR_PEERS = {
    "AAPL": {"sector": "Technology", "peers": ["MSFT", "GOOGL", "AMZN"]},
    "MSFT": {"sector": "Technology", "peers": ["AAPL", "GOOGL", "CRM"]},
    "GOOGL": {"sector": "Technology", "peers": ["META", "MSFT", "AMZN"]},
    "TSLA": {"sector": "Automotive/EV", "peers": ["RIVN", "F", "GM"]},
    "JPM": {"sector": "Financials", "peers": ["BAC", "GS", "MS"]},
    "NVDA": {"sector": "Semiconductors", "peers": ["AMD", "INTC", "AVGO"]},
    "META": {"sector": "Social Media", "peers": ["GOOGL", "SNAP", "PINS"]},
    "AMZN": {"sector": "E-Commerce/Cloud", "peers": ["MSFT", "GOOGL", "SHOP"]},
}

DEFAULT_PEERS = {"sector": "General", "peers": ["SPY", "QQQ", "IWM"]}


class SectorComparatorAgent(BaseAgent):
    name = "sector_comparator"
    description = "Benchmarks the target stock against its top 3 industry peers."

    def _mock_peer_data(self, ticker: str) -> dict:
        """Generate mock comparison data for a stock."""
        return {
            "ticker": ticker,
            "pe_ratio": round(random.uniform(10, 50), 1),
            "revenue_growth_pct": round(random.uniform(-5, 30), 1),
            "profit_margin_pct": round(random.uniform(5, 35), 1),
            "return_1m_pct": round(random.uniform(-10, 15), 1),
            "return_3m_pct": round(random.uniform(-20, 25), 1),
            "return_ytd_pct": round(random.uniform(-15, 40), 1),
            "market_cap_b": round(random.uniform(10, 3000), 0),
            "beta": round(random.uniform(0.5, 2.0), 2),
        }

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A").upper()

        peer_info = SECTOR_PEERS.get(ticker, DEFAULT_PEERS)
        sector = peer_info["sector"]
        peers = peer_info["peers"]

        # Generate comparison data
        target_data = self._mock_peer_data(ticker)
        peer_data = [self._mock_peer_data(p) for p in peers]

        # Rank target vs peers on key metrics
        all_tickers = [target_data] + peer_data
        rankings = {}
        for metric in ["pe_ratio", "revenue_growth_pct", "profit_margin_pct", "return_3m_pct"]:
            reverse = metric != "pe_ratio"  # Lower P/E = better
            sorted_list = sorted(all_tickers, key=lambda x: x[metric], reverse=reverse)
            rank = next(i for i, t in enumerate(sorted_list) if t["ticker"] == ticker) + 1
            rankings[metric] = rank

        avg_rank = sum(rankings.values()) / len(rankings)

        if avg_rank <= 1.5:
            signal = "bullish"
            score = random.uniform(70, 85)
            verdict = "Sector leader — outperforming peers on key metrics"
        elif avg_rank <= 2.5:
            signal = "neutral"
            score = random.uniform(45, 60)
            verdict = "Mid-pack — performing in line with sector"
        else:
            signal = "bearish"
            score = random.uniform(25, 40)
            verdict = "Lagging peers — underperforming sector"

        return self._make_output(
            confidence=round(random.uniform(0.55, 0.8), 2),
            signal=signal,
            score=round(score, 1),
            summary=f"Sector: {sector}. {verdict}. Average rank vs 3 peers: {avg_rank:.1f}/4.",
            data={
                "sector": sector,
                "target": target_data,
                "peers": peer_data,
                "rankings": rankings,
                "average_rank": round(avg_rank, 2),
            },
            key_findings=[
                f"Sector: {sector}",
                f"Peers: {', '.join(peers)}",
                f"Rank in P/E: #{rankings['pe_ratio']}/4",
                f"Rank in Growth: #{rankings['revenue_growth_pct']}/4",
                f"Rank in 3M Return: #{rankings['return_3m_pct']}/4",
                verdict,
            ],
        )
