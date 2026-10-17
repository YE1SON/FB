import sys
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from fastapi.testclient import TestClient
from server import app

client = TestClient(app)

def test_endpoints():
    print("\n--- TESTING FASTAPI ENDPOINTS ---")
    
    # 1. Health
    r = client.get("/health")
    assert r.status_code == 200, f"/health status {r.status_code}"
    print(f" [PASS] /health: {r.json()}")

    # 2. Themes
    r = client.get("/api/themes")
    assert r.status_code == 200
    themes = r.json()
    assert len(themes) == 26
    print(f" [PASS] /api/themes: {len(themes)} themes returned")

    # 3. Voices
    r = client.get("/api/voices")
    assert r.status_code == 200
    voices = r.json()
    print(f" [PASS] /api/voices: {len(voices)} available voices returned ({', '.join([v['key'] for v in voices[:4]])}...)")

    # 4. B-Roll Status
    r = client.get("/api/broll-status")
    assert r.status_code == 200
    print(f" [PASS] /api/broll-status: {r.json()}")

    # 5. TTS Status
    r = client.get("/api/tts-status")
    assert r.status_code == 200
    print(f" [PASS] /api/tts-status: {r.json()}")

    # 6. Subtitle Styles
    r = client.get("/api/subtitle-styles")
    assert r.status_code == 200
    styles = r.json()
    print(f" [PASS] /api/subtitle-styles: {[s['key'] for s in styles]}")
    assert set([s['key'] for s in styles]) == {"karaoke", "pop", "cinematic", "clean"}

    # 7. Daily Batch
    r = client.get("/api/daily-batch")
    assert r.status_code == 200
    batch = r.json()
    assert len(batch) == 3
    print(f" [PASS] /api/daily-batch: 3 daily slots returned ({[b['slot'] for b in batch]})")

    # 8. Script Generation Endpoint
    r = client.post("/api/generate-script", json={"theme_key": "morning_favor", "mode": "deep"})
    assert r.status_code == 200
    data = r.json()
    assert "hook" in data and "body" in data and "cta" in data
    print(f" [PASS] /api/generate-script: hook='{data['hook'][:40]}...'")

    print("\nALL FASTAPI ENDPOINTS VERIFIED SUCCESSFULLY!\n")

if __name__ == "__main__":
    test_endpoints()
