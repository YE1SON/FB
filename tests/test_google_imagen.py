"""
Pruebas unitarias para Google Imagen 3 (Google AI Studio) y Puter AI en JesusReels Studio.
"""

import os
import json
import unittest
from unittest.mock import patch, MagicMock
from io import BytesIO
from PIL import Image
from fastapi.testclient import TestClient

from server import app
from engine.image_gen import (
    load_keys,
    save_keys,
    get_providers_status,
    generate_google_imagen,
    generate_ai_scene_image,
    KEYS_FILE,
    ASSETS_DIR
)


def _create_dummy_jpeg_bytes(width=768, height=1360):
    img = Image.new("RGB", (width, height), (40, 70, 110))
    buf = BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


class GoogleImagenTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        # Asegurar backup temporal de claves
        self.original_keys = {}
        if os.path.exists(KEYS_FILE):
            with open(KEYS_FILE, "r", encoding="utf-8") as f:
                self.original_keys = json.load(f)

    def tearDown(self):
        # Restaurar claves originales
        if self.original_keys:
            with open(KEYS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.original_keys, f, indent=2)

    def test_keys_management_with_gemini(self):
        """Verifica que gemini_api_key se guarde y recupere correctamente."""
        test_key = "AIzaSy_fake_test_key_12345"
        save_keys(gemini_api_key=test_key)
        loaded = load_keys()
        self.assertEqual(loaded.get("gemini_api_key"), test_key)

    def test_providers_status_includes_google_imagen_and_puter(self):
        """Verifica que get_providers_status reporte tanto Google Imagen 3 como Puter AI."""
        status = get_providers_status()
        self.assertIn("google_imagen", status)
        self.assertIn("puter", status)
        self.assertIn("Google Imagen 3", status["google_imagen"]["name"])
        self.assertIn("Puter AI", status["puter"]["name"])
        self.assertTrue(status["puter"]["configured"])

    def test_generate_google_imagen_missing_key_raises_informative_error(self):
        """Verifica que falte la clave genere un error claro indicando dónde obtenerla gratis."""
        with patch.dict(os.environ, {"GEMINI_API_KEY": "", "GOOGLE_API_KEY": ""}):
            # Limpiar archivo de claves temporalmente
            if os.path.exists(KEYS_FILE):
                os.remove(KEYS_FILE)

            with self.assertRaises(ValueError) as ctx:
                generate_google_imagen("a mother praying at night", api_key="")
            self.assertIn("GEMINI_API_KEY", str(ctx.exception))
            self.assertIn("aistudio.google.com", str(ctx.exception))

    @patch("google.genai.Client")
    def test_generate_google_imagen_success_with_sdk(self, mock_client_cls):
        """Simula una respuesta exitosa del SDK oficial de Google GenAI."""
        fake_bytes = _create_dummy_jpeg_bytes()
        mock_client = MagicMock()
        mock_gen_img = MagicMock()
        mock_gen_img.image.image_bytes = fake_bytes
        mock_client.models.generate_images.return_value = MagicMock(generated_images=[mock_gen_img])
        mock_client_cls.return_value = mock_client

        img_bytes = generate_google_imagen("a mother praying peacefully", api_key="AIzaSyMockKey")
        self.assertEqual(img_bytes, fake_bytes)
        mock_client.models.generate_images.assert_called_once()

    @patch("google.genai.Client")
    def test_generate_ai_scene_image_with_google_imagen_provider(self, mock_client_cls):
        """Prueba generate_ai_scene_image con provider='google_imagen'."""
        fake_bytes = _create_dummy_jpeg_bytes(768, 1360)
        mock_client = MagicMock()
        mock_gen_img = MagicMock()
        mock_gen_img.image.image_bytes = fake_bytes
        mock_client.models.generate_images.return_value = MagicMock(generated_images=[mock_gen_img])
        mock_client_cls.return_value = mock_client

        res = generate_ai_scene_image(
            prompt="father hugging his son, emotional reconciliation, soft warm window light",
            provider="google_imagen",
            gemini_api_key="AIzaSyMockKey",
            scene_num=1
        )
        self.assertEqual(res["status"], "success")
        self.assertIn("custom_ai_", res["filename"])
        self.assertIn("Google Imagen 3", res["engine"])

        # Verificar que el archivo existe en ASSETS_DIR
        file_path = os.path.join(ASSETS_DIR, res["filename"])
        self.assertTrue(os.path.exists(file_path))
        # Limpieza
        if os.path.exists(file_path):
            os.remove(file_path)

    @patch("google.genai.Client")
    def test_api_generate_ai_image_endpoint(self, mock_client_cls):
        """Prueba endpoint POST /api/generate-ai-image con provider='google_imagen'."""
        fake_bytes = _create_dummy_jpeg_bytes(768, 1360)
        mock_client = MagicMock()
        mock_gen_img = MagicMock()
        mock_gen_img.image.image_bytes = fake_bytes
        mock_client.models.generate_images.return_value = MagicMock(generated_images=[mock_gen_img])
        mock_client_cls.return_value = mock_client

        payload = {
            "prompt": "elderly woman holding a worn bible with tearful joyful smile",
            "aspect_ratio": "9:16",
            "provider": "google_imagen",
            "gemini_api_key": "AIzaSyMockKey",
            "scene_num": 1
        }
        resp = self.client.post("/api/generate-ai-image", json=payload)
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertIn("custom_ai_", data["filename"])

        file_path = os.path.join(ASSETS_DIR, data["filename"])
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_api_save_keys_endpoint_with_gemini(self):
        """Prueba endpoint POST /api/save-image-keys con gemini_api_key."""
        test_key = "AIzaSyTestRestKey_9876"
        resp = self.client.post("/api/save-image-keys", json={"gemini_api_key": test_key})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(data["status"], "success")
        self.assertTrue(data["providers"]["google_imagen"]["configured"])


if __name__ == "__main__":
    unittest.main()
