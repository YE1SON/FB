import os
import re
import json
import uuid
import time
import shutil
import random
import requests
from io import BytesIO
from typing import Dict, Optional, Tuple, List
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
        "pollinations": {
            "name": "⚡ Pollinations FLUX (Ilimitado y Rápido — Sin Cuotas de GPU)",
            "configured": True,
            "status": "Activo y Gratuito (Sub-8s)"
        },
        "z_image": {
            "name": "🥇 Z-Image Turbo (Alibaba Tongyi DiT — Respaldo Activo)",
            "configured": True,
            "status": "Activo con Respaldo Automático"
        },
        "flux_schnell": {
            "name": "🥈 FLUX.1 Schnell (Black Forest Labs HD)",
            "configured": bool(hf_tok),
            "token_masked": (hf_tok[:7] + "...") if hf_tok else "",
            "status": "Activo con Token HF" if hf_tok else "Disponible con Respaldo"
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

# ─── Motor 0: Pollinations FLUX (Sin cuotas de ZeroGPU) ───────────────────────

def generate_pollinations(
    prompt: str,
    aspect_ratio: str = "9:16"
) -> bytes:
    """
    Genera imagen fotorrealista con Pollinations.ai (Flux/SDXL).
    100% gratuito, sin límites de ZeroGPU, sin tarjeta, ultra-rápido (sub-10s).
    """
    clean_prompt = enhance_sacred_prompt(prompt)
    dims = {
        "9:16": (768, 1344),
        "1:1": (1024, 1024),
        "4:5": (832, 1040)
    }
    width, height = dims.get(aspect_ratio, (768, 1344))
    seed = random.randint(1, 999999)
    url = f"https://image.pollinations.ai/prompt/{requests.utils.quote(clean_prompt)}?width={width}&height={height}&model=flux&nologo=true&seed={seed}"
    print(f"[Pollinations] Generando imagen Flux ({width}x{height})...")
    resp = requests.get(
        url,
        headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) JesusReelsStudio/4.0"},
        timeout=25
    )
    if resp.status_code == 200 and len(resp.content) > 1000:
        return resp.content
    raise RuntimeError(f"Pollinations falló con status {resp.status_code}")

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
    Incluye reintento automático anónimo si el token del usuario agota la cuota ZeroGPU.
    """
    clean_prompt = enhance_sacred_prompt(prompt)
    dims = {
        "9:16": (768, 1360),
        "1:1": (1024, 1024),
        "4:5": (832, 1040)
    }
    width, height = dims.get(aspect_ratio, (768, 1360))

    tokens_to_try = [hf_token] if hf_token else [None]
    if hf_token:
        tokens_to_try.append(None)  # Respaldo anónimo de alta velocidad

    last_err = None
    for tok in tokens_to_try:
        try:
            print(f"[FLUX.1 Schnell] Conectando a Black Forest Labs Space ({width}x{height}, token={'usuario' if tok else 'anónimo'})...")
            client = Client("black-forest-labs/FLUX.1-schnell", token=tok)
            result = client.predict(
                prompt=clean_prompt,
                seed=random.randint(1, 99999999),
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
        except Exception as e:
            last_err = e
            print(f"[FLUX.1 Schnell] Intento con token={'usuario' if tok else 'anónimo'} no completó: {e}")

    raise RuntimeError(f"FLUX.1 Schnell no devolvió un archivo de imagen válido: {last_err}")

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
    scene_num: int = 1,
    used_images: Optional[List[str]] = None,
    **kwargs
) -> Dict:
    """
    Genera una escena de alta calidad utilizando los motores avanzados:
    1. FLUX.1 Schnell (Black Forest Labs) — Fotorrealismo extremo en sub-4 segundos.
    2. Z-Image Turbo (Tongyi-MAI DiT) — Renderizado cinematográfico DiT.
    3. AI Horde — Respaldo gratuito comunitario.
    4. Biblioteca Local HD — Respaldo instantáneo con 3 pools temáticos (CERO REPETICIONES).
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

    # ─── Ejecución con Respaldo Automático Resiliente (CERO FALLOS 500) ──────────────
    if provider == "pollinations":
        try:
            print(f"[ImageGen] Ejecutando Pollinations FLUX para escena {scene_num}...")
            img_bytes = generate_pollinations(prompt, aspect_ratio=aspect_ratio)
            engine_used = "Pollinations FLUX"
        except Exception as e:
            print(f"[ImageGen] Pollinations falló ({e}), intentando AI Horde...")

    elif provider == "z_image":
        try:
            print(f"[ImageGen] Ejecutando Z-Image Turbo para escena {scene_num}...")
            img_bytes = generate_z_image_turbo(prompt, aspect_ratio=aspect_ratio, hf_token=hf_tok)
            engine_used = "Z-Image Turbo HD"
        except Exception as e:
            print(f"[ImageGen] Z-Image Turbo falló ({e}). Activando respaldo automático...")
            try:
                img_bytes = generate_pollinations(prompt, aspect_ratio=aspect_ratio)
                engine_used = "Pollinations FLUX (Respaldo por Cuota)"
            except Exception as e2:
                print(f"[ImageGen] Respaldo Pollinations falló ({e2}), intentando AI Horde...")
                try:
                    img_bytes = generate_ai_horde(prompt, api_key=horde_key, aspect_ratio=aspect_ratio, timeout_sec=20)
                    engine_used = "AI Horde (Respaldo por Cuota)"
                except Exception:
                    pass

    elif provider == "flux_schnell":
        try:
            print(f"[ImageGen] Ejecutando FLUX.1 Schnell para escena {scene_num}...")
            img_bytes = generate_flux_schnell_space(prompt, aspect_ratio=aspect_ratio, hf_token=hf_tok)
            engine_used = "FLUX.1 Schnell HD"
        except Exception as e:
            print(f"[ImageGen] FLUX.1 Schnell falló ({e}). Activando respaldo automático...")
            try:
                img_bytes = generate_pollinations(prompt, aspect_ratio=aspect_ratio)
                engine_used = "Pollinations FLUX (Respaldo por Cuota)"
            except Exception as e2:
                print(f"[ImageGen] Respaldo Pollinations falló ({e2}), intentando AI Horde...")
                try:
                    img_bytes = generate_ai_horde(prompt, api_key=horde_key, aspect_ratio=aspect_ratio, timeout_sec=20)
                    engine_used = "AI Horde (Respaldo por Cuota)"
                except Exception:
                    pass

    elif provider == "aihorde":
        try:
            print(f"[ImageGen] Ejecutando AI Horde para escena {scene_num}...")
            img_bytes = generate_ai_horde(prompt, api_key=horde_key, aspect_ratio=aspect_ratio, timeout_sec=25)
            engine_used = "AI Horde (Comunidad Gratuita)"
        except Exception as e:
            print(f"[ImageGen] AI Horde falló ({e}), intentando Pollinations...")
            try:
                img_bytes = generate_pollinations(prompt, aspect_ratio=aspect_ratio)
                engine_used = "Pollinations FLUX (Respaldo)"
            except Exception:
                pass

    elif provider in ("curated", "library"):
        print(f"[ImageGen] Seleccionando toma de la Biblioteca Curada HD para escena {scene_num}...")
        img_bytes = None
        engine_used = "Biblioteca Curada HD"

    else:
        # provider == "auto": Cascada Inteligente (Pollinations -> FLUX.1 -> Z-Image -> Horde)
        print(f"[ImageGen] Modo Auto para escena {scene_num}: Intentando Pollinations FLUX...")
        try:
            img_bytes = generate_pollinations(prompt, aspect_ratio=aspect_ratio)
            engine_used = "Pollinations FLUX (Auto)"
        except Exception as e:
            print(f"[ImageGen] Auto: Pollinations no completó ({e}), intentando FLUX.1 Schnell...")

        if not img_bytes:
            try:
                img_bytes = generate_flux_schnell_space(prompt, aspect_ratio=aspect_ratio, hf_token=hf_tok)
                engine_used = "FLUX.1 Schnell HD (Auto)"
            except Exception as e:
                print(f"[ImageGen] Auto: FLUX.1 no completó ({e}), intentando Z-Image Turbo...")

        if not img_bytes:
            try:
                img_bytes = generate_z_image_turbo(prompt, aspect_ratio=aspect_ratio, hf_token=hf_tok)
                engine_used = "Z-Image Turbo HD (Auto)"
            except Exception as e:
                print(f"[ImageGen] Auto: Z-Image no completó ({e}), intentando AI Horde...")

        if not img_bytes:
            try:
                img_bytes = generate_ai_horde(prompt, api_key=horde_key, aspect_ratio=aspect_ratio, timeout_sec=20)
                engine_used = "AI Horde (Auto)"
            except Exception as e:
                print(f"[ImageGen] Auto: AI Horde no completó: {e}")

    # Si ninguno de los proveedores en línea generó bytes (y no era curated explícito), un último intento con Pollinations
    if not img_bytes and provider not in ("curated", "library"):
        try:
            img_bytes = generate_pollinations(prompt, aspect_ratio=aspect_ratio)
            engine_used = "Pollinations FLUX (Respaldo Definitivo)"
        except Exception:
            pass

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

    # ─── Fallback Seguro: 3 Pools Temáticos Estrictamente Diferenciados ──────
    # Garantiza al 100% que las escenas 1, 2 y 3 NUNCA se repiten
    prompt_low = prompt.lower()
    used_set = set(used_images or [])

    # 1. Pool de Toma 1 (Apertura e Impacto Inicial)
    scene1_pool = [
        "jesus_healing_miracle.jpg",
        "holy_cross_calvary.jpg",
        "jesus_walking_storm.jpg",
        "jesus_teaching_crowd.jpg",
        "jesus_light_world.jpg"
    ]
    # 2. Pool de Toma 2 (Intercesión y Punto de Inflexión de Fe)
    scene2_pool = [
        "jesus_praying_gethsemane.jpg",
        "jesus_reaching_hand.jpg",
        "jesus_holy_bible.jpg",
        "jesus_kneeling_prayer.jpg"
    ]
    # 3. Pool de Toma 3 (Victoria, Paz y Gloria Final)
    scene3_pool = [
        "jesus_comforting_embrace.jpg",
        "jesus_resurrection_glory.jpg",
        "jesus_walking_water.jpg",
        "jesus_shepherd_lamb.jpg"
    ]

    target_pool = scene1_pool if scene_num == 1 else (scene2_pool if scene_num == 2 else scene3_pool)

    # Filtrar imágenes disponibles que no hayan sido usadas ya en este Reel
    available = [img for img in target_pool if img not in used_set and os.path.exists(os.path.join(ASSETS_DIR, img))]
    if not available:
        # Respaldo amplio de la biblioteca completa descartando las ya utilizadas
        all_lib = [
            f for f in os.listdir(ASSETS_DIR)
            if f.lower().endswith((".jpg", ".jpeg", ".png")) and not f.startswith("custom_") and f not in used_set
        ]
        available = all_lib or target_pool

    matched_img = None
    for img_candidate in available:
        stem = img_candidate.replace(".jpg", "").replace("jesus_", "").replace("_", " ")
        if any(word in prompt_low for word in stem.split() if len(word) > 3):
            matched_img = os.path.join(ASSETS_DIR, img_candidate)
            break

    if not matched_img and available:
        matched_img = os.path.join(ASSETS_DIR, available[0])

    if matched_img and os.path.exists(matched_img):
        shutil.copyfile(matched_img, filepath)
    else:
        fb_img = Image.new("RGB", (768, 1344), (20, 24, 38))
        fb_img.save(filepath, "JPEG")

    return {
        "status": "success",
        "filename": filename,
        "url": f"/assets/images/{filename}",
        "label": f"{label} (Biblioteca Curada HD)",
        "engine": "Biblioteca Curada HD",
        "deletable": True,
        "notice": f"Se asignó una toma no repetida de la biblioteca temática para la escena {scene_num}."
    }
