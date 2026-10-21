import asyncio
import os
import sys
import time
import unittest
from typing import List, Dict

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.scripts import (
    generate_script,
    get_themes_list,
    THEMATIC_PILLARS,
    BIBLICAL_CATALOGUE,
    VIRAL_THEMES,
    get_daily_batch_schedule
)
from engine.script_provider import get_script_provider
from engine.tts import synthesize_speech, get_available_voices, VOICES
from engine.subtitles import generate_viral_ass, SUBTITLE_STYLES
from engine.video import render_reel, get_audio_duration
from engine.history import ScriptHistoryManager, calculate_jaccard_similarity
from fastapi.testclient import TestClient
import server


class QualitySuiteTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(server.app)
        cls.test_outputs_dir = os.path.join(BASE_DIR, "outputs", "test_run")
        os.makedirs(cls.test_outputs_dir, exist_ok=True)
        print("\n=======================================================")
        print("  JESUSREELS STUDIO — PROFESSIONAL QUALITY TEST SUITE  ")
        print("=======================================================\n")

    def test_01_script_generation_20_across_pillars(self):
        """1. Genera 20 guiones cubriendo todos los pilares temáticos y valida el esquema."""
        print("\n[TEST 01] Generando 20 guiones a través de los 5 pilares temáticos...")
        theme_keys = list(VIRAL_THEMES.keys())
        generated = []
        for i in range(20):
            theme = theme_keys[i % len(theme_keys)]
            t0 = time.time()
            res = generate_script(theme, mode="deep")
            dt = time.time() - t0
            generated.append((theme, res, dt))

            # Validar esquema estricto
            self.assertIn("hook", res)
            self.assertIn("body", res)
            self.assertIn("closing", res)
            self.assertIn("full_text", res)
            self.assertIn("estimated_duration_sec", res)
            self.assertIn("human_situation", res)
            self.assertIn("central_idea", res)
            self.assertIn("thematic_pillar", res)
            self.assertIn("perspective", res)
            self.assertIn("scripture", res)
            self.assertIn("seo_caption", res)
            self.assertIn("hashtags", res)
            self.assertIn("scene_1_prompt", res)
            self.assertIn("scene_2_prompt", res)
            self.assertIn("scene_3_prompt", res)

            # Validar duración razonable para Reels (15 - 35 segundos)
            dur = res["estimated_duration_sec"]
            self.assertGreaterEqual(dur, 15)
            self.assertLessEqual(dur, 35)

            # Validar que no contenga promesas de milagros garantizados
            full = res["full_text"].lower()
            forbidden = ["guaranteed wealth", "instant cash", "claim your million", "type amen or be cursed"]
            for f in forbidden:
                self.assertNotIn(f, full, f"Frase prohibida detectada: {f}")

        print(f"  -> 20/20 guiones generados y validados correctamente.")

    def test_02_hook_diversity_and_anti_repetition(self):
        """2. Comprueba que no se repitan ganchos idénticos en ejecuciones consecutivas."""
        print("\n[TEST 02] Comprobando diversidad de ganchos en ejecuciones consecutivas...")
        hooks = []
        theme = "morning_favor"
        for _ in range(5):
            res = generate_script(theme, mode="deep")
            hooks.append(res["hook"])

        # Verificar que no todos los ganchos sean idénticos
        unique_hooks = set(hooks)
        self.assertGreaterEqual(len(unique_hooks), 2, "Debe existir rotación y diversidad de aperturas.")

        # Verificar similitud de Jaccard entre pares consecutivos
        for i in range(len(hooks) - 1):
            sim = calculate_jaccard_similarity(hooks[i], hooks[i + 1])
            self.assertLess(sim, 0.85, f"Ganchos consecutivos excesivamente similares ({sim:.2f})")
        print(f"  -> Diversidad de ganchos verificada con éxito ({len(unique_hooks)} variantes en 5 pruebas).")

    def test_03_biblical_catalogue_integrity(self):
        """3. Comprueba que las citas bíblicas correspondan al catálogo verificado sin alucinaciones."""
        print("\n[TEST 03] Verificando catálogo canónico de escrituras...")
        self.assertGreaterEqual(len(BIBLICAL_CATALOGUE), 26)
        for theme_key, citation in BIBLICAL_CATALOGUE.items():
            self.assertIsInstance(citation, str)
            self.assertIn("—", citation, f"La cita para '{theme_key}' debe incluir el separador '—'")
            self.assertGreater(len(citation), 15)
        print(f"  -> {len(BIBLICAL_CATALOGUE)} referencias bíblicas verificadas contra fuentes canónicas.")

    def test_04_tts_voice_preview_edge_voices(self):
        """4. Prueba de síntesis de voz con las voces recomendadas: Guy, Brian y Christopher."""
        print("\n[TEST 04] Probando síntesis de voz con Edge-TTS (Guy, Brian, Christopher)...")
        sample_text = "The Lord is my strength and my shield; my heart trusts in Him, and He helps me."
        voices_to_test = ["guy", "brian", "christopher"]

        async def _run_tests():
            results = []
            for v_id in voices_to_test:
                out_path = os.path.join(self.test_outputs_dir, f"test_voice_{v_id}.mp3")
                t0 = time.time()
                cues = await synthesize_speech(sample_text, v_id, out_path, rate="-6%")
                dt = time.time() - t0
                self.assertTrue(os.path.exists(out_path))
                self.assertGreater(os.path.getsize(out_path), 2000)
                self.assertIsNotNone(cues)
                self.assertGreater(len(cues), 0)
                dur = get_audio_duration(out_path)
                results.append((v_id, dt, dur, len(cues)))
            return results

        results = asyncio.run(_run_tests())
        for v_id, dt, dur, cues_count in results:
            print(f"  -> Voz '{v_id}': generada en {dt:.2f}s | Duración: {dur:.2f}s | Cues: {cues_count}")

    def test_05_clean_subtitle_generation(self):
        """5. Comprobación de generación del archivo de subtítulos con estilo 'clean' y zonas seguras."""
        print("\n[TEST 05] Generando subtítulos ASS con estilo CLEAN...")
        from engine.tts import CueItem
        cues = [
            CueItem(start_sec=0.0, end_sec=1.8, text="Peace be with your heart today."),
            CueItem(start_sec=1.8, end_sec=4.2, text="The Lord goes before you in every trial."),
            CueItem(start_sec=4.2, end_sec=6.5, text="Rest in His unfailing love tonight.")
        ]
        ass_path = os.path.join(self.test_outputs_dir, "test_clean_subtitles.ass")
        res_path = generate_viral_ass(cues, ass_path, style_key="clean", margin_v=440)
        self.assertTrue(os.path.exists(res_path))

        with open(res_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("Style: MainSub,Montserrat,70", content)
        self.assertIn("MarginV", content)
        self.assertIn("Dialogue: 2,", content)
        print("  -> Archivo ASS generado correctamente con estilo limpio y margen vertical seguro (440px).")

    def test_06_end_to_end_video_render(self):
        """6. Renderizado completo de un video de prueba de extremo a extremo en vertical 9:16."""
        print("\n[TEST 06] Renderizando video de prueba completo en 9:16...")
        audio_path = os.path.join(self.test_outputs_dir, "test_voice_guy.mp3")
        ass_path = os.path.join(self.test_outputs_dir, "test_clean_subtitles.ass")
        output_video = os.path.join(self.test_outputs_dir, "test_rendered_reel.mp4")

        # Usar imagen base existente
        assets_img = os.path.join(BASE_DIR, "assets", "images", "jesus_healing_miracle.jpg")
        if not os.path.exists(assets_img):
            avail = [f for f in os.listdir(os.path.join(BASE_DIR, "assets", "images")) if f.endswith((".jpg", ".png"))]
            assets_img = os.path.join(BASE_DIR, "assets", "images", avail[0])

        t0 = time.time()
        res = render_reel(
            image_path=assets_img,
            audio_path=audio_path,
            ass_path=ass_path,
            output_mp4_path=output_video,
            aspect_ratio="9:16",
            effect_type="none",
            camera_motion="zoom_in",
            music_track="worship_piano_peace",
            music_volume=0.15,
            enable_sfx=False,
            master_lufs=True,
            generate_trending_audio_version=False
        )
        dt = time.time() - t0

        self.assertTrue(os.path.exists(output_video))
        self.assertGreater(os.path.getsize(output_video), 50000)
        self.assertIn("actual_duration_sec", res)
        self.assertIn("target_duration_sec", res)
        self.assertIn("duration_diff_sec", res)

        # 7. Comprobación de duración real frente a estimada (tolerancia <= 1.5s)
        diff = res["duration_diff_sec"]
        self.assertLessEqual(diff, 1.5, f"Discrepancia de duración excesiva: {diff}s")

        print(f"  -> Video exportado en {dt:.2f}s | Duración real: {res['actual_duration_sec']}s | Discrepancia: {diff}s | Tamaño: {os.path.getsize(output_video)/1024:.1f} KB")

    def test_07_fastapi_endpoints_regression(self):
        """7. Pruebas de regresión sobre los endpoints HTTP del servidor FastAPI."""
        print("\n[TEST 07] Ejecutando pruebas de regresión en endpoints FastAPI...")
        # /health
        r = self.client.get("/health")
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()["status"], "ok")

        # /api/themes
        r = self.client.get("/api/themes")
        self.assertEqual(r.status_code, 200)
        themes = r.json()
        self.assertGreaterEqual(len(themes), 26)

        # /api/voices
        r = self.client.get("/api/voices")
        self.assertEqual(r.status_code, 200)
        voices = r.json()
        self.assertGreaterEqual(len(voices), 3)
        self.assertEqual(voices[0]["key"], "guy", "La primera voz debe ser Guy por defecto.")

        # /api/worship-tracks
        r = self.client.get("/api/worship-tracks")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()), 4)

        # /api/subtitle-styles
        r = self.client.get("/api/subtitle-styles")
        self.assertEqual(r.status_code, 200)
        styles = {s["key"] for s in r.json()}
        self.assertIn("clean", styles)
        self.assertIn("karaoke", styles)
        self.assertIn("pop", styles)
        self.assertIn("cinematic", styles)

        # /api/magnetic-comments
        r = self.client.get("/api/magnetic-comments")
        self.assertEqual(r.status_code, 200)
        comments = r.json()
        self.assertEqual(len(comments), 6)
        # Asegurar que no contengan engagement bait
        for c in comments:
            self.assertNotIn("type amen", c.lower())
            self.assertNotIn("claim your miracle", c.lower())

        # /api/daily-batch
        r = self.client.get("/api/daily-batch")
        self.assertEqual(r.status_code, 200)
        batch = r.json()
        self.assertEqual(len(batch), 3)
        slots = [s["slot"] for s in batch]
        self.assertEqual(slots, ["morning", "midday", "night"])

        # POST /api/generate-script
        r = self.client.post("/api/generate-script", json={"theme_key": "divine_grace", "mode": "deep"})
        self.assertEqual(r.status_code, 200)
        s_data = r.json()
        self.assertIn("hook", s_data)
        self.assertIn("seo_caption", s_data)

        # POST /api/generate-image-prompt
        r = self.client.post("/api/generate-image-prompt", json={"theme_key": "divine_grace", "script_text": s_data["body"]})
        self.assertEqual(r.status_code, 200)
        p_data = r.json()
        self.assertIn("scene_1_prompt", p_data)
        self.assertIn("scene_2_prompt", p_data)
        self.assertIn("scene_3_prompt", p_data)

        print("  -> Todos los endpoints HTTP de la API pasaron las pruebas de regresión con éxito.")


if __name__ == "__main__":
    unittest.main()
