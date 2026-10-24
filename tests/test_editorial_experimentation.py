"""
Tests para optimización editorial y experimentación A/B de FaithSpark Daily.
Verifica:
- Formatos A y B de descripciones (longitud, tono, sin falsas promesas).
- Estrategias de hashtags (0, 3, 5), normalización y deduplicación CamelCase.
- Eliminación de CTAs automáticos no solicitados.
- Detección de guion desactualizado (stale) y preservación de ediciones manuales.
- Validador editorial: español accidental, manipulación, citas bíblicas, duplicados.
- Registro de métricas distinguiendo null de 0.
- Exportación CSV y JSON.
"""

import json
import os
import unittest
from fastapi.testclient import TestClient

from server import app
from engine.editorial_captions import (
    THEMATIC_HASHTAGS,
    get_theme_hashtags,
    normalize_hashtag,
    deduplicate_hashtags,
    generate_caption_format_a,
    generate_caption_format_b,
    generate_optimized_social_post,
    EXPERIMENT_MATRIX_18,
    get_next_recommended_experiment
)
from engine.editorial_validator import (
    check_accidental_spanish,
    check_manipulative_cta,
    check_biblical_reference,
    check_caption_script_alignment,
    check_duplicate_content,
    check_stale_caption,
    validate_post_readiness
)
from engine.results import save_observation, list_results, export_results_csv, export_results_json
from engine.scripts import generate_script, BIBLICAL_CATALOGUE


class EditorialExperimentationTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)
        self.test_dir = os.path.join(os.path.dirname(__file__), "test_data")
        os.makedirs(self.test_dir, exist_ok=True)
        self.test_results_file = os.path.join(self.test_dir, "test_experiment_results.json")
        if os.path.exists(self.test_results_file):
            os.remove(self.test_results_file)

    def tearDown(self):
        if os.path.exists(self.test_results_file):
            os.remove(self.test_results_file)

    # ─── 1. Formato A y Formato B de Descripciones ────────────────────────────

    def test_format_a_word_count_and_tone(self):
        """Formato A: Breve emocional, ~20-40 palabras, sin promesas milagrosas."""
        for key in ["lost_child", "night_anxiety", "zero_balance", "morning_favor"]:
            caption, word_count = generate_caption_format_a(
                theme_key=key,
                hook="To every parent whispering silent prayers tonight...",
                body="May God's peace guard your home and guide their steps.",
                cta="Rest in His faithful love tonight."
            )
            # Conteo de palabras entre 20 y 45 palabras
            self.assertTrue(20 <= word_count <= 45, f"Formato A para {key} tuvo {word_count} palabras.")
            # Sin frases manipulativas ni promesas de curación o dinero
            self.assertIsNone(check_manipulative_cta(caption))
            # Sin caracteres en español
            self.assertIsNone(check_accidental_spanish(caption))

    def test_format_b_word_count_and_scripture(self):
        """Formato B: Reflexivo contextual, ~50-85 palabras, con cita bíblica pertinente."""
        for key in ["lost_child", "family_protection", "zero_balance", "grief_loss"]:
            scripture = BIBLICAL_CATALOGUE[key]
            caption, word_count = generate_caption_format_b(
                theme_key=key,
                hook="When someone you love feels distant...",
                body="God's compassion is larger than the miles between words.",
                scripture=scripture,
                cta="Hold steady in faithful hope."
            )
            self.assertTrue(45 <= word_count <= 90, f"Formato B para {key} tuvo {word_count} palabras.")
            self.assertIn("—", caption, f"Formato B para {key} debe incluir cita bíblica.")
            self.assertIsNone(check_manipulative_cta(caption))
            self.assertIsNone(check_accidental_spanish(caption))

    # ─── 2. Estrategias de Hashtags (0, 3, 5) y Normalización ──────────────────

    def test_hashtag_strategies(self):
        """Verifica estrategias de 0, 3 y 5 hashtags."""
        key = "lost_child"
        tags_0 = get_theme_hashtags(key, strategy=0)
        self.assertEqual(len(tags_0), 0)

        tags_3 = get_theme_hashtags(key, strategy=3)
        self.assertEqual(len(tags_3), 3)
        self.assertEqual(tags_3[0], "#PrayingParents")

        tags_5 = get_theme_hashtags(key, strategy=5)
        self.assertEqual(len(tags_5), 5)
        self.assertIn("#PrayingParents", tags_5)
        self.assertIn("#FaithSparkDaily", tags_5)

    def test_hashtag_normalization_and_camelcase(self):
        """Verifica normalización, preservación de CamelCase y deduplicación case-insensitive."""
        raw_tags = ["#prayingparents", "PrayingParents", "#prodigalson", "#PRAYINGPARENTS", "#familyprayer"]
        deduped = deduplicate_hashtags(raw_tags)
        self.assertEqual(len(deduped), 3)
        self.assertEqual(deduped[0], "#prayingparents")
        self.assertEqual(deduped[1], "#prodigalson")
        self.assertEqual(deduped[2], "#familyprayer")

        # CamelCase con entrada limpia
        clean = normalize_hashtag("FaithfulParenting")
        self.assertEqual(clean, "#FaithfulParenting")

    # ─── 3. Eliminación de CTAs Automáticos no Solicitados ─────────────────────

    def test_no_unsolicited_automatic_cta(self):
        """generate_script no debe forzar un CTA pidiendo nombres si no se proporciona uno."""
        result = generate_script("lost_child", brief={"include_cta": False})
        self.assertEqual(result["cta"], "")
        self.assertNotIn("Leave your first name below", result["full_text"])

    # ─── 4. Ensamblado de Publicación y Grupos Experimentales A1-B3 ────────────

    def test_optimized_social_post_assembly(self):
        """Comprueba el armado de publicaciones y asignación de grupo experimental."""
        # A1: Breve, 0 tags
        post_a1 = generate_optimized_social_post("night_anxiety", "Hook", "Body", format_type="A", hashtag_strategy=0)
        self.assertEqual(post_a1["experiment_group"], "A1")
        self.assertEqual(len(post_a1["hashtags"]), 0)
        self.assertIn("✝️", post_a1["full_post_text"])

        # A2: Breve, 3 tags
        post_a2 = generate_optimized_social_post("lost_child", "Hook", "Body", format_type="A", hashtag_strategy=3)
        self.assertEqual(post_a2["experiment_group"], "A2")
        self.assertEqual(len(post_a2["hashtags"]), 3)

        # B3: Reflexivo, 5 tags
        post_b3 = generate_optimized_social_post("zero_balance", "Hook", "Body", format_type="B", hashtag_strategy=5)
        self.assertEqual(post_b3["experiment_group"], "B3")
        self.assertEqual(len(post_b3["hashtags"]), 5)

    def test_18_reel_experiment_matrix(self):
        """Verifica la matriz de 18 Reels equilibrada en los 6 grupos y 3 temáticas."""
        self.assertEqual(len(EXPERIMENT_MATRIX_18), 18)
        group_counts = {}
        for slot in EXPERIMENT_MATRIX_18:
            group_counts[slot["group"]] = group_counts.get(slot["group"], 0) + 1
        # Cada uno de los 6 grupos debe tener exactamente 3 publicaciones
        for grp in ["A1", "A2", "A3", "B1", "B2", "B3"]:
            self.assertEqual(group_counts[grp], 3, f"El grupo {grp} debe tener exactamente 3 slots.")

        # Recomendación de siguiente slot
        next_slot_0 = get_next_recommended_experiment([])
        self.assertEqual(next_slot_0["slot"], 1)
        next_slot_1 = get_next_recommended_experiment([{"id": "1"}])
        self.assertEqual(next_slot_1["slot"], 2)

    # ─── 5. Validador Editorial Pre-Publicación ────────────────────────────────

    def test_validator_accidental_spanish(self):
        """Detecta caracteres en español o palabras clave en español en copys públicos."""
        self.assertIsNotNone(check_accidental_spanish("Lord, hear this oración tonight."))
        self.assertIsNotNone(check_accidental_spanish("Dios te bendiga hoy."))
        self.assertIsNotNone(check_accidental_spanish("Peace over your home tonight ¿how are you?"))
        self.assertIsNone(check_accidental_spanish("May the peace of God guard your family tonight."))

    def test_validator_manipulative_cta(self):
        """Detecta promesas de dinero, curaciones o condicionamiento de interacción."""
        self.assertIsNotNone(check_manipulative_cta("Type AMEN to claim your financial miracle!"))
        self.assertIsNotNone(check_manipulative_cta("Share this with 5 people to receive a blessing."))
        self.assertIsNotNone(check_manipulative_cta("Comment Amen and God will heal you tomorrow."))
        self.assertIsNone(check_manipulative_cta("May peace be with your home tonight."))
        self.assertIsNone(check_manipulative_cta("Save this prayer if it encouraged your heart today."))

    def test_validator_canonical_biblical_reference(self):
        """Verifica referencias bíblicas canónicas y alerta sobre formatos erróneos."""
        self.assertIsNone(check_biblical_reference("Luke 15:20 (NIV) — While he was still a long way off..."))
        self.assertIsNone(check_biblical_reference("Philippians 4:6-7 (NIV)"))
        self.assertIsNotNone(check_biblical_reference("Gospel of Hope 99:12 (Fake)"))

    def test_validator_stale_caption_detection(self):
        """Detecta cuando el guion fue editado después de generar la descripción."""
        hook_orig = "Before turning off the lights..."
        body_orig = "God is with you tonight."
        # Guion no modificado
        self.assertIsNone(check_stale_caption(hook_orig, body_orig, "", hook_orig, body_orig))
        # Guion modificado por el usuario
        hook_edited = "Before you close your eyes tonight..."
        self.assertIsNotNone(check_stale_caption(hook_edited, body_orig, "", hook_orig, body_orig))

    def test_validator_duplicate_content(self):
        """Alerta sobre descripciones idénticas o casi idénticas a publicaciones recientes."""
        recent = [
            "To every parent whispering silent prayers before switching off the light tonight. May God guard your home.",
            "When bills feel heavy, remember that your worth is not measured by a paycheck."
        ]
        identical = "To every parent whispering silent prayers before switching off the light tonight. May God guard your home."
        self.assertIsNotNone(check_duplicate_content(identical, recent))

        unique = "Stand firm in the truth today; courage begins with one small step."
        self.assertIsNone(check_duplicate_content(unique, recent))

    # ─── 6. Registro de Métricas Persistente (null vs 0) ─────────────────────────

    def test_metrics_null_vs_zero_preservation(self):
        """Comprueba que métricas no observadas permanezcan como null y que 0 real se preserve."""
        payload = {
            "experiment_group": "A2",
            "creative": {
                "theme_key": "lost_child",
                "series_key": "everyday",
                "format": "prayer",
                "hook": "Test hook",
                "body": "Test body",
                "cta": "",
                "caption": "Test caption",
                "voice": "guy",
                "provider": "template",
                "opening_variant": 0
            },
            "checkpoint": "48h",
            "post_url": "https://facebook.com/reel/123456789",
            "metrics": {
                "views": 250,
                "shares": 0,           # Cero real observado
                "followers": None,     # Ausente / no disponible
                "average_watch_sec": 4.2
            }
        }

        record = save_observation(payload, path=self.test_results_file)
        self.assertEqual(record["experiment_group"], "A2")
        obs = record["observations"][0]
        metrics = obs["metrics"]

        # 0 debe ser estrictamente 0
        self.assertEqual(metrics["shares"], 0)
        # null / None debe ser estrictamente None
        self.assertIsNone(metrics["followers"])
        self.assertIsNone(metrics["reactions"])
        # Valores medidos
        self.assertEqual(metrics["views"], 250)
        self.assertEqual(metrics["average_watch_sec"], 4.2)

    def test_export_results_csv_and_json(self):
        """Comprueba la exportación a CSV y JSON con distinción de campos vacíos."""
        payload = {
            "experiment_group": "B3",
            "creative": {
                "theme_key": "zero_balance",
                "series_key": "everyday",
                "format": "prayer",
                "hook": "Financial test hook",
                "body": "Financial test body",
                "cta": "",
                "caption": "Financial caption",
                "voice": "christopher",
                "provider": "template",
                "opening_variant": 0
            },
            "checkpoint": "7d",
            "post_url": "https://facebook.com/reel/987654321",
            "metrics": {
                "views": 520,
                "shares": 0,
                "followers": None
            }
        }
        save_observation(payload, path=self.test_results_file)

        # Probar exportación CSV
        csv_text = export_results_csv(path=self.test_results_file)
        self.assertIn("reel_id,created_at,experiment_group", csv_text)
        self.assertIn("B3", csv_text)
        self.assertIn("zero_balance", csv_text)
        self.assertIn(",520,", csv_text)
        self.assertIn(",0,", csv_text)  # shares=0

        # Probar exportación JSON
        json_text = export_results_json(path=self.test_results_file)
        parsed = json.loads(json_text)
        self.assertEqual(len(parsed), 1)
        self.assertEqual(parsed[0]["experiment_group"], "B3")
        self.assertIsNone(parsed[0]["observations"][0]["metrics"]["followers"])
        self.assertEqual(parsed[0]["observations"][0]["metrics"]["shares"], 0)

    # ─── 7. Endpoints HTTP FastAPI ─────────────────────────────────────────────

    def test_api_editorial_caption_endpoint(self):
        """Prueba endpoint POST /api/editorial-caption."""
        res = self.client.post("/api/editorial-caption", json={
            "theme_key": "night_anxiety",
            "hook": "When your mind will not rest tonight...",
            "body": "May God's quiet peace surround your pillow.",
            "cta": "Rest well tonight.",
            "format_type": "A",
            "hashtag_strategy": 3
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data["experiment_group"], "A2")
        self.assertEqual(len(data["hashtags"]), 3)
        self.assertIn("✝️", data["full_post_text"])

    def test_api_editorial_validate_endpoint(self):
        """Prueba endpoint POST /api/editorial-validate."""
        res = self.client.post("/api/editorial-validate", json={
            "theme_key": "lost_child",
            "script_hook": "To every parent whispering silent prayers tonight...",
            "script_body": "May God's quiet mercy meet your child wherever they walk.",
            "script_cta": "",
            "caption_text": "To every parent whispering silent prayers tonight. May peace guard your home.",
            "scripture_text": "Luke 15:20 (NIV)"
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertTrue(data["ready"])
        self.assertEqual(len(data["warnings"]), 0)

    def test_api_experiment_matrix_and_exports(self):
        """Prueba endpoints de matriz de experimentos y descargas CSV/JSON."""
        res_matrix = self.client.get("/api/editorial-experiment-matrix")
        self.assertEqual(res_matrix.status_code, 200)
        self.assertEqual(len(res_matrix.json()["matrix"]), 18)

        res_csv = self.client.get("/api/editorial-results/export/csv")
        self.assertEqual(res_csv.status_code, 200)
        self.assertIn("text/csv", res_csv.headers["content-type"])

        res_json = self.client.get("/api/editorial-results/export/json")
        self.assertEqual(res_json.status_code, 200)
        self.assertIn("application/json", res_json.headers["content-type"])


if __name__ == "__main__":
    unittest.main()
