from typing import List
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

def generate_viral_ass(cues: List[CueItem], output_path: str, style_key: str = "gold_highlight", margin_v: int = 750, hook_text: str = "") -> str:
    """
    Genera subtítulos ASS dinámicos con amplia variedad de estilos para vídeos 9:16.
    Includes optional bold hook_text overlay in the first 2 seconds for scroll-stopping impact.
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

    # HookBold: large centered text for the visual hook (first 2 seconds, stops scroll)
    hook_style_line = ""
    if hook_text:
        hook_style_line = f"\nStyle: HookBold,{font},95,&H00FFFFFF&,&H0000FFFF&,&H00000000&,&HC0000000&,-1,0,0,0,100,100,3,0,1,8,4,5,60,60,480,1"

    header = f"""[Script Info]
Title: Christian Viral Subtitles
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ViralMain,{font},{fontsize},{primary},&H0000FFFF&,{outline},{back_color},-1,0,0,0,100,100,2,0,{border_style},{outline_w},{shadow_w},2,40,40,{margin_v},1{hook_style_line}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []

    # Hook text overlay: large bold text in center of screen for first 2 seconds
    if hook_text:
        events.append(f"Dialogue: 1,0:00:00.00,0:00:02.20,HookBold,,0,0,0,,{{\\fad(150,500)\\an5}}{hook_text.upper()}")

    for cue in cues:
        raw_words = cue.text.strip().split()
        if not raw_words:
            continue
            
        start_sec = cue.start_sec
        end_sec = cue.end_sec
        duration = max(end_sec - start_sec, 0.4)
        total_chars = sum(len(w) for w in raw_words)

        # Dividir en grupos dinámicos de 2 a 3 palabras
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

            if len(chunk) > 1 and highlight_bgr != primary:
                normal_part = " ".join(chunk[:-1]).upper()
                highlight_word = chunk[-1].upper()
                # Dynamic pop animation: scale up to 125%, then shrink back to 100% over 120ms
                text_formatted = f"{normal_part} {{\\c{highlight_bgr}&\\fscx125\\fscy125\\t(0,120,\\fscx100\\fscy100)}}{highlight_word}{{\\r}}"
            else:
                text_formatted = f"{{\\c{highlight_bgr}&\\fscx125\\fscy125\\t(0,120,\\fscx100\\fscy100)}}{' '.join(chunk).upper()}{{\\r}}"

            events.append(f"Dialogue: 0,{t_start_str},{t_end_str},ViralMain,,0,0,0,,{text_formatted}")
            cur_time = chunk_end

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")
        
    return output_path
