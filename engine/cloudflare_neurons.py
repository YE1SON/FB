import os
import json
import time
from datetime import datetime, timezone
from typing import Dict, Any, Tuple, Optional

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
USAGE_FILE = os.path.join(DATA_DIR, "cloudflare_neurons.json")
os.makedirs(DATA_DIR, exist_ok=True)

# Límite gratuito diario de Neuronas en Cloudflare Workers AI (10,000 / día)
DEFAULT_DAILY_LIMIT = 10000.0

# Estimación oficial de Neuronas por inferencia (1 Megapixel ~768x1360)
MODEL_NEURON_RATES = {
    "@cf/black-forest-labs/flux-2-klein-9b": {
        "name": "FLUX.2 Klein 9B",
        "base_neurons": 1364.0,
        "ref_input_neurons": 182.0
    },
    "@cf/black-forest-labs/flux-2-klein-4b": {
        "name": "FLUX.2 Klein 4B",
        "base_neurons": 104.2,
        "ref_input_neurons": 21.5
    }
}


def _get_utc_today() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def load_neurons_data() -> Dict[str, Any]:
    """Carga los registros de consumo de neuronas desde el archivo persistente."""
    today = _get_utc_today()
    default_payload = {
        "date": today,
        "daily_limit": DEFAULT_DAILY_LIMIT,
        "consumed": 0.0,
        "generations_today": 0,
        "history": []
    }
    if not os.path.exists(USAGE_FILE):
        return default_payload

    try:
        with open(USAGE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Si cambió el día en UTC, reiniciar el contador diario automáticamente
        if data.get("date") != today:
            data["date"] = today
            data["consumed"] = 0.0
            data["generations_today"] = 0
            data["history"] = []
            save_neurons_data(data)
        return data
    except Exception as e:
        print(f"[Neurons Tracker] Error al leer {USAGE_FILE}: {e}")
        return default_payload


def save_neurons_data(data: Dict[str, Any]) -> None:
    """Guarda de forma atómica el estado de consumo de neuronas."""
    tmp_path = f"{USAGE_FILE}.tmp.{os.getpid()}"
    try:
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp_path, USAGE_FILE)
    except Exception as e:
        print(f"[Neurons Tracker] Error al guardar {USAGE_FILE}: {e}")
        if os.path.exists(tmp_path):
            try:
                os.remove(tmp_path)
            except OSError:
                pass


def estimate_neurons(model_name: str, has_reference: bool = False) -> float:
    """Calcula el costo estimado en neuronas para una inferencia con el modelo dado."""
    model_info = MODEL_NEURON_RATES.get(model_name)
    if not model_info:
        # Fallback conservador para modelos 9B / 4B no mapeados
        if "9b" in model_name.lower():
            base = 1364.0
            ref = 182.0
        else:
            base = 104.2
            ref = 21.5
    else:
        base = model_info["base_neurons"]
        ref = model_info["ref_input_neurons"]

    return base + (ref if has_reference else 0.0)


def check_quota_available(model_name: str, has_reference: bool = False) -> Tuple[bool, str, float]:
    """
    Comprueba si hay neuronas suficientes en la cuota diaria gratuita.
    Retorna (permitido, mensaje_explicativo, neuronas_estimadas).
    """
    data = load_neurons_data()
    consumed = float(data.get("consumed", 0.0))
    limit = float(data.get("daily_limit", DEFAULT_DAILY_LIMIT))
    needed = estimate_neurons(model_name, has_reference)

    if consumed + needed > limit:
        remaining = max(0.0, limit - consumed)
        msg = (
            f"Cuota diaria gratuita de Neuronas alcanzada en Cloudflare Workers AI. "
            f"Consumido hoy: {consumed:,.0f} de {limit:,.0f} neuronas. "
            f"La generación requiere ~{needed:,.0f} neuronas pero solo quedan {remaining:,.0f}. "
            f"Para evitar cobros automáticos en tu cuenta, la generación se ha pausado hasta el reinicio diario UTC (00:00 UTC)."
        )
        return False, msg, needed

    return True, "Cuota disponible", needed


def record_neurons_consumption(
    model_name: str,
    scene_num: int,
    has_reference: bool = False,
    prompt_preview: str = ""
) -> Dict[str, Any]:
    """Registra la inferencia ejecutada exitosamente y suma su consumo a la cuota."""
    data = load_neurons_data()
    needed = estimate_neurons(model_name, has_reference)
    data["consumed"] = round(float(data.get("consumed", 0.0)) + needed, 2)
    data["generations_today"] = int(data.get("generations_today", 0)) + 1

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model": model_name,
        "scene_num": scene_num,
        "has_reference": has_reference,
        "neurons_charged": needed,
        "prompt_preview": prompt_preview[:80]
    }
    history = data.get("history", [])
    history.append(entry)
    data["history"] = history[-30:]  # Mantener últimos 30 registros
    save_neurons_data(data)
    return data


def get_neurons_status() -> Dict[str, Any]:
    """Retorna un resumen estructurado para la interfaz y la API."""
    data = load_neurons_data()
    consumed = float(data.get("consumed", 0.0))
    limit = float(data.get("daily_limit", DEFAULT_DAILY_LIMIT))
    remaining = max(0.0, limit - consumed)
    pct = min(100.0, round((consumed / limit) * 100.0, 1)) if limit > 0 else 100.0

    # Estimación de Reels completos restantes en modo Auto (1x 9B + 2x 4B = ~1,572 neuronas)
    auto_reel_cost = estimate_neurons("@cf/black-forest-labs/flux-2-klein-9b") + (estimate_neurons("@cf/black-forest-labs/flux-2-klein-4b", True) * 2)
    reels_remaining = int(remaining // auto_reel_cost)

    return {
        "date_utc": data.get("date", _get_utc_today()),
        "consumed_neurons": consumed,
        "daily_limit": limit,
        "remaining_neurons": remaining,
        "percent_used": pct,
        "generations_today": data.get("generations_today", 0),
        "reels_remaining_approx": reels_remaining,
        "is_exhausted": consumed >= limit,
        "auto_reel_cost": round(auto_reel_cost, 1)
    }


def reset_daily_neurons() -> Dict[str, Any]:
    """Permite reiniciar manualmente el contador diario."""
    today = _get_utc_today()
    payload = {
        "date": today,
        "daily_limit": DEFAULT_DAILY_LIMIT,
        "consumed": 0.0,
        "generations_today": 0,
        "history": []
    }
    save_neurons_data(payload)
    return get_neurons_status()
