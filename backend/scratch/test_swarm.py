
import asyncio
from app.graph import swarm_graph

async def test_swarm():
    initial_state = {
        "ticker": "AAPL",
        "hold_period": "3m",
        "risk_tolerance": "moderate",
        "agent_outputs": {},
        "agent_statuses": [],
        "final_score": 0.0,
        "final_rating": "HOLD",
        "final_summary": "",
        "report": {},
        "errors": [],
    }
    
    print("🚀 Starting Swarm Analysis for AAPL...")
    result = swarm_graph.invoke(initial_state)
    
    print("\n--- RESULTS ---")
    print(f"Ticker: {result.get('ticker')}")
    print(f"Final Score: {result.get('final_score')}")
    print(f"Final Rating: {result.get('final_rating')}")
    print(f"Report Keys: {list(result.get('report', {}).keys())}")
    
    if "final_rating" in result.get("report", {}):
        print(f"Report Rating: {result['report']['final_rating']}")
    else:
        print("❌ CRITICAL: final_rating missing from report object!")

if __name__ == "__main__":
    asyncio.run(test_swarm())
