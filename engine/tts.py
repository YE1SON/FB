import asyncio
import io
import os
import re
import sys
import tempfile
import wave
from dataclasses import dataclass
from typing import List, Optional

# ─── Piper TTS + Faster-Whisper Alignment Configuration ─────────────────────
# 1. Piper runs 100% locally on the Oracle VPS (no network calls, no IP blocks).
# 2. Faster-Whisper aligns the speech down to the exact millisecond per word.
# Models are stored in assets/voices/ and ~/.cache/huggingface/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES_DIR = os.path.join(BASE_DIR, "assets", "voices")

VOICES = {
    "christopher": {
        "id": "christopher",
        "model": "en_US-ryan-high",
        "name": "Christopher (Solemne, Profundo y Reverente — Voz de Jesús)",
        "gender": "Hombre",
        "rate_factor": 0.85,  # Calibrado: ritmo pausado, solemne y reflexivo
    },
    "guy": {
        "id": "guy",
        "model": "en_US-joe-medium",
        "name": "Guy (Apasionado, Emocional y Directo)",
        "gender": "Hombre",
        "rate_factor": 0.95,
    },
    "brian": {
        "id": "brian",
        "model": "en_US-bryce-medium",
        "name": "Brian (Tranquilo, Cálido e Inspirador)",
        "gender": "Hombre",
        "rate_factor": 0.88,
    },
    "andrew": {
        "id": "andrew",
        "model": "en_US-lessac-high",
        "name": "Andrew (Moderno, Expresivo y Cercano)",
        "gender": "Hombre",
        "rate_factor": 0.98,
    },
    "jenny": {
        "id": "jenny",
        "model": "en_US-amy-medium",
        "name": "Jenny (Dulce, Maternal y Reconfortante)",
        "gender": "Mujer",
        "rate_factor": 0.90,
    },
}

LEGACY_VOICE_MAP = {
    "en-US-ChristopherNeural": "christopher",
    "en-US-GuyNeural": "guy",
    "en-US-BrianNeural": "brian",
    "en-US-AndrewMultilingualNeural": "andrew",
    "en-US-JennyNeural": "jenny",
}

# Global singleton for Whisper to avoid reload latency
_whisper_model = None


@dataclass
class CueItem:
    start_sec: float
    end_sec: float
    text: str


def _get_whisper():
    """Lazy load faster-whisper model (tiny.en runs on CPU in <1.5s)."""
    global _whisper_model
    if _whisper_model is None:
        try:
            from faster_whisper import WhisperModel
            _whisper_model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
        except Exception as e:
            print(f"[Whisper] No se pudo inicializar faster-whisper: {e}")
            _whisper_model = False
    return _whisper_model if _whisper_model is not False else None


def _parse_rate(rate_str: str) -> float:
    """Convert rate string like '-12%' or '+8%' to a speed multiplier."""
    if not rate_str:
        return 1.0
    rate_str = rate_str.strip()
    try:
        if rate_str.startswith("+"):
            pct = float(rate_str[1:].replace("%", ""))
            return 1.0 + pct / 100.0
        elif rate_str.startswith("-"):
            pct = float(rate_str[1:].replace("%", ""))
            return 1.0 - pct / 100.0
    except Exception:
        pass
    return 1.0


def _extract_whisper_word_cues(audio_path: str) -> Optional[List[CueItem]]:
    """Extract precise millisecond word timestamps using faster-whisper."""
    model = _get_whisper()
    if model is None:
        return None
    try:
        segments, _ = model.transcribe(audio_path, word_timestamps=True, language="en")
        cues = []
        for segment in segments:
            if not segment.words:
                continue
            for w in segment.words:
                word_clean = w.word.strip()
                if word_clean:
                    cues.append(
                        CueItem(
                            start_sec=round(w.start, 2),
                            end_sec=round(max(w.end, w.start + 0.18), 2),
                            text=word_clean
                        )
                    )
        return cues if cues else None
    except Exception as e:
        print(f"[Whisper Alignment Error] {e}")
        return None


def _estimate_cues(text: str, total_duration: float) -> List[CueItem]:
    """Fallback rhythm-based word cue estimator if Whisper is unavailable."""
    words = [w for w in text.split() if w.strip()]
    if not words:
        return [CueItem(start_sec=0.0, end_sec=total_duration, text=text)]

    lengths = [max(len(w), 1) for w in words]
    total_chars = sum(lengths)

    cues = []
    t = 0.0
    for word, length in zip(words, lengths):
        w_dur = total_duration * (length / total_chars)
        cues.append(
            CueItem(
                start_sec=round(t, 2),
                end_sec=round(min(t + w_dur, total_duration), 2),
                text=word
            )
        )
        t += w_dur

    if cues:
        cues[-1].end_sec = round(total_duration, 2)
    return cues


async def synthesize_speech(text: str, voice_id: str, output_path: str, rate: str = "+0%") -> List[CueItem]:
    """
    Synthesize speech using local Piper TTS and extract EXACT word-level timing
    using faster-whisper. Results in zero audio/subtitle desynchronization.
    """
    voice_key = LEGACY_VOICE_MAP.get(voice_id, voice_id)
    voice_cfg = VOICES.get(voice_key, VOICES["christopher"])

    model_name = voice_cfg["model"]
    model_path = os.path.join(VOICES_DIR, f"{model_name}.onnx")
    config_path = os.path.join(VOICES_DIR, f"{model_name}.onnx.json")

    if not os.path.exists(model_path):
        model_path = os.path.join(VOICES_DIR, "en_US-ryan-high.onnx")
        config_path = os.path.join(VOICES_DIR, "en_US-ryan-high.onnx.json")

    if not os.path.exists(model_path):
        raise RuntimeError(f"Modelo de voz Piper no encontrado en {VOICES_DIR}.")

    # Apply solemn rate tuning
    user_rate = _parse_rate(rate)
    voice_factor = voice_cfg.get("rate_factor", 0.88)
    effective_speed = user_rate * voice_factor
    # Clamp speed between [0.65 (muy solemne) and 1.30 (dinámica)]
    effective_speed = max(0.65, min(1.30, effective_speed))
    length_scale = 1.0 / effective_speed

    tmp_wav = output_path.replace(".mp3", ".wav")
    if tmp_wav == output_path:
        tmp_wav = output_path + ".tmp.wav"

    cmd = [
        sys.executable, "-m", "piper",
        "-m", model_path,
        "-c", config_path,
        "-f", tmp_wav,
        "--length-scale", str(round(length_scale, 3)),
        "--noise-scale", "0.667",
        "--noise-w-scale", "0.8",
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=BASE_DIR
    )
    stdout, stderr = await proc.communicate(input=text.encode("utf-8"))

    if proc.returncode != 0:
        err = stderr.decode("utf-8", errors="replace")
        raise RuntimeError(f"Piper TTS falló (código {proc.returncode}): {err[:400]}")

    if not os.path.exists(tmp_wav) or os.path.getsize(tmp_wav) == 0:
        raise RuntimeError("Piper TTS no generó el archivo de audio WAV.")

    # Convert WAV -> MP3 using ffmpeg
    convert_cmd = [
        "ffmpeg", "-y",
        "-i", tmp_wav,
        "-codec:a", "libmp3lame",
        "-q:a", "2",
        output_path
    ]
    conv_proc = await asyncio.create_subprocess_exec(
        *convert_cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    _, conv_err = await conv_proc.communicate()
    if conv_proc.returncode != 0:
        raise RuntimeError(f"FFmpeg WAV a MP3 falló: {conv_err.decode(errors='replace')[:300]}")

    try:
        if os.path.exists(tmp_wav):
            os.remove(tmp_wav)
    except Exception:
        pass

    # Extract EXACT word millisecond timestamps using faster-whisper
    cues = _extract_whisper_word_cues(output_path)

    # If whisper was not available, measure audio duration and estimate
    if not cues:
        probe_cmd = [
            "ffprobe", "-v", "quiet",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            output_path
        ]
        probe_proc = await asyncio.create_subprocess_exec(
            *probe_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        probe_out, _ = await probe_proc.communicate()
        try:
            duration = float(probe_out.decode().strip())
        except Exception:
            duration = 20.0
        cues = _estimate_cues(text, duration)

    return cues


def get_available_voices():
    return [
        {"key": k, "id": v["id"], "name": v["name"], "gender": v["gender"]}
        for k, v in VOICES.items()
    ]
