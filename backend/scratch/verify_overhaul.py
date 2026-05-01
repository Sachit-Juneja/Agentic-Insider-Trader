
import asyncio
import os
import sys
from dotenv import load_dotenv

# Add parent dir to path
sys.path.append(os.getcwd())

from app.graph import swarm_graph

async def test():
    load_dotenv()
    state = {
        "ticker": "TSLA",
        "hold_period": "3m",
        "risk_tolerance": "moderate",
        "agent_outputs": {},
        "agent_statuses": []
    }
    print("🚀 Starting Swarm Execution...")
    result = await swarm_graph.ainvoke(state)
    print(f"\n--- STATE KEYS ---")
    print(result.keys())
    print(f"Errors: {result.get('errors', [])}")
    
    report = result.get("report", {})
    print("\n--- REPORT KEYS ---")
    print(report.keys())
    
    print(f"\nCitations Count: {len(report.get('citations', []))}")
    print(f"Detailed Breakdown present: {bool(report.get('detailed_breakdown'))}")

if __name__ == "__main__":
    asyncio.run(test())
