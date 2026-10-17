import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import engine.video as v

def main():
    img_path = os.path.join("assets", "images", "jesus_healing_miracle.jpg")
    audio_path = os.path.join("outputs", "test_adam.mp3")
    ass_path = os.path.join("outputs", "test_karaoke.ass")
    out_mp4 = os.path.join("outputs", "test_render_karaoke.mp4")

    print("Starting test render...")
    out = v.render_reel(
        image_path=img_path,
        audio_path=audio_path,
        ass_path=ass_path,
        output_mp4_path=out_mp4,
        aspect_ratio="9:16",
        effect_type="cinematic_dust",
        camera_motion="zoom_in",
        music_track="worship_piano_peace",
        music_volume=0.20
    )
    print(f"SUCCESS! Rendered video: {out}")

    cmd = ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height,duration", "-of", "json", out]
    p = subprocess.run(cmd, capture_output=True, text=True, check=True)
    info = json.loads(p.stdout)["streams"][0]
    print(f"Verified Dimensions: {info['width']}x{info['height']}, Duration: {info['duration']}s")
    assert info['width'] == 1080 and info['height'] == 1920, "Resolution must be exactly 1080x1920"
    print("ALL ASSERTIONS PASSED: 1080x1920 Vertical HD Verified!")

if __name__ == "__main__":
    main()
