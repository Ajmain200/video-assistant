
import os
from typing import Tuple, List

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.documents import Document

from config import settings

_embeddings = None


def _get_embeddings() -> HuggingFaceEmbeddings:
    global _embeddings
    if _embeddings is None:
        _embeddings = HuggingFaceEmbeddings(model_name=settings.EMBEDDING_MODEL)
    return _embeddings


def build_rag_chain(transcript: str, job_id: str) -> Chroma:
   
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.RAG_CHUNK_SIZE,
        chunk_overlap=settings.RAG_CHUNK_OVERLAP,
    )
    docs: List[Document] = splitter.create_documents([transcript])

    persist_dir = os.path.join(settings.CHROMA_DIR, job_id)
    os.makedirs(persist_dir, exist_ok=True)

    vectorstore = Chroma(
        collection_name=f"job_{job_id}",
        embedding_function=_get_embeddings(),
        persist_directory=persist_dir,
    )
    if docs:
        vectorstore.add_documents(docs)

    return vectorstore


def ask_question(vectorstore: Chroma, question: str, k: int = 4) -> Tuple[str, List[str]]:
   
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    relevant_docs = retriever.invoke(question)
    context = "\n\n---\n\n".join(d.page_content for d in relevant_docs)

    prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You answer questions about a video/meeting transcript using ONLY the "
                "provided context. If the answer isn't in the context, say you don't "
                "have enough information from the transcript to answer. Be concise.",
            ),
            ("human", "Context:\n\n{context}\n\nQuestion: {question}\n\nAnswer:"),
        ]
    )
    llm = ChatMistralAI(
        api_key=settings.MISTRAL_API_KEY,
        model=settings.MISTRAL_CHAT_MODEL,
        temperature=0.2,
    )
    chain = prompt | llm | StrOutputParser()
    answer = chain.invoke({"context": context, "question": question}).strip()

    sources = [d.page_content[:200] + ("..." if len(d.page_content) > 200 else "") for d in relevant_docs]
    return answer, sources
