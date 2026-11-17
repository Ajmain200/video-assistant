
import json
import re
from typing import List

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import settings
from core.summarizer import _truncate

_SYSTEM = (
    "You extract structured information from meeting/video transcripts. "
    "Respond ONLY with a JSON array of strings — no prose, no markdown fences, "
    "no keys, just a JSON array. Each string should be one concise item. "
    "If there are none, respond with an empty array []."
)


def _llm() -> ChatMistralAI:
    return ChatMistralAI(
        api_key=settings.MISTRAL_API_KEY,
        model=settings.MISTRAL_CHAT_MODEL,
        temperature=0.1,
    )


def _extract_list(transcript: str, instruction: str) -> List[str]:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", _SYSTEM),
            ("human", f"{instruction}\n\nTranscript:\n\n{{transcript}}\n\nJSON array:"),
        ]
    )
    chain = prompt | _llm() | StrOutputParser()
    raw = chain.invoke({"transcript": _truncate(transcript)}).strip()

    
    raw = re.sub(r"^```(json)?", "", raw.strip())
    raw = re.sub(r"```$", "", raw.strip()).strip()

    try:
        items = json.loads(raw)
        if isinstance(items, list):
            return [str(item).strip() for item in items if str(item).strip()]
    except json.JSONDecodeError:
        pass

    
    return [line.strip("-• ").strip() for line in raw.splitlines() if line.strip()]


def extract_action_items(transcript: str) -> List[str]:
    return _extract_list(
        transcript,
        "List all concrete action items or tasks mentioned, phrased as short actionable statements.",
    )


def extract_key_decisions(transcript: str) -> List[str]:
    return _extract_list(
        transcript,
        "List the key decisions that were made or agreed upon.",
    )


def extract_questions(transcript: str) -> List[str]:
    return _extract_list(
        transcript,
        "List any open or unresolved questions raised that don't yet have an answer.",
    )
