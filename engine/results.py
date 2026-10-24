"""
JESUSREELS STUDIO - EDITORIAL & EXPERIMENTAL RESULTS JOURNAL
Registro atómico, seguro y persistente de publicaciones y métricas experimentales
para FaithSpark Daily.
- Distingue rigurosamente valores ausentes (null) de ceros observados reales (0).
- Soporta grupos experimentales (A1, A2, A3, B1, B2, B3).
- Chequeos de métricas a las 48 horas y 7 días.
- Exportación a formato CSV y JSON.
"""

import json
import os
import csv
import io
import tempfile
import threading
import uuid
from datetime import datetime, timezone
from typing import Dict, List, Optional, Any

RESULTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "editorial_results.json")
_lock = threading.Lock()


def _read(path: Optional[str] = None) -> List[Dict[str, Any]]:
    target = path or RESULTS_FILE
    if not os.path.exists(target):
        return []
    try:
        with open(target, "r", encoding="utf-8") as stream:
            data = json.load(stream)
        if not isinstance(data, list):
            raise ValueError("El registro de resultados no es una lista válida.")
        return data
    except (json.JSONDecodeError, OSError):
        return []


def list_results(path: Optional[str] = None) -> List[Dict[str, Any]]:
    """Retorna la lista completa de publicaciones y sus observaciones."""
    with _lock:
        return _read(path or RESULTS_FILE)


def save_observation(payload: Dict[str, Any], path: Optional[str] = None) -> Dict[str, Any]:
    """
    Guarda una publicación y/o agrega una observación (48h / 7d) asegurando
    que los campos no medidos se almacenen como null y no como 0.
    """
    target = path or RESULTS_FILE
    with _lock:
        records = _read(target)
        record_id = payload.get("record_id")
        record = next((r for r in records if r["id"] == record_id), None) if record_id else None

        if record_id and record is None:
            raise KeyError("La publicación seleccionada no existe.")

        now = datetime.now(timezone.utc).isoformat()
        creative = payload.get("creative", {})

        # Si es un nuevo registro
        if record is None:
            rec_id = record_id or uuid.uuid4().hex
            exp_group = payload.get("experiment_group") or creative.get("experiment_group") or "A1"
            record = {
                "id": rec_id,
                "created_at": now,
                "experiment_group": exp_group,
                "creative": creative,
                "observations": []
            }
            records.append(record)
        else:
            # Actualizar grupo o creative si se envían datos más completos
            if payload.get("experiment_group"):
                record["experiment_group"] = payload["experiment_group"]

        # Procesar métricas preservando null vs 0 explícito
        raw_metrics = payload.get("metrics", {})
        cleaned_metrics = {}
        metric_keys = [
            "duration_sec", "views", "average_watch_sec", "average_watched_pct",
            "reactions", "comments", "shares", "followers", "us_viewer_pct", "main_dropoff_sec"
        ]

        for k in metric_keys:
            val = raw_metrics.get(k)
            if val is None or val == "" or val == "null":
                cleaned_metrics[k] = None
            else:
                try:
                    cleaned_metrics[k] = float(val) if "." in str(val) else int(val)
                except (ValueError, TypeError):
                    cleaned_metrics[k] = None

        checkpoint = payload.get("checkpoint", "48h")
        post_url = payload.get("post_url", "")
        if isinstance(post_url, str):
            post_url = post_url.strip()
        else:
            post_url = str(post_url or "")

        observation_entry = {
            "observed_at": now,
            "checkpoint": checkpoint,
            "metrics": cleaned_metrics,
            "post_url": post_url
        }

        record["observations"].append(observation_entry)

        # Escritura atómica
        directory = os.path.dirname(os.path.abspath(target))
        os.makedirs(directory, exist_ok=True)
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory, delete=False) as out:
                temp_path = out.name
                json.dump(records, out, indent=2, ensure_ascii=False)
            os.replace(temp_path, target)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)

        return record


def export_results_csv(path: Optional[str] = None) -> str:
    """
    Exporta el historial de experimentos a una cadena CSV estándar.
    Distingue métricas ausentes (campo vacío) de valores reales en 0.
    """
    records = list_results(path)
    output = io.StringIO()
    writer = csv.writer(output)

    # Encabezados
    headers = [
        "reel_id", "created_at", "experiment_group", "theme_key", "caption_type",
        "duration_sec", "voice", "checkpoint", "observed_at", "views",
        "average_watch_sec", "average_watched_pct", "reactions", "comments",
        "shares", "followers", "us_viewer_pct", "post_url", "hook", "caption"
    ]
    writer.writerow(headers)

    for rec in records:
        r_id = rec.get("id", "")
        created_at = rec.get("created_at", "")
        exp_group = rec.get("experiment_group", "")
        creative = rec.get("creative", {})
        theme_key = creative.get("theme_key", "")
        caption_type = creative.get("caption_type", "")
        voice = creative.get("voice", "")
        hook = creative.get("hook", "")
        caption = creative.get("caption", "")

        observations = rec.get("observations", [])
        if not observations:
            # Escribir fila base sin observaciones aún
            writer.writerow([
                r_id, created_at, exp_group, theme_key, caption_type,
                "", voice, "none", "", "", "", "", "", "", "", "", "", "", hook, caption
            ])
        else:
            for obs in observations:
                chk = obs.get("checkpoint", "")
                obs_at = obs.get("observed_at", "")
                p_url = obs.get("post_url", "")
                m = obs.get("metrics", {})

                def fmt_val(v):
                    return "" if v is None else str(v)

                writer.writerow([
                    r_id,
                    created_at,
                    exp_group,
                    theme_key,
                    caption_type,
                    fmt_val(m.get("duration_sec")),
                    voice,
                    chk,
                    obs_at,
                    fmt_val(m.get("views")),
                    fmt_val(m.get("average_watch_sec")),
                    fmt_val(m.get("average_watched_pct")),
                    fmt_val(m.get("reactions")),
                    fmt_val(m.get("comments")),
                    fmt_val(m.get("shares")),
                    fmt_val(m.get("followers")),
                    fmt_val(m.get("us_viewer_pct")),
                    p_url,
                    hook,
                    caption
                ])

    return output.getvalue()


def export_results_json(path: Optional[str] = None) -> str:
    """Exporta el historial completo formateado en JSON indentado."""
    records = list_results(path)
    return json.dumps(records, indent=2, ensure_ascii=False)
