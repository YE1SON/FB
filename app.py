import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import uvicorn
import gradio as gr
from server import app as fastapi_app

# Gradio Blocks montado para compatibilidad total con el SDK de Hugging Face
with gr.Blocks(title="JesusReels Studio") as demo:
    gr.Markdown("# JesusReels Studio")

# Montar Gradio en /gradio sobre la aplicación FastAPI principal
# De esta manera, FastAPI sirve directamente la raíz '/' y todas las APIs sin bloqueos
app = gr.mount_gradio_app(fastapi_app, demo, path="/gradio")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    print("\n=======================================================")
    print(f"  JESUS REELS STUDIO - Hugging Face - Puerto {port}")
    print("=======================================================\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
