from typing import List
import random
import re
from .tts import CueItem

def format_ass_time(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"

# ─── Verified Linux/Windows Installed Fonts ──────────────────────────────────
# Anton: The #1 viral TikTok/Instagram Reels bold headline font.
# Bebas Neue: Tall, condensed, powerful modern gospel style.
# Liberation Serif: Sacred, biblical scriptures & reverent prayers.
# Roboto: Crisp modern clean aesthetic.

SUBTITLE_STYLES = {
    "gold_highlight": {
        "name": "🌟 Oro Viral (Anton - Blanco con Resalte Dorado)",
        "font": "Anton",
        "primary": "&H00FFFFFF&",    # Blanco puro
        "highlight": "&H0000D7FF&",  # Oro cálido (#FFD700 BGR)
        "outline": "&H00000000&",    # Negro absoluto
        "outline_width": 6,
        "shadow_width": 2,
        "fontsize": 84,
        "border_style": 1,
        "back_color": "&H80000000&"
    },
    "neon_cyan": {
        "name": "⚡ Neón Eléctrico (Bebas Neue - Blanco con Resalte Lima)",
        "font": "Bebas Neue",
        "primary": "&H00FFFFFF&",
        "highlight": "&H00CCFF00&",  # Cyan lima brillante
        "outline": "&H00000000&",
        "outline_width": 6,
        "shadow_width": 2,
        "fontsize": 96,
        "border_style": 1,
        "back_color": "&H80000000&"
    },
    "holy_scripture": {
        "name": "📖 Escritura Sagrada (Liberation Serif - Clásico Bíblico)",
        "font": "Liberation Serif",
        "primary": "&H00F0F8FF&",    # Marfil celestial suave
        "highlight": "&H0030C0FF&",  # Ámbar sagrado
        "outline": "&H00000000&",
        "outline_width": 5,
        "shadow_width": 3,
        "fontsize": 78,
        "border_style": 1,
        "back_color": "&H80000000&"
    },
    "fire_coral": {
        "name": "🔥 Fuego & Pasión (Anton - Blanco con Fuego)",
        "font": "Anton",
        "primary": "&H00FFFFFF&",
        "highlight": "&H002257FF&",  # Naranja fuego vibrante
        "outline": "&H00000000&",
        "outline_width": 6,
        "shadow_width": 2,
        "fontsize": 84,
        "border_style": 1,
        "back_color": "&H80000000&"
    },
    "black_box": {
        "name": "🏷️ Cartela Moderna (Roboto - Amarillo en Caja Negra)",
        "font": "Roboto",
        "primary": "&H0000FFFF&",    # Amarillo vibrante
        "highlight": "&H00FFFFFF&",  # Blanco
        "outline": "&H00000000&",
        "outline_width": 2,
        "shadow_width": 0,
        "fontsize": 76,
        "border_style": 3,           # Opaque background box
        "back_color": "&HA0000000&"  # Fondo negro translúcido
    },
    "pure_minimal": {
        "name": "⚪ Cine Minimalista (Roboto - Blanco Puro Suave)",
        "font": "Roboto",
        "primary": "&H00FFFFFF&",
        "highlight": "&H0080FFFF&",  # Amarillo sutil
        "outline": "&H00000000&",
        "outline_width": 5,
        "shadow_width": 3,
        "fontsize": 74,
        "border_style": 1,
        "back_color": "&H80000000&"
    }
}

FAITH_POWER_WORDS = {
    "GOD", "JESUS", "LORD", "CHRIST", "AMEN", "PRAY", "PRAYER", "FAITH",
    "HEAL", "HEALING", "HEALED", "MIRACLE", "MIRACLES", "PEACE", "STORM",
    "FEAR", "STRENGTH", "PROMISE", "BLESSED", "BLESSING", "RESTORE",
    "DOOR", "DOORS", "BREAKTHROUGH", "TEARS", "VALLEY", "SHIELD",
    "VICTORY", "WARFARE", "FAMILY", "CHILD", "CHILDREN", "FREEDOM",
    "CHAINS", "FORGIVE", "TODAY", "TONIGHT", "STOP", "SCROLLING", "SAVE",
    "PROTECT", "LOVE", "LIGHT", "HOPE", "HEAR", "ANSWER", "HOLY", "SPIRIT",
    "GRACE", "BLOOD", "FIRE", "CROSS", "HEAVEN", "ANGEL", "ANGELS"
}


def _group_cues_into_chunks(cues: List[CueItem], max_words: int = 3) -> List[List[CueItem]]:
    """Group word cues into natural 2-3 word clusters with boundary checks."""
    chunks = []
    i = 0
    n = len(cues)
    while i < n:
        chunk = []
        # Decide chunk size: 2 or 3 words
        target_size = max_words if (i + max_words <= n) else (n - i)
        for j in range(target_size):
            item = cues[i + j]
            chunk.append(item)
            # Break early if word ends with terminal punctuation (. ? !)
            clean_word = item.text.strip()
            if clean_word.endswith((".", "!", "?")):
                break
        chunks.append(chunk)
        i += len(chunk)
    return chunks


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
    Genera subtítulos ASS dinámicos con amplia variedad de fuentes, posiciones y animaciones.
    Sincronización milimétrica derivada de Whisper + Piper TTS.
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
        alignment = 5  # Middle-center
        margin_v_calc = 0
    elif position == "top":
        alignment = 8  # Top-center
        margin_v_calc = int(play_res_y * 0.12)
    else:  # bottom
        alignment = 2  # Bottom-center
        margin_v_calc = margin_v

    # HookBold: large centered text for the visual hook (Anton / High contrast yellow)
    hook_style_line = ""
    if hook_text:
        hook_fontsize = 94 if play_res_y > 1080 else 74
        hook_margin_v = int(play_res_y * 0.24) if position != "top" else int(play_res_y * 0.40)
        hook_style_line = f"\nStyle: HookBold,Anton,{hook_fontsize},&H0000FFFF&,&H00FFFFFF&,&H00000000&,&HD0000000&,-1,0,0,0,100,100,3,0,1,8,4,5,50,50,{hook_margin_v},1"

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

    # 1. Partículas Cinemáticas Flotantes
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
                color = "00D7FF"  # Oro puro
                alpha = random.choice(["00", "15", "2A", "40"])
            elif effect_type == "holy_fire":
                char = random.choice(["✦", "●"])
                color = random.choice(["0022FF", "0055FF", "0088FF", "00D7FF"])
                alpha = random.choice(["00", "10", "25"])
            elif effect_type == "celestial_glow":
                char = "●"
                color = random.choice(["FFFFFF", "E0F7FF", "C0FFFF"])
                alpha = random.choice(["10", "25", "40"])
                blur = random.randint(8, 20)
            elif effect_type == "golden_hour":
                char = "●"
                color = random.choice(["00B4FF", "00C8FF", "00D7FF"])
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
        events.append(f"Dialogue: 2,0:00:00.00,0:00:02.50,HookBold,,0,0,0,,{{\\fscx118\\fscy118\\t(0,180,\\fscx100\\fscy100)\\fad(100,450)\\an5}}{hook_text.upper()}")

    # 3. Subtítulos Sincronizados Milimétricamente
    # Definición de animación según selección del usuario
    if animation_type == "pop":
        anim_tag = "\\fscx120\\fscy120\\t(0,85,\\fscx100\\fscy100)"
    elif animation_type == "fade":
        anim_tag = "\\fad(100,50)"
    elif animation_type == "scale_slow":
        anim_tag = "\\fscx92\\fscy92\\t(0,250,\\fscx106\\fscy106)"
    elif animation_type == "glow":
        anim_tag = "\\blur6\\t(0,100,\\blur1)"
    else:
        anim_tag = ""

    chunks = _group_cues_into_chunks(cues, max_words=3)

    for chunk in chunks:
        if not chunk:
            continue

        chunk_start = chunk[0].start_sec
        chunk_end = max(chunk[-1].end_sec, chunk_start + 0.35)

        t_start_str = format_ass_time(chunk_start)
        t_end_str = format_ass_time(chunk_end)

        # Build formatted text with intelligent keyword highlighting
        word_texts = [c.text.strip() for c in chunk]
        
        # Find which word (if any) is a faith power word
        highlight_idx = None
        for idx, w in enumerate(word_texts):
            clean_token = re.sub(r'[^A-Za-z]', '', w).upper()
            if clean_token in FAITH_POWER_WORDS:
                highlight_idx = idx
                break

        formatted_tokens = []
        for idx, w in enumerate(word_texts):
            w_upper = w.upper()
            if idx == highlight_idx and highlight_bgr != primary:
                # Highlight faith keyword
                formatted_tokens.append(f"{{\\c{highlight_bgr}&}}{w_upper}{{\\c{primary}&}}")
            else:
                formatted_tokens.append(w_upper)

        line_content = " ".join(formatted_tokens)
        anim_prefix = f"{{{anim_tag}}}" if anim_tag else ""
        events.append(f"Dialogue: 2,{t_start_str},{t_end_str},ViralMain,,0,0,0,,{anim_prefix}{line_content}")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    return output_path
