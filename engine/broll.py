"""
B-Roll Video Engine — Downloads real video clips from Pixabay API
to replace static images and pass Facebook's Motion Score classifier.
"""
import os
import random
import requests
from typing import Optional, List, Dict
import urllib.parse

PIXABAY_API_KEY = os.environ.get("PIXABAY_API_KEY", "")
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE_DIR = os.path.join(BASE_DIR, "broll_cache")

# Thematic search queries for each content theme — portrait-friendly nature/faith visuals
THEME_BROLL_QUERIES = {
    "silent_battles": [
        "rain window",
        "candle dark",
        "ocean calm",
        "sad lonely",
        "sunset clouds"
    ],
    "financial_breakthrough": [
        "sunrise light",
        "wheat field",
        "river morning",
        "sunflower",
        "open door"
    ],
    "bedtime_blessing": [
        "night sky",
        "moon clouds",
        "calm lake",
        "fireplace",
        "sleeping peaceful"
    ],
    "family_healing": [
        "sunset nature",
        "forest light",
        "flowers field",
        "birds flying",
        "family silhouette"
    ],
    "divine_protection": [
        "storm lightning",
        "lighthouse ocean",
        "mountain peak",
        "eagle soaring",
        "shield light"
    ],
    "miracle_healing": [
        "sunlight trees",
        "water stream",
        "flower blooming",
        "morning dew",
        "dove bird"
    ]
}

UNIVERSAL_QUERIES = [
    "sunset sky",
    "peaceful nature",
    "candle flame",
    "sunlight rays",
    "ocean waves"
]


def ensure_cache_dir():
    """Create cache directory if it doesn't exist."""
    os.makedirs(CACHE_DIR, exist_ok=True)


def search_pixabay_videos(query: str, per_page: int = 15) -> List[Dict]:
    """Search Pixabay API for videos matching the query."""
    if not PIXABAY_API_KEY:
        return []

    url = "https://pixabay.com/api/videos/"
    # Encode the query properly
    encoded_query = urllib.parse.quote(query)
    
    params = {
        "key": PIXABAY_API_KEY,
        "q": encoded_query,
        "video_type": "all",
        "safesearch": "true",
        "per_page": per_page
    }

    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        return data.get("hits", [])
    except Exception as e:
        print(f"[B-Roll] Pixabay API error: {e}")
        return []


def get_best_video_file(video_data: Dict, max_width: int = 1920) -> Optional[str]:
    """Extract the best video file URL from Pixabay response data.
    Tries to find portrait or high-quality landscape videos."""
    videos_obj = video_data.get("videos", {})
    if not videos_obj:
        return None

    # Pixabay usually provides sizes like: large, medium, small, tiny
    # We prefer 'large' or 'medium'
    candidates = []
    for size_key in ["large", "medium", "small"]:
        if size_key in videos_obj and videos_obj[size_key].get("url"):
            candidates.append(videos_obj[size_key])

    if not candidates:
        return None

    # Filter by width constraint
    suitable = [f for f in candidates if f.get("width", 9999) <= max_width]
    if not suitable:
        suitable = candidates

    # Pick the highest quality one available
    suitable.sort(key=lambda f: f.get("height", 0), reverse=True)
    return suitable[0].get("url")


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
    Searches Pixabay API, downloads, and caches locally.
    Returns the path to the video file, or None if unavailable.
    """
    ensure_cache_dir()

    if not PIXABAY_API_KEY:
        print("[B-Roll] No PIXABAY_API_KEY set. Cannot download B-roll video.")
        return None

    # Choose a random query for variety across renders
    queries = THEME_BROLL_QUERIES.get(theme_key, UNIVERSAL_QUERIES)
    query = random.choice(queries)
    cache_key = query.replace(" ", "_")[:30]

    # Check cache — reuse if we already downloaded a clip for this query
    if os.path.exists(CACHE_DIR):
        cached = [f for f in os.listdir(CACHE_DIR) if f.startswith(cache_key) and f.endswith(".mp4")]
        if cached:
            chosen = os.path.join(CACHE_DIR, random.choice(cached))
            print(f"[B-Roll] Using cached clip: {chosen}")
            return chosen

    # Search Pixabay
    print(f"[B-Roll] Searching Pixabay for: '{query}' ...")
    videos = search_pixabay_videos(query, per_page=15)

    # Fallback to universal queries if theme search fails
    if not videos:
        fallback_query = random.choice(UNIVERSAL_QUERIES)
        print(f"[B-Roll] Theme search empty, trying fallback: '{fallback_query}'")
        videos = search_pixabay_videos(fallback_query, per_page=15)

    if not videos:
        print("[B-Roll] No videos found on Pixabay.")
        return None

    # Pick from top results randomly for visual variety
    video = random.choice(videos[:min(8, len(videos))])
    video_url = get_best_video_file(video)

    if not video_url:
        print("[B-Roll] No suitable video file in Pixabay response.")
        return None

    # Download the clip
    video_id = video.get("id", random.randint(10000, 99999))
    output_path = os.path.join(CACHE_DIR, f"{cache_key}_{video_id}.mp4")

    print(f"[B-Roll] Downloading Pixabay clip #{video_id}...")
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
        "available": bool(PIXABAY_API_KEY),
        "api_configured": bool(PIXABAY_API_KEY),
        "cached_clips": cached_count,
        "provider": "pixabay"
    }
