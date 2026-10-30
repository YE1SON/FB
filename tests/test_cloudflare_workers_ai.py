"""
Pruebas exhaustivas para la integración de Cloudflare Workers AI (FLUX.2 Klein 9B y 4B),
rastreador de consumo de neuronas y generador de prompts narrativos fotorrealistas.
"""

import os
from io import BytesIO
from PIL import Image
import unittest
from unittest.mock import patch, MagicMock
from fastapi.testclient import TestClient

import server
from engine.cloudflare_neurons import (
    load_neurons_data,
    save_neurons_data,
    estimate_neurons,
    check_quota_available,
    record_neurons_consumption,
    get_neurons_status,
    reset_daily_neurons,
    DEFAULT_DAILY_LIMIT,
    MODEL_NEURON_RATES
)
from engine.narrative_prompts import (
    generate_narrative_prompts_for_script,
    THEME_NARRATIVE_BLUEPRINTS,
    PHOTO_CUES
)
from engine.image_gen import (
    generate_cloudflare_flux_klein,
    generate_ai_scene_image,
    CLOUDFLARE_MODELS
)


class CloudflareWorkersAITests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(server.app)
        reset_daily_neurons()

    def tearDown(self):
        reset_daily_neurons()

    # ─── 1. Pruebas del Rastreador de Neuronas ───────────────────────────────

    def test_neuron_rates_and_estimation(self):
        """Verifica las tasas oficiales de neuronas para Klein 9B y 4B."""
        rate_9b = estimate_neurons("@cf/black-forest-labs/flux-2-klein-9b", has_reference=False)
        self.assertEqual(rate_9b, 1364.0)

        rate_4b = estimate_neurons("@cf/black-forest-labs/flux-2-klein-4b", has_reference=False)
        self.assertEqual(rate_4b, 104.2)

        rate_4b_ref = estimate_neurons("@cf/black-forest-labs/flux-2-klein-4b", has_reference=True)
        self.assertEqual(rate_4b_ref, 104.2 + 21.5)

    def test_quota_tracking_and_daily_exhaustion(self):
        """Verifica que la cuota evite sobregiros y reporte claramente al agotarse."""
        status_init = get_neurons_status()
        self.assertEqual(status_init["consumed_neurons"], 0.0)
        self.assertFalse(status_init["is_exhausted"])

        # Registrar consumo de una Escena 1 (Klein 9B)
        record_neurons_consumption("@cf/black-forest-labs/flux-2-klein-9b", scene_num=1, has_reference=False)
        status_after_s1 = get_neurons_status()
        self.assertEqual(status_after_s1["consumed_neurons"], 1364.0)
        self.assertEqual(status_after_s1["generations_today"], 1)

        # Simular consumo acumulado hasta el límite
        data = load_neurons_data()
        data["consumed"] = 9950.0
        save_neurons_data(data)

        # 9B requiere 1364 neuronas: debe ser rechazado
        allowed, msg, needed = check_quota_available("@cf/black-forest-labs/flux-2-klein-9b")
        self.assertFalse(allowed)
        self.assertIn("Cuota diaria gratuita de Neuronas alcanzada", msg)
        self.assertIn("Para evitar cobros automáticos", msg)

        # 4B requiere 104.2 neuronas: con 50 neuronas restantes también debe ser rechazado
        allowed_4b, msg_4b, _ = check_quota_available("@cf/black-forest-labs/flux-2-klein-4b")
        self.assertFalse(allowed_4b)

    def test_reset_neurons_endpoint(self):
        """Comprueba los endpoints REST de lectura y reseteo de neuronas."""
        record_neurons_consumption("@cf/black-forest-labs/flux-2-klein-4b", scene_num=2)
        res_get = self.client.get("/api/cloudflare/neurons")
        self.assertEqual(res_get.status_code, 200)
        data = res_get.json()
        self.assertGreater(data["consumed_neurons"], 0)

        res_reset = self.client.post("/api/cloudflare/neurons/reset")
        self.assertEqual(res_reset.status_code, 200)
        reset_data = res_reset.json()
        self.assertEqual(reset_data["consumed_neurons"], 0.0)

    # ─── 2. Pruebas de Prompts Narrativos Fotorrealistas ─────────────────────

    def test_narrative_prompts_reflect_authentic_situations(self):
        """Verifica que los prompts generen situaciones humanas auténticas sin clichés."""
        prompts = generate_narrative_prompts_for_script(
            theme_key="zero_balance",
            script_text="When the bank account says zero, fear wants to speak.",
            custom_topic="Late night budgeting"
        )
        s1 = prompts["scene_1_prompt"]
        s2 = prompts["scene_2_prompt"]
        s3 = prompts["scene_3_prompt"]

        # Debe incluir situación humana, no stock repetitivo de cruces
        self.assertIn("working adult", s1)
        self.assertIn("budget papers", s1)
        self.assertIn("Late night budgeting", s1)

        # Escenas 2 y 3 deben referenciar a image1 para coherencia multi-referencia
        self.assertIn("image1", s2)
        self.assertIn("image1", s3)

        # Reglas fotográficas
        self.assertIn("photorealistic", s1)
        self.assertIn("no text", s1)
        self.assertIn("no text", s2)
        self.assertIn("no text", s3)

    def test_narrative_prompts_for_all_thematic_blueprints(self):
        """Comprueba que todos los blueprints temáticos definidos produzcan 3 escenas coherentes."""
        for key in THEME_NARRATIVE_BLUEPRINTS:
            res = generate_narrative_prompts_for_script(theme_key=key)
            self.assertIn("scene_1_prompt", res)
            self.assertIn("scene_2_prompt", res)
            self.assertIn("scene_3_prompt", res)
            self.assertIn("no text", res["scene_1_prompt"])
            self.assertIn("Jesus", res["scene_1_prompt"])

    # ─── 3. Pruebas de Inferencia y Manejo de Errores Reales ─────────────────

    @patch("engine.image_gen.requests.post")
    def test_cloudflare_generation_success_and_neuron_charging(self, mock_post):
        """Simula una respuesta exitosa de Cloudflare Workers AI."""
        import base64
        buf = BytesIO()
        Image.new("RGB", (768, 1360), color=(100, 150, 200)).save(buf, format="JPEG")
        fake_jpeg = buf.getvalue()

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {
            "success": True,
            "result": {
                "image": base64.b64encode(fake_jpeg).decode("utf-8")
            }
        }
        mock_post.return_value = mock_resp

        result = generate_ai_scene_image(
            prompt="A cinematic 35mm portrait of a humble father praying",
            provider="cloudflare_auto",
            scene_num=1
        )
        self.assertEqual(result["status"], "success")
        self.assertIn("Klein 9B", result["label"])
        self.assertTrue(os.path.exists(os.path.join(server.ASSETS_DIR, result["filename"])))

        # Verificar que se registraron neuronas de Klein 9B
        st = get_neurons_status()
        self.assertEqual(st["consumed_neurons"], 1364.0)

        # Limpiar archivo temporal generado
        try:
            os.remove(os.path.join(server.ASSETS_DIR, result["filename"]))
        except OSError:
            pass

    @patch("engine.image_gen.requests.post")
    def test_cloudflare_real_error_reporting_no_silent_library_fallback(self, mock_post):
        """
        REGLA CRÍTICA: Cuando falle la generación con Cloudflare, debe mostrarse el error real.
        NO debe sustituir silenciosamente una imagen fallida por otra de la biblioteca.
        """
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.text = '{"errors": [{"code": 1000, "message": "Content moderation filter triggered"}]}'
        mock_resp.json.return_value = {
            "success": False,
            "errors": [{"code": 1000, "message": "Content moderation filter triggered"}]
        }
        mock_post.return_value = mock_resp

        with self.assertRaises(RuntimeError) as ctx:
            generate_ai_scene_image(
                prompt="Controversial prompt triggering filter",
                provider="cloudflare_auto",
                scene_num=1
            )
        self.assertIn("Content moderation filter triggered", str(ctx.exception))

    @patch("engine.image_gen.generate_pollinations")
    @patch("engine.image_gen.requests.post")
    def test_cloudflare_flagged_output_resilient_fallback(self, mock_post, mock_pollinations):
        """
        Verifica que ante un falso positivo del filtro de seguridad de Cloudflare ('Your output has been flagged'),
        el motor active el respaldo automático en Pollinations FLUX para asegurar la continuidad del reel.
        """
        import base64
        buf = BytesIO()
        Image.new("RGB", (768, 1360), color=(180, 210, 240)).save(buf, format="JPEG")
        fake_jpeg = buf.getvalue()

        # Cloudflare responde con HTTP 400 y el mensaje de flag oficial
        mock_resp = MagicMock()
        mock_resp.status_code = 400
        mock_resp.text = '{"errors": [{"code": 3030, "message": "AiError: Your output has been flagged. Please choose another prompt / input image combination (79171613-1c87-45b2-a59c-bc3d1313316a)"}]}'
        mock_resp.json.return_value = {
            "success": False,
            "errors": [{"code": 3030, "message": "AiError: Your output has been flagged. Please choose another prompt / input image combination (79171613-1c87-45b2-a59c-bc3d1313316a)"}]
        }
        mock_post.return_value = mock_resp

        # Pollinations genera la imagen de respaldo
        mock_pollinations.return_value = fake_jpeg

        result = generate_ai_scene_image(
            prompt="A vulnerable scene in the bedroom touching the bedside",
            provider="cloudflare_auto",
            scene_num=1
        )
        self.assertEqual(result["status"], "success")
        self.assertIn("Pollinations FLUX (Respaldo por filtro Cloudflare)", result["engine"])
        self.assertTrue(os.path.exists(os.path.join(server.ASSETS_DIR, result["filename"])))

        # Limpiar archivo temporal
        try:
            os.remove(os.path.join(server.ASSETS_DIR, result["filename"]))
        except OSError:
            pass

    def test_prompt_sanitization_removes_moderation_triggers(self):
        """Verifica que el sanitizador reemplace palabras de riesgo por términos fotográficos seguros."""
        from engine.image_gen import sanitize_prompt_for_image_engine
        raw = "intimate bedroom scene with vulnerability, touching the bedside, chest heavy with unworthiness"
        clean = sanitize_prompt_for_image_engine(raw)
        self.assertNotIn("intimate", clean.lower())
        self.assertNotIn("bedroom", clean.lower())
        self.assertNotIn("vulnerability", clean.lower())
        self.assertNotIn("bedside", clean.lower())
        self.assertNotIn("unworthiness", clean.lower())
        self.assertIn("living room", clean.lower())
        self.assertIn("text-free", clean.lower())

    def test_quota_exhaustion_raises_runtime_error(self):
        """Verifica que el generador rechace la llamada si se agotaron las 10,000 neuronas."""
        data = load_neurons_data()
        data["consumed"] = 10000.0
        save_neurons_data(data)

        with self.assertRaises(RuntimeError) as ctx:
            generate_ai_scene_image(
                prompt="Prompt after daily quota exhausted",
                provider="cloudflare_auto",
                scene_num=1
            )
        self.assertIn("Cuota diaria gratuita de Neuronas alcanzada", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
