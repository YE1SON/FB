"""
Arquitectura Modular de Proveedores de Guiones para JesusReels Studio.
Soporta generación estructurada mediante:
- TemplateScriptProvider: Generador interno de alta coherencia teológica y narrativa.
- OllamaScriptProvider: Generador con modelo local (referencia qwen3.5:4b / qwen3:8b) vía API JSON estructurada.
- AutoScriptProvider: Detección inteligente con fallback seguro y sin fricciones.
"""

import os
import re
import json
import time
import urllib.request
import urllib.error
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any
from pydantic import BaseModel, Field, ValidationError

# ─── Modelo Pydantic Estructurado para Salida de Guion ───────────────────────

class ScriptResult(BaseModel):
    theme_key: str
    theme_title_es: str
    human_situation: str = Field(default="", description="Situación o dolor humano concreto al que se dirige")
    central_idea: str = Field(default="", description="Idea teológica o reflexiva central")
    thematic_pillar: str = Field(default="spiritual_growth", description="Pilar temático teológico")
    hook: str = Field(description="Gancho inicial de 0-3s, situacional y honesto")
    body: str = Field(description="Desarrollo del mensaje y oración")
    closing: str = Field(default="", description="Cierre reconfortante de fe")
    cta: str = Field(default="", description="Llamado a la acción opcional y respetuoso")
    full_text: str = Field(description="Texto completo que será narrado")
    word_count: int
    target_duration_sec: float = Field(default=22.0, description="Duración objetivo deseada (18-25s)")
    estimated_duration_sec: float = Field(description="Duración calculada del habla")
    mode: str = Field(default="deep")
    seamless_loop: bool = Field(default=False)
    tone: str = Field(default="hopeful")
    perspective: str = Field(default="prayer", description="Perspectiva narrativa")
    hook_badge_text: str = Field(default="PRAYER OF FAITH")
    micro_cta_text: str = Field(default="")
    scripture: str = Field(description="Referencia bíblica verificada")
    pinned_comment: str = Field(default="")
    seo_caption: str = Field(description="Descripción y copy para redes sociales")
    hashtags: List[str] = Field(default_factory=list)
    scene_1_prompt: str = Field(description="Prompt visual escena 1: Apertura y contexto")
    scene_2_prompt: str = Field(description="Prompt visual escena 2: Mensaje y reflexión")
    scene_3_prompt: str = Field(description="Prompt visual escena 3: Cierre y resolución")
    image_prompt: str = Field(default="")
    provider_used: str = Field(default="template", description="Motor que generó el guion: 'template' o 'ollama'")


# ─── Clase Base Abstracta ───────────────────────────────────────────────────

class BaseScriptProvider(ABC):
    @abstractmethod
    def generate(
        self,
        theme_key: Optional[str] = None,
        custom_topic: Optional[str] = None,
        mode: str = "deep",
        tone: Optional[str] = None,
        seamless_loop: bool = False
    ) -> ScriptResult:
        pass

    @abstractmethod
    def is_available(self) -> bool:
        pass


# ─── Proveedor Interno por Plantillas Narrativas Estructuradas ─────────────

class TemplateScriptProvider(BaseScriptProvider):
    """Generador interno de guiones con pilares temáticos y variedad narrativa real."""

    def is_available(self) -> bool:
        return True

    def generate(
        self,
        theme_key: Optional[str] = None,
        custom_topic: Optional[str] = None,
        mode: str = "deep",
        tone: Optional[str] = None,
        seamless_loop: bool = False
    ) -> ScriptResult:
        # Importación tardía para evitar ciclos con engine.scripts
        from engine.scripts import generate_internal_template_script
        raw_dict = generate_internal_template_script(
            theme_key=theme_key,
            custom_topic=custom_topic,
            mode=mode,
            tone=tone,
            seamless_loop=seamless_loop
        )
        raw_dict["provider_used"] = "template"
        return ScriptResult(**raw_dict)


# ─── Proveedor Local Opcional con Ollama ─────────────────────────────────────

class OllamaScriptProvider(BaseScriptProvider):
    """
    Proveedor opcional que consulta una instancia local de Ollama.
    Requiere que Ollama esté ejecutándose (por defecto http://127.0.0.1:11434).
    Valida la salida contra el esquema Pydantic ScriptResult con timeout estricto.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None
    ):
        self.base_url = (base_url or os.environ.get("OLLAMA_BASE_URL", "http://127.0.0.1:11434")).rstrip("/")
        self.model = model or os.environ.get("OLLAMA_MODEL", "qwen3.5:4b")
        try:
            self.timeout = float(timeout or os.environ.get("OLLAMA_TIMEOUT", "15.0"))
        except ValueError:
            self.timeout = 15.0
        self._fallback = TemplateScriptProvider()
        self._circuit_open_until = 0.0

    def is_available(self) -> bool:
        """Comprueba conectividad rápida con el endpoint /api/tags de Ollama con circuit breaker."""
        if time.time() < self._circuit_open_until:
            return False
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", headers={"User-Agent": "JesusReelsStudio/4.0"})
            with urllib.request.urlopen(req, timeout=1.5) as r:
                return r.status == 200
        except Exception:
            return False

    def get_installed_models(self) -> List[str]:
        try:
            req = urllib.request.Request(f"{self.base_url}/api/tags", headers={"User-Agent": "JesusReelsStudio/4.0"})
            with urllib.request.urlopen(req, timeout=2.5) as r:
                data = json.loads(r.read().decode("utf-8"))
                return [m.get("name") for m in data.get("models", []) if "name" in m]
        except Exception:
            return []

    def generate(
        self,
        theme_key: Optional[str] = None,
        custom_topic: Optional[str] = None,
        mode: str = "deep",
        tone: Optional[str] = None,
        seamless_loop: bool = False
    ) -> ScriptResult:
        from engine.scripts import VIRAL_THEMES, BIBLICAL_CATALOGUE

        # Resolver modelo real: si el configurado no existe pero hay otro disponible, usarlo
        installed = self.get_installed_models()
        active_model = self.model
        if installed:
            matching = [m for m in installed if self.model in m]
            if matching:
                active_model = matching[0]
            else:
                active_model = installed[0]

        chosen_key = theme_key if (theme_key and theme_key in VIRAL_THEMES) else "morning_favor"
        theme_info = VIRAL_THEMES.get(chosen_key, VIRAL_THEMES["morning_favor"])
        verified_verse = BIBLICAL_CATALOGUE.get(chosen_key, theme_info.get("scripture", "Psalm 23:1 — The Lord is my shepherd; I shall not want."))

        system_prompt = (
            "You are a compassionate, thoughtful Christian writer crafting video devotions in contemporary US English. "
            "Write for an adult American audience seeking quiet reassurance and biblical encouragement.\n\n"
            "CRITICAL RULES:\n"
            "1. Focus on ONE concrete human situation (e.g. exhaustion after work, concern for a child, silent grief, waiting on God).\n"
            "2. Never use manipulative clickbait (No 'Stop scrolling', No 'God has an urgent message', No 'Type AMEN for a miracle').\n"
            "3. Never promise financial wealth, immediate cures, or guaranteed earthly results.\n"
            "4. Tone must be serene, heartfelt, and reverent, not overly dramatic.\n"
            "5. The output must be pure JSON conforming strictly to the requested schema.\n"
            f"6. You MUST use this exact verified biblical scripture: \"{verified_verse}\". Do not invent or alter verses."
        )

        user_prompt = f"""Generate a Christian video devotion for Facebook Reels (18-25 seconds length, ~45-60 words).
Theme: {theme_info['title']} ({theme_info.get('description', '')})
Custom Topic: {custom_topic or 'None'}
Duration Mode: {mode} (target 20-25 seconds)

Return ONLY a JSON object with these exact keys:
{{
  "human_situation": "One clear sentence describing the specific human need or moment",
  "central_idea": "The core theological or pastoral comfort being offered",
  "hook": "Opening hook (4-8 words), natural and situational, without sensationalism",
  "body": "Gentle prayer or reflection (25-40 words) connecting with the heart",
  "closing": "Peaceful conclusion of faith (8-15 words)",
  "cta": "Optional polite reflection or invitation to rest/pray (8-12 words)",
  "hook_badge_text": "Short 3-5 word uppercase header for the video",
  "hashtags": ["#Tag1", "#Tag2", "#Tag3", "#Tag4"],
  "scene_1_prompt": "Image prompt for opening scene: clear subject, context, and lighting (No '8k/masterpiece')",
  "scene_2_prompt": "Image prompt for middle scene: reflective action or biblical symbol in context",
  "scene_3_prompt": "Image prompt for final scene: peaceful resolution and serene composition"
}}"""

        payload = {
            "model": active_model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            "stream": False,
            "format": "json",
            "options": {
                "temperature": 0.65,
                "top_p": 0.90,
                "num_predict": 450
            }
        }

        try:
            req_data = json.dumps(payload).encode("utf-8")
            http_req = urllib.request.Request(
                f"{self.base_url}/api/chat",
                data=req_data,
                headers={"Content-Type": "application/json", "User-Agent": "JesusReelsStudio/4.0"}
            )
            t0 = time.time()
            with urllib.request.urlopen(http_req, timeout=self.timeout) as resp:
                raw_resp = json.loads(resp.read().decode("utf-8"))
                elapsed = time.time() - t0
                content_str = raw_resp.get("message", {}).get("content", "").strip()

            # Parsear JSON devuelto por Ollama
            parsed = json.loads(content_str)

            # Validar y ensamblar texto completo
            hook = parsed.get("hook", "").strip()
            body = parsed.get("body", "").strip()
            closing = parsed.get("closing", "").strip()
            cta = parsed.get("cta", "").strip()

            if seamless_loop and cta:
                loop_bridge = "Before you close your eyes in sleep tonight, remember that..."
                cta = f"{cta.rstrip('.! ')} — {loop_bridge}"

            full_text = f"{hook} {body} {closing} {cta}".strip()
            word_count = len(full_text.split())
            est_dur = round(max(15.0, (word_count / 2.15) + 1.2), 1)

            # Prompts
            p1 = parsed.get("scene_1_prompt", "")
            p2 = parsed.get("scene_2_prompt", "")
            p3 = parsed.get("scene_3_prompt", "")

            # Limpiar adjetivos de relleno si el modelo los añadió
            clean_cleaner = lambda s: re.sub(r'(?i)\b(photorealistic|8k|masterpiece|award winning|unreal engine)\b', '', s).strip()
            p1 = f"{clean_cleaner(p1)}, warm natural morning light, authentic biblical atmosphere --ar 9:16"
            p2 = f"{clean_cleaner(p2)}, peaceful reverent composition, volumetric soft lighting --ar 9:16"
            p3 = f"{clean_cleaner(p3)}, serene golden dawn sky, compassionate atmosphere --ar 9:16"

            hashtags = parsed.get("hashtags", theme_info.get("hashtags", ["#DailyPrayer", "#FaithInGod", "#ChristianFamily"]))
            if len(hashtags) > 5:
                hashtags = hashtags[:5]

            from engine.scripts import generate_seo_caption
            seo_caption = generate_seo_caption(theme_info["title"], full_text, verified_verse, cta, hashtags)

            result = ScriptResult(
                theme_key=chosen_key,
                theme_title_es=theme_info["title"],
                human_situation=parsed.get("human_situation", ""),
                central_idea=parsed.get("central_idea", ""),
                hook=hook,
                body=f"{body} {closing}".strip(),
                closing=closing,
                cta=cta,
                full_text=full_text,
                word_count=word_count,
                target_duration_sec=22.0,
                estimated_duration_sec=est_dur,
                mode=mode,
                seamless_loop=seamless_loop,
                tone=tone or "hopeful",
                hook_badge_text=parsed.get("hook_badge_text", theme_info.get("hook_badge_text", "PRAYER OF FAITH")),
                micro_cta_text=cta,
                scripture=verified_verse,
                pinned_comment=parsed.get("human_situation", "May God's peace rest upon you tonight."),
                seo_caption=seo_caption,
                hashtags=hashtags,
                scene_1_prompt=p1,
                scene_2_prompt=p2,
                scene_3_prompt=p3,
                image_prompt=p1,
                provider_used=f"ollama ({active_model}, {elapsed:.1f}s)"
            )
            print(f"[Ollama Provider] Guion generado con éxito en {elapsed:.2f}s ({active_model}).")
            return result

        except Exception as e:
            self._circuit_open_until = time.time() + 120.0
            print(f"[Ollama Fallback Warning]: Falló generación con Ollama ({e}). Activando generador interno...")
            fallback_res = self._fallback.generate(
                theme_key=theme_key,
                custom_topic=custom_topic,
                mode=mode,
                tone=tone,
                seamless_loop=seamless_loop
            )
            fallback_res.provider_used = "template (fallback from ollama)"
            return fallback_res


# ─── Proveedor Automático Inteligente ───────────────────────────────────────

class AutoScriptProvider(BaseScriptProvider):
    """
    Selecciona automáticamente el mejor proveedor según configuración y disponibilidad:
    - SCRIPT_PROVIDER='ollama' -> Ollama si está disponible.
    - SCRIPT_PROVIDER='template' -> Plantilla interna.
    - SCRIPT_PROVIDER='auto' (por defecto) -> Ollama si está disponible y rápido; si no, plantilla.
    """

    def __init__(self):
        self.template_provider = TemplateScriptProvider()
        self.ollama_provider = OllamaScriptProvider()

    def is_available(self) -> bool:
        return True

    def generate(
        self,
        theme_key: Optional[str] = None,
        custom_topic: Optional[str] = None,
        mode: str = "deep",
        tone: Optional[str] = None,
        seamless_loop: bool = False
    ) -> ScriptResult:
        provider_mode = os.environ.get("SCRIPT_PROVIDER", "auto").lower().strip()

        if provider_mode == "template":
            return self.template_provider.generate(theme_key, custom_topic, mode, tone, seamless_loop)

        if provider_mode == "ollama":
            if self.ollama_provider.is_available():
                return self.ollama_provider.generate(theme_key, custom_topic, mode, tone, seamless_loop)
            print("[Script Provider] Ollama no está accesible en la URL configurada. Usando fallback de plantilla.")
            return self.template_provider.generate(theme_key, custom_topic, mode, tone, seamless_loop)

        # Modo auto: intentar Ollama si está listo, sino usar plantilla interna de alta calidad
        if self.ollama_provider.is_available():
            try:
                return self.ollama_provider.generate(theme_key, custom_topic, mode, tone, seamless_loop)
            except Exception as e:
                print(f"[Script Provider Auto]: {e}. Usando plantilla interna.")
                return self.template_provider.generate(theme_key, custom_topic, mode, tone, seamless_loop)

        return self.template_provider.generate(theme_key, custom_topic, mode, tone, seamless_loop)


# ─── Fábrica Global ─────────────────────────────────────────────────────────

_auto_provider_instance = AutoScriptProvider()

def get_script_provider(provider_type: Optional[str] = None) -> BaseScriptProvider:
    if provider_type == "template":
        return TemplateScriptProvider()
    elif provider_type == "ollama":
        return OllamaScriptProvider()
    return _auto_provider_instance
