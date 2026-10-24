import os
import sys
import uuid
import shutil
import io
import random
import urllib.request
import urllib.parse
from PIL import Image
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, HttpUrl
from fastapi import FastAPI, HTTPException, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, PlainTextResponse, Response

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from engine.scripts import generate_script, get_themes_list, generate_image_prompt_for_script, generate_3scene_prompts_for_script, get_card_template_for_theme, get_daily_batch_schedule, VIRAL_THEMES
from engine.tts import synthesize_speech, get_available_voices, VOICES, LEGACY_VOICE_MAP, check_engine_availability
from engine.subtitles import generate_viral_ass, SUBTITLE_STYLES
from engine.video import render_reel, WORSHIP_TRACKS, get_audio_duration
from engine.image_cards import create_prayer_card_4_5
from engine.broll import get_broll_status, get_broll_clip
from engine.image_gen import generate_ai_scene_image, get_providers_status, save_keys, load_keys


ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
CARDS_DIR = os.path.join(OUTPUTS_DIR, "cards")
STATIC_DIR = os.path.join(BASE_DIR, "static")

os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(CARDS_DIR, exist_ok=True)
os.makedirs(STATIC_DIR, exist_ok=True)

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="JesusReels Studio", version="4.0.0")

env_origins = os.environ.get("ALLOWED_ORIGINS", "").strip()
if env_origins:
    allowed_origins = [o.strip() for o in env_origins.split(",") if o.strip()]
else:
    allowed_origins = [
        "http://localhost:8050",
        "http://127.0.0.1:8050",
        "http://localhost:3000",
        "https://132-145-202-1.sslip.io",
        "http://132-145-202-1.sslip.io"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Mount static, assets and cards output folders
# ─── Disable Browser Cache for Static Assets ─────────────────────────────────
@app.middleware("http")
async def add_no_cache_for_static(request: Request, call_next):
    response = await call_next(request)
    if request.url.path.startswith("/static/"):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/assets", StaticFiles(directory=os.path.join(BASE_DIR, "assets")), name="assets")
app.mount("/outputs/cards", StaticFiles(directory=CARDS_DIR), name="outputs_cards")
app.mount("/output/cards", StaticFiles(directory=CARDS_DIR), name="output_cards")
app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="outputs")

IMAGE_METADATA = {
    "jesus_healing_miracle.jpg": "🕊️ Jesús Sanando a un Quebrantado",
    "jesus_reaching_hand.jpg": "🌊 Jesús Rescatando en la Tormenta",
    "jesus_praying_gethsemane.jpg": "🌌 Jesús Orando en Getsemaní",
    "jesus_comforting_embrace.jpg": "🫂 Jesús Abrazando y Secando Lágrimas",
    "holy_cross_calvary.jpg": "✝️ La Santa Cruz en el Calvario",
    "jesus_holy_bible.jpg": "📖 Jesús con la Santa Biblia Iluminada"
}

class EditorialBrief(BaseModel):
    series_key: Literal["everyday", "quiet"] = "everyday"
    audience: str = Field(default="US adults", max_length=180)
    situation: str = Field(default="", max_length=500)
    central_idea: str = Field(default="", max_length=500)
    format: Literal["prayer", "reflection", "story"] = "prayer"
    target_duration_sec: float = Field(default=22, ge=12, le=60)
    include_cta: bool = False

class ScriptRequest(BaseModel):
    theme_key: Optional[str] = None
    custom_topic: Optional[str] = None
    mode: str = "deep"
    seamless_loop: Optional[bool] = False
    brief: Optional[EditorialBrief] = None

class EditorialReviewRequest(BaseModel):
    hook: str = Field(default="", max_length=1000)
    body: str = Field(default="", max_length=10000)
    cta: str = Field(default="", max_length=1000)
    caption: str = Field(default="", max_length=10000)
    target: float = Field(default=22, ge=12, le=60)

class CreativeSnapshot(BaseModel):
    theme_key: str = Field(max_length=80)
    series_key: str = Field(default="", max_length=80)
    format: str = Field(default="", max_length=80)
    hook: str = Field(max_length=1000)
    body: str = Field(default="", max_length=10000)
    cta: str = Field(default="", max_length=1000)
    caption: str = Field(default="", max_length=10000)
    voice: str = Field(default="", max_length=80)
    provider: str = Field(default="", max_length=160)
    opening_variant: int = Field(default=0, ge=0, le=2)
    experiment_group: Optional[str] = Field(default="A1", max_length=10)
    caption_type: Optional[str] = Field(default="short", max_length=20)
    hashtags: Optional[List[str]] = Field(default_factory=list)

class ObservedMetrics(BaseModel):
    duration_sec: Optional[float] = Field(default=None, gt=0)
    views: Optional[int] = Field(default=None, ge=0)
    average_watch_sec: Optional[float] = Field(default=None, ge=0)
    average_watched_pct: Optional[float] = Field(default=None, ge=0)
    reactions: Optional[int] = Field(default=None, ge=0)
    comments: Optional[int] = Field(default=None, ge=0)
    followers: Optional[int] = Field(default=None, ge=0)
    shares: Optional[int] = Field(default=None, ge=0)
    us_viewer_pct: Optional[float] = Field(default=None, ge=0, le=100)
    main_dropoff_sec: Optional[float] = Field(default=None, ge=0)

class ObservationRequest(BaseModel):
    record_id: Optional[str] = Field(default=None, max_length=40)
    creative: CreativeSnapshot
    checkpoint: Literal["48h", "7d", "other"] = "48h"
    post_url: Optional[str] = None
    metrics: ObservedMetrics

class GenerateOptimizedCaptionRequest(BaseModel):
    theme_key: str
    hook: str
    body: str
    scripture: Optional[str] = ""
    cta: Optional[str] = ""
    format_type: str = "A"
    hashtag_strategy: int = 3
    custom_tags: Optional[List[str]] = None

class ValidatePostReadinessRequest(BaseModel):
    theme_key: str
    script_hook: str
    script_body: str
    script_cta: Optional[str] = ""
    caption_text: str
    scripture_text: Optional[str] = ""
    caption_source_hook: Optional[str] = None
    caption_source_body: Optional[str] = None

class ImagePromptRequest(BaseModel):
    theme_key: Optional[str] = None
    script_text: str = ""
    custom_topic: Optional[str] = None

class SaveKeysRequest(BaseModel):
    hf_token: Optional[str] = None
    aihorde_api_key: Optional[str] = None

class GenerateAiImageRequest(BaseModel):
    prompt: str
    aspect_ratio: str = "9:16"
    provider: str = "auto"
    hf_token: Optional[str] = None
    aihorde_api_key: Optional[str] = None
    scene_num: int = 1
    used_images: Optional[List[str]] = None

class BatchGenerateAiImageRequest(BaseModel):
    prompts: List[str]
    aspect_ratio: str = "9:16"
    provider: str = "auto"
    hf_token: Optional[str] = None
    aihorde_api_key: Optional[str] = None

class AudioPreviewRequest(BaseModel):
    text: str
    voice_key: str = "christopher"
    rate: str = "+0%"

class RenderRequest(BaseModel):
    hook: str
    body: str
    cta: str = ""
    theme_key: Optional[str] = "morning_favor"
    voice_key: str = "guy"
    rate: str = "-6%"
    video_mode: str = "images"  # "images" or "broll"
    image_name: str = "jesus_healing_miracle.jpg"
    image_name_2: Optional[str] = None
    image_name_3: Optional[str] = None
    subtitle_style: str = "clean"
    subtitle_size: str = "normal"
    subtitle_animation: str = "pop"
    subtitle_position: str = "bottom"
    all_caps: Optional[bool] = False
    enable_hook_badge: bool = False
    enable_micro_cta: bool = False
    music_track: str = "worship_piano_peace"
    music_volume: float = 0.20
    aspect_ratio: str = "9:16"
    effect_type: str = "none"
    camera_motion: str = "zoom_in"
    transition_style: Optional[str] = "fade"
    hook_text: str = ""
    hook_badge_style: Optional[str] = "gold_luxury"
    hook_badge_font: Optional[str] = "Montserrat"
    hook_badge_size: Optional[str] = "normal"
    micro_cta_text: Optional[str] = ""
    enable_sfx: Optional[bool] = False
    seamless_loop: Optional[bool] = False
    master_lufs: Optional[bool] = True
    generate_trending_audio: Optional[bool] = False
    target_duration_sec: Optional[float] = None
    duration_mode: Optional[str] = "deep"

class ImageCardRequest(BaseModel):
    background_image_path: str
    title: str
    prayer_text: str
    verse_footer: str = ""
    watermark_text: Optional[str] = ""


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
    return generate_script(req.theme_key, req.custom_topic, mode=req.mode, seamless_loop=bool(req.seamless_loop),
                           brief=req.brief.model_dump() if req.brief else None)

@app.get("/api/editorial-config")
@app.get("/studio/api/editorial-config")
def editorial_config():
    from engine.editorial import SERIES
    return {"series": SERIES, "primary_voices": ["guy", "christopher"]}

@app.post("/api/editorial-review")
@app.post("/studio/api/editorial-review")
def editorial_review(req: EditorialReviewRequest):
    from engine.editorial import review_script
    return review_script(**req.model_dump())

@app.get("/api/editorial-results")
@app.get("/studio/api/editorial-results")
def editorial_results():
    from engine.results import list_results
    return list_results()

@app.post("/api/editorial-results")
@app.post("/studio/api/editorial-results")
def record_editorial_results(req: ObservationRequest):
    from engine.results import save_observation
    payload = req.model_dump(mode="json")
    if not req.record_id and not req.creative.hook.strip():
        raise HTTPException(status_code=422, detail="Genera o escribe una apertura antes de registrar la publicación.")
    try:
        return save_observation(payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

@app.post("/api/editorial-caption")
@app.post("/studio/api/editorial-caption")
def api_generate_editorial_caption(req: GenerateOptimizedCaptionRequest):
    from engine.editorial_captions import generate_optimized_social_post
    return generate_optimized_social_post(
        theme_key=req.theme_key,
        hook=req.hook,
        body=req.body,
        scripture=req.scripture or "",
        cta=req.cta or "",
        format_type=req.format_type,
        hashtag_strategy=req.hashtag_strategy,
        custom_tags=req.custom_tags
    )

@app.post("/api/editorial-validate")
@app.post("/studio/api/editorial-validate")
def api_validate_editorial_post(req: ValidatePostReadinessRequest):
    from engine.editorial_validator import validate_post_readiness
    from engine.results import list_results
    records = list_results()
    recent_captions = [r.get("creative", {}).get("caption", "") for r in records[-10:] if r.get("creative", {}).get("caption")]
    return validate_post_readiness(
        theme_key=req.theme_key,
        script_hook=req.script_hook,
        script_body=req.script_body,
        script_cta=req.script_cta or "",
        caption_text=req.caption_text,
        scripture_text=req.scripture_text or "",
        recent_captions=recent_captions,
        caption_source_hook=req.caption_source_hook,
        caption_source_body=req.caption_source_body
    )

@app.get("/api/editorial-experiment-matrix")
@app.get("/studio/api/editorial-experiment-matrix")
def api_get_experiment_matrix():
    from engine.editorial_captions import EXPERIMENT_MATRIX_18, get_next_recommended_experiment
    from engine.results import list_results
    records = list_results()
    next_slot = get_next_recommended_experiment(records)
    return {
        "matrix": EXPERIMENT_MATRIX_18,
        "total_recorded": len(records),
        "next_slot": next_slot
    }

@app.get("/api/editorial-results/export/csv")
@app.get("/studio/api/editorial-results/export/csv")
def api_export_results_csv():
    from engine.results import export_results_csv
    csv_data = export_results_csv()
    return PlainTextResponse(
        content=csv_data,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="faithspark_experiment_results.csv"'}
    )

@app.get("/api/editorial-results/export/json")
@app.get("/studio/api/editorial-results/export/json")
def api_export_results_json():
    from engine.results import export_results_json
    json_data = export_results_json()
    return Response(
        content=json_data,
        media_type="application/json",
        headers={"Content-Disposition": 'attachment; filename="faithspark_experiment_results.json"'}
    )

@app.post("/api/generate-image-prompt")
@app.post("/studio/api/generate-image-prompt")
def api_generate_image_prompt(req: ImagePromptRequest):
    prompts = generate_3scene_prompts_for_script(req.theme_key, req.script_text, req.custom_topic)
    return {
        "prompt": prompts["scene_1_prompt"],
        "scene_1_prompt": prompts["scene_1_prompt"],
        "scene_2_prompt": prompts["scene_2_prompt"],
        "scene_3_prompt": prompts["scene_3_prompt"]
    }



# ─── Voices & Subtitles ─────────────────────────────────────────────────────

@app.get("/api/voices")
@app.get("/studio/api/voices")
def list_voices():
    return get_available_voices()

@app.get("/api/tts-status")
@app.get("/studio/api/tts-status")
def api_tts_status():
    return check_engine_availability()

@app.get("/api/voices/preview/{voice_id}")
@app.get("/studio/api/voices/preview/{voice_id}")
async def api_voice_sample(voice_id: str):
    voice_key = LEGACY_VOICE_MAP.get(voice_id, voice_id)
    voice_info = VOICES.get(voice_key, VOICES.get("adam", list(VOICES.values())[0]))
    audio_id = f"sample_{voice_key}.mp3"
    audio_path = os.path.join(OUTPUTS_DIR, audio_id)
    sample_text = "The Lord is my shepherd, I shall not want. Peace and grace be with you."
    if not os.path.exists(audio_path):
        await synthesize_speech(sample_text, voice_info["id"], audio_path, rate="+0%")
    return {"audio_url": f"/outputs/{audio_id}"}

@app.get("/api/subtitle-styles")
@app.get("/studio/api/subtitle-styles")
def list_subtitle_styles():
    return [
        {"key": k, "name": v["name"], "font": v["font"]}
        for k, v in SUBTITLE_STYLES.items()
    ]

# ─── B-Roll & Video Footage ─────────────────────────────────────────────────

@app.get("/api/broll-status")
@app.get("/studio/api/broll-status")
def api_broll_status():
    return get_broll_status()


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

MAX_UPLOAD_SIZE = 15 * 1024 * 1024  # 15 MB
ALLOWED_UPLOAD_EXTS = {".jpg", ".jpeg", ".png", ".webp"}

@app.delete("/api/images/{filename}")
@app.delete("/studio/api/images/{filename}")
def delete_image(filename: str):
    safe_name = os.path.basename(filename.strip())
    filepath = os.path.abspath(os.path.join(ASSETS_DIR, safe_name))
    if not filepath.startswith(os.path.abspath(ASSETS_DIR)):
        raise HTTPException(status_code=400, detail="Ruta de archivo no permitida.")
    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail="Imagen no encontrada.")
    if safe_name in IMAGE_METADATA:
        raise HTTPException(status_code=400, detail="No se pueden eliminar las imágenes plantilla predeterminadas.")
    try:
        os.remove(filepath)
        return {"status": "success", "deleted": safe_name}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"No se pudo eliminar la imagen: {str(e)}")

@app.post("/api/upload-image")
@app.post("/studio/api/upload-image")
async def upload_image(file: UploadFile = File(...)):
    raw_name = os.path.basename(file.filename or "")
    ext = os.path.splitext(raw_name)[1].lower()
    if ext not in ALLOWED_UPLOAD_EXTS:
        raise HTTPException(status_code=400, detail="Formato no admitido. Usa imágenes JPG, PNG o WebP.")

    contents = await file.read()
    if len(contents) > MAX_UPLOAD_SIZE:
        raise HTTPException(status_code=400, detail="El archivo excede el tamaño máximo permitido de 15 MB.")
    if len(contents) < 100:
        raise HTTPException(status_code=400, detail="Archivo vacío o corrupto.")

    # Validar que sea un archivo de imagen real decodificable
    try:
        img = Image.open(io.BytesIO(contents))
        img.verify()
    except Exception:
        raise HTTPException(status_code=400, detail="El archivo proporcionado no es una imagen válida.")

    filename = f"custom_{uuid.uuid4().hex[:8]}{ext}"
    filepath = os.path.join(ASSETS_DIR, filename)
    with open(filepath, "wb") as f:
        f.write(contents)
    return {"filename": filename, "url": f"/assets/images/{filename}", "label": "Tu Imagen Subida", "deletable": True}

# ─── Image Generation Engine (Z-Image Turbo, FLUX.1 Schnell, AI Horde) ───────

@app.get("/api/image-providers")
@app.get("/studio/api/image-providers")
def api_image_providers():
    return get_providers_status()

@app.post("/api/save-image-keys")
@app.post("/studio/api/save-image-keys")
def api_save_image_keys(req: SaveKeysRequest):
    save_keys(
        hf_token=req.hf_token,
        aihorde_api_key=req.aihorde_api_key
    )
    return {"status": "success", "providers": get_providers_status()}

@app.post("/api/generate-ai-image")
@app.post("/studio/api/generate-ai-image")
def api_generate_ai_image(req: GenerateAiImageRequest):
    try:
        return generate_ai_scene_image(
            prompt=req.prompt,
            aspect_ratio=req.aspect_ratio,
            label=f"Escena {req.scene_num} IA",
            provider=req.provider,
            hf_token=req.hf_token,
            aihorde_api_key=req.aihorde_api_key,
            scene_num=req.scene_num,
            used_images=req.used_images
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Fallo al generar imagen con IA: {str(e)}")

@app.post("/api/generate-ai-image-batch")
@app.post("/studio/api/generate-ai-image-batch")
def api_generate_ai_image_batch(req: BatchGenerateAiImageRequest):
    prompts = [p.strip() for p in req.prompts if p.strip()]
    if not prompts:
        raise HTTPException(status_code=400, detail="Debe proporcionar al menos un prompt.")

    import concurrent.futures
    labels = ["Escena 1 (Apertura)", "Escena 2 (Intercesión)", "Escena 3 (Victoria)"]
    results = [None] * len(prompts)

    def _worker(idx, prompt_text):
        lbl = labels[idx] if idx < len(labels) else f"Escena {idx+1}"
        return generate_ai_scene_image(
            prompt=prompt_text,
            aspect_ratio=req.aspect_ratio,
            label=lbl,
            provider=req.provider,
            hf_token=req.hf_token,
            aihorde_api_key=req.aihorde_api_key
        )

    with concurrent.futures.ThreadPoolExecutor(max_workers=min(len(prompts), 3)) as executor:
        future_to_idx = {executor.submit(_worker, i, p): i for i, p in enumerate(prompts[:3])}
        for future in concurrent.futures.as_completed(future_to_idx):
            idx = future_to_idx[future]
            try:
                results[idx] = future.result()
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Fallo al generar imagen {idx+1}: {str(e)}")

    return {"status": "success", "images": results}


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
        # Calculate target duration based on request or mode
        if req.target_duration_sec and float(req.target_duration_sec) > 0:
            target_dur = round(float(req.target_duration_sec), 2)
        elif req.duration_mode == "micro":
            target_dur = 14.0
        else:
            target_dur = 28.0

        # Calculate estimated speaking duration (words / 125 wpm * 60)
        word_count = len(full_text.split())
        estimated_dur = round((word_count / 125.0) * 60.0, 1)

        # 1. Synthesize TTS audio
        voice_key = LEGACY_VOICE_MAP.get(req.voice_key, req.voice_key)
        voice_info = VOICES.get(voice_key, VOICES.get("adam", list(VOICES.values())[0]))
        cues = await synthesize_speech(full_text, voice_info["id"], audio_file, rate=req.rate)
        audio_dur = round(get_audio_duration(audio_file), 2)

        # 2. Generate ASS subtitles & Embedded Particles
        margin_v = 400 if req.subtitle_size == "large" else 440
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
            micro_cta_text=req.micro_cta_text or "",
            hook_badge_style=req.hook_badge_style or "gold_luxury",
            hook_badge_font=req.hook_badge_font or "Montserrat",
            hook_badge_size=req.hook_badge_size or "normal",
            animation_type=req.subtitle_animation,
            position=req.subtitle_position,
            effect_type=req.effect_type,
            play_res_x=play_w,
            play_res_y=play_h,
            enable_hook_badge=bool(req.enable_hook_badge),
            enable_micro_cta=bool(req.enable_micro_cta),
            all_caps=bool(req.all_caps),
            max_duration=audio_dur
        )

        # 3. Render video (3-Scene Dynamic Pipeline)
        image_file = None
        image_file_2 = None
        image_file_3 = None

        if req.video_mode == "broll":
            theme_k = req.theme_key or "morning_favor"
            b1 = get_broll_clip(theme_k, scene_idx=1)
            b2 = get_broll_clip(theme_k, scene_idx=2)
            b3 = get_broll_clip(theme_k, scene_idx=3)
            if b1:
                image_file = b1
            if b2:
                image_file_2 = b2
            if b3:
                image_file_3 = b3

        if not image_file:
            image_file = _resolve_image(req.image_name)

        if not image_file_2:
            if req.image_name_2 and req.image_name_2 not in ["none", ""]:
                safe2 = os.path.basename(req.image_name_2.strip())
                cand2 = os.path.abspath(os.path.join(ASSETS_DIR, safe2))
                if cand2.startswith(os.path.abspath(ASSETS_DIR)) and os.path.exists(cand2):
                    image_file_2 = cand2

        if not image_file_3:
            if req.image_name_3 and req.image_name_3 not in ["none", ""]:
                safe3 = os.path.basename(req.image_name_3.strip())
                cand3 = os.path.abspath(os.path.join(ASSETS_DIR, safe3))
                if cand3.startswith(os.path.abspath(ASSETS_DIR)) and os.path.exists(cand3):
                    image_file_3 = cand3

        render_result = render_reel(
            image_file, audio_file, ass_file, output_video,
            aspect_ratio=req.aspect_ratio,
            effect_type=req.effect_type,
            camera_motion=req.camera_motion,
            music_track=req.music_track,
            music_volume=req.music_volume,
            image_path_2=image_file_2,
            image_path_3=image_file_3,
            transition_style=req.transition_style or "fade",
            enable_sfx=bool(req.enable_sfx) if req.enable_sfx is not None else True,
            seamless_loop=bool(req.seamless_loop) if req.seamless_loop is not None else False,
            master_lufs=bool(req.master_lufs) if req.master_lufs is not None else True,
            generate_trending_audio_version=bool(req.generate_trending_audio) if req.generate_trending_audio is not None else True,
            target_duration=target_dur
        )

    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = str(e) or "Error desconocido en el servidor."
        print(f"[RENDER ERROR] session={session_id}\n{traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Fallo al renderizar: {error_detail}")

    trending_filename = os.path.basename(render_result.get("trending_audio_video", output_video))
    trending_url = f"/outputs/{trending_filename}"

    return {
        "status": "success",
        "video_url": f"/outputs/reel_{session_id}.mp4",
        "filename": f"reel_{session_id}.mp4",
        "trending_audio_video_url": trending_url,
        "trending_filename": trending_filename,
        "target_duration_sec": target_dur,
        "estimated_duration_sec": estimated_dur,
        "audio_duration_sec": audio_dur,
        "actual_duration_sec": render_result.get("actual_duration_sec"),
        "duration_diff_sec": render_result.get("duration_diff_sec")
    }


def _resolve_image(image_name: str) -> str:
    # Protección estricta contra path traversal
    safe_name = os.path.basename(image_name.strip()) if image_name else ""
    image_file = os.path.abspath(os.path.join(ASSETS_DIR, safe_name))
    if not safe_name or not image_file.startswith(os.path.abspath(ASSETS_DIR)) or not os.path.exists(image_file):
        avail = [f for f in os.listdir(ASSETS_DIR) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))]
        if avail:
            image_file = os.path.abspath(os.path.join(ASSETS_DIR, avail[0]))
        else:
            raise HTTPException(status_code=400, detail="No hay imágenes disponibles en el repositorio.")
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


# ─── Daily Batch Schedule & Respectful Community Reflections ────────────────
MAGNETIC_COMMENTS = [
    "May the peace of God, which surpasses all understanding, guard your heart and mind today. We're keeping you in prayer. 🙏",
    "If someone you love is carrying a heavy burden this week, feel free to share their first name so we can join in prayer for them.",
    "Remember that you do not have to carry tomorrow's worries today. Rest in His grace tonight.",
    "Which scripture has brought you comfort during difficult seasons? Feel free to share it below to encourage someone today.",
    "May the Lord give strength to your home and peace to your family tonight.",
    "Take a quiet moment today to reflect on God's faithfulness through every season of your life."
]

@app.get("/api/magnetic-comments")
@app.get("/studio/api/magnetic-comments")
def api_magnetic_comments():
    return MAGNETIC_COMMENTS

@app.get("/api/card-template/{theme_key}")
@app.get("/studio/api/card-template/{theme_key}")
def api_card_template(theme_key: str):
    return get_card_template_for_theme(theme_key)

@app.post("/api/render-image-card")
@app.post("/studio/api/render-image-card")
async def api_render_image_card(req: ImageCardRequest):
    try:
        card_id = str(uuid.uuid4())[:8]
        out_filename = f"card_{card_id}.jpg"
        out_path = os.path.join(CARDS_DIR, out_filename)

        bg_path = _resolve_image(req.background_image_path)

        create_prayer_card_4_5(
            background_image_path=bg_path,
            title=req.title,
            prayer_text=req.prayer_text,
            verse_footer=req.verse_footer,
            watermark_text=req.watermark_text or "",
            output_path=out_path
        )
        return {
            "success": True,
            "card_url": f"/outputs/cards/{out_filename}",
            "filename": out_filename
        }
    except Exception as e:
        import traceback
        print(f"[CARD ERROR]: {traceback.format_exc()}")
        return {"success": False, "error": str(e)}

@app.get("/api/daily-batch")
@app.get("/studio/api/daily-batch")
def api_daily_batch():
    return get_daily_batch_schedule()


if __name__ == "__main__":
    import uvicorn
    host = os.environ.get("HOST", "0.0.0.0")
    port = int(os.environ.get("PORT", "8050"))
    print("\n=======================================================")
    print(f"  JESUS REELS STUDIO v4.0 — http://{host}:{port}")
    print("=======================================================\n")
    uvicorn.run("server:app", host=host, port=port, reload=False)

