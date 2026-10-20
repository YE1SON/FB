import os
import subprocess
from typing import Optional, Dict, List, Tuple
from engine.audio import get_sfx_files

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio")

WORSHIP_TRACKS: Dict[str, str] = {
    "worship_piano_peace": "🕊️ Piano de Paz (Adoración Íntima y Pad Suave)",
    "celestial_strings_hope": "🌅 Cuerdas Celestiales (Esperanza y Victoria)",
    "midnight_prayer_acoustic": "🛌 Oración Nocturna (Ambiente Profundo de Reposo)",
    "none": "🔇 Sin Música de Fondo (Solo Voz)"
}

EFFECTS: Dict[str, str] = {
    "living_gold": "✨ Atmósfera Viva (Partículas y Luz Respirante)",
    "divine_rays": "☀️ Rayos Celestiales Dinámicos (Resplandor en Movimiento)",
    "sacred_candle": "🕯️ Parpadeo Cálido Íntimo (Vela Sagrada)",
    "angelic_shimmer": "🕊️ Destellos Angelicales (Brillo Continuo)",
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
) -> Tuple[str, float, float]:
    """
    Construye el filter_complex de FFmpeg con soporte unificado para:
    - Videos B-Roll o Imágenes estáticas con movimiento de cámara real.
    - Atmósfera Viva (Anti-Slideshow) con fluctuación de luz temporal y ruido orgánico.
    - Transiciones cinemáticas encadenadas (xfade).
    - Etalonaje de color profesional.
    - Burn-in de subtítulos ASS sincronizados.
    Retorna (filter_string, offset1, offset2)
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

    # Visual Grading Effects & Atmósfera Viva (Anti-Slideshow Plugin)
    fx_parts = []
    if effect_type == "living_gold":
        # Fluctuación orgánica de luz cálida + grano vivo temporal (meta-motion detector)
        fx_parts.append("eq=brightness='0.025*sin(2*PI*t/3.2)':contrast='1.18+0.04*cos(2*PI*t/4.1)':saturation=1.25")
        fx_parts.append("noise=alls=12:allf=t")
        fx_parts.append("colorchannelmixer=rr=1.06:gg=1.03:bb=0.94")
        fx_parts.append("vignette=PI/3.6")
    elif effect_type == "divine_rays":
        # Rayos celestiales con pulsación mística suave
        fx_parts.append("eq=brightness='0.03*sin(2*PI*t/2.8)':contrast='1.24+0.05*sin(2*PI*t/3.8)':saturation=1.28")
        fx_parts.append("colorbalance=rs=0.18:gs=0.09:bs=-0.12:rm=0.12:gm=0.06:bm=-0.08")
        fx_parts.append("vignette=PI/4.0")
    elif effect_type == "sacred_candle":
        # Parpadeo cálido de vela de oración
        fx_parts.append("eq=brightness='0.02*sin(2*PI*t/1.8)+0.01*sin(2*PI*t/0.9)':contrast=1.16:saturation=1.20")
        fx_parts.append("colorbalance=rs=0.16:gs=0.06:bs=-0.15")
        fx_parts.append("vignette=PI/3.5")
    elif effect_type == "angelic_shimmer":
        # Brillo angelical continuo
        fx_parts.append("eq=brightness='0.03*cos(2*PI*t/3.0)':contrast='1.20+0.03*sin(2*PI*t/2.5)':saturation=1.18")
        fx_parts.append("colorbalance=rs=0.08:gs=0.10:bs=0.06")
        fx_parts.append("vignette=PI/4.0")
    elif effect_type == "cinematic_dust":
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

    return ";".join(filters), offset1, offset2


def render_reel(
    image_path: str,
    audio_path: str,
    ass_path: str,
    output_mp4_path: str,
    aspect_ratio: str = "9:16",
    effect_type: str = "living_gold",
    camera_motion: str = "zoom_in",
    music_track: str = "worship_piano_peace",
    music_volume: float = 0.20,
    fps: int = 30,
    image_path_2: Optional[str] = None,
    image_path_3: Optional[str] = None,
    transition_style: str = "fade",
    enable_sfx: bool = True,
    generate_trending_audio_version: bool = True,
    seamless_loop: bool = False,
    master_lufs: bool = True
) -> Dict[str, str]:
    """
    Renderiza el Reel con la suite completa de 6 Plugins Algorítmicos:
    1. Anti-C2PA Sanitizer: Elimina metadatos de IA, inyecta perfiles de cámara móvil limpia.
    2. Living Atmosphere: Partículas vivas con variación temporal de luz contra el castigo de slideshow.
    3. Dual Export (Trending Audio Ready): Genera versión master + versión con voz limpia para audio viral de FB.
    4. Audio Punctuation (SFX): Sub-bass whoosh inicial (0s), swell sagrado y campanilla celestial.
    5. Seamless Loop: Cierre suave en el loop boundary sin cortes abruptos.
    6. Masterización Broadcast EBU R128 (-14 LUFS Meta Standard) para volumen perfecto en móviles.
    """
    duration = get_audio_duration(audio_path)
    norm_ass = os.path.abspath(ass_path).replace("\\", "/").replace(":", "\\:")
    music_file = _resolve_music_file(music_track)
    sfx_files = get_sfx_files()

    if aspect_ratio == "1:1":
        w, h = 1080, 1080
    elif aspect_ratio == "16:9":
        w, h = 1920, 1080
    else:  # default 9:16 vertical
        w, h = 1080, 1920

    # Resolver las 3 fuentes visuales
    inp1 = image_path if (image_path and os.path.exists(image_path)) else None
    inp2 = image_path_2 if (image_path_2 and os.path.exists(image_path_2)) else inp1
    inp3 = image_path_3 if (image_path_3 and os.path.exists(image_path_3)) else inp1

    if not inp1:
        raise FileNotFoundError(f"Archivo de fondo principal no encontrado: {image_path}")

    inputs = [inp1, inp2, inp3]

    video_filter, offset1, offset2 = build_3scene_video_filter(
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

    # Configurar SFX si están activos y existen los archivos
    has_sfx = enable_sfx and os.path.exists(sfx_files.get("whoosh", ""))
    sfx_input_indices = []
    if has_sfx:
        cmd.extend(["-i", sfx_files["whoosh"]]) # index 4
        sfx_input_indices.append(audio_idx + 1)
        if os.path.exists(sfx_files.get("swell", "")):
            cmd.extend(["-i", sfx_files["swell"]]) # index 5
            sfx_input_indices.append(audio_idx + 2)
        if os.path.exists(sfx_files.get("chime", "")):
            cmd.extend(["-i", sfx_files["chime"]]) # index 6
            sfx_input_indices.append(audio_idx + 3)

    music_idx = cmd.count("-i")  # índice exacto de entrada para el stream de música
    if music_file:
        cmd.extend(["-i", music_file])

    # Construir cadena de audio avanzada con Masterización LUFS y SFX
    audio_filters = []
    
    # 1. Ecualización de calidez vocal humana
    audio_filters.append(
        f"[{audio_idx}:a]equalizer=f=120:width_type=h:width=60:g=1.8,"
        f"equalizer=f=3300:width_type=h:width=1200:g=2.2,volume=1.0[voice_eq]"
    )

    # 2. Mezclar SFX si aplican
    if has_sfx and len(sfx_input_indices) >= 3:
        w_idx, s_idx, c_idx = sfx_input_indices[0], sfx_input_indices[1], sfx_input_indices[2]
        delay_swell_ms = int(max(offset1 * 1000 - 300, 1000))
        delay_chime_ms = int(max(offset2 * 1000 - 200, 3000))
        
        audio_filters.append(f"[{w_idx}:a]volume=0.55[sfx_w]")
        audio_filters.append(f"[{s_idx}:a]adelay={delay_swell_ms}|{delay_swell_ms},volume=0.38[sfx_s]")
        audio_filters.append(f"[{c_idx}:a]adelay={delay_chime_ms}|{delay_chime_ms},volume=0.32[sfx_c]")
        audio_filters.append(
            f"[voice_eq][sfx_w][sfx_s][sfx_c]amix=inputs=4:duration=first:dropout_transition=2[voice_and_sfx]"
        )
        pure_voice_label = "[voice_and_sfx]"
    else:
        pure_voice_label = "[voice_eq]"

    # 3. Mezclar Música o Salida Pura
    if music_file:
        # Fadeout según Bucle Infinito o estándar
        fade_dur = 1.0 if seamless_loop else 2.0
        fade_out_start = max(0.0, duration - fade_dur)
        audio_filters.append(
            f"[{music_idx}:a]volume={music_volume:.2f},"
            f"afade=t=in:st=0:d=1.2,afade=t=out:st={fade_out_start:.2f}:d={fade_dur:.2f}[musica]"
        )
        audio_filters.append(
            f"{pure_voice_label}[musica]amix=inputs=2:duration=first:dropout_transition=2[a_mixed]"
        )
        final_a_label = "[a_mixed]"
    else:
        final_a_label = pure_voice_label

    # 4. Masterización Broadcast Meta -14 LUFS
    if master_lufs:
        audio_filters.append(f"{final_a_label}loudnorm=I=-14:TP=-1.0:LRA=7[a_final]")
        a_out_target = "[a_final]"
    else:
        a_out_target = final_a_label

    full_filter_complex = f"{video_filter};{';'.join(audio_filters)}"
    cmd.extend(["-filter_complex", full_filter_complex, "-map", "[v]", "-map", a_out_target])

    # Sanitización de metadatos C2PA y perfil móvil limpio
    cmd.extend([
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "23", "-pix_fmt", "yuv420p",
        "-c:a", "aac", "-b:a", "192k",
        "-t", f"{duration:.2f}",
        "-map_metadata", "-1",
        "-fflags", "+bitexact",
        "-flags:v", "+bitexact",
        "-flags:a", "+bitexact",
        "-metadata:g", "encoder=Apple QuickTime",
        "-metadata:g", "comment=",
        "-metadata:g", "artist=",
        "-metadata:g", "title=",
        "-movflags", "+faststart",
        output_mp4_path
    ])

    print(f"[Render Reel] Ratio: {w}x{h}, Motion: {camera_motion}, FX: {effect_type}, Dur: {duration:.2f}s, SFX={has_sfx}, LUFS={master_lufs}")
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg rendering falló: {result.stderr[-600:]}")

    trending_mp4_path = output_mp4_path.replace(".mp4", "_trending_audio.mp4")

    # Plugin 3: Generación de la Versión "Trending Audio Ready" (Voz + SFX sin música)
    if generate_trending_audio_version and music_file:
        try:
            # Extraer audio limpio con SFX y masterizado en un archivo temporal
            temp_clean_audio = output_mp4_path.replace(".mp4", "_temp_clean_audio.wav")
            af_clean = [
                f"[{audio_idx}:a]equalizer=f=120:width_type=h:width=60:g=1.8,equalizer=f=3300:width_type=h:width=1200:g=2.2,volume=1.0[v_clean]"
            ]
            if has_sfx and len(sfx_input_indices) >= 3:
                af_clean.append(f"[{w_idx}:a]volume=0.55[sfx_w2]")
                af_clean.append(f"[{s_idx}:a]adelay={delay_swell_ms}|{delay_swell_ms},volume=0.38[sfx_s2]")
                af_clean.append(f"[{c_idx}:a]adelay={delay_chime_ms}|{delay_chime_ms},volume=0.32[sfx_c2]")
                af_clean.append("[v_clean][sfx_w2][sfx_s2][sfx_c2]amix=inputs=4:duration=first:dropout_transition=2[v_sfx2]")
                af_clean.append("[v_sfx2]loudnorm=I=-14:TP=-1.0:LRA=7[clean_final]")
            else:
                af_clean.append("[v_clean]loudnorm=I=-14:TP=-1.0:LRA=7[clean_final]")

            cmd_clean_a = ["ffmpeg", "-y"]
            cmd_clean_a.extend(["-i", audio_path])
            if has_sfx:
                cmd_clean_a.extend(["-i", sfx_files["whoosh"], "-i", sfx_files["swell"], "-i", sfx_files["chime"]])
            
            # Recalcular índices para el subcomando de audio
            if has_sfx:
                sub_filter = (
                    "[0:a]equalizer=f=120:width_type=h:width=60:g=1.8,equalizer=f=3300:width_type=h:width=1200:g=2.2[v0];"
                    f"[1:a]volume=0.55[w0];[2:a]adelay={delay_swell_ms}|{delay_swell_ms},volume=0.38[s0];[3:a]adelay={delay_chime_ms}|{delay_chime_ms},volume=0.32[c0];"
                    "[v0][w0][s0][c0]amix=inputs=4:duration=first:dropout_transition=2,loudnorm=I=-14:TP=-1.0:LRA=7[a_clean_out]"
                )
            else:
                sub_filter = "[0:a]equalizer=f=120:width_type=h:width=60:g=1.8,equalizer=f=3300:width_type=h:width=1200:g=2.2,loudnorm=I=-14:TP=-1.0:LRA=7[a_clean_out]"

            cmd_clean_a.extend(["-filter_complex", sub_filter, "-map", "[a_clean_out]", "-t", f"{duration:.2f}", temp_clean_audio])
            subprocess.run(cmd_clean_a, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

            # Ensamblar con el video maestro en 0.5s usando -c:v copy
            cmd_mux = [
                "ffmpeg", "-y",
                "-i", output_mp4_path,
                "-i", temp_clean_audio,
                "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k",
                "-map", "0:v:0",
                "-map", "1:a:0",
                "-map_metadata", "-1",
                "-movflags", "+faststart",
                trending_mp4_path
            ]
            subprocess.run(cmd_mux, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            if os.path.exists(temp_clean_audio):
                os.remove(temp_clean_audio)
            print(f"[Trending Audio Ready] Exportado exitosamente: {trending_mp4_path}")
        except Exception as err:
            print(f"[Trending Audio Warning]: {err}. Duplicando video maestro.")
            trending_mp4_path = output_mp4_path
    else:
        # Si no había música, el propio output_mp4_path ya es "trending audio ready"
        trending_mp4_path = output_mp4_path

    return {
        "master_video": output_mp4_path,
        "trending_audio_video": trending_mp4_path
    }
