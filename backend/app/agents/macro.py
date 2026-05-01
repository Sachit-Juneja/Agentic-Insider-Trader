"""
Agent #2: Macroeconomic Agent — analyzes CPI, Fed rates, yield curve, GDP.
"""

import random
from typing import Any

from app.agents.base import BaseAgent
from app.config import settings


class MacroAgent(BaseAgent):
    name = "macro_agent"
    description = "Analyzes broad macroeconomic conditions: CPI, Fed rates, yield curve, GDP growth."

    def _get_macro_data(self) -> dict:
        """Fetch or mock macroeconomic data."""
        # Mock data — in production, pull from FRED API or similar
        return {
            "fed_funds_rate": round(random.uniform(4.5, 5.5), 2),
            "cpi_yoy": round(random.uniform(2.5, 4.0), 1),
            "gdp_growth_q": round(random.uniform(-0.5, 3.0), 1),
            "yield_curve_spread": round(random.uniform(-0.5, 1.5), 2),  # 10Y - 2Y
            "unemployment_rate": round(random.uniform(3.5, 4.5), 1),
            "pce_inflation": round(random.uniform(2.0, 3.5), 1),
            "consumer_confidence": round(random.uniform(85, 115), 1),
            "ism_manufacturing": round(random.uniform(45, 55), 1),
        }

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        macro_data = self._get_macro_data()

        # Determine macro signal
        yield_spread = macro_data["yield_curve_spread"]
        cpi = macro_data["cpi_yoy"]
        gdp = macro_data["gdp_growth_q"]

        if yield_spread < 0 and cpi > 3.5:
            signal = "bearish"
            score = random.uniform(20, 35)
            outlook = "Inverted yield curve + elevated inflation = recessionary signal"
        elif gdp > 2.0 and cpi < 3.0:
            signal = "bullish"
            score = random.uniform(65, 80)
            outlook = "Solid GDP growth with cooling inflation = Goldilocks environment"
        else:
            signal = "neutral"
            score = random.uniform(40, 60)
            outlook = "Mixed macro signals — growth present but inflation concerns persist"

        llm_analysis = self._llm_call(
            system_prompt="You are a macroeconomic analyst. Provide a concise 2-3 sentence assessment.",
            user_prompt=(
                f"Given these macro conditions for analyzing {state.get('ticker', 'N/A')}:\n"
                f"Fed Rate: {macro_data['fed_funds_rate']}% | CPI: {macro_data['cpi_yoy']}%\n"
                f"GDP Growth: {macro_data['gdp_growth_q']}% | Yield Spread: {yield_spread}bps\n"
                f"Unemployment: {macro_data['unemployment_rate']}%\n"
                f"What is your macro outlook for equities over {state.get('hold_period', '3m')}?"
            ),
        )

        return self._make_output(
            confidence=round(random.uniform(0.55, 0.85), 2),
            signal=signal,
            score=round(score, 1),
            summary=f"{outlook}. {llm_analysis}",
            data=macro_data,
            key_findings=[
                f"Fed Funds Rate: {macro_data['fed_funds_rate']}%",
                f"CPI YoY: {macro_data['cpi_yoy']}%",
                f"Yield Curve: {'Inverted' if yield_spread < 0 else 'Normal'} ({yield_spread})",
                f"GDP Growth: {macro_data['gdp_growth_q']}%",
                outlook,
            ],
        )
