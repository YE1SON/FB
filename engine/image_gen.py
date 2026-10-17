import os
import re
import json
import base64
import random
import shutil
import uuid
import time
import requests
from io import BytesIO
from typing import Dict, Optional, Tuple
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
KEYS_FILE = os.path.join(BASE_DIR, "ai_keys.json")

os.makedirs(ASSETS_DIR, exist_ok=True)

# Modelos recomendados de Cloudflare Workers AI
CLOUDFLARE_MODELS = {
    "@cf/leonardo/phoenix-1.0": {
        "name": "🌟 Leonardo Phoenix 1.0 (Flagship: Fotorrealismo y Rostros)",
        "type": "leonardo"
    },
    "@cf/leonardo/lucid-origin": {
        "name": "🎨 Leonardo Lucid Origin (Ultra Definición y Texturas)",
        "type": "leonardo"
    },
    "@cf/black-forest-labs/flux-1-schnell": {
        "name": "⚡ FLUX.1 Schnell (Borrador Rápido 4 Pasos)",
        "type": "flux"
    },
    "@cf/bytedance/stable-diffusion-xl-lightning": {
        "name": "⚡ SDXL Lightning (Rápido)",
        "type": "sdxl"
    }
}

# ─── Gestión de Claves y Configuración ────────────────────────────────────────

def load_keys() -> Dict[str, str]:
    """Carga claves desde ai_keys.json y variables de entorno."""
    keys = {
        "cf_account_id": os.environ.get("CF_ACCOUNT_ID", os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")),
        "cf_api_token": os.environ.get("CF_API_TOKEN", os.environ.get("CLOUDFLARE_API_TOKEN", "")),
        "cf_model": os.environ.get("CF_MODEL", "@cf/leonardo/phoenix-1.0"),
        "aihorde_api_key": os.environ.get("AIHORDE_API_KEY", "0000000000"),
        "hf_token": os.environ.get("HF_TOKEN", os.environ.get("HUGGINGFACE_TOKEN", ""))
    }
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                for k, v in saved.items():
                    if v and not keys.get(k):
                        keys[k] = v
        except Exception as e:
            print(f"[ImageGen] Error al leer ai_keys.json: {e}")
    return keys

def save_keys(
    cf_account_id: Optional[str] = None,
    cf_api_token: Optional[str] = None,
    cf_model: Optional[str] = None,
    aihorde_api_key: Optional[str] = None,
    hf_token: Optional[str] = None
) -> Dict[str, str]:
    """Guarda claves en ai_keys.json para que persistan entre reinicios."""
    current = load_keys()
    if cf_account_id is not None:
        current["cf_account_id"] = cf_account_id.strip()
    if cf_api_token is not None:
        current["cf_api_token"] = cf_api_token.strip()
    if cf_model is not None and cf_model.strip():
        current["cf_model"] = cf_model.strip()
    if aihorde_api_key is not None:
        current["aihorde_api_key"] = aihorde_api_key.strip() or "0000000000"
    if hf_token is not None:
        current["hf_token"] = hf_token.strip()

    try:
        with open(KEYS_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2)
    except Exception as e:
        print(f"[ImageGen] Error al guardar ai_keys.json: {e}")
    return current

def get_providers_status() -> Dict:
    """Retorna el estado de configuración de los motores de IA."""
    keys = load_keys()
    cf_model = keys.get("cf_model") or "@cf/leonardo/phoenix-1.0"
    model_info = CLOUDFLARE_MODELS.get(cf_model, {"name": cf_model})
    return {
        "cloudflare": {
            "configured": bool(keys.get("cf_account_id") and keys.get("cf_api_token")),
            "account_id_masked": (keys.get("cf_account_id")[:6] + "...") if keys.get("cf_account_id") else "",
            "model": cf_model,
            "model_name": model_info.get("name", cf_model),
            "name": f"Cloudflare Workers AI ({model_info.get('name', 'Leonardo Phoenix')} — 10k Neuronas/día gratis)"
        },
        "aihorde": {
            "configured": True,
            "is_anonymous": keys.get("aihorde_api_key", "0000000000") in ("", "0000000000"),
            "name": "AI Horde (Comunidad Gratuita — GPUs Distribuidas sin límite de créditos)"
        },
        "huggingface": {
            "configured": bool(keys.get("hf_token")),
            "token_masked": (keys.get("hf_token")[:7] + "...") if keys.get("hf_token") else "",
            "model": "black-forest-labs/FLUX.1-schnell",
            "name": "Hugging Face Inference API (Status: 410 Deprecated)"
        }
    }

# ─── Optimizadores de Prompts ────────────────────────────────────────────────

def enhance_leonardo_prompt(prompt: str) -> str:
    """
    Optimiza el prompt para Leonardo Phoenix 1.0 y Lucid Origin.
    Acentúa fotorrealismo humano, iluminación dorada sagrada y calidad de retrato bíblico.
    """
    clean = prompt.strip()
    clean = re.sub(r'(?i)\b(octane render|unreal engine|8k|4k|hyperrealistic|masterpiece)\b', '', clean).strip()
    clean = re.sub(r'\s+', ' ', clean)

    cues = (
        "cinematic photograph, warm sacred golden hour lighting, authentic historical biblical atmosphere, "
        "dramatic depth of field, natural skin texture, 35mm portrait lens, photorealistic"
    )
    if "photograph" not in clean.lower() and "cinematic" not in clean.lower():
        return f"{clean}, {cues}"
    return f"{clean}, warm sacred golden hour lighting, photorealistic, 35mm lens"

def enhance_flux_prompt(prompt: str) -> str:
    """Optimiza el texto para FLUX.1 rápido."""
    clean = prompt.strip()
    clean = re.sub(r'(?i)\b(octane render|masterpiece|award winning|trending on artstation|hyperrealistic|8k|4k|unreal engine)\b', '', clean).strip()
    clean = re.sub(r'\s+', ' ', clean)
    return f"{clean}, cinematic photograph, warm sacred golden hour lighting, natural skin texture, 35mm lens portrait, photorealistic"

# ─── Motor 1: Cloudflare Workers AI (Leonardo Phoenix / Lucid / FLUX) ────────

def generate_cloudflare_image(
    prompt: str,
    account_id: str,
    api_token: str,
    model: str = "@cf/leonardo/phoenix-1.0"
) -> bytes:
    """
    Genera imagen usando modelos de Cloudflare Workers AI:
    - @cf/leonardo/phoenix-1.0 (Flagship: Fotográfico, rostros, iluminación dorada)
    - @cf/leonardo/lucid-origin (Ultra alta definición de texturas)
    - @cf/black-forest-labs/flux-1-schnell (Borrador veloz)
    """
    if not account_id or not api_token:
        raise ValueError("Cloudflare Account ID y API Token son obligatorios.")

    model = model.strip() if model else "@cf/leonardo/phoenix-1.0"
    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/{model}"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }

    if "leonardo" in model:
        payload = {
            "prompt": enhance_leonardo_prompt(prompt),
            "negative_prompt": "ugly, deformed, bad eyes, disfigured, extra limbs, low quality, blurry, modern clothes, text, watermark",
            "num_steps": 20,
            "guidance": 4.0
        }
    elif "flux" in model:
        payload = {
            "prompt": enhance_flux_prompt(prompt),
            "steps": 4
        }
    else:
        payload = {
            "prompt": enhance_leonardo_prompt(prompt),
            "num_steps": 20
        }

    print(f"[Cloudflare AI] Enviando petición a {model}...")
    resp = requests.post(endpoint, headers=headers, json=payload, timeout=45)

    if resp.status_code != 200:
        err_msg = resp.text
        try:
            err_json = resp.json()
            errors = err_json.get("errors", [])
            if errors:
                err_msg = errors[0].get("message", resp.text)
        except Exception:
            pass
        raise RuntimeError(f"Error de Cloudflare ({resp.status_code}): {err_msg}")

    c_type = resp.headers.get("Content-Type", "")
    if "application/json" in c_type:
        data = resp.json()
        img_b64 = None
        if isinstance(data, dict):
            if "result" in data and isinstance(data["result"], dict) and "image" in data["result"]:
                img_b64 = data["result"]["image"]
            elif "image" in data:
                img_b64 = data["image"]
        if img_b64:
            return base64.b64decode(img_b64)
        raise RuntimeError(f"Cloudflare no devolvió datos de imagen válidos: {str(data)[:200]}")
    else:
        # Retorno binario directo (image/jpeg o image/png)
        return resp.content

# ─── Motor 2: AI Horde (Comunidad Gratuita Descentralizada) ───────────────────

def generate_ai_horde(
    prompt: str,
    api_key: str = "0000000000",
    aspect_ratio: str = "9:16",
    timeout_sec: int = 55
) -> bytes:
    """
    Genera imagen usando el cluster distribuido de AI Horde (aihorde.net).
    100% gratuito, sin tarjeta de crédito ni número de teléfono.
    """
    dim_map = {
        "9:16": (512, 768),
        "1:1": (512, 512),
        "4:5": (512, 640)
    }
    width, height = dim_map.get(aspect_ratio, (512, 768))

    headers = {
        "apikey": api_key.strip() if api_key and api_key.strip() else "0000000000",
        "Client-Agent": "JesusReelsStudio:4.0:contact@jesusreels.local",
        "Content-Type": "application/json"
    }

    full_prompt = (
        f"{prompt.strip()}, cinematic sacred holy lighting, warm golden rays, "
        f"detailed biblical portrait, photorealistic, 8k ### ugly, deformed, blurry, low quality, modern clothes, text, watermark"
    )

    target_models = ["stable_diffusion"]
    if api_key and api_key not in ("0000000000", ""):
        target_models = ["stable_diffusion", "DreamShaper XL", "Stable Diffusion XL"]

    payload = {
        "prompt": full_prompt,
        "params": {
            "steps": 20,
            "width": width,
            "height": height,
            "sampler_name": "k_euler",
            "cfg_scale": 7.0
        },
        "models": target_models,
        "nsfw": False,
        "censor_nsfw": False
    }

    print(f"[AI Horde] Enviando tarea a la cola comunitaria ({width}x{height})...")
    res = requests.post("https://aihorde.net/api/v2/generate/async", json=payload, headers=headers, timeout=20)
    if res.status_code not in (200, 202):
        err_text = res.text[:250]
        raise RuntimeError(f"Error al enviar a AI Horde ({res.status_code}): {err_text}")

    task_id = res.json().get("id")
    if not task_id:
        raise RuntimeError("AI Horde no devolvió un ID de tarea.")

    start_time = time.time()
    while time.time() - start_time < timeout_sec:
        time.sleep(3)
        try:
            check_res = requests.get(f"https://aihorde.net/api/v2/generate/check/{task_id}", headers=headers, timeout=10)
            if check_res.status_code == 200:
                check = check_res.json()
                if check.get("done"):
                    status_res = requests.get(f"https://aihorde.net/api/v2/generate/status/{task_id}", headers=headers, timeout=10)
                    gens = status_res.json().get("generations", [])
                    if gens and gens[0].get("img"):
                        img_url = gens[0]["img"]
                        print(f"[AI Horde] Imagen completada. Descargando de {img_url[:60]}...")
                        img_resp = requests.get(img_url, timeout=20)
                        if img_resp.status_code == 200:
                            return img_resp.content
                    raise RuntimeError("AI Horde reportó éxito pero no devolvió el archivo de imagen.")
                if check.get("faulted"):
                    raise RuntimeError("La tarea de AI Horde falló en los servidores voluntarios.")
        except Exception as e:
            if "AI Horde" in str(e):
                raise
            print(f"[AI Horde] Reintentando verificación de cola: {e}")

    raise TimeoutError(f"AI Horde tardó más de {timeout_sec}s en la cola comunitaria.")

# ─── Motor 3: Hugging Face (Diagnóstico y Explicación de Estado 410) ──────────

def generate_huggingface_flux(prompt: str, hf_token: str) -> bytes:
    """
    Intento de llamada a Hugging Face Serverless.
    Informa detalladamente si el endpoint 410 está activo.
    """
    if not hf_token:
        raise ValueError("Hugging Face API Token (hf_...) es obligatorio.")

    endpoints = [
        "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell",
        "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
    ]
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    payload = {"inputs": prompt}

    last_err = ""
    for url in endpoints:
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=20)
            if resp.status_code == 200 and "image" in resp.headers.get("Content-Type", ""):
                return resp.content
            last_err = f"Status {resp.status_code}: {resp.text[:200]}"
        except Exception as e:
            last_err = str(e)

    raise RuntimeError(
        f"Hugging Face Inference API devolvió: {last_err}. "
        "Aviso técnico: Hugging Face descontinuó la generación serverless gratuita para este modelo (Status 410). "
        "Te recomendamos seleccionar Leonardo Phoenix en Cloudflare Workers AI o AI Horde."
    )

# ─── Función Maestra de Generación de Escena ──────────────────────────────────

def generate_ai_scene_image(
    prompt: str,
    aspect_ratio: str = "9:16",
    label: str = "Escena IA",
    provider: str = "auto",
    cf_model: Optional[str] = None,
    cf_account_id: Optional[str] = None,
    cf_api_token: Optional[str] = None,
    aihorde_api_key: Optional[str] = None,
    hf_token: Optional[str] = None
) -> Dict:
    """
    Genera una imagen con el motor elegido:
    - Cloudflare Workers AI (Leonardo Phoenix 1.0, Leonardo Lucid Origin, FLUX)
    - AI Horde (Comunidad gratuita sin suscripción)
    - Hugging Face
    - Auto (Prioriza Leonardo en Cloudflare si está configurado, luego AI Horde)
    - Fallback: Biblioteca temática local HD
    """
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("El prompt no puede estar vacío.")

    keys = load_keys()
    cf_acc = cf_account_id or keys.get("cf_account_id", "")
    cf_tok = cf_api_token or keys.get("cf_api_token", "")
    cf_mod = cf_model or keys.get("cf_model") or "@cf/leonardo/phoenix-1.0"
    horde_key = aihorde_api_key or keys.get("aihorde_api_key", "0000000000")
    hf_tok = hf_token or keys.get("hf_token", "")

    filename = f"custom_ai_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join(ASSETS_DIR, filename)

    img_bytes = None
    engine_used = None

    # Mapeo de providers desde el dropdown de interfaz
    is_cf = provider.startswith("cloudflare")
    if provider == "cloudflare_lucid":
        cf_mod = "@cf/leonardo/lucid-origin"
    elif provider == "cloudflare_flux":
        cf_mod = "@cf/black-forest-labs/flux-1-schnell"
    elif provider == "cloudflare_phoenix" or provider == "cloudflare":
        cf_mod = cf_mod or "@cf/leonardo/phoenix-1.0"

    quota_notice = None

    # Intento 1: Cloudflare Workers AI
    if (is_cf or (provider == "auto" and cf_acc and cf_tok)) and cf_acc and cf_tok:
        try:
            img_bytes = generate_cloudflare_image(prompt, cf_acc, cf_tok, model=cf_mod)
            model_display = "Leonardo Phoenix 1.0" if "phoenix" in cf_mod else ("Leonardo Lucid Origin" if "lucid" in cf_mod else "FLUX.1")
            engine_used = f"Cloudflare AI ({model_display})"
        except Exception as e:
            err_str = str(e)
            print(f"[ImageGen] Cloudflare falló: {err_str}")
            if "10,000 neurons" in err_str.lower() or "429" in err_str:
                quota_notice = "Tus 10,000 neuronas diarias de Cloudflare se agotaron por hoy. Generando con AI Horde como respaldo gratuito..."
                print(f"[ImageGen] {quota_notice}")
            elif is_cf and provider != "auto":
                # Si falló por otra causa y el usuario especificó Cloudflare, intentar AI Horde de rescate
                quota_notice = f"Cloudflare reportó: {err_str[:120]}. Activando respaldo con AI Horde..."

    # Intento 2: AI Horde (Si Cloudflare no devolvió imagen o si se seleccionó AI Horde / auto)
    if not img_bytes and (provider == "aihorde" or is_cf or provider == "auto"):
        try:
            img_bytes = generate_ai_horde(prompt, api_key=horde_key, aspect_ratio=aspect_ratio, timeout_sec=50)
            engine_used = "AI Horde (Comunidad Gratuita)"
        except Exception as e:
            print(f"[ImageGen] AI Horde falló: {e}")
            if provider == "aihorde":
                raise

    # Intento 3: Hugging Face si fue pedido expresamente
    if not img_bytes and provider == "huggingface" and hf_tok:
        try:
            img_bytes = generate_huggingface_flux(prompt, hf_tok)
            engine_used = "Hugging Face"
        except Exception as e:
            print(f"[ImageGen] Hugging Face falló: {e}")
            raise

    # Procesar y guardar bytes generados
    if img_bytes:
        try:
            pil_img = Image.open(BytesIO(img_bytes)).convert("RGB")
            pil_img.save(filepath, "JPEG", quality=95)
            ret = {
                "status": "success",
                "filename": filename,
                "url": f"/assets/images/{filename}",
                "label": f"{label} ({engine_used})",
                "engine": engine_used,
                "deletable": True
            }
            if quota_notice:
                ret["notice"] = quota_notice
            return ret
        except Exception as e:
            print(f"[ImageGen] Error al procesar imagen generada: {e}")

    # Fallback Seguro: Galería Local Cinematográfica
    prompt_low = prompt.lower()
    candidate_map = [
        (["child", "son", "daughter", "nieto", "baby", "crib", "youth"], "jesus_reaching_hand.jpg"),
        (["protect", "family", "shield", "muro", "home", "warfare", "battle"], "holy_cross_calvary.jpg"),
        (["night", "sleep", "anxiety", "insomnia", "peace", "rest", "worry"], "jesus_praying_gethsemane.jpg"),
        (["heal", "body", "sick", "doctor", "fever", "pain", "hospital"], "jesus_healing_miracle.jpg"),
        (["bible", "word", "scripture", "read", "truth", "verse"], "jesus_holy_bible.jpg"),
        (["embrace", "comfort", "tears", "cry", "love", "mercy"], "jesus_comforting_embrace.jpg")
    ]
    matched_img = None
    for keywords, img_name in candidate_map:
        if any(k in prompt_low for k in keywords):
            p = os.path.join(ASSETS_DIR, img_name)
            if os.path.exists(p):
                matched_img = p
                break

    if not matched_img:
        lib_imgs = [
            os.path.join(ASSETS_DIR, f) for f in os.listdir(ASSETS_DIR)
            if f.lower().endswith((".jpg", ".jpeg", ".png")) and not f.startswith("custom_")
        ]
        matched_img = random.choice(lib_imgs) if lib_imgs else os.path.join(ASSETS_DIR, "jesus_healing_miracle.jpg")

    if os.path.exists(matched_img):
        shutil.copyfile(matched_img, filepath)
    else:
        fb_img = Image.new("RGB", (768, 1344), (20, 24, 38))
        fb_img.save(filepath, "JPEG")

    return {
        "status": "success",
        "filename": filename,
        "url": f"/assets/images/{filename}",
        "label": f"{label} (Biblioteca HD)",
        "engine": "Biblioteca Local HD",
        "deletable": True,
        "notice": "Se asignó una escena cinematográfica HD de la biblioteca temática."
    }
