import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import spaces
import gradio as gr
from server import app as fastapi_app

# Minimal Gradio interface mounted at /gradio so Hugging Face Space detects Gradio SDK
demo = gr.Blocks(title="JesusReels Studio")
with demo:
    gr.Markdown("# JesusReels Studio Backend")

@spaces.GPU(duration=120)
def gpu_worker():
    return True

# Mount Gradio at /gradio: The root '/' serves our custom frontend (static/index.html)
app = gr.mount_gradio_app(fastapi_app, demo, path="/gradio")

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", "7860"))
    uvicorn.run(app, host="0.0.0.0", port=port)
