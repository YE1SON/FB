import os
import sys
import subprocess
import json
import asyncio
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.scripts import generate_script, get_themes_list, VIRAL_THEMES
from engine.tts import check_engine_availability, get_available_voices, synthesize_speech, VOICES
from engine.broll import get_broll_status, get_broll_clip
from engine.subtitles import generate_viral_ass, SUBTITLE_STYLES
from engine.video import render_reel, get_audio_duration
from engine.image_cards import create_prayer_card_4_5

OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
os.makedirs(OUTPUTS_DIR, exist_ok=True)

def run_ffprobe(video_path):
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,duration,r_frame_rate",
        "-of", "json",
        video_path
    ]
    res = subprocess.run(cmd, capture_output=True, text=True, check=True)
    return json.loads(res.stdout)

async def main():
    print("=================================================================")
    print("      JESUS REELS STUDIO v4.0 - PHASE 8 VERIFICATION SUITE       ")
    print("=================================================================")

    # 1. System availability
    print("\n--- TEST 1: System Availability & Engine Health ---")
    engines = check_engine_availability()
    print(f"TTS Engines: Kokoro={engines['kokoro']}, Edge-TTS={engines['edge_tts']}, Piper={engines['piper']}, Whisper={engines['faster_whisper']}")
    assert engines['edge_tts'] or engines['kokoro'], "Al menos un motor TTS debe estar disponible"
    assert engines['faster_whisper'], "Faster-Whisper debe estar disponible"
    print(" [PASS] TTS and Alignment Engines Verified.")

    # 2. B-Roll Status
    print("\n--- TEST 2: B-Roll Engine Status ---")
    broll_st = get_broll_status()
    print(f"B-Roll: {broll_st}")
    assert "available" in broll_st
    print(" [PASS] B-Roll status endpoint verified.")

    # 3. Themes List (26 themes)
    print("\n--- TEST 3: Script Engine Themes (26 Categories) ---")
    themes = get_themes_list()
    print(f"Total themes loaded: {len(themes)}")
    assert len(themes) == 26, f"Expected 26 themes, got {len(themes)}"
    print(" [PASS] Exactly 26 themes verified.")

    # 4. Script generation across modes
    print("\n--- TEST 4: Script Modes (micro, deep, story) ---")
    for mode in ["micro", "deep", "story"]:
        s = generate_script("morning_favor", mode=mode)
        full_text = f"{s['hook']} {s['body']} {s['cta']}"
        w_count = len(full_text.split())
        print(f" Mode {mode:5s}: words={w_count:2d}, hook={s['hook'][:35]}...")
        assert len(s["hook"]) > 0 and len(s["body"]) > 0 and len(s["cta"]) > 0
    print(" [PASS] All script modes generated successfully.")

    # 5. Audio Synthesis & Subtitle Alignment (Kokoro or Edge)
    print("\n--- TEST 5: TTS Speech Synthesis + Subtitle Millisecond Cues ---")
    test_text = "The Lord is your keeper today. He will preserve your soul from all evil, and give you quiet rest tonight."
    audio_test = os.path.join(OUTPUTS_DIR, "phase8_test_audio.mp3")

    v_key = "christopher"
    t0 = time.time()
    cues = await synthesize_speech(test_text, VOICES[v_key]["id"], audio_test, rate="+0%")
    dur = time.time() - t0
    audio_dur = get_audio_duration(audio_test)
    print(f" Synthesized with voice '{v_key}' in {dur:.2f}s. Audio length: {audio_dur:.2f}s, Cues count: {len(cues)}")
    assert os.path.exists(audio_test) and os.path.getsize(audio_test) > 5000
    assert len(cues) >= 10, "Faster-Whisper debe retornar al menos 10 cues"
    print(f" First cue: start={cues[0].start_sec:.2f}s, end={cues[0].end_sec:.2f}s, text='{cues[0].text}'")
    assert cues[0].start_sec < 0.8, f"Initial silence removal should put start < 0.8s, got {cues[0].start_sec}"
    print(" [PASS] TTS audio and millisecond cues verified.")

    # 6. Test all 4 ASS Subtitle Styles
    print("\n--- TEST 6: Subtitle Styles (.ass generation) ---")
    for style_key in ["karaoke", "pop", "cinematic", "clean"]:
        ass_path = os.path.join(OUTPUTS_DIR, f"phase8_test_{style_key}.ass")
        generate_viral_ass(cues, ass_path, style_key=style_key, play_res_x=1080, play_res_y=1920)
        assert os.path.exists(ass_path)
        with open(ass_path, "r", encoding="utf-8") as f:
            content = f.read()
        assert "Style: MainSub" in content
        assert "Dialogue:" in content
        print(f" Style '{style_key:9s}': .ass generated ({len(content)} bytes).")
    print(" [PASS] All 4 subtitle styles generated correctly.")

    # 7. Video Rendering - Karaoke Style (1080x1920 Vertical Reel)
    print("\n--- TEST 7: Full Video Render - Karaoke (1080x1920 Vertical) ---")
    img1 = os.path.join(ASSETS_DIR, "jesus_holy_bible.jpg")
    img2 = os.path.join(ASSETS_DIR, "jesus_praying_gethsemane.jpg")
    img3 = os.path.join(ASSETS_DIR, "jesus_reaching_hand.jpg")
    karaoke_ass = os.path.join(OUTPUTS_DIR, "phase8_test_karaoke.ass")
    out_karaoke = os.path.join(OUTPUTS_DIR, "phase8_reel_karaoke.mp4")

    t0 = time.time()
    render_reel(
        image_path=img1,
        audio_path=audio_test,
        ass_path=karaoke_ass,
        output_mp4_path=out_karaoke,
        aspect_ratio="9:16",
        effect_type="cinematic_dust",
        camera_motion="zoom_in",
        image_path_2=img2,
        image_path_3=img3,
        transition_style="fade"
    )
    render_dur = time.time() - t0
    print(f" Rendered in {render_dur:.2f}s -> {out_karaoke}")
    info = run_ffprobe(out_karaoke)
    st = info["streams"][0]
    w, h = int(st["width"]), int(st["height"])
    print(f" ffprobe probe: Resolution={w}x{h}, Duration={st.get('duration')}s")
    assert w == 1080 and h == 1920, f"Expected 1080x1920, got {w}x{h}"
    print(" [PASS] Karaoke Vertical Reel 1080x1920 verified.")

    # 8. Video Rendering - Pop Style with Divine Light
    print("\n--- TEST 8: Full Video Render - Pop Style (Divine Light FX) ---")
    pop_ass = os.path.join(OUTPUTS_DIR, "phase8_test_pop.ass")
    out_pop = os.path.join(OUTPUTS_DIR, "phase8_reel_pop.mp4")
    t0 = time.time()
    render_reel(
        image_path=img1,
        audio_path=audio_test,
        ass_path=pop_ass,
        output_mp4_path=out_pop,
        aspect_ratio="9:16",
        effect_type="divine_light",
        camera_motion="pan_up",
        image_path_2=img2,
        image_path_3=img3,
        transition_style="dissolve"
    )
    print(f" Rendered Pop Reel in {time.time()-t0:.2f}s -> {out_pop}")
    info_pop = run_ffprobe(out_pop)
    st_pop = info_pop["streams"][0]
    assert int(st_pop["width"]) == 1080 and int(st_pop["height"]) == 1920
    print(" [PASS] Pop Style Vertical Reel verified.")

    # 9. Video Rendering - Cinematic Style with Holy Fire
    print("\n--- TEST 9: Full Video Render - Cinematic Style (Holy Fire FX) ---")
    cin_ass = os.path.join(OUTPUTS_DIR, "phase8_test_cinematic.ass")
    out_cin = os.path.join(OUTPUTS_DIR, "phase8_reel_cinematic.mp4")
    t0 = time.time()
    render_reel(
        image_path=img1,
        audio_path=audio_test,
        ass_path=cin_ass,
        output_mp4_path=out_cin,
        aspect_ratio="9:16",
        effect_type="holy_fire",
        camera_motion="zoom_in_pan_up",
        image_path_2=img2,
        image_path_3=img3,
        transition_style="fadewhite"
    )
    print(f" Rendered Cinematic Reel in {time.time()-t0:.2f}s -> {out_cin}")
    info_cin = run_ffprobe(out_cin)
    st_cin = info_cin["streams"][0]
    assert int(st_cin["width"]) == 1080 and int(st_cin["height"]) == 1920
    print(" [PASS] Cinematic Style Vertical Reel verified.")

    # 10. Image Card 4:5 Feed Post
    print("\n--- TEST 10: Prayer Card 4:5 Feed Post ---")
    out_card = os.path.join(OUTPUTS_DIR, "phase8_card_test.jpg")
    create_prayer_card_4_5(
        background_image_path=img1,
        title="MORNING FAVOR AND PEACE",
        prayer_text="May the Lord lift up His countenance upon you and give you peace throughout this day.",
        verse_footer="Numbers 6:24-26",
        watermark_text="@JesusDailyFaith",
        output_path=out_card
    )
    assert os.path.exists(out_card)
    card_probe = run_ffprobe(out_card)
    c_st = card_probe["streams"][0]
    cw, ch = int(c_st["width"]), int(c_st["height"])
    print(f" Card output: {cw}x{ch} (Expected 1080x1350 for 4:5)")
    assert cw == 1080 and ch == 1350
    print(" [PASS] 4:5 Feed Prayer Card verified.")

    print("\n=================================================================")
    print("       ALL 10 PHASE 8 VERIFICATION TESTS PASSED SUCCESSFULLY!    ")
    print("=================================================================\n")

if __name__ == "__main__":
    asyncio.run(main())
