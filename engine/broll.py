"""
B-Roll Video Engine — Downloads real video clips from Pexels API
to replace static images and pass Facebook's Motion Score classifier.
"""
import os
import random
import requests
from typing import Optional, List, Dict

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "broll_cache")

# Thematic search queries for each content theme — portrait-friendly nature/faith visuals
THEME_BROLL_QUERIES = {
    "silent_battles": [
        "rain drops window peaceful",
        "candle flame darkness calm",
        "sunset clouds dramatic sky",
        "ocean waves calm shore",
        "person walking alone nature"
    ],
    "financial_breakthrough": [
        "sunrise golden light clouds",
        "wheat field golden hour wind",
        "light rays through clouds",
        "river flowing peaceful morning",
        "sunflower field sunshine"
    ],
    "bedtime_blessing": [
        "night sky stars peaceful",
        "candle flame cozy evening",
        "moonlight clouds timelapse",
        "calm lake night reflection",
        "fireplace warm flame"
    ],
    "family_healing": [
        "sunset warm golden nature",
        "tree sunlight forest peaceful",
        "flowers garden morning dew",
        "birds flying sunset freedom",
        "warm light window morning"
    ],
    "divine_protection": [
        "storm clouds dramatic lightning",
        "lighthouse ocean waves power",
        "sunrise mountain peak glory",
        "sunlight breaking dark clouds",
        "eagle soaring sky majestic"
    ],
    "miracle_healing": [
        "sunlight through forest trees",
        "water stream nature peaceful",
        "flower blooming close up",
        "morning dew grass nature",
        "dove bird flying sky"
    ]
}

UNIVERSAL_QUERIES = [
    "sunset sky clouds cinematic",
    "peaceful nature light water",
    "candle flame peaceful calm",
    "sunlight rays clouds heaven",
    "ocean waves sunset peaceful"
]


def ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    os.makedirs(CACHE_DIR, exist_ok=True)


def search_pexels_videos(
    query: str,
    orientation: str = "portrait",
    per_page: int = 10
) -> List[Dict]:
    """Search Pexels API for videos matching the query."""
    if not PEXELS_API_KEY:
        return []

    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query,
        "orientation": orientation,
        "per_page": per_page,
        "size": "medium"
    }

    try:
        resp = requests.get(url, headers=headers, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("videos", [])
    except Exception as e:
        print(f"[B-Roll] Pexels API error: {e}")
        return []


def get_best_video_file(video_data: Dict, max_width: int = 1920) -> Optional[str]:
    """Extract the best HD video file URL from Pexels response data.
    Prefers portrait-oriented files with good resolution."""
    files = video_data.get("video_files", [])
    if not files:
        return None

    # Prefer portrait files (height > width)
    portrait = [f for f in files if f.get("height", 0) > f.get("width", 0)]
    candidates = portrait if portrait else files

    # Filter to reasonable resolution (not too huge for fast download)
    suitable = [f for f in candidates if f.get("width", 0) <= max_width]
    if not suitable:
        suitable = candidates

    # Sort by height descending — pick highest quality
    suitable.sort(key=lambda f: f.get("height", 0), reverse=True)

    return suitable[0].get("link") if suitable else None


def download_video(url: str, output_path: str) -> str:
    """Download a video file from URL to local path."""
    resp = requests.get(url, stream=True, timeout=90)
    resp.raise_for_status()

    with open(output_path, "wb") as f:
        for chunk in resp.iter_content(chunk_size=16384):
            f.write(chunk)

    return output_path


def get_broll_clip(theme_key: str) -> Optional[str]:
    """
    Get a B-roll video clip for the given theme.
    Searches Pexels API, downloads, and caches locally.
    Returns the path to the video file, or None if unavailable.
    """
    ensure_cache_dir()

    if not PEXELS_API_KEY:
        print("[B-Roll] No PEXELS_API_KEY set. Cannot download B-roll video.")
        return None

    # Choose a random query for variety across renders
    queries = THEME_BROLL_QUERIES.get(theme_key, UNIVERSAL_QUERIES)
    query = random.choice(queries)
    cache_key = query.replace(" ", "_")[:50]

    # Check cache — reuse if we already downloaded a clip for this query
    if os.path.exists(CACHE_DIR):
        cached = [f for f in os.listdir(CACHE_DIR) if f.startswith(cache_key) and f.endswith(".mp4")]
        if cached:
            chosen = os.path.join(CACHE_DIR, random.choice(cached))
            print(f"[B-Roll] Using cached clip: {chosen}")
            return chosen

    # Search Pexels
    print(f"[B-Roll] Searching Pexels for: '{query}' ...")
    videos = search_pexels_videos(query, orientation="portrait", per_page=10)

    # Fallback to universal queries if theme search fails
    if not videos:
        fallback_query = random.choice(UNIVERSAL_QUERIES)
        print(f"[B-Roll] Theme search empty, trying fallback: '{fallback_query}'")
        videos = search_pexels_videos(fallback_query, orientation="portrait", per_page=10)

    if not videos:
        print("[B-Roll] No videos found on Pexels.")
        return None

    # Pick from top results randomly for visual variety
    video = random.choice(videos[:min(5, len(videos))])
    video_url = get_best_video_file(video)

    if not video_url:
        print("[B-Roll] No suitable video file in Pexels response.")
        return None

    # Download the clip
    video_id = video.get("id", random.randint(10000, 99999))
    output_path = os.path.join(CACHE_DIR, f"{cache_key}_{video_id}.mp4")

    print(f"[B-Roll] Downloading Pexels clip #{video_id}...")
    try:
        download_video(video_url, output_path)
        size_mb = os.path.getsize(output_path) / (1024 * 1024)
        print(f"[B-Roll] Downloaded: {output_path} ({size_mb:.1f} MB)")
        return output_path
    except Exception as e:
        print(f"[B-Roll] Download failed: {e}")
        if os.path.exists(output_path):
            os.remove(output_path)
        return None


def get_broll_status() -> Dict:
    """Return status of the B-Roll system for API/frontend."""
    cached_count = 0
    if os.path.exists(CACHE_DIR):
        cached_count = len([f for f in os.listdir(CACHE_DIR) if f.endswith(".mp4")])

    return {
        "available": bool(PEXELS_API_KEY),
        "api_configured": bool(PEXELS_API_KEY),
        "cached_clips": cached_count
    }
