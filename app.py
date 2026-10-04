import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import spaces
import gradio as gr
from gradio.routes import App
from server import app as fastapi_app

# Parchear App.create_app para insertar todas las rutas de FastAPI al inicio del router
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

with gr.Blocks(title="JesusReels Studio") as demo:
    btn = gr.Button("gpu", visible=False)
    btn.click(fn=gpu_worker)

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
