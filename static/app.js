function bootstrapJesusStudio() {
  const themeSelect = document.getElementById("themeSelect");
  if (!themeSelect) {
    setTimeout(bootstrapJesusStudio, 60);
    return;
  }

  // Elementos de la interfaz
  const customTopic = document.getElementById("customTopic");
  const scriptDurationMode = document.getElementById("scriptDurationMode");
  const scriptDurationEstimate = document.getElementById("scriptDurationEstimate");
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
  const hookBadgeFontSelect = document.getElementById("hookBadgeFontSelect");
  const hookBadgeSizeSelect = document.getElementById("hookBadgeSizeSelect");
  const btnRerollHookBadge = document.getElementById("btnRerollHookBadge");
  const stageHookBadge = document.getElementById("stageHookBadge");
  const btnPreviewShowHook = document.getElementById("btnPreviewShowHook");
  const btnPreviewShowCta = document.getElementById("btnPreviewShowCta");
  const formatPillGroup = document.getElementById("formatPillGroup");
  const aspectRatioSelect = document.getElementById("aspectRatioSelect");
  const btnRerollMagneticComment = document.getElementById("btnRerollMagneticComment");
  const transitionStyleSelect = document.getElementById("transitionStyleSelect");
  const chkSeamlessLoop = document.getElementById("chkSeamlessLoop");
  const chkEnableSfx = document.getElementById("chkEnableSfx");
  const chkMasterLufs = document.getElementById("chkMasterLufs");
  const chkGenerateTrendingAudio = document.getElementById("chkGenerateTrendingAudio");
  const btnDownloadTrendingAudioVideo = document.getElementById("btnDownloadTrendingAudioVideo");

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

  // Modo de Producción (Reels 9:16 vs Tarjetas Feed 4:5)
  const tabModeReels = document.getElementById("tabModeReels");
  const tabModeFeedCards = document.getElementById("tabModeFeedCards");
  const btnOpenDailyBatchTop = document.getElementById("btnOpenDailyBatchTop");
  const workspaceReels = document.getElementById("workspaceReels");
  const workspaceCards = document.getElementById("workspaceCards");

  // Estudio de Tarjetas de Oración 4:5
  const cardThemeSelect = document.getElementById("cardThemeSelect");
  const btnSyncCardTheme = document.getElementById("btnSyncCardTheme");
  const cardTitleInput = document.getElementById("cardTitleInput");
  const cardPrayerInput = document.getElementById("cardPrayerInput");
  const btnRerollCardPrayer = document.getElementById("btnRerollCardPrayer");
  const cardVerseInput = document.getElementById("cardVerseInput");
  const chkCardWatermark = document.getElementById("chkCardWatermark");
  const cardWatermarkInput = document.getElementById("cardWatermarkInput");
  const cardGalleryPicker = document.getElementById("cardGalleryPicker");
  const cardImageUpload = document.getElementById("cardImageUpload");
  const btnRenderCard = document.getElementById("btnRenderCard");
  const cardResultImg = document.getElementById("cardResultImg");
  const cardRenderOverlay = document.getElementById("cardRenderOverlay");
  const btnDownloadCard = document.getElementById("btnDownloadCard");
  const btnCopyCardFeedPost = document.getElementById("btnCopyCardFeedPost");
  const btnCopyCardPinnedComment = document.getElementById("btnCopyCardPinnedComment");
  const cardFeedCopyText = document.getElementById("cardFeedCopyText");
  const cardAiPrompt = document.getElementById("cardAiPrompt");
  const cardAiProviderSelect = document.getElementById("cardAiProviderSelect");
  const btnGenerateCardAiImage = document.getElementById("btnGenerateCardAiImage");
  const chkAutoCardImage = document.getElementById("chkAutoCardImage");
  const cardAiImageStatusBadge = document.getElementById("cardAiImageStatusBadge");
  const cardOverlayTitle = document.getElementById("cardOverlayTitle");
  const cardOverlayDesc = document.getElementById("cardOverlayDesc");

  let cardSelectedImageName = "jesus_healing_miracle.jpg";
  let cardCurrentPinnedComment = "";
  let cardStudioInitialized = false;

  function updateShelfThumbnails() {
    const t1 = document.getElementById("previewThumbScene1");
    const t2 = document.getElementById("previewThumbScene2");
    const t3 = document.getElementById("previewThumbScene3");
    const img1 = document.getElementById("shelfImgScene1");
    const img2 = document.getElementById("shelfImgScene2");
    const img3 = document.getElementById("shelfImgScene3");

    if (img1 && selectedImageName) {
      img1.src = (selectedImageName.startsWith("data:") || selectedImageName.startsWith("blob:") || selectedImageName.startsWith("http")) 
        ? selectedImageName 
        : `/assets/images/${selectedImageName}`;
    }
    if (img2) {
      if (selectedImageName2) {
        img2.src = (selectedImageName2.startsWith("data:") || selectedImageName2.startsWith("blob:") || selectedImageName2.startsWith("http"))
          ? selectedImageName2
          : `/assets/images/${selectedImageName2}`;
      } else {
        img2.src = "/assets/images/jesus_reaching_hand.jpg";
      }
    }
    if (img3) {
      if (selectedImageName3) {
        img3.src = (selectedImageName3.startsWith("data:") || selectedImageName3.startsWith("blob:") || selectedImageName3.startsWith("http"))
          ? selectedImageName3
          : `/assets/images/${selectedImageName3}`;
      } else {
        img3.src = "/assets/images/jesus_walking_storm.jpg";
      }
    }

    if (t1) t1.classList.toggle("active", currentSceneTab === 1);
    if (t2) t2.classList.toggle("active", currentSceneTab === 2);
    if (t3) t3.classList.toggle("active", currentSceneTab === 3);
  }

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

    updateShelfThumbnails();
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
  let hookPresetIdx = 0;
  const HOOK_BADGE_PRESETS = [
    "⚡ PRAYER FOR YOUR CHILDREN TONIGHT",
    "🙏 HEALING OVER YOUR TIRED MIND",
    "🛡️ GOD IS BREAKING EVERY HEAVY BURDEN",
    "🕊️ PEACE SURROUNDS YOUR HOME NOW",
    "✝️ JESUS HEALS WHAT NO ONE SEES",
    "🔥 THE LORD FIGHTS THIS BATTLE FOR YOU",
    "👑 HIS MERCIES ARE RENEWED RIGHT NOW",
    "✨ PROMISES OF RESTORATION FOR YOUR HOME",
    "🛡️ NO WEAPON FORMED AGAINST YOU SHALL PROSPER",
    "🌿 GRACE AND PROTECTION OVER YOUR HEALTH",
    "💧 AN END TO ANXIETY AND SILENT TEARS",
    "⚔️ GOD HAS ALREADY DECLARED YOUR VICTORY",
    "🌅 JOY COMES IN THE MORNING",
    "🙌 YOUR FAMILY IS IN GOD'S HANDS",
    "📖 HE WHO BEGAN A GOOD WORK WILL COMPLETE IT",
    "🕊️ UNCONDITIONAL FORGIVENESS AND NEW LIFE"
  ];

  function updateHookBadgeAppearance() {
    if (!stageHookBadge) return;
    const style = hookBadgeStyleSelect ? hookBadgeStyleSelect.value : "gold_luxury";
    const font = hookBadgeFontSelect ? hookBadgeFontSelect.value.replace(/\s+/g, "_") : "Montserrat";
    const size = hookBadgeSizeSelect ? hookBadgeSizeSelect.value : "normal";

    stageHookBadge.className = "stage-hook-badge";
    stageHookBadge.classList.add(`hook-style-${style}`);
    stageHookBadge.classList.add(`hook-font-${font}`);
    stageHookBadge.classList.add(`hook-size-${size}`);
  }
  const updateHookBadgeStyle = updateHookBadgeAppearance;

  if (hookBadgeStyleSelect) {
    hookBadgeStyleSelect.addEventListener("change", updateHookBadgeAppearance);
  }
  if (hookBadgeFontSelect) {
    hookBadgeFontSelect.addEventListener("change", updateHookBadgeAppearance);
  }
  if (hookBadgeSizeSelect) {
    hookBadgeSizeSelect.addEventListener("change", updateHookBadgeAppearance);
  }
  updateHookBadgeAppearance();

  // Selector de Capas en la Vista Previa (Gancho vs Píldora - Desfasadas en tiempo)
  if (btnPreviewShowHook) {
    btnPreviewShowHook.addEventListener("click", () => {
      btnPreviewShowHook.classList.add("active");
      if (btnPreviewShowCta) btnPreviewShowCta.classList.remove("active");
      if (stageHookBadge) {
        stageHookBadge.style.display = (chkEnableHookBadge && chkEnableHookBadge.checked) ? "block" : "none";
      }
      if (stageMicroCtaBadge) {
        stageMicroCtaBadge.style.display = "none";
      }
    });
  }

  if (btnPreviewShowCta) {
    btnPreviewShowCta.addEventListener("click", () => {
      btnPreviewShowCta.classList.add("active");
      if (btnPreviewShowHook) btnPreviewShowHook.classList.remove("active");
      if (stageMicroCtaBadge) {
        stageMicroCtaBadge.style.display = (chkEnableMicroCta && chkEnableMicroCta.checked) ? "block" : "none";
      }
      if (stageHookBadge) {
        stageHookBadge.style.display = "none";
      }
    });
  }

  if (chkEnableMicroCta) {
    chkEnableMicroCta.addEventListener("change", () => {
      if (stageMicroCtaBadge && btnPreviewShowCta && btnPreviewShowCta.classList.contains("active")) {
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
      if (hookBadgeInput) {
        hookBadgeInput.value = nextBadge;
      }
      if (stageHookBadge) {
        stageHookBadge.textContent = nextBadge;
        stageHookBadge.style.animation = "none";
        void stageHookBadge.offsetWidth;
        stageHookBadge.style.animation = "badgePop 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.275)";
      }
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
      if (stageHookBadge && (!btnPreviewShowCta || !btnPreviewShowCta.classList.contains("active"))) {
        stageHookBadge.style.display = chkEnableHookBadge.checked ? "block" : "none";
      }
    });
  }

  // Sincronización del Selector de Formato Inicial (Píldoras 9:16 / 1:1 / 16:9)
  if (formatPillGroup) {
    const pills = formatPillGroup.querySelectorAll(".btn-format-pill");
    pills.forEach(pill => {
      pill.addEventListener("click", () => {
        pills.forEach(p => p.classList.remove("active"));
        pill.classList.add("active");
        const ratio = pill.dataset.ratio || "9:16";
        if (aspectRatioSelect) {
          aspectRatioSelect.value = ratio;
        }
        updateAspectRatioPreview(ratio);
      });
    });
  }
  if (aspectRatioSelect) {
    aspectRatioSelect.addEventListener("change", () => {
      const val = aspectRatioSelect.value;
      if (formatPillGroup) {
        const pills = formatPillGroup.querySelectorAll(".btn-format-pill");
        pills.forEach(p => {
          p.classList.toggle("active", p.dataset.ratio === val);
        });
      }
      updateAspectRatioPreview(val);
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

  function updateProjectTitle() {
    const currentProjectTitle = document.getElementById("currentProjectTitle");
    if (currentProjectTitle && themeSelect && themeSelect.selectedIndex >= 0) {
      const selectedOption = themeSelect.options[themeSelect.selectedIndex];
      if (selectedOption) {
        currentProjectTitle.textContent = `Reel: ${selectedOption.textContent}`;
      }
    }
  }

  // Cinco pilares visibles; los 26 temas originales se conservan.
  const THEME_PILLAR_LABELS = {
    family_relationships: "1 · Familia y relaciones",
    peace_rest_daily: "2 · Paz, descanso y oración cotidiana",
    grief_solitude_comfort: "3 · Duelo, soledad y acompañamiento",
    faith_hope_trials: "4 · Fe y esperanza en las dificultades",
    gratitude_wisdom_growth: "5 · Gratitud y crecimiento espiritual"
  };

  function escapeThemeOption(value) {
    return String(value ?? "").replace(/[&<>"']/g, ch => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;"
    }[ch]));
  }

  function buildGroupedThemeOptions(themes) {
    const groups = new Map();
    themes.forEach(theme => {
      const pillar = Object.prototype.hasOwnProperty.call(THEME_PILLAR_LABELS, theme.pillar)
        ? theme.pillar
        : "other";
      if (!groups.has(pillar)) groups.set(pillar, []);
      groups.get(pillar).push(theme);
    });

    const order = [...Object.keys(THEME_PILLAR_LABELS), "other"];
    return order
      .filter(pillar => groups.has(pillar) && groups.get(pillar).length)
      .map(pillar => {
        const label = THEME_PILLAR_LABELS[pillar] || "Otros temas";
        const options = groups.get(pillar).map(theme =>
          `<option value="${escapeThemeOption(theme.key)}">${escapeThemeOption(theme.title)}</option>`
        ).join("");
        return `<optgroup label="${escapeThemeOption(label)}">${options}</optgroup>`;
      }).join("");
  }

  // 1. Cargar los 26 temas agrupados visualmente en sus cinco pilares.
  async function loadThemes() {
    try {
      const res = await fetch("/api/themes");
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const themes = await res.json();
      const optionsHtml = buildGroupedThemeOptions(themes);
      if (themeSelect) themeSelect.innerHTML = optionsHtml;
      if (cardThemeSelect) cardThemeSelect.innerHTML = optionsHtml;
      updateProjectTitle();
      updateScriptDurationEstimate();
    } catch (e) {
      console.error("Error al cargar temas:", e);
      if (themeSelect) themeSelect.innerHTML = '<option value="">No se pudieron cargar los temas</option>';
    }
  }

  function updateScriptDurationEstimate() {
    if (!scriptDurationEstimate) return;
    const joined = [scriptHook?.value, scriptBody?.value, scriptCta?.value]
      .filter(Boolean).join(" ").trim();
    const words = joined ? joined.split(/\s+/).filter(Boolean).length : 0;
    const seconds = words ? Math.round(words * 60 / 125) : 0;
    const duration = words
      ? (seconds >= 60
          ? `${Math.floor(seconds / 60)} min ${String(seconds % 60).padStart(2, "0")} s`
          : `~${seconds} s`)
      : "sin estimación todavía";
    const target = scriptDurationMode?.value === "micro"
      ? "objetivo del modo: 12–16 s"
      : "objetivo del modo: 25–32 s";
    scriptDurationEstimate.textContent =
      `Estimación orientativa de locución: ${words} palabras · ${duration}. ${target}. Cálculo aproximado a 125 palabras/min; el narrador, las pausas y el render pueden cambiar la duración real.`;
  }

  [scriptHook, scriptBody, scriptCta].forEach(field => {
    if (field) field.addEventListener("input", updateScriptDurationEstimate);
  });
  if (scriptDurationMode) scriptDurationMode.addEventListener("change", updateScriptDurationEstimate);

  // 2. Cargar Voces en Inglés (Guy como voz predeterminada conversacional)
  async function loadVoices() {
    try {
      const res = await fetch("/api/voices");
      const voices = await res.json();
      const defaultVoice = voices.some(v => v.key === "guy") ? "guy" : (voices[0]?.key || "christopher");
      voiceSelect.innerHTML = voices
        .map(v => `<option value="${v.key}" ${v.key === defaultVoice ? "selected" : ""}>${v.name}</option>`)
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

  // 2c. Verificar estado de B-Roll (Pexels / Pixabay / Local)
  async function loadBrollStatus() {
    try {
      const res = await fetch("/api/broll-status");
      const status = await res.json();
      if (brollApiStatus) {
        if (status.available) {
          const provs = [];
          if (status.pexels_configured) provs.push("Pexels HD");
          if (status.pixabay_configured) provs.push("Pixabay");
          if (status.cached_clips > 0) provs.push(`${status.cached_clips} en caché`);
          if (status.local_library_clips > 0) provs.push(`${status.local_library_clips} locales`);
          brollApiStatus.textContent = `✅ B-Roll Activo (${provs.join(" + ") || "Biblioteca Local"})`;
          brollApiStatus.style.color = "#2ecc71";
        } else {
          brollApiStatus.textContent = "⚠️ Sin API Keys (Usa Biblioteca Local / Respaldo Cinemático)";
          brollApiStatus.style.color = "#f59e0b";
        }
      }
    } catch (e) {
      if (brollApiStatus) {
        brollApiStatus.textContent = "⚠️ Motor B-Roll en modo respaldo.";
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

      // Cargar galería en el Estudio de Tarjetas 4:5
      if (cardGalleryPicker) {
        cardGalleryPicker.innerHTML = images
          .map(img => {
            const isCardSel = img.filename === cardSelectedImageName;
            return `
              <div class="image-thumb ${isCardSel ? "selected" : ""}" data-card-filename="${img.filename}">
                <img src="${img.url}" alt="${img.label}">
                <div class="thumb-title">${img.label}</div>
              </div>
            `;
          })
          .join("");

        cardGalleryPicker.querySelectorAll("[data-card-filename]").forEach(thumb => {
          thumb.addEventListener("click", () => {
            cardSelectedImageName = thumb.dataset.cardFilename;
            if (cardResultImg) cardResultImg.src = `/assets/images/${cardSelectedImageName}`;
            loadImages();
          });
        });
      }
    } catch (e) {
      console.error("Error al cargar imágenes:", e);
    }
  }

  // 4. Generar Guion y Sincronizar Prompt de Imagen Automáticamente
  async function triggerGenerateScript() {
    btnGenerateScript.disabled = true;
    btnGenerateScript.textContent = "⏳ Generando guion...";
    try {
      const durationMode = scriptDurationMode ? scriptDurationMode.value : "deep";
      const res = await fetch("/api/generate-script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          theme_key: themeSelect.value,
          custom_topic: customTopic.value,
          mode: durationMode,
          seamless_loop: !!(chkSeamlessLoop && chkSeamlessLoop.checked)
        })
      });
      const data = await res.json();
      scriptHook.value = data.hook;
      scriptBody.value = data.body;
      scriptCta.value = data.cta;
      updateScriptDurationEstimate();

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
        const postCopyArea = document.getElementById("reelPostCopyText");
        if (postCopyArea) {
          postCopyArea.value = data.seo_caption;
        }
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
          hookBadgeStyleSelect.value = "viral_indigo";
        } else if (tKey.includes("majesty") || tKey.includes("glory") || tKey.includes("praise") || tKey.includes("harvest") || tKey.includes("favor")) {
          hookBadgeStyleSelect.value = "gold_luxury";
        } else {
          hookBadgeStyleSelect.value = "clean_glass";
        }
        updateHookBadgeAppearance();
      }
      updateCharCounters();
      updateProjectTitle();
    } catch (e) {
      alert("Error al generar guion: " + e.message);
    } finally {
      btnGenerateScript.disabled = false;
      btnGenerateScript.textContent = "✨ Generar guion";
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
    let previewText = `${scriptHook.value} ${scriptBody.value}`.trim();
    if (!previewText) {
      previewText = "The Lord is your shepherd and your shield today. Grace and peace be over your home.";
    }
    // Para que la preescucha sea instantánea y ágil (< 2 segundos), tomar hasta 25 palabras
    const words = previewText.split(/\s+/);
    if (words.length > 25) {
      previewText = words.slice(0, 25).join(" ") + "...";
    }

    btnPreviewAudio.disabled = true;
    btnPreviewAudio.textContent = "⏳ Sintetizando Voz...";
    try {
      const res = await fetch("/api/preview-audio", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          text: previewText,
          voice_key: voiceSelect.value,
          rate: rateSelect.value
        })
      });
      const data = await res.json();
      audioPreviewPlayer.src = `${data.audio_url}?t=${Date.now()}`;
      audioPreviewPlayer.style.display = "block";
      await audioPreviewPlayer.play().catch(() => {});
    } catch (e) {
      alert("Aviso al reproducir audio: " + e.message);
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

  const aiImageProviderSelect = document.getElementById("aiImageProviderSelect");
  const btnToggleAiSettings = document.getElementById("btnToggleAiSettings");
  const btnCloseAiKeys = document.getElementById("btnCloseAiKeys");
  const aiKeysConfigBox = document.getElementById("aiKeysConfigBox");
  const aiHordeKeyInput = document.getElementById("aiHordeKeyInput");
  const hfTokenInput = document.getElementById("hfTokenInput");
  const btnSaveAiKeys = document.getElementById("btnSaveAiKeys");
  const aiKeysStatusText = document.getElementById("aiKeysStatusText");
  const btnCopyPromptForExternal = document.getElementById("btnCopyPromptForExternal");

  function updateAiProviderUI() {
    if (!aiImageProviderSelect) return;
    const prov = aiImageProviderSelect.value;
    const puterBox = document.getElementById("puterStatusBox");
    if (puterBox) {
      puterBox.style.display = prov === "puter" ? "flex" : "none";
    }
  }

  if (aiImageProviderSelect) {
    aiImageProviderSelect.addEventListener("change", updateAiProviderUI);
  }

  if (btnToggleAiSettings && aiKeysConfigBox) {
    btnToggleAiSettings.addEventListener("click", () => {
      aiKeysConfigBox.style.display = aiKeysConfigBox.style.display === "none" ? "block" : "none";
    });
  }

  if (btnCloseAiKeys && aiKeysConfigBox) {
    btnCloseAiKeys.addEventListener("click", () => {
      aiKeysConfigBox.style.display = "none";
    });
  }

  if (btnSaveAiKeys) {
    btnSaveAiKeys.addEventListener("click", async () => {
      btnSaveAiKeys.disabled = true;
      btnSaveAiKeys.textContent = "⏳ Guardando...";
      const hordeKey = aiHordeKeyInput ? aiHordeKeyInput.value.trim() : "0000000000";
      const hfTok = hfTokenInput ? hfTokenInput.value.trim() : "";

      try {
        localStorage.setItem("aihorde_api_key", hordeKey);
        localStorage.setItem("hf_token", hfTok);

        await fetch("/api/save-image-keys", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            aihorde_api_key: hordeKey,
            hf_token: hfTok
          })
        });

        if (aiKeysStatusText) {
          aiKeysStatusText.textContent = "✅ ¡Configuración guardada y activada con éxito!";
          setTimeout(() => { if (aiKeysStatusText) aiKeysStatusText.textContent = ""; }, 4000);
        }
        alert("¡Configuración guardada! Z-Image Turbo y FLUX.1 Schnell están listos para generar en alta definición.");
      } catch (err) {
        alert("Aviso al guardar claves: " + err.message);
      } finally {
        btnSaveAiKeys.disabled = false;
        btnSaveAiKeys.textContent = "💾 Guardar Claves";
      }
    });
  }

  if (btnCopyPromptForExternal) {
    btnCopyPromptForExternal.addEventListener("click", () => {
      const activePrompt = (scene1PromptInput && scene1PromptInput.value.trim()) ||
        (aiImagePrompt && aiImagePrompt.value.trim()) ||
        "Cinematic photograph of Jesus Christ, warm sacred golden hour lighting, gentle depth of field, photorealistic 35mm photograph";
      navigator.clipboard.writeText(activePrompt).then(() => {
        alert("📋 ¡Prompt copiado al portapapeles!\n\nPuedes pegarlo en:\n• Bing Image Creator (bing.com/images/create)\n• Recraft (recraft.ai)\n\nLuego descarga la foto y súbela con 'Subir Mi Propia Imagen'.");
      }).catch(() => {
        prompt("Copia tu prompt cinematográfico aquí:", activePrompt);
      });
    });
  }

  // 8. Motor de Generación Cinemática de 3 Escenas con IA (Cloudflare / Hugging Face / Puter)
  async function generateSingleScene(promptText, sceneNum = 1, label = "Escena") {
    let cleanPrompt = (promptText || "").trim();
    if (!cleanPrompt) {
      cleanPrompt = "Jesus Christ with compassionate loving eyes, gentle smile, sacred warm golden hour light, cinematic photorealistic";
    }

    const providerSelect = document.getElementById("aiImageProviderSelect");
    const activeProvider = providerSelect ? providerSelect.value : "z_image";

    const hordeKey = (aiHordeKeyInput ? aiHordeKeyInput.value.trim() : "") || localStorage.getItem("aihorde_api_key") || "0000000000";
    const hfTok = (hfTokenInput ? hfTokenInput.value.trim() : "") || localStorage.getItem("hf_token") || "";

    let savedFilename = null;
    let savedUrl = null;
    let usedPuter = false;

    // Ejecución Estricta según el Motor Elegido por el Usuario
    if (activeProvider === "puter") {
      if (typeof puter === "undefined" || !puter.ai || !puter.ai.txt2img) {
        throw new Error("Puter AI no está disponible en este navegador. Revisa tu conexión o usa Z-Image Turbo.");
      }
      if (!puter.auth || !puter.auth.isSignedIn()) {
        await puter.auth.signIn({ attempt_temp_user_creation: true });
      }
      try {
        let enhancedPuterPrompt = cleanPrompt;
        if (!enhancedPuterPrompt.toLowerCase().includes("cinematic")) {
          enhancedPuterPrompt = `Ultra-realistic cinematic portrait of ${cleanPrompt}, warm divine golden hour lighting, sacred holy atmosphere, highly detailed, dramatic, majestic, sharp focus`;
        }
        const imgElement = await puter.ai.txt2img(enhancedPuterPrompt);
        let blob;
        if (imgElement instanceof HTMLImageElement || (imgElement && imgElement.src)) {
          const response = await fetch(imgElement.src);
          blob = await response.blob();
        } else if (imgElement instanceof Blob) {
          blob = imgElement;
        }

        if (!blob) {
          throw new Error("Puter no devolvió un formato de imagen compatible.");
        }

        const file = new File([blob], `scene_${sceneNum}_${Date.now()}.png`, { type: "image/png" });
        const formData = new FormData();
        formData.append("file", file);
        const uploadRes = await fetch("/api/upload-image", { method: "POST", body: formData });
        if (!uploadRes.ok) {
          throw new Error("Error al guardar en el servidor la imagen generada por Puter.");
        }
        const upData = await uploadRes.json();
        savedFilename = upData.filename;
        savedUrl = upData.url;
        usedPuter = true;
      } catch (puterErr) {
        console.error("Fallo estricto en Puter AI:", puterErr);
        throw new Error("Puter AI falló o agotó sus créditos gratuitos: " + (puterErr.message || puterErr) + ". Puedes conectar otra cuenta de Puter o elegir Z-Image Turbo / FLUX.1 Schnell.");
      }
    } else {
      // Motor de Servidor (Z-Image Turbo, FLUX.1 Schnell, AI Horde, Auto, Biblioteca)
      const res = await fetch("/api/generate-ai-image", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          prompt: cleanPrompt,
          aspect_ratio: aspectRatioSelect ? aspectRatioSelect.value : "9:16",
          provider: activeProvider,
          hf_token: hfTok,
          aihorde_api_key: hordeKey,
          scene_num: sceneNum,
          used_images: [selectedImageName, selectedImageName2, selectedImageName3].filter(Boolean)
        })
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
    if (!liveSubPreview) return;
    const style = subtitleStyleSelect ? subtitleStyleSelect.value : "karaoke";
    const isLarge = subtitleSizeSelect && subtitleSizeSelect.value === "large";
    const chkAllCaps = document.getElementById("chkSubtitlesAllCaps");
    const isAllCaps = chkAllCaps ? chkAllCaps.checked : (style === "pop");

    liveSubPreview.style.fontSize = isLarge ? "28px" : "22px";
    liveSubPreview.style.padding = "0";
    liveSubPreview.style.background = "transparent";

    const textPrimary = isAllCaps ? "GOD IS " : "God is ";
    const textActive = isAllCaps ? "WITH YOU" : "with you";

    if (style === "karaoke") {
      liveSubPreview.innerHTML = `<span style="font-family: 'Montserrat', sans-serif; font-weight: 800; text-shadow: 0 2px 8px rgba(0,0,0,0.9); color: #ffffff;">${textPrimary}<span class="highlight" style="color: #ffd700; text-shadow: 0 0 12px rgba(255,215,0,0.6);">${textActive}</span></span>`;
    } else if (style === "pop") {
      liveSubPreview.innerHTML = `<span style="font-family: 'Anton', Impact, sans-serif; letter-spacing: 1px; color: #ffffff; text-shadow: 0 3px 8px rgba(0,0,0,0.9);">${textPrimary}<span class="highlight" style="color: #ffff00; font-size: 1.12em; display: inline-block; transform: scale(1.12); text-shadow: 0 0 14px rgba(255,255,0,0.8);">${textActive}</span></span>`;
    } else if (style === "cinematic") {
      liveSubPreview.innerHTML = `<span style="font-family: 'Cinzel', Georgia, serif; font-weight: 700; letter-spacing: 1.5px; color: #f4f4f4; text-shadow: 0 2px 10px rgba(0,0,0,0.9);">${textPrimary}<span style="color: #ffc030; text-shadow: 0 0 10px rgba(255,192,48,0.5);">${textActive}</span></span>`;
    } else if (style === "clean") {
      liveSubPreview.innerHTML = `<span style="font-family: 'Montserrat', sans-serif; background: rgba(10, 14, 26, 0.88); color: #ffffff; padding: 6px 14px; border-radius: 6px; font-weight: 600; box-shadow: 0 4px 12px rgba(0,0,0,0.6);">${textPrimary}${textActive}</span>`;
    } else {
      liveSubPreview.innerHTML = `<span style="font-family: 'Montserrat', sans-serif; font-weight: 800; color: #ffffff;">${textPrimary}<span class="highlight" style="color: #ffd700;">${textActive}</span></span>`;
    }
  }

  if (subtitleStyleSelect) subtitleStyleSelect.addEventListener("change", updateSubtitlePreview);
  if (subtitleSizeSelect) subtitleSizeSelect.addEventListener("change", updateSubtitlePreview);
  const chkSubtitlesAllCaps = document.getElementById("chkSubtitlesAllCaps");
  if (chkSubtitlesAllCaps) chkSubtitlesAllCaps.addEventListener("change", updateSubtitlePreview);
  updateSubtitlePreview();
  updateSubtitlePosition();
  updateSubtitleAnimation();

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

    if (effect === "living_gold") {
      // Atmósfera Dorada Viva (Pulsación de luz cálida temporal + Motes dorados ascendentes)
      const time = Date.now() * 0.0016;
      const pulse = 0.16 + 0.08 * Math.sin(time * 1.5);
      const gradient = fxCtx.createRadialGradient(w / 2, h * 0.45, 20, w / 2, h * 0.45, w * 0.85);
      gradient.addColorStop(0, `rgba(255, 220, 100, ${pulse * 1.3})`);
      gradient.addColorStop(0.5, `rgba(255, 180, 50, ${pulse * 0.6})`);
      gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
      fxCtx.fillStyle = gradient;
      fxCtx.fillRect(0, 0, w, h);

      particles.forEach(p => {
        p.y -= p.speedY * 1.1;
        p.x += p.speedX * 0.9;
        p.pulseVal += p.pulseSpeed * 1.2;
        const currentAlpha = p.alpha * (0.6 + 0.4 * Math.sin(p.pulseVal));
        if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
        fxCtx.fillStyle = `rgba(255, 225, 110, ${currentAlpha})`;
        fxCtx.shadowColor = "#ffd700";
        fxCtx.shadowBlur = 12;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "divine_rays") {
      // Rayos Celestiales Vivos (Pulsación de Luz Divina Cenital)
      const time = Date.now() * 0.0018;
      const intensity = 0.28 + 0.12 * Math.sin(time);
      const gradient = fxCtx.createRadialGradient(w / 2, 0, 20, w / 2, 0, h * 0.9);
      gradient.addColorStop(0, `rgba(255, 245, 200, ${intensity})`);
      gradient.addColorStop(0.4, `rgba(255, 215, 120, ${intensity * 0.6})`);
      gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
      fxCtx.fillStyle = gradient;
      fxCtx.fillRect(0, 0, w, h);

      particles.forEach(p => {
        p.y -= p.speedY * 0.7;
        p.pulseVal += p.pulseSpeed;
        const currentAlpha = p.alpha * 0.7;
        if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius * 0.9, 0, Math.PI * 2);
        fxCtx.fillStyle = `rgba(255, 250, 220, ${currentAlpha})`;
        fxCtx.shadowColor = "#fff8db";
        fxCtx.shadowBlur = 10;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "sacred_candle") {
      // Vela Sagrada en Penumbra (Calidez Fluctuante Ámbar y Fuego Santo)
      const time = Date.now() * 0.003;
      const flicker = 0.15 + 0.06 * Math.sin(time) + 0.03 * Math.sin(time * 2.7);
      const gradient = fxCtx.createRadialGradient(w / 2, h * 0.7, 10, w / 2, h * 0.7, w * 0.75);
      gradient.addColorStop(0, `rgba(255, 170, 40, ${flicker * 1.4})`);
      gradient.addColorStop(0.6, `rgba(200, 90, 10, ${flicker * 0.5})`);
      gradient.addColorStop(1, "rgba(0, 0, 0, 0)");
      fxCtx.fillStyle = gradient;
      fxCtx.fillRect(0, 0, w, h);

      particles.forEach(p => {
        p.y -= p.speedY * 1.3;
        p.x += (Math.random() - 0.5) * 0.8;
        p.pulseVal += p.pulseSpeed * 1.5;
        const currentAlpha = p.alpha * (0.5 + 0.5 * Math.sin(p.pulseVal));
        if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius * 0.85, 0, Math.PI * 2);
        fxCtx.fillStyle = `rgba(255, 160, 30, ${currentAlpha})`;
        fxCtx.shadowColor = "#ff8c00";
        fxCtx.shadowBlur = 8;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "angelic_shimmer") {
      // Destello Angélico Resplandeciente (Cristales Eclécticos Puros)
      particles.forEach(p => {
        p.y -= p.speedY * 0.7;
        p.x += p.speedX * 0.6;
        p.pulseVal += p.pulseSpeed * 1.4;
        const currentAlpha = p.alpha * (0.6 + 0.4 * Math.cos(p.pulseVal));
        if (p.y < -10) { p.y = h + 10; p.x = Math.random() * w; }
        fxCtx.beginPath();
        fxCtx.arc(p.x, p.y, p.radius * 1.15, 0, Math.PI * 2);
        fxCtx.fillStyle = `rgba(255, 255, 255, ${currentAlpha * 0.95})`;
        fxCtx.shadowColor = "#e6f2ff";
        fxCtx.shadowBlur = 14;
        fxCtx.fill();
      });
      fxCtx.shadowBlur = 0;
    } else if (effect === "cinematic_dust") {
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
    const pos = subtitlePositionSelect ? subtitlePositionSelect.value : "bottom";
    if (stageOverlay) {
      stageOverlay.classList.remove("pos-bottom", "pos-center", "pos-top");
      stageOverlay.classList.add(`pos-${pos}`);
    }
    if (liveSubPreview) {
      liveSubPreview.classList.remove("pos-bottom", "pos-center", "pos-top");
      liveSubPreview.classList.add(`pos-${pos}`);
    }
  }

  function updateSubtitleAnimation() {
    const anim = subtitleAnimationSelect ? subtitleAnimationSelect.value : "pop";
    if (stagePlaceholder) {
      stagePlaceholder.classList.remove("anim-pop", "anim-glow", "anim-fade", "anim-scale_slow", "anim-none");
      stagePlaceholder.classList.add(`anim-${anim}`);
    }
    if (liveSubPreview) {
      liveSubPreview.classList.remove("anim-pop", "anim-glow", "anim-fade", "anim-scale_slow", "anim-none");
      liveSubPreview.classList.add(`anim-${anim}`);
    }
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
    const phoneScreen = document.querySelector(".phone-screen");
    const badgeRatio = document.querySelector(".badge-ratio");
    const stageBlurBg = document.getElementById("stageBlurBg");
    const stageImg = document.getElementById("stageSelectedImage");
    if (!aspectSelect) return;

    const val = aspectSelect.value;
    if (badgeRatio) badgeRatio.textContent = val;

    if (stageBlurBg && selectedImageName) {
      const activeBg = (selectedImageName.startsWith("data:") || selectedImageName.startsWith("blob:") || selectedImageName.startsWith("http"))
        ? selectedImageName
        : `/assets/images/${selectedImageName}`;
      stageBlurBg.style.backgroundImage = `url('${activeBg}')`;
    }

    if (val === "9:16") {
      if (phoneMockup) phoneMockup.style.maxWidth = "320px";
      if (phoneScreen) phoneScreen.style.aspectRatio = "9 / 16";
      if (stageImg) stageImg.style.objectFit = "cover";
    } else if (val === "1:1") {
      if (phoneMockup) phoneMockup.style.maxWidth = "360px";
      if (phoneScreen) phoneScreen.style.aspectRatio = "1 / 1";
      if (stageImg) stageImg.style.objectFit = "contain";
    } else if (val === "16:9") {
      if (phoneMockup) phoneMockup.style.maxWidth = "440px";
      if (phoneScreen) phoneScreen.style.aspectRatio = "16 / 9";
      if (stageImg) stageImg.style.objectFit = "contain";
    }

    setTimeout(initParticles, 150);
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
          video_mode: videoModeSelect ? videoModeSelect.value : "images",
          image_name: selectedImageName,
          image_name_2: selectedImageName2 || "none",
          image_name_3: selectedImageName3 || "none",
          subtitle_style: subtitleStyleSelect.value,
          subtitle_size: subtitleSizeSelect.value,
          subtitle_animation: animSelect ? animSelect.value : "pop",
          subtitle_position: subPosSelect ? subPosSelect.value : "bottom",
          all_caps: !!(document.getElementById("chkSubtitlesAllCaps") && document.getElementById("chkSubtitlesAllCaps").checked),
          camera_motion: camSelect ? camSelect.value : "zoom_in",
          transition_style: transitionStyleSelect ? transitionStyleSelect.value : "fade",
          music_track: musicSelect ? musicSelect.value : "worship_piano_peace",
          music_volume: volumeInput ? parseFloat(volumeInput.value) / 100.0 : 0.20,
          aspect_ratio: aspectSelect ? aspectSelect.value : "9:16",
          effect_type: effectSelect ? effectSelect.value : "none",
          theme_key: themeSelect ? themeSelect.value : "morning_favor",
          enable_hook_badge: !!(chkEnableHookBadge && chkEnableHookBadge.checked),
          hook_text: (chkEnableHookBadge && chkEnableHookBadge.checked && hookBadgeInput) ? hookBadgeInput.value.trim() : "",
          hook_badge_style: hookBadgeStyleSelect ? hookBadgeStyleSelect.value : "gold_luxury",
          hook_badge_font: hookBadgeFontSelect ? hookBadgeFontSelect.value : "Montserrat",
          hook_badge_size: hookBadgeSizeSelect ? hookBadgeSizeSelect.value : "normal",
          enable_micro_cta: !!(chkEnableMicroCta && chkEnableMicroCta.checked),
          micro_cta_text: (chkEnableMicroCta && chkEnableMicroCta.checked && microCtaInput) ? microCtaInput.value.trim() : "",
          enable_sfx: chkEnableSfx ? chkEnableSfx.checked : false,
          seamless_loop: !!(chkSeamlessLoop && chkSeamlessLoop.checked),
          master_lufs: chkMasterLufs ? chkMasterLufs.checked : true,
          generate_trending_audio: chkGenerateTrendingAudio ? chkGenerateTrendingAudio.checked : false
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

      if (btnDownloadTrendingAudioVideo) {
        if (data.trending_audio_video_url && data.trending_audio_video_url !== data.video_url) {
          btnDownloadTrendingAudioVideo.href = data.trending_audio_video_url;
          btnDownloadTrendingAudioVideo.download = data.trending_filename || "jesus_reel_trending.mp4";
          btnDownloadTrendingAudioVideo.style.display = "block";
        } else {
          btnDownloadTrendingAudioVideo.style.display = "none";
        }
      }
      videoActions.style.display = "block";
      showVideoView();

      if (data.actual_duration_sec) {
        renderStatusText.textContent = `✅ Reel Generado con Éxito (${data.actual_duration_sec}s)`;
        renderStatusSub.textContent = `Duración objetivo: ${data.target_duration_sec || 0}s | Precisión: ${data.duration_diff_sec || 0}s`;
      }

      loadRecentOutputs();
    } catch (e) {
      alert("Fallo al renderizar: " + e.message);
    } finally {
      renderOverlay.style.display = "none";
      btnRenderVideo.disabled = false;
    }
  }

  // 11. Copiar Texto y Hashtags para Facebook
  if (btnCopyCaption) {
    btnCopyCaption.addEventListener("click", () => {
      const postCopyArea = document.getElementById("reelPostCopyText");
      let caption = "";
      if (postCopyArea && postCopyArea.value.trim()) {
        caption = postCopyArea.value.trim();
      } else if (currentSeoCaption) {
        caption = currentSeoCaption;
      } else {
        const hook = scriptHook ? scriptHook.value.trim() : "";
        const body = scriptBody ? scriptBody.value.trim() : "";
        const cta = scriptCta ? scriptCta.value.trim() : "";
        const pinned = currentPinnedComment || (scriptPinnedComment ? scriptPinnedComment.value.trim() : "");
        const scriptureText = currentScripture ? `📖 Scripture:\n"${currentScripture}"\n\n` : "";
        caption = `${hook}\n\n${body}\n\n${scriptureText}${cta}${pinned ? `\n\nReflection: ${pinned}` : ""}\n\n#DailyPrayer #Faith #ChristianReels #JesusChrist #GodIsGood`;
      }

      navigator.clipboard.writeText(caption).then(() => {
        btnCopyCaption.textContent = "✅ ¡Publicación Copiada al Portapapeles!";
        setTimeout(() => {
          btnCopyCaption.textContent = "📋 Copiar Publicación Completa para Facebook";
        }, 2500);
      }).catch(err => {
        alert("No se pudo copiar automáticamente: " + err);
      });
    });
  }

  // ─── MODO DE PRODUCCIÓN (REELS 9:16 VS TARJETAS FEED 4:5) ─────────────
  function switchProductionMode(mode) {
    if (mode === "cards") {
      if (tabModeReels) tabModeReels.classList.remove("active");
      if (tabModeFeedCards) tabModeFeedCards.classList.add("active");
      if (workspaceReels) workspaceReels.style.display = "none";
      if (workspaceCards) workspaceCards.style.display = "";
      if (!cardStudioInitialized) {
        syncCardTemplate(cardThemeSelect ? cardThemeSelect.value : "morning_favor");
        cardStudioInitialized = true;
      }
    } else {
      if (tabModeFeedCards) tabModeFeedCards.classList.remove("active");
      if (tabModeReels) tabModeReels.classList.add("active");
      if (workspaceCards) workspaceCards.style.display = "none";
      if (workspaceReels) workspaceReels.style.display = "";
    }
  }

  if (tabModeReels) {
    tabModeReels.addEventListener("click", () => switchProductionMode("reels"));
  }
  if (tabModeFeedCards) {
    tabModeFeedCards.addEventListener("click", () => switchProductionMode("cards"));
  }
  if (btnOpenDailyBatchTop) {
    btnOpenDailyBatchTop.addEventListener("click", openDailyBatchModal);
  }

  // ─── ESTUDIO DE TARJETAS DE ORACIÓN 4:5 (FEED HD) ──────────────────────
  async function syncCardTemplate(themeKey, useExistingImage = false) {
    const key = themeKey || (cardThemeSelect ? cardThemeSelect.value : "morning_favor");
    if (btnSyncCardTheme) {
      btnSyncCardTheme.disabled = true;
      btnSyncCardTheme.textContent = "⏳ Sincronizando...";
    }
    try {
      const res = await fetch(`/api/card-template/${encodeURIComponent(key)}`);
      const data = await res.json();
      if (cardTitleInput) cardTitleInput.value = data.title_english || "PRAYER OF FAITH";
      if (cardPrayerInput) cardPrayerInput.value = data.prayer_english || "";
      if (cardVerseInput) cardVerseInput.value = data.scripture || "";
      if (cardFeedCopyText) cardFeedCopyText.value = data.feed_copy || "";
      if (cardAiPrompt) cardAiPrompt.value = data.image_prompt || "";
      cardCurrentPinnedComment = data.pinned_comment || "";

      const shouldAutoAiImage = chkAutoCardImage && chkAutoCardImage.checked && !useExistingImage;
      if (shouldAutoAiImage) {
        await generateCardAiImage();
      } else {
        if (!useExistingImage && data.recommended_image) {
          cardSelectedImageName = data.recommended_image;
          if (cardResultImg) cardResultImg.src = `/assets/images/${cardSelectedImageName}`;
          loadImages();
        }
        await renderCardImage();
      }
    } catch (err) {
      console.error("Error al sincronizar plantilla de tarjeta:", err);
    } finally {
      if (btnSyncCardTheme) {
        btnSyncCardTheme.disabled = false;
        btnSyncCardTheme.textContent = "🪄 Sincronizar";
      }
    }
  }

  // Generador de Imagen Sagrada con IA Personalizada para la Tarjeta (4:5)
  async function generateCardAiImage() {
    const defaultPrompt = cardTitleInput ? `${cardTitleInput.value}, sacred golden light, serene divine presence, high contrast cinematic render --ar 4:5` : "A devout Christian praying with folded hands, warm glowing candlelight, sacred divine light, ultra realistic 4:5 --ar 4:5";
    const promptText = (cardAiPrompt ? cardAiPrompt.value.trim() : "") || defaultPrompt;
    const provider = cardAiProviderSelect ? cardAiProviderSelect.value : "auto";

    if (btnGenerateCardAiImage) {
      btnGenerateCardAiImage.disabled = true;
      btnGenerateCardAiImage.textContent = "⏳ Generando Imagen IA 4:5...";
    }
    if (cardAiImageStatusBadge) {
      cardAiImageStatusBadge.style.display = "inline-block";
      cardAiImageStatusBadge.className = "badge tag-blue";
      cardAiImageStatusBadge.textContent = "🎨 Creando Imagen IA...";
    }
    if (cardRenderOverlay) {
      if (cardOverlayTitle) cardOverlayTitle.textContent = "Creando Imagen Sagrada con IA (4:5)...";
      if (cardOverlayDesc) cardOverlayDesc.textContent = "Generando composición bíblica única para esta oración...";
      cardRenderOverlay.style.display = "flex";
    }

    try {
      let finalUrl = "";
      let finalFilename = "";
      let engineName = provider;

      if (provider === "puter") {
        if (typeof puter === "undefined" || !puter.ai) {
          throw new Error("Puter.js no está inicializado o disponible en este navegador.");
        }
        const imgEl = await puter.ai.txt2img(promptText);
        let blob;
        if (imgEl && imgEl.src) {
          const resp = await fetch(imgEl.src);
          blob = await resp.blob();
        } else {
          throw new Error("Puter.js no devolvió una imagen válida.");
        }
        const fd = new FormData();
        fd.append("file", blob, `card_puter_${Date.now()}.png`);
        const upRes = await fetch("/api/upload-image", { method: "POST", body: fd });
        const upData = await upRes.json();
        finalUrl = upData.url;
        finalFilename = upData.filename;
        engineName = "Puter.js AI";
      } else {
        const hordeKey = (aiHordeKeyInput ? aiHordeKeyInput.value.trim() : "") || localStorage.getItem("aihorde_api_key") || "0000000000";
        const hfTok = (hfTokenInput ? hfTokenInput.value.trim() : "") || localStorage.getItem("hf_token") || "";

        const res = await fetch("/api/generate-ai-image", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            prompt: promptText,
            aspect_ratio: "4:5",
            provider: provider,
            hf_token: hfTok || null,
            aihorde_api_key: hordeKey || null
          })
        });
        const data = await res.json();
        if (!data.success || !data.filename) {
          throw new Error(data.error || "Fallo al generar imagen con IA en el servidor.");
        }
        finalUrl = data.url;
        finalFilename = data.filename;
        engineName = data.engine_used || provider;
      }

      cardSelectedImageName = finalFilename;
      if (cardResultImg) cardResultImg.src = finalUrl + "?t=" + Date.now();

      if (cardAiImageStatusBadge) {
        cardAiImageStatusBadge.className = "badge tag-green";
        cardAiImageStatusBadge.textContent = `✅ Imagen Lista (${engineName})`;
      }

      // Recomponer la tarjeta final con la nueva imagen y textos
      await renderCardImage();
      await loadImages();
    } catch (err) {
      alert("Error al generar imagen con IA para la tarjeta: " + err.message);
      if (cardAiImageStatusBadge) {
        cardAiImageStatusBadge.className = "badge tag-gold";
        cardAiImageStatusBadge.textContent = "⚠️ Error en imagen IA";
      }
    } finally {
      if (btnGenerateCardAiImage) {
        btnGenerateCardAiImage.disabled = false;
        btnGenerateCardAiImage.textContent = "🎨 Generar Imagen IA (4:5)";
      }
      if (cardRenderOverlay) {
        cardRenderOverlay.style.display = "none";
        if (cardOverlayTitle) cardOverlayTitle.textContent = "Componiendo Tarjeta 4:5...";
        if (cardOverlayDesc) cardOverlayDesc.textContent = "Aplicando marco dorado, tipografía noble y marca de agua...";
      }
    }
  }

  async function renderCardImage() {
    const prayer = cardPrayerInput ? cardPrayerInput.value.trim() : "";
    if (!prayer) {
      alert("Por favor escribe o sincroniza una oración devocional para la tarjeta.");
      return;
    }

    if (cardRenderOverlay) {
      if (cardOverlayTitle) cardOverlayTitle.textContent = "Componiendo Tarjeta 4:5...";
      if (cardOverlayDesc) cardOverlayDesc.textContent = "Aplicando marco dorado, tipografía noble y marca de agua...";
      cardRenderOverlay.style.display = "flex";
    }
    if (btnRenderCard) {
      btnRenderCard.disabled = true;
      btnRenderCard.textContent = "⏳ COMPONIENDO TARJETA 4:5...";
    }

    const isWatermark = chkCardWatermark ? chkCardWatermark.checked : true;
    const watermarkVal = isWatermark ? (cardWatermarkInput ? cardWatermarkInput.value.trim() : "@JesusDailyFaith") : "";

    const payload = {
      background_image_path: cardSelectedImageName || "jesus_healing_miracle.jpg",
      title: cardTitleInput ? (cardTitleInput.value.trim() || "PRAYER OF FAITH") : "PRAYER OF FAITH",
      prayer_text: prayer,
      verse_footer: cardVerseInput ? (cardVerseInput.value.trim() || "Jeremiah 29:11") : "",
      watermark_text: watermarkVal
    };

    try {
      const res = await fetch("/api/render-image-card", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      const data = await res.json();
      if (data.success && data.card_url) {
        if (cardResultImg) cardResultImg.src = data.card_url + "?t=" + Date.now();
        if (btnDownloadCard) {
          btnDownloadCard.href = data.card_url;
          btnDownloadCard.download = `prayer_card_4_5_${Date.now()}.jpg`;
        }
      } else {
        alert("Error al renderizar tarjeta 4:5: " + (data.error || "Error desconocido"));
      }
    } catch (err) {
      alert("Error de conexión al renderizar la tarjeta: " + err.message);
    } finally {
      if (cardRenderOverlay) cardRenderOverlay.style.display = "none";
      if (btnRenderCard) {
        btnRenderCard.disabled = false;
        btnRenderCard.textContent = "✨ RENDERIZAR TARJETA DE ORACIÓN 4:5 (FEED HD)";
      }
    }
  }

  if (cardThemeSelect) {
    cardThemeSelect.addEventListener("change", () => syncCardTemplate(cardThemeSelect.value));
  }
  if (btnSyncCardTheme) {
    btnSyncCardTheme.addEventListener("click", () => syncCardTemplate(cardThemeSelect.value));
  }
  if (btnRerollCardPrayer) {
    btnRerollCardPrayer.addEventListener("click", () => syncCardTemplate(cardThemeSelect.value, true));
  }
  if (btnGenerateCardAiImage) {
    btnGenerateCardAiImage.addEventListener("click", generateCardAiImage);
  }
  if (btnRenderCard) {
    btnRenderCard.addEventListener("click", renderCardImage);
  }

  if (cardImageUpload) {
    cardImageUpload.addEventListener("change", async (e) => {
      const file = e.target.files[0];
      if (!file) return;
      const formData = new FormData();
      formData.append("file", file);
      try {
        const res = await fetch("/api/upload-image", { method: "POST", body: formData });
        const data = await res.json();
        cardSelectedImageName = data.filename;
        if (cardResultImg) cardResultImg.src = data.url;
        await loadImages();
      } catch (err) {
        alert("Fallo al subir imagen para tarjeta: " + err.message);
      }
    });
  }

  if (btnCopyCardFeedPost) {
    btnCopyCardFeedPost.addEventListener("click", () => {
      const text = cardFeedCopyText ? cardFeedCopyText.value.trim() : "";
      if (!text) {
        alert("No hay copy de publicación disponible para copiar.");
        return;
      }
      navigator.clipboard.writeText(text).then(() => {
        const orig = btnCopyCardFeedPost.innerHTML;
        btnCopyCardFeedPost.innerHTML = "✅ ¡Copy para Facebook Copiado!";
        setTimeout(() => { btnCopyCardFeedPost.innerHTML = orig; }, 2500);
      }).catch(err => alert("Error al copiar: " + err));
    });
  }

  if (btnCopyCardPinnedComment) {
    btnCopyCardPinnedComment.addEventListener("click", () => {
      const text = cardCurrentPinnedComment || "Type AMEN and write the name of who you are praying for today! 🙏";
      navigator.clipboard.writeText(text).then(() => {
        const orig = btnCopyCardPinnedComment.innerHTML;
        btnCopyCardPinnedComment.innerHTML = "✅ ¡Comentario Fijado Copiado!";
        setTimeout(() => { btnCopyCardPinnedComment.innerHTML = orig; }, 2500);
      }).catch(err => alert("Error al copiar: " + err));
    });
  }

  // Sincronizar desde Reel hacia Tarjeta 4:5
  if (btnGenerateCardFromReel) {
    btnGenerateCardFromReel.addEventListener("click", async () => {
      switchProductionMode("cards");
      const currentTheme = themeSelect ? themeSelect.value : "morning_favor";
      if (cardThemeSelect) cardThemeSelect.value = currentTheme;
      if (selectedImageName) {
        cardSelectedImageName = selectedImageName;
      }
      await syncCardTemplate(currentTheme, true);
      if (scriptBody && scriptBody.value.trim()) {
        cardPrayerInput.value = scriptBody.value.trim();
      }
      renderCardImage();
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
            const watermarkVal = (chkCardWatermark && chkCardWatermark.checked) ? (cardWatermarkInput ? cardWatermarkInput.value.trim() : "@JesusDailyFaith") : "";
            const res = await fetch("/api/render-image-card", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                background_image_path: slot.recommended_image || "jesus_holy_bible.jpg",
                title: rawTitle,
                prayer_text: slot.script.body,
                verse_footer: slot.script.scripture || "Jeremiah 29:11",
                watermark_text: watermarkVal
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

  // Inicialización de Eventos Principales
  btnGenerateScript.addEventListener("click", triggerGenerateScript);
  btnSyncScriptToImage.addEventListener("click", triggerSyncPrompt);
  btnPreviewAudio.addEventListener("click", triggerAudioPreview);
  btnRenderVideo.addEventListener("click", triggerRenderVideo);
  themeSelect.addEventListener("change", () => {
    updateProjectTitle();
    triggerGenerateScript();
  });
  if (videoModeSelect) {
    videoModeSelect.addEventListener("change", toggleVideoMode);
  }

  // ─── 1. SISTEMA DE NAVEGACIÓN POR ETAPAS (1 A 6) ───────────────────
  // Regla de Oro: Cambiar de etapa NUNCA borra los datos de los inputs
  const navStageButtons = [
    document.getElementById("navStage1"),
    document.getElementById("navStage2"),
    document.getElementById("navStage3"),
    document.getElementById("navStage4"),
    document.getElementById("navStage5"),
    document.getElementById("navStage6")
  ];

  const stagePanels = [
    document.getElementById("stagePanel1"),
    document.getElementById("stagePanel2"),
    document.getElementById("stagePanel3"),
    document.getElementById("stagePanel4"),
    document.getElementById("stagePanel5"),
    document.getElementById("stagePanel6")
  ];

  let currentActiveStage = 1;

  function switchStage(stageNum) {
    if (stageNum < 1 || stageNum > 6) return;
    currentActiveStage = stageNum;

    // Actualizar sidebar visualmente
    navStageButtons.forEach((btn, idx) => {
      if (btn) {
        if (idx + 1 === stageNum) {
          btn.classList.add("active");
        } else {
          btn.classList.remove("active");
        }
      }
    });

    // Mostrar panel activo y ocultar los demás (sin perder ningún input)
    stagePanels.forEach((panel, idx) => {
      if (panel) {
        if (idx + 1 === stageNum) {
          panel.style.display = "flex";
          panel.classList.add("active");
        } else {
          panel.style.display = "none";
          panel.classList.remove("active");
        }
      }
    });

    // Desplazar el panel central hacia arriba
    const centerPanel = document.getElementById("centerStagePanel");
    if (centerPanel) {
      centerPanel.scrollTop = 0;
    }
  }

  // Asignar clics a los botones de navegación del sidebar
  navStageButtons.forEach((btn, idx) => {
    if (btn) {
      btn.addEventListener("click", () => switchStage(idx + 1));
    }
  });

  // Botones de Siguiente y Anterior entre etapas
  const btnNavToStage2 = document.getElementById("btnNavToStage2");
  if (btnNavToStage2) btnNavToStage2.addEventListener("click", () => switchStage(2));

  const btnNavBackTo1 = document.getElementById("btnNavBackTo1");
  if (btnNavBackTo1) btnNavBackTo1.addEventListener("click", () => switchStage(1));

  const btnNavToStage3 = document.getElementById("btnNavToStage3");
  if (btnNavToStage3) btnNavToStage3.addEventListener("click", () => switchStage(3));

  const btnNavBackTo2 = document.getElementById("btnNavBackTo2");
  if (btnNavBackTo2) btnNavBackTo2.addEventListener("click", () => switchStage(2));

  const btnNavToStage4 = document.getElementById("btnNavToStage4");
  if (btnNavToStage4) btnNavToStage4.addEventListener("click", () => switchStage(4));

  const btnNavBackTo3 = document.getElementById("btnNavBackTo3");
  if (btnNavBackTo3) btnNavBackTo3.addEventListener("click", () => switchStage(3));

  const btnNavToStage5 = document.getElementById("btnNavToStage5");
  if (btnNavToStage5) btnNavToStage5.addEventListener("click", () => switchStage(5));

  const btnNavBackTo4 = document.getElementById("btnNavBackTo4");
  if (btnNavBackTo4) btnNavBackTo4.addEventListener("click", () => switchStage(4));

  const btnNavToStage6 = document.getElementById("btnNavToStage6");
  if (btnNavToStage6) btnNavToStage6.addEventListener("click", () => switchStage(6));

  const btnNavBackTo5 = document.getElementById("btnNavBackTo5");
  if (btnNavBackTo5) btnNavBackTo5.addEventListener("click", () => switchStage(5));

  // Botones de acceso rápido del sidebar
  const btnSidebarMyReels = document.getElementById("btnSidebarMyReels");
  if (btnSidebarMyReels) {
    btnSidebarMyReels.addEventListener("click", () => {
      switchProductionMode("reels");
      switchStage(6);
    });
  }

  const btnSidebarPrayerCards = document.getElementById("btnSidebarPrayerCards");
  if (btnSidebarPrayerCards) {
    btnSidebarPrayerCards.addEventListener("click", () => {
      switchProductionMode("cards");
    });
  }

  const btnSidebarDailyBatch = document.getElementById("btnSidebarDailyBatch");
  if (btnSidebarDailyBatch) {
    btnSidebarDailyBatch.addEventListener("click", openDailyBatchModal);
  }

  const btnNewProjectSidebar = document.getElementById("btnNewProjectSidebar");
  if (btnNewProjectSidebar) {
    btnNewProjectSidebar.addEventListener("click", () => {
      switchStage(1);
      triggerGenerateScript();
    });
  }

  const btnTopNewProject = document.getElementById("btnTopNewProject");
  if (btnTopNewProject) {
    btnTopNewProject.addEventListener("click", () => {
      switchStage(1);
      triggerGenerateScript();
    });
  }

  // ─── 2. CONTADORES DE CARACTERES EN VIVO (4 CAJAS DE GUION) ────────
  const hookCharCount = document.getElementById("hookCharCount");
  const bodyCharCount = document.getElementById("bodyCharCount");
  const ctaCharCount = document.getElementById("ctaCharCount");
  const badgeCharCount = document.getElementById("badgeCharCount");

  function updateCharCounters() {
    if (hookCharCount && scriptHook) {
      hookCharCount.textContent = `${scriptHook.value.length}/500`;
    }
    if (bodyCharCount && scriptBody) {
      bodyCharCount.textContent = `${scriptBody.value.length}/500`;
    }
    if (ctaCharCount && scriptCta) {
      ctaCharCount.textContent = `${scriptCta.value.length}/500`;
    }
    if (badgeCharCount && hookBadgeInput) {
      badgeCharCount.textContent = `${hookBadgeInput.value.length}/500`;
    }
  }

  if (scriptHook) scriptHook.addEventListener("input", updateCharCounters);
  if (scriptBody) scriptBody.addEventListener("input", updateCharCounters);
  if (scriptCta) scriptCta.addEventListener("input", updateCharCounters);
  if (hookBadgeInput) hookBadgeInput.addEventListener("input", updateCharCounters);

  // Botón para limpiar campos del guion
  const btnClearScriptFields = document.getElementById("btnClearScriptFields");
  if (btnClearScriptFields) {
    btnClearScriptFields.addEventListener("click", () => {
      if (confirm("¿Deseas vaciar los campos de guion y gancho?")) {
        if (scriptHook) scriptHook.value = "";
        if (scriptBody) scriptBody.value = "";
        if (scriptCta) scriptCta.value = "";
        if (hookBadgeInput) hookBadgeInput.value = "";
        if (customTopic) customTopic.value = "";
        updateCharCounters();
      }
    });
  }

  // ─── 3. SELECTOR DE TEMA DE 3 ESTADOS (CLARO / AUTO / OSCURO) ───────
  const btnThemeLight = document.getElementById("btnThemeLight");
  const btnThemeAuto = document.getElementById("btnThemeAuto");
  const btnThemeDark = document.getElementById("btnThemeDark");
  const btnToggleTheme = document.getElementById("btnToggleTheme");

  function getSystemTheme() {
    return (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) ? "dark" : "light";
  }

  function applyAppThemeMode(mode) {
    let effectiveTheme = mode;
    if (mode === "auto") {
      effectiveTheme = getSystemTheme();
    }
    document.documentElement.setAttribute("data-theme", effectiveTheme);
    localStorage.setItem("jesusreels_theme_mode", mode);

    if (btnThemeLight) btnThemeLight.classList.toggle("active", mode === "light");
    if (btnThemeAuto) btnThemeAuto.classList.toggle("active", mode === "auto");
    if (btnThemeDark) btnThemeDark.classList.toggle("active", mode === "dark");

    if (btnToggleTheme) {
      btnToggleTheme.innerHTML = effectiveTheme === "dark" 
        ? '☀️ <span class="theme-text">Modo Claro</span>' 
        : '🌙 <span class="theme-text">Modo Oscuro</span>';
    }
  }

  const savedThemeMode = localStorage.getItem("jesusreels_theme_mode") || "dark";
  applyAppThemeMode(savedThemeMode);

  if (btnThemeLight) btnThemeLight.addEventListener("click", () => applyAppThemeMode("light"));
  if (btnThemeAuto) btnThemeAuto.addEventListener("click", () => applyAppThemeMode("auto"));
  if (btnThemeDark) btnThemeDark.addEventListener("click", () => applyAppThemeMode("dark"));

  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", () => {
      const currentMode = localStorage.getItem("jesusreels_theme_mode") || "dark";
      if (currentMode === "auto") {
        applyAppThemeMode("auto");
      }
    });
  }

  if (btnToggleTheme) {
    btnToggleTheme.addEventListener("click", () => {
      const active = document.documentElement.getAttribute("data-theme") || "dark";
      applyAppThemeMode(active === "dark" ? "light" : "dark");
    });
  }

  // ─── 4. ESTANTE DE ESCENAS Y VISTA PREVIA DERECHA ──────────────────
  const previewThumbScene1 = document.getElementById("previewThumbScene1");
  const previewThumbScene2 = document.getElementById("previewThumbScene2");
  const previewThumbScene3 = document.getElementById("previewThumbScene3");
  const btnRightRender = document.getElementById("btnRightRender");

  if (previewThumbScene1) {
    previewThumbScene1.addEventListener("click", () => {
      if (btnTabScene1) btnTabScene1.click();
    });
  }
  if (previewThumbScene2) {
    previewThumbScene2.addEventListener("click", () => {
      if (btnTabScene2) btnTabScene2.click();
    });
  }
  if (previewThumbScene3) {
    previewThumbScene3.addEventListener("click", () => {
      if (btnTabScene3) btnTabScene3.click();
    });
  }

  if (btnRightRender) {
    btnRightRender.addEventListener("click", () => {
      triggerRenderVideo();
    });
  }

  // Controles del Reproductor de Teléfono Móvil
  const btnLivePlayPause = document.getElementById("btnLivePlayPause");
  const btnLiveMute = document.getElementById("btnLiveMute");
  const btnLiveFullscreen = document.getElementById("btnLiveFullscreen");

  if (btnLivePlayPause) {
    btnLivePlayPause.addEventListener("click", () => {
      if (finalVideoPlayer && finalVideoPlayer.style.display !== "none") {
        if (finalVideoPlayer.paused) {
          finalVideoPlayer.play();
          btnLivePlayPause.textContent = "⏸";
        } else {
          finalVideoPlayer.pause();
          btnLivePlayPause.textContent = "▶";
        }
      } else if (audioPreviewPlayer) {
        if (audioPreviewPlayer.src && !audioPreviewPlayer.paused) {
          audioPreviewPlayer.pause();
          btnLivePlayPause.textContent = "▶";
        } else if (audioPreviewPlayer.src) {
          audioPreviewPlayer.play();
          btnLivePlayPause.textContent = "⏸";
        } else {
          triggerAudioPreview();
        }
      }
    });
  }

  if (btnLiveMute) {
    btnLiveMute.addEventListener("click", () => {
      const isMuted = (finalVideoPlayer && finalVideoPlayer.muted) || (audioPreviewPlayer && audioPreviewPlayer.muted);
      const newMute = !isMuted;
      if (finalVideoPlayer) finalVideoPlayer.muted = newMute;
      if (audioPreviewPlayer) audioPreviewPlayer.muted = newMute;
      btnLiveMute.textContent = newMute ? "🔇" : "🔊";
    });
  }

  if (btnLiveFullscreen) {
    btnLiveFullscreen.addEventListener("click", () => {
      const screen = document.querySelector(".phone-screen");
      if (screen) {
        if (!document.fullscreenElement) {
          if (screen.requestFullscreen) screen.requestFullscreen();
        } else {
          if (document.exitFullscreen) document.exitFullscreen();
        }
      }
    });
  }

  // ─── 5. BOTONES DE UTILIDAD EN ENCABEZADO ───────────────────────────
  const btnHeaderHelp = document.getElementById("btnHeaderHelp");
  if (btnHeaderHelp) {
    btnHeaderHelp.addEventListener("click", () => {
      alert("✨ Consejos para Reels Virales en Meta 2026:\n\n1. Gancho (0-3s): Capta la atención de inmediato con preguntas o declaraciones de fe directas.\n2. Inflexión (3-10s): Presenta la promesa de Dios o solución bíblica.\n3. Victoria y CTA (10s al final): Pide nombres de oración en comentarios para disparar el algoritmo de conversación.\n4. Calidad Fotorrealista: Usa Z-Image Turbo o FLUX.1 Schnell con iluminación celestial dorada.");
    });
  }

  const btnHeaderNotif = document.getElementById("btnHeaderNotif");
  if (btnHeaderNotif) {
    btnHeaderNotif.addEventListener("click", () => {
      alert("🔔 Estado del Estudio:\n\n• Motor de Render: FFmpeg H.264 1080x1920 MP4 Activo\n• Síntesis de Voz: Edge TTS Neuronal (Inglés Reverente)\n• Subtítulos: Montserrat / Cinzel con Resalte Activo Dinámico\n• 3 Escenas: Apertura (0-3.2s), Intercesión (3.2-10s) y Victoria");
    });
  }

  const btnHeaderSettings = document.getElementById("btnHeaderSettings");
  if (btnHeaderSettings) {
    btnHeaderSettings.addEventListener("click", () => {
      switchStage(5);
    });
  }

  // Botones de Acceso Rápido en la Sub-barra del Proyecto
  const btnQuickSync = document.getElementById("btnQuickSync");
  if (btnQuickSync) {
    btnQuickSync.addEventListener("click", () => {
      triggerSyncPrompt();
    });
  }
  const btnQuickReroll = document.getElementById("btnQuickReroll");
  if (btnQuickReroll) {
    btnQuickReroll.addEventListener("click", () => {
      if (btnRerollPrompt) btnRerollPrompt.click();
    });
  }
  const btnQuickAiKeys = document.getElementById("btnQuickAiKeys");
  if (btnQuickAiKeys) {
    btnQuickAiKeys.addEventListener("click", () => {
      if (btnToggleAiSettings) btnToggleAiSettings.click();
    });
  }
  const btnQuickRender = document.getElementById("btnQuickRender");
  if (btnQuickRender) {
    btnQuickRender.addEventListener("click", () => {
      triggerRenderVideo();
    });
  }

  async function loadAiProviderKeys() {
    try {
      if (aiHordeKeyInput && !aiHordeKeyInput.value) {
        aiHordeKeyInput.value = localStorage.getItem("aihorde_api_key") || "";
      }
      if (hfTokenInput && !hfTokenInput.value) {
        hfTokenInput.value = localStorage.getItem("hf_token") || "";
      }

      const res = await fetch("/api/image-providers");
      if (res.ok) {
        const data = await res.json();
        if (data.flux_schnell && data.flux_schnell.configured && hfTokenInput && !hfTokenInput.value) {
          hfTokenInput.placeholder = `Configurado en servidor (${data.flux_schnell.token_masked})`;
        }
      }
    } catch (_) {}
    updateAiProviderUI();
  }

  async function init() {
    await loadThemes();
    await loadVoices();
    await loadWorshipTracks();
    await loadBrollStatus();
    await loadImages();
    await loadRecentOutputs();
    await loadAiProviderKeys();
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
