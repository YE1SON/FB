"""Small atomic JSON journal for manually entered aggregate post results."""
import json
import os
import tempfile
import threading
import uuid
from datetime import datetime, timezone

RESULTS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "editorial_results.json")
_lock = threading.Lock()


def _read(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as stream:
        data = json.load(stream)
    if not isinstance(data, list):
        raise ValueError("El registro de resultados no es una lista válida.")
    return data


def list_results(path=None):
    with _lock:
        return _read(path or RESULTS_FILE)


def save_observation(payload, path=None):
    path = path or RESULTS_FILE
    with _lock:
        records = _read(path)
        record_id = payload.get("record_id")
        record = next((r for r in records if r["id"] == record_id), None)
        if record_id and record is None:
            raise KeyError("La publicación seleccionada no existe.")
        now = datetime.now(timezone.utc).isoformat()
        if record is None:
            record = {"id": uuid.uuid4().hex, "created_at": now,
                      "creative": payload["creative"], "observations": []}
            records.append(record)
        record["observations"].append({"observed_at": now, "checkpoint": payload["checkpoint"],
                                       "metrics": payload["metrics"], "post_url": payload.get("post_url", "")})
        directory = os.path.dirname(os.path.abspath(path))
        os.makedirs(directory, exist_ok=True)
        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=directory, delete=False) as out:
                temp_path = out.name
                json.dump(records, out, indent=2, ensure_ascii=False)
            os.replace(temp_path, path)
        finally:
            if temp_path and os.path.exists(temp_path):
                os.unlink(temp_path)
        return record
