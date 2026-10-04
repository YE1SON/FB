import os
import subprocess

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio")

WORSHIP_TRACKS = {
    "worship_piano_peace": "🕊️ Piano de Paz (Adoración Íntima y Pad Suave)",
    "celestial_strings_hope": "🌅 Cuerdas Celestiales (Esperanza y Victoria)",
    "midnight_prayer_acoustic": "🛌 Oración Nocturna (Ambiente Profundo de Reposo)",
    "none": "🔇 Sin Música de Fondo (Solo Voz)"
}

def get_audio_duration(audio_path: str) -> float:
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())

def _build_audio_filter(audio_path: str, music_file: str, music_volume: float, duration: float) -> str:
    fade_out_start = max(0.0, duration - 2.0)
    return (
        f"[1:a]volume=1.0[voice];"
        f"[2:a]volume={music_volume:.2f},afade=t=out:st={fade_out_start:.2f}:d=2.0[bgm];"
        f"[voice][bgm]amix=inputs=2:duration=first:dropout_transition=2[a]"
    )

def _resolve_music_file(music_track: str):
    if music_track and music_track != "none":
        candidate = os.path.join(AUDIO_DIR, f"{music_track}.mp3")
        if os.path.exists(candidate):
            return candidate
    return None

def get_visual_effect_string(effect_type: str, total_frames: int, zoom_speed: float, w: int, h: int, fps: int) -> str:
    """Builds the visual filter string combining zoompan and dynamic particles/overlays."""
    # Base movement: Ken burns zoom
    base_zoom = f"zoompan=z='min(zoom+{zoom_speed:.6f},1.25)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}"
    
    if effect_type == "cinematic_dust":
        # temporal noise simulating dust particles + vignette
        return f"{base_zoom},noise=alls=12:allf=t+u,vignette=PI/3"
    elif effect_type == "divine_light":
        # color pulsing + slight vignette
        return f"{base_zoom},colorlevels=rimin=0.0:gimin=0.0:bimin=0.0:rimax=1.0:gimax=1.0:bimax=1.0,vignette=PI/4"
    elif effect_type == "dramatic_grain":
        # heavy film grain, no vignette
        return f"{base_zoom},noise=alls=20:allf=t+u"
    else:
        # "none" -> just the zoom
        return base_zoom

def render_reel(
    image_path: str,
    audio_path: str,
    ass_path: str,
    output_mp4_path: str,
    aspect_ratio: str = "9:16",
    effect_type: str = "cinematic_dust",
    music_track: str = "worship_piano_peace",
    music_volume: float = 0.20,
    fps: int = 30
) -> str:
    """
    Renders the final video with dynamic micro-motion effects to pass Facebook's motion score.
    """
    duration = get_audio_duration(audio_path)
    total_frames = int((duration + 0.5) * fps)
    zoom_speed = 0.20 / max(total_frames, 1)
    norm_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    music_file = _resolve_music_file(music_track)

    # Determine resolution based on aspect ratio
    if aspect_ratio == "1:1":
        w, h = 1080, 1080
    elif aspect_ratio == "16:9":
        w, h = 1920, 1080
    else: # default 9:16
        w, h = 1080, 1920

    # Build the visual string
    scale_crop = f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h}"
    visual_fx = get_visual_effect_string(effect_type, total_frames, zoom_speed, w, h, fps)
    
    # Complete video filter
    video_filter = f"[0:v]{scale_crop},{visual_fx},ass='{norm_ass}'[v]"

    cmd = ["ffmpeg", "-y", "-threads", "2", "-i", image_path, "-i", audio_path]
    if music_file:
        cmd.extend(["-i", music_file])
        audio_filter = _build_audio_filter(audio_path, music_file, music_volume, duration)
        filter_complex = f"{video_filter};{audio_filter}"
        cmd.extend(["-filter_complex", filter_complex, "-map", "[v]", "-map", "[a]"])
    else:
        filter_complex = video_filter
        cmd.extend(["-filter_complex", filter_complex, "-map", "[v]", "-map", "1:a"])

    cmd.extend([
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-shortest",
        output_mp4_path
    ])

    print(f"[Render] Mode: {aspect_ratio}, FX: {effect_type}, BGM Vol: {music_volume}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg rendering failed: {result.stderr[-500:]}")

    return output_mp4_path
