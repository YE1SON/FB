import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import spaces
import gradio as gr
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from server import app as fastapi_app

STATIC_DIR = os.path.join(BASE_DIR, "static")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

@spaces.GPU(duration=120)
def gpu_worker():
    return True

custom_css = """
body, .gradio-container, .main, #root, .contain {
    margin: 0 !important;
    padding: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    height: 100vh !important;
    background-color: #0b0f19 !important;
    overflow: hidden !important;
}
footer, .footer {
    display: none !important;
}
.full-frame {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    border: none;
    display: block;
    z-index: 10000;
}
"""

with gr.Blocks(title="JesusReels Studio") as demo:
    btn = gr.Button("gpu", visible=False)
    btn.click(fn=gpu_worker)
    # Carga la interfaz original directamente desde Hugging Face (sin dependencias de Render)
    gr.HTML('<iframe src="/app-view" class="full-frame" allow="clipboard-write; autoplay"></iframe>')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    res = demo.queue().launch(
        server_name="0.0.0.0",
        server_port=port,
        prevent_thread_lock=True,
        show_error=True,
        css=custom_css
    )
    launched_app = res[0]

    # Montar todas las rutas del backend de video, Edge-TTS, imágenes y scripts localmente en Hugging Face
    launched_app.include_router(fastapi_app.router)
    launched_app.mount("/static", StaticFiles(directory=STATIC_DIR), name="hf_static")
    launched_app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="hf_assets")
    launched_app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="hf_outputs")

    @launched_app.get("/app-view")
    def serve_local_studio():
        return FileResponse(os.path.join(STATIC_DIR, "index.html"))

    print("\n=======================================================")
    print(f"  JESUS REELS STUDIO (Hugging Face) - Activo en puerto {port}")
    print("=======================================================\n")
    demo.block_thread()
