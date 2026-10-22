// Run with jsdom available via NODE_PATH; no browser, TTS or Facebook connection.
const assert = require("node:assert/strict");
const fs = require("node:fs");
const path = require("node:path");
const {JSDOM} = require("jsdom");
const root = path.join(__dirname, "..");
const dom = new JSDOM(fs.readFileSync(path.join(root, "static/index.html"), "utf8"), {
  url: "http://localhost:8050", runScripts: "outside-only"
});
const w = dom.window, get = id => w.document.getElementById(id);
const calls = [], records = [];
let failReview = false, pauses = 0;
w.HTMLMediaElement.prototype.pause = function () { pauses++; };
w.HTMLMediaElement.prototype.play = async function () {};
get("editorialOpeningDialog").showModal = function () { this.open = true; };
get("editorialOpeningDialog").close = function () { this.open = false; this.dispatchEvent(new w.Event("close")); };
w.fetch = async (url, options = {}) => {
  const body = options.body ? JSON.parse(options.body) : null;
  calls.push({url, body});
  if (url === "/api/editorial-review") return {ok: !failReview, status: failReview ? 500 : 200,
    json: async () => failReview ? {detail: "Review offline"} : {warnings: []}};
  if (url === "/api/preview-audio") return {ok: true, json: async () => ({audio_url: "/outputs/preview_test.mp3"})};
  if (url === "/api/editorial-results" && body) {
    const record = {id: "saved", creative: body.creative, observations: [{checkpoint: body.checkpoint, metrics: body.metrics}]};
    records.push(record); return {ok: true, json: async () => record};
  }
  return {ok: true, json: async () => records};
};
w.eval(fs.readFileSync(path.join(root, "static/editorial.js"), "utf8"));
const studio = w.EditorialStudio;
const flush = async () => { await new Promise(setImmediate); await new Promise(setImmediate); };

(async () => {
  const themes = [{key: "lost_child", title: "Hijos"}, {key: "morning_favor", title: "Mañana"}];
  studio.configureThemes(themes, {everyday: {themes: ["lost_child"]}, quiet: {themes: ["morning_favor"]}});
  assert.equal(get("themeSelect").options.length, 1);
  get("editorialAllThemes").checked = true;
  get("editorialAllThemes").dispatchEvent(new w.Event("change"));
  assert.equal(get("themeSelect").options.length, 2);
  studio.configureVoices(["guy", "christopher", "brian"].map(key => ({key, name: key})));
  assert.equal(get("voiceSelect").options.length, 2);
  get("editorialAllVoices").checked = true;
  get("editorialAllVoices").dispatchEvent(new w.Event("change"));
  assert.equal(get("voiceSelect").options.length, 3);
  const data = {theme_key: "lost_child", english_title: "A Quiet Phone", scripture: "Luke 15:20", body: "Listen with patience.",
    hook_alternatives: ["The phone stays quiet.", "Your child is grown.", "Love leaves room."], selected_hook_index: 1, hashtags: ["#Faith"]};
  get("scriptHook").value = data.hook_alternatives[1]; get("scriptBody").value = data.body;
  studio.setScript(data); await flush();
  assert.equal(get("editorialHooks").querySelector('[aria-pressed="true"]').textContent.startsWith("2."), true);
  get("editorialHooks").querySelectorAll("button")[2].click();
  assert.equal(get("scriptHook").value, "Love leaves room.");
  assert.match(get("reelPostCopyText").value, /Love leaves room/);
  get("reelPostCopyText").value = "My manually edited English caption.";
  get("reelPostCopyText").dispatchEvent(new w.Event("input"));
  get("editorialHooks").querySelectorAll("button")[0].click();
  assert.equal(get("reelPostCopyText").value, "My manually edited English caption.");
  get("btnOpeningPreview").click(); await flush();
  assert.equal(get("editorialOpeningDialog").open, true);
  assert.match(get("editorialOpeningAudio").src, /preview_test/);
  const before = pauses; get("editorialOpeningAudio").currentTime = 3.1;
  get("editorialOpeningAudio").dispatchEvent(new w.Event("timeupdate"));
  assert.equal(pauses, before + 1);
  get("btnCloseOpeningPreview").click();
  get("metricViews").value = "0";
  get("editorialResultsForm").dispatchEvent(new w.Event("submit", {cancelable: true})); await flush();
  const saved = calls.find(c => c.url === "/api/editorial-results" && c.body).body;
  assert.equal(saved.metrics.views, 0);
  assert.equal(saved.metrics.average_watch_sec, null);
  assert.equal(saved.creative.hook, "The phone stays quiet.");
  assert.equal(get("editorialResultsRows").children.length, 1);
  assert.match(get("editorialResultsStatus").textContent, /guardada/);
  failReview = true; get("btnEditorialReview").click(); await flush();
  assert.match(get("editorialReview").textContent, /Review offline/);
  console.log("Editorial UI smoke: PASS (themes, voices, openings, caption editing, preview, observations, errors)");
  w.close();
})().catch(error => { w.close(); console.error(error); process.exitCode = 1; });
