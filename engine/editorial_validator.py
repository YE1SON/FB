"""
JESUSREELS STUDIO - EDITORIAL SAFETY & VALIDATION ENGINE
Verificador editorial previo a la publicación y exportación para FaithSpark Daily.
Previene errores de publicación sin bloquear falsos positivos:
- Detección de texto accidental en español en copys públicos en inglés.
- Detección de CTAs manipulativos o condicionados ("type Amen", "claim your miracle").
- Verificación de citas bíblicas canónicas contra el catálogo verificado.
- Verificación de coherencia temática entre el guion aprobado y la descripción.
- Detección de contenido repetido o idéntico a publicaciones recientes.
"""

import re
from typing import Dict, List, Optional, Any
from engine.scripts import BIBLICAL_CATALOGUE

# Palabras en español comunes que podrían filtrarse accidentalmente en copys en inglés
SPANISH_LEAK_WORDS = {
    "oracion", "oración", "señor", "senor", "dios", "hijos", "hijo", "hija",
    "fe", "paz", "noche", "dia", "día", "amen", "amén", "bendicion", "bendición",
    "esperanza", "familia", "gracia", "corazon", "corazón", "salvacion", "salvación",
    "palabra", "biblia", "cristo", "jesús", "padre", "espiritu", "espíritu",
    "consuelo", "fuerza", "vida", "descanso", "matrimonio", "sanidad", "sanacion", "sanación"
}

# Patrones de CTAs manipulativos, supersticiosos o que atribuyen citas falsas a Dios
MANIPULATIVE_PATTERNS = [
    r"\b(?:type|comment|write)\s+['\"]?amen['\"]?.{0,40}(?:claim|receive|bless|heal|miracle|money|god will)",
    r"\b(?:claim|receive)\s+(?:your\s+)?(?:miracle|financial blessing|debt cancellation|healing|check|blessing)",
    r"\b(?:if you\s+)?(?:scroll past|ignore this|skip this).{0,40}(?:bad luck|devil|shame)",
    r"\b(?:share|send)\s+(?:this\s+)?(?:with|to)\s+\d+\s+(?:people|friends)",
    r"\bgod\s+wants\s+you\s+to\s+(?:hear|know)\s+that\s+you\s+will\s+(?:receive\s+\$|be rich|never be sick)",
    r"\bgod\s+will\s+(?:heal you tomorrow|cancel your debt|give you \$|make you rich)",
    r"\bjesus\s+says\s*:\s*['\"]?(?:i will make you rich|type amen|send this)",
    r"\bleave\s+your\s+(?:first\s+)?name\s+to\s+(?:be saved|guarantee|claim)"
]


def check_accidental_spanish(text: str) -> Optional[str]:
    """Detecta caracteres con tilde, diéresis, ñ, o palabras en español dentro del texto público."""
    if not text:
        return None

    # 1. Caracteres ortográficos exclusivos del español
    if re.search(r"[áéíóúÁÉÍÓÚñÑ¿¡]", text):
        return "Se detectaron caracteres en español (tildes, ñ, signos ¿¡) en el texto público. Asegúrate de que el contenido esté en inglés estadounidense."

    # 2. Palabras completas en español
    words = re.findall(r"\b[a-zA-ZáéíóúÁÉÍÓÚñÑ]+\b", text.lower())
    found_spanish = [w for w in words if w in SPANISH_LEAK_WORDS]
    if found_spanish:
        unique_words = list(dict.fromkeys(found_spanish))[:3]
        return f"Posible vocabulario en español detectado: '{', '.join(unique_words)}'. El texto público debe ser inglés natural para la audiencia de EE. UU."

    return None


def check_manipulative_cta(text: str) -> Optional[str]:
    """Detecta llamadas a la acción manipulativas, condicionamientos de milagros o supersticiones."""
    if not text:
        return None

    text_lower = text.lower()
    for pattern in MANIPULATIVE_PATTERNS:
        if re.search(pattern, text_lower):
            return "Se detectó un CTA manipulativo o con promesa de beneficios espirituales/económicos a cambio de interacción. Usa una invitación natural y respetuosa."

    return None


def check_biblical_reference(scripture_text: str, theme_key: Optional[str] = None) -> Optional[str]:
    """Verifica si la cita bíblica coincide con un formato canónico o si está inventada."""
    if not scripture_text or not scripture_text.strip():
        return None  # El scripture es opcional según el formato

    # Comprobar formato de libro y capítulo:verso (e.g., "Luke 15:20", "Psalm 91:1-2")
    canonical_pattern = r"\b(?:Genesis|Exodus|Leviticus|Numbers|Deuteronomy|Joshua|Judges|Ruth|1\s+Samuel|2\s+Samuel|1\s+Kings|2\s+Kings|1\s+Chronicles|2\s+Chronicles|Ezra|Nehemiah|Esther|Job|Psalm|Psalms|Proverbs|Ecclesiastes|Song\s+of\s+Solomon|Isaiah|Jeremiah|Lamentations|Ezekiel|Daniel|Hosea|Joel|Amos|Obadiah|Jonah|Micah|Nahum|Habakkuk|Zephaniah|Haggai|Zechariah|Malachi|Matthew|Mark|Luke|John|Acts|Romans|1\s+Corinthians|2\s+Corinthians|Galatians|Ephesians|Philippians|Colossians|1\s+Thessalonians|2\s+Thessalonians|1\s+Timothy|2\s+Timothy|Titus|Philemon|Hebrews|James|1\s+Peter|2\s+Peter|1\s+John|2\s+John|3\s+John|Jude|Revelation)\s+\d+:\d+(?:-\d+)?\b"

    if not re.search(canonical_pattern, scripture_text, re.I):
        return f"La referencia '{scripture_text[:40]}...' no parece tener un formato canónico reconocido (ej. 'Luke 15:20 (NIV)'). Revisa la cita bíblica antes de publicar."

    # Si se proporcionó theme_key, verificar si coincide con el catálogo canónico del estudio
    if theme_key and theme_key in BIBLICAL_CATALOGUE:
        canonical_ref = BIBLICAL_CATALOGUE[theme_key].split("—")[0].strip()
        # Verificar que el libro y capítulo concuerden razonablemente
        book_chapter = canonical_ref.split(":")[0].strip().lower()
        if book_chapter not in scripture_text.lower():
            # Advertencia informativa no bloqueante
            return f"Nota editorial: El tema '{theme_key}' usualmente usa '{canonical_ref}', pero se detectó '{scripture_text[:30]}...'. Verifica que sea la cita deseada."

    return None


def check_caption_script_alignment(script_text: str, caption_text: str) -> Optional[str]:
    """Comprueba que la descripción comparta coherencia temática y vocabulario relevante con el guion aprobado."""
    if not script_text or not caption_text:
        return None

    # Extraer palabras clave de más de 4 letras ignorando stop words
    stop_words = {
        "about", "above", "after", "again", "against", "because", "before", "being",
        "below", "between", "both", "during", "further", "having", "myself", "other",
        "should", "their", "theirs", "themselves", "there", "these", "through", "under",
        "until", "where", "which", "while", "would", "yours", "tonight", "today", "peace",
        "heart", "faith", "prayer", "lord", "god", "every", "with"
    }

    script_words = set(w.lower() for w in re.findall(r"\b[a-zA-Z]{5,}\b", script_text) if w.lower() not in stop_words)
    caption_words = set(w.lower() for w in re.findall(r"\b[a-zA-Z]{5,}\b", caption_text) if w.lower() not in stop_words)

    overlap = script_words.intersection(caption_words)

    # Si no hay ninguna palabra temática compartida y ambos textos tienen longitud sustancial
    if len(script_words) >= 5 and len(caption_words) >= 5 and len(overlap) == 0:
        return "La descripción parece desconectada del guion narrado (no comparten palabras clave temáticas). Asegúrate de que la descripción corresponda a esta narración."

    return None


def check_duplicate_content(
    new_text: str,
    recent_texts: List[str],
    similarity_threshold: float = 0.85
) -> Optional[str]:
    """Comprueba si el texto es idéntico o muy similar a publicaciones recientes."""
    if not new_text or not recent_texts:
        return None

    norm_new = re.sub(r"\W+", " ", new_text.lower()).strip()
    words_new = set(norm_new.split())
    if not words_new:
        return None

    for idx, old in enumerate(recent_texts):
        if not old:
            continue
        norm_old = re.sub(r"\W+", " ", old.lower()).strip()
        if norm_new == norm_old:
            return f"Este texto es idéntico a una publicación reciente (Registro #{idx + 1}). Considera alternar la apertura o el enfoque para mantener frescura editorial."

        words_old = set(norm_old.split())
        if not words_old:
            continue
        intersection = words_new.intersection(words_old)
        union = words_new.union(words_old)
        jaccard = len(intersection) / len(union) if union else 0
        if jaccard >= similarity_threshold:
            return f"Este texto tiene un {round(jaccard * 100)}% de similitud con una publicación reciente. Considera redactar una variante para evitar repeticiones."

    return None


def check_stale_caption(
    script_hook: str,
    script_body: str,
    script_cta: str,
    caption_source_hook: Optional[str] = None,
    caption_source_body: Optional[str] = None
) -> Optional[str]:
    """Detecta si el guion fue editado después de que se generó la descripción."""
    if caption_source_hook is None and caption_source_body is None:
        return None  # No hay registro de origen, no advertir falsamente

    hook_changed = (script_hook.strip() != (caption_source_hook or "").strip())
    body_changed = (script_body.strip() != (caption_source_body or "").strip())

    if hook_changed or body_changed:
        return "El guion fue modificado después de generar la descripción. Haz clic en 'Regenerar Descripción' para actualizar el texto de publicación."

    return None


# ─── Validador General Pre-Publicación ─────────────────────────────────────────

def validate_post_readiness(
    theme_key: str,
    script_hook: str,
    script_body: str,
    script_cta: str,
    caption_text: str,
    scripture_text: str = "",
    recent_captions: Optional[List[str]] = None,
    caption_source_hook: Optional[str] = None,
    caption_source_body: Optional[str] = None
) -> Dict[str, Any]:
    """
    Ejecuta la suite completa de verificaciones editoriales.
    Retorna un diccionario con estado booleano 'ready', lista de 'warnings'
    y resultados de cada regla individual.
    """
    warnings: List[str] = []
    checks: Dict[str, bool] = {}

    full_narration = f"{script_hook} {script_body} {script_cta}".strip()

    # 1. Detección de español accidental
    spanish_warn = check_accidental_spanish(full_narration + " " + caption_text)
    checks["no_accidental_spanish"] = spanish_warn is None
    if spanish_warn:
        warnings.append(spanish_warn)

    # 2. CTA manipulativo
    manip_warn = check_manipulative_cta(full_narration + " " + caption_text)
    checks["no_manipulative_cta"] = manip_warn is None
    if manip_warn:
        warnings.append(manip_warn)

    # 3. Verificación bíblica
    if scripture_text:
        bible_warn = check_biblical_reference(scripture_text, theme_key)
        checks["biblical_reference_valid"] = bible_warn is None
        if bible_warn:
            warnings.append(bible_warn)
    else:
        checks["biblical_reference_valid"] = True

    # 4. Alineación guion - descripción
    align_warn = check_caption_script_alignment(full_narration, caption_text)
    checks["caption_script_aligned"] = align_warn is None
    if align_warn:
        warnings.append(align_warn)

    # 5. Detección de duplicados recientes
    if recent_captions:
        dup_warn = check_duplicate_content(caption_text, recent_captions)
        checks["no_recent_duplicate"] = dup_warn is None
        if dup_warn:
            warnings.append(dup_warn)
    else:
        checks["no_recent_duplicate"] = True

    # 6. Descripción desactualizada por edición de guion
    stale_warn = check_stale_caption(script_hook, script_body, script_cta, caption_source_hook, caption_source_body)
    checks["caption_up_to_date"] = stale_warn is None
    if stale_warn:
        warnings.append(stale_warn)

    # Estado listo: true si no hay advertencias críticas
    # Recuerda: es orientativo, no bloquea al usuario si desea proceder
    return {
        "ready": len(warnings) == 0,
        "warnings": warnings,
        "checks": checks,
        "warning_count": len(warnings)
    }
