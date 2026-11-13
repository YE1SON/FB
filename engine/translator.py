"""
JESUSREELS STUDIO - TRANSLATION MODULE
Servicio de traducción bidireccional de alto rendimiento sin costo para FaithSpark Daily.
Permite mostrar toda la interfaz y guiones en Español para el usuario,
mientras preserva la síntesis de audio y subtítulos en Inglés contemporáneo.
"""

import urllib.request
import urllib.parse
import json
import re
from typing import Optional, List, Dict

_TRANSLATION_CACHE: Dict[str, str] = {}

SPANISH_INDICATORS = set([
    "el", "la", "de", "que", "y", "en", "un", "ser", "se", "no", "haber", "por",
    "con", "su", "para", "como", "estar", "tener", "le", "lo", "lo", "todo",
    "pero", "más", "hacer", "o", "poder", "este", "ir", "otro", "ese", "la",
    "si", "me", "ya", "dios", "señor", "oración", "padre", "hijos", "hijo", "fe",
    "paz", "noche", "mañana", "familia", "gracia", "vida", "hoy", "amor", "corazón"
])

def is_spanish_text(text: Optional[str]) -> bool:
    """Detecta si un texto está predominantemente en español."""
    if not text or not text.strip():
        return False
    # Acentos y caracteres exclusivos del español
    if re.search(r"[áéíóúÁÉÍÓÚñÑ¿¡]", text):
        return True
    words = re.findall(r"\b[a-zA-ZáéíóúñÁÉÍÓÚÑ]+\b", text.lower())
    if not words:
        return False
    matches = sum(1 for w in words if w in SPANISH_INDICATORS)
    return (matches / len(words)) >= 0.20


def translate_text(text: str, source_lang: str = "auto", target_lang: str = "es") -> str:
    """
    Traduce texto utilizando el endpoint de traducción gratuito de Google con caché en memoria.
    source_lang: 'auto', 'en', 'es'
    target_lang: 'es' o 'en'
    """
    if not text or not text.strip():
        return ""
    
    clean_text = text.strip()
    cache_key = f"{source_lang}:{target_lang}:{clean_text}"
    if cache_key in _TRANSLATION_CACHE:
        return _TRANSLATION_CACHE[cache_key]

    try:
        url = f"https://translate.googleapis.com/translate_a/single?client=gtx&sl={source_lang}&tl={target_lang}&dt=t&q={urllib.parse.quote(clean_text)}"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            translated = "".join([segment[0] for segment in data[0] if segment and segment[0]])
            if translated:
                _TRANSLATION_CACHE[cache_key] = translated
                return translated
    except Exception as e:
        print(f"[Translator] Error traduciendo '{clean_text[:30]}...': {e}")

    return clean_text


def translate_en_to_es(text: str) -> str:
    """Traduce de Inglés a Español."""
    return translate_text(text, source_lang="en", target_lang="es")


def translate_es_to_en(text: str) -> str:
    """Traduce de Español a Inglés."""
    return translate_text(text, source_lang="es", target_lang="en")


def translate_list_en_to_es(texts: List[str]) -> List[str]:
    """Traduce una lista de textos de Inglés a Español."""
    return [translate_en_to_es(t) for t in texts]
