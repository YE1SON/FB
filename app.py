import os
import re
import sys
import spaces
import gradio as gr
from gradio.routes import App
from server import app as fastapi_app

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# Mount all FastAPI routes into Gradio
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

# Read index.html content directly
static_dir = os.path.join(BASE_DIR, "static")
index_path = os.path.join(static_dir, "index.html")
with open(index_path, "r", encoding="utf-8") as f:
    full_html = f.read()

# Extract body content (stripping out static script tags so they load via head)
body_match = re.search(r"<body[^>]*>(.*?)</body>", full_html, re.DOTALL | re.IGNORECASE)
body_html = body_match.group(1) if body_match else full_html
body_html = re.sub(r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>', '', body_html)

HEAD_TAGS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/static/style.css">
<script src="https://js.puter.com/v2/"></script>
<script src="/static/app.js" defer></script>
"""

CUSTOM_CSS = """
.gradio-container {
    padding: 0 !important;
    margin: 0 !important;
    max-width: 100% !important;
    background-color: #0b0e14 !important;
}
footer, .show-api, .built-with, .show-api-divider {
    display: none !important;
}
"""

with gr.Blocks(title="JesusReels Studio") as demo:
    btn = gr.Button("gpu", visible=False)
    btn.click(fn=gpu_worker)
    gr.HTML(body_html)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    print("\n=======================================================")
    print(f"  JESUS REELS STUDIO - Hugging Face - Puerto {port}")
    print("=======================================================\n")
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        prevent_thread_lock=False,
        show_error=True,
        head=HEAD_TAGS,
        css=CUSTOM_CSS
    )
