/* Editorial controls: no automatic Facebook access or publication. */
(() => {
  "use strict";
  const el = id => document.getElementById(id);
  const text = id => el(id)?.value.trim() || "";
  let script = null, themes = [], voices = [], selectedHook = 0, reviewVersion = 0;
  let previewVersion = 0, reviewTimer;
  let config = {};

  async function jsonRequest(url, options) {
    const response = await fetch(url, options);
    const data = await response.json();
    if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : `Error HTTP ${response.status}`);
    return data;
  }
  const post = (url, body) => jsonRequest(url, {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)});

  function filterThemes() {
    const select = el("themeSelect"), previous = select.value;
    const allowed = config[text("editorialSeries")]?.themes || themes.map(t => t.key);
    const visible = el("editorialAllThemes").checked ? themes : themes.filter(t => allowed.includes(t.key));
    select.replaceChildren(...visible.map(t => new Option(t.title, t.key)));
    if (visible.some(t => t.key === previous)) select.value = previous;
  }
  function filterVoices() {
    const select = el("voiceSelect"), previous = select.value;
    let visible = el("editorialAllVoices").checked ? voices : voices.filter(v => ["guy", "christopher"].includes(v.key));
    if (!visible.length) visible = voices;
    select.replaceChildren(...visible.map(v => new Option(v.name, v.key)));
    if (visible.some(v => v.key === previous)) select.value = previous;
    else if (visible.some(v => v.key === "guy")) select.value = "guy";
  }
  function getBrief() {
    return {series_key: text("editorialSeries"), audience: text("editorialAudience"),
      situation: text("editorialSituation") || text("customTopic"), central_idea: text("editorialIdea"),
      format: text("editorialFormat"), target_duration_sec: Number(text("editorialTarget")),
      include_cta: el("editorialIncludeCta").checked};
  }
  function updateCopy() {
    if (!script || el("reelPostCopyText").dataset.userEdited === "true") return;
    const hook = text("scriptHook"), cta = text("scriptCta");
    const copy = [script.english_title, hook, script.scripture,
      cta && cta !== hook ? cta : "", (script.hashtags || []).slice(0, 3).join(" ")].filter(Boolean).join("\n\n");
    el("reelPostCopyText").value = copy;
  }
  async function review() {
    const version = ++reviewVersion;
    try {
      const result = await post("/api/editorial-review", {hook: text("scriptHook"), body: text("scriptBody"),
        cta: text("scriptCta"), caption: text("reelPostCopyText"), target: Number(text("editorialTarget"))});
      if (version !== reviewVersion) return;
      const container = el("editorialReview");
      container.replaceChildren();
      const note = document.createElement("p");
      note.textContent = result.warnings.length ? "Antes de exportar:" : "Sin avisos automáticos. Revisa el sentido, el pasaje y la escucha final.";
      container.append(note);
      const list = document.createElement("ul");
      result.warnings.forEach(message => { const item = document.createElement("li"); item.textContent = message; list.append(item); });
      container.append(list);
    } catch (error) {
      if (version === reviewVersion) el("editorialReview").textContent = `No se pudo revisar: ${error.message}`;
    }
  }
  function setScript(data) {
    script = data; selectedHook = data.selected_hook_index || 0;
    el("reelPostCopyText").dataset.userEdited = "false";
    const container = el("editorialHooks");
    container.replaceChildren();
    (data.hook_alternatives || [data.hook]).forEach((hook, index) => {
      const button = document.createElement("button");
      button.type = "button"; button.className = "btn btn-outline editorial-hook";
      button.textContent = `${index + 1}. ${hook}`;
      button.setAttribute("aria-pressed", String(index === selectedHook));
      button.addEventListener("click", () => {
        selectedHook = index; el("scriptHook").value = hook;
        container.querySelectorAll("button").forEach((b, i) => b.setAttribute("aria-pressed", String(i === index)));
        el("scriptHook").dispatchEvent(new Event("input", {bubbles: true}));
      });
      container.append(button);
    });
    updateCopy(); review();
  }

  async function openingPreview() {
    if (!text("scriptHook")) { el("editorialReview").textContent = "Escribe o genera una apertura primero."; return; }
    const version = ++previewVersion;
    const dialog = el("editorialOpeningDialog"), audio = el("editorialOpeningAudio");
    audio.pause(); audio.removeAttribute("src");
    el("editorialOpeningText").textContent = text("scriptHook");
    const image = el("stageSelectedImage");
    el("editorialOpeningImage").src = image?.src || "";
    el("editorialOpeningStatus").textContent = "Preparando locución…";
    if (!dialog.open) dialog.showModal();
    try {
      const data = await post("/api/preview-audio", {text: [text("scriptHook"), text("scriptBody")].join(" ").split(/\s+/).slice(0, 25).join(" "),
        voice_key: text("voiceSelect"), rate: text("rateSelect")});
      if (version !== previewVersion || !dialog.open) return;
      audio.src = data.audio_url;
      el("editorialOpeningStatus").textContent = "La escucha se detiene a los 3 segundos. Puedes repetirla con Reproducir.";
      await audio.play().catch(() => {});
    } catch (error) { if (version === previewVersion) el("editorialOpeningStatus").textContent = error.message; }
  }
  const audio = el("editorialOpeningAudio");
  audio.addEventListener("timeupdate", () => { if (audio.currentTime >= 3) audio.pause(); });
  audio.addEventListener("play", () => { if (audio.currentTime >= 3) audio.currentTime = 0; });
  el("editorialOpeningDialog").addEventListener("close", () => { previewVersion++; audio.pause(); });
  el("btnCloseOpeningPreview").addEventListener("click", () => el("editorialOpeningDialog").close());
  el("btnOpeningPreview").addEventListener("click", openingPreview);
  el("btnEditorialReview").addEventListener("click", review);
  ["editorialSeries", "editorialAllThemes"].forEach(id => el(id).addEventListener("change", () => {
    filterThemes(); el("themeSelect").dispatchEvent(new Event("change", {bubbles: true}));
  }));
  el("editorialAllVoices").addEventListener("change", filterVoices);
  el("scriptDurationMode").addEventListener("change", () => {
    el("editorialTarget").value = {micro: 14, deep: 22, story: 40}[text("scriptDurationMode")] || 22;
    el("editorialTarget").dispatchEvent(new Event("input"));
  });
  ["scriptHook", "scriptBody", "scriptCta", "editorialTarget", "reelPostCopyText"].forEach(id => {
    el(id).addEventListener("input", () => {
      if (id === "reelPostCopyText") el(id).dataset.userEdited = "true";
      updateCopy(); clearTimeout(reviewTimer); reviewTimer = setTimeout(review, 350);
    });
  });

  const metricFields = {duration_sec: "metricDuration", views: "metricViews", average_watch_sec: "metricWatch",
    average_watched_pct: "metricPercent", followers: "metricFollowers", shares: "metricShares",
    us_viewer_pct: "metricUs", main_dropoff_sec: "metricDropoff"};
  const showMetric = value => value === null || value === undefined ? "—" : String(value);
  async function loadResults() {
    const rows = el("editorialResultsRows"), select = el("editorialRecord"), previous = select.value;
    const records = await jsonRequest("/api/editorial-results");
    select.replaceChildren(new Option("Registrar el guion actual como una publicación nueva", ""));
    rows.replaceChildren();
    records.forEach(record => {
      select.add(new Option(record.creative.hook.slice(0, 85), record.id));
      record.observations.forEach(observation => {
        const row = document.createElement("tr"), m = observation.metrics;
        [record.creative.hook, observation.checkpoint, m.views, m.average_watch_sec,
          m.average_watched_pct, m.us_viewer_pct, m.followers].forEach(value => {
          const cell = document.createElement("td"); cell.textContent = showMetric(value); row.append(cell);
        });
        rows.append(row);
      });
    });
    if (records.some(r => r.id === previous)) select.value = previous;
    return records;
  }
  el("editorialRecord").addEventListener("change", () => {
    Object.values(metricFields).forEach(id => { el(id).value = ""; });
    el("editorialPostUrl").value = "";
  });
  el("editorialResultsForm").addEventListener("submit", async event => {
    event.preventDefault();
    const button = event.submitter; if (button) button.disabled = true;
    try {
      const metrics = Object.fromEntries(Object.entries(metricFields).map(([name, id]) => [name, text(id) === "" ? null : Number(text(id))]));
      if (!text("editorialRecord") && !text("scriptHook")) throw new Error("Genera o escribe el guion antes de registrar una publicación nueva.");
      const record = await post("/api/editorial-results", {record_id: text("editorialRecord") || null,
        creative: {theme_key: script?.theme_key || text("themeSelect"), series_key: script?.series_key || text("editorialSeries"),
          format: script?.editorial_format || text("editorialFormat"), hook: text("scriptHook"), body: text("scriptBody"),
          cta: text("scriptCta"), caption: text("reelPostCopyText"), voice: text("voiceSelect"),
          provider: script?.provider_used || "manual", opening_variant: selectedHook},
        checkpoint: text("editorialCheckpoint"), post_url: text("editorialPostUrl") || null, metrics});
      await loadResults(); el("editorialRecord").value = record.id;
      el("editorialResultsStatus").textContent = "Observación guardada. La próxima observación conservará el guion original de esta publicación.";
    } catch (error) { el("editorialResultsStatus").textContent = `No se pudo completar el registro: ${error.message}`; }
    finally { if (button) button.disabled = false; }
  });
  el("btnRefreshEditorialResults").addEventListener("click", () => loadResults().catch(e => { el("editorialResultsStatus").textContent = e.message; }));
  el("editorialResultsPanel").addEventListener("toggle", () => {
    if (el("editorialResultsPanel").open) loadResults().catch(e => { el("editorialResultsStatus").textContent = e.message; });
  });
  window.EditorialStudio = {getBrief, setScript, configureThemes(list, series) { themes = list; config = series; filterThemes(); },
    configureVoices(list) { voices = list; filterVoices(); }, getTarget() { return Number(text("editorialTarget")) || 22; }};
})();
