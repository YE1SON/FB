"""
Gestor de Historial Local para JesusReels Studio.
Registra guiones y temas recientes para evitar repeticiones mecánicas en el generador y en el planificador diario.
Utiliza comparación ligera de n-gramas sin recopilar metadatos de usuario ni métricas externas.
"""

import os
import json
import time
from typing import List, Dict, Optional, Tuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HISTORY_FILE = os.path.join(BASE_DIR, "outputs", "script_history.json")

def _normalize_text(text: str) -> str:
    """Normaliza texto para comparación eliminando signos de puntuación y mayúsculas."""
    import re
    return re.sub(r'[^a-z0-9\s]', '', text.lower()).strip()

def _word_ngrams(text: str, n: int = 3) -> set:
    """Extrae n-gramas de palabras."""
    words = _normalize_text(text).split()
    if len(words) < n:
        return set([" ".join(words)]) if words else set()
    return set(" ".join(words[i:i+n]) for i in range(len(words) - n + 1))

def calculate_jaccard_similarity(text1: str, text2: str, n: int = 2) -> float:
    """Calcula similitud de Jaccard basada en 2-gramas de palabras."""
    ng1 = _word_ngrams(text1, n)
    ng2 = _word_ngrams(text2, n)
    if not ng1 or not ng2:
        return 0.0
    intersection = len(ng1.intersection(ng2))
    union = len(ng1.union(ng2))
    return float(intersection) / float(union) if union > 0 else 0.0


class ScriptHistoryManager:
    """Gestiona el almacenamiento y comprobación de guiones recientes."""

    def __init__(self, history_file: str = HISTORY_FILE, max_records: int = 30):
        self.history_file = history_file
        self.max_records = max_records
        os.makedirs(os.path.dirname(os.path.abspath(self.history_file)), exist_ok=True)

    def load_history(self) -> List[Dict]:
        if not os.path.exists(self.history_file):
            return []
        try:
            with open(self.history_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data if isinstance(data, list) else []
        except Exception as e:
            print(f"[HistoryManager] Error leyendo historial: {e}")
            return []

    def save_history(self, records: List[Dict]) -> None:
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                json.dump(records[-self.max_records:], f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[HistoryManager] Error guardando historial: {e}")

    def record_script(
        self,
        theme_key: str,
        hook: str,
        body: str,
        cta: str = "",
        scene_prompts: Optional[List[str]] = None
    ) -> None:
        """Registra un nuevo guion generado."""
        records = self.load_history()
        new_entry = {
            "timestamp": time.time(),
            "theme_key": theme_key,
            "hook": hook.strip(),
            "body_snippet": body.strip()[:350],
            "cta": cta.strip(),
            "prompts_snippet": " | ".join(scene_prompts or [])[:200]
        }
        records.append(new_entry)
        self.save_history(records)

    def is_similar_to_recent(
        self,
        hook: str,
        body: str = "",
        threshold: float = 0.60
    ) -> Tuple[bool, Optional[str]]:
        """
        Comprueba si el gancho o cuerpo propuesto es excesivamente similar a uno reciente.
        Retorna (es_similar, motivo)
        """
        records = self.load_history()
        # Evaluar los últimos 15 registros
        recent_records = records[-15:]
        for r in reversed(recent_records):
            prev_hook = r.get("hook", "")
            sim_hook = calculate_jaccard_similarity(hook, prev_hook)
            if sim_hook >= threshold:
                return True, f"Gancho similar ({sim_hook:.0%}) a uno reciente: '{prev_hook[:40]}...'"
            
            if body and r.get("body_snippet"):
                sim_body = calculate_jaccard_similarity(body[:300], r["body_snippet"][:300])
                if sim_body >= 0.50:
                    return True, f"Cuerpo similar ({sim_body:.0%}) a uno reciente."

        return False, None

    def get_recent_theme_keys(self, count: int = 5) -> List[str]:
        """Retorna las claves de temas utilizados en las últimas N generaciones."""
        records = self.load_history()
        return [r["theme_key"] for r in records[-count:] if "theme_key" in r]

    def clear_history(self) -> None:
        """Limpia el historial local."""
        self.save_history([])


_global_history_manager = ScriptHistoryManager()

def get_history_manager() -> ScriptHistoryManager:
    return _global_history_manager
