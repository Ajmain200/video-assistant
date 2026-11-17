from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from models.schemas import (
    CreateJobRequest,
    CreateJobResponse,
    JobStatusResponse,
    ChatRequest,
    ChatResponse,
)
from jobs.job_manager import create_job, get_job, chat_with_job

app = FastAPI(title="AI Video Assistant API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/jobs", response_model=CreateJobResponse)
def create_job_endpoint(payload: CreateJobRequest):
    if not payload.source.strip():
        raise HTTPException(status_code=400, detail="source is required")
    if payload.language not in ("english"):
        raise HTTPException(status_code=400, detail="language must be 'english' or 'bangla'")

    job = create_job(payload.source.strip(), payload.language)
    return CreateJobResponse(job_id=job.job_id)


@app.get("/api/jobs/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    return job.to_dict()


@app.post("/api/jobs/{job_id}/chat", response_model=ChatResponse)
def chat_endpoint(job_id: str, payload: ChatRequest):
    job = get_job(job_id)
    if job is None:
        raise HTTPException(status_code=404, detail="job not found")
    if not payload.question.strip():
        raise HTTPException(status_code=400, detail="question is required")

    try:
        answer, sources = chat_with_job(job, payload.question.strip())
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    return ChatResponse(answer=answer, sources=sources)
