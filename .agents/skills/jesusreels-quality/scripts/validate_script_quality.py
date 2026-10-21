#!/usr/bin/env python3
"""
Validador de calidad reproducible para JesusReels Studio.
Ejecuta comprobaciones sobre guiones generados, vocabulario, duración y prompts visuales.
Invocable como parte de la Agent Skill jesusreels-quality.
"""

import sys
import os
import re

# Añadir raíz del proyecto al path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.scripts import generate_script, VIRAL_THEMES

FORBIDDEN_PHRASES = [
    r"stop\s+scrolling",
    r"comment\s+amen\s+to\s+receive",
    r"drop\s+your\s+first\s+name\s+to\s+claim",
    r"urgent\s+message\s+from\s+god",
    r"financial\s+miracle\s+before",
    r"guaranteed\s+healing",
    r"share\s+this\s+or\s+be\s+cursed"
]

def validate_single_script(script_data: dict) -> list:
    """Retorna una lista de errores encontrados en el guion."""
    errors = []
    
    # 1. Campos obligatorios
    required_keys = ["theme_key", "hook", "body", "cta", "full_text", "scripture", "hashtags", "scene_1_prompt", "scene_2_prompt", "scene_3_prompt"]
    for k in required_keys:
        if k not in script_data or not script_data[k]:
            errors.append(f"Falta campo requerido: '{k}'")

    full_text = (script_data.get("full_text") or "").lower()
    
    # 2. Ausencia de manipulación / clickbait
    for pattern in FORBIDDEN_PHRASES:
        if re.search(pattern, full_text):
            errors.append(f"Frase prohibida/manipuladora detectada con patrón: '{pattern}'")

    # 3. Duración estimada
    est_dur = script_data.get("estimated_duration_sec", 0)
    if est_dur < 12.0 or est_dur > 45.0:
        errors.append(f"Duración estimada fuera de rango razonable (12-45s): {est_dur}s")

    # 4. Hashtags
    hashtags = script_data.get("hashtags", [])
    if len(hashtags) < 2 or len(hashtags) > 6:
        errors.append(f"Cantidad de hashtags fuera del estándar (2-6): {len(hashtags)}")

    # 5. Prompts visuales
    for sc in ["scene_1_prompt", "scene_2_prompt", "scene_3_prompt"]:
        p = script_data.get(sc, "")
        if "8k" in p.lower() or "masterpiece" in p.lower():
            errors.append(f"El prompt {sc} contiene adjetivos de relleno prohibidos ('8k', 'masterpiece')")

    return errors

def run_suite():
    print("=" * 60)
    print("  JESUSREELS QUALITY AUDIT - VALIDATION SUITE")
    print("=" * 60)

    total_tested = 0
    total_passed = 0
    all_errors = []

    # Probar 10 temas aleatorios
    theme_keys = list(VIRAL_THEMES.keys())[:10]
    for tk in theme_keys:
        total_tested += 1
        script = generate_script(theme_key=tk, mode="deep")
        errs = validate_single_script(script)
        if not errs:
            total_passed += 1
            print(f" [PASS] Tema: {tk:<20} | Duración: {script.get('estimated_duration_sec', 0):.1f}s | Palabras: {script.get('word_count', 0)}")
        else:
            print(f" [FAIL] Tema: {tk:<20} -> {len(errs)} error(es)")
            for e in errs:
                print(f"        * {e}")
                all_errors.append((tk, e))

    print("\n" + "-" * 60)
    print(f"Resultado: {total_passed}/{total_tested} guiones aprobados.")
    print("-" * 60)
    
    if total_passed == total_tested:
        print("Auditoría de calidad: SUPERADA EXITOSAMENTE.")
        return 0
    else:
        print(f"Auditoría de calidad: {len(all_errors)} fallas encontradas.")
        return 1

if __name__ == "__main__":
    sys.exit(run_suite())
