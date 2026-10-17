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
  let currentScripture = "";
  let selectedImageName = "jesus_healing_miracle.jpg";
  let selectedImageName2 = null;
  let selectedImageName3 = null;
  let currentSceneTab = 1;
  let currentMicroCtaText = "";

  const microCtaInput = document.getElementById("microCtaInput");
  const chkEnableMicroCta = document.getElementById("chkEnableMicroCta");
  const stageMicroCtaBadge = document.getElementById("stageMicroCtaBadge");
  const hookBadgeInput = document.getElementById("hookBadgeInput");
  const chkEnableHookBadge = document.getElementById("chkEnableHookBadge");
  const hookBadgeStyleSelect = document.getElementById("hookBadgeStyleSelect");
  const btnRerollHookBadge = document.getElementById("btnRerollHookBadge");
  const stageHookBadge = document.getElementById("stageHookBadge");
  const btnRerollMagneticComment = document.getElementById("btnRerollMagneticComment");
  const transitionStyleSelect = document.getElementById("transitionStyleSelect");

  const btnTabScene1 = document.getElementById("btnTabScene1");
  const btnTabScene2 = document.getElementById("btnTabScene2");
  const btnTabScene3 = document.getElementById("btnTabScene3");
  const sceneStatusBanner = document.getElementById("sceneStatusBanner");
  const sceneStatusText = document.getElementById("sceneStatusText");
  const btnClearScene2 = document.getElementById("btnClearScene2");
  const btnClearScene3 = document.getElementById("btnClearScene3");
  const btnGenerateCardFromReel = document.getElementById("btnGenerateCardFromReel");

  const btnGenerate3ScenesAi = document.getElementById("btnGenerate3ScenesAi");
  const batchGenProgressBox = document.getElementById("batchGenProgressBox");
  const batchGenProgressText = document.getElementById("batchGenProgressText");
  const batchGenProgressSub = document.getElementById("batchGenProgressSub");
  const scene1PromptInput = document.getElementById("scene1PromptInput");
  const scene2PromptInput = document.getElementById("scene2PromptInput");
  const scene3PromptInput = document.getElementById("scene3PromptInput");
  const btnGenScene1Only = document.getElementById("btnGenScene1Only");
  const btnGenScene2Only = document.getElementById("btnGenScene2Only");
  const btnGenScene3Only = document.getElementById("btnGenScene3Only");

  function updateSceneTabsUI() {
    const tabs = [
      { tab: 1, btn: btnTabScene1 },
      { tab: 2, btn: btnTabScene2 },
      { tab: 3, btn: btnTabScene3 }
    ];
    tabs.forEach(t => {
      if (t.btn) {
        if (currentSceneTab === t.tab) {
          t.btn.classList.add("btn-primary");
          t.btn.classList.remove("btn-outline");
        } else {
          t.btn.classList.add("btn-outline");
          t.btn.classList.remove("btn-primary");
        }
      }
    });

    if (btnClearScene2) {
      btnClearScene2.style.display = selectedImageName2 ? "inline-block" : "none";
    }
    if (btnClearScene3) {
      btnClearScene3.style.display = selectedImageName3 ? "inline-block" : "none";
    }

    if (sceneStatusText) {
      if (currentSceneTab === 1) {
        sceneStatusText.innerHTML = `🎬 <strong>Escena 1 Activa (Apertura con Flash-Focus):</strong> Duración 0.0s a 3.2s. Selecciona abajo la foto de apertura.`;
      } else if (currentSceneTab === 2) {
        if (selectedImageName2) {
          sceneStatusText.innerHTML = `✨ <strong>Escena 2 Asignada (Intercesión):</strong> Punto de inflexión desde 3.2s hasta el 62% del video con pan suave.`;
        } else {
          sceneStatusText.innerHTML = `✨ <strong>Escena 2 Activa (Intercesión):</strong> Selecciona abajo la foto para el punto de inflexión.`;
        }
      } else if (currentSceneTab === 3) {
        if (selectedImageName3) {
          sceneStatusText.innerHTML = `🕊️ <strong>Escena 3 Asignada (Victoria y Paz):</strong> Conclusión desde el 62% al final con zoom continuo.`;
        } else {
          sceneStatusText.innerHTML = `🕊️ <strong>Escena 3 Activa (Victoria y Paz):</strong> Selecciona abajo la foto para la promesa de paz.`;
        }
      }
    }
  }

  if (btnTabScene1) {
    btnTabScene1.addEventListener("click", () => {
      currentSceneTab = 1;
      updateSceneTabsUI();
      stageSelectedImage.src = `/assets/images/${selectedImageName}`;
      loadImages();
    });
  }

  if (btnTabScene2) {
    btnTabScene2.addEventListener("click", () => {
      currentSceneTab = 2;
      updateSceneTabsUI();
      if (selectedImageName2) {
        stageSelectedImage.src = `/assets/images/${selectedImageName2}`;
      }
      loadImages();
    });
  }

  if (btnTabScene3) {
    btnTabScene3.addEventListener("click", () => {
      currentSceneTab = 3;
      updateSceneTabsUI();
      if (selectedImageName3) {
        stageSelectedImage.src = `/assets/images/${selectedImageName3}`;
      }
      loadImages();
    });
  }

  if (btnClearScene2) {
    btnClearScene2.addEventListener("click", () => {
      selectedImageName2 = null;
      if (currentSceneTab === 2) currentSceneTab = 1;
      updateSceneTabsUI();
      stageSelectedImage.src = `/assets/images/${selectedImageName}`;
      loadImages();
    });
  }

  if (btnClearScene3) {
    btnClearScene3.addEventListener("click", () => {
      selectedImageName3 = null;
      if (currentSceneTab === 3) currentSceneTab = 1;
      updateSceneTabsUI();
      stageSelectedImage.src = `/assets/images/${selectedImageName}`;
      loadImages();
    });
  }

  // Hook Badge Presets (Estrictamente intercesores y de fe - Cero frases prohibidas)
  const HOOK_BADGE_PRESETS = [
    "⚡ PRAYER FOR YOUR CHILDREN TONIGHT",
    "🙏 HEALING OVER YOUR TIRED MIND",
    "🛡️ GOD IS BREAKING EVERY HEAVY BURDEN",
    "🕊️ PEACE SURROUNDS YOUR HOME NOW",
    "✝️ JESUS HEALS WHAT NO ONE SEES",
    "🔥 THE LORD FIGHTS THIS BATTLE FOR YOU",
    "👑 HIS MERCIES ARE RENEWED RIGHT NOW"
  ];
  function updateHookBadgeStyle() {
    if (!stageHookBadge) return;
    const style = hookBadgeStyleSelect ? hookBadgeStyleSelect.value : "gold_cinematic";
    stageHookBadge.className = "stage-hook-badge";
    stageHookBadge.classList.add(`hook-style-${style}`);
  }

  if (hookBadgeStyleSelect) {
    hookBadgeStyleSelect.addEventListener("change", updateHookBadgeStyle);
    updateHookBadgeStyle();
  }

  if (chkEnableMicroCta) {
    chkEnableMicroCta.addEventListener("change", () => {
      if (stageMicroCtaBadge) {
        stageMicroCtaBadge.style.display = chkEnableMicroCta.checked ? "block" : "none";
      }
    });
  }

  if (microCtaInput) {
    microCtaInput.addEventListener("input", () => {
      if (stageMicroCtaBadge) {
        stageMicroCtaBadge.textContent = microCtaInput.value.trim();
      }
    });
  }

  if (btnRerollHookBadge) {
    btnRerollHookBadge.addEventListener("click", () => {
      hookPresetIdx = (hookPresetIdx + 1) % HOOK_BADGE_PRESETS.length;
      const nextBadge = HOOK_BADGE_PRESETS[hookPresetIdx];
      if (hookBadgeInput) hookBadgeInput.value = nextBadge;
      if (stageHookBadge) stageHookBadge.textContent = nextBadge;
    });
  }

  if (hookBadgeInput) {
    hookBadgeInput.addEventListener("input", () => {
      if (stageHookBadge) {
        const val = hookBadgeInput.value.trim().toUpperCase();
        stageHookBadge.textContent = val;
      }
    });
  }

  if (chkEnableHookBadge) {
    chkEnableHookBadge.addEventListener("change", () => {
      if (stageHookBadge) {
        stageHookBadge.style.display = chkEnableHookBadge.checked ? "block" : "none";
      }
    });
  }

  if (btnRerollMagneticComment) {
    btnRerollMagneticComment.addEventListener("click", async () => {
      try {
        const res = await fetch("/api/magnetic-comments");
        const comments = await res.json();
        if (comments && comments.length > 0) {
          const randComment = comments[Math.floor(Math.random() * comments.length)];
          scriptPinnedComment.value = randComment;
          currentPinnedComment = randComment;
        }
      } catch (_) {}
    });
  }

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
        .map(v => `<option value="${v.key}" ${v.key === "adam" || v.key === "christopher" ? "selected" : ""}>${v.name}</option>`)
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
        .map(img => {
          const isScene1 = img.filename === selectedImageName;
          const isScene2 = img.filename === selectedImageName2;
          const isScene3 = img.filename === selectedImageName3;
          const isSelected = (currentSceneTab === 1 && isScene1) || (currentSceneTab === 2 && isScene2) || (currentSceneTab === 3 && isScene3);
          return `
            <div class="image-thumb ${isSelected ? "selected" : ""}" data-filename="${img.filename}">
              ${isScene1 ? `<span class="scene-badge-indicator" title="Escena 1 (Apertura)">1</span>` : ''}
              ${isScene2 ? `<span class="scene-badge-indicator scene-2" title="Escena 2 (Intercesión)">2</span>` : ''}
              ${isScene3 ? `<span class="scene-badge-indicator scene-3" title="Escena 3 (Victoria)">3</span>` : ''}
              ${img.deletable ? `<button class="thumb-delete-btn" title="Eliminar foto de la galería" data-del="${img.filename}">🗑️</button>` : ''}
              <img src="${img.url}" alt="${img.label}">
              <div class="thumb-title">${img.label}</div>
            </div>
          `;
        })
        .join("");

      // Eventos de selección de imagen
      document.querySelectorAll(".image-thumb").forEach(thumb => {
        thumb.addEventListener("click", () => {
          const fname = thumb.dataset.filename;
          if (currentSceneTab === 1) {
            selectedImageName = fname;
            stageSelectedImage.src = `/assets/images/${selectedImageName}`;
          } else if (currentSceneTab === 2) {
            selectedImageName2 = fname;
            stageSelectedImage.src = `/assets/images/${selectedImageName2}`;
          } else {
            selectedImageName3 = fname;
            stageSelectedImage.src = `/assets/images/${selectedImageName3}`;
          }
          const stageBlurBg = document.getElementById("stageBlurBg");
          if (stageBlurBg) {
            const activeImg = currentSceneTab === 1 ? selectedImageName : (currentSceneTab === 2 ? (selectedImageName2 || selectedImageName) : (selectedImageName3 || selectedImageName));
            stageBlurBg.style.backgroundImage = `url('/assets/images/${activeImg}')`;
          }
          updateSceneTabsUI();
          loadImages();
          showStageView();
        });
      });

      // Eventos de eliminación de imagen
      document.querySelectorAll(".thumb-delete-btn").forEach(btn => {
        btn.addEventListener("click", async (e) => {
          e.stopPropagation();
          const fname = btn.dataset.del;
          if (!confirm("¿Deseas eliminar esta imagen de tu galería?")) return;
          try {
            const delRes = await fetch(`/api/images/${fname}`, { method: "DELETE" });
            if (delRes.ok) {
              if (selectedImageName === fname) {
                selectedImageName = "jesus_healing_miracle.jpg";
                stageSelectedImage.src = `/assets/images/${selectedImageName}`;
              }
              if (selectedImageName2 === fname) {
                selectedImageName2 = null;
              }
              if (selectedImageName3 === fname) {
                selectedImageName3 = null;
              }
              updateSceneTabsUI();
              await loadImages();
            } else {
              const errData = await delRes.json();
              alert(errData.detail || "No se pudo eliminar la imagen.");
            }
          } catch (err) {
            alert("Error al eliminar la imagen: " + err.message);
          }
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

      const badge = data.hook_badge_text || data.hook_text;
      if (badge) {
        currentHookText = badge;
        if (hookBadgeInput) hookBadgeInput.value = badge;
        if (stageHookBadge) {
          stageHookBadge.textContent = badge;
        }
      }

      if (data.micro_cta_text) {
        currentMicroCtaText = data.micro_cta_text;
        if (microCtaInput) microCtaInput.value = data.micro_cta_text;
        if (stageMicroCtaBadge) stageMicroCtaBadge.textContent = data.micro_cta_text;
      }

      if (data.scripture) {
        currentScripture = data.scripture;
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

      // Sincronizar automáticamente los prompts de las 3 escenas
      if (data.scene_1_prompt && scene1PromptInput) scene1PromptInput.value = data.scene_1_prompt;
      if (data.scene_2_prompt && scene2PromptInput) scene2PromptInput.value = data.scene_2_prompt;
      if (data.scene_3_prompt && scene3PromptInput) scene3PromptInput.value = data.scene_3_prompt;
      if (data.image_prompt) {
        aiImagePrompt.value = data.image_prompt;
      }

      // Auto-adaptar estilo de la insignia superior según la temática
      const tKey = (themeSelect.value || "").toLowerCase();
      if (hookBadgeStyleSelect) {
        if (tKey.includes("warfare") || tKey.includes("fear") || tKey.includes("addiction") || tKey.includes("court") || tKey.includes("debt")) {
          hookBadgeStyleSelect.value = "urgency_red";
        } else if (tKey.includes("majesty") || tKey.includes("glory") || tKey.includes("praise") || tKey.includes("harvest") || tKey.includes("favor")) {
          hookBadgeStyleSelect.value = "royal_navy";
        } else {
          hookBadgeStyleSelect.value = "gold_cinematic";
        }
        updateHookBadgeStyle();
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
      btnRerollPrompt.textContent = "🎲 Otras 3 Variantes";
    });
  }

  // 5. Sincronizar Prompts de las 3 Escenas según el Guion Editado
  async function triggerSyncPrompt() {
    const fullText = `${scriptHook.value} ${scriptBody.value} ${scriptCta.value}`.trim();
    if (!fullText) {
      alert("Primero escribe o genera un guion.");
      return;
    }

    btnSyncScriptToImage.disabled = true;
    btnSyncScriptToImage.textContent = "⏳ Creando las 3 Tomas que Coincidan con la Oración...";

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
      if (data.prompt) aiImagePrompt.value = data.prompt;
      if (data.scene_1_prompt && scene1PromptInput) scene1PromptInput.value = data.scene_1_prompt;
      if (data.scene_2_prompt && scene2PromptInput) scene2PromptInput.value = data.scene_2_prompt;
      if (data.scene_3_prompt && scene3PromptInput) scene3PromptInput.value = data.scene_3_prompt;

      btnSyncScriptToImage.textContent = "✅ ¡3 Escenas Sincronizadas con la Oración!";
      setTimeout(() => {
        btnSyncScriptToImage.textContent = "🪄 Sincronizar: Crear Prompts de las 3 Escenas para este Guion";
        btnSyncScriptToImage.disabled = false;
      }, 2500);

      // Desplazar suavemente hacia el generador de 3 escenas
      if (scene1PromptInput) {
        scene1PromptInput.scrollIntoView({ behavior: "smooth", block: "center" });
      }
    } catch (err) {
      alert("Error al sincronizar prompts: " + err.message);
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

  const btnPuterReset = document.getElementById("btnPuterReset");
  const puterCreditAlert = document.getElementById("puterCreditAlert");
  const btnSwitchAccountNow = document.getElementById("btnSwitchAccountNow");

  async function resetPuterSession() {
    try {
      if (typeof puter !== "undefined" && puter.auth) {
        await puter.auth.signOut();
      }
    } catch (_) {}

    // Limpiar tokens residuales en el navegador
    try {
      for (let i = localStorage.length - 1; i >= 0; i--) {
        const k = localStorage.key(i);
        if (k && (k.toLowerCase().includes("puter") || k.includes("token"))) {
          localStorage.removeItem(k);
        }
      }
      sessionStorage.clear();
    } catch (_) {}

    updatePuterStatus();
    if (puterCreditAlert) puterCreditAlert.style.display = "none";

    try {
      await puter.auth.signIn({ attempt_temp_user_creation: true });
      updatePuterStatus();
      alert("¡Sesión actualizada! Si conectaste otra cuenta o correo, ya tienes créditos nuevos para seguir generando con DALL-E 3.");
    } catch (err) {
      console.error("Error al conectar nueva cuenta Puter:", err);
      updatePuterStatus();
    }
  }

  if (btnPuterReset) {
    btnPuterReset.addEventListener("click", resetPuterSession);
  }
  if (btnSwitchAccountNow) {
    btnSwitchAccountNow.addEventListener("click", resetPuterSession);
  }

  // 8. Motor de Generación Cinemática de 3 Escenas con IA (DALL-E 3 / Flux HD)
  async function generateSingleScene(promptText, sceneNum = 1, label = "Escena") {
    let cleanPrompt = (promptText || "").trim();
    if (!cleanPrompt) {
      cleanPrompt = "Jesus Christ with compassionate loving eyes, gentle smile, holy warm golden light, cinematic 8k";
    }

    let enhancedPrompt = cleanPrompt;
    if (!enhancedPrompt.toLowerCase().includes("cinematic") && !enhancedPrompt.toLowerCase().includes("masterpiece")) {
      enhancedPrompt = `Ultra-realistic cinematic 8k portrait of ${cleanPrompt}, warm divine golden hour lighting, sacred holy atmosphere, highly detailed, dramatic, majestic, octane render, masterpiece, award winning photography, sharp focus`;
    }

    let savedFilename = null;
    let savedUrl = null;

    // Intento 1: DALL-E 3 a través de Puter si está disponible y autenticado
    let usedPuter = false;
    if (typeof puter !== "undefined" && puter.ai && puter.ai.txt2img && puter.auth && puter.auth.isSignedIn()) {
      try {
        const imgElement = await puter.ai.txt2img(enhancedPrompt);
        let blob;
        if (imgElement instanceof HTMLImageElement || (imgElement && imgElement.src)) {
          const response = await fetch(imgElement.src);
          blob = await response.blob();
        } else if (imgElement instanceof Blob) {
          blob = imgElement;
        }

        if (blob) {
          const file = new File([blob], `scene_${sceneNum}_${Date.now()}.png`, { type: "image/png" });
          const formData = new FormData();
          formData.append("file", file);
          const uploadRes = await fetch("/api/upload-image", { method: "POST", body: formData });
          if (uploadRes.ok) {
            const upData = await uploadRes.json();
            savedFilename = upData.filename;
            savedUrl = upData.url;
            usedPuter = true;
          }
        }
      } catch (puterErr) {
        console.warn("Fallo en Puter, recurriendo a motor Flux HD del servidor:", puterErr);
        const pMsg = extractError(puterErr);
        if (pMsg.toLowerCase().includes("credits") || pMsg.toLowerCase().includes("billing")) {
          if (puterCreditAlert) puterCreditAlert.style.display = "block";
        }
      }
    }

    // Intento 2 / Fallback: Servidor Flux HD (rápido, sin bloqueos ni requerir sesión)
    if (!savedFilename) {
      const res = await fetch("/api/generate-ai-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ prompt: enhancedPrompt, aspect_ratio: "9:16" })
      });
      if (!res.ok) {
        const errJson = await res.json().catch(() => ({}));
        throw new Error(errJson.detail || "Error en el servidor de imágenes.");
      }
      const data = await res.json();
      savedFilename = data.filename;
      savedUrl = data.url;
    }

    // Asignación automática a la escena correspondiente
    if (sceneNum === 1) {
      selectedImageName = savedFilename;
      stageSelectedImage.src = savedUrl;
      const stageBlurBg = document.getElementById("stageBlurBg");
      if (stageBlurBg) stageBlurBg.style.backgroundImage = `url('${savedUrl}')`;
    } else if (sceneNum === 2) {
      selectedImageName2 = savedFilename;
    } else if (sceneNum === 3) {
      selectedImageName3 = savedFilename;
    }

    return { filename: savedFilename, url: savedUrl, usedPuter };
  }

  // 8b. Generador en 1 Clic de las 3 Escenas (Crear y Asignar)
  async function generateAll3Scenes() {
    if (!btnGenerate3ScenesAi) return;
    btnGenerate3ScenesAi.disabled = true;

    // Asegurar que existan prompts para las 3 tomas
    let p1 = scene1PromptInput ? scene1PromptInput.value.trim() : "";
    let p2 = scene2PromptInput ? scene2PromptInput.value.trim() : "";
    let p3 = scene3PromptInput ? scene3PromptInput.value.trim() : "";

    if (!p1 || !p2 || !p3) {
      await triggerSyncPrompt();
      p1 = scene1PromptInput ? scene1PromptInput.value.trim() : "";
      p2 = scene2PromptInput ? scene2PromptInput.value.trim() : "";
      p3 = scene3PromptInput ? scene3PromptInput.value.trim() : "";
    }

    if (batchGenProgressBox) batchGenProgressBox.style.display = "block";

    try {
      // Paso 1: Toma 1 (Apertura)
      if (batchGenProgressText) batchGenProgressText.textContent = "🎬 Generando Escena 1 de 3 (Apertura e Impacto)...";
      if (batchGenProgressSub) batchGenProgressSub.textContent = "Creando iluminación dorada y encuadre inicial (0-3.2s)...";
      await generateSingleScene(p1, 1, "Toma 1 (Apertura)");
      await loadImages();
      updateSceneTabsUI();

      // Paso 2: Toma 2 (Intercesión)
      if (batchGenProgressText) batchGenProgressText.textContent = "✨ Generando Escena 2 de 3 (Intercesión y Oración)...";
      if (batchGenProgressSub) batchGenProgressSub.textContent = "Creando punto de inflexión de fe y presencia sagrada (3.2s-10s)...";
      await generateSingleScene(p2, 2, "Toma 2 (Intercesión)");
      await loadImages();
      updateSceneTabsUI();

      // Paso 3: Toma 3 (Victoria)
      if (batchGenProgressText) batchGenProgressText.textContent = "🕊️ Generando Escena 3 de 3 (Victoria y Paz)...";
      if (batchGenProgressSub) batchGenProgressSub.textContent = "Creando desenlace glorioso y promesa divina (10s al final)...";
      await generateSingleScene(p3, 3, "Toma 3 (Victoria)");
      await loadImages();
      updateSceneTabsUI();

      if (batchGenProgressText) batchGenProgressText.textContent = "✅ ¡Las 3 Escenas fueron creadas y asignadas en 1 clic!";
      if (batchGenProgressSub) batchGenProgressSub.textContent = "Asignadas con éxito a las posiciones [1], [2] y [3] de tu Reel.";

      showStageView();
      setTimeout(() => {
        if (batchGenProgressBox) batchGenProgressBox.style.display = "none";
      }, 4000);

    } catch (err) {
      console.error("Error al generar las 3 escenas:", err);
      alert("Aviso al crear las 3 escenas: " + extractError(err));
      if (batchGenProgressBox) batchGenProgressBox.style.display = "none";
    } finally {
      btnGenerate3ScenesAi.disabled = false;
      btnGenerate3ScenesAi.textContent = "🚀 GENERAR LAS 3 ESCENAS CON IA EN 1 CLIC (CREAR Y ASIGNAR)";
    }
  }

  if (btnGenerate3ScenesAi) {
    btnGenerate3ScenesAi.addEventListener("click", generateAll3Scenes);
  }

  // Generadores individuales para afinar tomas específicas
  if (btnGenScene1Only) {
    btnGenScene1Only.addEventListener("click", async () => {
      btnGenScene1Only.disabled = true;
      btnGenScene1Only.textContent = "⏳ Creando 1...";
      try {
        const p1 = scene1PromptInput ? scene1PromptInput.value.trim() : "";
        await generateSingleScene(p1, 1, "Toma 1");
        await loadImages();
        updateSceneTabsUI();
        showStageView();
      } catch (e) { alert("Error: " + extractError(e)); }
      finally {
        btnGenScene1Only.disabled = false;
        btnGenScene1Only.textContent = "🎨 Crear solo Toma 1";
      }
    });
  }

  if (btnGenScene2Only) {
    btnGenScene2Only.addEventListener("click", async () => {
      btnGenScene2Only.disabled = true;
      btnGenScene2Only.textContent = "⏳ Creando 2...";
      try {
        const p2 = scene2PromptInput ? scene2PromptInput.value.trim() : "";
        await generateSingleScene(p2, 2, "Toma 2");
        await loadImages();
        updateSceneTabsUI();
      } catch (e) { alert("Error: " + extractError(e)); }
      finally {
        btnGenScene2Only.disabled = false;
        btnGenScene2Only.textContent = "🎨 Crear solo Toma 2";
      }
    });
  }

  if (btnGenScene3Only) {
    btnGenScene3Only.addEventListener("click", async () => {
      btnGenScene3Only.disabled = true;
      btnGenScene3Only.textContent = "⏳ Creando 3...";
      try {
        const p3 = scene3PromptInput ? scene3PromptInput.value.trim() : "";
        await generateSingleScene(p3, 3, "Toma 3");
        await loadImages();
        updateSceneTabsUI();
      } catch (e) { alert("Error: " + extractError(e)); }
      finally {
        btnGenScene3Only.disabled = false;
        btnGenScene3Only.textContent = "🎨 Crear solo Toma 3";
      }
    });
  }

  if (btnGenerateAiImage) {
    btnGenerateAiImage.addEventListener("click", async () => {
      btnGenerateAiImage.disabled = true;
      btnGenerateAiImage.textContent = "⏳ Creando...";
      try {
        const p = aiImagePrompt ? aiImagePrompt.value.trim() : "";
        await generateSingleScene(p, currentSceneTab);
        await loadImages();
        updateSceneTabsUI();
        showStageView();
      } catch (e) { alert("Error: " + extractError(e)); }
      finally {
        btnGenerateAiImage.disabled = false;
        btnGenerateAiImage.textContent = "🎨 Crear Imagen con IA (Alta Resolución)";
      }
    });
  }

  // 9. Actualizar Vista Previa de Subtítulos al Cambiar Estilo
  function updateSubtitlePreview() {
    const style = subtitleStyleSelect.value;
    const isLarge = subtitleSizeSelect.value === "large";

    liveSubPreview.style.fontSize = isLarge ? "28px" : "22px";

    if (style === "gold_highlight") {
      liveSubPreview.innerHTML = `<span style="font-family: Impact, Anton, sans-serif; letter-spacing: 0.5px;">GOD IS <span class="highlight" style="color: #ffd700; text-shadow: 0 0 10px rgba(255,215,0,0.4);">WITH YOU</span></span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "neon_cyan") {
      liveSubPreview.innerHTML = `<span style="font-family: 'Bebas Neue', Impact, sans-serif; letter-spacing: 1.5px; font-size: 1.15em;">GOD IS <span class="highlight" style="color: #00ffcc;">WITH YOU</span></span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "holy_scripture") {
      liveSubPreview.innerHTML = `<span style="font-family: 'Liberation Serif', Georgia, serif; font-style: italic; color: #f0f8ff;">THE LORD <span style="color: #ffd700; text-shadow: 0 2px 8px rgba(0,0,0,0.8);">IS WITH YOU</span></span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "fire_coral") {
      liveSubPreview.innerHTML = `<span style="font-family: Impact, Anton, sans-serif;">GOD IS <span class="highlight" style="color: #ff3b10;">WITH YOU</span></span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "black_box") {
      liveSubPreview.innerHTML = `<span style="font-family: Roboto, sans-serif; background: rgba(0,0,0,0.88); color: #ffff00; padding: 4px 12px; border-radius: 4px; font-weight: 800;">GOD IS WITH YOU</span>`;
      liveSubPreview.style.background = "transparent";
      liveSubPreview.style.padding = "0";
    } else if (style === "pure_minimal") {
      liveSubPreview.innerHTML = `<span style="font-family: Roboto, sans-serif; color: #ffffff; text-shadow: 0 2px 10px rgba(0,0,0,0.9); font-weight: 500;">GOD IS WITH YOU</span>`;
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
      // Fuego y Unción del Espíritu Santo (Chispas ámbar sagrado, dorado y resplandor cálido)
      particles.forEach(p => {
        p.y -= p.speedY * 1.4;
        p.x += p.speedX * 0.8;
        p.pulseVal += p.pulseSpeed * 1.3;
        const currentAlpha = p.alpha * (0.6 + 0.4 * Math.sin(p.pulseVal));

        if (p.y < -10) {
          p.y = h + 10;
          p.x = Math.random() * w;
        }

        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius * 0.9, 0, Math.PI * 2);
        fxCtx.fillStyle = p.radius > 2.5 ? `rgba(255, 175, 20, ${currentAlpha})` : `rgba(255, 220, 70, ${currentAlpha})`;
        fxCtx.shadowColor = "#ffb700";
        fxCtx.shadowBlur = 10;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "celestial_bloom") {
      // Resplandor de Gloria (Bloom Celestial suave y aura angelical)
      const time = Date.now() * 0.0015;
      const pulse = 0.12 + 0.05 * Math.sin(time);
      const gradient = fxCtx.createRadialGradient(w / 2, h * 0.35, 10, w / 2, h * 0.35, w * 0.8);
      gradient.addColorStop(0, `rgba(255, 255, 240, ${pulse * 1.2})`);
      gradient.addColorStop(0.6, `rgba(255, 235, 180, ${pulse * 0.5})`);
      gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
      fxCtx.fillStyle = gradient;
      fxCtx.fillRect(0, 0, w, h);

      particles.forEach(p => {
        p.y -= p.speedY * 0.5;
        p.pulseVal += p.pulseSpeed;
        const currentAlpha = p.alpha * 0.6;
        if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius * 1.1, 0, Math.PI * 2);
        fxCtx.fillStyle = `rgba(255, 255, 255, ${currentAlpha})`;
        fxCtx.shadowColor = "#fff8db";
        fxCtx.shadowBlur = 12;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "dawn_hope") {
      // Amanecer de Esperanza (Gradiente de alba con rayos suaves)
      const gradient = fxCtx.createLinearGradient(0, 0, 0, h);
      gradient.addColorStop(0, "rgba(255, 215, 140, 0.14)");
      gradient.addColorStop(0.5, "rgba(255, 180, 100, 0.08)");
      gradient.addColorStop(1, "rgba(0, 0, 0, 0.02)");
      fxCtx.fillStyle = gradient;
      fxCtx.fillRect(0, 0, w, h);

      particles.forEach(p => {
        p.y -= p.speedY * 0.7;
        p.pulseVal += p.pulseSpeed;
        const currentAlpha = p.alpha * 0.65;
        if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        fxCtx.fillStyle = `rgba(255, 230, 150, ${currentAlpha})`;
        fxCtx.shadowColor = "#ffe082";
        fxCtx.shadowBlur = 8;
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
          image_name_2: selectedImageName2 || "none",
          image_name_3: selectedImageName3 || "none",
          subtitle_style: subtitleStyleSelect.value,
          subtitle_size: subtitleSizeSelect.value,
          subtitle_animation: animSelect ? animSelect.value : "pop",
          subtitle_position: subPosSelect ? subPosSelect.value : "bottom",
          camera_motion: camSelect ? camSelect.value : "none",
          transition_style: transitionStyleSelect ? transitionStyleSelect.value : "fade",
          music_track: musicSelect ? musicSelect.value : "worship_piano_peace",
          music_volume: volumeInput ? parseFloat(volumeInput.value) / 100.0 : 0.20,
          aspect_ratio: aspectSelect ? aspectSelect.value : "9:16",
          effect_type: effectSelect ? effectSelect.value : "cinematic_dust",
          theme_key: themeSelect ? themeSelect.value : "",
          hook_text: (chkEnableHookBadge && chkEnableHookBadge.checked && hookBadgeInput) ? hookBadgeInput.value.trim() : "",
          hook_badge_style: hookBadgeStyleSelect ? hookBadgeStyleSelect.value : "gold_cinematic",
          micro_cta_text: (chkEnableMicroCta && chkEnableMicroCta.checked && microCtaInput) ? microCtaInput.value.trim() : ""
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
  if (btnCopyCaption) {
    btnCopyCaption.addEventListener("click", () => {
      const hook = scriptHook ? scriptHook.value.trim() : "";
      const body = scriptBody ? scriptBody.value.trim() : "";
      const cta = scriptCta ? scriptCta.value.trim() : "";
      const pinned = currentPinnedComment || (scriptPinnedComment ? scriptPinnedComment.value.trim() : "");
      const scriptureText = currentScripture ? `📖 SCRIPTURE TODAY:\n"${currentScripture}"\n\n` : "";

      let caption = `⚡ ${hook}\n\n${body}\n\n${scriptureText}${cta}\n\n👇 COMMENT BELOW:\n${pinned ? `"${pinned}"` : "Leave your first name or write 'AMEN' to agree in faith tonight."}\n\n#DailyPrayer #ChristianReels #JesusLovesYou #FaithOverFear #MiracleWorker`;

      navigator.clipboard.writeText(caption).then(() => {
        btnCopyCaption.textContent = "✅ ¡Publicación Viral Completa Copiada!";
        setTimeout(() => {
          btnCopyCaption.textContent = "📋 Copiar Publicación Completa para Facebook (Copy Viral SEO)";
        }, 2500);
      }).catch(err => {
        alert("No se pudo copiar automáticamente: " + err);
      });
    });
  }

  // 11b. Generar Tarjeta de Oración 4:5 para Facebook Feed (1080x1350)
  if (btnGenerateCardFromReel) {
    btnGenerateCardFromReel.addEventListener("click", async () => {
      btnGenerateCardFromReel.disabled = true;
      const originalText = btnGenerateCardFromReel.innerHTML;
      btnGenerateCardFromReel.innerHTML = "⏳ Generando Tarjeta 4:5 (1080x1350)...";

      try {
        const themeOption = themeSelect && themeSelect.options[themeSelect.selectedIndex];
        let rawTitle = themeOption ? themeOption.text : "DAILY BLESSING";
        rawTitle = rawTitle.replace(/^[\p{Emoji}\s]+/u, '').trim().toUpperCase();
        if (!rawTitle) rawTitle = "PRAYER OF FAITH";

        const prayer = (scriptBody ? scriptBody.value.trim() : "") || (scriptHook ? scriptHook.value.trim() : "May the Lord bless you and keep you today.");
        const verse = currentScripture || "Numbers 6:24-26";

        const res = await fetch("/api/render-image-card", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            background_image_path: selectedImageName,
            title: rawTitle,
            prayer_text: prayer,
            verse_footer: verse
          })
        });

        const data = await res.json();
        if (data.success && data.card_url) {
          const win = window.open(data.card_url, "_blank");
          if (!win) {
            alert(`¡Tarjeta 4:5 creada con éxito!\nPuedes verla y descargarla aquí: ${data.card_url}`);
          }
        } else {
          throw new Error(data.error || "No se pudo crear la tarjeta de oración.");
        }
      } catch (err) {
        alert("Error al generar la tarjeta de oración 4:5: " + err.message);
      } finally {
        btnGenerateCardFromReel.disabled = false;
        btnGenerateCardFromReel.innerHTML = originalText;
      }
    });
  }

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

  // 13. Modal y Planificador de Lote Diario (3 Videos del Día)
  const btnOpenDailyBatch = document.getElementById("btnOpenDailyBatch");
  const dailyBatchModal = document.getElementById("dailyBatchModal");
  const btnCloseDailyBatch = document.getElementById("btnCloseDailyBatch");
  const dailyBatchContent = document.getElementById("dailyBatchContent");

  async function openDailyBatchModal() {
    if (!dailyBatchModal) return;
    dailyBatchModal.style.display = "flex";
    if (dailyBatchContent) {
      dailyBatchContent.innerHTML = `<p style="color: #cbd5e1; text-align: center; padding: 25px;">⏳ Cargando planificación para hoy (3 horarios clave)...</p>`;
    }
    try {
      const res = await fetch("/api/daily-batch");
      const batch = await res.json();
      if (!dailyBatchContent) return;
      dailyBatchContent.innerHTML = batch.map((item, idx) => `
        <div class="daily-batch-card" style="background: rgba(15, 23, 42, 0.7); border: 1px solid rgba(255, 215, 0, 0.25); border-radius: 10px; padding: 16px;">
          <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 8px; margin-bottom: 10px;">
            <div>
              <span style="font-weight: 700; color: #ffd700; font-size: 15px;">${item.time_label}</span>
              <span style="display: block; font-size: 12px; color: #94a3b8;">${item.purpose}</span>
            </div>
            <div style="display: flex; gap: 6px;">
              <button type="button" class="btn btn-sm btn-gold btn-load-batch-slot" data-slot-index="${idx}" style="font-weight: 700;">
                ⚡ Cargar en el Estudio
              </button>
              <button type="button" class="btn btn-sm btn-outline btn-card-batch-slot" data-slot-index="${idx}" style="font-weight: 700;" title="Generar Tarjeta 4:5 para Facebook Feed">
                🖼️ Tarjeta 4:5
              </button>
            </div>
          </div>
          <div style="font-size: 13px; color: #e2e8f0; margin-bottom: 6px;">
            <strong>🎣 Gancho:</strong> <em>"${item.script.hook}"</em>
          </div>
          <div style="font-size: 12px; color: #cbd5e1; margin-bottom: 6px;">
            <strong>📖 Escritura:</strong> ${item.script.scripture || "Jeremiah 29:11"}
          </div>
          <div style="font-size: 11.5px; color: #a1a1aa;">
            💬 <strong>Comentario Fijado:</strong> ${item.script.pinned_comment}
          </div>
        </div>
      `).join("");

      // Cargar slot en el estudio (3 escenas completas)
      document.querySelectorAll(".btn-load-batch-slot").forEach(btn => {
        btn.addEventListener("click", () => {
          const sIdx = parseInt(btn.dataset.slotIndex, 10);
          const selectedSlot = batch[sIdx];
          if (!selectedSlot) return;

          if (themeSelect && selectedSlot.script.theme_key) {
            themeSelect.value = selectedSlot.script.theme_key;
          }
          if (scriptHook) scriptHook.value = selectedSlot.script.hook;
          if (scriptBody) scriptBody.value = selectedSlot.script.body;
          if (scriptCta) scriptCta.value = selectedSlot.script.cta;
          if (scriptPinnedComment) scriptPinnedComment.value = selectedSlot.script.pinned_comment;
          currentPinnedComment = selectedSlot.script.pinned_comment;
          currentScripture = selectedSlot.script.scripture || "";

          const badge = selectedSlot.script.hook_badge_text || selectedSlot.script.hook_text;
          if (badge) {
            currentHookText = badge;
            if (hookBadgeInput) hookBadgeInput.value = badge;
            if (stageHookBadge) stageHookBadge.textContent = badge;
          }

          if (selectedSlot.script.micro_cta_text) {
            currentMicroCtaText = selectedSlot.script.micro_cta_text;
            if (microCtaInput) microCtaInput.value = selectedSlot.script.micro_cta_text;
          }

          if (aiImagePrompt && selectedSlot.script.image_prompt) {
            aiImagePrompt.value = selectedSlot.script.image_prompt;
          }

          if (selectedSlot.recommended_image) {
            selectedImageName = selectedSlot.recommended_image;
          }
          if (selectedSlot.recommended_image_2) {
            selectedImageName2 = selectedSlot.recommended_image_2;
          }
          if (selectedSlot.recommended_image_3) {
            selectedImageName3 = selectedSlot.recommended_image_3;
          }

          if (stageSelectedImage) stageSelectedImage.src = `/assets/images/${selectedImageName}`;
          const stageBlurBg = document.getElementById("stageBlurBg");
          if (stageBlurBg) stageBlurBg.style.backgroundImage = `url('/assets/images/${selectedImageName}')`;

          if (musicSelect && selectedSlot.recommended_music) {
            musicSelect.value = selectedSlot.recommended_music;
          }

          dailyBatchModal.style.display = "none";
          showStageView();
          updateSceneTabsUI();
          loadImages();
          alert(`¡Reel de ${selectedSlot.time_label} cargado con 3 escenas en el estudio! Revisa los campos y pulsa "Generar Reel Viral".`);
        });
      });

      // Generar tarjeta 4:5 desde el lote diario
      document.querySelectorAll(".btn-card-batch-slot").forEach(btn => {
        btn.addEventListener("click", async (e) => {
          e.stopPropagation();
          const sIdx = parseInt(btn.dataset.slotIndex, 10);
          const slot = batch[sIdx];
          if (!slot) return;
          btn.disabled = true;
          const orig = btn.innerHTML;
          btn.innerHTML = "⏳ Creando...";
          try {
            const rawTitle = slot.purpose ? slot.purpose.replace(/^[\p{Emoji}\s]+/u, '').trim().toUpperCase() : "PRAYER OF FAITH";
            const res = await fetch("/api/render-image-card", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                background_image_path: slot.recommended_image || "jesus_holy_bible.jpg",
                title: rawTitle,
                prayer_text: slot.script.body,
                verse_footer: slot.script.scripture || "Jeremiah 29:11"
              })
            });
            const data = await res.json();
            if (data.success && data.card_url) {
              window.open(data.card_url, "_blank");
            } else {
              alert("Error: " + (data.error || "No se pudo generar la tarjeta"));
            }
          } catch (err) {
            alert("Error al generar tarjeta: " + err.message);
          } finally {
            btn.disabled = false;
            btn.innerHTML = orig;
          }
        });
      });
    } catch (e) {
      if (dailyBatchContent) {
        dailyBatchContent.innerHTML = `<p style="color: #ef4444; text-align: center;">Error al cargar el lote diario: ${e.message}</p>`;
      }
    }
  }

  if (btnOpenDailyBatch) {
    btnOpenDailyBatch.addEventListener("click", openDailyBatchModal);
  }
  if (btnCloseDailyBatch) {
    btnCloseDailyBatch.addEventListener("click", () => {
      if (dailyBatchModal) dailyBatchModal.style.display = "none";
    });
  }
  if (dailyBatchModal) {
    dailyBatchModal.addEventListener("click", (e) => {
      if (e.target === dailyBatchModal) dailyBatchModal.style.display = "none";
    });
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
