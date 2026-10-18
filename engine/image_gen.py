import os
import re
import json
import uuid
import time
import shutil
import random
import requests
from io import BytesIO
from typing import Dict, Optional, Tuple
from PIL import Image
from gradio_client import Client

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
KEYS_FILE = os.path.join(BASE_DIR, "ai_keys.json")

os.makedirs(ASSETS_DIR, exist_ok=True)

# ─── Gestión de Claves y Configuración ────────────────────────────────────────

def load_keys() -> Dict[str, str]:
    """Carga claves desde ai_keys.json y variables de entorno."""
    keys = {
        "hf_token": os.environ.get("HF_TOKEN", os.environ.get("HUGGINGFACE_TOKEN", "")),
        "aihorde_api_key": os.environ.get("AIHORDE_API_KEY", "0000000000")
    }
    if os.path.exists(KEYS_FILE):
        try:
            with open(KEYS_FILE, "r", encoding="utf-8") as f:
                saved = json.load(f)
                if saved.get("hf_token"):
                    keys["hf_token"] = saved["hf_token"]
                if saved.get("aihorde_api_key"):
                    keys["aihorde_api_key"] = saved["aihorde_api_key"]
        except Exception as e:
            print(f"[ImageGen] Error al leer ai_keys.json: {e}")
    return keys

def save_keys(
    hf_token: Optional[str] = None,
    aihorde_api_key: Optional[str] = None,
    **kwargs
) -> Dict[str, str]:
    """Guarda claves en ai_keys.json."""
    current = load_keys()
    if hf_token is not None:
        current["hf_token"] = hf_token.strip()
    if aihorde_api_key is not None:
        current["aihorde_api_key"] = aihorde_api_key.strip() or "0000000000"

    try:
        with open(KEYS_FILE, "w", encoding="utf-8") as f:
            json.dump(current, f, indent=2)
    except Exception as e:
        print(f"[ImageGen] Error al guardar ai_keys.json: {e}")
    return current

def get_providers_status() -> Dict:
    """Retorna el estado de los motores de generación de IA integrados."""
    keys = load_keys()
    hf_tok = keys.get("hf_token", "")
    return {
        "z_image": {
            "name": "🥇 Z-Image Turbo (Alibaba Tongyi DiT — Máxima Calidad y Rapidez)",
            "configured": True,
            "status": "Activo y Gratuito (Sub-5s)"
        },
        "flux_schnell": {
            "name": "🥈 FLUX.1 Schnell (Black Forest Labs HD)",
            "configured": bool(hf_tok),
            "token_masked": (hf_tok[:7] + "...") if hf_tok else "",
            "status": "Activo con Token HF" if hf_tok else "Disponible (Con o sin Token)"
        },
        "aihorde": {
            "name": "🥉 AI Horde (Comunidad Gratuita Descentralizada)",
            "configured": True,
            "status": "Activo (Sin límites)"
        }
    }

# ─── Optimización de Prompts Sagrados ────────────────────────────────────────

def enhance_sacred_prompt(prompt: str) -> str:
    """Optimiza el texto para máximo fotorrealismo bíblico e iluminación dorada."""
    clean = prompt.strip()
    clean = re.sub(r'(?i)\b(octane render|masterpiece|award winning|trending on artstation|hyperrealistic|8k|4k|unreal engine)\b', '', clean).strip()
    clean = re.sub(r'\s+', ' ', clean)

    cues = (
        "cinematic photograph, warm sacred golden hour lighting, authentic historical biblical atmosphere, "
        "dramatic depth of field, natural skin texture, 35mm portrait lens, photorealistic"
    )
    if "photograph" not in clean.lower() and "cinematic" not in clean.lower():
        return f"{clean}, {cues}"
    return f"{clean}, warm sacred golden hour lighting, photorealistic, 35mm lens"

# ─── Motor 1: Z-Image Turbo (Tongyi-MAI DiT) ──────────────────────────────────

def generate_z_image_turbo(
    prompt: str,
    aspect_ratio: str = "9:16",
    hf_token: Optional[str] = None
) -> bytes:
    """
    Genera imagen fotorrealista con Z-Image Turbo (Tongyi-MAI DiT).
    Tiempo de respuesta: ~5 segundos en VPS. Calidad superior con anatomía impecable.
    """
    clean_prompt = enhance_sacred_prompt(prompt)
    res_map = {
        "9:16": "720x1280 ( 9:16 )",
        "1:1": "1024x1024 ( 1:1 )",
        "4:5": "864x1152 ( 3:4 )"
    }
    resolution = res_map.get(aspect_ratio, "720x1280 ( 9:16 )")

    print(f"[Z-Image Turbo] Conectando a Tongyi-MAI Space ({resolution})...")
    client = Client("Tongyi-MAI/Z-Image-Turbo", token=hf_token or None)
    result = client.predict(
        prompt=clean_prompt,
        resolution=resolution,
        seed=random.randint(1, 999999),
        steps=8,
        shift=3.0,
        random_seed=True,
        gallery_images=[],
        api_name="/generate"
    )

    if isinstance(result, (tuple, list)) and len(result) > 0:
        gallery = result[0]
        if isinstance(gallery, list) and len(gallery) > 0 and "image" in gallery[0]:
            img_path = gallery[0]["image"]
            if os.path.exists(img_path):
                with open(img_path, "rb") as f:
                    return f.read()

    raise RuntimeError(f"Z-Image Turbo no devolvió un archivo de imagen válido: {result}")

# ─── Motor 2: FLUX.1 Schnell (Black Forest Labs Oficial) ─────────────────────

def generate_flux_schnell_space(
    prompt: str,
    aspect_ratio: str = "9:16",
    hf_token: Optional[str] = None
) -> bytes:
    """
    Genera imagen con el modelo oficial FLUX.1 [schnell] de Black Forest Labs.
    Fotorrealismo cinematográfico, iluminación de atardecer y proporciones exactas.
    """
    clean_prompt = enhance_sacred_prompt(prompt)
    dims = {
        "9:16": (768, 1360),
        "1:1": (1024, 1024),
        "4:5": (832, 1040)
    }
    width, height = dims.get(aspect_ratio, (768, 1360))

    print(f"[FLUX.1 Schnell] Conectando a Black Forest Labs Space ({width}x{height})...")
    client = Client("black-forest-labs/FLUX.1-schnell", token=hf_token or None)
    result = client.predict(
        prompt=clean_prompt,
        seed=0,
        randomize_seed=True,
        width=width,
        height=height,
        num_inference_steps=4,
        api_name="/infer"
    )

    if isinstance(result, (tuple, list)) and len(result) > 0:
        img_path = result[0]
        if isinstance(img_path, str) and os.path.exists(img_path):
            with open(img_path, "rb") as f:
                return f.read()

    raise RuntimeError(f"FLUX.1 Schnell no devolvió un archivo de imagen válido: {result}")

# ─── Motor 3: AI Horde (Red Comunitaria de GPUs) ─────────────────────────────

def generate_ai_horde(
    prompt: str,
    api_key: str = "0000000000",
    aspect_ratio: str = "9:16",
    timeout_sec: int = 50
) -> bytes:
    """
    Genera imagen usando el cluster distribuido de AI Horde (aihorde.net).
    100% gratuito, sin tarjeta ni suscripción.
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
            print(f"[AI Horde] Reintentando verificación: {e}")

    raise TimeoutError(f"AI Horde tardó más de {timeout_sec}s en la cola comunitaria.")

# ─── Función Maestra de Generación de Escena ──────────────────────────────────

def generate_ai_scene_image(
    prompt: str,
    aspect_ratio: str = "9:16",
    label: str = "Escena IA",
    provider: str = "auto",
    hf_token: Optional[str] = None,
    aihorde_api_key: Optional[str] = None,
    **kwargs
) -> Dict:
    """
    Genera una escena de alta calidad utilizando los motores avanzados:
    1. Z-Image Turbo (Tongyi-MAI DiT) — Máxima calidad fotográfica y velocidad.
    2. FLUX.1 Schnell (Black Forest Labs) — Fotorrealismo y luces cinematográficas.
    3. AI Horde — Respaldo gratuito comunitario.
    4. Biblioteca Local HD — Respaldo instantáneo sin fallos.
    """
    prompt = prompt.strip()
    if not prompt:
        raise ValueError("El prompt no puede estar vacío.")

    keys = load_keys()
    hf_tok = hf_token or keys.get("hf_token", "")
    horde_key = aihorde_api_key or keys.get("aihorde_api_key", "0000000000")

    filename = f"custom_ai_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join(ASSETS_DIR, filename)

    img_bytes = None
    engine_used = None

    # Intento 1: Z-Image Turbo (Si fue seleccionado o en auto)
    if provider in ("z_image", "auto"):
        try:
            img_bytes = generate_z_image_turbo(prompt, aspect_ratio=aspect_ratio, hf_token=hf_tok)
            engine_used = "Z-Image Turbo HD"
        except Exception as e:
            print(f"[ImageGen] Z-Image Turbo no pudo completar: {e}")
            if provider == "z_image":
                # Intentar rescate automático con FLUX.1 Schnell
                print("[ImageGen] Activando rescate automático con FLUX.1 Schnell...")

    # Intento 2: FLUX.1 Schnell (Si fue seleccionado o como rescate de Z-Image)
    if not img_bytes and provider in ("flux_schnell", "z_image", "auto"):
        try:
            img_bytes = generate_flux_schnell_space(prompt, aspect_ratio=aspect_ratio, hf_token=hf_tok)
            engine_used = "FLUX.1 Schnell HD"
        except Exception as e:
            print(f"[ImageGen] FLUX.1 Schnell no pudo completar: {e}")
            if provider == "flux_schnell":
                # Intentar rescate con Z-Image Turbo
                try:
                    img_bytes = generate_z_image_turbo(prompt, aspect_ratio=aspect_ratio, hf_token=hf_tok)
                    engine_used = "Z-Image Turbo HD (Rescate)"
                except Exception:
                    pass

    # Intento 3: AI Horde (Si fue seleccionado o como segundo respaldo)
    if not img_bytes and provider in ("aihorde", "auto", "z_image", "flux_schnell"):
        try:
            img_bytes = generate_ai_horde(prompt, api_key=horde_key, aspect_ratio=aspect_ratio, timeout_sec=45)
            engine_used = "AI Horde (Comunidad Gratuita)"
        except Exception as e:
            print(f"[ImageGen] AI Horde no pudo completar: {e}")
            if provider == "aihorde":
                raise

    # Procesar y guardar bytes generados
    if img_bytes:
        try:
            pil_img = Image.open(BytesIO(img_bytes)).convert("RGB")
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
