"""FastAPI server for CultureBridge — AI Cultural Consultant Engine."""

import asyncio
import json
import logging
import os
import time
import uuid
from typing import AsyncGenerator

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.config import validate_config
from backend.pipeline import PipelineEvent, run_pipeline

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("culturebridge")

validate_config()

app = FastAPI(
    title="CultureBridge",
    description="AI Cultural Consultant for Chinese Content Going Global",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

jobs: dict = {}


class CreateTaskRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=50000)
    content_type: str = Field(default="drama", pattern="^(drama|novel|game)$")
    target_lang: str = Field(default="en", pattern="^(en|ja|ko)$")
    target_market: str = Field(default="us", pattern="^(us|sea|jp|kr|eu|mena)$")


@app.post("/api/create")
async def create_task(req: CreateTaskRequest):
    job_id = str(uuid.uuid4())[:8]
    logger.info(
        "Job %s: created (type=%s, lang=%s, market=%s, len=%d)",
        job_id,
        req.content_type,
        req.target_lang,
        req.target_market,
        len(req.content),
    )
    jobs[job_id] = {
        "status": "pending",
        "progress": 0.0,
        "events": [],
        "output": None,
        "error": None,
        "created_at": time.time(),
    }
    asyncio.get_event_loop().run_in_executor(
        None,
        _run_job,
        job_id,
        req.content,
        req.content_type,
        req.target_lang,
        req.target_market,
    )
    return {"job_id": job_id}


@app.post("/api/create-srt")
async def create_task_srt(
    file: UploadFile = File(...),
    content_type: str = Form(default="drama"),
    target_lang: str = Form(default="en"),
    target_market: str = Form(default="us"),
):
    """Create task from SRT subtitle file upload."""
    raw = await file.read()
    content = raw.decode("utf-8-sig")
    job_id = str(uuid.uuid4())[:8]
    logger.info(
        "Job %s: created from SRT (type=%s, lang=%s)", job_id, content_type, target_lang
    )
    jobs[job_id] = {
        "status": "pending",
        "progress": 0.0,
        "events": [],
        "output": None,
        "error": None,
        "created_at": time.time(),
        "input_format": "srt",
    }
    asyncio.get_event_loop().run_in_executor(
        None,
        _run_job,
        job_id,
        content,
        content_type,
        target_lang,
        target_market,
    )
    return {"job_id": job_id}


def _run_job(
    job_id: str, content: str, content_type: str, target_lang: str, target_market: str
):
    jobs[job_id]["status"] = "running"
    start_time = time.time()

    def on_event(event: PipelineEvent):
        jobs[job_id]["progress"] = event.progress
        jobs[job_id]["events"].append(
            {
                "stage": event.stage,
                "message": event.message,
                "progress": event.progress,
                "data": event.data,
                "timestamp": event.timestamp,
            }
        )

    try:
        result = run_pipeline(
            content=content,
            content_type=content_type,
            target_lang=target_lang,
            target_market=target_market,
            on_event=on_event,
            job_id=job_id,
        )
        jobs[job_id]["status"] = "completed"
        jobs[job_id]["progress"] = 1.0
        jobs[job_id]["output"] = result.get("output", {})
        elapsed = time.time() - start_time
        logger.info("Job %s: completed in %.1fs", job_id, elapsed)
    except Exception as e:
        jobs[job_id]["status"] = "failed"
        jobs[job_id]["error"] = str(e)
        elapsed = time.time() - start_time
        logger.error(
            "Job %s: failed after %.1fs: %s", job_id, elapsed, e, exc_info=True
        )


@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")
    return jobs[job_id]


@app.get("/api/stream/{job_id}")
async def stream_events(job_id: str):
    if job_id not in jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    async def event_generator() -> AsyncGenerator[str, None]:
        last_idx = 0
        while True:
            job = jobs[job_id]
            events = job["events"]
            while last_idx < len(events):
                yield f"data: {json.dumps(events[last_idx], ensure_ascii=False)}\n\n"
                last_idx += 1
            if job["status"] in ("completed", "failed"):
                final = {
                    "stage": "done",
                    "message": "全部完成"
                    if job["status"] == "completed"
                    else f"失败: {job['error']}",
                    "progress": job["progress"],
                    "data": {"status": job["status"]},
                }
                yield f"data: {json.dumps(final, ensure_ascii=False)}\n\n"
                break
            await asyncio.sleep(1)

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )


@app.get("/api/health")
async def health():
    return {"status": "ok", "service": "CultureBridge"}


_frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.isdir(_frontend_dir):
    app.mount("/", StaticFiles(directory=_frontend_dir, html=True), name="frontend")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
