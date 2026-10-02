import random
from typing import Dict, List, Optional

VIRAL_THEMES = {
    "silent_battles": {
        "title": "💔 Batallas Silenciosas y Sanidad Emocional",
        "description": "Para creyentes que enfrentan soledad, dolor oculto o cargas pesadas.",
        "scripture": "Psalm 34:18 — The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
        "hashtags": ["#DailyPrayer", "#ChristianReels", "#HealingPrayer", "#JesusLovesYou"],
        "hooks": [
            "The enemy wants you to believe you are fighting this battle alone. Here is the truth:",
            "Before you carry that heavy worry into tomorrow, take 20 seconds to receive this peace.",
            "If your heart felt overwhelmed today, let these words from Jesus comfort your soul:",
            "Whenever you feel at your breaking point, remember what God promises you right now:"
        ],
        "bodies": [
            "Jesus says: I see every burden you carry in silence. The storm you are in right now is not meant to break you, but to draw you closer to My heart. I am restoring your peace, lifting the heaviness from your chest, and fighting for you even when you cannot see it.",
            "Jesus says: My child, you do not have to carry tomorrow's worries tonight. I collected every tear you shed in secret. I am turning your deepest pain into your greatest testimony, and My supernatural peace is surrounding your mind right now.",
            "Jesus says: Come to Me, all you who are weary and burdened, and I will give you rest. Lay down the guilt, the exhaustion, and the fear. You are deeply loved, and My strength is made perfect in your weakness."
        ],
        "ctas": [
            "Drop a heart or leave your prayer request below. Our community is praying over every comment tonight.",
            "Leave your first name below so we can lift you up in prayer. Save this reminder for tomorrow morning.",
            "Who in your life needs this comfort today? Share this blessing to bring God's light into their day."
        ]
    },
    "financial_breakthrough": {
        "title": "💰 Provisión Divina y Puertas Abiertas",
        "description": "Para quienes necesitan fe para el trabajo, deudas o sustento familiar.",
        "scripture": "Philippians 4:19 — And my God will meet all your needs according to the riches of his glory in Christ Jesus.",
        "hashtags": ["#DailyPrayer", "#ChristianReels", "#FinancialBreakthrough", "#GodProvides"],
        "hooks": [
            "If you have been losing sleep worrying about finances or bills, listen to this promise:",
            "When every earthly door seems closed, remember who holds the keys to heaven:",
            "God saw your faithfulness in the struggle, and your season of famine is about to shift:",
            "Before you let financial stress steal your peace, let this scripture anchor your soul:"
        ],
        "bodies": [
            "Jesus says: I own the cattle on a thousand hills. Do not let numbers and deadlines make you forget that I am your Provider. I will open doors no man can shut, and release unexpected favor into your home.",
            "Jesus says: You have sowed in tears, and now you will reap in joy. Trust My timing. What seemed impossible in your bank account, I am turning into a miraculous breakthrough for your household.",
            "Jesus says: Seek first the kingdom of God, and all these things will be added to you. I will never leave your table empty. Keep your eyes on Me, for divine abundance is heading your way."
        ],
        "ctas": [
            "Leave your prayer request for provision below. We are believing together for open doors in your life.",
            "Save this prayer to start your week in faith, and share it with someone who needs financial hope.",
            "Drop a 🙏 below if you trust God as your Provider tonight. We are praying for your family's breakthrough."
        ]
    },
    "bedtime_blessing": {
        "title": "🛌 Paz y Protección Antes de Dormir",
        "description": "Oraciones serenas de descanso para calmar la mente y alejar pesadillas.",
        "scripture": "Psalm 4:8 — In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.",
        "hashtags": ["#BedtimePrayer", "#NightPrayer", "#ChristianReels", "#PeaceOfGod"],
        "hooks": [
            "Before you close your eyes to sleep tonight, leave every battle in God's hands:",
            "If your mind is racing with anxious thoughts tonight, breathe in this sacred peace:",
            "The day is finished, and God kept you awake for this 20-second bedtime blessing:",
            "Before you put your phone down to rest, receive this peaceful prayer over your home:"
        ],
        "bodies": [
            "Jesus says: Sleep in peace. No weapon of darkness will touch your dwelling. My holy angels are stationed around your home, watching over your children and covering your mind with celestial calm.",
            "Jesus says: Breathe out the tension of today. In My presence there is quiet rest. You do not have to solve tomorrow tonight. Close your eyes knowing you are safe under the shadow of My wings.",
            "Jesus says: Be still and know that I am God. While you rest your weary body, I am working on the answers you need. Tomorrow brings new mercies and fresh morning joy."
        ],
        "ctas": [
            "Leave your first name or family name below so we can cover your sleep in prayer tonight.",
            "Save this prayer for every night you need deep peace, and send it to someone you love before they rest.",
            "Drop a 🕊️ below to claim God's restful peace over your home tonight."
        ]
    },
    "family_healing": {
        "title": "👨‍👩‍👧 Protección y Unidad Familiar",
        "description": "Para bendecir a los hijos, sanar matrimonios y proteger el hogar.",
        "scripture": "Joshua 24:15 — But as for me and my household, we will serve the Lord.",
        "hashtags": ["#FamilyPrayer", "#ChristianReels", "#MarriageBlessing", "#FaithInGod"],
        "hooks": [
            "If you love your family and children, let this scripture cover your home today:",
            "God has heard every quiet prayer you whispered for your loved ones. Here is His promise:",
            "Before discord or worry tries to steal your household's joy, speak this truth:",
            "A powerful blessing of protection over your children and family tonight:"
        ],
        "bodies": [
            "Jesus says: Peace be still in your home. I am placing a hedge of holy protection around your family. Where there was division, I will restore unity; where there was rebellion, I will place wisdom and love.",
            "Jesus says: Trust your children into My hands. My angels are guarding their footsteps from every hidden snare. Sickness will flee, and My divine joy will fill every room of your house.",
            "Jesus says: I am healing the broken communication in your home. Let My love wash over your marriage and your children. Your household will stand as a shining light of My grace."
        ],
        "ctas": [
            "Write the name of a family member below so we can lift them up in prayer tonight.",
            "Save this blessing for your family altar, and share it to protect another home today.",
            "Drop a ❤️ in the comments to claim divine peace over your children and marriage."
        ]
    },
    "divine_protection": {
        "title": "🛡️ Escudo Contra la Ansiedad y el Temor",
        "description": "Autoridad bíblica para derribar el pánico, ataques espirituales y miedo al futuro.",
        "scripture": "Isaiah 41:10 — Fear not, for I am with you; be not dismayed, for I am your God.",
        "hashtags": ["#FaithOverFear", "#OvercomingAnxiety", "#ChristianReels", "#JesusSaves"],
        "hooks": [
            "When fear whispers that you won't survive this storm, remember who commands the wind:",
            "If anxiety is trying to overwhelm your chest right now, take a deep breath and listen:",
            "You are not losing your mind; you are in a spiritual battle, and Jesus is fighting for you:",
            "Before you let fear dictate your decisions, anchor your thoughts in this eternal promise:"
        ],
        "bodies": [
            "Jesus says: Fear is a liar, and anxiety has no power over you. I have already defeated the darkness at the cross. The giant in front of you is nothing compared to the God inside of you. Stand firm.",
            "Jesus says: Peace I leave with you; My supernatural peace I give to you. I have given you power, love, and a sound mind. You will walk out of this trial stronger and full of My glory.",
            "Jesus says: No weapon formed against you will prosper. I am your fortress and your deliverer. Even when you walk through the darkest valley, My rod and staff will comfort you."
        ],
        "ctas": [
            "Leave a prayer request below if you need prayer against anxiety tonight. You are not alone.",
            "Save this verse on your phone for whenever panic tries to return. God is with you.",
            "Drop a 🛡️ in the comments to declare that fear has no authority over your life today."
        ]
    },
    "miracle_healing": {
        "title": "🕊️ Sanidad Milagrosa y Fortaleza Física",
        "description": "Para quienes luchan con diagnósticos médicos, dolor físico o agotamiento.",
        "scripture": "Jeremiah 17:14 — Heal me, Lord, and I will be healed; save me and I will be saved, for you are the one I praise.",
        "hashtags": ["#HealingPrayer", "#Miracles", "#ChristianReels", "#JesusHeals"],
        "hooks": [
            "The doctor may have given a difficult report, but God always has the final word:",
            "If your physical body is tired and aching tonight, receive this prayer of divine strength:",
            "Before sickness steals your hope, remember that Jesus carried our infirmities on the cross:",
            "A sacred prayer for physical healing and renewed strength over your life right now:"
        ],
        "bodies": [
            "Jesus says: I am the Lord who heals you. I am sending divine restoration into your cells, renewing your energy like the eagles, and washing away pain from the crown of your head to your feet.",
            "Jesus says: Do not lose hope. What medical science could not fix, My holy grace is touching right now. Let My supernatural warmth flow through your body, restoring health and vitality.",
            "Jesus says: I see the silent physical battle you have fought. Rise up in faith. My healing light is driving away disease and breathing new life into your spirit."
        ],
        "ctas": [
            "Leave the first name of someone who needs physical healing below. Our community is praying for them.",
            "Save this prayer to listen to each morning for strength, and share it with someone who is sick today.",
            "Drop a 🙏 below in faith for complete healing and restoration over your body."
        ]
    }
}

# Banco de escenas para el generador de imágenes (sin cambios drásticos, ya funciona de maravilla)
SCENARIO_POOLS = {
    "storm_rescue": [
        "Dramatic first-person POV looking up as Jesus Christ stands on turbulent stormy sea waves, reaching his strong compassionate hand directly toward the viewer to pull them from dark crashing waves, radiant sunbeams piercing through storm clouds",
        "Jesus Christ standing at the bow of an ancient wooden fishing boat on the Sea of Galilee, holding up his right hand commanding the raging tempest to be still, clouds breaking to reveal brilliant golden heavenly light",
        "Jesus Christ pulling a trembling believer up out of roaring ocean waters into safety, compassionate urgent gaze, clothes wet from sea spray, dramatic golden divine rim lighting",
        "Jesus Christ walking serenely across churning ocean waves in the middle of a thunderstorm, illuminated by a celestial golden aura, smiling calmly with outstretched hand of rescue"
    ],
    "miracle_healing": [
        "Jesus Christ gently placing his glowing sacred hands on the forehead of a suffering sick person lying in bed, holy radiant amber light emanating from his touch, peaceful expression of miraculous recovery",
        "Jesus Christ kneeling beside a disabled, broken person on a sunlit ancient stone path, taking their hands and lifting them up to walk, radiant sunbeams, emotional onlookers weeping in reverence",
        "First-person POV looking up from a hospital bed or sickbed as Jesus Christ leans down with infinite warmth and love, placing his healing hand over the viewer's heart with pulsating divine golden light",
        "Jesus Christ embracing a healed person who weeps with intense relief and gratitude, sacred golden aura enveloping both of them, sacred atmosphere of triumph over sickness",
        "Jesus Christ praying fervently with hands lifted over a person seeking healing, glorious rays of divine restoration descending from heaven onto their body"
    ],
    "financial_doors": [
        "Majestic Jesus Christ standing before colossal glowing open golden heavenly gates of light, blessing hands extended forward releasing divine favor and abundance, glorious sunbeams illuminating the path ahead",
        "Jesus Christ placing a comforting strong hand on the shoulder of a stressed person sitting at a table with bills, as radiant heavenly light fills the room turning despair into hope",
        "Jesus Christ pouring liquid golden divine light from his glowing palms into the open praying hands of a faithful believer, sacred atmosphere of supernatural provision and open doors",
        "Jesus Christ opening two giant ancient wooden doors carved with holy emblems, revealing a breathtaking sunlit valley of abundance and peace, gesturing warmly for the viewer to walk through",
        "Jesus Christ standing in a golden wheat field at harvest time under a radiant sunrise, smiling with hands outstretched in blessing of prosperity and fruitfulness"
    ],
    "night_peace": [
        "Serene Jesus Christ watching over a peaceful home under a breathtaking Galilean night sky filled with glowing stars, celestial soft blue and golden aura protecting the dwelling",
        "Jesus Christ standing beside a quiet bedside, placing a gentle hand of peace over a sleeping person's head, whispering divine protection against fear and nightmares",
        "Jesus Christ holding a warm glowing lantern on a quiet cobblestone path at twilight, smiling serenely into the camera, illuminating the darkness with sacred tranquility",
        "Jesus Christ sitting in a quiet candlelit room beside a resting person, holding their hand in silent comfort as golden candlelight dances on the stone walls"
    ],
    "family_children": [
        "Jesus Christ standing inside a warm ancient stone Galilean home, placing his loving hands on a family and young children gathered together in prayer, glowing divine warmth, sacred harmony and protection",
        "Jesus Christ gently blessing a young boy and girl sitting on a wooden bench, smiling with deep fatherly affection, golden sunlight streaming through open archways",
        "Jesus Christ placing his hands of blessing on a husband and wife holding hands in prayer, divine light healing their bond with peace and renewed love",
        "Jesus Christ kneeling to wrap a distressed teenager or child in a loving protective embrace, assuring them that they are cherished and never abandoned"
    ],
    "anxiety_shield": [
        "Jesus Christ standing heroically in front of the viewer with an impenetrable glowing shield of divine golden light, deflecting shadows and dark clouds, authoritative divine protector",
        "Jesus Christ placing both hands gently on the trembling cheeks of an anxious person, looking deeply into their eyes with supernatural tranquility, calming their racing thoughts",
        "Jesus Christ breaking heavy iron chains into glowing dust with his bare hands, freeing a kneeling believer from captivity, radiant divine light banishing all shadows",
        "Jesus Christ walking fearlessly through a shadowy dark valley, a radiant pillar of holy golden light surrounding him, signaling total victory over spiritual fear"
    ],
    "gethsemane_prayer": [
        "Jesus Christ kneeling in fervent, emotional prayer against a massive ancient gnarled olive tree in the Garden of Gethsemane under moonlit clouds, tears glistening with divine surrender and holy passion",
        "Jesus Christ looking up to heaven on a quiet rocky hilltop at twilight, arms open in deep devotion, divine rays of twilight celestial light illuminating his holy face",
        "Jesus Christ sitting alone in deep contemplative prayer on the Mount of Olives at dawn, morning mist rising with the first rays of golden sunlight touching his white robe"
    ],
    "tears_comfort": [
        "Close-up emotional portrait of Jesus Christ gently wiping a single tear from the cheek of a weeping person, eyes filled with infinite empathy, tenderness, and unconditional love",
        "Jesus Christ sitting on the floor beside a brokenhearted person in a quiet dimly lit room, wrapping an arm around their shoulders in comforting solidarity",
        "Jesus Christ wrapping a weeping, heartbroken person in a deep, tight protective embrace, resting his chin on their head, warm golden divine halo",
        "Jesus Christ holding the trembling hands of a weeping soul against his chest, divine golden light warming their sorrow into supernatural peace"
    ],
    "cross_calvary": [
        "Magnificent Holy Cross standing atop Mount Calvary at golden hour sunset, dramatic celestial sunbeams and golden God rays breaking through parting storm clouds, glowing holy aura, white doves flying toward heaven",
        "Jesus Christ standing before the radiant empty tomb at dawn, glorious sunrise breaking over Jerusalem, white robe glowing with resurrection light and triumph",
        "Jesus Christ looking toward Mount Calvary with solemn reverence, golden morning light illuminating his profile, symbol of eternal sacrifice and love"
    ],
    "holy_scriptures": [
        "Jesus Christ sitting peacefully in a warm candlelit ancient stone sanctuary, holding open the Holy Bible scriptures glowing with soft divine golden light, looking up directly toward viewer with loving teaching eyes",
        "Jesus Christ holding an ancient sacred glowing scroll in a stone temple courtyard, sunlight catching dust motes in sacred silence, wisdom and authority in his gentle gaze",
        "Jesus Christ opening the scriptures with golden light emanating from the sacred text, illuminating the faces of eager listeners gathered at his feet"
    ]
}

CUSTOM_TOPIC_TRANSLATIONS = {
    "hijo": "a beloved sick or struggling son/child",
    "hija": "a beloved sick or struggling daughter/child",
    "hijos": "beloved children and youth",
    "mama": "a loving mother in need of peace",
    "mamá": "a loving mother in need of peace",
    "papa": "a hardworking father seeking strength",
    "papá": "a hardworking father seeking strength",
    "padres": "parents praying for their household",
    "esposo": "a husband praying for guidance and peace",
    "esposa": "a wife praying for strength and comfort",
    "matrimonio": "a marriage relationship in need of reconciliation and healing",
    "deudas": "financial debt, unpaid bills, and lack",
    "deuda": "financial debt, unpaid bills, and lack",
    "dinero": "financial provision and open doors",
    "trabajo": "employment, career breakthrough, and provision",
    "empleo": "employment, career breakthrough, and provision",
    "negocio": "a family business and financial breakthrough",
    "salud": "physical health, bodily recovery, and strength",
    "enfermedad": "sickness, bodily infirmity, and physical pain",
    "cancer": "cancer diagnosis and miraculous cellular healing",
    "cáncer": "cancer diagnosis and miraculous cellular healing",
    "ansiedad": "overwhelming anxiety, panic attacks, and racing thoughts",
    "depresion": "depression, heavy mental darkness, and sadness",
    "depresión": "depression, heavy mental darkness, and sadness",
    "soledad": "loneliness, feeling abandoned, and heartbreak",
    "miedo": "fear, terror, and sleepless nights",
    "duelo": "grief, mourning, and loss of a loved one",
    "perdon": "forgiveness, release of bitterness, and peace",
    "perdón": "forgiveness, release of bitterness, and peace"
}

CAMERA_ANGLES = [
    "cinematic 8k vertical 9:16 portrait",
    "hyper-realistic biblical masterpiece, 9:16 vertical ratio",
    "emotional close-up portrait with cinematic depth of field, 9:16 vertical",
    "dramatic eye-level vertical shot, photorealistic 8k",
    "intimate vertical composition with shallow focus, 8k resolution"
]

LIGHTING_MOODS = [
    "warm divine golden hour illumination with soft God rays",
    "sacred ethereal sunbeams piercing through clouds with luminous particles",
    "dramatic cinematic volumetric lighting with warm amber rim light",
    "soft candlelight glow and radiant heavenly halo",
    "celestial twilight glow with brilliant warm highlights"
]

ARTISTIC_DETAILS = [
    "deeply expressive compassionate eyes looking directly at viewer, classic flowing brown hair and gentle beard, authentic white tunic and crimson sash, sacred realism",
    "gentle reassuring smile, detailed facial texture, solemn yet deeply comforting presence, cinematic holy atmosphere",
    "masterpiece quality, photorealistic skin and fabric textures, sacred reverence, intense emotional resonance"
]

def generate_image_prompt_for_script(theme_key: Optional[str] = None, script_text: str = "", custom_topic: Optional[str] = None) -> str:
    full_text = f"{script_text} {custom_topic or ''}".lower()
    scores = {cat: 0 for cat in SCENARIO_POOLS.keys()}
    
    if theme_key == "financial_breakthrough":
        scores["financial_doors"] += 4
    elif theme_key == "bedtime_blessing":
        scores["night_peace"] += 4
    elif theme_key == "family_healing":
        scores["family_children"] += 4
    elif theme_key == "divine_protection":
        scores["anxiety_shield"] += 4
    elif theme_key == "miracle_healing":
        scores["miracle_healing"] += 4
    elif theme_key == "silent_battles":
        scores["tears_comfort"] += 3

    for w in ["storm", "water", "drown", "sea", "wave", "sink", "boat", "ocean", "tempest", "tormenta", "olas", "mar"]:
        if w in full_text:
            scores["storm_rescue"] += 2

    for w in ["heal", "sick", "disease", "pain", "doctor", "medicine", "body", "cells", "infirmity", "cancer", "fever", "stripes", "sanar", "sanidad", "enfermedad", "dolor", "salud"]:
        if w in full_text:
            scores["miracle_healing"] += 2

    for w in ["financial", "money", "debt", "bills", "lack", "famine", "provision", "job", "doors", "bank", "breakthrough", "dinero", "deuda", "deudas", "finanzas", "trabajo", "puertas", "cuentas"]:
        if w in full_text:
            scores["financial_doors"] += 2

    for w in ["sleep", "night", "bed", "dream", "nightmare", "rest", "weary", "awake", "evening", "dormir", "noche", "cama", "sueño", "descanso"]:
        if w in full_text:
            scores["night_peace"] += 2

    for w in ["family", "child", "children", "son", "daughter", "mother", "father", "marriage", "husband", "wife", "home", "household", "familia", "hijo", "hijos", "hija", "madre", "padre", "matrimonio", "hogar", "casa"]:
        if w in full_text:
            scores["family_children"] += 2

    for w in ["anxiety", "fear", "panic", "enemy", "attack", "chains", "armor", "giant", "darkness", "mind", "shield", "protect", "ansiedad", "miedo", "temor", "pánico", "enemigo", "mente", "escudo"]:
        if w in full_text:
            scores["anxiety_shield"] += 2

    for w in ["gethsemane", "garden", "kneel", "pray", "prayer", "solitary", "alone", "getsemaní", "oración", "orar"]:
        if w in full_text:
            scores["gethsemane_prayer"] += 2

    for w in ["tear", "tears", "cried", "wept", "broken", "brokenhearted", "sorrow", "grief", "weeping", "lágrima", "lágrimas", "llorar", "quebrantado", "tristeza"]:
        if w in full_text:
            scores["tears_comfort"] += 2

    for w in ["cross", "calvary", "tomb", "resurrection", "sacrifice", "blood", "cruz", "calvario", "tumba", "resurrección"]:
        if w in full_text:
            scores["cross_calvary"] += 2

    for w in ["bible", "scripture", "scriptures", "word", "verse", "scroll", "biblia", "palabra", "escritura"]:
        if w in full_text:
            scores["holy_scriptures"] += 2

    best_score = max(scores.values())
    top_categories = [cat for cat, s in scores.items() if s == best_score and s > 0]
    
    if top_categories:
        chosen_category = random.choice(top_categories)
    elif theme_key and theme_key in ["financial_breakthrough", "bedtime_blessing", "family_healing", "divine_protection", "miracle_healing", "silent_battles"]:
        mapping = {
            "financial_breakthrough": "financial_doors",
            "bedtime_blessing": "night_peace",
            "family_healing": "family_children",
            "divine_protection": "anxiety_shield",
            "miracle_healing": "miracle_healing",
            "silent_battles": "tears_comfort"
        }
        chosen_category = mapping[theme_key]
    else:
        chosen_category = random.choice(list(SCENARIO_POOLS.keys()))

    base_scene = random.choice(SCENARIO_POOLS[chosen_category])

    topic_addon = ""
    if custom_topic and custom_topic.strip():
        ct_clean = custom_topic.strip().lower()
        matched_translation = None
        for k, v in CUSTOM_TOPIC_TRANSLATIONS.items():
            if k in ct_clean:
                matched_translation = v
                break
        if not matched_translation:
            matched_translation = custom_topic.strip()
        topic_addon = f", especially centered on bringing miraculous intervention and peace for {matched_translation}"

    angle = random.choice(CAMERA_ANGLES)
    lighting = random.choice(LIGHTING_MOODS)
    details = random.choice(ARTISTIC_DETAILS)

    return f"{base_scene}{topic_addon}, {lighting}, {details}, {angle}"

def generate_seo_caption(theme_key: str, hook: str, body: str, cta: str) -> str:
    """
    Generates a high-converting, Facebook SEO-compliant caption for 2026:
    - Line 1: Keyword-rich hook anchor
    - Line 2: The scripture verse
    - Line 3: Authentic prayer wall CTA (Meaningful Social Interaction)
    - Line 4: Exactly 3 to 4 hyper-targeted CamelCase hashtags (Zero spam)
    """
    theme = VIRAL_THEMES.get(theme_key, VIRAL_THEMES["silent_battles"])
    scripture = theme.get("scripture", "Psalm 34:18 — The Lord is close to the brokenhearted.")
    hashtags = " ".join(theme.get("hashtags", ["#DailyPrayer", "#ChristianReels", "#FaithInGod"]))
    
    caption = (
        f"{hook} 🙏✨\n\n"
        f"📖 Scripture: {scripture}\n\n"
        f"{cta}\n\n"
        f"{hashtags}"
    )
    return caption

def generate_script(theme_key: Optional[str] = None, custom_topic: Optional[str] = None) -> Dict[str, str]:
    if theme_key and theme_key in VIRAL_THEMES:
        chosen_key = theme_key
    else:
        chosen_key = random.choice(list(VIRAL_THEMES.keys()))
        
    theme = VIRAL_THEMES[chosen_key]

    hook = random.choice(theme["hooks"])
    body = random.choice(theme["bodies"])
    cta = random.choice(theme["ctas"])

    if custom_topic and custom_topic.strip():
        topic = custom_topic.strip().lower()
        # Translate or clean up topic
        clean_topic = CUSTOM_TOPIC_TRANSLATIONS.get(topic, topic)
        hook = f"If you have been praying silently over {clean_topic}, receive this promise from God tonight:"

    full_text = f"{hook} {body} {cta}"
    image_prompt = generate_image_prompt_for_script(chosen_key, full_text, custom_topic)
    seo_caption = generate_seo_caption(chosen_key, hook, body, cta)

    return {
        "theme": theme["title"],
        "theme_key": chosen_key,
        "hook": hook,
        "body": body,
        "cta": cta,
        "full_text": full_text,
        "image_prompt": image_prompt,
        "seo_caption": seo_caption,
        "scripture": theme["scripture"]
    }

def get_themes_list():
    return [
        {"key": k, "title": v["title"], "description": v["description"]}
        for k, v in VIRAL_THEMES.items()
    ]
