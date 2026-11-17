
import threading
import traceback
import uuid
from typing import Dict, Optional

from core.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.rag_engine import build_rag_chain, ask_question


class Job:
    def __init__(self, job_id: str, source: str, language: str):
        self.job_id = job_id
        self.source = source
        self.language = language
        self.status = "queued"  
        self.steps = {
            "audio": "pending",
            "transcript": "pending",
            "title": "pending",
            "summary": "pending",
            "extract": "pending",
            "rag": "pending",
        }
        self.error: Optional[str] = None
        self.result: Dict = {}
        self.vectorstore = None  

    def to_dict(self):
        return {
            "job_id": self.job_id,
            "status": self.status,
            "steps": self.steps,
            "error": self.error,
            "result": {
                "title": self.result.get("title"),
                "transcript": self.result.get("transcript"),
                "summary": self.result.get("summary"),
                "action_items": self.result.get("action_items"),
                "key_decisions": self.result.get("key_decisions"),
                "open_questions": self.result.get("open_questions"),
            }
            if self.result
            else None,
        }


_jobs: Dict[str, Job] = {}
_lock = threading.Lock()


def create_job(source: str, language: str) -> Job:
    job_id = uuid.uuid4().hex[:12]
    job = Job(job_id, source, language)
    with _lock:
        _jobs[job_id] = job
    thread = threading.Thread(target=_run_pipeline, args=(job,), daemon=True)
    thread.start()
    return job


def get_job(job_id: str) -> Optional[Job]:
    return _jobs.get(job_id)


def _run_pipeline(job: Job):
    job.status = "running"
    try:
        job.steps["audio"] = "active"
        chunks = process_input(job.source, job.job_id)
        job.steps["audio"] = "done"

        job.steps["transcript"] = "active"
        transcript = transcribe_all(chunks, job.language)
        job.result["transcript"] = transcript
        job.steps["transcript"] = "done"

        job.steps["title"] = "active"
        job.result["title"] = generate_title(transcript)
        job.steps["title"] = "done"

        job.steps["summary"] = "active"
        job.result["summary"] = summarize(transcript)
        job.steps["summary"] = "done"

        job.steps["extract"] = "active"
        job.result["action_items"] = extract_action_items(transcript)
        job.result["key_decisions"] = extract_key_decisions(transcript)
        job.result["open_questions"] = extract_questions(transcript)
        job.steps["extract"] = "done"

        job.steps["rag"] = "active"
        job.vectorstore = build_rag_chain(transcript, job.job_id)
        job.steps["rag"] = "done"

        job.status = "done"
    except Exception as e:
        job.status = "error"
        job.error = f"{e}"
        traceback.print_exc()
        for key, state in job.steps.items():
            if state == "active":
                job.steps[key] = "pending"


def chat_with_job(job: Job, question: str):
    if job.vectorstore is None:
        raise ValueError("This job's RAG index isn't ready yet.")
    return ask_question(job.vectorstore, question)
