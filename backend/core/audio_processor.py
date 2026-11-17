
import os
import uuid
from typing import List

import yt_dlp
from pydub import AudioSegment

from config import settings


def download_audio(youtube_url: str, job_id: str) -> str:
    
    out_dir = os.path.join(settings.AUDIO_DIR, job_id)
    os.makedirs(out_dir, exist_ok=True)
    out_template = os.path.join(out_dir, "source.%(ext)s")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": out_template,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "wav",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    wav_path = os.path.join(out_dir, "source.wav")
    if not os.path.exists(wav_path):
       
        for f in os.listdir(out_dir):
            if f.startswith("source."):
                wav_path = os.path.join(out_dir, f)
                break

    return wav_path


def chunk_audio(wav_path: str, job_id: str) -> List[str]:
   
    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = settings.AUDIO_CHUNK_MINUTES * 60 * 1000

    out_dir = os.path.join(settings.AUDIO_DIR, job_id, "chunks")
    os.makedirs(out_dir, exist_ok=True)

    chunk_paths = []
    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start : start + chunk_ms]
        chunk_path = os.path.join(out_dir, f"chunk_{i:03d}_{uuid.uuid4().hex[:6]}.wav")
        chunk.export(chunk_path, format="wav")
        chunk_paths.append(chunk_path)

    return chunk_paths


def process_input(source: str, job_id: str) -> List[str]:
    
    wav_path = download_audio(source, job_id)
    return chunk_audio(wav_path, job_id)
