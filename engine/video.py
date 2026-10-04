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

def build_video_filter(
    w: int, h: int,
    aspect_ratio: str,
    effect_type: str,
    camera_motion: str,
    total_frames: int,
    norm_ass: str,
    fps: int = 30
) -> str:
    """
    Builds the professional video filter graph:
    1. Smart fitting: If 1:1 or 16:9, generates a blurred background so the image is NEVER cropped.
    2. Camera motion: If 'none', 100% rock-solid stable (zero jitter). If 'zoom_in', smooth zoom.
    3. Visual effects: High-contrast noticeable particles, divine glow, or film grain.
    4. Burned-in ASS subtitles.
    """
    filters = []

    # 1. Base Framing & Canvas Fit
    if aspect_ratio in ["1:1", "16:9"]:
        # Split into blurred background + centered uncropped image
        base_setup = (
            f"[0:v]split=2[bg][fg];"
            f"[bg]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},boxblur=25:5,setsar=1[bgblur];"
            f"[fg]scale={w}:{h}:force_original_aspect_ratio=decrease,setsar=1[fgfit];"
            f"[bgblur][fgfit]overlay=(W-w)/2:(H-h)/2[canvas]"
        )
        current_pad = "[canvas]"
    else: # 9:16 vertical
        base_setup = f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1[canvas]"
        current_pad = "[canvas]"

    filters.append(base_setup)

    # 2. Camera Motion (Only if explicitly requested by user)
    if camera_motion == "zoom_in":
        zoom_speed = 0.15 / max(total_frames, 1)
        motion_str = f"{current_pad}zoompan=z='min(zoom+{zoom_speed:.6f},1.20)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}[motion]"
        filters.append(motion_str)
        current_pad = "[motion]"
    elif camera_motion == "zoom_out":
        zoom_speed = 0.15 / max(total_frames, 1)
        motion_str = f"{current_pad}zoompan=z='max(1.20-({zoom_speed:.6f}*on),1.0)':d={total_frames}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}[motion]"
        filters.append(motion_str)
        current_pad = "[motion]"

    # 3. Visual Effects (Noticeable and Atmospheric)
    fx_parts = []
    if effect_type == "cinematic_dust":
        # Golden dust motes, warm glow, and cinematic vignette
        fx_parts.append("noise=alls=26:allf=t+u")
        fx_parts.append("colorchannelmixer=rr=1.05:gg=1.02:bb=0.96")
        fx_parts.append("vignette=PI/3.5")
    elif effect_type == "divine_light":
        # Radiant warm holy aura and contrast boost
        fx_parts.append("eq=brightness=0.06:contrast=1.12:saturation=1.20")
        fx_parts.append("colorbalance=rs=0.10:gs=0.04:bs=-0.08")
        fx_parts.append("vignette=PI/4")
    elif effect_type == "dramatic_grain":
        # High impact indie film grain
        fx_parts.append("noise=alls=35:allf=t+u")
        fx_parts.append("eq=contrast=1.10:saturation=0.90")

    # 4. Burn in Subtitles
    fx_parts.append(f"ass='{norm_ass}'")

    fx_str = f"{current_pad}{','.join(fx_parts)}[v]"
    filters.append(fx_str)

    return ";".join(filters)

def render_reel(
    image_path: str,
    audio_path: str,
    ass_path: str,
    output_mp4_path: str,
    aspect_ratio: str = "9:16",
    effect_type: str = "cinematic_dust",
    camera_motion: str = "none",
    music_track: str = "worship_piano_peace",
    music_volume: float = 0.20,
    fps: int = 30
) -> str:
    """
    Renders the final video with user-controlled camera motion and noticeable visual effects.
    """
    duration = get_audio_duration(audio_path)
    total_frames = int((duration + 0.5) * fps)
    norm_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    music_file = _resolve_music_file(music_track)

    # Determine resolution based on aspect ratio
    if aspect_ratio == "1:1":
        w, h = 1080, 1080
    elif aspect_ratio == "16:9":
        w, h = 1920, 1080
    else: # default 9:16
        w, h = 1080, 1920

    # Build video filter graph
    video_filter = build_video_filter(w, h, aspect_ratio, effect_type, camera_motion, total_frames, norm_ass, fps)

    cmd = ["ffmpeg", "-y", "-threads", "2", "-loop", "1", "-i", image_path, "-i", audio_path]
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

    print(f"[Render] Ratio: {aspect_ratio}, Motion: {camera_motion}, FX: {effect_type}, BGM Vol: {music_volume}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg rendering failed: {result.stderr[-500:]}")

    return output_mp4_path
