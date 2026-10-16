import os
import sys
import uuid
import shutil
import io
import random
import urllib.request
import urllib.parse
from PIL import Image
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.scripts import generate_script, get_themes_list, generate_image_prompt_for_script, VIRAL_THEMES
from engine.tts import synthesize_speech, get_available_voices, VOICES, LEGACY_VOICE_MAP
from engine.subtitles import generate_viral_ass, SUBTITLE_STYLES
from engine.video import render_reel, WORSHIP_TRACKS

ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="JesusReels Studio", version="4.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static and assets folders
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")

IMAGE_METADATA = {
    "jesus_healing_miracle.jpg": "🕊️ Jesús Sanando a un Quebrantado",
    "jesus_reaching_hand.jpg": "🌊 Jesús Rescatando en la Tormenta",
    "jesus_praying_gethsemane.jpg": "🌌 Jesús Orando en Getsemaní",
    "jesus_comforting_embrace.jpg": "🫂 Jesús Abrazando y Secando Lágrimas",
    "holy_cross_calvary.jpg": "✝️ La Santa Cruz en el Calvario",
    "jesus_holy_bible.jpg": "📖 Jesús con la Santa Biblia Iluminada"
}

class ScriptRequest(BaseModel):
    theme_key: Optional[str] = None
    custom_topic: Optional[str] = None
    mode: str = "deep"

class ImagePromptRequest(BaseModel):
    theme_key: Optional[str] = None
    script_text: str = ""
    custom_topic: Optional[str] = None

class GenerateAiImageRequest(BaseModel):
    prompt: str
    aspect_ratio: str = "9:16"

class AudioPreviewRequest(BaseModel):
    text: str
    voice_key: str = "christopher"
    rate: str = "+0%"

class RenderRequest(BaseModel):
    hook: str
    body: str
    cta: str
    voice_key: str = "christopher"
    rate: str = "+0%"
    image_name: str = "jesus_healing_miracle.jpg"
    image_name_2: Optional[str] = None
    subtitle_style: str = "gold_highlight"
    subtitle_size: str = "normal"
    subtitle_animation: str = "pop"
    subtitle_position: str = "bottom"
    music_track: str = "worship_piano_peace"
    music_volume: float = 0.20
    aspect_ratio: str = "9:16"
    effect_type: str = "cinematic_dust"
    camera_motion: str = "none"
    hook_text: str = ""


# ─── Worship Tracks ──────────────────────────────────────────────────────────

@app.get("/api/worship-tracks")
@app.get("/studio/api/worship-tracks")
def list_worship_tracks():
    return [
        {"key": k, "name": v}
        for k, v in WORSHIP_TRACKS.items()
    ]


# ─── Health & Index ──────────────────────────────────────────────────────────

@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": "JesusReels Studio",
        "version": "4.0.0"
    }

@app.get("/")
@app.get("/app-view")
def serve_index():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


# ─── Themes & Scripts ────────────────────────────────────────────────────────

@app.get("/api/themes")
@app.get("/studio/api/themes")
def list_themes():
    return get_themes_list()

@app.post("/api/generate-script")
@app.post("/studio/api/generate-script")
def api_generate_script(req: ScriptRequest):
    return generate_script(req.theme_key, req.custom_topic, mode=req.mode)

@app.post("/api/generate-image-prompt")
@app.post("/studio/api/generate-image-prompt")
def api_generate_image_prompt(req: ImagePromptRequest):
    prompt = generate_image_prompt_for_script(req.theme_key, req.script_text, req.custom_topic)
    return {"prompt": prompt}


# ─── Voices & Subtitles ─────────────────────────────────────────────────────

@app.get("/api/voices")
@app.get("/studio/api/voices")
def list_voices():
    return get_available_voices()

@app.get("/api/subtitle-styles")
@app.get("/studio/api/subtitle-styles")
def list_subtitle_styles():
    return [
        {"key": k, "name": v["name"], "font": v["font"]}
        for k, v in SUBTITLE_STYLES.items()
    ]


# ─── Images ─────────────────────────────────────────────────────────────────

@app.get("/api/images")
@app.get("/studio/api/images")
def list_images():
    files = [
        f for f in os.listdir(ASSETS_DIR)
        if f.lower().endswith((".jpg", ".jpeg", ".png", ".webp"))
    ]
    files.sort(key=lambda x: (0 if x in IMAGE_METADATA else 1, x))
    return [
        {
            "filename": f,
            "url": f"/assets/images/{f}",
            "label": IMAGE_METADATA.get(f, f"Personalizada ({f[:15]}...)"),
            "deletable": f not in IMAGE_METADATA
        }
        for f in files
    ]

@app.delete("/api/images/{filename}")
@app.delete("/studio/api/images/{filename}")
def delete_image(filename: str):
    filename = os.path.basename(filename)
    filepath = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Imagen no encontrada.")
    if filename in IMAGE_METADATA:
        raise HTTPException(status_code=400, detail="No se pueden eliminar las 6 imágenes plantilla predeterminadas.")
    try:
        os.remove(filepath)
        return {"status": "success", "deleted": filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo eliminar la imagen: {str(e)}")

@app.post("/api/upload-image")
@app.post("/studio/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    filename = f"custom_{uuid.uuid4().hex[:8]}_{file.filename}"
    filepath = os.path.join(ASSETS_DIR, filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"filename": filename, "url": f"/assets/images/{filename}", "label": "Tu Imagen Subida", "deletable": True}

@app.post("/api/generate-ai-image")
@app.post("/studio/api/generate-ai-image")
def api_generate_ai_image(req: GenerateAiImageRequest):
    prompt = req.prompt.strip()
    if not prompt:
        raise HTTPException(status_code=400, detail="El prompt no puede estar vacío.")

    enhanced_prompt = prompt
    if "cinematic" not in enhanced_prompt.lower() and "masterpiece" not in enhanced_prompt.lower():
        enhanced_prompt = f"Ultra-realistic cinematic 8k portrait of {prompt}, warm divine golden hour lighting, sacred holy atmosphere, highly detailed, dramatic, majestic, octane render, masterpiece, award winning photography, sharp focus"

    # Map aspect ratio to dimensions
    width, height = 768, 1344
    if req.aspect_ratio == "1:1":
        width, height = 1024, 1024
    elif req.aspect_ratio == "16:9":
        width, height = 1344, 768

    seed = random.randint(100000, 999999)
    encoded_prompt = urllib.parse.quote(enhanced_prompt)
    url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model=flux&nologo=true&seed={seed}"

    filename = f"custom_flux_{uuid.uuid4().hex[:8]}.jpg"
    filepath = os.path.join(ASSETS_DIR, filename)

    try:
        req_obj = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
        )
        with urllib.request.urlopen(req_obj, timeout=60) as resp:
            content_type = resp.headers.get("Content-Type", "")
            data = resp.read()
            if "image" not in content_type and len(data) < 2000:
                raise RuntimeError(f"Respuesta no válida del proveedor: {data.decode(errors='replace')[:200]}")
            with open(filepath, "wb") as f:
                f.write(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo al generar imagen con Flux AI: {str(e)}")

    return {
        "status": "success",
        "filename": filename,
        "url": f"/assets/images/{filename}",
        "label": "IA Flux HD",
        "deletable": True
    }


# ─── Audio Preview ──────────────────────────────────────────────────────────

@app.post("/api/preview-audio")
@app.post("/studio/api/preview-audio")
async def preview_audio(req: AudioPreviewRequest):
    if not req.text.strip():
        raise HTTPException(status_code=400, detail="El texto no puede estar vacío.")

    voice_key = LEGACY_VOICE_MAP.get(req.voice_key, req.voice_key)
    voice_info = VOICES.get(voice_key, VOICES.get("adam", list(VOICES.values())[0]))
    audio_id = f"preview_{uuid.uuid4().hex[:8]}.mp3"
    audio_path = os.path.join(OUTPUTS_DIR, audio_id)

    await synthesize_speech(req.text, voice_info["id"], audio_path, rate=req.rate)
    return {"audio_url": f"/outputs/{audio_id}"}


# ─── VIDEO RENDER (Main Endpoint) ───────────────────────────────────────────

@app.post("/api/render-video")
@app.post("/studio/api/render-video")
async def api_render_video(req: RenderRequest):
    full_text = f"{req.hook.strip()} {req.body.strip()} {req.cta.strip()}"
    if not full_text.strip():
        raise HTTPException(status_code=400, detail="El guion no puede estar vacío.")

    session_id = uuid.uuid4().hex[:8]
    audio_file = os.path.join(OUTPUTS_DIR, f"{session_id}_audio.mp3")
    ass_file = os.path.join(OUTPUTS_DIR, f"{session_id}_subs.ass")
    output_video = os.path.join(OUTPUTS_DIR, f"reel_{session_id}.mp4")

    try:
        # 1. Synthesize TTS audio
        voice_key = LEGACY_VOICE_MAP.get(req.voice_key, req.voice_key)
        voice_info = VOICES.get(voice_key, VOICES.get("adam", list(VOICES.values())[0]))
        cues = await synthesize_speech(full_text, voice_info["id"], audio_file, rate=req.rate)

        # 2. Generate ASS subtitles & Embedded Particles
        margin_v = 400 if req.subtitle_size == "large" else 450
        play_w = 1080
        play_h = 1920
        if req.aspect_ratio == "1:1":
            margin_v = 150
            play_w, play_h = 1080, 1080
        elif req.aspect_ratio == "16:9":
            margin_v = 100
            play_w, play_h = 1920, 1080

        generate_viral_ass(
            cues, ass_file,
            style_key=req.subtitle_style,
            margin_v=margin_v,
            hook_text=req.hook_text,
            animation_type=req.subtitle_animation,
            position=req.subtitle_position,
            effect_type=req.effect_type,
            play_res_x=play_w,
            play_res_y=play_h
        )

        # 3. Render video (Micro-Motion Engine with smart fit, camera choice & dual scene)
        image_file = _resolve_image(req.image_name)
        image_file_2 = None
        if req.image_name_2 and req.image_name_2 not in ["none", ""]:
            cand2 = os.path.join(ASSETS_DIR, os.path.basename(req.image_name_2))
            if os.path.exists(cand2):
                image_file_2 = cand2

        render_reel(
            image_file, audio_file, ass_file, output_video,
            aspect_ratio=req.aspect_ratio,
            effect_type=req.effect_type,
            camera_motion=req.camera_motion,
            music_track=req.music_track,
            music_volume=req.music_volume,
            image_path_2=image_file_2
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = str(e) or "Error desconocido en el servidor."
        print(f"[RENDER ERROR] session={session_id}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Fallo al renderizar: {error_detail}")

    return {
        "status": "success",
        "video_url": f"/outputs/reel_{session_id}.mp4",
        "filename": f"reel_{session_id}.mp4"
    }


def _resolve_image(image_name: str) -> str:
    image_file = os.path.join(ASSETS_DIR, image_name)
    if not os.path.exists(image_file):
        avail = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        if avail:
            image_file = os.path.join(ASSETS_DIR, avail[0])
        else:
            raise HTTPException(status_code=400, detail="No hay imágenes disponibles.")
    return image_file


# ─── Outputs ────────────────────────────────────────────────────────────────

@app.get("/api/outputs")
@app.get("/studio/api/outputs")
def list_outputs():
    files = [
        f for f in os.listdir(OUTPUTS_DIR)
        if f.lower().endswith(".mp4")
    ]
    files.sort(key=lambda f: os.path.getmtime(os.path.join(OUTPUTS_DIR, f)), reverse=True)
    return [{"filename": f, "url": f"/outputs/{f}"} for f in files]


# ─── Daily Batch Schedule & Magnetic Engagement ─────────────────────────────

MAGNETIC_COMMENTS = [
    "👇 God sees your exact situation today. Drop your first name below so our community can agree in prayer over your home tonight! Say 'I receive it' 🙏",
    "👇 A praying family breaks every chain. Type the first name or initial of your child/loved one and claim: 'They are protected in Jesus' name!' ❤️",
    "👇 Sickness does not have the final say. Drop your name below and declare: 'By His stripes I am healed!' 🕊️",
    "👇 If you woke up carrying fear or anxiety, breathe. Leave a '🙏' below and let us carry this burden in prayer with you right now.",
    "👇 Drop your first name below to stand in agreement for a financial miracle before this week ends. Type AMEN! 💸",
    "👇 Comment 'THANK YOU JESUS' and leave one thing you are grateful for today so we can rejoice together! 🙌"
]

@app.get("/api/magnetic-comments")
@app.get("/studio/api/magnetic-comments")
def api_magnetic_comments():
    return MAGNETIC_COMMENTS

@app.get("/api/daily-batch")
@app.get("/studio/api/daily-batch")
def api_daily_batch():
    return [
        {
            "slot": "morning",
            "time_label": "🌅 Mañana (7:00 AM - 8:30 AM EST)",
            "purpose": "Apertura de Bendición, Favor y Gratitud",
            "script": generate_script("morning_favor", mode="deep"),
            "recommended_image": "jesus_praying_gethsemane.jpg",
            "recommended_music": "celestial_strings_hope"
        },
        {
            "slot": "midday",
            "time_label": "☀️ Mediodía (12:30 PM - 2:00 PM EST)",
            "purpose": "Paz Mental, Sanidad y Superación de Cargas",
            "script": generate_script("medical_fear", mode="deep"),
            "recommended_image": "jesus_healing_miracle.jpg",
            "recommended_music": "worship_piano_peace"
        },
        {
            "slot": "night",
            "time_label": "🌙 Noche (8:30 PM - 10:00 PM EST)",
            "purpose": "Milagro Financiero, Familia y Reposo",
            "script": generate_script("zero_balance", mode="deep"),
            "recommended_image": "jesus_comforting_embrace.jpg",
            "recommended_music": "midnight_prayer_acoustic"
        }
    ]


if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8050"))
    print("\n=======================================================")
    print(f"  JESUS REELS STUDIO v4.0 — http://{host}:{port}")
    print("=======================================================\n")
    uvicorn.run("server:app", host=host, port=port, reload=False)
