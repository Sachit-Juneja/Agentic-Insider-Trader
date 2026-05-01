"""
Agent #10: Insider Trading Agent — the star of the show.
Scrapes SEC Form 4s and tracks Congressional stock trades.
"""

import random
from typing import Any
from datetime import datetime, timedelta

from app.agents.base import BaseAgent


# Mock congressional trading data
CONGRESS_MEMBERS = [
    {"name": "Nancy Pelosi", "party": "D", "role": "Former Speaker"},
    {"name": "Dan Crenshaw", "party": "R", "role": "Representative"},
    {"name": "Tommy Tuberville", "party": "R", "role": "Senator"},
    {"name": "Michael McCaul", "party": "R", "role": "Representative"},
    {"name": "Ro Khanna", "party": "D", "role": "Representative"},
    {"name": "Pat Fallon", "party": "R", "role": "Representative"},
    {"name": "Josh Gottheimer", "party": "D", "role": "Representative"},
]

INSIDER_TITLES = [
    "CEO", "CFO", "COO", "CTO", "Director", "VP Sales",
    "EVP", "General Counsel", "Board Member", "SVP Engineering",
]


class InsiderTradingAgent(BaseAgent):
    name = "insider_trading_agent"
    description = "Scrapes SEC Form 4s and tracks Congressional stock trades (Nancy Pelosi's portfolio moves)."

    def _mock_form4_filings(self, ticker: str) -> list[dict]:
        """Generate mock SEC Form 4 insider trading data."""
        filings = []
        now = datetime.now()

        for i in range(random.randint(3, 10)):
            days_ago = random.randint(1, 90)
            filing_date = now - timedelta(days=days_ago)
            is_buy = random.choice([True, True, False])  # bias buy
            shares = random.randint(1000, 500_000)
            price = round(random.uniform(50, 500), 2)

            filings.append({
                "filing_date": filing_date.strftime("%Y-%m-%d"),
                "insider_name": f"{'John' if random.random() > 0.5 else 'Jane'} {'Smith' if random.random() > 0.5 else 'Doe'}",
                "insider_title": random.choice(INSIDER_TITLES),
                "transaction_type": "Purchase" if is_buy else "Sale",
                "shares": shares,
                "price_per_share": price,
                "total_value_usd": shares * price,
                "shares_owned_after": random.randint(10_000, 5_000_000),
                "is_10b5_1_plan": random.choice([True, False]),
            })

        return sorted(filings, key=lambda x: x["filing_date"], reverse=True)

    def _mock_congressional_trades(self, ticker: str) -> list[dict]:
        """Generate mock Congressional trading data."""
        trades = []
        now = datetime.now()

        # Not all tickers have congressional trades
        if random.random() > 0.4:
            num_trades = random.randint(1, 4)
            for _ in range(num_trades):
                days_ago = random.randint(5, 120)
                member = random.choice(CONGRESS_MEMBERS)
                is_buy = random.choice([True, True, False])

                trades.append({
                    "disclosure_date": (now - timedelta(days=days_ago)).strftime("%Y-%m-%d"),
                    "member": member["name"],
                    "party": member["party"],
                    "role": member["role"],
                    "transaction_type": "Purchase" if is_buy else "Sale",
                    "amount_range": random.choice([
                        "$1,001 - $15,000",
                        "$15,001 - $50,000",
                        "$50,001 - $100,000",
                        "$100,001 - $250,000",
                        "$250,001 - $500,000",
                        "$500,001 - $1,000,000",
                    ]),
                    "days_until_disclosure": random.randint(15, 45),
                })

        return trades

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")

        form4_filings = self._mock_form4_filings(ticker)
        congressional_trades = self._mock_congressional_trades(ticker)

        # Analyze insider sentiment
        insider_buys = sum(1 for f in form4_filings if f["transaction_type"] == "Purchase")
        insider_sells = len(form4_filings) - insider_buys
        insider_buy_value = sum(f["total_value_usd"] for f in form4_filings if f["transaction_type"] == "Purchase")
        insider_sell_value = sum(f["total_value_usd"] for f in form4_filings if f["transaction_type"] == "Sale")

        congress_buys = sum(1 for t in congressional_trades if t["transaction_type"] == "Purchase")
        congress_sells = len(congressional_trades) - congress_buys

        # Score
        if insider_buys > insider_sells and insider_buy_value > insider_sell_value:
            signal = "bullish"
            score = random.uniform(65, 82)
            insider_verdict = "Net insider BUYING — management putting money where mouth is"
        elif insider_sells > insider_buys * 2:
            signal = "bearish"
            score = random.uniform(20, 35)
            insider_verdict = "Heavy insider SELLING — management heading for the exits"
        else:
            signal = "neutral"
            score = random.uniform(40, 58)
            insider_verdict = "Mixed insider activity — no clear directional signal"

        # Congressional trading bonus
        congress_note = ""
        if congressional_trades:
            if congress_buys > congress_sells:
                score = min(score + 8, 100)
                congress_note = f" Congress is buying ({congress_buys} buys vs {congress_sells} sells) — historically bullish signal."
            elif congress_sells > congress_buys:
                score = max(score - 8, 0)
                congress_note = f" Congress is selling ({congress_sells} sells vs {congress_buys} buys) — concerning."

        return self._make_output(
            confidence=round(random.uniform(0.5, 0.8), 2),
            signal=signal,
            score=round(score, 1),
            summary=f"{insider_verdict}.{congress_note}",
            data={
                "form4_filings": form4_filings,
                "congressional_trades": congressional_trades,
                "insider_buys": insider_buys,
                "insider_sells": insider_sells,
                "insider_buy_value": insider_buy_value,
                "insider_sell_value": insider_sell_value,
                "congress_buys": congress_buys,
                "congress_sells": congress_sells,
                "net_insider_sentiment": "bullish" if insider_buy_value > insider_sell_value else "bearish",
            },
            key_findings=[
                f"📋 {len(form4_filings)} Form 4 filings in last 90 days",
                f"Insider Buys: {insider_buys} (${insider_buy_value:,.0f})",
                f"Insider Sells: {insider_sells} (${insider_sell_value:,.0f})",
                f"🏛️ Congressional trades: {len(congressional_trades)}",
            ] + ([f"🔥 {t['member']} ({t['party']}) {t['transaction_type']}: {t['amount_range']}" for t in congressional_trades[:3]]),
        )
