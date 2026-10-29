"""Composición editorial local: diversidad narrativa y CTA contextual sin IA externa.

Las variantes se construyen a partir de las situaciones y textos específicos de
los 26 temas. No se prometen resultados ni se inventan testimonios.
"""
import random
import re
from engine.history import calculate_jaccard_similarity
from engine.thematic_variations import get_candidate_bodies_for_theme

NARRATION_TYPES = ("prayer", "reflection", "story", "comfort")

# Cada invitación menciona una necesidad humana del tema en lugar de pedir
# interacciones genéricas o condicionar bendiciones a comentarios.
CONTEXTUAL_CTAS = {
    "lost_child": [
        "If you're waiting for a call from someone you love, what helps you hold on to hope?",
        "Save this for a night when the distance from your child feels especially heavy.",
        "Share this with a parent who is learning to love without controlling every step.",
    ],
    "family_protection": [
        "What small act of kindness brought peace into your home this week?",
        "Save this prayer for an evening when everyone in your family needs to feel safe.",
        "Send this to someone carrying the quiet responsibility of caring for a family.",
    ],
    "marriage_healing": [
        "What gentle word could help begin a difficult conversation at home?",
        "Save this for the next time choosing patience feels harder than speaking.",
        "Share this with a couple who are rebuilding trust one honest conversation at a time.",
    ],
    "single_parent": [
        "What has helped you through a demanding day of caring for your children?",
        "Save this for a morning when parenting feels like more than one person can carry.",
        "Send this to a parent who rarely hears how much their quiet work matters.",
    ],
    "elderly_parents": [
        "What's one memory with an aging parent you wish you could revisit?",
        "Save this for a day when caregiving asks more of your heart than your energy.",
        "Share this with someone loving a parent through the changes of age.",
    ],
    "sick_grandchild": [
        "What simple comfort has helped your family through a child's difficult days?",
        "Save this prayer for a night when concern for a little one keeps you awake.",
        "Share this gently with a grandparent whose heart is carrying worry.",
    ],
    "morning_favor": [
        "What is one small thing you want to approach with grace today?",
        "Save this for the mornings when responsibilities arrive before your peace does.",
        "Send this to someone beginning another day with more courage than they feel.",
    ],
    "night_anxiety": [
        "Which thought is hardest for you to release at the end of the day?",
        "Save this for a sleepless night when your mind won't slow down.",
        "Share this with someone who finds the quietest hours the hardest.",
    ],
    "restless_sleep": [
        "What helps your heart settle when you can't find rest?",
        "Save this prayer for a night when sleep feels far away.",
        "Send this to someone who has been carrying their worries into bed.",
    ],
    "unspoken_prayer": [
        "Have you ever needed prayer but struggled to find the words?",
        "Save this for the days when your heart has more to say than your voice.",
        "Share this with someone who is carrying something they cannot yet explain.",
    ],
    "peace_in_storm": [
        "What has helped you stay grounded while everything around you changed?",
        "Save this for the next time a difficult day feels like a storm.",
        "Send this to someone facing more uncertainty than they expected.",
    ],
    "lonely_widow": [
        "What memory still brings warmth into a quiet room?",
        "Save this for an evening when missing someone feels particularly sharp.",
        "Share this with someone adjusting to a home that suddenly feels too quiet.",
    ],
    "grief_loss": [
        "Is there a small memory of someone you miss that still makes you smile?",
        "Save this reflection for a day when grief returns without warning.",
        "Share this gently with someone learning to live with an empty chair.",
    ],
    "healing_depression": [
        "What small act of care has helped you through an especially heavy day?",
        "Save this for a morning when even the next small step feels difficult.",
        "Send this with tenderness to someone who needs company rather than advice.",
    ],
    "medical_fear": [
        "What helps you feel less alone while waiting for medical answers?",
        "Save this prayer for an appointment day when uncertainty feels overwhelming.",
        "Share this with someone who needs courage during a long season of care.",
    ],
    "zero_balance": [
        "What practical kindness has helped you during a financially difficult season?",
        "Save this for a night when the unpaid bills seem louder than your hope.",
        "Send this to someone facing financial pressure without many people noticing.",
    ],
    "job_breakthrough": [
        "What has helped you keep your confidence after a difficult job search?",
        "Save this for the next day of waiting after another application.",
        "Share this with someone who needs reminding that their worth exceeds a job title.",
    ],
    "addiction_chains": [
        "What small, honest step has helped you move toward a healthier day?",
        "Save this for a day when recovery requires courage all over again.",
        "Share this privately with someone working hard to begin again.",
    ],
    "court_legal": [
        "What helps you stay patient when an important decision is beyond your control?",
        "Save this for a day when legal uncertainty makes it hard to rest.",
        "Send this to someone hoping for fairness during a long process.",
    ],
    "spiritual_warfare": [
        "Which Scripture helps steady you when fear grows loud?",
        "Save this for a moment when you need to remember you can pray honestly.",
        "Share this with a friend seeking courage and peace in their faith.",
    ],
    "strength_weary": [
        "When did someone last notice how much you've been carrying?",
        "Save this for the end of a day when you gave more than you had.",
        "Send this to the person who keeps showing up even when exhausted.",
    ],
    "guidance_direction": [
        "What decision have you been trying to make with patience and wisdom?",
        "Save this for the next time you're standing between two uncertain paths.",
        "Share this with someone trying to choose their next faithful step.",
    ],
    "gratitude_harvest": [
        "What ordinary blessing almost went unnoticed in your day?",
        "Save this as a reminder to notice the small gifts of this season.",
        "Share this with someone whose quiet kindness deserves to be seen.",
    ],
    "forgiving_past": [
        "What has helped you find peace without pretending the hurt never happened?",
        "Save this for a day when an old memory feels unexpectedly close.",
        "Send this to someone taking careful steps toward forgiveness.",
    ],
    "business_blessing": [
        "What value do you hope people experience through the work of your hands?",
        "Save this for a morning when the responsibility of your work feels heavy.",
        "Share this with someone building something honest with patience and faith.",
    ],
    "divine_grace": [
        "When has an unexpected act of grace changed an ordinary day?",
        "Save this for a moment when you're being harder on yourself than you need to be.",
        "Share this with someone who could use a reminder of mercy today.",
    ],
}

STORY_OPENERS = (
    "Picture an ordinary moment:",
    "Imagine a scene that seldom makes it into photographs:",
    "Consider this quiet moment:",
    "Think of a day that begins like so many others:",
)
REFLECTION_OPENERS = (
    "Scripture offers a quieter way to see this:",
    "Faith does not make this struggle imaginary.",
    "An honest question of faith sits beneath this moment:",
    "A biblical reminder can meet us in an ordinary room:",
)
COMFORT_OPENERS = (
    "There is room for weariness here.",
    "You do not have to make this moment look easy.",
    "Some burdens are carried without anyone noticing.",
    "A small moment of grace can still matter.",
)

def _sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]

def _pick_by_history(candidates, recent_texts, threshold=0.5):
    items = list(dict.fromkeys(s.strip() for s in candidates if s and s.strip()))
    if not items:
        return ""
    random.shuffle(items)
    def score(candidate):
        return max((calculate_jaccard_similarity(candidate, old) for old in recent_texts if old), default=0.0)
    good = [c for c in items if score(c) < threshold]
    return min(good or items, key=score)

def _shorten_at_sentence(text, max_words):
    parts = _sentences(text)
    chosen = []
    for sentence in parts:
        if len((" ".join(chosen + [sentence])).split()) > max_words:
            break
        chosen.append(sentence)
    return " ".join(chosen) if chosen else (parts[0] if parts else text)

def build_narration(theme_key, theme, narration_type, mode, custom_topic, recent_records, include_cta=True):
    """Devuelve texto narrativo, cierre y CTA alineados con un estilo explícito."""
    style = narration_type if narration_type in NARRATION_TYPES else "prayer"
    candidates = get_candidate_bodies_for_theme(theme_key)
    perspectives = theme.get("perspectives", {})
    recent_bodies = [r.get("body_snippet", "") for r in recent_records[-90:]]
    context = custom_topic.strip().rstrip(".") if custom_topic else theme.get("human_situation", "").strip().rstrip(".")
    central = theme.get("central_idea", "").strip()
    prayer_candidates = list(dict.fromkeys(candidates + [perspectives.get("prayer", "")]))
    prayer_candidates = [x for x in prayer_candidates if x]

    if style == "prayer":
        # Aumenta las combinaciones sin añadir frases genéricas: un inicio y
        # petición de la misma temática pueden provenir de variantes distintas.
        constructed = []
        for first in prayer_candidates:
            sentences = _sentences(first)
            for second in prayer_candidates:
                more = _sentences(second)
                if not sentences or not more:
                    continue
                if first == second:
                    constructed.append(first)
                else:
                    constructed.append(" ".join([sentences[0], *sentences[1:2], more[-1]]))
        body = _pick_by_history(constructed, recent_bodies, threshold=0.43)
    elif style == "reflection":
        scripture = perspectives.get("scripture_reflection", "")
        human = perspectives.get("heart_comfort", "")
        alternatives = [
            f"{intro} {scripture} {human}" for intro in REFLECTION_OPENERS
        ] + [f"{human} {scripture}", f"{scripture} {human}"]
        body = _pick_by_history(alternatives, recent_bodies)
    elif style == "comfort":
        human = perspectives.get("heart_comfort", "")
        reflection = perspectives.get("scripture_reflection", "")
        alternatives = [
            f"{intro} {human} {reflection}" for intro in COMFORT_OPENERS
        ] + [f"{human} {central}", f"{reflection} {human}"]
        body = _pick_by_history(alternatives, recent_bodies)
    else:
        # Un relato es una ilustración imaginada: no una falsa historia real.
        lesson = perspectives.get("story_lesson", "")
        comfort = perspectives.get("heart_comfort", "")
        scenarios = [
            f"{opener} {context}. {comfort} {central}"
            for opener in STORY_OPENERS
        ] + [
            f"{opener} {context}. {lesson} {comfort}"
            for opener in STORY_OPENERS if "once said" not in lesson.lower()
        ]
        body = _pick_by_history(scenarios, recent_bodies, threshold=0.48)

    # Una situación personalizada debe aparecer en el desarrollo, pero no
    # inyectamos fórmulas vacías ni afirmamos que la oración garantiza resultados.
    if custom_topic and custom_topic.strip() and custom_topic.lower() not in body.lower():
        detail = f"Bring this particular concern into prayer: {context}."
        if style == "prayer":
            detail = f"Lord, You know the situation we carry today: {context}."
        body = f"{detail} {body}"

    budget = {"micro": 23, "deep": 48, "story": 78}.get(mode, 48)
    body = _shorten_at_sentence(body, budget)
    recent_closings = [r.get("closing", "") for r in recent_records[-35:]]
    closings = theme.get("closings", [])
    closing = "" if mode == "micro" else _pick_by_history(closings, recent_closings, 0.6)

    ctas = CONTEXTUAL_CTAS.get(theme_key, [])
    recent_ctas = [r.get("cta", "") for r in recent_records[-75:]]
    # Evitar llamadas a la acción genéricas incluso al agotar variaciones.
    cta = _pick_by_history(ctas, recent_ctas, 0.55) if include_cta else ""
    return {"body": body, "closing": closing, "cta": cta, "narration_type": style}
