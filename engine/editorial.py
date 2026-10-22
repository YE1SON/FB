"""Editorial briefs, English publishing copy and a factual quality checklist.

This module makes no predictions about reach or virality. All lengths are
estimates until the generated audio and final MP4 have been inspected.
"""
import re


# Internal Spanish category labels remain in scripts.py; publishing titles are English.
# Each theme has a different concrete opening rather than a generic prayer heading.
THEME_OPENINGS = {
    "lost_child": ("When Your Grown Child Pulls Away", "Your child is grown. You still worry.", "The phone stays quiet tonight.", "Love can leave room for listening."),
    "family_protection": ("Peace After a Difficult Day", "The argument ended. The tension stayed.", "Home feels tense after today.", "Peace can begin with one kind word."),
    "medical_fear": ("While You Wait for Answers", "The test results are not back yet.", "Waiting makes the hours feel longer.", "You can pray without having the answers."),
    "zero_balance": ("When the Bills Feel Heavy", "Another bill. The same paycheck.", "The numbers still do not add up.", "One difficult month is not your worth."),
    "night_anxiety": ("When Your Mind Will Not Rest", "The house is quiet. Your mind is not.", "Tomorrow keeps interrupting tonight.", "You can rest before everything is resolved."),
    "morning_favor": ("Before the Day Gets Busy", "The day starts before you feel ready.", "Your to-do list can wait one moment.", "Begin with grace, before the demands."),
    "marriage_healing": ("Making Room for Reconciliation", "You share a home, but feel distant.", "That conversation still hurts.", "Listening can be a beginning."),
    "healing_depression": ("Faith on a Difficult Morning", "Getting out of bed feels hard today.", "Some mornings ask more of you.", "Struggling does not make your faith smaller."),
    "job_breakthrough": ("After Another Job Rejection", "Another application. Another quiet inbox.", "The rejection email arrived today.", "A job title cannot measure your worth."),
    "lonely_widow": ("When the House Feels Empty", "Dinner is ready. One chair stays empty.", "Evenings can feel especially quiet.", "Missing someone leaves room for love."),
    "addiction_chains": ("Faith for the Next Small Step", "Today asks for another honest step.", "You do not have to struggle alone.", "Asking for support can be an act of faith."),
    "elderly_parents": ("When Caring for a Parent Is Hard", "You love your parent. You feel exhausted.", "Work ended. Your caregiving day continues.", "Needing rest does not mean loving less."),
    "single_parent": ("Grace for a Tired Parent", "Everyone needs you. You need rest too.", "The children sleep. The chores remain.", "You deserve care as you give it."),
    "sick_grandchild": ("When Your Grandchild Is Unwell", "You wish you could carry their pain.", "The family waits for another update.", "Love can sit quietly beside uncertainty."),
    "court_legal": ("Before a Difficult Appointment", "Tomorrow's appointment keeps you awake.", "The paperwork feels heavier tonight.", "You can seek wisdom one step at a time."),
    "restless_sleep": ("A Prayer Before Sleep", "The lights are off. Worry stays awake.", "You keep replaying the day.", "Tonight can end without every answer."),
    "gratitude_harvest": ("Finding Gratitude in Ordinary Things", "The ordinary things deserve a second look.", "What helped you through today?", "Gratitude can begin with something small."),
    "unspoken_prayer": ("When Prayer Has Few Words", "You sit down to pray. Words fail.", "Some prayers begin with a sigh.", "You can come to God without a speech."),
    "spiritual_warfare": ("Standing Firm Through Fear", "Fear has been doing all the talking.", "The same anxious thought returns.", "Courage can be quiet and steady."),
    "business_blessing": ("Faith in Your Daily Work", "You closed the shop. Worry came home.", "The workday ended with unfinished questions.", "Integrity matters on the difficult days too."),
    "forgiving_past": ("When an Old Hurt Returns", "An old memory interrupted today.", "Forgiveness can feel unfinished.", "You can seek peace while keeping wise boundaries."),
    "grief_loss": ("When Grief Changes Your Day", "You reached for the phone, then remembered.", "A familiar song brought the tears back.", "Grief does not follow a tidy schedule."),
    "guidance_direction": ("When the Next Step Is Unclear", "Both choices feel uncertain.", "You keep asking which way to go.", "Wisdom can begin with one small step."),
    "strength_weary": ("Grace When You Are Worn Out", "You got through today. You feel empty.", "Being strong has become exhausting.", "Rest belongs in a faithful life too."),
    "peace_in_storm": ("Peace in an Unsettled Season", "The bad news keeps arriving.", "Everything feels unsettled this week.", "Peace can share a room with uncertainty."),
    "divine_grace": ("Grace After a Difficult Day", "You are still replaying that mistake.", "Today did not go as you hoped.", "One mistake is not your whole story."),
}

SERIES = {
    "everyday": {"name": "Faith for Everyday Life", "themes": [
        "lost_child", "elderly_parents", "zero_balance", "marriage_healing",
        "single_parent", "sick_grandchild", "job_breakthrough", "medical_fear",
        "court_legal", "business_blessing", "addiction_chains", "guidance_direction"]},
    "quiet": {"name": "A Quiet Moment with God", "themes": [
        "morning_favor", "night_anxiety", "restless_sleep", "grief_loss",
        "family_protection", "lonely_widow", "healing_depression", "gratitude_harvest",
        "unspoken_prayer", "spiritual_warfare", "forgiving_past", "strength_weary",
        "peace_in_storm", "divine_grace"]},
}

FORMATS = {"prayer": "prayer", "reflection": "scripture_reflection", "story": "story_lesson"}


def english_title(theme_key):
    return THEME_OPENINGS.get(theme_key, ("A Moment of Faith",))[0]


def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def clean_narration(text):
    text = re.sub(r"\s+", " ", text or "").strip()
    # Remove the legacy unfinished bridge; loops must never add dangling sentences.
    text = re.sub(r"\s*[—–-]?\s*(?:Before you close your eyes in sleep tonight, remember that|And always remember that|Hold onto this promise tonight, and remember that|As scripture quietly declares)\s*\.{0,3}\s*$", "", text, flags=re.I)
    unique, seen = [], set()
    for sentence in sentences(text):
        normalized = re.sub(r"\W+", " ", sentence).strip().lower()
        if normalized not in seen:
            unique.append(sentence)
            seen.add(normalized)
    return " ".join(unique).strip(" —–-")


def review_script(hook, body, cta="", caption="", target=22):
    narration = " ".join(filter(None, [hook, body, cta]))
    warnings = []
    if len(hook.split()) > 9:
        warnings.append("La apertura tiene más de 9 palabras: escucha si la situación se entiende en los primeros segundos.")
    if re.search(r"[áéíóúñ¿¡]|\b(?:oración|protección|sabiduría|dificultad|señor|hijos)\b", narration + " " + caption, re.I):
        warnings.append("Posible texto en español dentro del contenido público. Revisa el inglés antes de exportar.")
    if re.search(r"(?:remember that|because|and then)\s*(?:\.{3}|…)?$", narration, re.I):
        warnings.append("El cierre parece inconcluso. Termina la idea antes de publicar.")
    normalized = [re.sub(r"\W+", " ", s).lower().strip()
                  for part in (hook, body, cta) for s in sentences(part)]
    if len(normalized) != len(set(normalized)):
        warnings.append("Hay frases repetidas en la narración.")
    if re.search(r"(?:share|comment|type).{0,60}(?:claim|miracle|receive a blessing)|God wants you to hear|Jesus says:", narration, re.I):
        warnings.append("Revisa la atribución a Dios y cualquier beneficio espiritual condicionado a interactuar.")
    estimate = round(len(narration.split()) / (125 / 60), 1)
    if estimate > target + 3:
        warnings.append(f"La estimación ({estimate} s) supera el objetivo ({target:g} s). Recorta una frase y vuelve a escuchar.")
    return {"warnings": warnings, "estimated_duration_sec": estimate,
            "note": "Revisión editorial orientativa; no verifica teología ni predice rendimiento."}


def scene_prompts(theme_key, script_text, situation=""):
    """Use actual narrative beats. The text is context, never a request to draw text."""
    beats = sentences(clean_narration(script_text))
    if not beats:
        return None
    first, middle, last = " ".join(beats[:2]), beats[len(beats) // 2], beats[-1]
    contexts = [
        f"Opening context: {situation or first}. Narrative beat: {first}",
        f"Development of the same person's situation. Narrative beat: {middle}",
        f"Closing reflection in the same setting. Narrative beat: {last}",
    ]
    prompts = [f"Editorial photograph illustrating this context: {context}. "
               "An adult in an everyday setting consistent with the narrative; show an appropriate visible action, "
               "consistent character and environment, natural light, balanced vertical composition. "
               "Do not depict an outcome not established in the narration. No text or lettering. --ar 9:16"
               for context in contexts]
    return {"prompt": prompts[0], **{f"scene_{i+1}_prompt": p for i, p in enumerate(prompts)}}


def apply_brief(result, brief, theme):
    """Direct the finite local template honestly; Ollama keeps its generated body."""
    from engine.scripts import generate_seo_caption
    key = result["theme_key"]
    opening = THEME_OPENINGS.get(key, (english_title(key), "Today asks for a little grace.",
                                      "What has been weighing on you?", "Begin with one faithful step."))
    situation = (brief.get("situation") or "").strip()
    idea = (brief.get("central_idea") or "").strip()
    fmt = brief.get("format", "prayer")
    alternatives = list(opening[1:])
    if situation:
        alternatives = [situation.rstrip(".!?") + ".",
                        f"A moment of faith for this: {situation.rstrip('.!?')}.",
                        f"Bring this concern into prayer: {situation.rstrip('.!?')}."]
    from engine.history import get_history_manager
    history = get_history_manager()
    recent_hooks = [r.get("hook", "") for r in history.load_history()[-15:]]
    selected = next((i for i, hook in enumerate(alternatives) if hook not in recent_hooks), None)
    if selected is None:
        last = recent_hooks[-2] if len(recent_hooks) >= 2 else ""
        selected = next((i for i, hook in enumerate(alternatives) if hook != last), 0)
    result["hook"] = alternatives[selected]
    if not result.get("provider_used", "").startswith("ollama ("):
        perspective = FORMATS.get(fmt, "prayer")
        base = theme.get("perspectives", {}).get(perspective, result["body"])
        body = " ".join(sentences(clean_narration(base))[:2])
        if fmt == "story":
            # Clearly an imagined everyday illustration, never a fabricated testimony.
            context = situation or theme.get("human_situation", "A person having a difficult day")
            body = f"Imagine this everyday scene: {context.rstrip('.')}. "
            body += " " .join(sentences(clean_narration(theme.get("perspectives", {}).get("heart_comfort", base)))[:1])
        result["body"] = body
    if idea:
        result["body"] = clean_narration(result["body"] + " " + idea.rstrip(".!?") + ".")
    if result.get("mode") == "micro":
        result["body"] = " ".join(sentences(result["body"])[:1])
    elif result.get("mode") == "story":
        result["body"] += " " + theme.get("central_idea", "")
    result["body"] = clean_narration(result["body"])
    # CTA is genuinely optional. No additional generic conclusion is appended.
    result["cta"] = "May God's peace be with you today." if brief.get("include_cta") else ""
    result["closing"] = ""
    result["full_text"] = " ".join(filter(None, [result["hook"], result["body"], result["cta"]]))
    result["word_count"] = len(result["full_text"].split())
    result["estimated_duration_sec"] = round(result["word_count"] / (125 / 60), 1)
    result["target_duration_sec"] = brief.get("target_duration_sec", 22)
    result["english_title"] = english_title(key)
    result["hook_badge_text"] = english_title(key).upper()
    result["micro_cta_text"] = ""
    result["series_key"] = brief.get("series_key", "everyday")
    result["editorial_format"] = fmt
    result["audience"] = brief.get("audience", "US adults")
    result["human_situation"] = situation or theme.get("human_situation", "")
    result["central_idea"] = idea or theme.get("central_idea", "")
    result["hook_alternatives"] = alternatives
    result["selected_hook_index"] = selected
    result["seamless_loop"] = False
    result["seo_caption"] = generate_seo_caption(result["english_title"], result["full_text"],
                                                  result["scripture"], result["cta"], result["hashtags"])
    result["pinned_comment"] = "A moment to reflect on today's passage together."
    result.update(scene_prompts(key, result["full_text"], result["human_situation"]) or {})
    result["image_prompt"] = result["scene_1_prompt"]
    result["editorial_review"] = review_script(result["hook"], result["body"], result["cta"],
                                               result["seo_caption"], result["target_duration_sec"])
    history.record_script(key, result["hook"], result["body"], result["cta"],
                          [result[f"scene_{i}_prompt"] for i in (1, 2, 3)])
    return result
