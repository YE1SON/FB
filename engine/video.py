import os
import subprocess
import shutil

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio")

WORSHIP_TRACKS = {
    "worship_piano_peace": "🕊️ Piano de Paz (Adoración Íntima y Pad Suave)",
    "celestial_strings_hope": "🌅 Cuerdas Celestiales (Esperanza y Victoria)",
    "midnight_prayer_acoustic": "🛌 Oración Nocturna (Ambiente Profundo de Reposo)",
    "none": "🔇 Sin Música de Fondo (Solo Voz)"
}

def get_audio_duration(audio_path: str) -> float:
    """Get precise duration of audio file using ffprobe."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def render_reel(
    image_path: str,
    audio_path: str,
    ass_path: str,
    output_mp4_path: str,
    music_track: str = "worship_piano_peace",
    music_volume: float = 0.20,
    fps: int = 30
) -> str:
    """
    Renders high-quality 1080x1920 vertical Reel with smooth, dynamic Ken Burns camera zoom-in animation
    towards Jesus' face, burned ASS dynamic subtitles, and ambient worship background music.
    """
    duration = get_audio_duration(audio_path)
    total_frames = int((duration + 0.5) * fps)
    
    # Velocidad de zoom dinámico: acercamiento progresivo y fluido del 1.0 hasta 1.25 durante todo el audio
    zoom_speed = 0.22 / max(total_frames, 1)

    # Windows path formatting for FFmpeg ass filter
    norm_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    
    # Check if background music is requested and exists
    music_file = None
    if music_track and music_track != "none":
        candidate = os.path.join(AUDIO_DIR, f"{music_track}.mp3")
        if os.path.exists(candidate):
            music_file = candidate

    fade_out_start = max(0.0, duration - 2.0)

    if music_file:
        filter_complex = (
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"zoompan=z='min(zoom+{zoom_speed:.6f},1.26)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih*0.35-(ih*0.35/zoom)':s=1080x1920:fps={fps},"
            f"ass='{norm_ass}'[v];"
            f"[1:a]volume=1.0[voice];"
            f"[2:a]volume={music_volume:.2f},afade=t=out:st={fade_out_start:.2f}:d=2.0[bgm];"
            f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-threads", "2",
            "-i", image_path,
            "-i", audio_path,
            "-i", music_file,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "[a]",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_mp4_path
        ]
    else:
        filter_complex = (
            f"[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"zoompan=z='min(zoom+{zoom_speed:.6f},1.26)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih*0.35-(ih*0.35/zoom)':s=1080x1920:fps={fps},"
            f"ass='{norm_ass}'[v]"
        )
        cmd = [
            "ffmpeg", "-y",
            "-threads", "2",
            "-i", image_path,
            "-i", audio_path,
            "-filter_complex", filter_complex,
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "ultrafast",
            "-crf", "23",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-shortest",
            output_mp4_path
        ]

    print(f"Running FFmpeg render (BGM: {music_track if music_file else 'none'}, {total_frames} frames)...")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        print("FFmpeg Error:", result.stderr)
        raise RuntimeError(f"FFmpeg rendering failed: {result.stderr[-500:]}")
        
    print(f"Render complete: {output_mp4_path} ({os.path.getsize(output_mp4_path)} bytes)")
    return output_mp4_path
