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

FAITH_KEYWORDS = {
    "god", "jesus", "lord", "christ", "faith", "pray", "prayer", "praying",
    "peace", "grace", "love", "hope", "amen", "glory", "holy", "spirit",
    "bless", "blessed", "blessing", "father", "mercy", "strength", "heart",
    "soul", "heavens", "heaven", "light", "cross"
}

# Presets de Insignia Superior (Hook Badge) — Modernos, tipo píldora / glassmorphic, sin tipografías anticuadas
HOOK_BADGE_PRESETS: Dict[str, Dict] = {
    "clean_glass": {
        "name": "🪟 Cristal Oscuro Minimalista (Píldora Moderna)",
        "font": "Montserrat",
        "fontsize": 42,
        "primary": "&H00FFFFFF&",    # Blanco puro
        "outline": "&H00302824&",
        "back_color": "&HA015111E&", # Píldora oscura translúcida
        "bold": -1,
        "outline_w": 2,
        "shadow_w": 0,
        "spacing": 2,
        "border_style": 3            # Cartela tipo píldora
    },
    "gold_luxury": {
        "name": "🌟 Oro Sagrado Elegante (Píldora Minimalista)",
        "font": "Montserrat",
        "fontsize": 42,
        "primary": "&H0025D4F5&",    # Oro cálido (#F5D425 en BGR)
        "outline": "&H00000000&",
        "back_color": "&HB00A0A0E&", # Píldora obsidiana profunda
        "bold": -1,
        "outline_w": 2,
        "shadow_w": 0,
        "spacing": 2,
        "border_style": 3
    },
    "viral_indigo": {
        "name": "⚡ Indigo Moderno (Estilo Estudio Viral)",
        "font": "Montserrat",
        "fontsize": 42,
        "primary": "&H00FFFFFF&",
        "outline": "&H00F16663&",    # Borde índigo/violeta
        "back_color": "&H95552070&", # Píldora violeta moderna
        "bold": -1,
        "outline_w": 2,
        "shadow_w": 0,
        "spacing": 2,
        "border_style": 3
    },
    "editorial_white": {
        "name": "📰 Editorial Blanco (Alto Contraste)",
        "font": "Montserrat",
        "fontsize": 40,
        "primary": "&H000F172A&",    # Texto oscuro slate
        "outline": "&H00FFFFFF&",
        "back_color": "&H15FFFFFF&", # Píldora blanca pura
        "bold": -1,
        "outline_w": 2,
        "shadow_w": 0,
        "spacing": 2,
        "border_style": 3
    },
    "sacred_fire": {
        "name": "🔥 Fuego Sagrado & Devoción",
        "font": "Cinzel",
        "fontsize": 44,
        "primary": "&H00F5F5FF&",    # Blanco cálido
        "outline": "&H001050E0&",    # Borde dorado ámbar
        "back_color": "&H90101580&", # Rojo carmesí profundo
        "bold": -1,
        "outline_w": 2,
        "shadow_w": 0,
        "spacing": 2,
        "border_style": 3
    }
}

# Mapeo de compatibilidad hacia atrás
HOOK_BADGE_PRESETS["gold_cinematic"] = HOOK_BADGE_PRESETS["gold_luxury"]
HOOK_BADGE_PRESETS["urgency_red"] = HOOK_BADGE_PRESETS["viral_indigo"]
HOOK_BADGE_PRESETS["royal_navy"] = HOOK_BADGE_PRESETS["clean_glass"]


def format_ass_time(seconds: float) -> str:
    """Convierte segundos flotantes al formato ASS H:MM:SS.cs con redondeo centesimal exacto."""
    total_cs = max(0, int(round(float(seconds) * 100)))
    h = total_cs // 360000
    m = (total_cs % 360000) // 6000
    s = (total_cs % 6000) // 100
    cs = total_cs % 100
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def _chunk_cues(cues: List[CueItem], max_words: int = 4, max_chars: int = 28) -> List[List[CueItem]]:
    """
    Agrupa los cues de palabras en frases legibles de 2 a 4 palabras,
    respetando pausas naturales y signos de puntuación (. ! ? , ; : —).
    Si un CueItem ya contiene varias palabras (por ejemplo de segment cues),
    se conserva íntegro sin fragmentación arbitraria.
    """
    chunks: List[List[CueItem]] = []
    current_chunk: List[CueItem] = []
    current_chars = 0

    for cue in cues:
        raw_text = cue.text.strip()
        if not raw_text:
            continue

        # Si el cue ya es una frase o cláusula completa procedente del estimador
        if " " in raw_text and len(raw_text.split()) > 2:
            if current_chunk:
                chunks.append(current_chunk)
                current_chunk = []
                current_chars = 0
            chunks.append([cue])
            continue

        w_len = len(raw_text)
        if current_chunk and (len(current_chunk) >= max_words or (current_chars + w_len + 1) > max_chars):
            chunks.append(current_chunk)
            current_chunk = []
            current_chars = 0

        current_chunk.append(cue)
        current_chars += w_len + 1

        if raw_text.endswith((".", "!", "?", ":", ";", "—")):
            chunks.append(current_chunk)
            current_chunk = []
            current_chars = 0

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def generate_viral_ass(
    cues: List[CueItem],
    output_path: str,
    style_key: str = "clean",
    margin_v: int = 440,
    hook_text: str = "",
    micro_cta_text: str = "",
    hook_badge_style: str = "gold_cinematic",
    hook_badge_font: Optional[str] = None,
    hook_badge_size: Optional[str] = "normal",
    animation_type: str = "pop",
    position: str = "bottom",
    effect_type: str = "cinematic_dust",
    play_res_x: int = 1080,
    play_res_y: int = 1920,
    enable_hook_badge: bool = False,
    enable_micro_cta: bool = False,
    all_caps: Optional[bool] = None,
    max_duration: Optional[float] = None
) -> str:
    """
    Genera un archivo .ass optimizado para Facebook Reels y videos verticales:
    - 4 estilos tipográficos: CLEAN (predeterminado), CINEMATIC, KARAOKE, POP.
    - Zonas seguras verticales respetadas (MarginV por defecto 440 en 1080x1920).
    - Agrupación semántica que garantiza un tiempo mínimo de lectura confortable (>=0.75s).
    - Acotado estricto a la duración real del audio (max_duration) para evitar subtítulos fantasma.
    """
    if not cues:
        cues = [CueItem(start_sec=0.0, end_sec=5.0, text="May the peace of Christ guard your home.")]

    # Límite superior del audio / transcripción disponible
    positive_ends = [float(cue.end_sec) for cue in cues if float(cue.end_sec) > 0]
    timeline_end_sec = max(positive_ends, default=5.0)
    if max_duration is not None and float(max_duration) > 0:
        timeline_end_sec = min(timeline_end_sec, float(max_duration))

    style_cfg = SUBTITLE_STYLES.get(style_key, SUBTITLE_STYLES["clean"])
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
        b_cfg = HOOK_BADGE_PRESETS.get(hook_badge_style, HOOK_BADGE_PRESETS["clean_glass"])
        b_font = hook_badge_font or b_cfg["font"]
        b_size = b_cfg["fontsize"]
        
        # Ajuste por tamaño seleccionado
        if hook_badge_size == "small":
            b_size = int(b_size * 0.85)
        elif hook_badge_size == "large":
            b_size = int(b_size * 1.22)
        elif hook_badge_size == "xlarge":
            b_size = int(b_size * 1.45)

        b_prim = b_cfg["primary"]
        b_out = b_cfg["outline"]
        b_bg = b_cfg["back_color"]
        b_bord = b_cfg["border_style"]
        b_ow = b_cfg["outline_w"]
        b_sh = b_cfg["shadow_w"]
        b_sp = b_cfg["spacing"]
        b_margin_v = 130 if play_res_y > 1080 else 48

        badge_styles_block = (
            f"\nStyle: HookBadge,{b_font},{b_size},{b_prim},&H000000FF&,{b_out},{b_bg},-1,0,0,0,100,100,{b_sp},0,{b_bord},{b_ow},{b_sh},8,60,60,{b_margin_v},1"
            f"\nStyle: MicroCTABadge,Montserrat,36,&H00E0E0E0,&H000000FF,&H00403020,&HB0121B2A,1,0,0,0,100,100,1,0,3,1,0,8,60,60,{b_margin_v},1"
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

    # 1. Insignias Opcionales con Temporalidad Desfasada (Cero saturación visual)
    # Gancho Visual: Segundos 0.0s a 3.5s (Apertura Scroll-Stopper)
    if enable_hook_badge and hook_text:
        clean_hook = re.sub(r'^[^\w]+', '', hook_text).strip()
        if clean_hook:
            events.append(
                f"Dialogue: 3,0:00:00.00,0:00:03.50,HookBadge,,0,0,0,,{{\\an8\\fad(80,250)}}{clean_hook.upper()}"
            )

    # Píldora de Invitación a Comentar (Micro-CTA): Segundos 4.5s a 9.5s (Segundo tercio)
    if enable_micro_cta and micro_cta_text:
        clean_cta = re.sub(r'^[^\w]+', '', micro_cta_text).strip()
        if clean_cta:
            events.append(
                f"Dialogue: 3,0:00:04.50,0:00:09.50,MicroCTABadge,,0,0,0,,{{\\an8\\fad(250,250)}}{clean_cta}"
            )

    # 2. Generación Dinámica según Estilo
    max_w = 4 if style_key in ["karaoke", "clean"] else 3
    chunks = _chunk_cues(cues, max_words=max_w, max_chars=26)

    c_high = highlight if highlight.endswith("&") else f"{highlight}&"
    c_prim = primary if primary.endswith("&") else f"{primary}&"

    for chunk in chunks:
        if not chunk:
            continue

        chunk_start = min(max(0.0, float(chunk[0].start_sec)), timeline_end_sec)
        raw_chunk_end = max(float(chunk[-1].end_sec), chunk_start + 0.75)
        chunk_end = min(raw_chunk_end, timeline_end_sec)
        if chunk_end <= chunk_start:
            continue

        # ─── MODO 1: KARAOKE (Palabra por palabra activa sincrónica) ───────────
        if style_key == "karaoke":
            for active_idx, active_cue in enumerate(chunk):
                w_start = min(max(0.0, float(active_cue.start_sec)), timeline_end_sec)
                raw_word_end = max(float(active_cue.end_sec), w_start + 0.20)
                w_end = min(raw_word_end, timeline_end_sec)
                if w_end <= w_start:
                    continue

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

        # ─── MODO 2: POP (Salto cinético con destello de color, base estable sin jitter) ───────
        elif style_key == "pop":
            for active_idx, active_cue in enumerate(chunk):
                w_start = min(max(0.0, float(active_cue.start_sec)), timeline_end_sec)
                raw_word_end = max(float(active_cue.end_sec), w_start + 0.20)
                w_end = min(raw_word_end, timeline_end_sec)
                if w_end <= w_start:
                    continue

                s_time = format_ass_time(w_start)
                e_time = format_ass_time(w_end)

                formatted_words = []
                for idx, item in enumerate(chunk):
                    txt = item.text.upper() if use_caps else item.text
                    if idx == active_idx:
                        # Resalte de alta visibilidad: destello de color y borde de glow,
                        # manteniendo estricto \fscy100 para evitar cualquier salto vertical o jitter
                        formatted_words.append(f"{{\\c{c_high}\\bord{outline_w+2}\\3c{c_high}}}{txt}{{\\c{c_prim}\\bord{outline_w}\\3c{outline}}}")
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
