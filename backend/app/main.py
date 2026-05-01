"""
FastAPI main application — REST + SSE endpoints for the agent swarm.
"""

import asyncio
import json
import uuid
import math
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, BackgroundTasks

def safe_json_dumps(obj: Any) -> str:
    """JSON dumps that replaces NaN/Inf with None."""
    def clean(o):
        if isinstance(o, float):
            if math.isnan(o) or math.isinf(o):
                return None
        elif isinstance(o, dict):
            return {k: clean(v) for k, v in o.items()}
        elif isinstance(o, (list, tuple)):
            return [clean(i) for i in o]
        return o
    return json.dumps(clean(obj))
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse

from app.config import settings
from app.models import AnalysisRequest, AnalysisReport

# ─── App Setup ────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Agentic Insider Trader API",
    description="16-Agent Stock Analysis Swarm",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory job store (production: use Redis)
jobs: dict[str, dict[str, Any]] = {}


# ─── Helper: Run swarm in background ─────────────────────────────────────────

async def run_swarm(job_id: str, request: AnalysisRequest):
    """Execute the agent swarm and store results."""
    from app.graph import swarm_graph

    jobs[job_id]["status"] = "running"
    jobs[job_id]["started_at"] = datetime.now().isoformat()

    try:
        initial_state = {
            "ticker": request.ticker.upper(),
            "hold_period": request.hold_period,
            "risk_tolerance": request.risk_tolerance.value,
            "agent_outputs": {},
            "agent_statuses": [],
            "final_score": 0.0,
            "final_rating": "HOLD",
            "final_summary": "",
            "report": {},
            "errors": [],
        }

        # Run the graph (blocking — wrapped in executor for async)
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None,
            lambda: swarm_graph.invoke(initial_state)
        )

        jobs[job_id]["status"] = "complete"
        jobs[job_id]["result"] = result
        jobs[job_id]["completed_at"] = datetime.now().isoformat()

    except Exception as e:
        jobs[job_id]["status"] = "error"
        jobs[job_id]["error"] = str(e)
        jobs[job_id]["completed_at"] = datetime.now().isoformat()


# ─── Endpoints ────────────────────────────────────────────────────────────────

@app.get("/")
async def root():
    return {
        "name": "Agentic Insider Trader API",
        "version": "1.0.0",
        "status": "operational",
        "agents": 16,
    }


@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


@app.post("/api/analyze")
async def start_analysis(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """Start a new analysis job. Returns a job_id for polling/streaming."""
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "job_id": job_id,
        "status": "queued",
        "request": request.model_dump(),
        "created_at": datetime.now().isoformat(),
        "result": None,
        "error": None,
    }

    background_tasks.add_task(run_swarm, job_id, request)

    return {"job_id": job_id, "status": "queued", "ticker": request.ticker.upper()}


@app.get("/api/analyze/{job_id}/status")
async def get_job_status(job_id: str):
    """Get the current status of an analysis job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]
    response = {
        "job_id": job_id,
        "status": job["status"],
        "created_at": job.get("created_at"),
    }

    if job["status"] == "complete" and job["result"]:
        result = job["result"]
        response["agent_statuses"] = result.get("agent_statuses", [])

    if job["status"] == "error":
        response["error"] = job.get("error")

    return response


@app.get("/api/analyze/{job_id}/result")
async def get_job_result(job_id: str):
    """Get the full result of a completed analysis job."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = jobs[job_id]

    if job["status"] != "complete":
        return {"job_id": job_id, "status": job["status"], "message": "Analysis not yet complete"}

    result = job["result"]
    return {
        "job_id": job_id,
        "status": "complete",
        "report": result.get("report", {}),
        "agent_statuses": result.get("agent_statuses", []),
        "errors": result.get("errors", []),
    }


@app.get("/api/analyze/{job_id}/stream")
async def stream_analysis(job_id: str):
    """SSE endpoint for real-time agent status updates."""
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    async def event_generator():
        last_status_count = 0
        while True:
            job = jobs.get(job_id)
            if not job:
                break

            # Send new agent statuses
            if job["status"] in ("running", "complete") and job.get("result"):
                statuses = job["result"].get("agent_statuses", [])
                if len(statuses) > last_status_count:
                    for status in statuses[last_status_count:]:
                        yield f"data: {safe_json_dumps({'type': 'agent_status', 'data': status})}\n\n"
                    last_status_count = len(statuses)

            # Send completion event
            if job["status"] == "complete":
                report = job["result"].get("report", {})
                yield f"data: {safe_json_dumps({'type': 'complete', 'data': report})}\n\n"
                break
            elif job["status"] == "error":
                yield f"data: {safe_json_dumps({'type': 'error', 'data': {'error': job.get('error', 'Unknown error')}})}\n\n"
                break

            await asyncio.sleep(0.5)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )

@app.get("/api/weekly-picks")
async def get_weekly_picks():
    """Get the top stock picks for the current week based on swarm intelligence."""
    # In a real app, this would be computed by a dedicated scanner agent.
    picks = [
        {
            "ticker": "NVDA",
            "rating": "STRONG BUY",
            "score": 94,
            "predicted_increase": "+8.5%",
            "reason": "Institutional dark pool accumulation reaching 12-month highs ahead of Blackwell production ramp. Technical confluence at $118 support.",
            "confidence": 0.92,
            "catalysts": ["Blackwell ramp", "Data center demand", "Dark pool flow"]
        },
        {
            "ticker": "AMD",
            "rating": "BUY",
            "score": 78,
            "predicted_increase": "+5.2%",
            "reason": "MI300X software ecosystem parity improving. Oversold on daily RSI with bullish divergence in options flow (call premium bias).",
            "confidence": 0.85,
            "catalysts": ["MI300X sales", "Market share gains", "Technical bounce"]
        },
        {
            "ticker": "AAPL",
            "rating": "BUY",
            "score": 82,
            "predicted_increase": "+4.1%",
            "reason": "AI-driven replacement cycle coming into focus. Strong institutional support in options chain for $225 strikes.",
            "confidence": 0.88,
            "catalysts": ["iPhone 16 AI", "Service growth", "Buyback program"]
        },
        {
            "ticker": "GOOGL",
            "rating": "BUY",
            "score": 86,
            "predicted_increase": "+6.3%",
            "reason": "Cloud revenue acceleration + Gemini integration tailwinds. Significant insider accumulation detected in dark pool signatures.",
            "confidence": 0.89,
            "catalysts": ["Cloud growth", "AI integration", "Institutional accumulation"]
        }
    ]
    return {"timestamp": datetime.now().isoformat(), "picks": picks}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
