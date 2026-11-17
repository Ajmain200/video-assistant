from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class CreateJobRequest(BaseModel):
    source: str = Field(..., description="YouTube URL (local file paths not accepted over the API)")
    language: str = Field("english", description="'english' or 'bangla'")


class CreateJobResponse(BaseModel):
    job_id: str


class StepStatus(BaseModel):
    audio: str = "pending"
    transcript: str = "pending"
    title: str = "pending"
    summary: str = "pending"
    extract: str = "pending"
    rag: str = "pending"


class JobResult(BaseModel):
    title: Optional[str] = None
    transcript: Optional[str] = None
    summary: Optional[str] = None
    action_items: Optional[List[str]] = None
    key_decisions: Optional[List[str]] = None
    open_questions: Optional[List[str]] = None


class JobStatusResponse(BaseModel):
    job_id: str
    status: str  
    steps: StepStatus
    error: Optional[str] = None
    result: Optional[JobResult] = None


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
    sources: Optional[List[str]] = None
