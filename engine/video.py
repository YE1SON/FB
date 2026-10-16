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

EFFECTS = {
    "cinematic_dust": "✨ Polvo de Oro Divino (Partículas doradas)",
    "divine_light": "☀️ Rayos de Luz Celestial (Aura dorada y resplandor visible)",
    "dramatic_grain": "🎬 Grano de Cine Épico (Textura 35mm y alto contraste)",
    "celestial_glow": "🕊️ Resplandor de Gloria (Niebla mística y difusión divina)",
    "golden_hour": "🌅 Hora Dorada Sagrada (Luz cálida de atardecer de oración)",
    "holy_fire": "🔥 Fuego del Espíritu Santo (Tonos fuego y victoria espiritual)",
    "none": "🖼️ Sin Efectos (Imagen Limpia y Pura)"
}

CAMERA_MOTIONS = {
    "none": "🔒 Fija / Estable (Sin Movimiento)",
    "zoom_in": "🔍 Acercamiento Lento (Zoom In al Centro)",
    "zoom_out": "🔭 Alejamiento Suave (Zoom Out Panorámico)",
    "pan_up": "⬆️ Inclinación al Cielo (Pan Up hacia Arriba)",
    "pan_down": "⬇️ Revelación Divina (Pan Down hacia Abajo)",
    "pan_right": "➡️ Barrido Cinematográfico (Izquierda a Derecha)",
    "pan_left": "⬅️ Barrido Inverso (Derecha a Izquierda)",
    "zoom_in_pan_up": "✨ Ascenso + Zoom Épico (Acercamiento y Subida al Cielo)"
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
    duration: float,
    fps: int = 30
) -> str:
    """
    Builds an optimized, high-performance FFmpeg filter graph:
    1. Continuous Camera Motion: zoompan runs across the ENTIRE duration of the video
       using dynamic 'on / total_frames' so motion NEVER freezes prematurely.
    2. Smart Framing: For 1:1 or 16:9 on vertical reels, blurred background preserves full image.
    3. Noticeable Visual Effects: Color-balanced, LUT-accelerated shaders for instant visible impact.
    4. Burned-in ASS subtitles and floating particle elements.
    """
    filters = []
    has_motion = camera_motion and camera_motion != "none"

    if has_motion:
        # Camera motion generated smoothly across the entire video duration
        tf = max(total_frames, 1)
        if camera_motion == "zoom_in":
            motion_filter = f"[0:v]zoompan=z='1.0+(0.22*on/{tf})':d={tf}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}[motion]"
        elif camera_motion == "zoom_out":
            motion_filter = f"[0:v]zoompan=z='1.22-(0.22*on/{tf})':d={tf}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}[motion]"
        elif camera_motion == "pan_up":
            motion_filter = f"[0:v]zoompan=z=1.18:d={tf}:x='iw/2-(iw/zoom/2)':y='(ih-(ih/zoom))*(1.0-on/{tf})':s={w}x{h}:fps={fps}[motion]"
        elif camera_motion == "pan_down":
            motion_filter = f"[0:v]zoompan=z=1.18:d={tf}:x='iw/2-(iw/zoom/2)':y='(ih-(ih/zoom))*(on/{tf})':s={w}x{h}:fps={fps}[motion]"
        elif camera_motion == "pan_right":
            motion_filter = f"[0:v]zoompan=z=1.18:d={tf}:x='(iw-(iw/zoom))*(on/{tf})':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}[motion]"
        elif camera_motion == "pan_left":
            motion_filter = f"[0:v]zoompan=z=1.18:d={tf}:x='(iw-(iw/zoom))*(1.0-on/{tf})':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}[motion]"
        elif camera_motion == "zoom_in_pan_up":
            motion_filter = f"[0:v]zoompan=z='1.0+(0.24*on/{tf})':d={tf}:x='iw/2-(iw/zoom/2)':y='(ih-(ih/zoom))*(1.0-on/{tf})':s={w}x{h}:fps={fps}[motion]"
        else:
            motion_filter = f"[0:v]zoompan=z='1.0+(0.20*on/{tf})':d={tf}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}[motion]"

        filters.append(motion_filter)
    else:
        # Static framing (fast scale & crop on looped input)
        if aspect_ratio in ["1:1", "16:9"]:
            base_setup = (
                f"[0:v]split=2[bg][fg];"
                f"[bg]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},avgblur=20,setsar=1[bgblur];"
                f"[fg]scale={w}:{h}:force_original_aspect_ratio=decrease,setsar=1[fgfit];"
                f"[bgblur][fgfit]overlay=(W-w)/2:(H-h)/2[motion]"
            )
        else:
            base_setup = f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1[motion]"

        filters.append(base_setup)

    # Visual Effects Grading
    fx_parts = []
    if effect_type == "cinematic_dust":
        # Polvo de oro: tinte dorado cálido y viñeta de cine suave
        fx_parts.append("colorchannelmixer=rr=1.06:gg=1.03:bb=0.95")
        fx_parts.append("vignette=PI/3.5")
    elif effect_type == "divine_light":
        # Rayos de Luz Celestial: aura resplandeciente, cálida y de gran impacto visual
        fx_parts.append("eq=brightness=0.09:contrast=1.30:saturation=1.35")
        fx_parts.append("colorbalance=rs=0.22:gs=0.10:bs=-0.14:rm=0.15:gm=0.08:bm=-0.10")
        fx_parts.append("vignette=PI/4")
    elif effect_type == "dramatic_grain":
        # Grano de cine dramático 35mm Hollywood, alto contraste y sombras profundas
        fx_parts.append("noise=alls=45:allf=t+u")
        fx_parts.append("eq=contrast=1.38:saturation=0.78")
        fx_parts.append("vignette=PI/3.0")
    elif effect_type == "celestial_glow":
        # Resplandor Celestial / Niebla de Gloria
        fx_parts.append("eq=brightness=0.12:contrast=1.22:saturation=1.25")
        fx_parts.append("colorbalance=rs=0.14:gs=0.12:bs=0.02")
        fx_parts.append("vignette=PI/4.2")
    elif effect_type == "golden_hour":
        # Hora Dorada Sagrada
        fx_parts.append("colorbalance=rs=0.28:gs=0.14:bs=-0.22:rh=0.22:gh=0.10:bh=-0.25")
        fx_parts.append("eq=saturation=1.40:contrast=1.22")
        fx_parts.append("vignette=PI/3.8")
    elif effect_type == "holy_fire":
        # Fuego y Unción del Espíritu Santo (Resplandor ámbar cálido y destellos dorados sin quemar en rojo)
        fx_parts.append("colorbalance=rh=0.14:gh=0.06:bh=-0.16:rm=0.06:gm=0.02:bm=-0.08")
        fx_parts.append("eq=contrast=1.18:saturation=1.12:brightness=0.03")
        fx_parts.append("vignette=PI/3.8")
    elif effect_type == "celestial_bloom":
        # Aura de Gloria Celestial (Resplandor suave en las altas luces y presencia divina)
        fx_parts.append("eq=brightness=0.07:contrast=1.15:saturation=1.16")
        fx_parts.append("colorbalance=rh=0.10:gh=0.10:bh=0.04")
        fx_parts.append("vignette=PI/4.0")
    elif effect_type == "dawn_hope":
        # Amanecer de Esperanza (Luz cálida y suave para oraciones de sanidad y mañana)
        fx_parts.append("colorbalance=rh=0.16:gh=0.08:bh=-0.12:rm=0.08:gm=0.04:bm=-0.06")
        fx_parts.append("eq=contrast=1.12:saturation=1.10:brightness=0.04")
        fx_parts.append("vignette=PI/4.2")

    # Burn in Subtitles & Embedded Floating Particles
    fx_parts.append(f"ass='{norm_ass}'")

    fx_str = f"[motion]{','.join(fx_parts)}[v]"
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
    Renders the final vertical video using all 4 CPU cores, ultra-fast encoding,
    and rock-solid memory management.
    """
    duration = get_audio_duration(audio_path)
    total_frames = int((duration + 0.5) * fps)
    norm_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    music_file = _resolve_music_file(music_track)

    if aspect_ratio == "1:1":
        w, h = 1080, 1080
    elif aspect_ratio == "16:9":
        w, h = 1920, 1080
    else: # default 9:16
        w, h = 1080, 1920

    video_filter = build_video_filter(
        w, h, aspect_ratio, effect_type, camera_motion, total_frames, norm_ass, duration, fps
    )

    has_motion = camera_motion and camera_motion != "none"
    cmd = ["ffmpeg", "-y", "-threads", "4"]

    if has_motion:
        # Single image input without loop: zoompan handles frame generation cleanly
        cmd.extend(["-i", image_path])
    else:
        # Looped input bounded strictly to the audio duration
        cmd.extend(["-loop", "1", "-t", f"{duration + 0.2:.2f}", "-i", image_path])

    cmd.extend(["-i", audio_path])

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
        "-t", f"{duration:.2f}",
        output_mp4_path
    ])

    print(f"[Render] Ratio: {aspect_ratio}, Motion: {camera_motion}, FX: {effect_type}, Duration: {duration:.2f}s")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg rendering failed: {result.stderr[-500:]}")

    return output_mp4_path
