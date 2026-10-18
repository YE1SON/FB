import os
import subprocess
from typing import Optional, Dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio")

WORSHIP_TRACKS: Dict[str, str] = {
    "worship_piano_peace": "🕊️ Piano de Paz (Adoración Íntima y Pad Suave)",
    "celestial_strings_hope": "🌅 Cuerdas Celestiales (Esperanza y Victoria)",
    "midnight_prayer_acoustic": "🛌 Oración Nocturna (Ambiente Profundo de Reposo)",
    "none": "🔇 Sin Música de Fondo (Solo Voz)"
}

EFFECTS: Dict[str, str] = {
    "cinematic_dust": "✨ Polvo de Oro Divino (Partículas doradas)",
    "divine_light": "☀️ Rayos de Luz Celestial (Aura dorada y resplandor visible)",
    "dramatic_grain": "🎬 Grano de Cine Épico (Textura 35mm y alto contraste)",
    "celestial_glow": "🕊️ Resplandor de Gloria (Niebla mística y difusión divina)",
    "golden_hour": "🌅 Hora Dorada Sagrada (Luz cálida de atardecer de oración)",
    "holy_fire": "🔥 Fuego del Espíritu Santo (Tonos fuego y victoria espiritual)",
    "none": "🖼️ Sin Efectos (Imagen Limpia y Pura)"
}

CAMERA_MOTIONS: Dict[str, str] = {
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
    """Extrae la duración exacta del audio con ffprobe."""
    cmd = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", audio_path
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(res.stdout.strip())


def _resolve_music_file(music_track: str) -> Optional[str]:
    """Resuelve la ruta absoluta del archivo de música seleccionado."""
    if music_track and music_track != "none":
        candidate = os.path.join(AUDIO_DIR, f"{music_track}.mp3")
        if os.path.exists(candidate):
            return candidate
    return None


def _is_video_file(file_path: Optional[str]) -> bool:
    """Comprueba si el archivo es un video (.mp4, .mov, .webm)."""
    if not file_path:
        return False
    ext = os.path.splitext(file_path)[1].lower()
    return ext in [".mp4", ".mov", ".webm", ".mkv"]


def _get_zoompan_expr(motion: str, tf: int, w: int, h: int, fps: int = 30) -> str:
    """Genera la expresión FFmpeg zoompan según el movimiento de cámara seleccionado."""
    tf = max(tf, 30)
    m = motion.lower().strip() if motion else "zoom_in"

    if m == "zoom_out":
        return f"zoompan=z='1.12-(0.09*on/{tf})':d={tf}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}"
    elif m == "pan_up":
        return f"zoompan=z=1.06:d={tf}:x='iw/2-(iw/zoom/2)':y='(ih-(ih/zoom))*(1.0-on/{tf})':s={w}x{h}:fps={fps}"
    elif m == "pan_down":
        return f"zoompan=z=1.06:d={tf}:x='iw/2-(iw/zoom/2)':y='(ih-(ih/zoom))*(on/{tf})':s={w}x{h}:fps={fps}"
    elif m == "pan_right":
        return f"zoompan=z=1.06:d={tf}:x='(iw-(iw/zoom))*(on/{tf})':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}"
    elif m == "pan_left":
        return f"zoompan=z=1.06:d={tf}:x='(iw-(iw/zoom))*(1.0-on/{tf})':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}"
    elif m == "zoom_in_pan_up":
        return f"zoompan=z='1.0+(0.08*on/{tf})':d={tf}:x='iw/2-(iw/zoom/2)':y='(ih-(ih/zoom))*(1.0-on/{tf})':s={w}x{h}:fps={fps}"
    elif m == "none":
        return f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps}"
    else:  # default zoom_in
        return f"zoompan=z='1.0+(0.09*on/{tf})':d={tf}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps}"


def build_3scene_video_filter(
    inputs: list,
    w: int, h: int,
    effect_type: str,
    norm_ass: str,
    duration: float,
    camera_motion: str = "zoom_in",
    fps: int = 30,
    transition_style: str = "fade"
) -> str:
    """
    Construye el filter_complex de FFmpeg con soporte unificado para:
    - Videos B-Roll o Imágenes estáticas con movimiento de cámara real.
    - Transiciones cinemáticas encadenadas (xfade).
    - Etalonaje de color profesional.
    - Burn-in de subtítulos ASS sincronizados.
    """
    filters = []

    t2 = round(max(duration * 0.60, 4.2), 2)
    d1 = 0.35
    d2 = 0.50
    offset1 = round(max(3.20 - d1, 0.5), 2)
    offset2 = round(max(t2 - d2, offset1 + 1.2), 2)

    dur1 = offset1 + d1 + 0.5
    dur2 = (offset2 - offset1) + d2 + 0.5
    dur3 = (duration - offset2) + 1.0

    tf1 = max(int(dur1 * fps), 30)
    tf2 = max(int(dur2 * fps), 30)
    tf3 = max(int(dur3 * fps), 30)

    # Función auxiliar para encuadre inteligente sin recortes en 1:1
    def _get_scene_base_filter(idx: int, motion_expr: str) -> str:
        if w == h:
            # Encuadre inteligente 1:1 (Square Feed): Fondo con resplandor difuminado + primer plano completo sin cortes
            return (
                f"[{idx}:v]split=2[bg_raw_{idx}][fg_raw_{idx}];"
                f"[bg_raw_{idx}]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},gblur=sigma=22,eq=brightness=-0.12[bg_{idx}];"
                f"[fg_raw_{idx}]scale={w}:{h}:force_original_aspect_ratio=decrease[fg_{idx}];"
                f"[bg_{idx}][fg_{idx}]overlay=(W-w)/2:(H-h)/2,setsar=1,"
                f"{motion_expr}"
            )
        else:
            return (
                f"[{idx}:v]scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,"
                f"{motion_expr}"
            )

    # Procesar entrada 1
    if _is_video_file(inputs[0]):
        s1 = (
            f"[0:v]loop=loop=-1:size=2:start=0,"
            f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps},"
            f"trim=0:{dur1:.2f},setpts=PTS-STARTPTS[v1]"
        )
    else:
        motion_expr_1 = _get_zoompan_expr(camera_motion, tf1, w, h, fps)
        base_1 = _get_scene_base_filter(0, motion_expr_1)
        s1 = (
            f"{base_1},"
            f"split=2[v1_sharp][v1_blur_in];"
            f"[v1_blur_in]gblur=sigma=10[v1_blurred];"
            f"[v1_sharp][v1_blurred]blend=all_expr='if(lt(T,0.30), B*(1-T/0.30)+A*(T/0.30), A)',"
            f"eq=brightness='if(lt(t,0.35), 0.12*(1-t/0.35), 0)'[v1]"
        )
    filters.append(s1)

    # Procesar entrada 2
    if _is_video_file(inputs[1]):
        s2 = (
            f"[1:v]loop=loop=-1:size=2:start=0,"
            f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps},"
            f"trim=0:{dur2:.2f},setpts=PTS-STARTPTS[v2]"
        )
    else:
        # Alternar movimiento cinemático para escena 2
        alt_motion = "pan_up" if camera_motion == "zoom_in" else "zoom_in"
        motion_expr_2 = _get_zoompan_expr(alt_motion, tf2, w, h, fps)
        s2 = f"{_get_scene_base_filter(1, motion_expr_2)}[v2]"
    filters.append(s2)

    # Procesar entrada 3
    if _is_video_file(inputs[2]):
        s3 = (
            f"[2:v]loop=loop=-1:size=2:start=0,"
            f"scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},setsar=1,fps={fps},"
            f"trim=0:{dur3:.2f},setpts=PTS-STARTPTS[v3]"
        )
    else:
        motion_expr_3 = _get_zoompan_expr(camera_motion, tf3, w, h, fps)
        s3 = f"{_get_scene_base_filter(2, motion_expr_3)}[v3]"
    filters.append(s3)

    # Transiciones encadenadas xfade
    valid_transitions = {
        "fade", "fadewhite", "circlecrop", "dissolve", "smoothup",
        "hblur", "wipeleft", "fadeblack", "radial", "slideup"
    }
    trans = transition_style.lower().strip() if (transition_style and transition_style.lower().strip() in valid_transitions) else "fade"

    blend_filter = (
        f"[v1][v2]xfade=transition={trans}:duration={d1}:offset={offset1}[v12];"
        f"[v12][v3]xfade=transition={trans}:duration={d2}:offset={offset2}[motion]"
    )
    filters.append(blend_filter)

    # Visual Grading Effects
    fx_parts = []
    if effect_type == "cinematic_dust":
        fx_parts.append("colorchannelmixer=rr=1.05:gg=1.02:bb=0.96")
        fx_parts.append("vignette=PI/3.6")
    elif effect_type == "divine_light":
        fx_parts.append("eq=brightness=0.07:contrast=1.25:saturation=1.28")
        fx_parts.append("colorbalance=rs=0.18:gs=0.08:bs=-0.12:rm=0.12:gm=0.06:bm=-0.08")
        fx_parts.append("vignette=PI/4.0")
    elif effect_type == "dramatic_grain":
        fx_parts.append("noise=alls=35:allf=t+u")
        fx_parts.append("eq=contrast=1.30:saturation=0.82")
        fx_parts.append("vignette=PI/3.2")
    elif effect_type == "celestial_glow":
        fx_parts.append("eq=brightness=0.10:contrast=1.20:saturation=1.20")
        fx_parts.append("colorbalance=rs=0.12:gs=0.10:bs=0.02")
        fx_parts.append("vignette=PI/4.2")
    elif effect_type == "golden_hour":
        fx_parts.append("colorbalance=rs=0.24:gs=0.12:bs=-0.18:rh=0.18:gh=0.08:bh=-0.20")
        fx_parts.append("eq=saturation=1.35:contrast=1.20")
        fx_parts.append("vignette=PI/3.8")
    elif effect_type == "holy_fire":
        fx_parts.append("colorbalance=rh=0.12:gh=0.05:bh=-0.14:rm=0.05:gm=0.02:bm=-0.06")
        fx_parts.append("eq=contrast=1.16:saturation=1.10:brightness=0.02")
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
    camera_motion: str = "zoom_in",
    music_track: str = "worship_piano_peace",
    music_volume: float = 0.20,
    fps: int = 30,
    image_path_2: Optional[str] = None,
    image_path_3: Optional[str] = None,
    transition_style: str = "fade"
) -> str:
    """
    Renderiza el Reel vertical 1080x1920 con el pipeline de 3 escenas,
    movimiento de cámara respetado, música balanceada y subtítulos ASS dinámicos.
    """
    duration = get_audio_duration(audio_path)
    norm_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    music_file = _resolve_music_file(music_track)

    if aspect_ratio == "1:1":
        w, h = 1080, 1080
    elif aspect_ratio == "16:9":
        w, h = 1920, 1080
    else:  # default 9:16 vertical
        w, h = 1080, 1920

    # Resolver las 3 fuentes
    inp1 = image_path if (image_path and os.path.exists(image_path)) else None
    inp2 = image_path_2 if (image_path_2 and os.path.exists(image_path_2)) else inp1
    inp3 = image_path_3 if (image_path_3 and os.path.exists(image_path_3)) else inp1

    if not inp1:
        raise FileNotFoundError(f"Archivo de fondo principal no encontrado: {image_path}")

    inputs = [inp1, inp2, inp3]

    video_filter = build_3scene_video_filter(
        inputs=inputs,
        w=w, h=h,
        effect_type=effect_type,
        norm_ass=norm_ass,
        duration=duration,
        camera_motion=camera_motion,
        fps=fps,
        transition_style=transition_style
    )

    cmd = ["ffmpeg", "-y", "-threads", "4"]
    cmd.extend(["-i", inp1, "-i", inp2, "-i", inp3])
    cmd.extend(["-i", audio_path])
    audio_idx = 3

    if music_file:
        cmd.extend(["-i", music_file])
        music_idx = audio_idx + 1
        fade_out_start = max(0.0, duration - 2.0)
        audio_filter = (
            f"[{audio_idx}:a]volume=1.0[maina];"
            f"[{music_idx}:a]volume={music_volume:.2f},afade=t=in:st=0:d=1.5,afade=t=out:st={fade_out_start:.2f}:d=2.0[musica];"
            f"[maina][musica]amix=inputs=2:duration=first:dropout_transition=2[a]"
        )
        filter_complex = f"{video_filter};{audio_filter}"
        cmd.extend(["-filter_complex", filter_complex, "-map", "[v]", "-map", "[a]"])
    else:
        filter_complex = video_filter
        cmd.extend(["-filter_complex", filter_complex, "-map", "[v]", "-map", f"{audio_idx}:a"])

    cmd.extend([
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{duration:.2f}",
        output_mp4_path
    ])

    print(f"[Render Reel] Ratio: {w}x{h}, Motion: {camera_motion}, FX: {effect_type}, Dur: {duration:.2f}s")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg rendering falló: {result.stderr[-600:]}")

    return output_mp4_path
