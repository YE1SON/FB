"""
Unit and regression tests for FaithSpark Daily Redesign:
- AI Narrative Engine (Gemini / Groq / Local fallback)
- 3 Hook alternatives generation
- 26 Themes with specific human focus options
- Single Image Reel FFmpeg filter and video rendering
- Visual style analysis (auto, jesus, family, bible, cross, landscape)
"""

import os
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

from engine.scripts import VIRAL_THEMES, THEME_FOCUS_OPTIONS, get_themes_list, generate_script
from engine.ai_narrative import generate_ai_narrative_script, call_gemini_api, call_groq_api
from engine.narrative_prompts import generate_single_image_prompt
from engine.video import build_single_image_video_filter
import server

class FaithSparkRedesignTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(server.app)

    def test_all_26_themes_have_at_least_4_focus_options_in_spanish(self):
        """Verifica que los 26 pilares temáticos tengan al menos 4 enfoques específicos redactados en español."""
        self.assertEqual(len(VIRAL_THEMES), 26)
        spanish_indicators = ["de", "en", "el", "la", "un", "una", "y", "que", "para", "con", "por", "dios", "oración"]
        for theme_key in VIRAL_THEMES:
            focus_opts = THEME_FOCUS_OPTIONS.get(theme_key, [])
            self.assertGreaterEqual(
                len(focus_opts), 4,
                f"El tema {theme_key} debe tener al menos 4 enfoques específicos"
            )
            # Verificar que las opciones contengan texto en español
            combined = " ".join(focus_opts).lower()
            has_spanish = any(f" {w} " in f" {combined} " for w in spanish_indicators)
            self.assertTrue(
                has_spanish,
                f"Las opciones de enfoque para '{theme_key}' deben estar en español: {focus_opts[0]}"
            )

    def test_test_narrative_key_endpoint_validation(self):
        """Verifica que /api/test-narrative-key valide la presencia de clave."""
        resp = self.client.post("/api/test-narrative-key", json={"provider": "gemini", "api_key": ""})
        self.assertEqual(resp.status_code, 400)

    def test_themes_list_endpoint_includes_focus_options(self):
        """Verifica que /api/themes retorne los 26 temas con sus listas de enfoques."""
        resp = self.client.get("/api/themes")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data), 26)
        for t in data:
            self.assertIn("key", t)
            self.assertIn("focus_options", t)
            self.assertGreaterEqual(len(t["focus_options"]), 4)

    def test_single_image_prompt_generator_visual_styles(self):
        """Verifica la generación de prompts para 1 sola imagen con diferentes estilos visuales."""
        styles = ["jesus", "family", "bible", "cross", "landscape", "auto"]
        for st in styles:
            p = generate_single_image_prompt(
                theme_key="night_anxiety",
                script_text="Lord, bring peace to my heart tonight.",
                visual_style=st
            )
            self.assertIn("vertical 9:16", p)
            self.assertIn("strictly no text", p)
            self.assertIn("photorealistic", p)

    def test_ai_narrative_fallback_to_local_engine(self):
        """Verifica que si no hay claves API o fallan, el motor local genera el guion limpiamente."""
        res = generate_ai_narrative_script(
            theme_key="morning_favor",
            specific_focus="Opening your eyes with quiet gratitude before reaching for the phone",
            narration_type="prayer",
            mode="deep",
            include_cta=True,
            engine_provider="gemini",
            gemini_api_key=None,
            groq_api_key=None
        )
        self.assertTrue(res["hook"])
        self.assertTrue(res["body"])
        self.assertTrue(res["cta"])
        self.assertEqual(len(res["hook_options"]), 3)
        self.assertIn("Motor Local", res["provider_used"])
        self.assertIn("image_prompt", res)
        self.assertIn("strictly no text", res["image_prompt"])

    def test_build_single_image_video_filter_generates_valid_filtergraph(self):
        """Verifica que build_single_image_video_filter produzca un filter_complex de FFmpeg continuo."""
        filt = build_single_image_video_filter(
            input_path="assets/images/sample.jpg",
            w=1080,
            h=1920,
            effect_type="living_gold",
            norm_ass="C\\:/test/subtitles.ass",
            duration=20.0,
            camera_motion="zoom_in",
            fps=30
        )
        self.assertIn("zoompan=", filt)
        self.assertIn("ass='C\\:/test/subtitles.ass'", filt)
        self.assertIn("[motion]", filt)
        self.assertIn("[v]", filt)
        self.assertIn("vignette=", filt)

    def test_api_version_v5_and_feature_flags(self):
        """Verifica que /api/version retorne versión 5.0.0 con soporte de single_image_reel y ai_narrative_engine."""
        resp = self.client.get("/api/version")
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["version"], "5.0.0")
        feats = data["features"]
        self.assertTrue(feats["single_image_reel"])
        self.assertTrue(feats["ai_narrative_engine"])
        self.assertTrue(feats["google_gemini_free"])
        self.assertTrue(feats["groqcloud_free"])

    def test_api_generate_script_with_focus_and_hook_options(self):
        """Verifica que el endpoint /api/generate-script retorne 3 alternativas de gancho y campos completos."""
        payload = {
            "theme_key": "zero_balance",
            "specific_focus": "Looking at unpaid monthly bills with an empty bank account",
            "narrative_engine": "local",
            "mode": "deep",
            "narration_type": "prayer",
            "include_cta": True
        }
        resp = self.client.post("/api/generate-script", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertTrue(data["hook"])
        self.assertTrue(data["body"])
        self.assertTrue(data["cta"])
        self.assertIn("hook_options", data)
        self.assertEqual(len(data["hook_options"]), 3)

    def test_api_generate_image_prompt_endpoint(self):
        """Verifica que /api/generate-image-prompt retorne prompt único y limpio de texto."""
        payload = {
            "theme_key": "lost_child",
            "script_text": "Father, watch over my son who feels so distant.",
            "visual_style": "jesus",
            "narration_type": "prayer",
            "script_hook": "When an adult child stops answering calls",
            "script_body": "Father, hold my heart in peace.",
            "script_cta": "Leave their first name below so we can pray together."
        }
        resp = self.client.post("/api/generate-image-prompt", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn("prompt", data)
        self.assertIn("single_prompt", data)
        self.assertIn("strictly no text", data["single_prompt"])


if __name__ == "__main__":
    unittest.main()
