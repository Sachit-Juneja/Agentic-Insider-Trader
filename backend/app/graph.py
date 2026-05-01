"""
LangGraph State Graph — orchestrates the 15-agent swarm with parallel execution.
"""

from langgraph.graph import StateGraph, START, END

from app.models import SwarmState
from app.agents.user_proxy import UserProxyAgent
from app.agents.macro import MacroAgent
from app.agents.geopolitical import GeopoliticalAgent
from app.agents.market_regime import MarketRegimeAgent
from app.agents.technical import TechnicalAnalystAgent
from app.agents.options_flow import OptionsFlowAgent
from app.agents.dark_pool import DarkPoolAgent
from app.agents.fundamental import FundamentalAgent
from app.agents.sector_comparator import SectorComparatorAgent
from app.agents.insider_trading import InsiderTradingAgent
from app.agents.media_sentiment import MediaSentimentAgent
from app.agents.social_scraper import SocialScraperAgent
from app.agents.risk_optimization import RiskOptimizationAgent
from app.agents.grand_synthesizer import GrandSynthesizerAgent
from app.agents.report_generator import ReportGeneratorAgent


# ─── Instantiate Agents ──────────────────────────────────────────────────────

user_proxy = UserProxyAgent()
macro = MacroAgent()
geopolitical = GeopoliticalAgent()
market_regime = MarketRegimeAgent()
technical = TechnicalAnalystAgent()
options_flow = OptionsFlowAgent()
dark_pool = DarkPoolAgent()
fundamental = FundamentalAgent()
sector_comp = SectorComparatorAgent()
insider = InsiderTradingAgent()
media = MediaSentimentAgent()
social = SocialScraperAgent()
risk_opt = RiskOptimizationAgent()
synthesizer = GrandSynthesizerAgent()
report_gen = ReportGeneratorAgent()


# ─── Node Functions (wrappers around agent.run) ─────────────────────────────

def node_user_proxy(state: SwarmState) -> dict:
    return user_proxy.run(state)

def node_macro(state: SwarmState) -> dict:
    return macro.run(state)

def node_geopolitical(state: SwarmState) -> dict:
    return geopolitical.run(state)

def node_market_regime(state: SwarmState) -> dict:
    return market_regime.run(state)

def node_technical(state: SwarmState) -> dict:
    return technical.run(state)

def node_options_flow(state: SwarmState) -> dict:
    return options_flow.run(state)

def node_dark_pool(state: SwarmState) -> dict:
    return dark_pool.run(state)

def node_fundamental(state: SwarmState) -> dict:
    return fundamental.run(state)

def node_sector_comp(state: SwarmState) -> dict:
    return sector_comp.run(state)

def node_insider(state: SwarmState) -> dict:
    return insider.run(state)

def node_media(state: SwarmState) -> dict:
    return media.run(state)

def node_social(state: SwarmState) -> dict:
    return social.run(state)

def node_risk_opt(state: SwarmState) -> dict:
    return risk_opt.run(state)

def node_synthesizer(state: SwarmState) -> dict:
    return synthesizer.run(state)

def node_report_gen(state: SwarmState) -> dict:
    return report_gen.run(state)


# ─── Build the Graph ─────────────────────────────────────────────────────────

def build_swarm_graph() -> StateGraph:
    """Build and compile the LangGraph swarm pipeline."""

    builder = StateGraph(SwarmState)

    # Add all nodes
    builder.add_node("user_proxy", node_user_proxy)

    # Tier 1: Context Agents (parallel)
    builder.add_node("macro", node_macro)
    builder.add_node("geopolitical", node_geopolitical)
    builder.add_node("market_regime", node_market_regime)

    # Tier 2: Quant Agents (parallel)
    builder.add_node("technical", node_technical)
    builder.add_node("options_flow", node_options_flow)
    builder.add_node("dark_pool", node_dark_pool)

    # Tier 3: Fundamentals & Sentiment (parallel)
    builder.add_node("fundamental", node_fundamental)
    builder.add_node("sector_comp", node_sector_comp)
    builder.add_node("insider", node_insider)
    builder.add_node("media", node_media)
    builder.add_node("social", node_social)

    # Synthesis (sequential)
    builder.add_node("risk_opt", node_risk_opt)
    builder.add_node("synthesizer", node_synthesizer)
    builder.add_node("report_gen", node_report_gen)

    # ─── Edges ────────────────────────────────────────────────────────────

    # START -> User Proxy
    builder.add_edge(START, "user_proxy")

    # User Proxy fans out to ALL data agents (parallel execution)
    # Tier 1
    builder.add_edge("user_proxy", "macro")
    builder.add_edge("user_proxy", "geopolitical")
    builder.add_edge("user_proxy", "market_regime")
    # Tier 2
    builder.add_edge("user_proxy", "technical")
    builder.add_edge("user_proxy", "options_flow")
    builder.add_edge("user_proxy", "dark_pool")
    # Tier 3
    builder.add_edge("user_proxy", "fundamental")
    builder.add_edge("user_proxy", "sector_comp")
    builder.add_edge("user_proxy", "insider")
    builder.add_edge("user_proxy", "media")
    builder.add_edge("user_proxy", "social")

    # All data agents fan in to risk_opt (LangGraph auto-waits for all)
    builder.add_edge("macro", "risk_opt")
    builder.add_edge("geopolitical", "risk_opt")
    builder.add_edge("market_regime", "risk_opt")
    builder.add_edge("technical", "risk_opt")
    builder.add_edge("options_flow", "risk_opt")
    builder.add_edge("dark_pool", "risk_opt")
    builder.add_edge("fundamental", "risk_opt")
    builder.add_edge("sector_comp", "risk_opt")
    builder.add_edge("insider", "risk_opt")
    builder.add_edge("media", "risk_opt")
    builder.add_edge("social", "risk_opt")

    # Sequential synthesis
    builder.add_edge("risk_opt", "synthesizer")
    builder.add_edge("synthesizer", "report_gen")
    builder.add_edge("report_gen", END)

    return builder.compile()


# Compile the graph once at module level
swarm_graph = build_swarm_graph()
