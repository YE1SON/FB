import json
import os
import random
import subprocess
import urllib.parse
from typing import Dict, List, Optional
import requests

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "broll_cache")
LOCAL_VIDEOS_DIR = os.path.join(BASE_DIR, "assets", "videos")

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY", "")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(LOCAL_VIDEOS_DIR, exist_ok=True)

# Consultas temáticas para cada escena
SCENE_QUERIES = {
    1: [  # Apertura y gancho
        "peaceful sunrise morning",
        "golden sunlight rays",
        "candle flame dark room",
        "gentle rain window",
        "misty green mountains"
    ],
    2: [  # Intercesión y reflexión
        "person praying hands",
        "open holy bible sunlight",
        "walking path forest",
        "calm ocean waves",
        "warm fireplace glow"
    ],
    3: [  # Paz y victoria
        "golden clouds sky sunset",
        "radiant sunburst mountains",
        "peaceful river nature",
        "bright sky sunbeams",
        "dove flying sky"
    ]
}

THEME_KEYWORDS: Dict[str, List[str]] = {
    "lost_child": ["family home", "walking path", "evening window", "open bible"],
    "family_protection": ["peaceful living room", "warm candlelight", "cozy home", "calm night"],
    "medical_fear": ["gentle sunrise", "morning light", "holding hands", "calm forest"],
    "zero_balance": ["sunrise mountains", "wheat field golden", "flowing stream", "open door"],
    "night_anxiety": ["starry night sky", "calm lake night", "peaceful moon", "candle light"],
    "morning_favor": ["glorious sunrise", "morning dew flowers", "sunlight rays", "mountain dawn"],
    "marriage_healing": ["couple walking sunset", "holding hands", "warm home", "gentle ocean"],
    "healing_depression": ["sunlight through trees", "mountain peak clouds", "peaceful nature", "gentle stream"],
    "job_breakthrough": ["morning city sun", "open door light", "walking forward", "golden sunrise"],
    "lonely_widow": ["cozy home fireplace", "peaceful garden", "soft sunlight window", "open bible"],
    "addiction_chains": ["breaking storm clouds", "running water river", "sunrise horizon", "ocean waves"],
    "elderly_parents": ["warm family table", "holding hands elders", "peaceful porch", "morning garden"],
    "single_parent": ["mother child embrace", "warm kitchen sunset", "park sunlight", "peaceful home"],
    "sick_grandchild": ["gentle sunrise", "flowers blooming", "peaceful morning", "holding hands"],
    "court_legal": ["sunlight pillars", "open sky mountains", "calm river", "golden dawn"],
    "restless_sleep": ["calm water reflection", "soft moonlight clouds", "candle flame", "peaceful night"],
    "gratitude_harvest": ["wheat field golden", "autumn forest sunlight", "fruit trees", "sunny meadow"],
    "unspoken_prayer": ["candle flame dark", "quiet room window", "misty lake dawn", "open bible"],
    "spiritual_warfare": ["mountain peaks clouds", "dramatic sky sunburst", "ocean cliffs", "eagle soaring"],
    "business_blessing": ["sunrise over fields", "flowing river clear", "morning light desk", "golden dawn"],
    "forgiving_past": ["calm ocean waves", "gentle morning breeze", "sunlight trees", "peaceful garden"],
    "grief_loss": ["peaceful sunset clouds", "candle flame soft", "quiet lake dawn", "dove in sky"],
    "guidance_direction": ["path in forest sunlight", "mountain trail sunrise", "lighthouse ocean", "compass map"],
    "strength_weary": ["eagle flying soaring", "mighty waterfall", "mountain sunrise", "running river"],
    "peace_in_storm": ["storm clouds breaking sunlight", "lighthouse stormy sea", "anchor water", "calm after rain"],
    "divine_grace": ["majestic sunbeams clouds", "golden cross hill", "celestial sunlight sky", "open heavens"]
}


def verify_video_file(file_path: str) -> Optional[Dict]:
    """
    Inspecciona con ffprobe el archivo de video real para garantizar:
    - Archivo válido y legible.
    - Resolución mínima aceptable (mínimo 720p).
    - Duración mínima de 3.0 segundos para evitar cortes bruscos.
    """
    if not os.path.exists(file_path) or os.path.getsize(file_path) < 100000:
        return None

    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,duration:format=duration",
        "-of", "json",
        file_path
    ]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=10)
        data = json.loads(proc.stdout)
        streams = data.get("streams", [])
        if not streams:
            return None

        v_stream = streams[0]
        width = int(v_stream.get("width", 0))
        height = int(v_stream.get("height", 0))

        # Extraer duración
        dur = 0.0
        if "duration" in v_stream and v_stream["duration"]:
            try:
                dur = float(v_stream["duration"])
            except Exception:
                pass
        if dur <= 0.0 and "format" in data and "duration" in data["format"]:
            try:
                dur = float(data["format"]["duration"])
            except Exception:
                pass

        # Validaciones de calidad estrictas
        if width < 720 and height < 720:
            print(f"[B-Roll Rejected] Baja resolución ({width}x{height}) en {file_path}")
            return None

        if dur > 0.0 and dur < 2.5:
            print(f"[B-Roll Rejected] Duración demasiado corta ({dur:.1f}s) en {file_path}")
            return None

        is_portrait = height >= width

        return {
            "file_path": file_path,
            "width": width,
            "height": height,
            "duration": dur if dur > 0 else 5.0,
            "is_portrait": is_portrait,
            "valid": True
        }
    except Exception as e:
        print(f"[B-Roll Probe Error] {file_path}: {e}")
        return None


def search_pexels_videos(query: str, per_page: int = 15) -> List[Dict]:
    """Busca videos HD verticales u horizontales en Pexels API."""
    if not PEXELS_API_KEY:
        return []

    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "orientation": "portrait",
        "size": "medium",
        "per_page": per_page
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("videos", [])
        else:
            print(f"[B-Roll Pexels] Status {resp.status_code}: {resp.text[:200]}")
            return []
    except Exception as e:
        print(f"[B-Roll Pexels Error]: {e}")
        return []


def search_pixabay_videos(query: str, per_page: int = 15) -> List[Dict]:
    """Busca videos HD en Pixabay API como alternativa gratuita."""
    if not PIXABAY_API_KEY:
        return []

    url = "https://pixabay.com/api/videos/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": urllib.parse.quote(query),
        "video_type": "all",
        "safesearch": "true",
        "per_page": per_page
    }

    try:
        resp = requests.get(url, params=params, timeout=12)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("hits", [])
        return []
    except Exception as e:
        print(f"[B-Roll Pixabay Error]: {e}")
        return []


def download_and_cache_video(url: str, filename_prefix: str) -> Optional[str]:
    """Descarga el video con streaming a la caché y lo valida."""
    safe_name = re.sub(r'[^A-Za-z0-9_]', '_', filename_prefix)[:40]
    out_name = f"{safe_name}_{random.randint(1000, 9999)}.mp4"
    out_path = os.path.join(CACHE_DIR, out_name)

    try:
        resp = requests.get(url, stream=True, timeout=60)
        resp.raise_for_status()

        with open(out_path, "wb") as f:
            for chunk in resp.iter_content(chunk_size=32768):
                f.write(chunk)

        # Validación de integridad técnica
        v_info = verify_video_file(out_path)
        if v_info and v_info["valid"]:
            print(f"[B-Roll Validated] {out_path} ({v_info['width']}x{v_info['height']}, {v_info['duration']:.1f}s)")
            return out_path
        else:
            if os.path.exists(out_path):
                os.remove(out_path)
            return None
    except Exception as e:
        print(f"[B-Roll Download Error]: {e}")
        if os.path.exists(out_path):
            os.remove(out_path)
        return None


def get_cached_or_local_clip(query_tag: str) -> Optional[str]:
    """Busca clips previamente descargados y aprobados en la biblioteca local o en caché."""
    candidates = []

    # 1. Revisar biblioteca aprobada local
    if os.path.exists(LOCAL_VIDEOS_DIR):
        for f in os.listdir(LOCAL_VIDEOS_DIR):
            if f.lower().endswith((".mp4", ".mov", ".webm")):
                candidates.append(os.path.join(LOCAL_VIDEOS_DIR, f))

    # 2. Revisar caché existente
    if os.path.exists(CACHE_DIR):
        clean_tag = query_tag.replace(" ", "_")[:25].lower()
        matched = [
            os.path.join(CACHE_DIR, f) for f in os.listdir(CACHE_DIR)
            if f.lower().endswith(".mp4") and clean_tag in f.lower()
        ]
        if matched:
            candidates.extend(matched)
        else:
            all_cached = [
                os.path.join(CACHE_DIR, f) for f in os.listdir(CACHE_DIR)
                if f.lower().endswith(".mp4")
            ]
            candidates.extend(all_cached)

    valid_candidates = []
    for c in candidates:
        v = verify_video_file(c)
        if v and v["valid"]:
            valid_candidates.append(c)

    if valid_candidates:
        return random.choice(valid_candidates)
    return None


def get_broll_clip(theme_key: str, scene_idx: int = 1, custom_query: Optional[str] = None) -> Optional[str]:
    """
    Obtiene un clip de video vertical o HD verificado para la escena:
    1. Si hay clips en caché o biblioteca local con calidad aprobada, los reutiliza.
    2. Si hay Pexels API Key configurada, busca y descarga video vertical HD.
    3. Si falla, intenta con Pixabay API.
    4. Si no hay conexión o claves, retorna None (activando el respaldo cinemático en video.py).
    """
    # Elegir query según tema y escena
    theme_terms = THEME_KEYWORDS.get(theme_key, ["peaceful sunrise", "open bible", "golden sunlight"])
    scene_pool = SCENE_QUERIES.get(scene_idx, SCENE_QUERIES[1])

    if custom_query and custom_query.strip():
        query = custom_query.strip()
    else:
        query = f"{random.choice(theme_terms)} {random.choice(scene_pool)}"

    # 1. Verificar si ya tenemos un clip válido en caché
    cached_clip = get_cached_or_local_clip(query)
    if cached_clip and random.random() < 0.60:
        return cached_clip

    # 2. Buscar en Pexels
    if PEXELS_API_KEY:
        print(f"[B-Roll] Buscando en Pexels: '{query}'...")
        pexels_vids = search_pexels_videos(query, per_page=10)
        for v in pexels_vids:
            files = v.get("video_files", [])
            # Priorizar HD portrait
            files.sort(key=lambda f: (1 if f.get("height", 0) >= f.get("width", 0) else 0, f.get("height", 0)), reverse=True)
            for f in files:
                url = f.get("link")
                if url:
                    downloaded = download_and_cache_video(url, f"pexels_{query}")
                    if downloaded:
                        return downloaded

    # 3. Buscar en Pixabay como alternativa
    if PIXABAY_API_KEY:
        print(f"[B-Roll] Buscando en Pixabay: '{query}'...")
        pixabay_hits = search_pixabay_videos(query, per_page=10)
        for hit in pixabay_hits:
            v_dict = hit.get("videos", {})
            for sz in ["large", "medium"]:
                if sz in v_dict and v_dict[sz].get("url"):
                    downloaded = download_and_cache_video(v_dict[sz]["url"], f"pixabay_{query}")
                    if downloaded:
                        return downloaded

    # 4. Respaldo en biblioteca existente
    return get_cached_or_local_clip(query)


def get_broll_status() -> Dict:
    """Devuelve el estado del motor B-Roll para la API y la interfaz."""
    cached_count = len([f for f in os.listdir(CACHE_DIR) if f.endswith(".mp4")]) if os.path.exists(CACHE_DIR) else 0
    local_count = len([f for f in os.listdir(LOCAL_VIDEOS_DIR) if f.endswith((".mp4", ".mov"))]) if os.path.exists(LOCAL_VIDEOS_DIR) else 0

    return {
        "available": bool(PEXELS_API_KEY or PIXABAY_API_KEY or cached_count > 0 or local_count > 0),
        "pexels_configured": bool(PEXELS_API_KEY),
        "pixabay_configured": bool(PIXABAY_API_KEY),
        "cached_clips": cached_count,
        "local_library_clips": local_count
    }
