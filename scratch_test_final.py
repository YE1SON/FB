import sys
sys.stdout.reconfigure(encoding='utf-8')
import requests
import threading
import time
import uvicorn
from server import app

server = threading.Thread(
    target=uvicorn.run,
    args=(app,),
    kwargs={"host": "127.0.0.1", "port": 7897, "log_level": "warning"},
    daemon=True
)
server.start()
time.sleep(2)

base = "http://127.0.0.1:7897"

# 1. Test worship-tracks endpoint
r_tracks = requests.get(base + "/studio/api/worship-tracks")
print("Worship tracks status:", r_tracks.status_code)
tracks = r_tracks.json()
print("Tracks count:", len(tracks))
for t in tracks:
    print(" ", t["key"], "->", t["name"])

# 2. Test generate-script endpoint with seo_caption
r_script = requests.post(base + "/studio/api/generate-script", json={"theme_key": "silent_battles"})
script_data = r_script.json()
print("\nGenerated Script:")
print("  Hook:", script_data["hook"])
print("  Body:", script_data["body"])
print("  CTA:", script_data["cta"])
print("  Word count:", len(script_data["full_text"].split()))
print("\nSEO Caption for Facebook:\n" + script_data["seo_caption"])

# 3. Test video rendering with worship music
print("\nTesting full video render with worship music...")
r_render = requests.post(
    base + "/studio/api/render-video",
    json={
        "hook": script_data["hook"],
        "body": script_data["body"],
        "cta": script_data["cta"],
        "voice_key": "christopher",
        "rate": "+0%",
        "image_name": "jesus_healing_miracle.jpg",
        "subtitle_style": "gold_highlight",
        "subtitle_size": "normal",
        "music_track": "worship_piano_peace"
    },
    timeout=90
)
assert r_render.status_code == 200, f"Render failed: {r_render.text}"
print("Rendered video with BGM:", r_render.json()["video_url"])
print("\n*** ALL TESTS PASSED WITH 100% SUCCESS! ***")
