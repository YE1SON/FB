"""Offline regression coverage for the local devotional editorial pipeline."""
import os
import tempfile
import unittest
from unittest.mock import patch
from engine.history import ScriptHistoryManager
from engine.scripts import generate_script, generate_3scene_prompts_for_script, VIRAL_THEMES
from engine.tts import VOICES
from engine.narrative_composer import CONTEXTUAL_CTAS, NARRATION_TYPES

class LocalEditorialEngineTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.history = ScriptHistoryManager(os.path.join(self.temp.name, "history.json"))
        patcher = patch("engine.scripts.get_history_manager", return_value=self.history)
        patcher.start()
        self.addCleanup(patcher.stop)

    def test_all_four_narrations_and_twenty_six_themes(self):
        self.assertEqual(len(VIRAL_THEMES), 26)
        self.assertEqual(set(CONTEXTUAL_CTAS), set(VIRAL_THEMES))
        for style in NARRATION_TYPES:
            result = generate_script("lost_child", mode="deep", narration_type=style)
            self.assertEqual(result["narration_type"], style)
            self.assertTrue(result["hook"] and result["body"])
            self.assertIn("Jesus Christ", result["scene_1_prompt"])
            self.assertIn("Jesus Christ", result["scene_2_prompt"])
            self.assertIn("Jesus Christ", result["scene_3_prompt"])

    def test_no_generic_engagement_bait(self):
        for key in VIRAL_THEMES:
            result = generate_script(key, narration_type="prayer")
            self.assertIn(result["cta"], CONTEXTUAL_CTAS[key])
            self.assertNotIn("Type Amen", result["cta"])
            self.assertNotIn("Leave your first name", result["cta"])

    def test_user_can_disable_cta(self):
        result = generate_script("lost_child", brief={"include_cta": False})
        self.assertEqual(result["cta"], "")

    def test_image_prompt_uses_selected_narration_and_excludes_cta(self):
        p = generate_3scene_prompts_for_script(
            "lost_child", script_text="A mother waits. She prays tonight. Share this reel.",
            hook="A mother waits.", body="She prays tonight.",
            cta="Share this reel.", narration_type="reflection"
        )
        self.assertIn("A mother waits.", p["scene_1_prompt"])
        self.assertIn("She prays tonight.", p["scene_2_prompt"])
        self.assertNotIn("Share this reel", p["scene_3_prompt"])
        self.assertIn("Holy Bible", p["scene_2_prompt"])

    def test_three_and_only_three_voices(self):
        self.assertEqual(set(VOICES), {"guy","christopher","brian"})
        self.assertTrue(all(v["engine"] == "edge" for v in VOICES.values()))

    def test_recent_scripts_rotate(self):
        hooks = [generate_script("night_anxiety")["hook"] for _ in range(4)]
        self.assertGreater(len(set(hooks)), 1)

if __name__ == "__main__":
    unittest.main()
