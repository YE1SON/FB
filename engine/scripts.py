import random
from typing import Dict, List, Optional

VIRAL_THEMES = {
    "silent_battles": {
        "title": "💔 Batallas Silenciosas y Lágrimas en Secreto",
        "description": "Para espectadores que luchan con soledad, dolor oculto o depresión.",
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

# Banco rico de escenarios visuales detallados y específicos para cada contexto
SCENARIO_POOLS = {
    "storm_rescue": [
        "Dramatic first-person POV looking up as Jesus Christ stands on turbulent stormy sea waters, reaching his strong compassionate hand directly toward the viewer to pull them from dark crashing waves, radiant sunbeams piercing through storm clouds",
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

# Mapeo de términos en español/inglés para temas personalizados
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
    """
    Analiza el texto exacto del guion, tema y dolor personalizado para generar
    un prompt de imagen único, altamente específico y variado que coincide con la oración.
    """
    full_text = f"{script_text} {custom_topic or ''}".lower()
    
    # Sistema de puntuación para seleccionar la categoría más precisa
    scores = {cat: 0 for cat in SCENARIO_POOLS.keys()}
    
    # Puntuación por tema predeterminado
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

    # Palabras clave para tormenta / rescate
    for w in ["storm", "water", "drown", "sea", "wave", "sink", "boat", "ocean", "tempest", "tormenta", "olas", "mar"]:
        if w in full_text:
            scores["storm_rescue"] += 2

    # Palabras clave para sanidad física
    for w in ["heal", "sick", "disease", "pain", "doctor", "medicine", "body", "cells", "infirmity", "cancer", "fever", "stripes", "sanar", "sanidad", "enfermedad", "dolor", "salud"]:
        if w in full_text:
            scores["miracle_healing"] += 2

    # Palabras clave para finanzas / puertas
    for w in ["financial", "money", "debt", "bills", "lack", "famine", "provision", "job", "doors", "bank", "breakthrough", "dinero", "deuda", "deudas", "finanzas", "trabajo", "puertas", "cuentas"]:
        if w in full_text:
            scores["financial_doors"] += 2

    # Palabras clave para noche / dormir
    for w in ["sleep", "night", "bed", "dream", "nightmare", "rest", "weary", "awake", "evening", "dormir", "noche", "cama", "sueño", "descanso"]:
        if w in full_text:
            scores["night_peace"] += 2

    # Palabras clave para familia / niños / matrimonio
    for w in ["family", "child", "children", "son", "daughter", "mother", "father", "marriage", "husband", "wife", "home", "household", "familia", "hijo", "hijos", "hija", "madre", "padre", "matrimonio", "hogar", "casa"]:
        if w in full_text:
            scores["family_children"] += 2

    # Palabras clave para ansiedad / pánico / protección
    for w in ["anxiety", "fear", "panic", "enemy", "attack", "chains", "armor", "giant", "darkness", "mind", "shield", "protect", "ansiedad", "miedo", "temor", "pánico", "enemigo", "mente", "escudo"]:
        if w in full_text:
            scores["anxiety_shield"] += 2

    # Palabras clave para Getsemaní / oración solitaria
    for w in ["gethsemane", "garden", "kneel", "pray", "prayer", "solitary", "alone", "getsemaní", "oración", "orar"]:
        if w in full_text:
            scores["gethsemane_prayer"] += 2

    # Palabras clave para lágrimas / quebranto
    for w in ["tear", "tears", "cried", "wept", "broken", "brokenhearted", "sorrow", "grief", "weeping", "lágrima", "lágrimas", "llorar", "quebrantado", "tristeza"]:
        if w in full_text:
            scores["tears_comfort"] += 2

    # Palabras clave para cruz / calvario
    for w in ["cross", "calvary", "tomb", "resurrection", "sacrifice", "blood", "cruz", "calvario", "tumba", "resurrección"]:
        if w in full_text:
            scores["cross_calvary"] += 2

    # Palabras clave para biblia / escrituras
    for w in ["bible", "scripture", "scriptures", "word", "verse", "scroll", "biblia", "palabra", "escritura"]:
        if w in full_text:
            scores["holy_scriptures"] += 2

    # Elegir la categoría ganadora (con un pequeño elemento de selección si hay empate)
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

    # Elegir una escena del grupo ganador aleatoriamente para garantizar variedad
    base_scene = random.choice(SCENARIO_POOLS[chosen_category])

    # Manejar tema personalizado si existe
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

    # Añadir variaciones cinematográficas aleatorias
    angle = random.choice(CAMERA_ANGLES)
    lighting = random.choice(LIGHTING_MOODS)
    details = random.choice(ARTISTIC_DETAILS)

    prompt = f"{base_scene}{topic_addon}, {lighting}, {details}, {angle}"
    return prompt

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

def get_themes_list():
    return [
        {"key": k, "title": v["title"], "description": v["description"]}
        for k, v in VIRAL_THEMES.items()
    ]
