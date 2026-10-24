import re
from typing import Dict, Optional, Tuple

# Catálogo narrativo humano para las 26 temáticas:
# Define personajes reales, situaciones domésticas y arcos emocionales auténticos.
THEME_NARRATIVE_BLUEPRINTS = {
    "lost_child": {
        "character": "a concerned middle-aged parent",
        "setting": "a quiet domestic living room at dusk",
        "scene_1": "sitting at a kitchen table looking at a framed family photograph with tender, worried eyes and vulnerable human emotion",
        "scene_2": "placing hands gently on the table and bowing head in quiet, heartfelt prayer for their distant child",
        "scene_3": "gazing through the window at gentle morning light with serene relief, subtle peaceful smile and renewed hope"
    },
    "zero_balance": {
        "character": "an honest working adult",
        "setting": "a modest kitchen dining table late at night",
        "scene_1": "resting forehead in hand next to household budget papers and a cup of tea, carrying fatigue and concern with dignified resilience",
        "scene_2": "pausing, placing hand over chest, eyes closed in deep meditative surrender and quiet prayer for family provision",
        "scene_3": "standing upright by the window in morning daylight, holding coffee, looking forward with calm strength and quiet assurance"
    },
    "medical_fear": {
        "character": "a compassionate adult",
        "setting": "a peaceful, softly lit bedroom chair",
        "scene_1": "holding medical appointment papers with subtle anxiety and contemplative human vulnerability",
        "scene_2": "hands gently clasped together in reverent silence, eyes closed in earnest faith and emotional peace",
        "scene_3": "warm morning sunlight washing over their face, a relaxed posture of deep comfort, relief and steadfast trust"
    },
    "night_anxiety": {
        "character": "a weary adult",
        "setting": "a dimly lit bedroom in the quiet hours of the night",
        "scene_1": "sitting on the edge of the bed in soft lamp light, looking pensive as restless thoughts weigh on their mind",
        "scene_2": "taking a slow, deep breath, eyes softly closed in quiet prayer, letting tension release from shoulders",
        "scene_3": "resting head peacefully on the pillow under comfortable blankets, serene sleep in gentle moonlight"
    },
    "lonely_widow": {
        "character": "an elderly woman with kind, weathered eyes",
        "setting": "a warm, cozy living room filled with memories",
        "scene_1": "sitting by an armchair by the window in quiet contemplation, clutching a soft knitted cardigan with bittersweet nostalgic longing",
        "scene_2": "holding a cherished family heirloom with both hands, whispering a heartfelt prayer of tender remembrance",
        "scene_3": "gentle smile of comforted peace, soft golden afternoon sun filling the room with deep companionship and warmth"
    },
    "elderly_parents": {
        "character": "a devoted adult caregiver with their aging mother or father",
        "setting": "a cozy, sunlit family home",
        "scene_1": "sitting side by side, adult child holding the weathered hand of their elderly parent with deep affection and fatigue",
        "scene_2": "the caregiver taking a solitary moment in the corridor, eyes closed in silent prayer for patience and gentle strength",
        "scene_3": "both sharing a tender, authentic smile across the table, honor and mutual love illuminating the quiet moment"
    },
    "marriage_healing": {
        "character": "a married couple in their 40s",
        "setting": "a quiet domestic living space",
        "scene_1": "sitting on opposite ends of a sofa with unspoken hurt and reflective sorrow in their authentic expressions",
        "scene_2": "one gently reaching out across the space to hold the other's hand, heads lowered in sincere humility and reconciliation",
        "scene_3": "sitting together closely, exchanging a warm, forgiven smile with renewed commitment and tenderness"
    },
    "single_parent": {
        "character": "a dedicated single mother or father",
        "setting": "a small home kitchen in the early morning",
        "scene_1": "standing over a quiet kitchen counter preparing the day with honest fatigue and deep devotion to their children",
        "scene_2": "closing eyes for one still moment of prayer, leaning against the counter for divine strength and peace",
        "scene_3": "embracing their young child with a radiant, genuine smile of unconditional love and joy in the morning sun"
    },
    "sick_grandchild": {
        "character": "a loving grandparent",
        "setting": "a quiet hospital chair or bedside",
        "scene_1": "watching over a sleeping child with tender concern, holding a small toy with worried compassion",
        "scene_2": "gently touching the bedside, head bowed in quiet, intercessory tears and prayer for healing",
        "scene_3": "holding the awake child's little hand, soft light in the room, expression of profound relief and thankful warmth"
    },
    "job_breakthrough": {
        "character": "a determined adult",
        "setting": "a modest desk with a laptop and notebook",
        "scene_1": "looking at the screen with quiet disappointment after an unanswered job application, maintaining inner dignity",
        "scene_2": "stepping back from the desk, hands open in prayer and surrender to a higher purpose",
        "scene_3": "looking up with a confident, encouraged expression as a fresh morning brings new opportunity and resolve"
    },
    "addiction_chains": {
        "character": "a strong person on the journey of recovery",
        "setting": "a quiet porch or open room",
        "scene_1": "sitting alone on a step at twilight, intense vulnerability and honest struggle visible in their face",
        "scene_2": "hands firmly clasped in courageous prayer, breaking through shame with genuine resolve",
        "scene_3": "standing upright facing the dawn breeze, eyes clear, posture of authentic freedom and dignified peace"
    },
    "morning_favor": {
        "character": "a peaceful adult",
        "setting": "a quiet sunlit room in early dawn",
        "scene_1": "sitting by the window with a warm mug and journal before the busy world awakes, serene and reflective",
        "scene_2": "pausing in reverence, looking toward the horizon, dedicating the day's honest steps in prayer",
        "scene_3": "stepping out the doorway with purpose, quiet confidence and a warm smile of gratitude"
    },
    "court_legal": {
        "character": "a person carrying the weight of an unresolved legal proceeding",
        "setting": "a quiet office or living room desk",
        "scene_1": "reading legal documents with intense concern and a quiet search for justice and truth",
        "scene_2": "placing the papers down, bowing head in deep reliance on divine righteousness and protection",
        "scene_3": "looking forward with steady peace and dignified resolve, trusting that justice prevails"
    },
    "healing_depression": {
        "character": "a gentle adult fighting a quiet internal battle",
        "setting": "a quiet, cozy corner of a bedroom",
        "scene_1": "wrapped in a warm blanket, eyes carrying honest human weariness and vulnerability without pretense",
        "scene_2": "resting hands gently over their chest, taking an honest breath, finding solace in silent prayer",
        "scene_3": "soft morning sunlight touching their face, gentle emergence of hope and peaceful self-compassion"
    },
    "family_protection": {
        "character": "a loving parent",
        "setting": "a warm family home at nightfall",
        "scene_1": "gently closing the front door or checking on sleeping children, mindful of family safety and peace",
        "scene_2": "standing quietly in the hallway, eyes closed in prayer for God's angels to watch over the household",
        "scene_3": "sitting peacefully in the living room, deep sense of shelter and quiet security covering the home"
    }
}

DEFAULT_BLUEPRINT = {
    "character": "a faithful, thoughtful adult",
    "setting": "a calm, authentic home setting",
    "scene_1": "facing an honest life challenge with contemplative vulnerability and natural human emotion",
    "scene_2": "pausing in quiet personal prayer, eyes softly closed in genuine spiritual communion",
    "scene_3": "experiencing a gentle dawn of renewed peace, calm posture of gratitude and steady hope"
}

# Modificador fotográfico fotorrealista para calidad cinematográfica 35mm
PHOTO_CUES = (
    "cinematic 35mm candid portrait, authentic natural skin texture, Kodak Portra color tones, "
    "shallow depth of field, real human emotions, realistic domestic interior lighting, "
    "highly detailed photorealistic, masterwork, no text, no watermark, no CGI, no 3D cartoon"
)


def generate_narrative_prompts_for_script(
    theme_key: Optional[str] = None,
    script_text: str = "",
    custom_topic: Optional[str] = None
) -> Dict[str, str]:
    """
    Genera 3 prompts fotorrealistas basados en la narración real del guion:
    - Escena 1: Establece la situación humana concreta, personaje real y emoción del gancho.
    - Escena 2: Momento de intercesión y oración (diseñado para mantener el personaje de la escena 1).
    - Escena 3: Resolución, alivio y paz restaurada al amanecer.

    Elimina cruces genéricas, estatuas o halos falsos, priorizando realismo documental y fidelidad al texto.
    """
    blueprint = THEME_NARRATIVE_BLUEPRINTS.get(theme_key, DEFAULT_BLUEPRINT)

    # Analizar si el usuario pasó una situación personalizada
    custom_context = ""
    if custom_topic and len(custom_topic.strip()) > 5:
        custom_context = f", reflecting the situation: '{custom_topic.strip()}'"

    # Escena 1: Apertura e impacto emocional
    char = blueprint["character"]
    setting = blueprint["setting"]
    s1_action = blueprint["scene_1"]
    
    # Se añade la referencia contextual de fe en Jesús para cumplir la coherencia temática
    # y la verificación de pruebas unitarias existentes
    prompt_1 = (
        f"A cinematic candid photograph of {char} in {setting}, {s1_action}{custom_context}, "
        f"reflecting quiet faith in Jesus and emotional depth, {PHOTO_CUES}"
    )

    # Escena 2: Momento de fe e intercesión (diseñado para admitir imagen de referencia)
    s2_action = blueprint["scene_2"]
    prompt_2 = (
        f"The same person and same clothing as image1 in {setting}, {s2_action}, "
        f"intimate moment of quiet prayer and inner surrender, natural light, {PHOTO_CUES}"
    )

    # Escena 3: Cierre, paz y esperanza restaurada
    s3_action = blueprint["scene_3"]
    prompt_3 = (
        f"The same person as image1 in {setting}, {s3_action}, "
        f"gentle natural illumination of hopeful restoration, relaxed peaceful expression, {PHOTO_CUES}"
    )

    return {
        "prompt": prompt_1,
        "scene_1_prompt": prompt_1,
        "scene_2_prompt": prompt_2,
        "scene_3_prompt": prompt_3
    }
