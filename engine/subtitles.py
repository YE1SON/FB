import os
import re
from typing import Dict, List, Optional
from .tts import CueItem

# =============================================================================
# JESUS REELS STUDIO v4.0 - ADVANCED DYNAMIC SUBTITLE SYSTEM (CapCut/TikTok)
# =============================================================================
# 4 Estilos Animados Completamente Diferenciados:
# 1. KARAOKE:   Resaltado palabra por palabra al milisegundo exacto de la locución.
# 2. POP:       Aumento cinético de escala (112%) y destello activo en la palabra hablada.
# 3. CINEMATIC: Frases breves, tipografía sagrada noble (Cinzel), fade suave y resalte sereno.
# 4. CLEAN:     Máxima legibilidad, fondo en cartela discreta (border_style=3), moderno y claro.
#
# Cumplimiento Estricto:
# - Zonas seguras de Facebook Reels (márgenes inferiores >420px, laterales >80px).
# - Preservación de mayúsculas/minúsculas naturales (sin forzar mayúsculas).
# - Insignias superiores desactivadas por defecto para no saturar.
# - División inteligente de líneas en bloques de 2 a 4 palabras sin desbordamiento.
# =============================================================================

SUBTITLE_STYLES: Dict[str, Dict] = {
    "karaoke": {
        "key": "karaoke",
        "name": "🎤 KARAOKE (Resaltado Palabra por Palabra — Estilo CapCut)",
        "font": "Montserrat",
        "primary": "&H00FFFFFF&",    # Blanco puro
        "highlight": "&H0000D7FF&",  # Oro cálido (#FFD700 en BGR)
        "outline": "&H00000000&",    # Negro absoluto
        "outline_width": 5,
        "shadow_width": 1,
        "fontsize": 78,
        "border_style": 1,
        "back_color": "&H80000000&",
        "bold": -1,
        "all_caps": False
    },
    "pop": {
        "key": "pop",
        "name": "💥 POP DINÁMICO (Salto Cinético y Color en Palabra Activa)",
        "font": "Anton",
        "primary": "&H00FFFFFF&",    # Blanco puro
        "highlight": "&H0000FFFF&",  # Amarillo vibrante (#FFFF00 en BGR)
        "outline": "&H00000000&",    # Borde negro sólido
        "outline_width": 6,
        "shadow_width": 2,
        "fontsize": 82,
        "border_style": 1,
        "back_color": "&H80000000&",
        "bold": -1,
        "all_caps": True
    },
    "cinematic": {
        "key": "cinematic",
        "name": "🎬 CINEMATIC NOBLE (Tipografía Sagrada Cinzel con Fade Elegante)",
        "font": "Cinzel",
        "primary": "&H00F4F4F4&",    # Marfil celestial
        "highlight": "&H0030C0FF&",  # Ámbar dorado divino
        "outline": "&H00000000&",    # Sombra suave
        "outline_width": 4,
        "shadow_width": 2,
        "fontsize": 72,
        "border_style": 1,
        "back_color": "&H90000000&",
        "bold": -1,
        "all_caps": False
    },
    "clean": {
        "key": "clean",
        "name": "🏷️ CLEAN PROFESSIONAL (Cartela Discreta y Alta Legibilidad)",
        "font": "Montserrat",
        "primary": "&H00FFFFFF&",    # Blanco limpio
        "highlight": "&H0080FFFF&",  # Amarillo suave
        "outline": "&H00000000&",
        "outline_width": 2,
        "shadow_width": 0,
        "fontsize": 70,
        "border_style": 3,           # Fondo de caja opaca redondeada
        "back_color": "&HA00E1520&",  # Slate oscuro translúcido
        "bold": 0,
        "all_caps": False
    }
}

# Palabras de fe para resalte inteligente en modo Cinematic
FAITH_KEYWORDS = {
    "god", "jesus", "lord", "christ", "amen", "pray", "prayer", "faith",
    "peace", "healing", "grace", "love", "mercy", "home", "family", "children",
    "strength", "comfort", "rest", "promise", "light", "hope", "presence",
    "freedom", "healed", "forgiven", "safe", "shelter", "victory"
}


def format_ass_time(seconds: float) -> str:
    """Convierte segundos flotantes al formato ASS H:MM:SS.cs"""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds - int(seconds)) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _chunk_cues(cues: List[CueItem], max_words: int = 3, max_chars: int = 24) -> List[List[CueItem]]:
    """
    Agrupa los cues de palabras en frases cortas de 2 a 4 palabras,
    respetando signos de puntuación terminales para no cortar pensamientos naturales.
    """
    chunks: List[List[CueItem]] = []
    current_chunk: List[CueItem] = []
    current_chars = 0

    for cue in cues:
        word = cue.text.strip()
        if not word:
            continue

        w_len = len(word)
        # Si agregar la palabra excede el límite de palabras o caracteres, cerrar chunk
        if current_chunk and (len(current_chunk) >= max_words or (current_chars + w_len + 1) > max_chars):
            chunks.append(current_chunk)
            current_chunk = []
            current_chars = 0

        current_chunk.append(cue)
        current_chars += w_len + 1

        # Si la palabra termina en puntuación mayor (. ! ? : ;), cortar el chunk de inmediato
        if word.endswith((".", "!", "?", ":", ";")):
            chunks.append(current_chunk)
            current_chunk = []
            current_chars = 0

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def generate_viral_ass(
    cues: List[CueItem],
    output_path: str,
    style_key: str = "karaoke",
    margin_v: int = 440,
    hook_text: str = "",
    micro_cta_text: str = "",
    hook_badge_style: str = "gold_cinematic",
    animation_type: str = "pop",
    position: str = "bottom",
    effect_type: str = "cinematic_dust",
    play_res_x: int = 1080,
    play_res_y: int = 1920,
    enable_hook_badge: bool = False,
    enable_micro_cta: bool = False,
    all_caps: Optional[bool] = None
) -> str:
    """
    Genera un archivo .ass optimizado para Facebook Reels:
    - 4 estilos animados reales: KARAOKE, POP, CINEMATIC, CLEAN.
    - Zonas seguras respetadas (MarginV por defecto 440 en 1080x1920).
    - Insignias superiores desactivadas por defecto (activables si el usuario lo desea).
    - Subtítulos siempre sincronizados palabra por palabra.
    """
    if not cues:
        cues = [CueItem(start_sec=0.0, end_sec=5.0, text="May the peace of Christ guard your home.")]

    style_cfg = SUBTITLE_STYLES.get(style_key, SUBTITLE_STYLES["karaoke"])
    font = style_cfg["font"]
    primary = style_cfg["primary"]
    highlight = style_cfg["highlight"]
    outline = style_cfg["outline"]
    outline_w = style_cfg["outline_width"]
    shadow_w = style_cfg["shadow_width"]
    fontsize = style_cfg["fontsize"]
    border_style = style_cfg.get("border_style", 1)
    back_color = style_cfg.get("back_color", "&H80000000&")
    bold = style_cfg.get("bold", -1)

    # Decidir si forzar mayúsculas
    use_caps = all_caps if (all_caps is not None) else style_cfg.get("all_caps", False)

    # Adaptar tamaño de fuente si el formato es 1:1 o 16:9
    if play_res_y <= 1080:
        fontsize = int(fontsize * 0.82)
        margin_v_safe = int(margin_v * 0.40)
    else:
        margin_v_safe = margin_v

    # Configuración de alineación según posición elegida
    if position == "center":
        alignment = 5  # Centrado en pantalla
        margin_v_calc = 0
    elif position == "top":
        alignment = 8  # Arriba en zona segura
        margin_v_calc = 300 if play_res_y > 1080 else 90
    else:  # bottom (default en zona segura Reels sobre descripción de FB)
        alignment = 2  # Abajo centrado
        margin_v_calc = margin_v_safe

    # Estilos de insignias superiores (solo si están habilitadas)
    badge_styles_block = ""
    if enable_hook_badge or enable_micro_cta:
        badge_styles_block = (
            f"\nStyle: HookBadge,Cinzel,42,&H00FFFFFF,&H000000FF,&H0000D7FF,&HE60A0E1A,-1,0,0,0,100,100,2,0,3,3,2,8,60,60,110,1"
            f"\nStyle: MicroCTABadge,Montserrat,34,&H00E0E0E0,&H000000FF,&H00808080,&HC00D1520,1,0,0,0,100,100,1,0,3,2,1,8,60,60,110,1"
        )

    header = f"""[Script Info]
Title: JesusReels Studio CapCut-Grade Subtitles
ScriptType: v4.00+
PlayResX: {play_res_x}
PlayResY: {play_res_y}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: MainSub,{font},{fontsize},{primary},&H000000FF&,{outline},{back_color},{bold},0,0,0,100,100,1,0,{border_style},{outline_w},{shadow_w},{alignment},80,120,{margin_v_calc},1{badge_styles_block}

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events: List[str] = []

    # 1. Insignias Opcionales
    if enable_hook_badge and hook_text:
        clean_hook = re.sub(r'^[^\w]+', '', hook_text).strip()
        if clean_hook:
            events.append(
                f"Dialogue: 3,0:00:00.00,0:00:03.20,HookBadge,,0,0,0,,{{\\an8\\fad(80,200)}}{clean_hook}"
            )

    if enable_micro_cta and micro_cta_text:
        clean_cta = re.sub(r'^[^\w]+', '', micro_cta_text).strip()
        if clean_cta:
            events.append(
                f"Dialogue: 3,0:00:03.40,0:00:07.50,MicroCTABadge,,0,0,0,,{{\\an8\\fad(200,200)}}{clean_cta}"
            )

    # 2. Generación Dinámica según Estilo
    max_w = 4 if style_key in ["karaoke", "clean"] else 3
    chunks = _chunk_cues(cues, max_words=max_w, max_chars=26)

    c_high = highlight if highlight.endswith("&") else f"{highlight}&"
    c_prim = primary if primary.endswith("&") else f"{primary}&"

    for chunk in chunks:
        if not chunk:
            continue

        chunk_start = chunk[0].start_sec
        chunk_end = max(chunk[-1].end_sec, chunk_start + 0.40)

        # ─── MODO 1: KARAOKE (Palabra por palabra activa sincrónica) ───────────
        if style_key == "karaoke":
            for active_idx, active_cue in enumerate(chunk):
                w_start = active_cue.start_sec
                w_end = active_cue.end_sec
                if w_end <= w_start:
                    w_end = w_start + 0.20

                s_time = format_ass_time(w_start)
                e_time = format_ass_time(w_end)

                formatted_words = []
                for idx, item in enumerate(chunk):
                    txt = item.text.upper() if use_caps else item.text
                    if idx == active_idx:
                        formatted_words.append(f"{{\\c{c_high}\\bord{outline_w+1}}}{txt}{{\\c{c_prim}\\bord{outline_w}}}")
                    else:
                        formatted_words.append(txt)

                line_text = " ".join(formatted_words)
                events.append(f"Dialogue: 2,{s_time},{e_time},MainSub,,0,0,0,,{line_text}")

        # ─── MODO 2: POP (Salto cinético con escala y destello de color) ───────
        elif style_key == "pop":
            for active_idx, active_cue in enumerate(chunk):
                w_start = active_cue.start_sec
                w_end = active_cue.end_sec
                if w_end <= w_start:
                    w_end = w_start + 0.20

                s_time = format_ass_time(w_start)
                e_time = format_ass_time(w_end)

                formatted_words = []
                for idx, item in enumerate(chunk):
                    txt = item.text.upper() if use_caps else item.text
                    if idx == active_idx:
                        formatted_words.append(f"{{\\fscx112\\fscy112\\t(0,70,\\fscx100\\fscy100)\\c{c_high}\\bord{outline_w+1}}}{txt}{{\\c{c_prim}\\bord{outline_w}}}")
                    else:
                        formatted_words.append(txt)

                line_text = " ".join(formatted_words)
                events.append(f"Dialogue: 2,{s_time},{e_time},MainSub,,0,0,0,,{line_text}")

        # ─── MODO 3: CINEMATIC (Frases breves, tipografía noble, fade y resalte de fe) ──
        elif style_key == "cinematic":
            s_time = format_ass_time(chunk_start)
            e_time = format_ass_time(chunk_end)

            formatted_words = []
            for item in chunk:
                clean_w = re.sub(r'[^A-Za-z]', '', item.text).lower()
                txt = item.text.upper() if use_caps else item.text
                if clean_w in FAITH_KEYWORDS and highlight != primary:
                    formatted_words.append(f"{{\\c{c_high}}}{txt}{{\\c{c_prim}}}")
                else:
                    formatted_words.append(txt)

            line_text = " ".join(formatted_words)
            events.append(f"Dialogue: 2,{s_time},{e_time},MainSub,,0,0,0,,{{\\fad(90,70)}}{line_text}")

        # ─── MODO 4: CLEAN (Cartela limpia, legible, moderna con fade sutil) ───
        else:
            s_time = format_ass_time(chunk_start)
            e_time = format_ass_time(chunk_end)

            words_txt = [(w.text.upper() if use_caps else w.text) for w in chunk]
            line_text = " ".join(words_txt)
            events.append(f"Dialogue: 2,{s_time},{e_time},MainSub,,0,0,0,,{{\\fad(70,50)}}{line_text}")

    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(header + "\n".join(events) + "\n")

    return output_path
