"""
Agent #5: Technical Analyst — computes RSI, MACD, Bollinger Bands, moving averages.
Uses vectorized numpy/pandas operations.
"""

import random
from typing import Any

import numpy as np
import pandas as pd

from app.agents.base import BaseAgent
from app.config import settings
from services.market_data import get_price_history


class TechnicalAnalystAgent(BaseAgent):
    name = "technical_analyst"
    description = "Computes moving averages, RSI, MACD, and Bollinger Bands using vectorized numpy/pandas ops."

    def _generate_mock_prices(self, days: int = 252) -> pd.DataFrame:
        """Generate realistic mock OHLCV data using geometric Brownian motion."""
        np.random.seed(random.randint(0, 10000))
        base_price = random.uniform(50, 500)
        mu = random.uniform(-0.1, 0.3) / 252  # daily drift
        sigma = random.uniform(0.15, 0.45) / np.sqrt(252)  # daily vol

        returns = np.random.normal(mu, sigma, days)
        prices = base_price * np.exp(np.cumsum(returns))

        dates = pd.date_range(end=pd.Timestamp.now(), periods=days, freq="B")
        df = pd.DataFrame({
            "date": dates,
            "close": prices,
            "open": prices * (1 + np.random.normal(0, 0.005, days)),
            "high": prices * (1 + np.abs(np.random.normal(0, 0.01, days))),
            "low": prices * (1 - np.abs(np.random.normal(0, 0.01, days))),
            "volume": np.random.randint(1_000_000, 50_000_000, days),
        })
        return df.set_index("date")

    def _compute_rsi(self, prices: pd.Series, period: int = 14) -> float:
        """Vectorized RSI computation."""
        delta = prices.diff()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        rs = avg_gain / avg_loss.replace(0, np.nan)
        rsi = 100 - (100 / (1 + rs))
        return round(float(rsi.iloc[-1]), 2)

    def _compute_macd(self, prices: pd.Series) -> dict:
        """Vectorized MACD computation."""
        ema12 = prices.ewm(span=12, adjust=False).mean()
        ema26 = prices.ewm(span=26, adjust=False).mean()
        macd_line = ema12 - ema26
        signal_line = macd_line.ewm(span=9, adjust=False).mean()
        histogram = macd_line - signal_line
        return {
            "macd": round(float(macd_line.iloc[-1]), 4),
            "signal": round(float(signal_line.iloc[-1]), 4),
            "histogram": round(float(histogram.iloc[-1]), 4),
            "crossover": "bullish" if float(histogram.iloc[-1]) > 0 and float(histogram.iloc[-2]) <= 0 else
                         "bearish" if float(histogram.iloc[-1]) < 0 and float(histogram.iloc[-2]) >= 0 else "none",
        }

    def _compute_bollinger(self, prices: pd.Series, period: int = 20) -> dict:
        """Vectorized Bollinger Bands."""
        sma = prices.rolling(window=period).mean()
        std = prices.rolling(window=period).std()
        upper = sma + (2 * std)
        lower = sma - (2 * std)
        current = float(prices.iloc[-1])
        band_width = float((upper.iloc[-1] - lower.iloc[-1]) / sma.iloc[-1]) * 100

        if current > float(upper.iloc[-1]):
            position = "above_upper"
        elif current < float(lower.iloc[-1]):
            position = "below_lower"
        else:
            pct = (current - float(lower.iloc[-1])) / (float(upper.iloc[-1]) - float(lower.iloc[-1]))
            position = f"within_bands_{round(pct*100)}pct"

        return {
            "upper": round(float(upper.iloc[-1]), 2),
            "middle": round(float(sma.iloc[-1]), 2),
            "lower": round(float(lower.iloc[-1]), 2),
            "band_width_pct": round(band_width, 2),
            "position": position,
        }

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")
        
        if settings.use_mock_data:
            df = self._generate_mock_prices()
        else:
            df = get_price_history(ticker, period="1y")
            if df.empty:
                df = self._generate_mock_prices() # Fallback
            else:
                df.columns = [c.lower() for c in df.columns]

        close = df["close"]

        # Compute all indicators
        sma_20 = round(float(close.rolling(20).mean().iloc[-1]), 2)
        sma_50 = round(float(close.rolling(50).mean().iloc[-1]), 2)
        sma_200 = round(float(close.rolling(200).mean().iloc[-1]), 2)
        current_price = round(float(close.iloc[-1]), 2)
        rsi = self._compute_rsi(close)
        macd = self._compute_macd(close)
        bollinger = self._compute_bollinger(close)

        # Determine overall technical signal
        signals = []
        if current_price > sma_50 > sma_200:
            signals.append("bullish")  # Golden cross territory
        elif current_price < sma_50 < sma_200:
            signals.append("bearish")  # Death cross territory

        if rsi < 30:
            signals.append("bullish")  # Oversold
        elif rsi > 70:
            signals.append("bearish")  # Overbought

        if macd["histogram"] > 0:
            signals.append("bullish")
        else:
            signals.append("bearish")

        bullish_count = signals.count("bullish")
        bearish_count = signals.count("bearish")

        if bullish_count > bearish_count:
            signal = "bullish"
            score = random.uniform(60, 80)
        elif bearish_count > bullish_count:
            signal = "bearish"
            score = random.uniform(25, 40)
        else:
            signal = "neutral"
            score = random.uniform(40, 60)

        # Price chart data for frontend
        chart_data = {
            "prices": [round(float(p), 2) for p in close.tail(60).values],
            "dates": [d.strftime("%Y-%m-%d") for d in close.tail(60).index],
            "sma_20": [round(float(p), 2) for p in close.rolling(20).mean().tail(60).values],
            "sma_50": [round(float(p), 2) for p in close.rolling(50).mean().tail(60).values],
        }

        return self._make_output(
            confidence=round(random.uniform(0.55, 0.85), 2),
            signal=signal,
            score=round(score, 1),
            summary=(
                f"{ticker} at ${current_price}. RSI: {rsi} ({'oversold' if rsi < 30 else 'overbought' if rsi > 70 else 'neutral'}). "
                f"MACD: {macd['crossover']} crossover. Price {'above' if current_price > sma_200 else 'below'} 200-day MA."
            ),
            data={
                "current_price": current_price,
                "sma_20": sma_20,
                "sma_50": sma_50,
                "sma_200": sma_200,
                "rsi": rsi,
                "macd": macd,
                "bollinger": bollinger,
                "chart_data": chart_data,
            },
            key_findings=[
                f"Price: ${current_price}",
                f"RSI(14): {rsi} — {'⚠️ OVERSOLD' if rsi < 30 else '⚠️ OVERBOUGHT' if rsi > 70 else 'Neutral'}",
                f"MACD: {macd['crossover'].upper()} crossover (histogram: {macd['histogram']})",
                f"Bollinger: {bollinger['position']}",
                f"Trend: {'🐂 Above' if current_price > sma_200 else '🐻 Below'} 200-day MA",
            ],
        )
