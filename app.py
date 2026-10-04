import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import spaces
import gradio as gr
from gradio.routes import App
from server import app as fastapi_app

# Parchear App.create_app para insertar todas las rutas de FastAPI
original_create_app = App.create_app

def custom_create_app(*args, **kwargs):
    gradio_app = original_create_app(*args, **kwargs)
    for route in reversed(fastapi_app.routes):
        gradio_app.router.routes.insert(0, route)
    return gradio_app

App.create_app = custom_create_app

# ZeroGPU registration
@spaces.GPU(duration=120)
def gpu_worker():
    return True

CUSTOM_CSS = """
.gradio-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
    min-height: 100vh !important;
}
footer, .show-api, .built-with {
    display: none !important;
}
"""

with gr.Blocks(title="JesusReels Studio", css=CUSTOM_CSS) as demo:
    btn = gr.Button("gpu", visible=False)
    btn.click(fn=gpu_worker)
    gr.HTML('<iframe src="/app-view" style="width:100%; height:100vh; border:none; display:block; position:fixed; top:0; left:0; right:0; bottom:0; z-index:999999;"></iframe>')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    print("\n=======================================================")
    print(f"  JESUS REELS STUDIO - Hugging Face - Puerto {port}")
    print("=======================================================\n")
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        prevent_thread_lock=False,
        show_error=True
    )
