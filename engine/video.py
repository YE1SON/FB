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

def _resolve_music_file(music_track: str):
    if music_track and music_track != "none":
        candidate = os.path.join(AUDIO_DIR, f"{music_track}.mp3")
        if os.path.exists(candidate):
            return candidate
    return None

def build_3scene_video_filter(
    w: int, h: int,
    aspect_ratio: str,
    effect_type: str,
    norm_ass: str,
    duration: float,
    fps: int = 30
) -> str:
    """
    Pipeline de Composición de 3 Escenas Dinámicas con Flash-Focus Cinético:
    - Escena 1 (Gancho): 0.0s a 3.2s con Flash-Focus inicial (desenfoque gaussiano
      disipándose en 0.35s + pulso de brillo dorado en 0.40s) y Zoom-In centrado.
    - Transición 1 (3.2s): Disolución rápida (xfade 0.35s, offset 2.85s).
    - Escena 2 (Punto de Inflexión / Intercesión): 3.2s a D * 0.62 con cinemática alternada.
    - Transición 2: Disolución suave (xfade 0.60s, offset (D*0.62)-0.60s).
    - Escena 3 (Paz / Victoria / Promesa): D * 0.62 al final con Zoom-In suave continuo.
    - Etalonaje de color + Subtítulos SSA/ASS con Doble Insignia Superior.
    """
    filters = []

    t2 = round(max(duration * 0.62, 4.5), 2)
    d1 = 0.35
    d2 = 0.60
    offset1 = round(max(3.20 - d1, 0.5), 2)
    offset2 = round(max(t2 - d2, offset1 + 1.0), 2)

    tf1 = max(int((3.20 + 1.0) * fps), 30)
    tf2 = max(int(((t2 - offset1) + 1.5) * fps), 30)
    tf3 = max(int(((duration - offset2) + 1.5) * fps), 30)

    # 1. Escena 1: Scale/Crop + Zoom-in centrado (1.0 -> 1.08) + Flash-Focus
    s1_filter = (
        f"[0:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,"
        f"zoompan=z='1.0+(0.08*on/{tf1})':d={tf1}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps},"
        f"split=2[v1_sharp][v1_blur_in];"
        f"[v1_blur_in]gblur=sigma=12[v1_blurred];"
        f"[v1_sharp][v1_blurred]blend=all_expr='if(lt(T,0.35), B*(1-T/0.35)+A*(T/0.35), A)',"
        f"eq=brightness='if(lt(t,0.40), 0.15*(1-t/0.40), 0)'[v1]"
    )
    filters.append(s1_filter)

    # 2. Escena 2: Scale/Crop + Cinemática alternada (Zoom-out y pan hacia arriba)
    s2_filter = (
        f"[1:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,"
        f"zoompan=z='1.10-(0.08*on/{tf2})':d={tf2}:x='iw/2-(iw/zoom/2)':y='(ih-(ih/zoom))*(1.0-on/{tf2})':s={w}x{h}:fps={fps}[v2]"
    )
    filters.append(s2_filter)

    # 3. Escena 3: Scale/Crop + Zoom-in continuo suave (1.0 -> 1.10)
    s3_filter = (
        f"[2:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,"
        f"zoompan=z='1.0+(0.10*on/{tf3})':d={tf3}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}[v3]"
    )
    filters.append(s3_filter)

    # 4. Transiciones encadenadas xfade
    blend_filter = (
        f"[v1][v2]xfade=transition=fade:duration={d1}:offset={offset1}[v12];"
        f"[v12][v3]xfade=transition=fade:duration={d2}:offset={offset2}[motion]"
    )
    filters.append(blend_filter)

    # 5. Visual Effects Grading
    fx_parts = []
    if effect_type == "cinematic_dust":
        fx_parts.append("colorchannelmixer=rr=1.06:gg=1.03:bb=0.95")
        fx_parts.append("vignette=PI/3.5")
    elif effect_type == "divine_light":
        fx_parts.append("eq=brightness=0.09:contrast=1.30:saturation=1.35")
        fx_parts.append("colorbalance=rs=0.22:gs=0.10:bs=-0.14:rm=0.15:gm=0.08:bm=-0.10")
        fx_parts.append("vignette=PI/4")
    elif effect_type == "dramatic_grain":
        fx_parts.append("noise=alls=45:allf=t+u")
        fx_parts.append("eq=contrast=1.38:saturation=0.78")
        fx_parts.append("vignette=PI/3.0")
    elif effect_type == "celestial_glow":
        fx_parts.append("eq=brightness=0.12:contrast=1.22:saturation=1.25")
        fx_parts.append("colorbalance=rs=0.14:gs=0.12:bs=0.02")
        fx_parts.append("vignette=PI/4.2")
    elif effect_type == "golden_hour":
        fx_parts.append("colorbalance=rs=0.28:gs=0.14:bs=-0.22:rh=0.22:gh=0.10:bh=-0.25")
        fx_parts.append("eq=saturation=1.40:contrast=1.22")
        fx_parts.append("vignette=PI/3.8")
    elif effect_type == "holy_fire":
        fx_parts.append("colorbalance=rh=0.14:gh=0.06:bh=-0.16:rm=0.06:gm=0.02:bm=-0.08")
        fx_parts.append("eq=contrast=1.18:saturation=1.12:brightness=0.03")
        fx_parts.append("vignette=PI/3.8")

    # Burn-in Subtítulos ASS
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
    fps: int = 30,
    image_path_2: str = None,
    image_path_3: str = None
) -> str:
    """
    Renderiza el Reel final utilizando el pipeline cinemático de 3 escenas,
    Flash-Focus instantáneo en el segundo 0, y subtítulos de doble insignia.
    """
    duration = get_audio_duration(audio_path)
    norm_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    music_file = _resolve_music_file(music_track)

    if aspect_ratio == "1:1":
        w, h = 1080, 1080
    elif aspect_ratio == "16:9":
        w, h = 1920, 1080
    else:  # default 9:16
        w, h = 1080, 1920

    # Resolución y duplicación inteligente de imágenes según disponibilidad
    img1 = image_path if (image_path and os.path.exists(image_path)) else None
    img2 = image_path_2 if (image_path_2 and os.path.exists(image_path_2)) else None
    img3 = image_path_3 if (image_path_3 and os.path.exists(image_path_3)) else None

    if not img1:
        raise FileNotFoundError(f"Imagen principal no encontrada: {image_path}")

    if img1 and img2 and not img3:
        img3 = img1  # Duplicar imagen 1 para escena 3 con encuadre y zoom alternativo
    elif img1 and not img2 and not img3:
        img2 = img1
        img3 = img1

    video_filter = build_3scene_video_filter(
        w, h, aspect_ratio, effect_type, norm_ass, duration, fps
    )

    cmd = ["ffmpeg", "-y", "-threads", "4"]
    # 3 entradas de video para la composición dinámica
    cmd.extend(["-i", img1, "-i", img2, "-i", img3])
    cmd.extend(["-i", audio_path])
    audio_input_idx = 3

    if music_file:
        cmd.extend(["-i", music_file])
        music_input_idx = audio_input_idx + 1
        fade_out_start = max(0.0, duration - 2.0)
        audio_filter = (
            f"[{audio_input_idx}:a]volume=1.0[maina];"
            f"[{music_input_idx}:a]volume={music_volume:.2f},afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out_start:.2f}:d=2.0[musica];"
            f"[maina][musica]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        filter_complex = f"{video_filter};{audio_filter}"
        cmd.extend(["-filter_complex", filter_complex, "-map", "[v]", "-map", "[a]"])
    else:
        filter_complex = video_filter
        cmd.extend(["-filter_complex", filter_complex, "-map", "[v]", "-map", f"{audio_input_idx}:a"])

    cmd.extend([
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{duration:.2f}",
        output_mp4_path
    ])

    print(f"[Render 3-Scene] Ratio: {aspect_ratio}, FX: {effect_type}, Dur: {duration:.2f}s")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg rendering failed: {result.stderr[-500:]}")

    return output_mp4_path
