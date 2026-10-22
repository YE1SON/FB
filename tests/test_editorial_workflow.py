"""Offline regression tests for editorial generation and manual result observations."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

os.environ["SCRIPT_PROVIDER"] = "template"

from fastapi.testclient import TestClient
from engine.editorial import SERIES, THEME_OPENINGS, clean_narration, review_script
from engine.history import ScriptHistoryManager
from engine.scripts import VIRAL_THEMES, generate_script, generate_3scene_prompts_for_script
import engine.results as results
import server


class EditorialWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.history = ScriptHistoryManager(os.path.join(self.temp.name, "history.json"))
        self.patches = [patch("engine.history.get_history_manager", return_value=self.history),
                        patch("engine.scripts.get_history_manager", return_value=self.history),
                        patch.object(results, "RESULTS_FILE", os.path.join(self.temp.name, "results.json"))]
        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)
        self.client = TestClient(server.app)

    def test_catalog_keeps_all_themes_and_distinct_formats(self):
        keys = [key for series in SERIES.values() for key in series["themes"]]
        self.assertCountEqual(keys, VIRAL_THEMES)
        self.assertEqual(set(THEME_OPENINGS), set(VIRAL_THEMES))
        for key in VIRAL_THEMES:
            scripts = [generate_script(key, brief={"format": fmt}) for fmt in ("prayer", "reflection", "story")]
            self.assertEqual(len({s["body"] for s in scripts}), 3, key)
            for script in scripts:
                self.assertEqual(script["cta"], "")
                self.assertEqual(len(script["hook_alternatives"]), 3)
                self.assertNotIn(VIRAL_THEMES[key]["title"], script["seo_caption"])
                self.assertFalse(script["full_text"].endswith("..."))
                self.assertIn(script["hook"], script["scene_1_prompt"])
            self.assertIn("Imagine", scripts[2]["body"])

    def test_user_situation_and_idea_survive_with_english_copy(self):
        situation = "Waiting for a call from your grown child."
        script = generate_script("lost_child", brief={"format": "reflection", "situation": situation,
                                                       "central_idea": "Listening can be an act of love"})
        self.assertIn(situation, script["hook_alternatives"])
        self.assertIn("Listening can be an act of love.", script["body"])
        self.assertIn(situation, script["scene_1_prompt"])

    def test_modes_have_different_lengths_and_openings_rotate(self):
        brief = {"format": "prayer"}
        micro = generate_script("family_protection", mode="micro", brief=brief)
        deep = generate_script("family_protection", mode="deep", brief=brief)
        extended = generate_script("family_protection", mode="story", brief=brief)
        self.assertLess(micro["word_count"], deep["word_count"])
        self.assertLess(deep["word_count"], extended["word_count"])
        self.assertEqual(len({s["hook"] for s in (micro, deep, extended)}), 3)

    def test_legacy_loop_bridges_removed_and_review_is_specific(self):
        clean = clean_narration("Rest in peace. Rest in peace. — And always remember that...")
        self.assertEqual(clean, "Rest in peace.")
        warnings = review_script("Una oración por tus hijos", "Peace today. Peace today.", "remember that...")["warnings"]
        self.assertGreaterEqual(len(warnings), 3)
        legacy = self.client.post("/api/generate-script", json={"theme_key": "morning_favor", "seamless_loop": True}).json()
        self.assertNotIn("always remember that", legacy["full_text"])

    def test_api_aliases_optional_cta_and_validation(self):
        for prefix in ("/api", "/studio/api"):
            self.assertEqual(self.client.get(prefix + "/themes").status_code, 200)
            self.assertEqual(self.client.get(prefix + "/editorial-config").status_code, 200)
            response = self.client.post(prefix + "/generate-script", json={"theme_key": "zero_balance", "brief": {"format": "prayer"}})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["cta"], "")
            self.assertEqual(self.client.post(prefix + "/editorial-review", json={"hook": "Another bill.", "body": "Lord, grant us wisdom."}).status_code, 200)
        self.assertEqual(server.RenderRequest(hook="A bill.", body="A prayer.").cta, "")
        self.assertEqual(self.client.post("/api/generate-script", json={"brief": {"target_duration_sec": -1}}).status_code, 422)

    def test_scenes_change_with_the_narrative(self):
        first = generate_3scene_prompts_for_script("lost_child", "The phone is quiet. A parent waits. Listen with patience.")
        second = generate_3scene_prompts_for_script("lost_child", "A letter arrives. A parent reads. Take time to answer.")
        self.assertNotEqual(first, second)
        self.assertIn("A parent waits.", first["scene_2_prompt"])

    def test_results_preserve_creative_and_unknown_values(self):
        payload = {"creative": {"theme_key": "lost_child", "hook": "The phone stays quiet."},
                   "checkpoint": "48h", "metrics": {"views": 0, "average_watch_sec": None}}
        created = self.client.post("/api/editorial-results", json=payload)
        self.assertEqual(created.status_code, 200)
        payload["record_id"] = created.json()["id"]
        payload["creative"]["hook"] = "An unrelated new draft."
        payload["checkpoint"] = "7d"
        payload["metrics"] = {"views": 200, "average_watch_sec": 4}
        self.assertEqual(self.client.post("/studio/api/editorial-results", json=payload).status_code, 200)
        record = self.client.get("/api/editorial-results").json()[0]
        self.assertEqual(record["creative"]["hook"], "The phone stays quiet.")
        self.assertEqual(len(record["observations"]), 2)
        self.assertIsNone(record["observations"][0]["metrics"]["average_watch_sec"])
        self.assertEqual(record["observations"][0]["metrics"]["views"], 0)
        self.assertEqual(self.client.get("/outputs/editorial_results.json").status_code, 404)
        payload["metrics"] = {"us_viewer_pct": 101}
        self.assertEqual(self.client.post("/api/editorial-results", json=payload).status_code, 422)
        payload["metrics"] = {}; payload["record_id"] = "missing"
        self.assertEqual(self.client.post("/api/editorial-results", json=payload).status_code, 404)


if __name__ == "__main__":
    unittest.main()
