import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import spaces
import gradio as gr
from server import app as fastapi_app

# Función decorada con ZeroGPU para satisfacer los requisitos del runtime de Hugging Face
@spaces.GPU(duration=120)
def gpu_worker():
    return True

with gr.Blocks(title="JesusReels Studio") as demo:
    btn = gr.Button("gpu", visible=False)
    btn.click(fn=gpu_worker)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    
    # 1. Iniciar Gradio con cola activa (ZeroGPU engancha aquí su informe de inicio)
    res = demo.queue().launch(
        server_name="0.0.0.0",
        server_port=port,
        prevent_thread_lock=True,
        show_error=True
    )
    launched_app = res[0]

    # 2. Insertar todas las rutas del servidor FastAPI (incluyendo '/', '/assets', '/static', '/studio/api/...')
    # en la posición 0 del router de Gradio para que se atiendan directamente sin ser interceptadas por el catch-all de Gradio.
    for route in reversed(fastapi_app.routes):
        launched_app.router.routes.insert(0, route)

    print("\n=======================================================")
    print(f"  JESUS REELS STUDIO - Hugging Face - Activo en puerto {port}")
    print("=======================================================\n")
    
    demo.block_thread()
