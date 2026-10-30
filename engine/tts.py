import asyncio
import io
import os
import re
import sys
import tempfile
from dataclasses import dataclass
from typing import Dict, List, Optional
from engine.audio import sanitize_and_trim_audio

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOICES_DIR = os.path.join(BASE_DIR, "assets", "voices")

# ─── Data Structure for Subtitle Cues ─────────────────────────────────────────

@dataclass
class CueItem:
    start_sec: float
    end_sec: float
    text: str

# ─── Voice Registry ───────────────────────────────────────────────────────────

VOICES: Dict[str, Dict] = {
    # ─── Edge-TTS Online Neural Voices (Voces recomendadas para inglés de EE. UU.) ─
    "guy": {
        "id": "guy",
        "engine": "edge",
        "voice_name": "en-US-GuyNeural",
        "name": "Guy (Conversacional y Empático — Edge HD)",
        "gender": "Hombre",
        "base_speed": 0.94,
    },
    "brian": {
        "id": "brian",
        "engine": "edge",
        "voice_name": "en-US-BrianNeural",
        "name": "Brian (Tranquilo e Inspirador — Edge HD)",
        "gender": "Hombre",
        "base_speed": 0.94,
    },
    "christopher": {
        "id": "christopher",
        "engine": "edge",
        "voice_name": "en-US-ChristopherNeural",
        "name": "Christopher (Firme, Confiado y Cálido — Edge HD)",
        "gender": "Hombre",
        "base_speed": 0.94,
    },
    "andrew": {
        "id": "andrew",
        "engine": "edge",
        "voice_name": "en-US-AndrewMultilingualNeural",
        "name": "Andrew (Dinámico y Conmovedor — Edge HD)",
        "gender": "Hombre",
        "base_speed": 0.94,
    },

}

LEGACY_VOICE_MAP = {
    "en-US-GuyNeural": "guy",
    "en-US-ChristopherNeural": "christopher",
    "en-US-BrianNeural": "brian",
    "en-US-AndrewMultilingualNeural": "andrew"

}

# Singletons
_whisper_model = None


def check_engine_availability() -> Dict[str, bool]:
    """Registra los motores que se utilizan: Edge-TTS y Whisper."""
    try:
        import edge_tts
        edge_ok = True
    except ImportError:
        edge_ok = False
    try:
        import faster_whisper
        whisper_ok = True
    except ImportError:
        whisper_ok = False
    return {"edge": edge_ok, "edge_tts": edge_ok, "whisper": whisper_ok,
            "faster_whisper": whisper_ok, "kokoro": False, "piper": False}


def _get_whisper():
    """Lazy load faster-whisper singleton."""
    global _whisper_model
    if _whisper_model is None:
        try:
            from faster_whisper import WhisperModel
            _whisper_model = WhisperModel("tiny.en", device="cpu", compute_type="int8")
            print("[TTS Engine] faster-whisper tiny.en cargado con éxito en CPU.")
        except Exception as e:
            print(f"[TTS Engine] No se pudo inicializar faster-whisper: {e}")
            _whisper_model = False
    return _whisper_model if _whisper_model is not False else None



def _parse_rate(rate_str: str) -> float:
    """Convert rate string like '-10%' or '+8%' to speed multiplier."""
    if not rate_str:
        return 1.0
    rate_str = str(rate_str).strip()
    try:
        if rate_str.startswith("+"):
            return 1.0 + float(rate_str[1:].replace("%", "")) / 100.0
        elif rate_str.startswith("-"):
            return 1.0 - float(rate_str[1:].replace("%", "")) / 100.0
    except Exception:
        pass
    return 1.0


def _extract_whisper_word_cues(audio_path: str) -> Optional[List[CueItem]]:
    """Extrae marcas de tiempo de cada palabra con precisión de milisegundos usando faster-whisper con filtro VAD."""
    model = _get_whisper()
    if model is None:
        return None
    try:
        segments, _ = model.transcribe(
            audio_path,
            word_timestamps=True,
            language="en",
            vad_filter=True,
            vad_parameters=dict(min_silence_duration_ms=250)
        )
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
                            end_sec=round(max(w.end, w.start + 0.15), 2),
                            text=word_clean
                        )
                    )
        return cues if cues else None
    except Exception as e:
        print(f"[Whisper Alignment Error]: {e}")
        return None


def _estimate_segment_cues(text: str, total_duration: float) -> List[CueItem]:
    """
    Alineación estructurada por oraciones y cláusulas cuando Faster-Whisper no está disponible.
    Respeta la puntuación natural para mantener subtítulos legibles y estables
    en lugar de proyectar marcas artificiales palabra por palabra.
    """
    raw_clauses = re.split(r'([.?!,;:\n—]+)', text)
    clauses = []
    temp = ""
    for part in raw_clauses:
        if not part:
            continue
        if re.match(r'^[.?!,;:\n—]+$', part):
            temp += part
            if temp.strip():
                clauses.append(temp.strip())
            temp = ""
        else:
            if temp.strip():
                clauses.append(temp.strip())
            temp = part
    if temp.strip():
        clauses.append(temp.strip())

    if not clauses:
        clauses = [w for w in text.split() if w.strip()]
        if not clauses:
            return [CueItem(start_sec=0.0, end_sec=total_duration, text=text)]

    char_counts = [max(len(c), 1) for c in clauses]
    total_chars = sum(char_counts)
    cues = []
    t = 0.0
    for clause, count in zip(clauses, char_counts):
        dur = total_duration * (count / total_chars)
        cues.append(
            CueItem(
                start_sec=round(t, 2),
                end_sec=round(min(t + dur, total_duration), 2),
                text=clause
            )
        )
        t += dur

    if cues:
        cues[-1].end_sec = round(total_duration, 2)
    return cues


# Alias para compatibilidad hacia atrás
_estimate_cues = _estimate_segment_cues


async def synthesize_speech(
    text: str,
    voice_id: str,
    output_path: str,
    rate: str = "+0%"
) -> List[CueItem]:
    """Sintetiza una de las cuatro voces Edge-TTS y alinea subtítulos."""
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("El texto para síntesis de voz no puede estar vacío.")

    voice_key = LEGACY_VOICE_MAP.get(voice_id, voice_id)
    voice_cfg = VOICES.get(voice_key)

    # Si la voz no existe, asignar la primera voz válida recomendada
    if not voice_cfg:
        voice_cfg = VOICES["guy"]

    engine_pref = voice_cfg.get("engine", "kokoro")
    user_rate = _parse_rate(rate)

    tmp_wav = output_path.replace(".mp3", ".wav")
    if tmp_wav == output_path:
        tmp_wav = output_path + ".tmp.wav"

    # Cuatro voces permitidas: exclusivamente Edge-TTS (Guy, Christopher,
    # Brian y Andrew). No se cambia silenciosamente a una voz eliminada.
    if engine_pref != "edge":
        raise RuntimeError("Solo están habilitadas las voces Edge-TTS seleccionadas.")
    try:
        import edge_tts
        v_name = voice_cfg["voice_name"]
        rate_pct = int((user_rate - 1.0) * 100)
        communicate = edge_tts.Communicate(clean_text, v_name, rate=f"{rate_pct:+d}%")
        await communicate.save(tmp_wav)
    except Exception as exc:
        raise RuntimeError(f"No fue posible sintetizar la voz {voice_key} con Edge-TTS: {exc}") from exc
    if not os.path.exists(tmp_wav) or os.path.getsize(tmp_wav) < 1000:
        raise RuntimeError(f"Edge-TTS no produjo audio para la voz {voice_key}.")
    engine_used = "edge_tts"

    print(f"[TTS Synthesized] Motor: {engine_used} | Voz: {voice_cfg['name']} | Velocidad: {user_rate:.2f}x")

    # Sanitizar silencios iniciales (>20ms bajo -45dB), masterizar presencia y convertir a MP3
    await asyncio.to_thread(sanitize_and_trim_audio, tmp_wav, output_path)

    try:
        if os.path.exists(tmp_wav):
            os.remove(tmp_wav)
    except Exception:
        pass

    # Extraer marcas de tiempo exactas por palabra con faster-whisper
    cues = _extract_whisper_word_cues(output_path)

    # Si Whisper no devolvió marcas, usar segmentos aproximados
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
            dur = float(probe_out.decode().strip())
        except Exception:
            dur = 20.0
        cues = _estimate_segment_cues(clean_text, dur)

    return cues


def get_available_voices() -> List[Dict]:
    """Expone únicamente las cuatro voces Edge-TTS aprobadas."""
    return [
        {"key": k, "id": v["id"], "name": v["name"],
         "gender": v["gender"], "engine": "edge"}
        for k, v in VOICES.items()
    ]
