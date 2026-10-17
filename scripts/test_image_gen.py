import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.image_gen import (
    load_keys, save_keys, get_providers_status,
    enhance_flux_prompt, generate_ai_scene_image
)

def test_image_engine():
    print("\n--- TEST: Image Generation Engine (Cloudflare & Hugging Face) ---")
    
    # 1. Provider status
    st = get_providers_status()
    print(" Providers Status:", st)
    assert "cloudflare" in st and "huggingface" in st
    print(" [PASS] get_providers_status verified.")

    # 2. Prompt enhancement for FLUX
    raw_p = "Jesus healing a sick child, octane render, 8k, masterpiece"
    enhanced = enhance_flux_prompt(raw_p)
    print(" Original prompt:", raw_p)
    print(" Enhanced prompt:", enhanced)
    assert "octane render" not in enhanced and "8k" not in enhanced
    assert "photograph" in enhanced.lower()
    print(" [PASS] enhance_flux_prompt verified.")

    # 3. Test generate_ai_scene_image with local fallback (when no external keys)
    img_res = generate_ai_scene_image("Jesus comforting someone who is crying", aspect_ratio="9:16", label="Test Scene")
    print(" Generation Result:", img_res)
    assert img_res["status"] == "success"
    assert os.path.exists(os.path.join(BASE_DIR, "assets", "images", img_res["filename"]))
    print(" [PASS] generate_ai_scene_image verified.")

    print("\nALL IMAGE GENERATION UNIT TESTS PASSED!\n")

if __name__ == "__main__":
    test_image_engine()
