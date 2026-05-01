"""
FastAPI main application — REST + SSE endpoints for the agent swarm.
"""

import asyncio
import json
import uuid
from datetime import datetime
from typing import Any

from fastapi import FastAPI, HTTPException, BackgroundTasks
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
                        yield f"data: {json.dumps({'type': 'agent_status', 'data': status})}\n\n"
                    last_status_count = len(statuses)

            # Send completion event
            if job["status"] == "complete":
                report = job["result"].get("report", {})
                yield f"data: {json.dumps({'type': 'complete', 'data': report})}\n\n"
                break
            elif job["status"] == "error":
                yield f"data: {json.dumps({'type': 'error', 'data': {'error': job.get('error', 'Unknown error')}})}\n\n"
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


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port)
