"""
Market Data Service — yfinance wrapper for price and company data.
"""

from typing import Any, Optional
import yfinance as yf
import pandas as pd


def get_price_history(ticker: str, period: str = "6mo", interval: str = "1d") -> pd.DataFrame:
    """Fetch historical OHLCV data from Yahoo Finance."""
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(period=period, interval=interval)
        return df
    except Exception as e:
        print(f"[MarketData] Error fetching {ticker}: {e}")
        return pd.DataFrame()


def get_company_info(ticker: str) -> dict[str, Any]:
    """Fetch company fundamentals and metadata."""
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            "name": info.get("longName", ticker),
            "sector": info.get("sector", "Unknown"),
            "industry": info.get("industry", "Unknown"),
            "market_cap": info.get("marketCap", 0),
            "pe_ratio": info.get("trailingPE", 0),
            "forward_pe": info.get("forwardPE", 0),
            "price": info.get("currentPrice", 0),
            "52w_high": info.get("fiftyTwoWeekHigh", 0),
            "52w_low": info.get("fiftyTwoWeekLow", 0),
            "beta": info.get("beta", 1.0),
            "dividend_yield": info.get("dividendYield", 0),
            "revenue": info.get("totalRevenue", 0),
            "profit_margin": info.get("profitMargins", 0),
        }
    except Exception as e:
        print(f"[MarketData] Error fetching info for {ticker}: {e}")
        return {}


def get_options_chain(ticker: str) -> Optional[dict]:
    """Fetch options chain data."""
    try:
        stock = yf.Ticker(ticker)
        expirations = stock.options
        if not expirations:
            return None
        # Get nearest expiration
        nearest = expirations[0]
        chain = stock.option_chain(nearest)
        return {
            "expiration": nearest,
            "calls": chain.calls.to_dict("records") if not chain.calls.empty else [],
            "puts": chain.puts.to_dict("records") if not chain.puts.empty else [],
        }
    except Exception as e:
        print(f"[MarketData] Error fetching options for {ticker}: {e}")
        return None


def get_market_indices() -> dict[str, Any]:
    """Fetch SPY and VIX data for market regime detection."""
    result = {}
    for symbol, name in [("SPY", "spy"), ("^VIX", "vix")]:
        try:
            data = yf.Ticker(symbol)
            hist = data.history(period="3mo")
            if not hist.empty:
                result[name] = {
                    "current": float(hist["Close"].iloc[-1]),
                    "change_20d": float((hist["Close"].iloc[-1] / hist["Close"].iloc[-20] - 1) * 100) if len(hist) > 20 else 0,
                    "change_60d": float((hist["Close"].iloc[-1] / hist["Close"].iloc[0] - 1) * 100),
                }
        except Exception:
            pass
    return result
