"""Deployment identity endpoint regressions."""
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
import server

class ReleaseVerificationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(server.app)

    def test_health(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "ok")
        self.assertEqual(response.json()["version"], server.app.version)

    def test_running_commit_and_features(self):
        with patch("server._deployed_commit", return_value="123456789abc"):
            for path in ("/api/version", "/studio/api/version"):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertEqual(data["git_commit"], "123456789abc")
                self.assertEqual(data["voices"], ["brian", "christopher", "guy"])
                self.assertTrue(data["features"]["audio_aligned_scene_transitions"])
                self.assertEqual(len(data["narration_formats"]), 4)

if __name__ == "__main__":
    unittest.main()
