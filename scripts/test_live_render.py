import requests
import urllib3
urllib3.disable_warnings()

url = "https://132-145-202-1.sslip.io/api/render-video"
payload = {
    "hook": "The peace of God surpasses all understanding.",
    "body": "May His presence protect your household tonight and banish every fear.",
    "cta": "Type Amen and claim this promise for your home.",
    "voice_key": "adam",
    "subtitle_style": "karaoke",
    "camera_motion": "zoom_in"
}

print(f"Enviando solicitud de renderizado a {url}...")
res = requests.post(url, json=payload, verify=False, timeout=120)
print(f"Status Code: {res.status_code}")
try:
    print("Respuesta:", res.json())
except Exception:
    print("Respuesta texto:", res.text[:200])
