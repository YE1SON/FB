import os
import sys
import time
from playwright.sync_api import sync_playwright

ARTIFACT_DIR = r"C:\Users\yeison diaz\.gemini\antigravity\brain\7a16ae56-6c8c-464a-98ac-7ba3fe7e7290"
URL = "https://132-145-202-1.sslip.io"

def run_inspection():
    print(f"Iniciando inspección en vivo de {URL} con Chromium/Playwright...")
    with sync_playwright() as p:
        # 1. Desktop Viewport (1440x900)
        print("Lanzando navegador Chromium para vista de Escritorio...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1440, "height": 900},
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        )
        page = context.new_page()

        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"[{msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: console_logs.append(f"[ERROR] {err}"))

        page.goto(URL, wait_until="domcontentloaded", timeout=45000)
        page.wait_for_selector("#workspaceReels", timeout=15000)
        time.sleep(2)

        # Captura 1: Vista general de Escritorio (Etapa 1 activa)
        path_desktop = os.path.join(ARTIFACT_DIR, "live_desktop_studio.png")
        page.screenshot(path=path_desktop, full_page=False)
        print(f"Captura Escritorio guardada: {path_desktop}")

        # Navegar a Etapa 2 (Voz y Plugins de Audio)
        btn_stage2 = page.query_selector("#navStage2")
        if btn_stage2:
            btn_stage2.click()
            time.sleep(1)
            path_stage2 = os.path.join(ARTIFACT_DIR, "live_stage2_audio_plugins.png")
            page.screenshot(path=path_stage2, full_page=False)
            print(f"Captura Etapa 2 guardada: {path_stage2}")

        # Navegar a Etapa 5 (Configuración Avanzada y Efectos)
        btn_stage5 = page.query_selector("#navStage5")
        if btn_stage5:
            btn_stage5.click()
            time.sleep(1)
            path_stage5 = os.path.join(ARTIFACT_DIR, "live_stage5_living_atmosphere.png")
            page.screenshot(path=path_stage5, full_page=False)
            print(f"Captura Etapa 5 guardada: {path_stage5}")

        browser.close()

        # 2. Mobile Viewport (Android / Pixel 7: 412x915)
        print("Lanzando navegador Chromium para vista Móvil (Android Pixel)...")
        browser_mobile = p.chromium.launch(headless=True)
        context_mobile = browser_mobile.new_context(
            viewport={"width": 412, "height": 915},
            is_mobile=True,
            has_touch=True,
            ignore_https_errors=True,
            user_agent="Mozilla/5.0 (Linux; Android 14; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Mobile Safari/537.36"
        )
        page_m = context_mobile.new_page()
        page_m.goto(URL, wait_until="domcontentloaded", timeout=45000)
        page_m.wait_for_selector("#workspaceReels", timeout=15000)
        time.sleep(2)

        path_mobile = os.path.join(ARTIFACT_DIR, "live_mobile_studio.png")
        page_m.screenshot(path=path_mobile, full_page=False)
        print(f"Captura Móvil guardada: {path_mobile}")

        # Comprobar estado de la consola
        print(f"Total de registros de consola interceptados: {len(console_logs)}")
        js_errors = [l for l in console_logs if "[error]" in l.lower() or "[error]" in l]
        print(f"Errores JS detectados: {len(js_errors)}")
        for err in js_errors[:5]:
            print("  ->", err)

        browser_mobile.close()
        print("Inspección completada con éxito.")

if __name__ == "__main__":
    run_inspection()
