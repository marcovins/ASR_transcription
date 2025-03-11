from whisperx.types import AlignedTranscriptionResult, TranscriptionResult
from whisperx.diarize import DiarizationPipeline, assign_word_speakers
import whisperx, logging, os, torch, gc, asyncio, shutil
from typing import Optional, Union
from moviepy import VideoFileClip
from pydub import AudioSegment

HUGGINGFACE_KEY = os.getenv("HUGGING")
BASE_PATH = "temp/"
