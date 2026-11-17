
from typing import List

import whisper

from config import settings

_model = None


def _get_model():
    global _model
    if _model is None:
        _model = whisper.load_model(settings.WHISPER_MODEL)
    return _model


def transcribe_chunk(chunk_path: str, language: str) -> str:
    model = _get_model()

    if language == "bangla":
        result = model.transcribe(chunk_path, task="translate")
    else:
        result = model.transcribe(chunk_path, task="transcribe", language="en")

    return result.get("text", "").strip()


def transcribe_all(chunk_paths: List[str], language: str = "english") -> str:
    parts = []
    for path in chunk_paths:
        text = transcribe_chunk(path, language)
        if text:
            parts.append(text)
    return "\n".join(parts).strip()
