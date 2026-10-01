import os
import sys
import uuid
import asyncio
from pathlib import Path
import spaces

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import gradio as gr
from engine.scripts import generate_script, get_themes_list, generate_image_prompt_for_script, VIRAL_THEMES
from engine.tts import synthesize_speech, VOICES
from engine.subtitles import generate_viral_ass, SUBTITLE_STYLES
from engine.video import render_reel

ASSETS_DIR = os.path.join(BASE_DIR, "assets", "images")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
os.makedirs(ASSETS_DIR, exist_ok=True)
os.makedirs(OUTPUTS_DIR, exist_ok=True)

# Mapeo de imágenes bíblicas predeterminadas
IMAGE_MAP = {
    "🕊️ Jesús Sanando a un Quebrantado": os.path.join(ASSETS_DIR, "jesus_healing_miracle.jpg"),
    "🌊 Jesús Rescatando en la Tormenta": os.path.join(ASSETS_DIR, "jesus_reaching_hand.jpg"),
    "🌌 Jesús Orando en Getsemaní": os.path.join(ASSETS_DIR, "jesus_praying_gethsemane.jpg"),
    "🫂 Jesús Abrazando y Secando Lágrimas": os.path.join(ASSETS_DIR, "jesus_comforting_embrace.jpg"),
    "✝️ La Santa Cruz en el Calvario": os.path.join(ASSETS_DIR, "holy_cross_calvary.jpg"),
    "📖 Jesús con la Santa Biblia Iluminada": os.path.join(ASSETS_DIR, "jesus_holy_bible.jpg"),
}

# Mapeo de temas
THEMES_DICT = {t["title"]: t["key"] for t in get_themes_list()}
THEME_CHOICES = list(THEMES_DICT.keys())

# Mapeo de voces
VOICE_MAP = {
    "Christopher (Solemne, Profundo y Reverente — Voz de Jesús)": "christopher",
    "Guy (Apasionado, Emocional y Directo)": "guy",
    "Brian (Tranquilo, Cálido e Inspirador)": "brian",
    "Andrew (Moderno, Expresivo y Cercano)": "andrew",
    "Jenny (Dulce, Maternal y Reconfortante)": "jenny",
}

# Mapeo de estilos de subtítulos
STYLE_MAP = {
    "Oro Real (Palabra activa en Oro Brillante)": "gold_highlight",
    "Neón Eléctrico (Palabra activa en Cian Neón)": "neon_blue",
    "Fuego y Pasión (Palabra activa en Rojo Coral)": "fire_coral",
    "Púrpura Celestial (Palabra activa en Morado Místico)": "purple_magic",
    "Caja Negra Viral (Estilo TikTok / Alex Hormozi)": "black_box",
    "Minimalista Limpio (Texto blanco sin caja)": "clean_white",
}

SPEED_CHOICES = ["-5% (Lento y Solemne)", "+0% (Normal)", "+5% (Dinámico)", "+10% (Rápido)"]
SPEED_MAP = {
    "-5% (Lento y Solemne)": "-5%",
    "+0% (Normal)": "+0%",
    "+5% (Dinámico)": "+5%",
    "+10% (Rápido)": "+10%"
}

def fn_generate_script(theme_label, custom_topic):
    theme_key = THEMES_DICT.get(theme_label)
    data = generate_script(theme_key, custom_topic)
    return data["hook"], data["body"], data["cta"]

def fn_generate_prompt(theme_label, hook, body, cta, custom_topic):
    theme_key = THEMES_DICT.get(theme_label)
    full_text = f"{hook} {body} {cta}".strip()
    prompt = generate_image_prompt_for_script(theme_key, full_text, custom_topic)
    return prompt

def fn_update_image_preview(image_label):
    path = IMAGE_MAP.get(image_label)
    if path and os.path.exists(path):
        return path
    return None

def fn_preview_audio(hook, body, cta, voice_label, speed_label):
    full_text = f"{hook.strip()} {body.strip()} {cta.strip()}".strip()
    if not full_text:
        raise gr.Error("Por favor ingresa texto en el guion para generar el audio.")
        
    voice_key = VOICE_MAP.get(voice_label, "christopher")
    voice_info = VOICES.get(voice_key, VOICES["christopher"])
    rate = SPEED_MAP.get(speed_label, "+0%")
    
    audio_id = f"preview_{uuid.uuid4().hex[:8]}.mp3"
    audio_path = os.path.join(OUTPUTS_DIR, audio_id)
    
    asyncio.run(synthesize_speech(full_text, voice_info["id"], audio_path, rate=rate))
    return audio_path

@spaces.GPU(duration=120)
def fn_render_video(hook, body, cta, voice_label, speed_label, image_label, uploaded_image, style_label, size_label, progress=gr.Progress()):
    full_text = f"{hook.strip()} {body.strip()} {cta.strip()}".strip()
    if not full_text:
        raise gr.Error("El guion no puede estar vacío.")

    progress(0.1, desc="Preparando recursos y escena bíblica...")
    
    # Resolver imagen
    if uploaded_image is not None:
        image_path = uploaded_image
    else:
        image_path = IMAGE_MAP.get(image_label)
        if not image_path or not os.path.exists(image_path):
            first_avail = next((p for p in IMAGE_MAP.values() if os.path.exists(p)), None)
            if not first_avail:
                raise gr.Error("No se encontró ninguna imagen para el fondo.")
            image_path = first_avail

    session_id = uuid.uuid4().hex[:8]
    audio_file = os.path.join(OUTPUTS_DIR, f"{session_id}_audio.mp3")
    ass_file = os.path.join(OUTPUTS_DIR, f"{session_id}_subs.ass")
    output_video = os.path.join(OUTPUTS_DIR, f"reel_{session_id}.mp4")

    voice_key = VOICE_MAP.get(voice_label, "christopher")
    voice_info = VOICES.get(voice_key, VOICES["christopher"])
    rate = SPEED_MAP.get(speed_label, "+0%")

    progress(0.3, desc="Generando narración en audio y marcas de tiempo con Edge-TTS...")
    cues = asyncio.run(synthesize_speech(full_text, voice_info["id"], audio_file, rate=rate))

    progress(0.5, desc="Generando subtítulos dinámicos con sincronización palabra a palabra...")
    style_key = STYLE_MAP.get(style_label, "gold_highlight")
    margin_v = 700 if size_label == "Grande" else 750
    generate_viral_ass(cues, ass_file, style_key=style_key, margin_v=margin_v)

    progress(0.7, desc="Renderizando video 9:16 con cámara cinematográfica Ken Burns y subtítulos...")
    render_reel(image_path, audio_file, ass_file, output_video)

    progress(1.0, desc="¡Video renderizado con éxito!")
    return output_video

# Configurar Interfaz con tema visual cristiano moderno y elegante
custom_css = """
body, .gradio-container {
    background-color: #0b0f19 !important;
    color: #e2e8f0 !important;
    font-family: 'Segoe UI', system-ui, -apple-system, sans-serif !important;
}
.header-box {
    text-align: center;
    padding: 24px;
    background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
    border: 1px solid rgba(245, 158, 11, 0.3);
    border-radius: 16px;
    margin-bottom: 24px;
    box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.5);
}
.header-title {
    font-size: 2.2rem;
    font-weight: 800;
    background: linear-gradient(90deg, #fbbf24, #f59e0b, #fef08a);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 8px;
}
.header-sub {
    color: #cbd5e1;
    font-size: 1.05rem;
    max-width: 800px;
    margin: 0 auto;
}
.gold-btn {
    background: linear-gradient(135deg, #f59e0b, #d97706) !important;
    color: #000000 !important;
    font-weight: bold !important;
    border: none !important;
    font-size: 1.1rem !important;
    box-shadow: 0 4px 14px 0 rgba(245, 158, 11, 0.39) !important;
}
.gold-btn:hover {
    background: linear-gradient(135deg, #fbbf24, #f59e0b) !important;
    transform: translateY(-1px);
}
.action-btn {
    background: #312e81 !important;
    color: #e0e7ff !important;
    font-weight: 600 !important;
    border: 1px solid #4338ca !important;
}
.action-btn:hover {
    background: #3730a3 !important;
}
"""

with gr.Blocks(title="JesusReels Studio - Generador de Videos") as demo:
    gr.HTML("""
    <div class="header-box">
        <div class="header-title">✝️ JesusReels Studio</div>
        <div class="header-sub">
            Generador automatizado de Reels y Shorts cristianos en formato vertical 9:16 para tu página de Facebook.
            Guiones en inglés nativo con alta retención, narración solemne, escenas bíblicas cinematográficas y subtítulos con resaltado dinámico.
        </div>
    </div>
    """)

    with gr.Row():
        with gr.Column(scale=6):
            with gr.Accordion("📝 1. Guion Viral en Inglés", open=True):
                with gr.Row():
                    theme_dropdown = gr.Dropdown(
                        choices=THEME_CHOICES,
                        value=THEME_CHOICES[0],
                        label="Tema de Alto Impacto para Facebook (EE.UU.)",
                        interactive=True
                    )
                with gr.Row():
                    custom_topic_input = gr.Textbox(
                        label="Tema Específico Opcional (ej: healing mother, comfort after loss, debt relief)",
                        placeholder="Escribe un tema bíblico o déjalo vacío para usar el tema seleccionado...",
                        lines=1
                    )
                btn_gen_script = gr.Button("⚡ Generar Guion Viral Nuevo", elem_classes=["action-btn"])
                
                with gr.Row():
                    hook_input = gr.Textbox(
                        label="1. Gancho Viral (Hook - Primeros 3 segundos)",
                        lines=2,
                        value="Stop scrolling. Jesus wants you to hear this right now.",
                        placeholder="Gancho en inglés...",
                        interactive=True
                    )
                with gr.Row():
                    body_input = gr.Textbox(
                        label="2. Mensaje / Oración (Body - Conexión emocional)",
                        lines=4,
                        value="I know your heart has been heavy and fear whispers that you are all alone. But the Lord says: 'Fear not, for I am with you; be not dismayed, for I am your God.' Every tear you wept in secret, He collected. Your battle ends today in His victory.",
                        placeholder="Cuerpo de la oración en inglés...",
                        interactive=True
                    )
                with gr.Row():
                    cta_input = gr.Textbox(
                        label="3. Llamado a la Acción (CTA - Comentarios y Compartir)",
                        lines=2,
                        value="If you receive His peace today, type Amen and share this blessing with someone who needs hope.",
                        placeholder="Llamado a la acción en inglés...",
                        interactive=True
                    )

            with gr.Accordion("🎨 2. Imagen Bíblica y Generador de Prompt IA", open=True):
                gr.Markdown("Elige una de las 6 escenas bíblicas 9:16 incluidas, o sube tu propia imagen. También puedes generar un prompt optimizado para crear una imagen con IA acorde al guion.")
                
                with gr.Row():
                    btn_gen_prompt = gr.Button("🪄 Generar Prompt IA Acorde al Guion", elem_classes=["action-btn"])
                with gr.Row():
                    prompt_output = gr.Textbox(
                        label="Prompt Fotorealista 8K para IA (Midjourney, Puter.js, Bing Creator)",
                        lines=3,
                        interactive=True
                    )
                
                with gr.Row():
                    with gr.Column(scale=1):
                        image_dropdown = gr.Dropdown(
                            choices=list(IMAGE_MAP.keys()),
                            value="🕊️ Jesús Sanando a un Quebrantado",
                            label="Seleccionar Escena Bíblica Oficial",
                            interactive=True
                        )
                        image_upload = gr.Image(
                            label="O subir tu propia imagen (opcional)",
                            type="filepath",
                            sources=["upload"]
                        )
                    with gr.Column(scale=1):
                        image_preview = gr.Image(
                            label="Vista Previa de la Escena Seleccionada",
                            value=IMAGE_MAP["🕊️ Jesús Sanando a un Quebrantado"],
                            interactive=False,
                            height=320
                        )

            with gr.Accordion("🎙️ 3. Voz y Narración (Edge-TTS Gratuito)", open=True):
                with gr.Row():
                    voice_dropdown = gr.Dropdown(
                        choices=list(VOICE_MAP.keys()),
                        value="Christopher (Solemne, Profundo y Reverente — Voz de Jesús)",
                        label="Voz en Inglés Americano",
                        interactive=True
                    )
                    speed_dropdown = gr.Dropdown(
                        choices=SPEED_CHOICES,
                        value="+0% (Normal)",
                        label="Velocidad de Habla",
                        interactive=True
                    )
                with gr.Row():
                    btn_preview_audio = gr.Button("🔊 Escuchar Muestra de Audio", elem_classes=["action-btn"])
                with gr.Row():
                    audio_preview = gr.Audio(label="Reproductor de Audio de Prueba", interactive=False)

            with gr.Accordion("✨ 4. Estilo de Subtítulos Virales", open=True):
                with gr.Row():
                    sub_style_dropdown = gr.Dropdown(
                        choices=list(STYLE_MAP.keys()),
                        value="Oro Real (Palabra activa en Oro Brillante)",
                        label="Estilo de Subtítulo (Animación por palabra)",
                        interactive=True
                    )
                    sub_size_dropdown = gr.Radio(
                        choices=["Normal", "Grande"],
                        value="Normal",
                        label="Tamaño del Subtítulo",
                        interactive=True
                    )

        with gr.Column(scale=5):
            gr.Markdown("### 🎬 Renderizado Final del Video")
            btn_render = gr.Button("🚀 RENDERIZAR VIDEO REEL (9:16)", elem_classes=["gold-btn"], size="lg")
            
            video_output = gr.Video(
                label="Video Generado (Vertical 9:16)",
                format="mp4",
                interactive=False,
                height=580
            )

    # Eventos interactivos
    btn_gen_script.click(
        fn=fn_generate_script,
        inputs=[theme_dropdown, custom_topic_input],
        outputs=[hook_input, body_input, cta_input]
    )

    btn_gen_prompt.click(
        fn=fn_generate_prompt,
        inputs=[theme_dropdown, hook_input, body_input, cta_input, custom_topic_input],
        outputs=[prompt_output]
    )

    image_dropdown.change(
        fn=fn_update_image_preview,
        inputs=[image_dropdown],
        outputs=[image_preview]
    )

    btn_preview_audio.click(
        fn=fn_preview_audio,
        inputs=[hook_input, body_input, cta_input, voice_dropdown, speed_dropdown],
        outputs=[audio_preview]
    )

    btn_render.click(
        fn=fn_render_video,
        inputs=[
            hook_input, body_input, cta_input,
            voice_dropdown, speed_dropdown,
            image_dropdown, image_upload,
            sub_style_dropdown, sub_size_dropdown
        ],
        outputs=[video_output]
    )

if __name__ == "__main__":
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=7860,
        show_error=True,
        theme=gr.themes.Soft(primary_hue="amber", neutral_hue="slate"),
        css=custom_css
    )
