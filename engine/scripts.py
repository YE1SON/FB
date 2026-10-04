import random
from typing import Dict, List, Optional

# =============================================================================
# COMPACT HIGH-RETENTION SCRIPTS (30-45 words → 7-15 seconds audio)
# Share-oriented CTAs. No engagement bait. Algorithmically safe for Meta 2026.
# =============================================================================

VIRAL_THEMES = {
    "silent_battles": {
        "title": "💔 Batallas Silenciosas y Sanidad Emocional",
        "description": "Para creyentes que enfrentan soledad, dolor oculto o cargas pesadas.",
        "scripture": "Psalm 34:18 — The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
        "hashtags": ["#DailyPrayer", "#ChristianReels", "#HealingPrayer", "#JesusLovesYou"],
        "hook_texts": [
            "YOU ARE NOT ALONE",
            "GOD SEES YOUR TEARS",
            "YOUR PAIN HAS PURPOSE"
        ],
        "hooks": [
            "If you feel like you are fighting alone tonight, hear this truth:",
            "Before you carry that heavy burden into tomorrow, receive this peace:",
            "If your heart felt overwhelmed today, let Jesus speak to you:",
            "When you feel at your breaking point, remember this promise:"
        ],
        "bodies": [
            "Jesus says: I see every tear you hide. This storm is drawing you closer to My heart. I am fighting for you right now.",
            "Jesus says: You are not alone in this battle. I am restoring your peace and lifting the weight from your spirit tonight.",
            "Jesus says: Come to Me with your weariness. My strength is made perfect in your weakness. Rest in My love.",
            "Jesus says: The pain you carry in silence, I already bore on the cross. Let My peace wash over your soul tonight."
        ],
        "ctas": [
            "Share this prayer with someone who needs to hear this tonight.",
            "Send this to a friend going through a silent storm right now.",
            "Share this blessing with someone carrying a heavy burden today."
        ]
    },
    "financial_breakthrough": {
        "title": "💰 Provisión Divina y Puertas Abiertas",
        "description": "Para quienes necesitan fe para el trabajo, deudas o sustento familiar.",
        "scripture": "Philippians 4:19 — And my God will meet all your needs according to the riches of his glory in Christ Jesus.",
        "hashtags": ["#DailyPrayer", "#ChristianReels", "#FinancialBreakthrough", "#GodProvides"],
        "hook_texts": [
            "YOUR SEASON IS SHIFTING",
            "DOORS ARE OPENING",
            "GOD IS YOUR PROVIDER"
        ],
        "hooks": [
            "If financial stress is stealing your peace tonight, hear this promise:",
            "When every door seems closed, remember who holds the keys to heaven:",
            "God sees your faithfulness in the struggle. Your season is about to shift:",
            "Before worry steals your sleep, anchor your soul in this truth:"
        ],
        "bodies": [
            "Jesus says: I own the cattle on a thousand hills. I will open doors no man can shut and release unexpected favor into your home.",
            "Jesus says: You have sowed in tears, and now you will reap in joy. Trust My timing. Divine provision is heading your way.",
            "Jesus says: Seek first My kingdom, and all these things will be added unto you. I will never leave your table empty.",
            "Jesus says: What seems impossible in your finances, I am turning into a miraculous breakthrough for your household."
        ],
        "ctas": [
            "Share this with someone who needs a financial breakthrough today.",
            "Send this prayer of provision to someone who is struggling right now.",
            "Share this with a family that needs to hear God's promise tonight."
        ]
    },
    "bedtime_blessing": {
        "title": "🛌 Paz y Protección Antes de Dormir",
        "description": "Oraciones serenas de descanso para calmar la mente y alejar pesadillas.",
        "scripture": "Psalm 4:8 — In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.",
        "hashtags": ["#BedtimePrayer", "#NightPrayer", "#ChristianReels", "#PeaceOfGod"],
        "hook_texts": [
            "REST IN HIS PEACE",
            "SLEEP IN SAFETY",
            "GOD WATCHES OVER YOU"
        ],
        "hooks": [
            "Before you close your eyes tonight, leave every battle in God's hands:",
            "If your mind is racing with anxious thoughts, breathe in this peace:",
            "God kept you through today. Receive this bedtime blessing over your home:",
            "Before you put your phone down to rest, receive this prayer:"
        ],
        "bodies": [
            "Jesus says: Sleep in peace tonight. My angels guard your home. No darkness will touch your dwelling. You are safe under My wings.",
            "Jesus says: Breathe out the tension of today. You do not have to solve tomorrow tonight. Rest knowing I am in control.",
            "Jesus says: Be still and know that I am God. While you rest, I am working on the answers you need. Tomorrow brings new mercies.",
            "Jesus says: Let go of every worry. My supernatural peace covers your mind, your family, and your home right now."
        ],
        "ctas": [
            "Share this bedtime prayer with someone you love before they sleep.",
            "Send this peaceful blessing to someone who needs rest tonight.",
            "Share this prayer of peace with your family before bed."
        ]
    },
    "family_healing": {
        "title": "👨‍👩‍👧 Protección y Unidad Familiar",
        "description": "Para bendecir a los hijos, sanar matrimonios y proteger el hogar.",
        "scripture": "Joshua 24:15 — But as for me and my household, we will serve the Lord.",
        "hashtags": ["#FamilyPrayer", "#ChristianReels", "#MarriageBlessing", "#FaithInGod"],
        "hook_texts": [
            "YOUR HOME IS BLESSED",
            "GOD HEALS FAMILIES",
            "UNITY IS COMING"
        ],
        "hooks": [
            "If you love your family, let this scripture cover your home today:",
            "God heard every quiet prayer you whispered for your loved ones:",
            "A powerful blessing of protection over your children and family:",
            "Before worry touches your household, speak this truth over your home:"
        ],
        "bodies": [
            "Jesus says: Peace be still in your home. I am placing a hedge of protection around your family. Where there was division, I restore unity.",
            "Jesus says: Trust your children into My hands. My angels guard their steps from every hidden snare tonight.",
            "Jesus says: I am healing the broken bonds in your home. My love washes over your marriage and your children right now.",
            "Jesus says: Your household is under My divine covering. Sickness flees, joy returns, and My peace fills every room."
        ],
        "ctas": [
            "Share this family blessing with someone who needs prayer for their home.",
            "Send this to a parent who is praying for their children tonight.",
            "Share this prayer of protection with a family you love."
        ]
    },
    "divine_protection": {
        "title": "🛡️ Escudo Contra la Ansiedad y el Temor",
        "description": "Autoridad bíblica para derribar el pánico, ataques espirituales y miedo al futuro.",
        "scripture": "Isaiah 41:10 — Fear not, for I am with you; be not dismayed, for I am your God.",
        "hashtags": ["#FaithOverFear", "#OvercomingAnxiety", "#ChristianReels", "#JesusSaves"],
        "hook_texts": [
            "FEAR HAS NO POWER",
            "GOD IS YOUR SHIELD",
            "YOU ARE PROTECTED"
        ],
        "hooks": [
            "When fear whispers that you won't survive this, remember who commands the wind:",
            "If anxiety is overwhelming you right now, take a deep breath and listen:",
            "You are in a spiritual battle, and Jesus is fighting for you:",
            "Before fear steals your peace, anchor yourself in this eternal promise:"
        ],
        "bodies": [
            "Jesus says: Fear is a liar. I defeated the darkness at the cross. The giant before you is nothing compared to the God inside of you.",
            "Jesus says: I have given you power, love, and a sound mind. You will walk through this trial stronger and full of My glory.",
            "Jesus says: No weapon formed against you shall prosper. I am your fortress. Even in the darkest valley, My comfort surrounds you.",
            "Jesus says: Be strong and courageous. I go before you. I will never leave you nor forsake you. Stand firm in My name."
        ],
        "ctas": [
            "Share this with someone fighting anxiety or fear right now.",
            "Send this prayer of strength to someone who needs courage today.",
            "Share this with anyone facing a battle they feel they cannot win."
        ]
    },
    "miracle_healing": {
        "title": "🕊️ Sanidad Milagrosa y Fortaleza Física",
        "description": "Para quienes luchan con diagnósticos médicos, dolor físico o agotamiento.",
        "scripture": "Jeremiah 17:14 — Heal me, Lord, and I will be healed; save me and I will be saved, for you are the one I praise.",
        "hashtags": ["#HealingPrayer", "#Miracles", "#ChristianReels", "#JesusHeals"],
        "hook_texts": [
            "HEALING IS YOURS",
            "GOD HAS THE FINAL WORD",
            "RESTORATION IS COMING"
        ],
        "hooks": [
            "The doctor may have given a hard report, but God always has the final word:",
            "If your body is tired and aching tonight, receive this prayer of strength:",
            "Before sickness steals your hope, remember Jesus carried our pain on the cross:",
            "A sacred prayer of healing and renewed strength over your life right now:"
        ],
        "bodies": [
            "Jesus says: I am the Lord who heals you. I am sending restoration into your body, renewing your strength like the eagles.",
            "Jesus says: Do not lose hope. What medicine cannot fix, My grace is touching right now. Healing flows through your veins.",
            "Jesus says: I see the silent battle you have fought. Rise up in faith. My healing light drives away disease and renews your spirit.",
            "Jesus says: By My stripes you are healed. Receive complete restoration in your body, your mind, and your strength tonight."
        ],
        "ctas": [
            "Share this healing prayer with someone who is fighting sickness today.",
            "Send this to someone who needs a miracle in their body right now.",
            "Share this prayer of restoration with a loved one battling illness."
        ]
    }
}

# =============================================================================
# IMAGE PROMPT GENERATION (kept for fallback image mode)
# =============================================================================

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
        "Jesus Christ embracing a healed person who weeps with intense relief and gratitude, sacred golden aura enveloping both of them, sacred atmosphere of triumph over sickness"
    ],
    "financial_doors": [
        "Majestic Jesus Christ standing before colossal glowing open golden heavenly gates of light, blessing hands extended forward releasing divine favor and abundance, glorious sunbeams illuminating the path ahead",
        "Jesus Christ placing a comforting strong hand on the shoulder of a stressed person sitting at a table with bills, as radiant heavenly light fills the room turning despair into hope",
        "Jesus Christ opening two giant ancient wooden doors carved with holy emblems, revealing a breathtaking sunlit valley of abundance and peace, gesturing warmly for the viewer to walk through"
    ],
    "night_peace": [
        "Serene Jesus Christ watching over a peaceful home under a breathtaking Galilean night sky filled with glowing stars, celestial soft blue and golden aura protecting the dwelling",
        "Jesus Christ standing beside a quiet bedside, placing a gentle hand of peace over a sleeping person's head, whispering divine protection against fear and nightmares",
        "Jesus Christ holding a warm glowing lantern on a quiet cobblestone path at twilight, smiling serenely into the camera, illuminating the darkness with sacred tranquility"
    ],
    "family_children": [
        "Jesus Christ standing inside a warm ancient stone Galilean home, placing his loving hands on a family and young children gathered together in prayer, glowing divine warmth, sacred harmony and protection",
        "Jesus Christ gently blessing a young boy and girl sitting on a wooden bench, smiling with deep fatherly affection, golden sunlight streaming through open archways",
        "Jesus Christ placing his hands of blessing on a husband and wife holding hands in prayer, divine light healing their bond with peace and renewed love"
    ],
    "anxiety_shield": [
        "Jesus Christ standing heroically in front of the viewer with an impenetrable glowing shield of divine golden light, deflecting shadows and dark clouds, authoritative divine protector",
        "Jesus Christ placing both hands gently on the trembling cheeks of an anxious person, looking deeply into their eyes with supernatural tranquility, calming their racing thoughts",
        "Jesus Christ breaking heavy iron chains into glowing dust with his bare hands, freeing a kneeling believer from captivity, radiant divine light banishing all shadows"
    ],
    "gethsemane_prayer": [
        "Jesus Christ kneeling in fervent, emotional prayer against a massive ancient gnarled olive tree in the Garden of Gethsemane under moonlit clouds, tears glistening with divine surrender and holy passion",
        "Jesus Christ looking up to heaven on a quiet rocky hilltop at twilight, arms open in deep devotion, divine rays of twilight celestial light illuminating his holy face"
    ],
    "tears_comfort": [
        "Close-up emotional portrait of Jesus Christ gently wiping a single tear from the cheek of a weeping person, eyes filled with infinite empathy, tenderness, and unconditional love",
        "Jesus Christ wrapping a weeping, heartbroken person in a deep, tight protective embrace, resting his chin on their head, warm golden divine halo",
        "Jesus Christ holding the trembling hands of a weeping soul against his chest, divine golden light warming their sorrow into supernatural peace"
    ],
    "cross_calvary": [
        "Magnificent Holy Cross standing atop Mount Calvary at golden hour sunset, dramatic celestial sunbeams and golden God rays breaking through parting storm clouds, glowing holy aura, white doves flying toward heaven",
        "Jesus Christ standing before the radiant empty tomb at dawn, glorious sunrise breaking over Jerusalem, white robe glowing with resurrection light and triumph"
    ],
    "holy_scriptures": [
        "Jesus Christ sitting peacefully in a warm candlelit ancient stone sanctuary, holding open the Holy Bible scriptures glowing with soft divine golden light, looking up directly toward viewer with loving teaching eyes",
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

    keyword_map = {
        "storm_rescue": ["storm", "water", "drown", "sea", "wave", "sink", "boat", "ocean", "tempest"],
        "miracle_healing": ["heal", "sick", "disease", "pain", "doctor", "body", "cancer", "fever", "stripes", "sanar", "sanidad"],
        "financial_doors": ["financial", "money", "debt", "bills", "lack", "provision", "job", "doors", "breakthrough", "dinero", "deuda"],
        "night_peace": ["sleep", "night", "bed", "dream", "nightmare", "rest", "weary", "dormir", "noche", "descanso"],
        "family_children": ["family", "child", "children", "son", "daughter", "mother", "father", "marriage", "husband", "wife", "home"],
        "anxiety_shield": ["anxiety", "fear", "panic", "enemy", "attack", "chains", "armor", "darkness", "mind", "shield", "ansiedad", "miedo"],
        "gethsemane_prayer": ["gethsemane", "garden", "kneel", "pray", "prayer", "solitary", "alone"],
        "tears_comfort": ["tear", "tears", "cried", "broken", "brokenhearted", "sorrow", "grief", "weeping"],
        "cross_calvary": ["cross", "calvary", "tomb", "resurrection", "sacrifice", "blood"],
        "holy_scriptures": ["bible", "scripture", "word", "verse", "scroll"]
    }

    for cat, words in keyword_map.items():
        for w in words:
            if w in full_text:
                scores[cat] += 2

    best_score = max(scores.values())
    top_categories = [cat for cat, s in scores.items() if s == best_score and s > 0]

    if top_categories:
        chosen_category = random.choice(top_categories)
    elif theme_key:
        mapping = {
            "financial_breakthrough": "financial_doors",
            "bedtime_blessing": "night_peace",
            "family_healing": "family_children",
            "divine_protection": "anxiety_shield",
            "miracle_healing": "miracle_healing",
            "silent_battles": "tears_comfort"
        }
        chosen_category = mapping.get(theme_key, random.choice(list(SCENARIO_POOLS.keys())))
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
    - Line 1: Emotional hook (keyword anchor for Meta's NLP indexing)
    - Line 2: Scripture verse (trust signal)
    - Line 3: Share-oriented CTA (triggers Meaningful Social Interactions via DM shares)
    - Line 4: Exactly 3-4 hyper-targeted CamelCase hashtags
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
    hook_text = random.choice(theme["hook_texts"])

    if custom_topic and custom_topic.strip():
        topic = custom_topic.strip().lower()
        clean_topic = CUSTOM_TOPIC_TRANSLATIONS.get(topic, topic)
        hook = f"If you have been praying silently over {clean_topic}, receive this promise from God:"

    full_text = f"{hook} {body} {cta}"
    image_prompt = generate_image_prompt_for_script(chosen_key, full_text, custom_topic)
    seo_caption = generate_seo_caption(chosen_key, hook, body, cta)

    return {
        "theme": theme["title"],
        "theme_key": chosen_key,
        "hook": hook,
        "body": body,
        "cta": cta,
        "hook_text": hook_text,
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
