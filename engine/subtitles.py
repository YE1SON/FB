from typing import List
import random
from .tts import CueItem

def format_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

SUBTITLE_STYLES = {
    "gold_highlight": {
        "name": "🌟 Oro Viral (Blanco con Resalte Dorado)",
        "font": "Impact",
        "primary": "&H00FFFFFF&",    # Blanco puro
        "highlight": "&H00D7FF&",    # Oro cálido (#FFD700 BGR)
        "outline": "&H00000000&",    # Negro absoluto
        "outline_width": 6,
        "shadow_width": 2,
        "fontsize": 78,
        "border_style": 1,
        "back_color": "&H80000000&"
    },
    "neon_cyan": {
        "name": "⚡ Neón Eléctrico (Blanco con Resalte Cyan/Lima)",
        "font": "Impact",
        "primary": "&H00FFFFFF&",
        "highlight": "&H00CCFF00&",  # Cyan lima brillante
        "outline": "&H00000000&",
        "outline_width": 6,
        "shadow_width": 2,
        "fontsize": 78,
        "border_style": 1,
        "back_color": "&H80000000&"
    },
    "fire_coral": {
        "name": "🔥 Fuego & Pasión (Blanco con Resalte Coral Fuego)",
        "font": "Impact",
        "primary": "&H00FFFFFF&",
        "highlight": "&H002257FF&",  # Naranja fuego
        "outline": "&H00000000&",
        "outline_width": 6,
        "shadow_width": 2,
        "fontsize": 78,
        "border_style": 1,
        "back_color": "&H80000000&"
    },
    "royal_purple": {
        "name": "👑 Púrpura Sacro (Blanco con Resalte Magenta Real)",
        "font": "Impact",
        "primary": "&H00FFFFFF&",
        "highlight": "&H00FB40E0&",  # Magenta / Púrpura celestial
        "outline": "&H00000000&",
        "outline_width": 6,
        "shadow_width": 2,
        "fontsize": 78,
        "border_style": 1,
        "back_color": "&H80000000&"
    },
    "black_box": {
        "name": "🏷️ Cartela Moderna (Texto Amarillo en Caja Negra)",
        "font": "Impact",
        "primary": "&H0000FFFF&",    # Amarillo vibrante
        "highlight": "&H00FFFFFF&",  # Blanco
        "outline": "&H00000000&",
        "outline_width": 2,
        "shadow_width": 0,
        "fontsize": 74,
        "border_style": 3,           # Opaque background box
        "back_color": "&HA0000000&"  # Fondo negro translúcido
    },
    "pure_minimal": {
        "name": "⚪ Blanco Puro Minimalista (Cinematográfico)",
        "font": "Arial",
        "primary": "&H00FFFFFF&",
        "highlight": "&H00FFFFFF&",
        "outline": "&H00000000&",
        "outline_width": 5,
        "shadow_width": 3,
        "fontsize": 72,
        "border_style": 1,
        "back_color": "&H80000000&"
    }
}

def generate_viral_ass(
    cues: List[CueItem],
    output_path: str,
    style_key: str = "gold_highlight",
    margin_v: int = 450,
    hook_text: str = "",
    animation_type: str = "pop",
    position: str = "bottom",
    effect_type: str = "cinematic_dust",
    play_res_x: int = 1080,
    play_res_y: int = 1920
) -> str:
    """
    Genera subtítulos ASS dinámicos con amplia variedad de estilos, posiciones y animaciones.
    Además, inyecta partículas visuales de polvo de oro, destellos sagrados y fuegos en alta fidelidad.
    """
    style_cfg = SUBTITLE_STYLES.get(style_key, SUBTITLE_STYLES["gold_highlight"])
    font = style_cfg["font"]
    primary = style_cfg["primary"]
    highlight_bgr = style_cfg["highlight"]
    outline = style_cfg["outline"]
    outline_w = style_cfg["outline_width"]
    shadow_w = style_cfg["shadow_width"]
    fontsize = style_cfg["fontsize"]
    border_style = style_cfg.get("border_style", 1)
    back_color = style_cfg.get("back_color", "&H80000000&")

    # Adaptar tamaño de fuente si el formato es 1:1 o 16:9
    if play_res_y <= 1080:
        fontsize = int(fontsize * 0.85)

    # Configure alignment and margins based on user choice
    if position == "center":
        alignment = 5 # Middle-center
        margin_v_calc = 0
    elif position == "top":
        alignment = 8 # Top-center
        margin_v_calc = int(play_res_y * 0.12)
    else: # bottom
        alignment = 2 # Bottom-center
        margin_v_calc = margin_v

    # HookBold: large centered text for the visual hook (High contrast yellow & black border)
    hook_style_line = ""
    if hook_text:
        hook_fontsize = 92 if play_res_y > 1080 else 72
        hook_margin_v = int(play_res_y * 0.24) if position != "top" else int(play_res_y * 0.40)
        hook_style_line = f"\nStyle: HookBold,{font},{hook_fontsize},&H0000FFFF&,&H00FFFFFF&,&H00000000&,&HD0000000&,-1,0,0,0,100,100,3,0,1,8,4,5,50,50,{hook_margin_v},1"

    # Style para partículas cinemáticas
    particle_style_line = f"\nStyle: FXParticle,Arial,32,&H00D7FF&,&H00D7FF&,&H00D7FF&,&H000000&,1,0,0,0,100,100,0,0,1,0,0,5,10,10,10,1"

    header = f"""[Script Info]
Title: Christian Viral Subtitles & Effects
ScriptType: v4.00+
PlayResX: {play_res_x}
PlayResY: {play_res_y}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ViralMain,{font},{fontsize},{primary},&H0000FFFF&,{outline},{back_color},-1,0,0,0,100,100,2,0,{border_style},{outline_w},{shadow_w},{alignment},40,40,{margin_v_calc},1{hook_style_line}{particle_style_line}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    # 1. Partículas Cinemáticas Flotantes (Polvo de Oro, Resplandor de Gloria, Fuego Santo)
    total_dur = cues[-1].end_sec if cues else 20.0
    if effect_type in ["cinematic_dust", "golden_hour", "holy_fire", "celestial_glow"]:
        num_particles = 45
        for i in range(num_particles):
            t_start = round((i * (total_dur / float(num_particles))) * 0.9, 2)
            t_dur = random.uniform(4.0, 7.5)
            t_end = min(round(t_start + t_dur, 2), total_dur + 0.5)
            if t_end <= t_start:
                continue

            x1 = random.randint(int(play_res_x * 0.05), int(play_res_x * 0.95))
            x2 = x1 + random.randint(-60, 60)
            y1 = random.randint(int(play_res_y * 0.55), int(play_res_y * 1.05))
            y2 = y1 - random.randint(int(play_res_y * 0.45), int(play_res_y * 0.85))

            size = random.randint(20, 52)
            blur = random.randint(4, 14)

            if effect_type == "cinematic_dust":
                char = "●"
                color = "00D7FF" # Oro puro
                alpha = random.choice(["00", "15", "2A", "40"])
            elif effect_type == "holy_fire":
                char = random.choice(["✦", "●"])
                color = random.choice(["0022FF", "0055FF", "0088FF", "00D7FF"]) # Fuego y brasas
                alpha = random.choice(["00", "10", "25"])
            elif effect_type == "celestial_glow":
                char = "●"
                color = random.choice(["FFFFFF", "E0F7FF", "C0FFFF"]) # Blanco/Cyan angelical
                alpha = random.choice(["10", "25", "40"])
                blur = random.randint(8, 20)
            elif effect_type == "golden_hour":
                char = "●"
                color = random.choice(["00B4FF", "00C8FF", "00D7FF"]) # Ámbar cálido
                alpha = random.choice(["05", "18", "30"])
            else:
                char = "●"
                color = "00D7FF"
                alpha = "00"

            s_str = format_ass_time(t_start)
            e_str = format_ass_time(t_end)
            events.append(
                f"Dialogue: 1,{s_str},{e_str},FXParticle,,0,0,0,,{{\\an5\\move({x1},{y1},{x2},{y2})\\1c&H{alpha}{color}&\\3c&H{alpha}{color}&\\blur{blur}\\fad(400,400)\\fs{size}}}{char}"
            )

    # 2. Hook Visual Inicial (Pattern Interrupt en el segundo 0 a 2.5)
    if hook_text:
        events.append(f"Dialogue: 2,0:00:00.00,0:00:02.50,HookBold,,0,0,0,,{{\\fscx115\\fscy115\\t(0,180,\\fscx100\\fscy100)\\fad(100,450)\\an5}}{hook_text.upper()}")

    # 3. Subtítulos Sincronizados
    for cue in cues:
        raw_words = cue.text.strip().split()
        if not raw_words:
            continue

        start_sec = cue.start_sec
        end_sec = cue.end_sec
        duration = max(end_sec - start_sec, 0.4)
        total_chars = sum(len(w) for w in raw_words)

        chunk_size = 2 if len(raw_words) <= 6 else 3
        chunks = [raw_words[i:i + chunk_size] for i in range(0, len(raw_words), chunk_size)]

        cur_time = start_sec
        for idx, chunk in enumerate(chunks):
            chunk_chars = sum(len(w) for w in chunk)
            chunk_dur = duration * (chunk_chars / max(total_chars, 1))

            chunk_end = min(cur_time + chunk_dur, end_sec)
            if idx == len(chunks) - 1:
                chunk_end = end_sec

            t_start_str = format_ass_time(cur_time)
            t_end_str = format_ass_time(chunk_end)

            if animation_type == "pop":
                anim_tag = "\\fscx130\\fscy130\\t(0,120,\\fscx100\\fscy100)"
            elif animation_type == "fade":
                anim_tag = "\\alpha&HFF&\\t(0,250,\\alpha&H00&)"
            elif animation_type == "scale_slow":
                anim_tag = "\\fscx85\\fscy85\\t(0,400,\\fscx110\\fscy110)"
            else:
                anim_tag = ""

            chunk_text = " ".join(chunk).upper()
            color_prefix = "{\\c" + highlight_bgr + "&" + anim_tag + "}"
            reset_suffix = "{\\r}"

            if len(chunk) > 1 and highlight_bgr != primary:
                normal_part = " ".join(chunk[:-1]).upper()
                highlight_word = chunk[-1].upper()
                text_formatted = f"{normal_part} {color_prefix}{highlight_word}{reset_suffix}"
            else:
                text_formatted = f"{color_prefix}{chunk_text}{reset_suffix}"

            events.append(f"Dialogue: 2,{t_start_str},{t_end_str},ViralMain,,0,0,0,,{text_formatted}")
            cur_time = chunk_end

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    return output_path
