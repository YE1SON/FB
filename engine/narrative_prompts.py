import re
import random
from typing import Dict, Optional, Tuple

# Catálogo narrativo humano para las 26 temáticas:
# Cada temática define un personaje real, un entorno auténtico y la presencia reverente y contextual
# de Jesucristo interactuando en las 3 escenas de acuerdo al propósito de la oración:
# - Escena 1: Situación humana vulnerable con Jesucristo presente a su lado con mirada compasiva y consuelo.
# - Escena 2: Momento de oración e intercesión con Jesucristo posando su mano amorosa sobre el hombro/manos.
# - Escena 3: Restauración, paz y esperanza con Jesucristo bendiciendo al personaje bajo luz matutina.

THEME_NARRATIVE_BLUEPRINTS = {
    "lost_child": {
        "character": "a concerned middle-aged parent",
        "setting": "a quiet domestic living room at dusk",
        "scene_1": "sitting at a kitchen table looking at a framed family photograph with tender, worried eyes, as Jesus Christ stands gently beside them with a comforting, loving presence",
        "scene_2": "placing hands gently on the table and bowing head in quiet, heartfelt prayer for their distant child, as Jesus Christ gently places His hand over theirs in divine reassurance",
        "scene_3": "gazing through the window at gentle morning light with serene relief, subtle peaceful smile and renewed hope, as Jesus Christ stands beside them with a warm, comforting smile"
    },
    "zero_balance": {
        "character": "an honest working adult",
        "setting": "a modest kitchen dining table late at night",
        "scene_1": "resting forehead in hand next to household budget papers and a cup of tea, carrying fatigue and concern, as Jesus Christ stands quietly beside them with compassionate eyes and loving divine comfort",
        "scene_2": "pausing, placing hand over chest, eyes closed in deep meditative surrender and quiet prayer for family provision, as Jesus Christ places a comforting hand upon their shoulder and hands",
        "scene_3": "standing upright by the window in morning daylight, holding coffee, looking forward with calm strength and quiet assurance, as Jesus Christ stands beside them in bright warm light with a reassuring smile of divine blessing"
    },
    "medical_fear": {
        "character": "a compassionate adult",
        "setting": "a peaceful, softly lit bedroom chair",
        "scene_1": "holding medical appointment papers with subtle anxiety and contemplative human vulnerability, as Jesus Christ sits gently beside them, gazing with deep empathy and calming presence",
        "scene_2": "hands gently clasped together in reverent silence, eyes closed in earnest faith and emotional peace, as Jesus Christ places a warm, healing hand of grace upon their shoulder",
        "scene_3": "warm morning sunlight washing over their face, a relaxed posture of deep comfort, relief and steadfast trust, as Jesus Christ stands beside them with a gentle smile of divine restoration"
    },
    "night_anxiety": {
        "character": "a weary adult",
        "setting": "a dimly lit bedroom in the quiet hours of the night",
        "scene_1": "sitting on the edge of the bed in soft lamp light, looking pensive as restless thoughts weigh on their mind, as Jesus Christ sits gently next to them with deep calm and loving empathy",
        "scene_2": "taking a slow, deep breath, eyes softly closed in quiet prayer, as Jesus Christ places a gentle, soothing hand upon their back, releasing tension and fear",
        "scene_3": "resting head peacefully on the pillow under comfortable blankets, serene sleep in gentle moonlight, as Jesus Christ watches over them with tranquil protection and peace"
    },
    "lonely_widow": {
        "character": "an elderly woman with kind, weathered eyes",
        "setting": "a warm, cozy living room filled with memories",
        "scene_1": "sitting in an armchair by the window clutching a soft knitted cardigan with bittersweet nostalgic longing, as Jesus Christ stands beside her armchair with tender, eternal companionship",
        "scene_2": "holding a cherished family heirloom with both hands, whispering a heartfelt prayer of tender remembrance, as Jesus Christ places a loving, comforting hand over her shoulder",
        "scene_3": "gentle smile of comforted peace, soft golden afternoon sun filling the room with deep companionship and warmth, as Jesus Christ smiles gently beside her, assuring her she is never alone"
    },
    "elderly_parents": {
        "character": "a devoted adult caregiver with their aging mother or father",
        "setting": "a cozy, sunlit family home",
        "scene_1": "sitting side by side, adult child holding the weathered hand of their elderly parent with deep affection and fatigue, as Jesus Christ stands gently behind them with loving honor and compassion",
        "scene_2": "the caregiver taking a solitary moment in the corridor, eyes closed in silent prayer for patience and gentle strength, as Jesus Christ places a supportive hand on their shoulder",
        "scene_3": "both sharing a tender, authentic smile across the table, honor and mutual love illuminating the quiet moment, as Jesus Christ smiles warmly beside them, sanctifying their family bond"
    },
    "marriage_healing": {
        "character": "a married couple in their 40s",
        "setting": "a quiet domestic living space",
        "scene_1": "sitting on opposite ends of a sofa with unspoken hurt and reflective sorrow in their expressions, as Jesus Christ stands between them with a look of boundless grace and reconciliation",
        "scene_2": "one gently reaching out across the space to hold the other's hand, heads lowered in sincere humility and joint prayer, as Jesus Christ places His hands over theirs, healing wounds",
        "scene_3": "sitting together closely, exchanging a warm, forgiven smile with renewed commitment and tenderness, as Jesus Christ stands beside them in warm afternoon light, uniting their hearts in love"
    },
    "single_parent": {
        "character": "a dedicated single mother or father",
        "setting": "a small home kitchen in the early morning",
        "scene_1": "standing over a quiet kitchen counter preparing the day with honest fatigue and deep devotion to their children, as Jesus Christ stands supportive at their side, watching over their sacrificial love",
        "scene_2": "closing eyes for one still moment of prayer, leaning against the counter for divine strength and peace, as Jesus Christ places a comforting, strengthening hand upon their shoulder",
        "scene_3": "embracing their young child with a radiant, genuine smile of unconditional love and joy in the morning sun, as Jesus Christ smiles beside them, multiplying their provision and peace"
    },
    "sick_grandchild": {
        "character": "a loving grandparent",
        "setting": "a quiet bedside in a softly lit bedroom",
        "scene_1": "watching over a resting child with tender concern and worry, as Jesus Christ stands at the bedside with overflowing mercy and divine tenderness",
        "scene_2": "gently touching the child's hand while whispering a tearful prayer of faith, as Jesus Christ places His healing hand over the child's head and the grandparent's hand",
        "scene_3": "holding the awake child's little hand with an expression of profound relief and thankful warmth in the soft morning light, as Jesus Christ stands beside them with a joyful smile of answered healing"
    },
    "job_breakthrough": {
        "character": "a determined adult",
        "setting": "a modest desk with a laptop and notebook",
        "scene_1": "looking at the screen with quiet disappointment after an unanswered job application, as Jesus Christ stands quietly beside them with encouraging warmth and steadfast presence",
        "scene_2": "stepping back from the desk, hands open in prayer and surrender to divine purpose, as Jesus Christ places a reassuring hand upon their shoulder, promising faithful provision",
        "scene_3": "looking up with a confident, encouraged expression as a fresh morning brings new opportunity and resolve, as Jesus Christ gestures ahead with blessing, preparing the path before them"
    },
    "addiction_chains": {
        "character": "a strong person on the journey of recovery",
        "setting": "a quiet porch or open room at twilight",
        "scene_1": "sitting alone on a step at twilight with intense vulnerability and honest struggle visible in their face, as Jesus Christ stands firmly beside them with unconditional mercy and strength",
        "scene_2": "hands firmly clasped in courageous prayer, breaking through shame with genuine resolve, as Jesus Christ places strong, loving hands upon their shoulders, breaking the heavy weight",
        "scene_3": "standing upright facing the dawn breeze, eyes clear, posture of authentic freedom and dignified peace, as Jesus Christ stands beside them with an outstretched hand of enduring victory and freedom"
    },
    "morning_favor": {
        "character": "a peaceful adult",
        "setting": "a quiet sunlit room in early dawn",
        "scene_1": "sitting by the window with a warm mug and journal before the busy world awakes, serene and reflective, as Jesus Christ stands nearby with a gentle, encouraging gaze in the dawn light",
        "scene_2": "pausing in reverence, looking toward the horizon, dedicating the day's honest steps in prayer, as Jesus Christ extends a loving hand of guidance over their head, bestowing wisdom and favor",
        "scene_3": "stepping out the doorway with purpose, quiet confidence and a warm smile of gratitude, as Jesus Christ walks beside them in radiant morning sunlight, opening doors of blessing"
    },
    "court_legal": {
        "character": "a person carrying the weight of an unresolved legal proceeding",
        "setting": "a quiet office or living room desk",
        "scene_1": "reading legal documents with intense concern and a quiet search for justice and truth, as Jesus Christ stands steadily beside them as their righteous advocate",
        "scene_2": "placing the papers down, bowing head in deep reliance on divine righteousness and protection, as Jesus Christ places a firm, reassuring hand upon their shoulder, imparting divine justice",
        "scene_3": "looking forward with steady peace and dignified resolve, trusting that justice prevails, as Jesus Christ stands beside them, having established righteousness and peace"
    },
    "healing_depression": {
        "character": "a gentle adult fighting a quiet internal battle",
        "setting": "a quiet, cozy corner of a bedroom",
        "scene_1": "wrapped in a warm blanket, eyes carrying honest human weariness and vulnerability, as Jesus Christ kneels gently beside them, looking with tender compassion and no judgment",
        "scene_2": "resting hands gently over their chest, taking an honest breath, finding solace in silent prayer, as Jesus Christ places a warm hand of life and comfort over their heart, breaking the darkness",
        "scene_3": "soft morning sunlight touching their face, gentle emergence of hope and peaceful self-compassion, as Jesus Christ stands beside them smiling with renewing grace"
    },
    "family_protection": {
        "character": "a loving parent",
        "setting": "a warm family home at nightfall",
        "scene_1": "gently closing the front door or checking on sleeping children, mindful of family safety and peace, as Jesus Christ stands watchfully at their side with a protective presence",
        "scene_2": "standing quietly in the hallway, eyes closed in prayer for God's angels to watch over the household, as Jesus Christ places a caring hand upon their shoulder, extending His divine shield of peace",
        "scene_3": "sitting peacefully in the living room, deep sense of shelter and quiet security covering the home, as Jesus Christ blesses the home with outstretched hands of lasting protection and grace"
    },
    "restless_sleep": {
        "character": "an exhausted adult seeking sleep",
        "setting": "a calm bedroom in the quiet late night",
        "scene_1": "tossing restlessly in bed with weary eyes carrying the day's burdens, as Jesus Christ sits gently by the bedside with a tranquil, soothing presence",
        "scene_2": "sitting up slowly, folding hands in quiet prayer of total surrender, as Jesus Christ places a gentle, cooling hand upon their forehead, calming every racing thought",
        "scene_3": "resting peacefully with eyes softly closed in deep, restorative sleep, as Jesus Christ stands watchfully beside the bed under quiet moonbeams, granting divine rest"
    },
    "gratitude_harvest": {
        "character": "a humble, thankful person",
        "setting": "a warm family dining table or garden porch in golden afternoon light",
        "scene_1": "pausing to reflect on past hardships and unexpected blessings with a humble heart, as Jesus Christ stands nearby with a pleased and joyful countenance",
        "scene_2": "clasping hands and looking upward with tears of deep gratitude in prayer, as Jesus Christ smiles warmly, receiving their heartfelt thanksgiving with open arms",
        "scene_3": "sharing bread and joy with loved ones in golden sunlight, as Jesus Christ raises His hands in blessing over their lives, multiplying grace and peace"
    },
    "unspoken_prayer": {
        "character": "a contemplative adult carrying a quiet sorrow",
        "setting": "a quiet window corner in a peaceful domestic room",
        "scene_1": "staring silently into the distance with tears welling in their eyes, unable to put pain into words, as Jesus Christ sits beside them, understanding every unspoken ache",
        "scene_2": "closing eyes and bowing head, allowing the heart to pray in silent faith, as Jesus Christ places both hands warmly over their hands, interceding on their behalf before God",
        "scene_3": "wiping away the tear with a profound sigh of deep inner peace and calm dignity, as Jesus Christ smiles with boundless tenderness, having heard the hidden cry"
    },
    "spiritual_warfare": {
        "character": "a steadfast believer standing firm in faith",
        "setting": "a quiet room at night with an open Bible on the table",
        "scene_1": "standing firm despite feeling heavy spiritual resistance in the atmosphere, as Jesus Christ stands beside them, radiant with holy authority and protective presence",
        "scene_2": "kneeling beside the open Bible, raising hands in bold prayer of faith and authority, as Jesus Christ extends His protective arm, shielding them with divine heavenly light",
        "scene_3": "standing victorious with a serene, unshakeable expression in clear morning light, as Jesus Christ smiles beside them, having vanquished fear and established peace"
    },
    "business_blessing": {
        "character": "an honest worker or small business owner",
        "setting": "a modest workshop or storefront in early dawn",
        "scene_1": "looking over work plans or tools with dedication and honest concern, as Jesus Christ stands approvingly beside them, honoring their honest labor",
        "scene_2": "pausing at the workstation, placing hands upon the tools in prayer dedicating the work to God, as Jesus Christ places a blessing hand over their hands and workspace",
        "scene_3": "opening the doors or meeting people with an honest, inviting smile in bright sunlight, as Jesus Christ stands beside them, pouring favor and honest fruitfulness"
    },
    "forgiving_past": {
        "character": "a person overcoming past hurt",
        "setting": "a tranquil domestic room or quiet garden bench",
        "scene_1": "sitting alone with tense posture, holding a painful memory from years past, as Jesus Christ kneels gently beside them with eyes full of forgiving grace and mercy",
        "scene_2": "opening tight fists and exhaling slowly in prayer, choosing to release resentment into God's hands, as Jesus Christ gently takes their hands, healing the old scar",
        "scene_3": "breathing freely with relaxed shoulders and an unburdened, gentle smile in warm sunlight, as Jesus Christ stands beside them, clothing them in freedom and peace"
    },
    "grief_loss": {
        "character": "a grieving person mourning a loved one",
        "setting": "a softly lit living room chair with an empty chair nearby",
        "scene_1": "looking at an empty seat or cherished keepsake with quiet tears of heartbreak, as Jesus Christ sits gently beside them, comforting them with tears of divine empathy",
        "scene_2": "bowing head with hands over heart, crying out in prayer for strength to endure the grief, as Jesus Christ wraps a warm, loving arm of comfort around their trembling shoulders",
        "scene_3": "looking up toward the gentle window light with soft peace and eternal hope, as Jesus Christ stands beside them, whispering eternal life and heavenly comfort"
    },
    "guidance_direction": {
        "character": "a thoughtful adult standing at a crossroads",
        "setting": "a quiet study or path at dawn with an open journal",
        "scene_1": "looking at multiple options or an open road with contemplative uncertainty, as Jesus Christ stands patiently beside them with gentle, reassuring guidance",
        "scene_2": "closing eyes, placing hand over the journal in earnest prayer for wisdom, as Jesus Christ points gently forward with a hand of divine clarity and counsel",
        "scene_3": "walking forward with firm, confident steps and a peaceful countenance in morning light, as Jesus Christ walks alongside them, lighting each step of the way"
    },
    "strength_weary": {
        "character": "an exhausted worker or caregiver near burnout",
        "setting": "a porch or quiet hallway at the end of a long day",
        "scene_1": "leaning against a wall with heavy fatigue and weary posture, as Jesus Christ steps forward with compassionate love and boundless strength",
        "scene_2": "sliding hands down in humble exhaustion, whispering a prayer for strength, as Jesus Christ places strong, life-giving hands on their shoulders, renewing their spirit",
        "scene_3": "standing upright with refreshed posture, clear eyes, and a deep breath of renewed vitality in the morning breeze, as Jesus Christ smiles with empowering grace"
    },
    "peace_in_storm": {
        "character": "a person facing unexpected crisis",
        "setting": "a room during a sudden downpour against the windowpane",
        "scene_1": "watching rain lash against the window with tense worry in their eyes, as Jesus Christ stands calm and serene beside them in the midst of the storm",
        "scene_2": "turning away from the window, closing eyes and lifting hands in prayer of faith, as Jesus Christ extends a calm, authoritative hand toward the window, speaking stillness",
        "scene_3": "clouds breaking as golden sun rays pierce through the glass, the person smiling with profound stillness, as Jesus Christ stands beside them in perfect peace"
    },
    "divine_grace": {
        "character": "a person seeking God's mercy and forgiveness",
        "setting": "a humble domestic room in soft evening light",
        "scene_1": "looking down at their hands with quiet humility and a sense of unworthiness, as Jesus Christ approaches with eyes radiant with unconditional love and forgiveness",
        "scene_2": "kneeling in prayer, confessing shortcomings with a broken and contrite heart, as Jesus Christ lifts their chin gently with loving grace, washing away all guilt",
        "scene_3": "standing upright in bright morning illumination, filled with dignity, joy, and peace, as Jesus Christ smiles warmly, clothing them in divine righteousness"
    }
}

DEFAULT_BLUEPRINT = {
    "character": "a faithful, thoughtful adult",
    "setting": "a calm, authentic home setting",
    "scene_1": "facing an honest life challenge with contemplative vulnerability, as Jesus Christ stands gently beside them with compassionate eyes and loving divine comfort",
    "scene_2": "closing eyes with clasped hands in earnest personal prayer, as Jesus Christ places a warm, comforting hand of peace upon their shoulder and hands",
    "scene_3": "experiencing a gentle dawn of renewed hope and peaceful joy, as Jesus Christ stands beside them raising a hand of divine blessing in the golden light"
}

# Modificador fotográfico fotorrealista para calidad cinematográfica 35mm
PHOTO_CUES = (
    "cinematic 35mm candid portrait, authentic natural skin texture, Kodak Portra color tones, "
    "shallow depth of field, real human emotions, realistic domestic interior lighting, "
    "highly detailed photorealistic, masterwork, no text, no watermark, no CGI, no 3D cartoon"
)


# Small visual vocabulary per shot. Rotate filming choices to reduce image
# repetition while retaining the selected subject, geography and Christian
# symbols. Prompt variation cannot guarantee provider output consistency.
CAMERA_PLANS = (
    ("eye-level medium shot", "over-the-shoulder close shot", "gentle wide shot"),
    ("intimate face-and-hands close-up", "eye-level medium shot", "quiet doorway composition"),
    ("over-the-shoulder view", "hands-and-Bible close-up", "balanced three-quarter view"),
    ("cinematic wide establishing shot", "close portrait of prayer", "medium shot in natural window light"),
)

ENGAGEMENT_ENDINGS = re.compile(
    r"^(?:share|save|comment|type amen|leave your|drop your|follow|tag a friend|send this|"
    r"what helps|which thought|have you ever|what small|what memory|what does).*",
    re.IGNORECASE,
)

def _split_beats(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", (text or "").strip())
            if len(s.strip()) > 6]

def _faith_subject(theme_key, blueprint, custom_topic):
    # The thematic blueprint supplies a repeatable believable person and room,
    # while a personal topic can shift focus without inventing a miraculous event.
    who = blueprint["character"]
    place = blueprint["setting"]
    override = (custom_topic or "").lower()
    if any(x in override for x in ("hospital", "diagnos", "cancer", "sick", "health", "enfermed", "salud")):
        who, place = "an adult facing a health concern", "an authentic hospital waiting area"
    elif any(x in override for x in ("job", "work", "unemploy", "empleo", "trabajo")):
        who, place = "an adult bearing work uncertainty", "a modest kitchen table with a notebook"
    elif re.search(r"\\b(?:son|daughter|hijo|hija|child|children)\\b", override):
        who, place = "a parent worried about an adult child", "a lived-in family living room"
    elif any(x in override for x in ("debt", "bill", "deuda", "dinero")):
        who, place = "an adult worried about household expenses", "a modest dining table with a closed bill envelope"
    return who, place

def generate_narrative_prompts_for_script(theme_key=None, script_text="",
                                          custom_topic=None, narration_type="prayer",
                                          hook="", body="", cta=""):
    """Images directly illustrate speech beats, NOT the call to action.

    Scene 1: human need and Christian context.
    Scene 2: embodied prayer/Scripture tied to the middle of the message.
    Scene 3: earned emotional step forward, not fabricated material victory.
    """
    blueprint = THEME_NARRATIVE_BLUEPRINTS.get(theme_key, DEFAULT_BLUEPRINT)
    who, place = _faith_subject(theme_key, blueprint, custom_topic)
    segments = _split_beats(script_text)
    if not hook and segments:
        hook = segments[0]
    if not body:
        narration_without_hook = segments[1:] if len(segments) > 1 else segments
        if cta and narration_without_hook and narration_without_hook[-1].strip() == cta.strip():
            narration_without_hook.pop()
        while narration_without_hook and ENGAGEMENT_ENDINGS.match(narration_without_hook[-1]):
            narration_without_hook.pop()
        body = " ".join(narration_without_hook)
    beats = _split_beats(body)
    opening = hook or (beats[0] if beats else "A quiet struggle before prayer.")
    development = beats[0] if beats else opening
    inner = beats[len(beats)//2] if beats else development
    resolution = beats[-1] if beats else development
    kind = narration_type if narration_type in ("prayer", "reflection", "story", "comfort") else "prayer"
    focus = {
        "prayer": "visible honest prayer, a person addressing Jesus with folded hands",
        "reflection": "the person's attention to an open Bible and the meaning of a passage",
        "story": "a believable illustrated everyday moment; not a documentary claim or fabricated testimony",
        "comfort": "compassionate human presence and quiet consolation rather than spectacular miracles",
    }[kind]
    # Maintain Jesus visually as an integral part of the established niche.
    # The same human and Christ are pictured in different compositions.
    first, middle, last = random.choice(CAMERA_PLANS)
    opening_action = blueprint["scene_1"]
    prayer_action = blueprint["scene_2"]
    closing_action = blueprint["scene_3"]
    cautious = {
        "medical_fear": "the same person waiting calmly, no miracle cure or test results shown",
        "sick_grandchild": "the same grandparent comforting the child, no implied cure",
        "job_breakthrough": "the same adult taking one practical step with courage, no guaranteed offer",
        "zero_balance": "the same adult making a humble budget plan, no sudden pile of cash",
        "lost_child": "the same parent finding calm by the window, no invented return or reunion",
        "grief_loss": "the same mourner honoring a memory, no invented reunion",
        "healing_depression": "the same person accepting a moment of support, no instant recovery",
    }
    closing_action = cautious.get(theme_key, closing_action)
    continuity = (
        f"One consistent protagonist: {who}, same age, recognizable face and same clothing "
        f"across all three images, always in {place}. Jesus Christ is depicted "
        "reverently with a consistent appearance, naturally integrated into the scene. "
    )
    constraints = (
        "photorealistic documentary-inspired 35mm cinematic image, vertical 9:16, "
        "credible environment, authentic human expressions, natural light and skin texture; "
        "one dominant clear action, legible subject in center-safe area for Reel captions; "
        "no text, no printed words, no logos, no watermarks, no fantasy graphics, no unrelated objects."
    )
    scene1 = (
        f"SCENE 1 — {first}. {continuity}"
        f"The concrete opening moment: {opening_action}. "
        f"Emotion or action to illustrate from the spoken HOOK: {opening[:210]}. "
        "A modest wooden Christian cross in the room establishes the faith context; "
        f"Jesus Christ is present compassionately without dominating the person. {constraints}"
    )
    scene2 = (
        f"SCENE 2 — {middle}. SAME protagonist and SAME wardrobe as scene 1. {continuity}"
        f"Action: {prayer_action}. Type of storytelling: {focus}. "
        f"Illustrate these spoken DEVELOPMENT beats: {development[:130]} / {inner[:130]}. "
        "Open Holy Bible visible in foreground; Jesus Christ accompanies the prayer. "
        f"Do not invent a separate story or turn the Bible passage into screen lettering. {constraints}"
    )
    scene3 = (
        f"SCENE 3 — {last}. SAME protagonist and SAME wardrobe as scene 1. {continuity}"
        f"An emotionally believable next moment: {closing_action}. "
        f"Illustrate this ENDING idea from the narration: {resolution[:190]}. "
        "A simple cross and Holy Bible remain recognizable; Jesus Christ stands alongside. "
        "Do not depict new money, an instant cure, a reunion, or a miraculous guarantee "
        "unless explicitly present and justified in the narration. Never draw the CTA, "
        f"likes, comments, or social media interface. {constraints}"
    )
    return {
        "prompt": scene1,
        "scene_1_prompt": scene1,
        "scene_2_prompt": scene2,
        "scene_3_prompt": scene3,
        "storyboard_beats": [opening, inner, resolution],
        "scene_1_beat": opening, "scene_2_beat": inner, "scene_3_beat": resolution,
    }
