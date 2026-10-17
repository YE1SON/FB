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

# ─── Gestión de Claves y Configuración ────────────────────────────────────────

def load_keys() -> Dict[str, str]:
    """Carga claves desde ai_keys.json y variables de entorno."""
    keys = {
        "cf_account_id": os.environ.get("CF_ACCOUNT_ID", os.environ.get("CLOUDFLARE_ACCOUNT_ID", "")),
        "cf_api_token": os.environ.get("CF_API_TOKEN", os.environ.get("CLOUDFLARE_API_TOKEN", "")),
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

def save_keys(cf_account_id: Optional[str] = None, cf_api_token: Optional[str] = None, hf_token: Optional[str] = None) -> Dict[str, str]:
    """Guarda claves en ai_keys.json para que persistan entre reinicios."""
    current = load_keys()
    if cf_account_id is not None:
        current["cf_account_id"] = cf_account_id.strip()
    if cf_api_token is not None:
        current["cf_api_token"] = cf_api_token.strip()
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
    return {
        "cloudflare": {
            "configured": bool(keys.get("cf_account_id") and keys.get("cf_api_token")),
            "account_id_masked": (keys.get("cf_account_id")[:6] + "...") if keys.get("cf_account_id") else "",
            "model": "@cf/black-forest-labs/flux-1-schnell",
            "name": "Cloudflare Workers AI (FLUX.1 HD — 10k Neuronas/día gratis)"
        },
        "huggingface": {
            "configured": bool(keys.get("hf_token")),
            "token_masked": (keys.get("hf_token")[:7] + "...") if keys.get("hf_token") else "",
            "model": "black-forest-labs/FLUX.1-schnell",
            "name": "Hugging Face Inference API (FLUX.1 HD — Token Gratuito)"
        }
    }

# ─── Optimización de Prompts para FLUX.1 ──────────────────────────────────────

def enhance_flux_prompt(prompt: str) -> str:
    """
    Optimiza el texto para el modelo FLUX.1.
    Elimina términos anticuados de Midjourney/SD (octane render, 8k) que empeoran a FLUX,
    y añade descriptores ópticos de cámara y luz sagrada natural.
    """
    clean = prompt.strip()
    # Eliminar clichés que deforman o artificializan a FLUX
    clean = re.sub(r'(?i)\b(octane render|masterpiece|award winning|trending on artstation|hyperrealistic|8k|4k|unreal engine)\b', '', clean).strip()
    clean = re.sub(r'\s+', ' ', clean)

    cinematic_cues = (
        "cinematic photograph, warm sacred golden hour lighting, gentle depth of field, "
        "natural skin texture, authentic holy atmosphere, 35mm lens portrait, dramatic composition, photorealistic"
    )

    if "photograph" not in clean.lower() and "photo" not in clean.lower():
        return f"{clean}, {cinematic_cues}"
    return f"{clean}, warm sacred golden hour lighting, high fidelity, 35mm lens"

# ─── Motor 1: Cloudflare Workers AI (FLUX.1-schnell) ──────────────────────────

def generate_cloudflare_flux(prompt: str, account_id: str, api_token: str) -> bytes:
    """
    Genera imagen usando el modelo oficial @cf/black-forest-labs/flux-1-schnell
    alojado en Cloudflare Workers AI (10,000 neuronas gratis por día).
    """
    if not account_id or not api_token:
        raise ValueError("Cloudflare Account ID y API Token son obligatorios.")

    endpoint = f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/@cf/black-forest-labs/flux-1-schnell"
    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "prompt": enhance_flux_prompt(prompt),
        "steps": 4  # Optimizado para schnell
    }

    print(f"[Cloudflare FLUX] Enviando petición a Workers AI...")
    resp = requests.post(endpoint, headers=headers, json=payload, timeout=40)

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
        # Respuesta binaria directa (image/png o image/jpeg)
        return resp.content

# ─── Motor 2: Hugging Face Serverless API (FLUX.1-schnell) ───────────────────

def generate_huggingface_flux(prompt: str, hf_token: str) -> bytes:
    """
    Genera imagen usando el modelo oficial black-forest-labs/FLUX.1-schnell
    a través de la API Serverless de Hugging Face.
    """
    if not hf_token:
        raise ValueError("Hugging Face API Token (hf_...) es obligatorio.")

    endpoints = [
        "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell",
        "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
    ]
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }
    payload = {
        "inputs": enhance_flux_prompt(prompt),
        "parameters": {
            "num_inference_steps": 4
        }
    }

    last_err = ""
    for url in endpoints:
        try:
            print(f"[HuggingFace FLUX] Enviando petición a {url}...")
            for attempt in range(2):
                resp = requests.post(url, headers=headers, json=payload, timeout=45)
                if resp.status_code == 200 and "image" in resp.headers.get("Content-Type", "image/"):
                    return resp.content
                if resp.status_code == 503:
                    # Modelo inicializándose, esperar y reintentar
                    print("[HuggingFace FLUX] Modelo en cola (503). Esperando 4 segundos...")
                    time.sleep(4)
                    continue
                last_err = f"Status {resp.status_code}: {resp.text[:300]}"
                break
        except Exception as e:
            last_err = str(e)

    raise RuntimeError(f"Error en Hugging Face: {last_err}")

# ─── Función Maestra de Generación de Escena ──────────────────────────────────

def generate_ai_scene_image(
    prompt: str,
    aspect_ratio: str = "9:16",
    label: str = "Escena IA",
    provider: str = "auto",
    cf_account_id: Optional[str] = None,
    cf_api_token: Optional[str] = None,
    hf_token: Optional[str] = None
) -> Dict:
    """
    Genera una imagen con el motor elegido (Cloudflare o Hugging Face).
    Si faltan credenciales o fallan las llamadas, asigna con seguridad una escena
    cinematográfica de la biblioteca bíblica local en alta resolución (NUNCA Pollinations).
    """
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("El prompt no puede estar vacío.")

    keys = load_keys()
    cf_acc = cf_account_id or keys.get("cf_account_id", "")
    cf_tok = cf_api_token or keys.get("cf_api_token", "")
    hf_tok = hf_token or keys.get("hf_token", "")

    filename = f"custom_ai_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join(ASSETS_DIR, filename)

    img_bytes = None
    engine_used = None

    # Determinar orden de intentos según provider
    if provider == "cloudflare" or (provider == "auto" and cf_acc and cf_tok):
        try:
            img_bytes = generate_cloudflare_flux(prompt, cf_acc, cf_tok)
            engine_used = "Cloudflare FLUX.1 HD"
        except Exception as e:
            print(f"[ImageGen] Cloudflare falló: {e}")
            if provider == "cloudflare":
                raise

    if not img_bytes and (provider == "huggingface" or (provider == "auto" and hf_tok)):
        try:
            img_bytes = generate_huggingface_flux(prompt, hf_tok)
            engine_used = "Hugging Face FLUX.1 HD"
        except Exception as e:
            print(f"[ImageGen] Hugging Face falló: {e}")
            if provider == "huggingface":
                raise

    # Si obtuvimos bytes de imagen de Cloudflare o Hugging Face:
    if img_bytes:
        try:
            pil_img = Image.open(BytesIO(img_bytes)).convert("RGB")
            # Guardar con calidad 95
            pil_img.save(filepath, "JPEG", quality=95)
            print(f"[ImageGen] Imagen generada con éxito ({engine_used}) -> {filename}")
            return {
                "status": "success",
                "filename": filename,
                "url": f"/assets/images/{filename}",
                "label": f"{label} ({engine_used})",
                "engine": engine_used,
                "deletable": True
            }
        except Exception as e:
            print(f"[ImageGen] Error al procesar imagen generada: {e}")

    # Fallback Seguro: Galería Local Cinematográfica (Cero dependencias fallidas)
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
