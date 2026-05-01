"""
Agent #15: Report Generator — formats output into wealth-management-grade report.
"""

from typing import Any
from datetime import datetime

from app.agents.base import BaseAgent


class ReportGeneratorAgent(BaseAgent):
    name = "report_generator"
    description = "Formats the final output into a wealth-management-grade report with chart configs."

    def execute(self, state: dict[str, Any]) -> dict[str, Any]:
        ticker = state.get("ticker", "N/A")
        hold_period = state.get("hold_period", "3m")
        agent_outputs = state.get("agent_outputs", {})
        final_score = state.get("final_score", 50)
        final_rating = state.get("final_rating", "HOLD")
        final_summary = state.get("final_summary", "")

        # Build gauge chart config
        gauge_config = {
            "type": "gauge",
            "score": final_score,
            "min": 0,
            "max": 100,
            "zones": [
                {"min": 0, "max": 25, "color": "#ff3366", "label": "STRONG SELL"},
                {"min": 25, "max": 40, "color": "#ff6b35", "label": "SELL"},
                {"min": 40, "max": 60, "color": "#ffaa00", "label": "HOLD"},
                {"min": 60, "max": 75, "color": "#00cc88", "label": "BUY"},
                {"min": 75, "max": 100, "color": "#00ff88", "label": "STRONG BUY"},
            ],
        }

        # Build agent signal breakdown for visualization
        agent_breakdown = []
        for name, output in agent_outputs.items():
            if isinstance(output, dict) and "score" in output:
                agent_breakdown.append({
                    "name": name.replace("_", " ").title(),
                    "score": output.get("score", 50),
                    "signal": output.get("signal", "neutral"),
                    "confidence": output.get("confidence", 0.5),
                    "summary": output.get("summary", "")[:200],
                    "key_findings": output.get("key_findings", [])[:5],
                })

        # Build risk/reward matrix data
        risk_data = agent_outputs.get("risk_optimization_agent", {}).get("data", {})

        # Extract insider trading highlights
        insider_data = agent_outputs.get("insider_trading_agent", {}).get("data", {})

        # Extract flow analysis data
        options_data = agent_outputs.get("options_flow_agent", {}).get("data", {})
        darkpool_data = agent_outputs.get("dark_pool_monitor", {}).get("data", {})

        # Citations / Sources
        citations = [
            {"source": "SEC EDGAR", "type": "Regulatory", "link": f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={ticker}"},
            {"source": "Yahoo Finance", "type": "Market Data", "link": f"https://finance.yahoo.com/quote/{ticker}"},
            {"source": "Dark Pool Index", "type": "Liquidity", "link": "#"},
            {"source": "Institutional Swarm", "type": "AI Synthesis", "link": "#"},
        ]

        report = {
            "ticker": ticker,
            "hold_period": hold_period,
            "timestamp": datetime.now().isoformat(),
            "final_score": final_score,
            "final_rating": final_rating,
            "final_summary": final_summary,
            "detailed_breakdown": agent_outputs.get("grand_synthesizer", {}).get("data", {}).get("detailed_report", final_summary),
            "citations": citations,
            "gauge_config": gauge_config,
            "agent_breakdown": agent_breakdown,
            "risk_metrics": {
                "kelly_fraction": risk_data.get("adjusted_kelly_fraction", 0),
                "position_size": risk_data.get("position_size_usd", 0),
                "sharpe_ratio": risk_data.get("sharpe_ratio", 0),
                "var_95": risk_data.get("var_95_usd", 0),
                "max_drawdown": risk_data.get("max_drawdown_pct", 0),
            },
            "insider_highlights": {
                "form4_count": len(insider_data.get("form4_filings", [])),
                "congressional_count": len(insider_data.get("congressional_trades", [])),
                "net_sentiment": insider_data.get("net_insider_sentiment", "neutral"),
                "filings": insider_data.get("form4_filings", [])[:5],
                "congressional": insider_data.get("congressional_trades", [])[:3],
            },
            "flow_analysis": {
                "put_call_ratio": options_data.get("put_call_ratio", 0),
                "unusual_trades": options_data.get("unusual_trades", [])[:5],
                "dark_pool_pct": darkpool_data.get("dark_pool_pct", 0),
                "institutional_bias": darkpool_data.get("institutional_bias", "neutral"),
            },
            "technical_charts": {
                "price_data": tech_data.get("chart_data", {}),
                "rsi": tech_data.get("rsi", 50),
                "macd": tech_data.get("macd", {}),
                "bollinger": tech_data.get("bollinger", {}),
            },
        }

        return {
            "agent_outputs": {
                self.name: {
                    "agent_name": self.name,
                    "confidence": 1.0,
                    "signal": "neutral",
                    "score": final_score,
                    "summary": f"Deep analysis report generated for {ticker}.",
                    "data": {},
                    "key_findings": [f"Final Score: {final_score}", f"Rating: {final_rating}"],
                }
            },
            "report": report,
        }
