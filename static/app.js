document.addEventListener("DOMContentLoaded", () => {
  // Elementos de la interfaz
  const themeSelect = document.getElementById("themeSelect");
  const customTopic = document.getElementById("customTopic");
  const btnGenerateScript = document.getElementById("btnGenerateScript");
  const scriptHook = document.getElementById("scriptHook");
  const scriptBody = document.getElementById("scriptBody");
  const scriptCta = document.getElementById("scriptCta");
  const btnSyncScriptToImage = document.getElementById("btnSyncScriptToImage");

  const voiceSelect = document.getElementById("voiceSelect");
  const rateSelect = document.getElementById("rateSelect");
  const btnPreviewAudio = document.getElementById("btnPreviewAudio");
  const audioPreviewPlayer = document.getElementById("audioPreviewPlayer");

  const imageGallery = document.getElementById("imageGallery");
  const imageUpload = document.getElementById("imageUpload");
  const aiImagePrompt = document.getElementById("aiImagePrompt");
  const btnGenerateAiImage = document.getElementById("btnGenerateAiImage");

  const subtitleStyleSelect = document.getElementById("subtitleStyleSelect");
  const subtitleSizeSelect = document.getElementById("subtitleSizeSelect");
  const liveSubPreview = document.getElementById("liveSubPreview");

  const btnRenderVideo = document.getElementById("btnRenderVideo");
  const stagePlaceholder = document.getElementById("stagePlaceholder");
  const stageSelectedImage = document.getElementById("stageSelectedImage");
  const finalVideoPlayer = document.getElementById("finalVideoPlayer");
  const renderOverlay = document.getElementById("renderOverlay");
  const renderStatusText = document.getElementById("renderStatusText");
  const renderStatusSub = document.getElementById("renderStatusSub");
  const videoActions = document.getElementById("videoActions");
  const btnDownloadVideo = document.getElementById("btnDownloadVideo");
  const btnCopyCaption = document.getElementById("btnCopyCaption");
  const recentList = document.getElementById("recentList");

  let selectedImageName = "jesus_healing_miracle.jpg";

  // 1. Cargar Temas Virales
  async function loadThemes() {
    try {
      const res = await fetch("/studio/api/themes");
      const themes = await res.json();
      themeSelect.innerHTML = themes
        .map(t => `<option value="${t.key}">${t.title}</option>`)
        .join("");
    } catch (e) {
      console.error("Error al cargar temas:", e);
    }
  }

  // 2. Cargar Voces en Inglés
  async function loadVoices() {
    try {
      const res = await fetch("/studio/api/voices");
      const voices = await res.json();
      voiceSelect.innerHTML = voices
        .map(v => `<option value="${v.key}" ${v.key === "christopher" ? "selected" : ""}>${v.name}</option>`)
        .join("");
    } catch (e) {
      console.error("Error al cargar voces:", e);
    }
  }

  // 3. Cargar Imágenes y Escenas Bíblicas
  async function loadImages() {
    try {
      const res = await fetch("/studio/api/images");
      const images = await res.json();
      imageGallery.innerHTML = images
        .map(img => `
          <div class="image-thumb ${img.filename === selectedImageName ? "selected" : ""}" data-filename="${img.filename}">
            <img src="${img.url}" alt="${img.label}">
            <div class="thumb-title">${img.label}</div>
          </div>
        `)
        .join("");

      // Eventos de selección de imagen
      document.querySelectorAll(".image-thumb").forEach(thumb => {
        thumb.addEventListener("click", () => {
          document.querySelectorAll(".image-thumb").forEach(t => t.classList.remove("selected"));
          thumb.classList.add("selected");
          selectedImageName = thumb.dataset.filename;
          stageSelectedImage.src = `/assets/images/${selectedImageName}`;
        });
      });
    } catch (e) {
      console.error("Error al cargar imágenes:", e);
    }
  }

  // 4. Generar Guion y Sincronizar Prompt de Imagen Automáticamente
  async function triggerGenerateScript() {
    btnGenerateScript.disabled = true;
    btnGenerateScript.textContent = "⏳ Generando Guion en Inglés...";
    try {
      const res = await fetch("/studio/api/generate-script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          theme_key: themeSelect.value,
          custom_topic: customTopic.value
        })
      });
      const data = await res.json();
      scriptHook.value = data.hook;
      scriptBody.value = data.body;
      scriptCta.value = data.cta;

      // Sincronizar automáticamente el prompt para la IA
      if (data.image_prompt) {
        aiImagePrompt.value = data.image_prompt;
      }
    } catch (e) {
      alert("Error al generar guion: " + e.message);
    } finally {
      btnGenerateScript.disabled = false;
      btnGenerateScript.textContent = "✨ Generar Guion de Alta Retención (en Inglés)";
    }
  }

  const btnRerollPrompt = document.getElementById("btnRerollPrompt");
  if (btnRerollPrompt) {
    btnRerollPrompt.addEventListener("click", async () => {
      btnRerollPrompt.disabled = true;
      btnRerollPrompt.textContent = "⏳ Variando...";
      await triggerSyncPrompt();
      btnRerollPrompt.disabled = false;
      btnRerollPrompt.textContent = "🎲 Otra Variación de Escena";
    });
  }

  // 5. Sincronizar Prompt de Imagen según el Guion Editado
  async function triggerSyncPrompt() {
    const fullText = `${scriptHook.value} ${scriptBody.value} ${scriptCta.value}`.trim();
    if (!fullText) {
      alert("Primero escribe o genera un guion.");
      return;
    }

    btnSyncScriptToImage.disabled = true;
    btnSyncScriptToImage.textContent = "⏳ Creando Escena que Coincida con la Oración...";

    try {
      const res = await fetch("/studio/api/generate-image-prompt", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          theme_key: themeSelect.value,
          script_text: fullText,
          custom_topic: customTopic.value
        })
      });
      const data = await res.json();
      aiImagePrompt.value = data.prompt;
      btnSyncScriptToImage.textContent = "✅ ¡Escena Sincronizada con la Oración!";
      setTimeout(() => {
        btnSyncScriptToImage.textContent = "🪄 Sincronizar: Crear Prompt de Imagen que Coincida con este Guion";
        btnSyncScriptToImage.disabled = false;
      }, 2500);

      // Desplazar suavemente hacia el generador de imágenes
      aiImagePrompt.scrollIntoView({ behavior: "smooth", block: "center" });
      aiImagePrompt.focus();
    } catch (err) {
      alert("Error al sincronizar prompt: " + err.message);
      btnSyncScriptToImage.disabled = false;
    }
  }

  // 6. Preescucha de Audio
  async function triggerAudioPreview() {
    const fullText = `${scriptHook.value} ${scriptBody.value} ${scriptCta.value}`.trim();
    if (!fullText) {
      alert("Primero genera o escribe un guion.");
      return;
    }

    btnPreviewAudio.disabled = true;
    btnPreviewAudio.textContent = "⏳ Sintetizando Voz...";
    try {
      const res = await fetch("/studio/api/preview-audio", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: fullText,
          voice_key: voiceSelect.value,
          rate: rateSelect.value
        })
      });
      const data = await res.json();
      audioPreviewPlayer.src = data.audio_url;
      audioPreviewPlayer.style.display = "block";
      audioPreviewPlayer.play();
    } catch (e) {
      alert("Error al reproducir audio: " + e.message);
    } finally {
      btnPreviewAudio.disabled = false;
      btnPreviewAudio.textContent = "🔊 Escuchar Previa del Audio";
    }
  }

  // 7. Subir Imagen Propia
  imageUpload.addEventListener("change", async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await fetch("/studio/api/upload-image", {
        method: "POST",
        body: formData
      });
      const data = await res.json();
      selectedImageName = data.filename;
      stageSelectedImage.src = data.url;
      await loadImages();
    } catch (err) {
      alert("Fallo al subir imagen: " + err.message);
    }
  });

  // 8. Generación de Imagen con IA (Puter.js)
  btnGenerateAiImage.addEventListener("click", async () => {
    const promptText = aiImagePrompt.value.trim();
    if (!promptText) {
      alert("Por favor escribe o sincroniza un prompt para la imagen.");
      return;
    }

    btnGenerateAiImage.disabled = true;
    btnGenerateAiImage.textContent = "🎨 Generando con IA... (Espera unos segundos)";

    try {
      let enhancedPrompt = promptText;
      if (!enhancedPrompt.toLowerCase().includes("8k") && !enhancedPrompt.toLowerCase().includes("vertical")) {
        enhancedPrompt = `Ultra-realistic cinematic 8k vertical 9:16 portrait of ${enhancedPrompt}, warm divine golden hour lighting, sacred holy atmosphere, highly detailed, dramatic, majestic`;
      }

      if (typeof puter !== "undefined" && puter.ai && puter.ai.txt2img) {
        const imgElement = await puter.ai.txt2img(enhancedPrompt);
        
        // Convertir imagen a Blob y subirla al backend
        const response = await fetch(imgElement.src);
        const blob = await response.blob();
        const file = new File([blob], `ai_${Date.now()}.png`, { type: "image/png" });

        const formData = new FormData();
        formData.append("file", file);

        const uploadRes = await fetch("/studio/api/upload-image", {
          method: "POST",
          body: formData
        });
        const uploadData = await uploadRes.json();
        selectedImageName = uploadData.filename;
        stageSelectedImage.src = uploadData.url;
        await loadImages();
        alert("¡Imagen creada en base a tu guion y añadida a la galería!");
      } else {
        alert("El generador Puter en el navegador no está listo. Puedes usar las imágenes maestras o subir una imagen propia.");
      }
    } catch (err) {
      console.error("Error en generación con IA:", err);
      alert("No se pudo generar la imagen automáticamente (" + err.message + "). Puedes seleccionar una escena de la galería o subir tu imagen.");
    } finally {
      btnGenerateAiImage.disabled = false;
      btnGenerateAiImage.textContent = "🎨 Crear Imagen con IA (Puter / Navegador)";
    }
  });

  // 9. Actualizar Vista Previa de Subtítulos al Cambiar Estilo
  function updateSubtitlePreview() {
    const style = subtitleStyleSelect.value;
    const isLarge = subtitleSizeSelect.value === "large";

    liveSubPreview.style.fontSize = isLarge ? "28px" : "22px";

    if (style === "gold_highlight") {
      liveSubPreview.innerHTML = `<span class="sub-word">DO</span> <span class="sub-word highlight" style="color: #ffd700;">NOT</span> <span class="sub-word">SCROLL</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "neon_cyan") {
      liveSubPreview.innerHTML = `<span class="sub-word">DO</span> <span class="sub-word highlight" style="color: #00ffcc;">NOT</span> <span class="sub-word">SCROLL</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "fire_coral") {
      liveSubPreview.innerHTML = `<span class="sub-word">DO</span> <span class="sub-word highlight" style="color: #ff5722;">NOT</span> <span class="sub-word">SCROLL</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "royal_purple") {
      liveSubPreview.innerHTML = `<span class="sub-word">DO</span> <span class="sub-word highlight" style="color: #e040fb;">NOT</span> <span class="sub-word">SCROLL</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "black_box") {
      liveSubPreview.innerHTML = `<span style="background: rgba(0,0,0,0.85); color: #ffff00; padding: 4px 10px; border-radius: 4px;">DO NOT SCROLL</span>`;
    } else if (style === "pure_minimal") {
      liveSubPreview.innerHTML = `<span style="color: #ffffff; text-shadow: 0 2px 8px rgba(0,0,0,0.9);">DO NOT SCROLL</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    }
  }

  subtitleStyleSelect.addEventListener("change", updateSubtitlePreview);
  subtitleSizeSelect.addEventListener("change", updateSubtitlePreview);

  // 10. Renderizar Video Completo (MP4)
  async function triggerRenderVideo() {
    const hook = scriptHook.value.trim();
    const body = scriptBody.value.trim();
    const cta = scriptCta.value.trim();

    if (!hook || !body || !cta) {
      alert("Por favor asegúrate de que el Gancho, Mensaje y Llamado a la Acción no estén vacíos.");
      return;
    }

    // Scroll al reproductor en móviles si está fuera de pantalla
    if (window.innerWidth <= 960) {
      document.getElementById("previewSection").scrollIntoView({ behavior: "smooth" });
    }

    btnRenderVideo.disabled = true;
    renderOverlay.style.display = "flex";
    stagePlaceholder.style.display = "block";
    finalVideoPlayer.style.display = "none";
    videoActions.style.display = "none";

    renderStatusText.textContent = "Sintetizando Voz Solemne en Inglés...";
    renderStatusSub.textContent = "Extrayendo marcas de tiempo palabra por palabra...";

    try {
      const progressTimer = setTimeout(() => {
        renderStatusText.textContent = "Quemando Subtítulos Dinámicos...";
        renderStatusSub.textContent = "Animando movimiento de cámara Ken Burns (1080x1920)...";
      }, 3000);

      const res = await fetch("/studio/api/render-video", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          hook: hook,
          body: body,
          cta: cta,
          voice_key: voiceSelect.value,
          rate: rateSelect.value,
          image_name: selectedImageName,
          subtitle_style: subtitleStyleSelect.value,
          subtitle_size: subtitleSizeSelect.value
        })
      });

      clearTimeout(progressTimer);

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Error en el renderizado");
      }

      const data = await res.json();

      stagePlaceholder.style.display = "none";
      finalVideoPlayer.src = data.video_url;
      finalVideoPlayer.style.display = "block";
      finalVideoPlayer.play();

      btnDownloadVideo.href = data.video_url;
      btnDownloadVideo.download = data.filename;
      videoActions.style.display = "block";

      loadRecentOutputs();
    } catch (e) {
      alert("Fallo al renderizar: " + e.message);
    } finally {
      renderOverlay.style.display = "none";
      btnRenderVideo.disabled = false;
    }
  }

  // 11. Copiar Texto y Hashtags para Facebook
  btnCopyCaption.addEventListener("click", () => {
    const caption = `${scriptHook.value} 🙏\n\n${scriptBody.value}\n\n${scriptCta.value}\n\n#Jesus #GodLovesYou #Faith #ChristianReels #Prayer #Amen #DailyDevotional #JesusChrist`;
    navigator.clipboard.writeText(caption).then(() => {
      btnCopyCaption.textContent = "✅ ¡Copiado al Portapapeles!";
      setTimeout(() => {
        btnCopyCaption.textContent = "📋 Copiar Texto del Post y Hashtags para Facebook";
      }, 2500);
    });
  });

  // 12. Cargar Biblioteca de Videos Recientes
  async function loadRecentOutputs() {
    try {
      const res = await fetch("/studio/api/outputs");
      const outputs = await res.json();
      if (outputs.length === 0) {
        recentList.innerHTML = `<p class="text-muted">Aún no hay videos generados.</p>`;
        return;
      }
      recentList.innerHTML = outputs.map(item => `
        <div class="recent-item" data-url="${item.url}">
          <span>📹 ${item.filename}</span>
          <a href="${item.url}" target="_blank">Reproducir ↗</a>
        </div>
      `).join("");

      document.querySelectorAll(".recent-item").forEach(item => {
        item.addEventListener("click", () => {
          stagePlaceholder.style.display = "none";
          finalVideoPlayer.src = item.dataset.url;
          finalVideoPlayer.style.display = "block";
          finalVideoPlayer.play();
          btnDownloadVideo.href = item.dataset.url;
          btnDownloadVideo.download = item.querySelector("span").textContent.replace("📹 ", "");
          videoActions.style.display = "block";
        });
      });
    } catch (e) {
      console.error("Error al cargar historial:", e);
    }
  }

  // Inicialización de Eventos
  btnGenerateScript.addEventListener("click", triggerGenerateScript);
  btnSyncScriptToImage.addEventListener("click", triggerSyncPrompt);
  btnPreviewAudio.addEventListener("click", triggerAudioPreview);
  btnRenderVideo.addEventListener("click", triggerRenderVideo);
  themeSelect.addEventListener("change", triggerGenerateScript);

  async function init() {
    await loadThemes();
    await loadVoices();
    await loadImages();
    await loadRecentOutputs();
    await triggerGenerateScript();
    updateSubtitlePreview();
  }

  init();
});
