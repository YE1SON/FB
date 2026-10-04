import os
import sys
import uvicorn
import spaces
import gradio as gr
from server import app as fastapi_app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ZeroGPU registration
@spaces.GPU(duration=120)
def gpu_worker():
    return True

with gr.Blocks(title="JesusReels Studio") as demo:
    btn = gr.Button("gpu", visible=False)
    btn.click(fn=gpu_worker)

# Mount Gradio into FastAPI cleanly so FastAPI directly handles / and all routes
app = gr.mount_gradio_app(fastapi_app, demo, path="/gradio")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    print("\n=======================================================")
    print(f"  JESUS REELS STUDIO - Hugging Face - Puerto {port}")
    print("=======================================================\n")
    uvicorn.run(app, host="0.0.0.0", port=port)
