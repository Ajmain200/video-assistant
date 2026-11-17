# AI Video Assistant

Paste a YouTube link, get a transcript, title, summary, action items, key
decisions, open questions — and chat with the video via RAG.

**Stack**
- Backend: FastAPI + LangChain, Mistral AI (free-tier chat model) for
  summarization/extraction/Q&A, local OpenAI Whisper for transcription,
  ChromaDB + local HuggingFace embeddings for RAG.
- Frontend: React (Vite) + Tailwind CSS.

## Architecture

```
YouTube URL → yt-dlp (download audio) → pydub (chunk audio)
            → Whisper (transcribe/translate chunks) → full transcript
            → Mistral: title, summary, action items, decisions, questions
            → Chroma + HuggingFace embeddings (index transcript for RAG)
            → chat: retrieve relevant chunks → Mistral answers
```

The backend runs each job in a background thread and exposes a status
endpoint the frontend polls, so long-running transcription doesn't block
the UI.

## Prerequisites

- Python >= 3.10
- Node.js >= 18
- FFmpeg installed and on your PATH (required by yt-dlp/pydub/Whisper)
- A free Mistral API key: https://console.mistral.ai/

## Backend setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env and set MISTRAL_API_KEY

uvicorn main:app --reload --port 8000
```

The API is now at `http://localhost:8000` (docs at `/docs`).

## Frontend setup

```bash
cd frontend
npm install

cp .env.example .env
# defaults to http://localhost:8000, adjust if needed

npm run dev
```

Open `http://localhost:5173`.

