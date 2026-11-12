"""
JESUSREELS STUDIO / FAITHSPARK DAILY — AI NARRATIVE ENGINE
Generador de guiones mediante IA gratuita (Google Gemini API & GroqCloud) con
respaldo automático en el motor editorial local.
Diseñado para audiencia adulta estadounidense en inglés contemporáneo digno y reverente.
"""

import os
import json
import re
import random
from typing import Dict, List, Optional, Any, Tuple
import requests

from engine.history import get_history_manager, calculate_jaccard_similarity
from engine.scripts import BIBLICAL_CATALOGUE, THEMATIC_PILLARS, generate_script as generate_local_script

# ─── Modelos Gratuitos Disponibles ───────────────────────────────────────────
GEMINI_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite-preview",
    "gemini-3.6-flash",
    "gemini-3.5-flash",
    "gemini-3.8-flash"
]

GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant"
]

# ─── Duraciones Objetivo ─────────────────────────────────────────────────────
DURATION_TARGETS = {
    "micro": {"words_min": 28, "words_max": 42, "target_sec": 16.0},
    "deep": {"words_min": 45, "words_max": 65, "target_sec": 22.0},
    "story": {"words_min": 75, "words_max": 105, "target_sec": 36.0}
}

# ─── Instrucciones del Sistema para la IA ────────────────────────────────────
SYSTEM_NARRATIVE_PROMPT = """You are a senior Christian devotional writer and liturgical editor crafting vertical short-form video narrations (Reels) for "FaithSpark Daily", speaking to Christian adults in the United States (primarily ages 40-70).

CORE IDENTITY & SPIRITUAL TONE:
- Write in contemporary, natural, dignified American English.
- Sincere, warm, calm, reverent, and emotionally grounded.
- Speak directly to real human situations: late-night worries, praying for grown children, medical test waiting, financial bills, caregiving fatigue, quiet grief, family reconciliation.

STRICT EDITORIAL RULES (NEVER VIOLATE):
1. NO clickbait or superstition: NEVER write "Stop scrolling", "This video was meant to find you", "God told me to tell you", "If you scroll away you reject God", or "Comment AMEN to receive a miracle".
2. NO prosperity gospel or magical promises: Never promise sudden cash deposits, instantaneous physical cures, or that viewing this video triggers a miracle.
3. NO fake Bible verses: If quoting Scripture, use accurate NIV or ESV canonical texts. If no verse fits cleanly, state a spiritual paraphrase or leave the scripture field empty.
4. Provide exactly 3 DISTINCT opening hook options in the JSON response:
   - Option 1: Direct emotional resonance addressing the viewer's heart.
   - Option 2: Relational intercession (thinking of a family member/friend).
   - Option 3: Quiet biblical/theological reassurance.
5. The Call to Action (CTA) must be relational, encouraging, and natural:
   - Invite intercession ("Leave their first name below so we can pray together"),
   - Sharing with a loved one ("Share this prayer with someone who hasn't been sleeping well"), or
   - Honest reflection ("What burden are you placing into God's hands tonight?").
6. Output MUST be valid strict JSON only. No markdown fences, no conversational preamble.
"""

def _build_user_prompt(
    theme_title: str,
    human_situation: str,
    specific_focus: Optional[str],
    custom_topic: Optional[str],
    narration_type: str,
    mode: str,
    verse_candidate: str,
    recent_hooks: List[str]
) -> str:
    target = DURATION_TARGETS.get(mode, DURATION_TARGETS["deep"])
    
    avoid_block = ""
    if recent_hooks:
        cleaned_recent = [h.strip() for h in recent_hooks[-6:] if h and len(h.strip()) > 10]
        if cleaned_recent:
            avoid_block = (
                "\nAVOID REPEATING ANY OF THESE RECENT OPENING HOOKS (make your openings completely fresh):\n" +
                "\n".join(f"- {h}" for h in cleaned_recent)
            )

    style_guide = {
        "prayer": "First-person humble prayer directly addressing God/Jesus ('Father, ...', 'Lord, ...'). Warm, earnest communion.",
        "reflection": "Insightful biblical reflection connecting Scripture to daily modern life. Contemplative and wise.",
        "story": "A short relatable real-life human moment with an enduring spiritual lesson. Authentic and believable.",
        "comfort": "Tender, quiet consolation for someone carrying invisible weariness or heartache. Compassionate companionship."
    }.get(narration_type, "First-person humble prayer addressing God.")

    return f"""TASK: Generate a complete Christian devotional narration.

Theme: {theme_title}
Underlying Human Need: {human_situation}
Specific Focus/Angle: {specific_focus or 'General comforting reflection on this theme'} (NOTE: The angle or situation may be provided in Spanish, but you must write the entire devotional script strictly in natural, contemporary, dignified American English addressing this exact human reality with deep empathy)
Custom Situation from User: {custom_topic or 'None provided'}
Narration Style: {narration_type.upper()} ({style_guide})
Target Word Count for Body: {target['words_min']} to {target['words_max']} words.
Biblical Reference Base: {verse_candidate}
{avoid_block}

RESPOND WITH A SINGLE VALID JSON OBJECT MATCHING THIS EXACT SCHEMA:
{{
  "title": "Short title (3-5 words in English)",
  "hook": "Primary opening hook (1-2 sentences, ~8-16 words, spoken in first 3 seconds)",
  "hook_options": [
    "Hook Option 1: Direct emotional hook",
    "Hook Option 2: Relational hook (praying for family / friend)",
    "Hook Option 3: Quiet biblical reassurance hook"
  ],
  "body": "Devotional message ({target['words_min']}-{target['words_max']} words in natural US English)",
  "cta": "Contextual call to action (relational / prayer request / gentle sharing, ~12-22 words)",
  "scripture": "Canonical Bible verse with book, chapter, verse and translation, e.g. 'Philippians 4:6-7 (NIV) — ...'",
  "visual_prompt": "Cinematic vertical 9:16 photorealistic prompt for ONE single impactful visual (Jesus reverent, open Bible with warm candlelight, praying family, or majestic cross at sunrise). Strictly text-free."
}}"""


# ─── 1. Motor Google Gemini API (Nivel Gratuito) ──────────────────────────────

def call_gemini_api(
    api_key: str,
    user_prompt: str,
    system_prompt: str = SYSTEM_NARRATIVE_PROMPT,
    timeout: int = 25
) -> Dict[str, Any]:
    """Llama a Google Gemini API utilizando modelos del nivel gratuito."""
    if not api_key:
        raise ValueError("Google Gemini API Key no proporcionada.")

    headers = {"Content-Type": "application/json"}
    last_err = None

    for model in GEMINI_MODELS:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": f"{system_prompt}\n\n{user_prompt}"}
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json",
                "temperature": 0.7,
                "maxOutputTokens": 2500
            }
        }
        try:
            print(f"[Gemini API] Solicitando guion con modelo {model}...")
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates and "content" in candidates[0]:
                    parts = candidates[0]["content"].get("parts", [])
                    if parts and "text" in parts[0]:
                        raw_text = parts[0]["text"].strip()
                        json_str = _extract_json_string(raw_text)
                        try:
                            parsed = json.loads(json_str)
                        except Exception:
                            # Reintento con limpieza de caracteres de control
                            cleaned_json = re.sub(r"[\x00-\x1f]+", " ", json_str)
                            try:
                                parsed = json.loads(cleaned_json)
                            except Exception:
                                # Fallback básico con regex si el JSON vino cortado
                                parsed = _parse_loose_json(json_str)
                        parsed["provider_used"] = f"Google Gemini ({model})"
                        return parsed
            elif resp.status_code == 429:
                print(f"[Gemini API] Cuota excedida (429) en {model}. Intentando siguiente modelo...")
                last_err = f"Cuota gratuita excedida (HTTP 429) en {model}"
                continue
            elif resp.status_code == 503:
                print(f"[Gemini API] Alta demanda temporal (503) en {model}. Intentando siguiente modelo...")
                last_err = f"Alta demanda temporal (HTTP 503) en {model}"
                continue
            else:
                err_text = resp.text[:180]
                print(f"[Gemini API] Error {resp.status_code} en {model}: {err_text}")
                last_err = f"HTTP {resp.status_code}: {err_text}"
        except requests.exceptions.Timeout:
            print(f"[Gemini API] Tiempo de espera agotado ({timeout}s) en {model}. Intentando siguiente modelo...")
            last_err = f"Tiempo de espera agotado en {model}"
        except Exception as e:
            print(f"[Gemini API] Excepción al llamar a {model}: {e}")
            last_err = str(e)

    raise RuntimeError(f"Fallo en Google Gemini API: {last_err}")


# ─── 2. Motor GroqCloud API (Nivel Gratuito) ──────────────────────────────────

def call_groq_api(
    api_key: str,
    user_prompt: str,
    system_prompt: str = SYSTEM_NARRATIVE_PROMPT,
    timeout: int = 25
) -> Dict[str, Any]:
    """Llama a GroqCloud API con modelos ultrarrápidos de nivel gratuito."""
    if not api_key:
        raise ValueError("GroqCloud API Key no proporcionada.")

    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    last_err = None

    for model in GROQ_MODELS:
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.7,
            "max_tokens": 1200
        }
        try:
            print(f"[GroqCloud API] Solicitando guion con modelo {model}...")
            resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
            if resp.status_code == 200:
                data = resp.json()
                choices = data.get("choices", [])
                if choices and "message" in choices[0]:
                    raw_text = choices[0]["message"].get("content", "").strip()
                    json_str = _extract_json_string(raw_text)
                    parsed = json.loads(json_str)
                    parsed["provider_used"] = f"GroqCloud ({model})"
                    return parsed
            elif resp.status_code == 429:
                print(f"[GroqCloud API] Cuota temporal excedida (429) en {model}...")
                last_err = f"Cuota gratuita excedida (HTTP 429) en {model}"
                continue
            else:
                err_text = resp.text[:180]
                print(f"[GroqCloud API] Error {resp.status_code} en {model}: {err_text}")
                last_err = f"HTTP {resp.status_code}: {err_text}"
        except Exception as e:
            print(f"[GroqCloud API] Excepción al llamar a {model}: {e}")
            last_err = str(e)

    raise RuntimeError(f"Fallo en GroqCloud API: {last_err}")


# ─── 3. Extractor Auxiliar de JSON ───────────────────────────────────────────

def _parse_loose_json(text: str) -> Dict[str, Any]:
    """Extrae campos del JSON con expresiones regulares si el JSON está truncado o malformado."""
    result: Dict[str, Any] = {}
    for field in ["title", "hook", "body", "devotional_body", "cta", "call_to_action", "scripture", "visual_prompt"]:
        m = re.search(rf'"{field}"\s*:\s*"([^"\\]*(?:\\.[^"\\]*)*)"', text, re.IGNORECASE)
        if m:
            val = m.group(1).encode('utf-8').decode('unicode_escape', errors='ignore')
            result[field] = val
    # Extraer hook_options si existen
    options_m = re.search(r'"hook_options"\s*:\s*\[(.*?)\]', text, re.DOTALL | re.IGNORECASE)
    if options_m:
        raw_opts = options_m.group(1)
        opts = [o.strip(' "\'\r\n') for o in re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"', raw_opts) if o.strip()]
        if opts:
            result["hook_options"] = opts
    return result


def _extract_json_string(text: str) -> str:
    """Limpia bloques de código markdown y extrae el JSON válido."""
    clean = text.strip()
    if clean.startswith("```"):
        clean = re.sub(r"^```(?:json)?\s*", "", clean)
        clean = re.sub(r"\s*```$", "", clean)
    # Buscar el primer '{' y el último '}'
    start = clean.find("{")
    end = clean.rfind("}")
    if start != -1 and end != -1:
        return clean[start:end+1]
    return clean


# ─── 4. Orquestador Principal de Guiones ──────────────────────────────────────

def generate_ai_narrative_script(
    theme_key: str,
    specific_focus: Optional[str] = None,
    custom_topic: Optional[str] = None,
    narration_type: str = "prayer",
    mode: str = "deep",
    include_cta: bool = True,
    engine_provider: str = "gemini",
    gemini_api_key: Optional[str] = None,
    groq_api_key: Optional[str] = None
) -> Dict[str, Any]:
    """
    Genera un guion completo con IA gratuita (Gemini o Groq) y 3 alternativas de apertura.
    Si el proveedor seleccionado no tiene clave o falla, activa el respaldo en el motor local.
    """
    from engine.scripts import VIRAL_THEMES, BIBLICAL_CATALOGUE
    from engine.narrative_prompts import generate_single_image_prompt

    # Resolver datos del tema
    theme_info = VIRAL_THEMES.get(theme_key, VIRAL_THEMES.get("morning_favor"))
    theme_title = theme_info["title"]
    human_situation = theme_info.get("human_situation", "An honest human daily challenge")
    verse_candidate = BIBLICAL_CATALOGUE.get(theme_key, theme_info.get("scripture", ""))

    history = get_history_manager()
    if hasattr(history, "get_recent_scripts"):
        recent_records = history.get_recent_scripts(limit=25)
    elif hasattr(history, "load_history"):
        recent_records = history.load_history()[-25:]
    else:
        recent_records = []
    recent_hooks = [s.get("hook", "") for s in recent_records if isinstance(s, dict)]

    user_prompt = _build_user_prompt(
        theme_title=theme_title,
        human_situation=human_situation,
        specific_focus=specific_focus,
        custom_topic=custom_topic,
        narration_type=narration_type,
        mode=mode,
        verse_candidate=verse_candidate,
        recent_hooks=recent_hooks
    )

    parsed_result = None
    provider_used = "Motor Local Editorial"
    error_note = None

    norm_provider = (engine_provider or "gemini").lower().strip()

    # Intento 1: Google Gemini API
    if norm_provider in ("gemini", "google", "gemini_free"):
        if gemini_api_key:
            try:
                parsed_result = call_gemini_api(api_key=gemini_api_key, user_prompt=user_prompt)
                provider_used = parsed_result.get("provider_used", "Google Gemini")
            except Exception as e:
                error_note = f"Gemini falló: {e}. Activando motor local de respaldo."
                print(f"[AI Narrative] {error_note}")
        else:
            error_note = "Clave de Google Gemini no configurada. Usando motor local de respaldo."
            print(f"[AI Narrative] {error_note}")

    # Intento 2: GroqCloud API
    elif norm_provider in ("groq", "groqcloud", "groq_free"):
        if groq_api_key:
            try:
                parsed_result = call_groq_api(api_key=groq_api_key, user_prompt=user_prompt)
                provider_used = parsed_result.get("provider_used", "GroqCloud")
            except Exception as e:
                error_note = f"Groq falló: {e}. Activando motor local de respaldo."
                print(f"[AI Narrative] {error_note}")
        else:
            error_note = "Clave de GroqCloud no configurada. Usando motor local de respaldo."
            print(f"[AI Narrative] {error_note}")

    # Si se solicitó motor local explícitamente o si la IA falló:
    if not parsed_result:
        local_res = generate_local_script(
            theme_key=theme_key,
            custom_topic=custom_topic or specific_focus,
            mode=mode,
            narration_type=narration_type,
            include_cta=include_cta
        )
        # Construir 3 alternativas de apertura para el motor local
        theme_openings = theme_info.get("hooks", [local_res.get("hook", "")])
        hook_options = list(dict.fromkeys([
            local_res.get("hook", ""),
            theme_openings[0] if len(theme_openings) > 0 else "Before you close your eyes in sleep tonight...",
            theme_openings[1] if len(theme_openings) > 1 else "When the quiet hours of the night arrive...",
            theme_openings[2] if len(theme_openings) > 2 else "Take one deep breath and rest in God's peace..."
        ]))[:3]

        parsed_result = {
            "title": local_res.get("english_title", theme_title),
            "hook": local_res.get("hook", ""),
            "hook_options": hook_options,
            "body": local_res.get("body", ""),
            "cta": local_res.get("cta", ""),
            "scripture": local_res.get("scripture", verse_candidate),
            "visual_prompt": local_res.get("scene_1_prompt", "")
        }
        if error_note:
            provider_used = f"Motor Local (Respaldo: {error_note})"
        else:
            provider_used = "Motor Local Editorial (Catálogo canónico)"

    # Normalizar campos obtenidos con soporte para sinónimos del modelo
    hook = str(
        parsed_result.get("hook") or
        parsed_result.get("opening_hook") or
        parsed_result.get("opening") or
        (parsed_result.get("hook_options") and parsed_result["hook_options"][0]) or
        ""
    ).strip()

    hook_options = parsed_result.get("hook_options", [])
    if not isinstance(hook_options, list) or len(hook_options) < 3:
        hook_options = [hook, f"If your heart needed a quiet reminder today: {hook}", f"A gentle prayer for tonight: {hook}"][:3]
    else:
        hook_options = [str(h).strip() for h in hook_options[:3]]

    body = str(
        parsed_result.get("body") or
        parsed_result.get("devotional_body") or
        parsed_result.get("prayer") or
        parsed_result.get("prayer_text") or
        parsed_result.get("message") or
        parsed_result.get("content") or
        ""
    ).strip()

    cta = ""
    if include_cta:
        cta = str(
            parsed_result.get("cta") or
            parsed_result.get("call_to_action") or
            parsed_result.get("cta_text") or
            ""
        ).strip()

    scripture = str(
        parsed_result.get("scripture") or
        parsed_result.get("scripture_reference") or
        parsed_result.get("bible_verse") or
        verse_candidate
    ).strip()

    title = str(
        parsed_result.get("title") or
        parsed_result.get("topic") or
        theme_title
    ).strip()

    # Construir texto completo para locución
    full_text_parts = [hook, body]
    if include_cta and cta:
        full_text_parts.append(cta)
    full_text = " ".join(filter(None, full_text_parts))

    word_count = len(full_text.split())
    # Estimación de locución TTS (~125 palabras por minuto a velocidad -6%)
    estimated_duration_sec = min(36.0, max(14.0, round(word_count * 60 / 125, 1)))

    # Generar prompt visual único para 1 sola imagen
    single_image_prompt = generate_single_image_prompt(
        theme_key=theme_key,
        script_text=full_text,
        specific_focus=specific_focus or custom_topic,
        narration_type=narration_type,
        hook=hook,
        body=body,
        cta=cta
    )

    # Registrar en historial para evitar repeticiones futuras
    history.record_script(
        theme_key=theme_key,
        hook=hook,
        body=body,
        cta=cta,
        closing="",
        narration_type=narration_type,
        narrative_angle=specific_focus or "ai_generated",
        scene_prompts=[single_image_prompt]
    )

    return {
        "theme_key": theme_key,
        "theme_title": theme_title,
        "english_title": title,
        "specific_focus": specific_focus or "",
        "custom_topic": custom_topic or "",
        "narration_type": narration_type,
        "mode": mode,
        "hook": hook,
        "hook_options": hook_options,
        "body": body,
        "cta": cta,
        "include_cta": include_cta,
        "full_text": full_text,
        "scripture": scripture,
        "word_count": word_count,
        "estimated_duration_sec": estimated_duration_sec,
        "image_prompt": single_image_prompt,
        "scene_1_prompt": single_image_prompt,
        "provider_used": provider_used,
        "error_note": error_note
    }
