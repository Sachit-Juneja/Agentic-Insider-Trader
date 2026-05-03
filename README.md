# Agentic Insider Trader

> A 16-agent AI swarm that analyzes stocks from every conceivable angle. Built different.

## What Is This?

A full-stack stock analysis platform that deploys a **massive multi-agent swarm** to analyze any ticker. 16 specialized AI agents work in parallel — from macro economics to Reddit sentiment to dark pool flows — then a Grand Synthesizer agent resolves conflicts and delivers a final verdict.

Think Bloomberg Terminal meets r/wallstreetbets meets Skynet.

## Architecture

- **Frontend:** Next.js 14 + Tailwind CSS + Shadcn UI — looks like an institutional wealth management terminal
- **Backend:** FastAPI + LangGraph — orchestrates 16 concurrent AI agents
- **LLM:** OpenAI GPT-4o for agent reasoning
- **Data:** yfinance, SEC EDGAR, news APIs, social sentiment

## The 16 Agents

| # | Agent | Role |
|---|-------|------|
| 1 | User Proxy | Parses request, dispatches swarm |
| 2 | Macroeconomic | CPI, Fed rates, yield curve |
| 3 | Geopolitical Risk | Global events, tariffs, supply chains |
| 4 | Market Regime | VIX, SPY trends, bull/bear classification |
| 5 | Technical Analyst | RSI, MACD, Bollinger Bands, moving averages |
| 6 | Options Flow | Unusual activity, gamma exposure, P/C ratios |
| 7 | Dark Pool Monitor | Institutional blocks, off-exchange volumes |
| 8 | Fundamental | SEC filings, P/E, debt-to-equity |
| 9 | Sector Comparator | Peer benchmarking |
| 10 | Insider Trading | SEC Form 4s, Congressional trades |
| 11 | Media Sentiment | Bloomberg, WSJ, CNBC headlines |
| 12 | Social Scraper | Reddit, X/Twitter, StockTwits |
| 13 | Risk & Optimization | Kelly Criterion, position sizing |
| 14 | Grand Synthesizer | Conflict resolution, final 0-100 score |
| 15 | Report Generator | Wealth-management-grade reports |
| 16 | Git-Ops Committer | Auto-commits with unhinged messages |

## Quick Start

```bash
# Backend
cd backend
pip install -r requirements.txt
cp .env.example .env  # Add your OpenAI API key
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

## Disclaimer

This is for educational and entertainment purposes only. Not financial advice. The "Insider Trading Agent" analyzes *publicly available* SEC filings — we are not actually insider trading. SEC, please don't come for us.

## License

MIT — do whatever you want with it, just don't blame us if you lose money.
