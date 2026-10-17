import os
import subprocess
from pathlib import Path

def sanitize_and_trim_audio(input_audio_path: str, output_audio_path: str) -> str:
    """
    Elimina silencios al inicio (>20ms bajo -45dB) y aplica compresión vocal
    para presencia inmediata en los primeros 500ms de reproducción.
    Garantiza que la locución empiece a modular antes de los 50ms en Facebook Reels.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_audio_path)), exist_ok=True)
    command = [
        "ffmpeg", "-y",
        "-i", input_audio_path,
        "-af", (
            "silenceremove=start_periods=1:start_duration=0.02:start_threshold=-45dB,"
            "acompressor=threshold=-16dB:ratio=2.5:attack=10:release=80,"
            "volume=1.2"
        ),
        "-c:a", "libmp3lame",
        "-b:a", "192k",
        output_audio_path
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Error procesando audio con FFmpeg: {result.stderr}")
    return output_audio_path
