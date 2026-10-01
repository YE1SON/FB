import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

import spaces
import gradio as gr

@spaces.GPU(duration=120)
def gpu_worker():
    return True

# Estilos para que el iframe ocupe el 100% de la pantalla sin bordes ni barras de Gradio
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
    gr.HTML('<iframe src="https://fb-fosp.onrender.com" class="full-frame" allow="clipboard-write; autoplay"></iframe>')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "7860"))
    demo.queue().launch(server_name="0.0.0.0", server_port=port, show_error=True, css=custom_css)
