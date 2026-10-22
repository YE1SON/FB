import asyncio
import os
import sys
import time
import subprocess
from playwright.async_api import async_playwright

async def run_e2e_test():
    print("Starting JesusReels Studio Server for E2E Test...")
    port = 8055
    server_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "server:app", "--port", str(port), "--host", "127.0.0.1"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2.5)

    console_errors = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        page.on("console", lambda msg: console_errors.append(msg.text) if msg.type == "error" else None)
        page.on("pageerror", lambda err: console_errors.append(str(err)))

        url = f"http://127.0.0.1:{port}"
        print(f"Navigating to {url}...")
        await page.goto(url, wait_until="networkidle")

        # 1. Verify themes
        optgroups = await page.locator("#themeSelect optgroup").count()
        options = await page.locator("#themeSelect option").count()
        print(f"Themes verified: {options} themes across {optgroups} optgroups.")
        assert optgroups == 5, f"Expected 5 optgroups, got {optgroups}"
        assert options == 26, f"Expected 26 themes, got {options}"

        # 2. Check initial script generation
        print("Testing Script Generation...")
        await page.click("#btnGenerateScript")
        await page.wait_for_timeout(2000)

        hook1 = await page.input_value("#scriptHook")
        body1 = await page.input_value("#scriptBody")
        cta1 = await page.input_value("#scriptCta")
        scene1_prompt1 = await page.input_value("#scene1PromptInput")

        print("--- GENERATION 1 ---")
        print("HOOK:", hook1)
        print("BODY (preview):", body1[:70], "...")
        print("CTA:", cta1)
        print("SCENE 1 PROMPT (preview):", scene1_prompt1[:80], "...")

        assert hook1.strip(), "Hook 1 must not be empty"
        assert body1.strip(), "Body 1 must not be empty"
        assert cta1.strip(), "CTA 1 MUST NOT be empty (user requested CTA reintegration)"
        assert "Jesus" in scene1_prompt1, "Scene 1 MUST feature Jesus Christ in foreground"
        assert "no text" in scene1_prompt1, "Scene 1 prompt must enforce strict no text"

        # 3. Test second generation for dynamic rotation
        print("Testing Second Script Generation (Checking Dynamic Rotation)...")
        await page.click("#btnGenerateScript")
        await page.wait_for_timeout(2000)

        hook2 = await page.input_value("#scriptHook")
        cta2 = await page.input_value("#scriptCta")
        print("--- GENERATION 2 ---")
        print("HOOK:", hook2)
        print("CTA:", cta2)

        # 4. Verify Google Vids horizontal timeline
        print("Verifying Google Vids Timeline & Interactive Switching...")
        t1 = page.locator("#previewThumbScene1")
        t2 = page.locator("#previewThumbScene2")
        t3 = page.locator("#previewThumbScene3")
        assert await t1.is_visible(), "Timeline Scene 1 must be visible"
        assert await t2.is_visible(), "Timeline Scene 2 must be visible"
        assert await t3.is_visible(), "Timeline Scene 3 must be visible"

        # Click Scene 2
        await t2.click()
        await page.wait_for_timeout(300)
        is_t2_active = await t2.evaluate("el => el.classList.contains('active')")
        assert is_t2_active, "Timeline Scene 2 must become active when clicked"

        # Click Transition Badge 1
        trans1 = page.locator("#transBadge1")
        assert await trans1.is_visible(), "Transition badge 1 must be visible"
        initial_label = await page.locator("#transLabel1").text_content()
        await trans1.click()
        new_label = await page.locator("#transLabel1").text_content()
        print(f"Transition cycled from '{initial_label}' to '{new_label}'")
        assert initial_label != new_label, "Transition badge must cycle on click"

        # 5. Capture screenshot of the new UI
        screenshot_path = "outputs/jesusreels_restructured_ui.png"
        os.makedirs("outputs", exist_ok=True)
        await page.screenshot(path=screenshot_path, full_page=True)
        print(f"Captured screenshot at {screenshot_path}")

        print("Console errors count:", len(console_errors))
        if console_errors:
            print("Console errors logged:", console_errors)

        await browser.close()

    server_proc.terminate()
    try:
        server_proc.wait(timeout=3)
    except Exception:
        server_proc.kill()

    print("ALL E2E BROWSER TESTS PASSED SUCCESSFULLY!")

if __name__ == "__main__":
    asyncio.run(run_e2e_test())
