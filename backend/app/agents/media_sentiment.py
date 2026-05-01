"""
Agent #11: Traditional Media Sentiment Agent — analyzes Bloomberg, WSJ, CNBC headlines.
"""

import random
from typing import Any
from datetime import datetime, timedelta

from app.agents.base import BaseAgent

MOCK_HEADLINES = [
    ("{ticker} beats Q3 earnings estimates, shares surge", "bullish", "Bloomberg"),
    ("{ticker} faces regulatory scrutiny", "bearish", "WSJ"),
    ("Analysts upgrade {ticker} citing strong AI momentum", "bullish", "CNBC"),
    ("{ticker} CFO sells $2M in shares", "bearish", "Bloomberg"),
    ("{ticker} announces $10B buyback program", "bullish", "WSJ"),
    ("Supply chain concerns weigh on {ticker}", "bearish", "Reuters"),
    ("{ticker} expands into new markets", "bullish", "CNBC"),
    ("Competition intensifies for {ticker}", "bearish", "Bloomberg"),
    ("{ticker} raises full-year guidance", "bullish", "MarketWatch"),
    ("Activist investor takes stake in {ticker}", "neutral", "WSJ"),
    ("{ticker} partners with tech firm for AI", "bullish", "TechCrunch"),
    ("Labor disputes threaten {ticker} timeline", "bearish", "Reuters"),
    ("{ticker} dividend increase signals confidence", "bullish", "Barron's"),
    ("Macro headwinds may slow {ticker}, says Goldman", "bearish", "Bloomberg"),
    ("{ticker} launches innovative product line", "bullish", "CNBC"),
]


class MediaSentimentAgent(BaseAgent):
    name = "media_sentiment_agent"
    description = "Analyzes Bloomberg, WSJ, and CNBC headlines for traditional media sentiment."

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")
        now = datetime.now()
        num = random.randint(8, 15)
        selected = random.sample(MOCK_HEADLINES, min(num, len(MOCK_HEADLINES)))

        headlines = []
        for tmpl, sentiment, source in selected:
            headlines.append({
                "headline": tmpl.format(ticker=ticker),
                "source": source,
                "sentiment": sentiment,
                "date": (now - timedelta(days=random.randint(0, 14))).strftime("%Y-%m-%d"),
            })

        bullish = sum(1 for h in headlines if h["sentiment"] == "bullish")
        bearish = sum(1 for h in headlines if h["sentiment"] == "bearish")
        total = len(headlines)
        bp = bullish / total * 100
        brp = bearish / total * 100

        if bp > 60:
            signal, score = "bullish", random.uniform(62, 78)
        elif brp > 60:
            signal, score = "bearish", random.uniform(25, 38)
        else:
            signal, score = "neutral", random.uniform(42, 58)

        return self._make_output(
            confidence=round(random.uniform(0.45, 0.75), 2),
            signal=signal,
            score=round(score, 1),
            summary=f"Media sentiment: {bp:.0f}% bullish / {brp:.0f}% bearish across {total} articles.",
            data={"headlines": headlines, "bullish_pct": round(bp, 1), "bearish_pct": round(brp, 1)},
            key_findings=[
                f"📰 {total} articles analyzed",
                f"Bullish: {bullish} ({bp:.0f}%) | Bearish: {bearish} ({brp:.0f}%)",
                f"Top: {headlines[0]['headline']}",
            ],
        )
