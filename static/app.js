function bootstrapJesusStudio() {
  const themeSelect = document.getElementById("themeSelect");
  if (!themeSelect) {
    setTimeout(bootstrapJesusStudio, 60);
    return;
  }

  // Elementos de la interfaz
  const customTopic = document.getElementById("customTopic");
  const scriptDurationMode = document.getElementById("scriptDurationMode");
  const btnGenerateScript = document.getElementById("btnGenerateScript");
  const scriptHook = document.getElementById("scriptHook");
  const scriptBody = document.getElementById("scriptBody");
  const scriptCta = document.getElementById("scriptCta");
  const btnSyncScriptToImage = document.getElementById("btnSyncScriptToImage");

  const voiceSelect = document.getElementById("voiceSelect");
  const rateSelect = document.getElementById("rateSelect");
  const musicSelect = document.getElementById("musicSelect");
  const btnPreviewAudio = document.getElementById("btnPreviewAudio");
  const audioPreviewPlayer = document.getElementById("audioPreviewPlayer");

  let currentSeoCaption = "";
  let currentHookText = "";

  const videoModeSelect = document.getElementById("videoModeSelect");
  const imageGallerySection = document.getElementById("imageGallerySection");
  const brollInfo = document.getElementById("brollInfo");
  const brollApiStatus = document.getElementById("brollApiStatus");

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
  const scriptPinnedComment = document.getElementById("scriptPinnedComment");
  const btnCopyPinnedComment = document.getElementById("btnCopyPinnedComment");
  const btnCopyFinalPinnedComment = document.getElementById("btnCopyFinalPinnedComment");
  const btnViewStage = document.getElementById("btnViewStage");
  const btnViewVideo = document.getElementById("btnViewVideo");
  const puterStatusDot = document.getElementById("puterStatusDot");
  const puterStatusText = document.getElementById("puterStatusText");
  const btnPuterConnect = document.getElementById("btnPuterConnect");
  const recentList = document.getElementById("recentList");

  let currentPinnedComment = "";
  let selectedImageName = "jesus_healing_miracle.jpg";

  // 1. Cargar Temas Virales
  async function loadThemes() {
    try {
      const res = await fetch("/api/themes");
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
      const res = await fetch("/api/voices");
      const voices = await res.json();
      voiceSelect.innerHTML = voices
        .map(v => `<option value="${v.key}" ${v.key === "christopher" ? "selected" : ""}>${v.name}</option>`)
        .join("");
    } catch (e) {
      console.error("Error al cargar voces:", e);
    }
  }

  // 2b. Cargar Música de Fondo de Adoración
  async function loadWorshipTracks() {
    try {
      const res = await fetch("/api/worship-tracks");
      const tracks = await res.json();
      if (musicSelect) {
        musicSelect.innerHTML = tracks
          .map(t => `<option value="${t.key}" ${t.key === "worship_piano_peace" ? "selected" : ""}>${t.name}</option>`)
          .join("");
      }
    } catch (e) {
      console.error("Error al cargar pistas de adoración:", e);
    }
  }

  // 2c. Verificar estado de B-Roll (Pixabay API)
  async function loadBrollStatus() {
    try {
      const res = await fetch("/api/broll-status");
      const status = await res.json();
      if (brollApiStatus) {
        if (status.available) {
          brollApiStatus.textContent = `✅ Pixabay API conectada. ${status.cached_clips} clips en caché.`;
          brollApiStatus.style.color = "#2ecc71";
        } else {
          brollApiStatus.textContent = "⚠️ PIXABAY_API_KEY no configurada. Configúrala en los Secrets del Space para usar B-Roll.";
          brollApiStatus.style.color = "#e74c3c";
        }
      }
    } catch (e) {
      if (brollApiStatus) {
        brollApiStatus.textContent = "⚠️ No se pudo verificar la conexión con Pixabay.";
      }
    }
  }

  // 2d. Toggle entre modo B-Roll y modo Imagen
  function toggleVideoMode() {
    if (!videoModeSelect) return;
    const mode = videoModeSelect.value;
    if (mode === "broll") {
      if (brollInfo) brollInfo.style.display = "block";
      if (imageGallerySection) imageGallerySection.style.display = "none";
    } else {
      if (brollInfo) brollInfo.style.display = "none";
      if (imageGallerySection) imageGallerySection.style.display = "block";
    }
  }

  // 3. Cargar Imágenes y Escenas Bíblicas
  async function loadImages() {
    try {
      const res = await fetch("/api/images");
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
          const stageBlurBg = document.getElementById("stageBlurBg");
          if (stageBlurBg) {
            stageBlurBg.style.backgroundImage = `url('/assets/images/${selectedImageName}')`;
          }
          showStageView();
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
      const durationMode = scriptDurationMode ? scriptDurationMode.value : "deep";
      const res = await fetch("/api/generate-script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          theme_key: themeSelect.value,
          custom_topic: customTopic.value,
          mode: durationMode
        })
      });
      const data = await res.json();
      scriptHook.value = data.hook;
      scriptBody.value = data.body;
      scriptCta.value = data.cta;

      if (data.hook_text) {
        currentHookText = data.hook_text;
      }

      if (data.seo_caption) {
        currentSeoCaption = data.seo_caption;
      }

      if (data.pinned_comment) {
        currentPinnedComment = data.pinned_comment;
        if (scriptPinnedComment) {
          scriptPinnedComment.value = data.pinned_comment;
        }
      }

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

  // Copiar Comentario Fijado al Portapapeles
  function copyPinnedComment() {
    const text = currentPinnedComment || (scriptPinnedComment ? scriptPinnedComment.value : "");
    if (!text) {
      alert("Genera primero un guion para obtener el comentario fijado.");
      return;
    }
    navigator.clipboard.writeText(text).then(() => {
      if (btnCopyPinnedComment) {
        btnCopyPinnedComment.textContent = "✅ ¡Copiado!";
        setTimeout(() => {
          btnCopyPinnedComment.textContent = "📋 Copiar Comentario";
        }, 2500);
      }
      if (btnCopyFinalPinnedComment) {
        btnCopyFinalPinnedComment.textContent = "✅ ¡Comentario Copiado!";
        setTimeout(() => {
          btnCopyFinalPinnedComment.textContent = "📌 Copiar Comentario Fijado del Video";
        }, 2500);
      }
    }).catch(err => {
      alert("No se pudo copiar automáticamente: " + err);
    });
  }

  if (btnCopyPinnedComment) btnCopyPinnedComment.addEventListener("click", copyPinnedComment);
  if (btnCopyFinalPinnedComment) btnCopyFinalPinnedComment.addEventListener("click", copyPinnedComment);

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
      const res = await fetch("/api/generate-image-prompt", {
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
      const res = await fetch("/api/preview-audio", {
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
      const res = await fetch("/api/upload-image", {
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

  // ─── Utilidad para extraer mensajes de error limpios ───────────────────────
  function extractError(err) {
    if (!err) return "Error desconocido";
    if (typeof err === "string") return err;
    if (err.message && typeof err.message === "string") return err.message;
    if (err.error) {
      if (typeof err.error === "string") return err.error;
      if (err.error.message && typeof err.error.message === "string") return err.error.message;
      try { return JSON.stringify(err.error); } catch (_) {}
    }
    try { return JSON.stringify(err); } catch (_) { return String(err); }
  }

  // ─── Estado y Conexión de Puter AI ─────────────────────────────────────────
  function updatePuterStatus() {
    if (!puterStatusDot || !puterStatusText) return;
    try {
      if (typeof puter !== "undefined" && puter.auth && puter.auth.isSignedIn()) {
        puterStatusDot.style.background = "#22c55e";
        puterStatusText.textContent = "Puter AI: Conectado (Listo para crear en HD)";
        if (btnPuterConnect) btnPuterConnect.style.display = "none";
        return true;
      }
    } catch (_) {}
    puterStatusDot.style.background = "#f59e0b";
    puterStatusText.textContent = "Puter AI: Pendiente de activar";
    if (btnPuterConnect) {
      btnPuterConnect.style.display = "inline-block";
      btnPuterConnect.textContent = "🔑 Conectar con 1 Clic";
      btnPuterConnect.disabled = false;
    }
    return false;
  }

  if (btnPuterConnect) {
    btnPuterConnect.addEventListener("click", async () => {
      btnPuterConnect.disabled = true;
      btnPuterConnect.textContent = "Abriendo ventana...";

      try {
        await puter.auth.signIn({ attempt_temp_user_creation: true });
        updatePuterStatus();
        alert("¡Conexión exitosa con Puter AI! Ya puedes generar imágenes con máxima resolución y sin marcas de agua.");
      } catch (err) {
        console.error("Error al conectar con Puter:", err);
        updatePuterStatus();
        const errStr = extractError(err);
        alert("Aviso de conexión: " + errStr + "\n\nTip: Si tu navegador bloqueó la ventana emergente, mira en la barra de direcciones de tu navegador (arriba a la derecha) y dale a 'Permitir ventanas emergentes'.");
      } finally {
        updatePuterStatus();
      }
    });
  }

  // 8. Generación de Imagen con IA (Puter.js - Máxima Calidad sin Marcas de Agua)
  btnGenerateAiImage.addEventListener("click", async () => {
    const promptText = aiImagePrompt.value.trim();
    if (!promptText) {
      alert("Por favor escribe o sincroniza un prompt para la imagen.");
      return;
    }

    if (typeof puter === "undefined" || !puter.ai || !puter.ai.txt2img) {
      alert("El motor Puter no está cargado en el navegador. Por favor recarga la página.");
      return;
    }

    // Si aún no está conectado, abrir la ventana de autorización con este clic
    if (puter.auth && !puter.auth.isSignedIn()) {
      btnGenerateAiImage.disabled = true;
      btnGenerateAiImage.textContent = "🔑 Abriendo ventana de conexión Puter...";
      try {
        await puter.auth.signIn({ attempt_temp_user_creation: true });
        updatePuterStatus();
      } catch (authErr) {
        btnGenerateAiImage.disabled = false;
        btnGenerateAiImage.textContent = "🎨 Crear Imagen con IA (Puter - Alta Resolución)";
        updatePuterStatus();
        alert("Se requiere autorizar Puter para crear imágenes:\n" + extractError(authErr) + "\n\nTip: Asegúrate de permitir ventanas emergentes si tu navegador te lo solicita.");
        return;
      }
    }

    btnGenerateAiImage.disabled = true;
    btnGenerateAiImage.textContent = "🎨 Generando imagen en alta resolución... (Puter)";

    try {
      let enhancedPrompt = promptText;
      if (!enhancedPrompt.toLowerCase().includes("cinematic") && !enhancedPrompt.toLowerCase().includes("masterpiece")) {
        enhancedPrompt = `Ultra-realistic cinematic 8k portrait of ${enhancedPrompt}, warm divine golden hour lighting, sacred holy atmosphere, highly detailed, dramatic, majestic, octane render, masterpiece, award winning photography, sharp focus`;
      }

      const imgElement = await puter.ai.txt2img(enhancedPrompt);

      let blob;
      if (imgElement instanceof HTMLImageElement || (imgElement && imgElement.src)) {
        btnGenerateAiImage.textContent = "💾 Guardando imagen en tu galería...";
        const response = await fetch(imgElement.src);
        blob = await response.blob();
      } else if (imgElement instanceof Blob) {
        btnGenerateAiImage.textContent = "💾 Guardando imagen en tu galería...";
        blob = imgElement;
      } else {
        throw new Error("Puter no devolvió una imagen válida.");
      }

      const file = new File([blob], `ai_${Date.now()}.png`, { type: "image/png" });

      const formData = new FormData();
      formData.append("file", file);

      const uploadRes = await fetch("/api/upload-image", {
        method: "POST",
        body: formData
      });

      if (!uploadRes.ok) {
        throw new Error("Error al guardar la imagen en el servidor.");
      }

      const uploadData = await uploadRes.json();
      selectedImageName = uploadData.filename;
      stageSelectedImage.src = uploadData.url;
      const stageBlurBg = document.getElementById("stageBlurBg");
      if (stageBlurBg) {
        stageBlurBg.style.backgroundImage = `url('${uploadData.url}')`;
      }

      await loadImages();
      showStageView();
      alert("¡Imagen creada en alta resolución con IA y añadida a tu galería!");
    } catch (err) {
      console.error("Error en generación con Puter:", err);
      alert("No se pudo generar la imagen: " + extractError(err));
    } finally {
      btnGenerateAiImage.disabled = false;
      btnGenerateAiImage.textContent = "🎨 Crear Imagen con IA (Puter - Alta Resolución)";
    }
  });

  // 9. Actualizar Vista Previa de Subtítulos al Cambiar Estilo
  function updateSubtitlePreview() {
    const style = subtitleStyleSelect.value;
    const isLarge = subtitleSizeSelect.value === "large";

    liveSubPreview.style.fontSize = isLarge ? "28px" : "22px";

    if (style === "gold_highlight") {
      liveSubPreview.innerHTML = `<span class="sub-word">GOD IS</span> <span class="sub-word highlight" style="color: #ffd700;">WITH YOU</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "neon_cyan") {
      liveSubPreview.innerHTML = `<span class="sub-word">GOD IS</span> <span class="sub-word highlight" style="color: #00ffcc;">WITH YOU</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "fire_coral") {
      liveSubPreview.innerHTML = `<span class="sub-word">GOD IS</span> <span class="sub-word highlight" style="color: #ff5722;">WITH YOU</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "royal_purple") {
      liveSubPreview.innerHTML = `<span class="sub-word">GOD IS</span> <span class="sub-word highlight" style="color: #e040fb;">WITH YOU</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "black_box") {
      liveSubPreview.innerHTML = `<span style="background: rgba(0,0,0,0.85); color: #ffff00; padding: 4px 10px; border-radius: 4px;">GOD IS WITH YOU</span>`;
    } else if (style === "pure_minimal") {
      liveSubPreview.innerHTML = `<span style="color: #ffffff; text-shadow: 0 2px 8px rgba(0,0,0,0.9);">GOD IS WITH YOU</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    }
  }

  subtitleStyleSelect.addEventListener("change", updateSubtitlePreview);
  subtitleSizeSelect.addEventListener("change", updateSubtitlePreview);

  // ─── Canvas Particle & Visual Effects Engine ────────────────────────────────
  const fxCanvas = document.getElementById("fxCanvas");
  let fxCtx = fxCanvas ? fxCanvas.getContext("2d") : null;
  let fxAnimationId = null;
  let particles = [];

  function initParticles(count = 35) {
    particles = [];
    if (!fxCanvas) return;
    const w = fxCanvas.width = fxCanvas.offsetWidth || 320;
    const h = fxCanvas.height = fxCanvas.offsetHeight || 568;
    for (let i = 0; i < count; i++) {
      particles.push({
        x: Math.random() * w,
        y: Math.random() * h,
        radius: Math.random() * 3.5 + 1.2,
        speedY: Math.random() * 0.8 + 0.35,
        speedX: (Math.random() - 0.5) * 0.5,
        alpha: Math.random() * 0.7 + 0.3,
        pulseSpeed: Math.random() * 0.04 + 0.02,
        pulseVal: Math.random() * Math.PI
      });
    }
  }

  function renderFx() {
    if (!fxCanvas || !fxCtx) return;
    const effectSelect = document.getElementById("effectTypeSelect");
    const effect = effectSelect ? effectSelect.value : "cinematic_dust";
    const w = fxCanvas.width;
    const h = fxCanvas.height;

    fxCtx.clearRect(0, 0, w, h);

    if (effect === "cinematic_dust") {
      // Golden Dust Motes floating up with sparkling glow
      particles.forEach(p => {
        p.y -= p.speedY;
        p.x += p.speedX;
        p.pulseVal += p.pulseSpeed;
        const currentAlpha = p.alpha * (0.6 + 0.4 * Math.sin(p.pulseVal));

        if (p.y < -10) {
          p.y = h + 10;
          p.x = Math.random() * w;
        }

        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        fxCtx.fillStyle = `rgba(255, 215, 0, ${currentAlpha})`;
        fxCtx.shadowColor = "#ffd700";
        fxCtx.shadowBlur = 10;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "holy_fire") {
      // Fuego del Espíritu Santo (Chispas rubí, ámbar y oro)
      particles.forEach(p => {
        p.y -= p.speedY * 1.6;
        p.x += p.speedX * 1.2;
        p.pulseVal += p.pulseSpeed * 1.5;
        const currentAlpha = p.alpha * (0.7 + 0.3 * Math.sin(p.pulseVal));

        if (p.y < -10) {
          p.y = h + 10;
          p.x = Math.random() * w;
        }

        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius * 0.9, 0, Math.PI * 2);
        fxCtx.fillStyle = p.radius > 2.5 ? `rgba(255, 60, 20, ${currentAlpha})` : `rgba(255, 190, 0, ${currentAlpha})`;
        fxCtx.shadowColor = "#ff4500";
        fxCtx.shadowBlur = 12;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "celestial_glow") {
      // Resplandor de Gloria (Motes angelicales blancos y suaves)
      particles.forEach(p => {
        p.y -= p.speedY * 0.6;
        p.x += p.speedX * 0.5;
        p.pulseVal += p.pulseSpeed;
        const currentAlpha = p.alpha * (0.5 + 0.5 * Math.sin(p.pulseVal));

        if (p.y < -10) {
          p.y = h + 10;
          p.x = Math.random() * w;
        }

        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius * 1.3, 0, Math.PI * 2);
        fxCtx.fillStyle = `rgba(255, 255, 255, ${currentAlpha * 0.85})`;
        fxCtx.shadowColor = "#ffffff";
        fxCtx.shadowBlur = 15;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "golden_hour") {
      // Hora Dorada Sagrada (Luz cálida de atardecer)
      const gradient = fxCtx.createLinearGradient(0, 0, 0, h);
      gradient.addColorStop(0, "rgba(255, 180, 50, 0.15)");
      gradient.addColorStop(1, "rgba(255, 120, 0, 0.22)");
      fxCtx.fillStyle = gradient;
      fxCtx.fillRect(0, 0, w, h);

      particles.forEach(p => {
        p.y -= p.speedY * 0.8;
        p.pulseVal += p.pulseSpeed;
        const currentAlpha = p.alpha * 0.7;
        if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        fxCtx.fillStyle = `rgba(255, 200, 80, ${currentAlpha})`;
        fxCtx.shadowColor = "#ffa500";
        fxCtx.shadowBlur = 8;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "divine_light") {
      // Radiant golden divine sunbeams pulsing from top
      const time = Date.now() * 0.0018;
      const gradient = fxCtx.createRadialGradient(w / 2, 0, 15, w / 2, 0, h * 0.85);
      const intensity = 0.32 + 0.12 * Math.sin(time);
      gradient.addColorStop(0, `rgba(255, 235, 140, ${intensity})`);
      gradient.addColorStop(0.45, `rgba(255, 190, 40, ${intensity * 0.55})`);
      gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
      fxCtx.fillStyle = gradient;
      fxCtx.fillRect(0, 0, w, h);
    } else if (effect === "dramatic_grain") {
      // Dynamic high-contrast film grain simulation
      const imgData = fxCtx.createImageData(w, h);
      const buffer = new Uint32Array(imgData.data.buffer);
      const len = buffer.length;
      for (let i = 0; i < len; i += 2) {
        if (Math.random() < 0.15) {
          const v = Math.random() > 0.5 ? 255 : 0;
          buffer[i] = (60 << 24) | (v << 16) | (v << 8) | v;
        }
      }
      fxCtx.putImageData(imgData, 0, 0);
    }

    fxAnimationId = requestAnimationFrame(renderFx);
  }

  function startFxLoop() {
    if (fxAnimationId) cancelAnimationFrame(fxAnimationId);
    initParticles(35);
    renderFx();
  }

  const effectTypeSelect = document.getElementById("effectTypeSelect");
  if (effectTypeSelect) {
    effectTypeSelect.addEventListener("change", () => {
      startFxLoop();
    });
  }

  // ─── Live Previews: Subtitle Position & Animation ─────────────────────────
  const subtitlePositionSelect = document.getElementById("subtitlePositionSelect");
  const subtitleAnimationSelect = document.getElementById("subtitleAnimationSelect");
  const stageOverlay = document.getElementById("stageOverlay");

  function updateSubtitlePosition() {
    if (!stageOverlay || !subtitlePositionSelect) return;
    stageOverlay.classList.remove("pos-bottom", "pos-center", "pos-top");
    stageOverlay.classList.add(`pos-${subtitlePositionSelect.value}`);
  }

  function updateSubtitleAnimation() {
    if (!stagePlaceholder || !subtitleAnimationSelect) return;
    stagePlaceholder.classList.remove("anim-pop", "anim-fade", "anim-scale_slow", "anim-none");
    stagePlaceholder.classList.add(`anim-${subtitleAnimationSelect.value}`);
  }

  if (subtitlePositionSelect) {
    subtitlePositionSelect.addEventListener("change", updateSubtitlePosition);
  }
  if (subtitleAnimationSelect) {
    subtitleAnimationSelect.addEventListener("change", updateSubtitleAnimation);
  }

  // ─── Live Preview: Camera Motion ──────────────────────────────────────────
  const cameraMotionSelect = document.getElementById("cameraMotionSelect");
  function updateCameraMotionPreview() {
    if (!stagePlaceholder || !cameraMotionSelect) return;
    stagePlaceholder.classList.remove(
      "camera-none", "camera-zoom_in", "camera-zoom_out",
      "camera-pan_up", "camera-pan_down", "camera-pan_right", "camera-pan_left", "camera-zoom_in_pan_up"
    );
    stagePlaceholder.classList.add(`camera-${cameraMotionSelect.value}`);
  }
  if (cameraMotionSelect) {
    cameraMotionSelect.addEventListener("change", updateCameraMotionPreview);
  }

  // ─── Live Preview: Aspect Ratio & Smart Fitting ───────────────────────────
  function updateAspectRatioPreview() {
    const aspectSelect = document.getElementById("aspectRatioSelect");
    const phoneMockup = document.querySelector(".phone-mockup");
    const stageBlurBg = document.getElementById("stageBlurBg");
    if (!aspectSelect || !phoneMockup) return;

    if (stageBlurBg) {
      stageBlurBg.style.backgroundImage = `url('/assets/images/${selectedImageName}')`;
    }

    if (aspectSelect.value === "9:16") {
      phoneMockup.style.aspectRatio = "9/16";
      phoneMockup.style.maxWidth = "320px";
      stagePlaceholder.classList.remove("fit-contain");
    } else if (aspectSelect.value === "1:1") {
      phoneMockup.style.aspectRatio = "1/1";
      phoneMockup.style.maxWidth = "380px";
      stagePlaceholder.classList.add("fit-contain");
    } else if (aspectSelect.value === "16:9") {
      phoneMockup.style.aspectRatio = "16/9";
      phoneMockup.style.maxWidth = "480px";
      stagePlaceholder.classList.add("fit-contain");
    }

    setTimeout(initParticles, 150);
  }

  const aspectRatioSelect = document.getElementById("aspectRatioSelect");
  if (aspectRatioSelect) {
    aspectRatioSelect.addEventListener("change", () => {
      updateAspectRatioPreview();
      showStageView();
    });
  }

  // ─── Control de Modo de Vista Previa (Diseño vs Video) ─────────────────────
  function showStageView() {
    stagePlaceholder.style.display = "block";
    finalVideoPlayer.style.display = "none";
    finalVideoPlayer.pause();
    if (btnViewStage) btnViewStage.classList.add("active");
    if (btnViewVideo) btnViewVideo.classList.remove("active");
  }

  function showVideoView() {
    stagePlaceholder.style.display = "none";
    finalVideoPlayer.style.display = "block";
    if (btnViewVideo) {
      btnViewVideo.classList.add("active");
      btnViewVideo.disabled = false;
    }
    if (btnViewStage) btnViewStage.classList.remove("active");
    finalVideoPlayer.play().catch(() => {});
  }

  if (btnViewStage) {
    btnViewStage.addEventListener("click", showStageView);
  }
  if (btnViewVideo) {
    btnViewVideo.addEventListener("click", () => {
      if (!btnViewVideo.disabled) showVideoView();
    });
  }

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
      const effectSelect = document.getElementById("effectTypeSelect");
      const aspectSelect = document.getElementById("aspectRatioSelect");
      const camSelect = document.getElementById("cameraMotionSelect");
      const subPosSelect = document.getElementById("subtitlePositionSelect");
      const animSelect = document.getElementById("subtitleAnimationSelect");
      const volumeInput = document.getElementById("musicVolume");

      let elapsed = 0;
      const progressInterval = setInterval(() => {
        elapsed += 5;
        if (elapsed === 5) {
          renderStatusText.textContent = "🎙️ Sintetizando voz y sincronizando audio...";
          renderStatusSub.textContent = "Generando locución con entonación natural...";
        } else if (elapsed === 10) {
          renderStatusText.textContent = "📝 Diseñando subtítulos dinámicos...";
          renderStatusSub.textContent = "Estilizando tipografía de alta retención viral...";
        } else if (elapsed === 18) {
          renderStatusText.textContent = "🎬 Componiendo movimiento de cámara y encuadre...";
          renderStatusSub.textContent = "Aplicando cinemática suave en 1080x1920 HD...";
        } else if (elapsed === 30) {
          renderStatusText.textContent = "✨ Renderizando efectos visuales y música...";
          renderStatusSub.textContent = "Mezclando piano de adoración y partículas sagradas...";
        } else if (elapsed >= 45) {
          renderStatusText.textContent = "⚡ Codificando video final (H.264 Ultrafast)...";
          renderStatusSub.textContent = "Casi listo, afinando calidad para Facebook Reels...";
        }
      }, 5000);

      const res = await fetch("/api/render-video", {
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
          subtitle_size: subtitleSizeSelect.value,
          subtitle_animation: animSelect ? animSelect.value : "pop",
          subtitle_position: subPosSelect ? subPosSelect.value : "bottom",
          camera_motion: camSelect ? camSelect.value : "none",
          music_track: musicSelect ? musicSelect.value : "worship_piano_peace",
          music_volume: volumeInput ? parseFloat(volumeInput.value) / 100.0 : 0.20,
          aspect_ratio: aspectSelect ? aspectSelect.value : "9:16",
          effect_type: effectSelect ? effectSelect.value : "cinematic_dust",
          theme_key: themeSelect ? themeSelect.value : "",
          hook_text: currentHookText || ""
        })
      });

      clearInterval(progressInterval);

      let data;
      const contentType = res.headers.get("content-type") || "";
      if (contentType.includes("application/json")) {
        const json = await res.json();
        if (!res.ok) {
          throw new Error(json.detail || json.message || "Error en el renderizado");
        }
        data = json;
      } else {
        const text = await res.text();
        if (!res.ok) {
          if (res.status === 504) {
            throw new Error("El renderizado tardó más de lo esperado. Por favor intenta de nuevo con un guion un poco más breve.");
          }
          throw new Error("Error del servidor (" + res.status + ")");
        }
        try {
          data = JSON.parse(text);
        } catch (_) {
          throw new Error("Respuesta no válida del servidor.");
        }
      }

      finalVideoPlayer.src = data.video_url;
      btnDownloadVideo.href = data.video_url;
      btnDownloadVideo.download = data.filename;
      videoActions.style.display = "block";
      showVideoView();

      loadRecentOutputs();
    } catch (e) {
      alert("Fallo al renderizar: " + e.message);
    } finally {
      renderOverlay.style.display = "none";
      btnRenderVideo.disabled = false;
    }
  }

  // 11. Copiar Texto y Hashtags para Facebook (Optimizado para SEO de Meta 2026)
  btnCopyCaption.addEventListener("click", () => {
    let caption = currentSeoCaption;
    if (!caption) {
      caption = `${scriptHook.value} 🙏✨\n\n${scriptBody.value}\n\n${scriptCta.value}\n\n#DailyPrayer #ChristianReels #FaithOverFear #JesusLovesYou`;
    }
    navigator.clipboard.writeText(caption).then(() => {
      btnCopyCaption.textContent = "✅ ¡Copiado con SEO y 4 Hashtags!";
      setTimeout(() => {
        btnCopyCaption.textContent = "📋 Copiar Texto del Post y Hashtags para Facebook";
      }, 2500);
    });
  });

  // 12. Cargar Biblioteca de Videos Recientes
  async function loadRecentOutputs() {
    try {
      const res = await fetch("/api/outputs");
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
          finalVideoPlayer.src = item.dataset.url;
          btnDownloadVideo.href = item.dataset.url;
          btnDownloadVideo.download = item.querySelector("span").textContent.replace("📹 ", "");
          videoActions.style.display = "block";
          showVideoView();
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
  if (videoModeSelect) {
    videoModeSelect.addEventListener("change", toggleVideoMode);
  }

  async function init() {
    await loadThemes();
    await loadVoices();
    await loadWorshipTracks();
    await loadBrollStatus();
    await loadImages();
    await loadRecentOutputs();
    await triggerGenerateScript();
    updateSubtitlePreview();
    updateSubtitlePosition();
    updateSubtitleAnimation();
    updateCameraMotionPreview();
    updateAspectRatioPreview();
    startFxLoop();
    toggleVideoMode();
    updatePuterStatus();
    setTimeout(updatePuterStatus, 1000);
    setTimeout(updatePuterStatus, 3000);
  }

  init();
}

bootstrapJesusStudio();
