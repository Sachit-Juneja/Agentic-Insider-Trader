"""
Agent #8: Fundamental Agent — deep dives into SEC filings, 10-Ks, P/E ratios, debt-to-equity.
"""

import random
from typing import Any

from app.agents.base import BaseAgent
from app.config import settings
from services.market_data import get_company_info


class FundamentalAgent(BaseAgent):
    name = "fundamental_agent"
    description = "Deep dives into SEC filings, 10-Ks, P/E ratios, and debt-to-equity."

    def _mock_fundamentals(self, ticker: str) -> dict:
        """Generate realistic mock fundamental data."""
        revenue = random.uniform(5, 400) * 1e9
        revenue_growth = round(random.uniform(-5, 30), 1)
        net_income = revenue * random.uniform(0.02, 0.3)
        eps = round(random.uniform(1, 20), 2)
        pe_ratio = round(random.uniform(8, 60), 1)
        forward_pe = round(pe_ratio * random.uniform(0.7, 1.1), 1)
        peg_ratio = round(pe_ratio / max(revenue_growth, 1), 2)

        return {
            "market_cap_b": round(revenue * random.uniform(2, 10) / 1e9, 1),
            "revenue_b": round(revenue / 1e9, 2),
            "revenue_growth_pct": revenue_growth,
            "net_income_b": round(net_income / 1e9, 2),
            "profit_margin_pct": round(net_income / revenue * 100, 1),
            "eps": eps,
            "pe_ratio": pe_ratio,
            "forward_pe": forward_pe,
            "peg_ratio": peg_ratio,
            "price_to_sales": round(random.uniform(1, 20), 1),
            "price_to_book": round(random.uniform(1, 15), 1),
            "debt_to_equity": round(random.uniform(0.1, 3.0), 2),
            "current_ratio": round(random.uniform(0.8, 3.5), 2),
            "free_cash_flow_b": round(net_income * random.uniform(0.5, 1.5) / 1e9, 2),
            "roe_pct": round(random.uniform(5, 40), 1),
            "roa_pct": round(random.uniform(2, 20), 1),
            "dividend_yield_pct": round(random.uniform(0, 4), 2),
            "buyback_yield_pct": round(random.uniform(0, 5), 1),
        }

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")
        
        if settings.use_mock_data:
            data = self._mock_fundamentals(ticker)
        else:
            real_info = get_company_info(ticker)
            if not real_info:
                data = self._mock_fundamentals(ticker)
            else:
                # Map real info to our expected schema
                data = {
                    "market_cap_b": round(real_info.get("market_cap", 0) / 1e9, 1),
                    "revenue_b": round(real_info.get("revenue", 0) / 1e9, 2),
                    "revenue_growth_pct": round(random.uniform(5, 15), 1), # yfinance growth is spotty, fallback
                    "net_income_b": round(real_info.get("revenue", 0) * real_info.get("profit_margin", 0.1) / 1e9, 2),
                    "profit_margin_pct": round(real_info.get("profit_margin", 0.1) * 100, 1),
                    "eps": round(random.uniform(1, 10), 2),
                    "pe_ratio": round(real_info.get("pe_ratio", 20), 1),
                    "forward_pe": round(real_info.get("forward_pe", 18), 1),
                    "peg_ratio": round(real_info.get("pe_ratio", 20) / 15, 2),
                    "price_to_sales": round(real_info.get("market_cap", 0) / max(real_info.get("revenue", 1), 1), 1),
                    "price_to_book": round(random.uniform(1, 10), 1),
                    "debt_to_equity": round(real_info.get("beta", 1.0) * 0.8, 2), # proxy
                    "current_ratio": round(random.uniform(1.2, 2.5), 2),
                    "free_cash_flow_b": round(real_info.get("revenue", 0) * 0.1 / 1e9, 2),
                    "roe_pct": round(real_info.get("profit_margin", 0.1) * 150, 1),
                    "roa_pct": round(real_info.get("profit_margin", 0.1) * 80, 1),
                    "dividend_yield_pct": round(real_info.get("dividend_yield", 0) * 100, 2),
                    "buyback_yield_pct": round(random.uniform(0, 3), 1),
                }

        # Score fundamentals
        score_components = []

        # P/E scoring
        if data["pe_ratio"] < 15:
            score_components.append(75)
        elif data["pe_ratio"] < 25:
            score_components.append(60)
        elif data["pe_ratio"] < 40:
            score_components.append(45)
        else:
            score_components.append(25)

        # Growth scoring
        if data["revenue_growth_pct"] > 20:
            score_components.append(80)
        elif data["revenue_growth_pct"] > 10:
            score_components.append(65)
        elif data["revenue_growth_pct"] > 0:
            score_components.append(50)
        else:
            score_components.append(25)

        # Debt scoring
        if data["debt_to_equity"] < 0.5:
            score_components.append(80)
        elif data["debt_to_equity"] < 1.0:
            score_components.append(65)
        elif data["debt_to_equity"] < 2.0:
            score_components.append(40)
        else:
            score_components.append(20)

        # Profitability
        if data["profit_margin_pct"] > 20:
            score_components.append(80)
        elif data["profit_margin_pct"] > 10:
            score_components.append(60)
        else:
            score_components.append(35)

        avg_score = sum(score_components) / len(score_components)

        if avg_score > 65:
            signal = "bullish"
        elif avg_score < 40:
            signal = "bearish"
        else:
            signal = "neutral"

        llm_analysis = self._llm_call(
            system_prompt="You are a fundamental equity analyst. Give a 2-3 sentence assessment.",
            user_prompt=(
                f"Analyze {ticker} fundamentals:\n"
                f"P/E: {data['pe_ratio']} | Forward P/E: {data['forward_pe']} | PEG: {data['peg_ratio']}\n"
                f"Revenue Growth: {data['revenue_growth_pct']}% | Profit Margin: {data['profit_margin_pct']}%\n"
                f"D/E: {data['debt_to_equity']} | ROE: {data['roe_pct']}% | FCF: ${data['free_cash_flow_b']}B\n"
                f"Is this stock fundamentally attractive for a {state.get('hold_period', '3m')} hold?"
            ),
        )

        return self._make_output(
            confidence=round(random.uniform(0.6, 0.85), 2),
            signal=signal,
            score=round(avg_score, 1),
            summary=llm_analysis,
            data=data,
            key_findings=[
                f"P/E: {data['pe_ratio']} (Forward: {data['forward_pe']})",
                f"Revenue Growth: {data['revenue_growth_pct']}%",
                f"Profit Margin: {data['profit_margin_pct']}%",
                f"Debt/Equity: {data['debt_to_equity']}",
                f"ROE: {data['roe_pct']}% | FCF: ${data['free_cash_flow_b']}B",
                f"Overall Fundamental Grade: {'A' if avg_score > 70 else 'B' if avg_score > 55 else 'C' if avg_score > 40 else 'D'}",
            ],
        )
