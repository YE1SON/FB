"""Regression tests for story-first Christian Reels and voice-scene alignment."""
import os
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from fastapi.testclient import TestClient
from engine.history import ScriptHistoryManager
from engine.scripts import VIRAL_THEMES, generate_script, generate_3scene_prompts_for_script
from engine.scene_timing import compute_scene_breaks
from engine.tts import VOICES
import server

class AudienceStorytellingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.history = ScriptHistoryManager(os.path.join(self.temp.name, "history.json"))
        patcher = patch("engine.scripts.get_history_manager", return_value=self.history)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.client = TestClient(server.app)

    def test_all_themes_all_formats_have_coherent_faith_visuals(self):
        for theme in VIRAL_THEMES:
            for style in ("prayer", "reflection", "story", "comfort"):
                with self.subTest(theme=theme, style=style):
                    item = generate_script(theme, narration_type=style)
                    self.assertTrue(item["hook"])
                    self.assertTrue(item["body"])
                    self.assertEqual(item["narration_type"], style)
                    for scene in (1, 2, 3):
                        prompt = item[f"scene_{scene}_prompt"]
                        self.assertIn("Jesus Christ", prompt)
                        self.assertIn("no text", prompt)
                        self.assertIn("SAME protagonist", prompt) if scene != 1 else None

    def test_many_regenerations_do_not_duplicate_previous_full_script(self):
        scripts = [generate_script("lost_child", narration_type="prayer")["full_text"]
                   for _ in range(15)]
        self.assertGreaterEqual(len(set(scripts)), 10)

    def test_micro_mode_stays_brief_across_randomized_regenerations(self):
        for key in ("night_anxiety", "lost_child", "medical_fear", "zero_balance"):
            for _ in range(8):
                micro = generate_script(key, mode="micro")
                standard = generate_script(key, mode="deep")
                self.assertLessEqual(micro["word_count"], standard["word_count"])
                self.assertTrue(micro["cta"])
                self.assertTrue(micro["body"].endswith((".", "!", "?")))

    def test_custom_topic_affects_actual_image_story(self):
        data = generate_3scene_prompts_for_script(
            "divine_grace",
            "A parent is waiting. Jesus comforts the heart. A quiet moment of hope.",
            "I worry about my daughter",
            narration_type="comfort",
            hook="A parent is waiting.",
            body="Jesus comforts the heart. A quiet moment of hope.",
            cta="Share this Reel."
        )
        self.assertIn("parent worried about an adult child", data["scene_1_prompt"])
        self.assertIn("Holy Bible", data["scene_2_prompt"])
        self.assertNotIn("Share this Reel.", data["scene_3_prompt"])
        self.assertIn("quiet moment of hope", data["scene_3_prompt"].lower())

    def test_story_must_not_manufacture_false_testimony(self):
        samples = [generate_script("lost_child", narration_type="story")["body"] for _ in range(12)]
        self.assertFalse(any("A wanderer once said" in x for x in samples))

    def test_voice_selection_and_api_are_three(self):
        self.assertEqual(set(VOICES), {"guy", "christopher", "brian"})
        resp = self.client.get("/api/voices")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual({v["key"] for v in resp.json()}, set(VOICES))

    def test_api_respects_narration_and_cta_choice(self):
        resp = self.client.post("/api/generate-script", json={
            "theme_key":"medical_fear", "narration_type":"story",
            "include_cta":False, "mode":"deep"
        })
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["narration_type"], "story")
        self.assertEqual(data["cta"], "")
        self.assertNotIn("Type Amen", data["full_text"])

    def test_voice_boundaries_follow_audio_not_fixed_percentages(self):
        cues = [
            SimpleNamespace(text="A parent waits tonight.", end_sec=3.8),
            SimpleNamespace(text="Lord Jesus protect my daughter.", end_sec=9.5),
            SimpleNamespace(text="Give her hope and quiet courage.", end_sec=15.1),
            SimpleNamespace(text="Save this prayer for later.", end_sec=20.1),
        ]
        first, second = compute_scene_breaks(
            "A parent waits tonight.",
            "Lord Jesus protect my daughter. Give her hope and quiet courage.",
            "Save this prayer for later.", 20.1, cues=cues
        )
        self.assertGreaterEqual(first, 2.6)
        self.assertLess(first, second)
        self.assertLess(second, 20.1)
        self.assertAlmostEqual(first, 3.8, delta=1.0)

    def test_video_filter_accepts_speech_scene_boundaries(self):
        from engine.video import build_3scene_video_filter
        filtergraph, first, second = build_3scene_video_filter(
            inputs=["a.jpg","b.jpg","c.jpg"], w=1080, h=1920,
            effect_type="none", norm_ass="sub.ass", duration=22,
            scene_breaks=(4.4, 15.2)
        )
        self.assertIn("xfade", filtergraph)
        self.assertAlmostEqual(first, 4.05, places=2)
        self.assertAlmostEqual(second, 14.7, places=2)

if __name__ == "__main__":
    unittest.main()
