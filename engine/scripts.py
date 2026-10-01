import random
from typing import Dict, List, Optional

VIRAL_THEMES = {
    "silent_battles": {
        "title": "💔 Batallas Silenciosas y Lágrimas en Secreto",
        "description": "Para espectadores que luchan con soledad, dolor oculto o depresión.",
        "default_image_prompt": "Heartwarming and emotional 8k cinematic vertical 9:16 portrait of Jesus Christ gently wiping away the tears of a weeping broken person, resting his loving hand on their head in comfort, warm divine golden lighting, deeply compassionate eyes, white robe and red mantle, sacred atmosphere",
        "hooks": [
            "Do not scroll past this video. God told me someone watching this cried themselves to sleep last night.",
            "Stop scrolling for just 20 seconds. Jesus knows the heavy burden you couldn't tell anyone about.",
            "This video didn't appear on your screen by accident. Jesus wants you to know He saw your silent tears.",
            "Wait, don't swipe away. God has an urgent message for the battle you are fighting alone."
        ],
        "bodies": [
            "You have been smiling in front of people, but breaking down when you are alone. Jesus says: My child, I have not forgotten you. The storm you are in right now is not meant to drown you; it is meant to clear your path. I am restoring what was broken, healing your wounded heart, and fighting battles you know nothing about.",
            "You feel like you are at your breaking point, wondering if anyone cares. Jesus says: I was right there in the room when you wept in silence. I am collecting every single tear you shed. Your pain has an expiration date, and your breakthrough is closer than you think. Stand firm, because I am holding your hand.",
            "You have been carrying a heavy weight on your chest for so long. Jesus says: Lay it at My feet right now. You were never created to carry this anxiety on your own. I am releasing supernatural peace over your mind, lifting your depression, and breathing new life into your spirit."
        ],
        "ctas": [
            "If you receive this promise in your spirit tonight, comment 'AMEN', share this with someone who needs God's peace, and follow for your daily prayer.",
            "If you believe God is fighting for you, type 'AMEN', send this to a friend fighting a silent battle, and follow this page so you never miss your daily blessing.",
            "Claim this victory right now by commenting 'AMEN'. Share this message to spread God's love, and follow for more daily hope."
        ]
    },
    "financial_breakthrough": {
        "title": "💰 Milagro Financiero y Puertas Abiertas",
        "description": "Para personas con deudas, desempleo o estrés por cuentas pendientes.",
        "default_image_prompt": "Majestic Jesus Christ standing before radiant golden open heavenly doors of light, blessing hands extended forward with divine abundance and favor, glorious sunbeams breaking through, holy warm atmosphere, photorealistic 8k vertical 9:16",
        "hooks": [
            "Before you close this app, listen closely: your season of financial famine is ending this week.",
            "If you are stressed about money, debts, or unpaid bills, do not scroll past this 30-second prayer.",
            "Jesus says: The door that was slammed in your face was Me protecting you from a trap. Listen to this.",
            "Stop scrolling right now. God is about to turn your financial struggle into a testimony."
        ],
        "bodies": [
            "You have been lying awake calculating numbers and wondering how you will make it through. Jesus says: I own the cattle on a thousand hills. I will open doors that no man can shut. I will send provision from places you never expected. Trust My timing, because lack is not your final chapter.",
            "You have sowed in tears, and now you are about to reap in joy. Jesus says: Do not lose faith in the middle of the struggle. I am preparing a table before you. Unexpected blessings, relief, and divine favor are on their way to your home right now.",
            "The enemy tried to make you believe you would stay trapped in debt and struggle forever. Jesus says: I am the God of breakthroughs. What seemed impossible in your bank account, I am turning around for your good."
        ],
        "ctas": [
            "Type 'I RECEIVE IT' and 'AMEN' in the comments to seal this blessing. Share this with your family and follow for your daily prayer.",
            "If you trust God with your finances, comment 'AMEN', share this video with someone who needs hope, and follow this page.",
            "Comment 'AMEN' to claim your breakthrough, share this to bless someone today, and follow for more inspirational prayers."
        ]
    },
    "bedtime_blessing": {
        "title": "🛌 Oración de Paz Antes de Dormir",
        "description": "Oraciones reconfortantes para antes de dormir para aliviar la mente.",
        "default_image_prompt": "Serene Jesus Christ watching over a peaceful home under a tranquil starry night sky, celestial soft golden aura and angels protecting the dwelling, calm loving expression, cinematic biblical 8k vertical 9:16",
        "hooks": [
            "Before you close your eyes and go to sleep tonight, give Jesus just 25 seconds.",
            "Do not go to sleep tonight with anxiety in your chest. Listen to this blessing first.",
            "It's late, but God kept you awake for this exact video. Take a deep breath and listen.",
            "Before you put your phone down to sleep, receive this powerful night prayer."
        ],
        "bodies": [
            "Tonight, leave every worry, every fear, and every unfinished battle in My hands. Jesus says: Sleep in peace. No evil will come near your dwelling. My angels are stationed around your home, watching over your children and protecting your mind from nightmares and fear.",
            "The day was hard, but it is finished. Jesus says: In My presence there is rest. Breathe out the tension, breathe in My grace. Tomorrow is filled with new mercies and fresh strength. Close your eyes knowing you are deeply loved.",
            "You don't have to figure everything out tonight. Jesus says: Be still and know that I am God. Rest your weary head. I am working on the solutions while you sleep, and joy is coming in the morning."
        ],
        "ctas": [
            "Comment 'AMEN' to receive God's peace over your sleep, share this with someone you love before they rest, and follow for daily night prayers.",
            "Type 'AMEN' for peaceful sleep tonight. Share this blessing and follow this page to wake up with God tomorrow.",
            "Declare peace over your home by commenting 'AMEN', share with family, and follow for your nightly prayer."
        ]
    },
    "family_healing": {
        "title": "👨‍👩‍👧 Protección y Restauración Familiar",
        "description": "Para discordia familiar, hijos rebeldes, enfermedad o matrimonios heridos.",
        "default_image_prompt": "Jesus Christ standing inside a warm ancient stone home, placing his loving hands on a family and children gathered together in peace, glowing divine golden light, sacred harmony and protection, cinematic 8k vertical 9:16",
        "hooks": [
            "If you love your family, do not scroll past this prayer. Jesus is stepping into your home.",
            "Stop scrolling right now. This is a powerful prayer of protection for your children and family.",
            "Jesus says: I have heard every prayer you whispered for your loved ones. Listen to this.",
            "Before you swipe away, let this prayer cover your household from sickness and discord."
        ],
        "bodies": [
            "I see the division, the stress, and the sickness that has tried to attack your family. Jesus says: Peace be still in your household. I am breaking every generational curse, healing physical pain, and restoring love between parents and children. Your home will be a sanctuary of light.",
            "You have been worried sick about your children and their future. Jesus says: Hand them to Me. My angels are guarding their footsteps. Where there was rebellion, I will place wisdom; where there was sorrow, I will plant laughter.",
            "No weapon formed against your family will prosper. Jesus says: I am placing a hedge of holy protection around your front door. Sickness will flee, anxiety will break, and My divine health will reign in your house."
        ],
        "ctas": [
            "Write the first name of your family member in the comments with 'AMEN' to cover them in prayer. Share this and follow for daily blessings.",
            "Comment 'AMEN' to protect your household today. Share this with your loved ones and follow this page.",
            "Claim healing for your family by typing 'AMEN', share this prayer, and follow for daily spiritual encouragement."
        ]
    },
    "divine_protection": {
        "title": "🛡️ Contra la Ansiedad y Ataques del Enemigo",
        "description": "Oración de alta autoridad contra el pánico, dudas y batallas espirituales.",
        "default_image_prompt": "Dramatic first-person perspective POV of Jesus Christ standing on turbulent stormy sea waters, reaching his strong compassionate hand directly toward the viewer to rescue them from drowning, storm clouds with divine golden light piercing through, iconic Jesus with white and blue robe, flowing hair, intense loving urgent gaze, cinematic 8k vertical 9:16",
        "hooks": [
            "The enemy does not want you to watch this video, but Jesus wants you to hear it right now.",
            "If your heart is racing with anxiety or fear today, pause and let Jesus speak to you.",
            "Do not scroll. You are not losing your mind, you are under spiritual attack, and God is fighting for you.",
            "Stop scrolling for 20 seconds. The battle you are in right now ends in your victory."
        ],
        "bodies": [
            "Fear is a liar, and anxiety has no authority over you. Jesus says: I have already defeated the darkness. Put on the full armor of God. No scheme of the enemy will derail the destiny I have written for your life. You are more than a conqueror through Christ who strengthens you.",
            "When anxiety whispers that you won't survive this, remember the Red Sea, remember the empty tomb. Jesus says: Peace I leave with you, My peace I give to you. Stand strong. The giant in front of you is nothing compared to the God inside of you.",
            "I break every chain of panic, fear, and hopelessness right now. Jesus says: Rise up. I have given you power, love, and a sound mind. You will walk out of this season stronger, wiser, and anointed."
        ],
        "ctas": [
            "Comment 'I AM PROTECTED' and 'AMEN' right now. Share this to break someone else's anxiety today, and follow this page.",
            "Type 'AMEN' if you trust Jesus more than your fear. Share this video and follow for your daily spiritual shield.",
            "Declare your victory by commenting 'AMEN'. Send this to a friend who needs courage, and follow for more daily faith."
        ]
    },
    "miracle_healing": {
        "title": "🕊️ Sanidad Milagrosa y Fuerza Física",
        "description": "Para quienes sufren dolor corporal, diagnósticos médicos o cansancio extremo.",
        "default_image_prompt": "Majestic iconic Jesus Christ laying his glowing hands on a kneeling sick and broken person, performing a miraculous healing with holy golden light emanating from his hands, warm compassionate face with flowing hair and beard, white and red robe, cinematic 9:16 vertical masterpiece, emotional, spiritual, 8k",
        "hooks": [
            "If you or someone you love needs physical healing today, do not scroll past this prayer.",
            "Jesus says: By My stripes, you are healed. Stop scrolling and let these words touch your body.",
            "The doctor may have given a bad report, but God has the final say. Listen to this 30 seconds."
        ],
        "bodies": [
            "I see the physical exhaustion and the pain you have endured. Jesus says: I am the Lord who heals you. I am sending divine restoration into your cells, cleansing your bloodstream, and renewing your strength like the eagles. What medicine couldn't fix, My holy grace is touching right now.",
            "Do not give up hope. Jesus says: I carried every disease and infirmity to the cross. Let My peace wash over your body from the crown of your head to the soles of your feet. You will live and declare the works of the Lord."
        ],
        "ctas": [
            "Comment 'I RECEIVE MY HEALING' and 'AMEN'. Share this with someone who is sick today, and follow for your daily prayer.",
            "Type 'AMEN' in faith for complete healing. Share this blessing and follow this page for daily encouragement."
        ]
    }
}

def generate_script(theme_key: Optional[str] = None, custom_topic: Optional[str] = None) -> Dict[str, str]:
    if theme_key and theme_key in VIRAL_THEMES:
        theme = VIRAL_THEMES[theme_key]
        chosen_key = theme_key
    else:
        chosen_key = random.choice(list(VIRAL_THEMES.keys()))
        theme = VIRAL_THEMES[chosen_key]

    hook = random.choice(theme["hooks"])
    body = random.choice(theme["bodies"])
    cta = random.choice(theme["ctas"])

    if custom_topic and custom_topic.strip():
        topic = custom_topic.strip()
        hook = f"Do not scroll past this video. If you are struggling with {topic.lower()} right now, listen to what Jesus says."

    full_text = f"{hook} {body} {cta}"
    image_prompt = generate_image_prompt_for_script(chosen_key, full_text, custom_topic)

    return {
        "theme": theme["title"],
        "theme_key": chosen_key,
        "hook": hook,
        "body": body,
        "cta": cta,
        "full_text": full_text,
        "image_prompt": image_prompt
    }

def generate_image_prompt_for_script(theme_key: Optional[str], script_text: str = "", custom_topic: Optional[str] = None) -> str:
    """
    Generates a highly contextual visual prompt linking the script's core message to the image scene.
    """
    text_lower = (script_text + " " + (custom_topic or "")).lower()

    if "storm" in text_lower or "water" in text_lower or "drown" in text_lower or "sea" in text_lower:
        return "Dramatic first-person perspective POV of Jesus Christ standing on turbulent stormy sea waters, reaching his strong compassionate hand directly toward the viewer to rescue them from drowning, storm clouds with divine golden light piercing through, iconic Jesus with white and blue robe, flowing hair, intense loving urgent gaze, cinematic 8k vertical 9:16"
    
    if "tear" in text_lower or "cried" in text_lower or "alone" in text_lower or "broken" in text_lower or "wept" in text_lower:
        return "Heartwarming and emotional 8k cinematic vertical 9:16 portrait of Jesus Christ gently wiping away the tears of a weeping broken person, resting his loving hand on their head in comfort, warm divine golden lighting, deeply compassionate eyes, white robe and red mantle, sacred atmosphere"
        
    if "heal" in text_lower or "sick" in text_lower or "doctor" in text_lower or "pain" in text_lower or "disease" in text_lower:
        return "Majestic iconic Jesus Christ laying his glowing hands on a kneeling sick and broken person, performing a miraculous healing with holy golden light emanating from his hands, warm compassionate face with flowing hair and beard, white and red robe, cinematic 9:16 vertical masterpiece, emotional, spiritual, 8k"

    if "debt" in text_lower or "money" in text_lower or "financial" in text_lower or "door" in text_lower or "bills" in text_lower:
        return "Majestic Jesus Christ standing before radiant golden open heavenly doors of light, blessing hands extended forward with divine abundance and favor, glorious sunbeams breaking through, holy warm atmosphere, photorealistic 8k vertical 9:16"

    if "sleep" in text_lower or "night" in text_lower or "bed" in text_lower or "dream" in text_lower:
        return "Serene Jesus Christ watching over a peaceful home under a tranquil starry night sky, celestial soft golden aura and angels protecting the dwelling, calm loving expression, cinematic biblical 8k vertical 9:16"

    if "family" in text_lower or "child" in text_lower or "house" in text_lower or "home" in text_lower:
        return "Jesus Christ standing inside a warm ancient stone home, placing his loving hands on a family and children gathered together in peace, glowing divine golden light, sacred harmony and protection, cinematic 8k vertical 9:16"

    if "cross" in text_lower:
        return "Magnificent Holy Cross standing atop Mount Calvary at golden hour sunset, dramatic celestial sunbeams and golden God rays breaking through parting storm clouds, glowing holy aura, white doves flying toward heaven, cinematic biblical spiritual atmosphere, ultra-realistic 8k photography vertical 9:16"

    if "bible" in text_lower or "word" in text_lower or "scripture" in text_lower:
        return "Jesus Christ sitting peacefully in a warm candlelit ancient stone sanctuary, holding open the Holy Bible scriptures glowing with soft divine golden light, looking up directly toward viewer with loving teaching eyes, white robe and red mantle, sacred holy presence, 8k cinematic vertical 9:16"

    # Default fallback to theme preset
    if theme_key and theme_key in VIRAL_THEMES:
        return VIRAL_THEMES[theme_key].get("default_image_prompt", VIRAL_THEMES["silent_battles"]["default_image_prompt"])

    return "Iconic majestic portrait of Jesus Christ looking directly into camera with intense compassionate love, soft divine warm rim lighting, classic flowing hair and gentle beard, white tunic and red mantle, 8k cinematic vertical 9:16"

def get_themes_list():
    return [
        {"key": k, "title": v["title"], "description": v["description"]}
        for k, v in VIRAL_THEMES.items()
    ]
