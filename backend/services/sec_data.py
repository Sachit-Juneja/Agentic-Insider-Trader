"""
SEC Data Service — EDGAR Form 4 and institutional holdings.
"""

import httpx
from typing import Any

from app.config import settings

SEC_BASE = "https://efts.sec.gov/LATEST/search-index"
EDGAR_BASE = "https://data.sec.gov"


async def get_insider_trades(ticker: str) -> list[dict[str, Any]]:
    """Fetch Form 4 insider trading filings from SEC EDGAR."""
    headers = {"User-Agent": settings.sec_user_agent}
    url = f"{EDGAR_BASE}/cgi-bin/browse-edgar?action=getcompany&company={ticker}&type=4&dateb=&owner=include&count=20&search_text=&action=getcompany"

    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(url, headers=headers, timeout=10)
            # In production: parse the HTML/XML response
            # For now, return empty — agents use mock data
            return []
    except Exception as e:
        print(f"[SEC] Error fetching insider trades for {ticker}: {e}")
        return []


async def get_institutional_holdings(ticker: str) -> list[dict[str, Any]]:
    """Fetch 13F institutional holdings data."""
    # Placeholder — would use SEC EDGAR 13F filings
    return []


async def get_financial_statements(ticker: str) -> dict[str, Any]:
    """Fetch 10-K/10-Q financial statement data."""
    # Placeholder — would parse XBRL from EDGAR
    return {}
