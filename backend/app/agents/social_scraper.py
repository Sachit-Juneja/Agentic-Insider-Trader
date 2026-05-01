"""
Agent #12: Degenerate Social Scraper — scans Reddit, X/Twitter, StockTwits for retail sentiment.
"""

import random
from typing import Any

from app.agents.base import BaseAgent

MOCK_POSTS = [
    {"source": "r/wallstreetbets", "text": "{ticker} to the moon 🚀🚀🚀 diamond hands", "sentiment": "bullish", "upvotes": 2847},
    {"source": "r/wallstreetbets", "text": "Just YOLOd my entire portfolio into {ticker} calls expiring Friday", "sentiment": "bullish", "upvotes": 1523},
    {"source": "r/wallstreetbets", "text": "{ticker} puts printing. bears eating tonight 🐻", "sentiment": "bearish", "upvotes": 892},
    {"source": "StockTwits", "text": "${ticker} breakout incoming. Volume is insane today", "sentiment": "bullish", "upvotes": 445},
    {"source": "StockTwits", "text": "${ticker} bag holders cope thread", "sentiment": "bearish", "upvotes": 678},
    {"source": "X/Twitter", "text": "Everyone sleeping on ${ticker}. This is a generational buy.", "sentiment": "bullish", "upvotes": 12400},
    {"source": "X/Twitter", "text": "${ticker} is going to zero. Change my mind.", "sentiment": "bearish", "upvotes": 3200},
    {"source": "r/stocks", "text": "{ticker} DD: undervalued based on DCF model", "sentiment": "bullish", "upvotes": 567},
    {"source": "r/wallstreetbets", "text": "My wife's boyfriend said to sell {ticker}. Inversing him.", "sentiment": "bullish", "upvotes": 4200},
    {"source": "StockTwits", "text": "${ticker} shorts about to get squeezed hard", "sentiment": "bullish", "upvotes": 890},
]


class SocialScraperAgent(BaseAgent):
    name = "social_scraper"
    description = "Scans Reddit (r/wallstreetbets), X/Twitter, StockTwits for retail momentum and meme potential."

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")
        selected = random.sample(MOCK_POSTS, min(random.randint(5, 10), len(MOCK_POSTS)))
        posts = [{"text": p["text"].format(ticker=ticker), "source": p["source"],
                   "sentiment": p["sentiment"], "upvotes": p["upvotes"]} for p in selected]

        bullish = sum(1 for p in posts if p["sentiment"] == "bullish")
        bearish = len(posts) - bullish
        mention_velocity = random.randint(50, 5000)
        meme_score = round(random.uniform(0, 10), 1)
        wsb_mentions = random.randint(0, 500)

        if bullish > bearish and meme_score > 6:
            signal, score = "bullish", random.uniform(60, 80)
        elif bearish > bullish:
            signal, score = "bearish", random.uniform(25, 40)
        else:
            signal, score = "neutral", random.uniform(40, 58)

        return self._make_output(
            confidence=round(random.uniform(0.3, 0.6), 2),
            signal=signal, score=round(score, 1),
            summary=f"Retail sentiment: {bullish}/{len(posts)} bullish. Meme score: {meme_score}/10. WSB mentions: {wsb_mentions}.",
            data={"posts": posts, "mention_velocity": mention_velocity,
                   "meme_score": meme_score, "wsb_mentions": wsb_mentions},
            key_findings=[
                f"🦍 WSB Mentions: {wsb_mentions}/day",
                f"Meme Score: {meme_score}/10 {'🔥' if meme_score > 7 else ''}",
                f"Retail Sentiment: {bullish} bullish / {bearish} bearish",
                f"Mention Velocity: {mention_velocity}/hr",
            ],
        )
