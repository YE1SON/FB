import random
from typing import Dict, List, Optional

# =============================================================================
# HYPER-SPECIFIC PAIN POINT THEMES (Meta 2026 Optimized)
# =============================================================================

VIRAL_THEMES = {
    "zero_balance": {
        "title": "💸 Milagro Financiero (Facturas / $0 en el banco)",
        "description": "Pánico financiero inmediato y necesidad de un milagro de provisión urgente.",
        "scripture": "Philippians 4:19 — And my God will supply every need of yours according to his riches in glory.",
        "hashtags": ["#FinancialMiracle", "#TrustGod", "#GodProvides", "#FaithOverFear"],
        "hook_texts": [
            "WHEN YOUR BANK IS AT $0",
            "GOD SEES YOUR BILLS",
            "A MIRACLE IS COMING"
        ],
        "hooks": [
            "If you are staring at an empty bank account and overdue bills today, hear this:",
            "When the math doesn't make sense and you feel drowning in debt, listen:",
            "If financial panic is gripping your chest right now, God wants you to hear this:"
        ],
        "bodies": [
            "Jesus says: Do not panic. I own the cattle on a thousand hills. I am opening a door of provision that no man can shut. Money is coming.",
            "Jesus says: I see the silent tears over those bills. Your breakthrough is closer than you think. I will make a way in the wilderness of your finances.",
            "Jesus says: Hand the heavy burden of debt over to Me. I am moving people and resources in your favor today. Expect an unexpected blessing."
        ],
        "ctas": [
            "Send this prayer to someone who needs a financial miracle today.",
            "Share this message to claim your financial breakthrough this week."
        ]
    },
    "lost_child": {
        "title": "🚶‍♂️ Por el hijo/hija que se alejó de Dios",
        "description": "Dolor de un padre/madre por un hijo en rebeldía, adicción o lejos de la fe.",
        "scripture": "Luke 15:20 — But while he was still a long way off, his father saw him and was filled with compassion.",
        "hashtags": ["#PrayingMom", "#ProdigalSon", "#FamilyRestoration", "#JesusSaves"],
        "hook_texts": [
            "FOR YOUR WANDERING CHILD",
            "GOD IS CHASING THEM",
            "THEY WILL COME HOME"
        ],
        "hooks": [
            "If your heart is breaking for a child who has walked away from God, hear this promise:",
            "To the mother or father crying themselves to sleep over their prodigal child:",
            "If you feel like you failed as a parent because of the path your child chose, listen:"
        ],
        "bodies": [
            "Jesus says: I have not forgotten your child. My spirit is pursuing them even in the darkest places. I will bring them back home.",
            "Jesus says: Your prayers are not empty words; they are building a wall of protection around them. I will encounter them soon.",
            "Jesus says: Release the guilt. I love them more than you do. I am breaking chains of addiction and rebellion over their life right now."
        ],
        "ctas": [
            "Share this prayer with another parent fighting for their child's soul.",
            "Send this to a mother or father who needs hope today."
        ]
    },
    "night_anxiety": {
        "title": "🌌 Cuando la ansiedad no te deja dormir (3 AM)",
        "description": "Paz de emergencia para mentes aceleradas, ataques de pánico y miedo nocturno.",
        "scripture": "Psalm 4:8 — In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.",
        "hashtags": ["#AnxietyRelief", "#NightPrayer", "#PeaceOfMind", "#ChristianReels"],
        "hook_texts": [
            "TO THE RACING MIND AT 3AM",
            "BREATHE IN GOD'S PEACE",
            "ANXIETY HAS NO POWER"
        ],
        "hooks": [
            "If it's late at night, your mind is racing, and anxiety won't let you sleep, hear this:",
            "If you feel a heavy weight on your chest and fear about tomorrow is overwhelming you:",
            "Before another panic attack steals your peace tonight, take a breath and listen:"
        ],
        "bodies": [
            "Jesus says: Breathe. You do not have to figure out tomorrow tonight. I am fighting the battles you cannot see. Close your eyes and rest in My peace.",
            "Jesus says: I command the storm in your mind to be still. I am placing a hedge of protection around your thoughts right now. You are safe.",
            "Jesus says: The spirit of heavy anxiety is broken. My perfect love casts out all fear. I am holding you tight until the morning comes."
        ],
        "ctas": [
            "Send this to someone who struggles with anxiety at night.",
            "Share this prayer to cover a loved one's mind with peace tonight."
        ]
    },
    "medical_fear": {
        "title": "🩺 Un diagnóstico médico que aterroriza",
        "description": "Sanidad desesperada frente a enfermedades graves, cáncer o dolor crónico.",
        "scripture": "Jeremiah 17:14 — Heal me, Lord, and I will be healed; save me and I will be saved.",
        "hashtags": ["#HealingMiracle", "#GodIsTheHealer", "#JesusHeals", "#FaithJourney"],
        "hook_texts": [
            "GOD HAS THE FINAL WORD",
            "HEALING IS IN YOUR BLOOD",
            "THE DOCTOR IS NOT THE CREATOR"
        ],
        "hooks": [
            "If you or someone you love just received a terrifying medical diagnosis, hear this:",
            "When the doctor's report steals the breath from your lungs, remember who gives you breath:",
            "If you are exhausted from chronic pain and hospital visits, Jesus has a word for you:"
        ],
        "bodies": [
            "Jesus says: I am the Great Physician. Human science has limits, but My healing power has none. I am sending divine restoration into your cells.",
            "Jesus says: Do not accept the timeline of fear. I have the final word over your body. By My stripes, supernatural healing is flowing through you right now.",
            "Jesus says: I see your silent tears of pain. I am stepping into that hospital room with you. Stand firm in faith; a miracle testimony is coming."
        ],
        "ctas": [
            "Share this prayer of healing with someone fighting sickness right now.",
            "Send this to a family believing for a medical miracle."
        ]
    },
    "betrayal": {
        "title": "💔 Traición de alguien en quien confiabas",
        "description": "Corazón roto, perdón difícil y justicia divina ante la deslealtad humana.",
        "scripture": "Psalm 147:3 — He heals the brokenhearted and binds up their wounds.",
        "hashtags": ["#BrokenHeart", "#GodIsMyDefender", "#HealingJourney", "#ChristianReels"],
        "hook_texts": [
            "GOD SAW THE BETRAYAL",
            "HE WILL VINDICATE YOU",
            "YOUR HEART WILL HEAL"
        ],
        "hooks": [
            "If your heart was completely shattered by someone you trusted deeply, hear this:",
            "When the person you stood by in their darkest hour walks away in yours, listen:",
            "If you are struggling to forgive someone who isn't even sorry, God wants you to know this:"
        ],
        "bodies": [
            "Jesus says: I know the pain of a Judas kiss. Hand Me your broken heart. I will be your defender and restore double for your shame.",
            "Jesus says: Let go of the anger; it is poison. Let Me fight this battle. I am removing the wrong people to bring you into a season of true blessing.",
            "Jesus says: They walked away, but I will never leave you. I am healing the wounds they left behind. Your best days are ahead, not behind you."
        ],
        "ctas": [
            "Share this with someone who is recovering from a broken heart.",
            "Send this prayer to a friend who needs to know God is their defender."
        ]
    },
    "morning_favor": {
        "title": "🌅 Bendición y Favor de la Mañana",
        "description": "Ideal para empezar el día. Oración de puertas abiertas, protección y favor.",
        "scripture": "Lamentations 3:22-23 — His compassions never fail. They are new every morning.",
        "hashtags": ["#MorningPrayer", "#BlessedDay", "#FavorOfGod", "#ChristianReels"],
        "hook_texts": [
            "BEFORE YOU START YOUR DAY",
            "TODAY IS BLESSED",
            "DOORS ARE OPENING"
        ],
        "hooks": [
            "If you are seeing this before you start your day, do not scroll past this blessing:",
            "Before you step out of your house today, let me pray this powerful blessing over your life:",
            "God woke you up this morning for a reason. Receive this word for your day:"
        ],
        "bodies": [
            "Jesus says: I go before you today. I am making the crooked paths straight and opening doors of favor that will surprise you. Step out in faith.",
            "Jesus says: No weapon formed against your day will prosper. I am commanding My angels to guard your steps, your family, and your work today.",
            "Jesus says: Leave yesterday's mistakes behind. Today is a blank canvas of My mercy. I am breathing new strength and divine appointments into your schedule."
        ],
        "ctas": [
            "Share this morning blessing with someone you want to see succeed today.",
            "Send this prayer to a loved one to cover their day with God's favor."
        ]
    }
}

# =============================================================================
# CINEMATIC AI IMAGE GENERATION PROMPTS (Non-flat, Hyperrealistic)
# =============================================================================

SCENARIO_POOLS = {
    "storm_rescue": [
        "Dynamic low-angle shot, Jesus Christ standing on turbulent roaring ocean waves, reaching hand out to viewer, massive dark storm clouds parting to reveal blinding divine golden God-rays, splashing water, dramatic lighting, epic cinematic composition"
    ],
    "miracle_healing": [
        "Intimate emotional close-up, Jesus Christ with glowing hands gently touching the forehead of a person in a hospital bed, dramatic chiaroscuro lighting, warm amber light cutting through cold shadows, tears of relief, photorealistic masterpiece"
    ],
    "financial_doors": [
        "Epic wide shot, Jesus Christ opening colossal ancient wooden doors glowing with blinding supernatural golden light, stepping from darkness into a valley of abundance, dust motes floating in the air, highly detailed, octane render"
    ],
    "night_peace": [
        "Cinematic moody lighting, Jesus Christ standing over a quiet bed in a dark room, moonlight streaming through a window, soft glowing divine aura protecting the room, hyper-detailed, peaceful atmosphere"
    ],
    "family_children": [
        "Warm glowing cinematic lighting, Jesus Christ embracing a broken family, divine golden light healing their bond, dust particles floating in the warm sunbeams, ultra-realistic emotional portrait, masterpiece"
    ],
    "anxiety_shield": [
        "Heroic epic composition, Jesus Christ standing in front of the viewer holding up his hands, deflecting dark shadows and smoke with a brilliant blinding shield of pure white and gold light, intense dynamic angle, 8k"
    ],
    "tears_comfort": [
        "Ultra-realistic extreme close-up, Jesus Christ gently wiping a tear from a weeping person's cheek, deep compassionate eyes looking directly into the camera, cinematic depth of field, warm candlelight glow, deeply emotional"
    ]
}

CUSTOM_TOPIC_TRANSLATIONS = {
    "hijo": "a beloved child", "deuda": "heavy financial debt", "salud": "physical sickness",
    "ansiedad": "overwhelming panic and anxiety", "soledad": "deep loneliness"
}

CAMERA_ANGLES = [
    "hyper-realistic Unreal Engine 5 render, octane render, 8k resolution",
    "cinematic masterpiece, dramatic volumetric lighting, highly detailed, depth of field",
    "photorealistic emotional photography, dramatic chiaroscuro lighting, cinematic color grading"
]

def generate_image_prompt_for_script(theme_key: Optional[str] = None, script_text: str = "", custom_topic: Optional[str] = None) -> str:
    mapping = {
        "zero_balance": "financial_doors",
        "lost_child": "family_children",
        "night_anxiety": "night_peace",
        "medical_fear": "miracle_healing",
        "betrayal": "tears_comfort",
        "morning_favor": "financial_doors"
    }
    chosen_category = mapping.get(theme_key, random.choice(list(SCENARIO_POOLS.keys())))
    base_scene = random.choice(SCENARIO_POOLS[chosen_category])
    
    # We enforce the aspect ratio tag directly in the prompt generation inside app.js or let Puter figure it out, 
    # but we can add a strong instruction here just in case.
    return f"{base_scene}, {random.choice(CAMERA_ANGLES)}, dynamic and intense, hyper-detailed, NOT flat, masterpiece"


def generate_seo_caption(theme_key: str, hook: str, body: str, cta: str) -> str:
    theme = VIRAL_THEMES.get(theme_key, VIRAL_THEMES["morning_favor"])
    scripture = theme.get("scripture", "Psalm 34:18 — The Lord is close to the brokenhearted.")
    hashtags = " ".join(theme.get("hashtags", ["#DailyPrayer", "#ChristianReels", "#FaithInGod"]))
    return f"{hook} 🙏✨\n\n📖 Scripture: {scripture}\n\n{cta}\n\n{hashtags}"


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
        hook = f"If you are praying silently over {clean_topic}, receive this promise from God:"

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
    return [{"key": k, "title": v["title"], "description": v["description"]} for k, v in VIRAL_THEMES.items()]
