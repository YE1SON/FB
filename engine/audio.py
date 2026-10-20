import os
import subprocess
from pathlib import Path
from typing import Dict

def get_sfx_files() -> Dict[str, str]:
    """Retorna las rutas a los micro-efectos de sonido cinemáticos y sagrados."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sfx_dir = os.path.join(base_dir, "assets", "audio", "sfx")
    return {
        "whoosh": os.path.join(sfx_dir, "sfx_scroll_stopper.mp3"),
        "chime": os.path.join(sfx_dir, "sfx_divine_chime.mp3"),
        "swell": os.path.join(sfx_dir, "sfx_holy_swell.mp3")
    }

def sanitize_and_trim_audio(input_audio_path: str, output_audio_path: str, master_lufs: bool = True) -> str:
    """
    Elimina silencios al inicio (>20ms bajo -45dB), aplica compresión vocal,
    ecualización de presencia/calidez humana y masterización broadcast -14 LUFS (Estándar Meta).
    Garantiza que la locución empiece a modular antes de los 50ms en Facebook Reels.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)
    
    af_filters = [
        "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-45dB",
        "acompressor=threshold=-16dB:ratio=2.5:attack=10:release=80",
        "equalizer=f=120:width_type=h:width=60:g=1.8",
        "equalizer=f=3300:width_type=h:width=1200:g=2.2"
    ]
    if master_lufs:
        af_filters.append("loudnorm=I=-14:TP=-1.0:LRA=7")
    else:
        af_filters.append("volume=1.2")
        
    command = [
        "ffmpeg", "-y",
        "-i", input_audio_path,
        "-af", ",".join(af_filters),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_audio_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Error procesando audio con FFmpeg: {result.stderr}")
    return output_audio_path
