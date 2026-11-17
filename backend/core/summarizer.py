
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from config import settings

MAX_CHARS = 12000  


def _llm(temperature: float = 0.3) -> ChatMistralAI:
    return ChatMistralAI(
        api_key=settings.MISTRAL_API_KEY,
        model=settings.MISTRAL_CHAT_MODEL,
        temperature=temperature,
    )


def _truncate(text: str) -> str:
    return text if len(text) <= MAX_CHARS else text[:MAX_CHARS] + "\n...[truncated]"


def generate_title(transcript: str) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You write short, specific titles for meeting/video transcripts. "
                       "Respond with the title only, no quotes, no punctuation at the end, "
                       "max 10 words."),
            ("human", "Transcript:\n\n{transcript}\n\nTitle:"),
        ]
    )
    chain = prompt | _llm(temperature=0.4) | StrOutputParser()
    return chain.invoke({"transcript": _truncate(transcript)}).strip().strip('"')


def summarize(transcript: str) -> str:
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", "You are an expert meeting/video summarizer. Produce a clear, "
                       "well-organized summary using short paragraphs and, where useful, "
                       "bullet points. Cover the main topics, outcomes, and context. "
                       "Do not invent information that isn't in the transcript."),
            ("human", "Transcript:\n\n{transcript}\n\nSummary:"),
        ]
    )
    chain = prompt | _llm(temperature=0.3) | StrOutputParser()
    return chain.invoke({"transcript": _truncate(transcript)}).strip()
