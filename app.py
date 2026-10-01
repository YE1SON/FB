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

# Clean full-screen iframe wrapper so Gradio displays the exact custom web studio
custom_css = """
body, .gradio-container, .main, #root {
    margin: 0 !important;
    padding: 0 !important;
    max-width: 100% !important;
    width: 100% !important;
    height: 100vh !important;
    background-color: #0b0f19 !important;
    overflow: hidden !important;
}
footer {
    display: none !important;
}
iframe {
    width: 100% !important;
    height: 100vh !important;
    border: none !important;
    display: block !important;
}
"""

with gr.Blocks(title="JesusReels Studio") as demo:
    btn = gr.Button("gpu", visible=False)
    btn.click(fn=gpu_worker)
    gr.HTML('<iframe src="/app-view" allow="clipboard-write"></iframe>')

# Mount backend API routes and static assets onto Gradio's internal FastAPI app
demo.app.include_router(fastapi_app.router)
demo.app.mount("/static", StaticFiles(directory=STATIC_DIR), name="hf_static")
demo.app.mount("/assets", StaticFiles(directory=ASSETS_DIR), name="hf_assets")
demo.app.mount("/outputs", StaticFiles(directory=OUTPUTS_DIR), name="hf_outputs")

@demo.app.get("/app-view")
def serve_custom_ui():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    demo.queue().launch(server_name="0.0.0.0", server_port=port, show_error=True, css=custom_css)
