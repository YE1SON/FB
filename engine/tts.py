import asyncio
import io
import os
import re
import sys
import tempfile
import wave
from dataclasses import dataclass
from typing import List

# ─── Piper TTS Configuration ─────────────────────────────────────────────────
# Runs 100% locally on the Oracle VPS — no external API calls, zero rate limits, no 403 blocks.
# Neural voice models are stored in assets/voices/

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES_DIR = os.path.join(BASE_DIR, "assets", "voices")

VOICES = {
    "christopher": {
        "id": "christopher",
        "model": "en_US-ryan-high",
        "name": "Christopher (Solemne, Profundo y Reverente — Voz de Jesús)",
        "gender": "Hombre",
        "rate_factor": 0.90,  # ritmo solemne y reverente
    },
    "guy": {
        "id": "guy",
        "model": "en_US-joe-medium",
        "name": "Guy (Apasionado, Emocional y Directo)",
        "gender": "Hombre",
        "rate_factor": 1.00,
    },
    "brian": {
        "id": "brian",
        "model": "en_US-bryce-medium",
        "name": "Brian (Tranquilo, Cálido e Inspirador)",
        "gender": "Hombre",
        "rate_factor": 0.92,
    },
    "andrew": {
        "id": "andrew",
        "model": "en_US-lessac-high",
        "name": "Andrew (Moderno, Expresivo y Cercano)",
        "gender": "Hombre",
        "rate_factor": 1.02,
    },
    "jenny": {
        "id": "jenny",
        "model": "en_US-amy-medium",
        "name": "Jenny (Dulce, Maternal y Reconfortante)",
        "gender": "Mujer",
        "rate_factor": 0.95,
    },
}

# Legacy Edge-TTS voice key mapping
LEGACY_VOICE_MAP = {
    "en-US-ChristopherNeural": "christopher",
    "en-US-GuyNeural": "guy",
    "en-US-BrianNeural": "brian",
    "en-US-AndrewMultilingualNeural": "andrew",
    "en-US-JennyNeural": "jenny",
}


@dataclass
class CueItem:
    start_sec: float
    end_sec: float
    text: str


def _parse_rate(rate_str: str) -> float:
    """Convert rate string like '+10%' or '-5%' to a float multiplier."""
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


def _split_into_phrases(text: str) -> List[str]:
    """
    Split text into natural conversational phrase segments of 3-7 words,
    respecting punctuation (periods, commas, exclamation/question marks).
    This feeds into subtitles.py to generate dynamic, viral word groups.
    """
    # First split by major punctuation marks
    raw_sentences = re.split(r'([.?!,;:]+)', text)
    sentences = []
    i = 0
    while i < len(raw_sentences):
        segment = raw_sentences[i].strip()
        if i + 1 < len(raw_sentences) and re.match(r'^[.?!,;:]+$', raw_sentences[i + 1]):
            segment += raw_sentences[i + 1]
            i += 1
        if segment:
            sentences.append(segment)
        i += 1

    # Now ensure no phrase is too long (break phrases longer than 7 words)
    phrases = []
    for s in sentences:
        words = s.split()
        if len(words) <= 7:
            phrases.append(s)
        else:
            # Split long sentences into 4-5 word sub-phrases
            cur = []
            for w in words:
                cur.append(w)
                if len(cur) >= 5:
                    phrases.append(" ".join(cur))
                    cur = []
            if cur:
                phrases.append(" ".join(cur))

    return phrases if phrases else [text]


def _estimate_cues(text: str, total_duration: float) -> List[CueItem]:
    """
    Generate rhythmic phrase cues based on character length weighting.
    Provides natural pacing for subtitles.py.
    """
    phrases = _split_into_phrases(text)
    if not phrases:
        return [CueItem(start_sec=0.0, end_sec=total_duration, text=text)]

    lengths = [max(len(p), 1) for p in phrases]
    total_chars = sum(lengths)

    cues = []
    t = 0.0
    for i, (phrase, length) in enumerate(zip(phrases, lengths)):
        p_dur = total_duration * (length / total_chars)
        # Ensure minimum duration per phrase
        p_dur = max(p_dur, 0.5)
        cues.append(
            CueItem(
                start_sec=round(t, 2),
                end_sec=round(min(t + p_dur, total_duration), 2),
                text=phrase
            )
        )
        t += p_dur

    # Ensure last cue reaches the end
    if cues:
        cues[-1].end_sec = round(total_duration, 2)

    return cues


async def synthesize_speech(text: str, voice_id: str, output_path: str, rate: str = "+0%") -> List[CueItem]:
    """
    Synthesize audio using local neural Piper TTS on Oracle VPS.
    Converts WAV to MP3 and returns timing cues for subtitle generation.
    """
    # Resolve voice config
    voice_key = LEGACY_VOICE_MAP.get(voice_id, voice_id)
    voice_cfg = VOICES.get(voice_key, VOICES["christopher"])

    model_name = voice_cfg["model"]
    model_path = os.path.join(VOICES_DIR, f"{model_name}.onnx")
    config_path = os.path.join(VOICES_DIR, f"{model_name}.onnx.json")

    if not os.path.exists(model_path):
        # Fallback to Ryan high if specified model is missing
        model_path = os.path.join(VOICES_DIR, "en_US-ryan-high.onnx")
        config_path = os.path.join(VOICES_DIR, "en_US-ryan-high.onnx.json")

    if not os.path.exists(model_path):
        raise RuntimeError(
            f"Modelo de voz Piper no encontrado en {VOICES_DIR}. "
            "Por favor verifica los archivos .onnx en el servidor."
        )

    # Calculate length scale (Piper: higher length_scale = slower speech)
    user_rate = _parse_rate(rate)
    voice_factor = voice_cfg.get("rate_factor", 1.0)
    effective_speed = user_rate * voice_factor
    # Clamp speed to sane bounds [0.70, 1.40]
    effective_speed = max(0.70, min(1.40, effective_speed))
    length_scale = 1.0 / effective_speed

    tmp_wav = output_path.replace(".mp3", ".wav")
    if tmp_wav == output_path:
        tmp_wav = output_path + ".tmp.wav"

    # Call piper using the active Python executable (sys.executable)
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

    # Remove temporary WAV
    try:
        if os.path.exists(tmp_wav):
            os.remove(tmp_wav)
    except Exception:
        pass

    # Get exact duration of the output MP3 using ffprobe
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
