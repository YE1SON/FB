"""
JESUSREELS STUDIO v4.5 - NARRATIVE ENGINE & THEMATIC PILLARS
Generador de guiones con variedad narrativa real, situaciones humanas específicas,
catálogo bíblico verificado y soporte de 5 pilares temáticos para evitar repeticiones.
Diseñado para audiencia adulta estadounidense en inglés natural contemporáneo.
"""

import random
import re
from typing import Dict, List, Optional, Any
from engine.history import get_history_manager

# ─── 5 Pilares Temáticos Organizados ─────────────────────────────────────────

THEMATIC_PILLARS = {
    "family_relationships": {
        "name": "Familia y Relaciones",
        "description": "Oraciones por hijos, matrimonio, padres ancianos y reconciliación en el hogar.",
        "themes": ["lost_child", "family_protection", "marriage_healing", "single_parent", "elderly_parents", "sick_grandchild"]
    },
    "peace_rest_daily": {
        "name": "Paz, Descanso y Oración Cotidiana",
        "description": "Serenidad mental, entrega de la ansiedad nocturna, devoción matutina y descanso reparador.",
        "themes": ["morning_favor", "night_anxiety", "restless_sleep", "unspoken_prayer", "peace_in_storm"]
    },
    "grief_solitude_comfort": {
        "name": "Duelo, Soledad y Acompañamiento Emocional",
        "description": "Consuelo en el luto, soledad, desgaste emocional y vulnerabilidad física.",
        "themes": ["lonely_widow", "grief_loss", "healing_depression", "medical_fear"]
    },
    "faith_hope_trials": {
        "name": "Fe y Esperanza durante las Dificultades",
        "description": "Confianza en momentos de estrechez económica, desempleo, batallas legales y pruebas.",
        "themes": ["zero_balance", "job_breakthrough", "addiction_chains", "court_legal", "spiritual_warfare", "strength_weary", "guidance_direction"]
    },
    "gratitude_wisdom_growth": {
        "name": "Gratitud, Sabiduría y Crecimiento Espiritual",
        "description": "Agradecimiento, perdón de heridas pasadas, bendición en el trabajo y gracia divina.",
        "themes": ["gratitude_harvest", "forgiving_past", "business_blessing", "divine_grace"]
    }
}

# ─── Catálogo Bíblico Verificado (Textos Exactos en Inglés ESV/NIV) ─────────

BIBLICAL_CATALOGUE = {
    "lost_child": "Luke 15:20 — While he was still a long way off, his father saw him and was filled with compassion for him.",
    "family_protection": "Psalm 91:11 — For he will command his angels concerning you to guard you in all your ways.",
    "medical_fear": "2 Corinthians 12:9 — My grace is sufficient for you, for my power is made perfect in weakness.",
    "zero_balance": "Philippians 4:19 — And my God will meet all your needs according to the riches of his glory in Christ Jesus.",
    "night_anxiety": "Philippians 4:6-7 — Do not be anxious about anything, but in every situation present your requests to God.",
    "morning_favor": "Lamentations 3:22-23 — The steadfast love of the Lord never ceases; his mercies are new every morning.",
    "marriage_healing": "Colossians 3:13 — Bear with each other and forgive one another if any of you has a grievance against someone.",
    "healing_depression": "Psalm 34:18 — The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
    "job_breakthrough": "Proverbs 3:5-6 — Trust in the Lord with all your heart and lean not on your own understanding.",
    "lonely_widow": "Psalm 68:5 — A father to the fatherless, a defender of widows, is God in his holy dwelling.",
    "addiction_chains": "John 8:36 — So if the Son sets you free, you will be free indeed.",
    "elderly_parents": "Isaiah 46:4 — Even to your old age and gray hairs I am he, I am he who will sustain you.",
    "single_parent": "Isaiah 40:29 — He gives strength to the weary and increases the power of the weak.",
    "sick_grandchild": "Matthew 19:14 — Jesus said, 'Let the little children come to me, and do not hinder them.'",
    "court_legal": "Psalm 37:5-6 — Commit your way to the Lord; trust in him and he will act.",
    "restless_sleep": "Psalm 4:8 — In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.",
    "gratitude_harvest": "1 Thessalonians 5:18 — Give thanks in all circumstances; for this is God's will for you in Christ Jesus.",
    "unspoken_prayer": "Romans 8:26 — The Spirit helps us in our weakness, interceding with groans that words cannot express.",
    "spiritual_warfare": "2 Thessalonians 3:3 — The Lord is faithful, and he will strengthen you and protect you from the evil one.",
    "business_blessing": "Proverbs 16:3 — Commit to the Lord whatever you do, and he will establish your plans.",
    "forgiving_past": "Ephesians 4:32 — Be kind and compassionate to one another, forgiving each other, just as in Christ God forgave you.",
    "grief_loss": "Matthew 5:4 — Blessed are those who mourn, for they will be comforted.",
    "guidance_direction": "Psalm 32:8 — I will instruct you and teach you in the way you should go; I will counsel you with my loving eye upon you.",
    "strength_weary": "Isaiah 40:31 — Those who hope in the Lord will renew their strength. They will soar on wings like eagles.",
    "peace_in_storm": "Mark 4:39 — He got up, rebuked the wind and said to the waves, 'Quiet! Be still!' Then the wind died down.",
    "divine_grace": "Hebrews 4:16 — Let us approach God's throne of grace with confidence, so that we may receive mercy in time of need."
}

# ─── Mapeo de Traducciones para Temas Libres ────────────────────────────────

CUSTOM_TOPIC_TRANSLATIONS = {
    "hijo": "a son who feels distant from faith",
    "hijos": "our children and their future steps",
    "hija": "a daughter walking through deep trials",
    "nieto": "a grandchild needing care and protection",
    "nietos": "the younger generation of our family",
    "familia": "restoring quiet understanding at home",
    "deuda": "the stress of unpaid bills and financial strain",
    "deudas": "financial pressure weighing on the mind",
    "dinero": "honest provision for daily necessities",
    "trabajo": "finding purposeful work and direction",
    "empleo": "an open door for employment",
    "negocio": "guidance and wisdom in daily business",
    "salud": "physical fatigue and managing illness",
    "enfermedad": "facing a difficult health diagnosis",
    "cancer": "walking through a frightening medical season",
    "dolor": "living with chronic physical pain",
    "ansiedad": "restless thoughts when trying to sleep",
    "panico": "finding calm during overwhelming panic",
    "insomnio": "restoring quiet sleep after long nights",
    "soledad": "loneliness and the desire for genuine companionship",
    "depresion": "emotional weariness and finding quiet hope",
    "matrimonio": "rebuilding patience and warmth between spouses",
    "pareja": "mutual respect and kindness in a relationship",
    "divorcio": "healing after a painful separation",
    "duelo": "grieving the empty chair of someone loved",
    "luto": "bereavement and holding onto eternal hope",
    "perdon": "letting go of bitter memories and choosing peace",
    "adiccion": "breaking free from dependencies step by step",
    "juicio": "fairness and resolution in legal disputes",
    "abuela": "comfort and strength for an aging grandmother",
    "abuelo": "health and peace for an aging grandfather",
    "padres": "wisdom in caring for aging parents",
    "madre soltera": "daily endurance and grace for a single mother",
    "padre soltero": "patience and provision for a single father",
    "fuerza": "renewed strength when energy is depleted",
    "fe": "holding steady when faith feels quiet or small",
    "paz": "the peace of God that calms an uneasy heart"
}

def _translate_topic(topic: Optional[str]) -> str:
    if not topic or not topic.strip():
        return ""
    clean = topic.strip().lower()
    for es, en in CUSTOM_TOPIC_TRANSLATIONS.items():
        if es in clean:
            return en
    return topic.strip()


# ─── 26 Temas con Situación Humana, Idea Central y Perspectivas Múltiples ───

VIRAL_THEMES: Dict[str, Dict[str, Any]] = {
    "lost_child": {
        "title": "🚶‍♂️ Por el hijo o hija que se alejó",
        "pillar": "family_relationships",
        "description": "Oración y esperanza para padres con hijos distanciados o atravesando momentos difíciles.",
        "human_situation": "A parent lying awake with quiet heartache for an adult son or daughter who has drifted from home or faith.",
        "central_idea": "Love does not stop at the doorway; God's unseen care is larger than the distance between human words.",
        "hook_badge_text": "WHEN A CHILD FEELS DISTANT",
        "recommended_image": "jesus_reaching_hand.jpg",
        "scripture": BIBLICAL_CATALOGUE["lost_child"],
        "hashtags": ["#PrayingParents", "#FaithfulGod", "#FamilyGrace", "#ProdigalLove"],
        "hooks": [
            "If your heart aches tonight over a child who feels far away...",
            "To every parent whispering silent prayers before switching off the light...",
            "When your advice cannot reach them, remember that God's patience does.",
            "Before worry steals your rest regarding your son or daughter tonight..."
        ],
        "perspectives": {
            "prayer": "Lord, You know every step my child takes. Where my voice cannot go, let Your quiet mercy meet them. Protect their life, guard their conscience, and remind them that they remain deeply loved.",
            "scripture_reflection": "In Scripture, the father watched the horizon daily, not with anger, but with open arms. When you cannot fix their choices, place their tomorrow into the hands of the One who never leaves.",
            "heart_comfort": "Parenting often means learning to release what we cherish into God's keeping. Your tears are not forgotten, and no prayer prayed in faith is ever lost.",
            "story_lesson": "A wanderer once said that in his darkest hour, what kept him safe was remembering his mother's steady faith. Keep loving; your quiet prayers are still bearing fruit."
        },
        "closings": [
            "May God's peace guard both their heart and yours tonight.",
            "Rest in the knowledge that those you love are held in faithful hands.",
            "Tomorrow carries fresh grace; leave their steps with the Lord."
        ],
        "ctas": [
            "Take a quiet breath and rest in God's faithfulness tonight.",
            "Hold steady in hope; love never gives up.",
            "Save this prayer if your heart needed this quiet reminder today."
        ]
    },

    "family_protection": {
        "title": "🛡️ Protección y Paz sobre el Hogar",
        "pillar": "family_relationships",
        "description": "Serenidad y cobertura sobre la casa, los seres queridos y el descanso nocturno.",
        "human_situation": "Families facing stressful schedules, emotional friction, and the need for a quiet sanctuary.",
        "central_idea": "A home centered on grace is a shelter from the noise and pressure of the outside world.",
        "hook_badge_text": "PEACE OVER THIS HOUSE",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["family_protection"],
        "hashtags": ["#FamilyPrayer", "#PeaceInTheHome", "#ChristianLiving", "#NightDevotion"],
        "hooks": [
            "Tonight, let quiet peace settle inside the walls of your home.",
            "Before turning off the lights, bring the day's stress to a calm halt.",
            "If the world outside felt noisy today, let your home be a quiet refuge.",
            "Step into the stillness of God's presence as this evening winds down."
        ],
        "perspectives": {
            "prayer": "Father, place a gentle hedge of peace around this home tonight. Silence anxious thoughts upon our pillows, mend tired tempers with kindness, and let Your quiet rest cover every room.",
            "scripture_reflection": "Psalm 91 reminds us that true safety is found in dwelling near the Almighty. When Christ is welcomed inside, fear loses its authority over the household.",
            "heart_comfort": "Peace is not the total absence of life's demands; it is the steady assurance that God dwells with you right in the middle of them.",
            "story_lesson": "Homes built on patience endure the hardest seasons. May grace be the foundation under your roof tonight."
        },
        "closings": [
            "May your sleep be deep and your household sheltered in grace.",
            "Rest easy knowing God watches over all who dwell here.",
            "Peace be upon this house, and quiet strength for the morning."
        ],
        "ctas": [
            "Breathe out the tensions of today and rest in His peace.",
            "Share this gentle prayer with someone whose home needs quiet rest.",
            "May your heart find quiet refuge tonight."
        ]
    },

    "medical_fear": {
        "title": "🩺 Fortaleza ante la Enfermedad y el Dolor",
        "pillar": "grief_solitude_comfort",
        "description": "Consuelo, serenidad y paciencia para quienes enfrentan diagnósticos o debilidad física.",
        "human_situation": "Individuals or caregivers navigating medical appointments, test results, or daily physical limitation.",
        "central_idea": "Physical frailty does not diminish our spiritual worth; God meets us with gentle endurance in weakness.",
        "hook_badge_text": "STRENGTH IN WEAKNESS",
        "recommended_image": "jesus_healing_miracle.jpg",
        "scripture": BIBLICAL_CATALOGUE["medical_fear"],
        "hashtags": ["#StrengthInChrist", "#ComfortAndFaith", "#DailyEndurance", "#PeaceInTrials"],
        "hooks": [
            "If your body feels weary and medical worries cloud your thoughts today...",
            "When waiting for health answers makes tomorrow feel fragile...",
            "To anyone managing quiet pain or sitting in hospital waiting rooms...",
            "Take courage today: your worth is sustained by a compassionate God."
        ],
        "perspectives": {
            "prayer": "Lord Jesus, You know what it is to walk through human pain. Touch the places that feel exhausted. Grant wisdom to physicians, quiet patience to the heart, and gentle relief for the hours ahead.",
            "scripture_reflection": "The Apostle Paul learned that when human strength feels smallest, God's grace stands closest. You do not have to carry tomorrow's burdens with today's tired hands.",
            "heart_comfort": "Healing begins in the soul when we stop fighting our limitations and allow God's love to cradle our vulnerability.",
            "story_lesson": "Countless faithful souls before us found that the quietest hospital rooms can become sacred spaces of peace. You are not walking this path alone."
        },
        "closings": [
            "May His comfort sustain your body and calm your spirit.",
            "Rest gently tonight, knowing you are held by enduring grace.",
            "Tomorrow carries fresh endurance; trust each step to God."
        ],
        "ctas": [
            "Take a quiet breath and rest your body in His care.",
            "Remember you are valued and never forgotten.",
            "Save this reflection for moments when you need quiet courage."
        ]
    },

    "zero_balance": {
        "title": "🌾 Confianza en Tiempos de Dificultad Económica",
        "pillar": "faith_hope_trials",
        "description": "Serenidad y fe cuando las cuentas y las responsabilidades económicas generan presión.",
        "human_situation": "Hardworking individuals balancing unpaid bills and wondering how to meet next week's necessities.",
        "central_idea": "Our dignity does not depend on our bank balance; God remains the faithful provider of our daily bread.",
        "hook_badge_text": "TRUST IN PROVISION",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["zero_balance"],
        "hashtags": ["#FaithfulGod", "#DailyBread", "#ChristianHope", "#TrustingGod"],
        "hooks": [
            "If checking your finances today left a knot of worry in your stomach...",
            "When bills arrive faster than income, take a moment to breathe.",
            "To every honest worker doing their best to provide for their family...",
            "Before financial panic keeps you awake through the night..."
        ],
        "perspectives": {
            "prayer": "Father, You know every practical need in this home. When numbers do not seem to add up, give us wisdom, open honest doors, and deliver us from the fear of tomorrow.",
            "scripture_reflection": "Jesus reminded His followers that the birds of the air neither sow nor reap, yet our Heavenly Father feeds them. Do not measure God's care by one difficult season.",
            "heart_comfort": "Financial stress can make us feel isolated, but your character and hard work are seen by God. He provides manna one day at a time.",
            "story_lesson": "Many families look back on their leanest chapters not with bitterness, but as the time they discovered the true depth of God's daily provision."
        },
        "closings": [
            "May God grant you wisdom, open doors, and peaceful rest.",
            "Trust that God sees your honest labor and will provide.",
            "Rest tonight; panic cannot solve what faith can endure."
        ],
        "ctas": [
            "Release the pressure into His hands and take some rest tonight.",
            "Hold steady; difficult seasons do not last forever.",
            "Keep doing what is honest, and trust God with the rest."
        ]
    },

    "night_anxiety": {
        "title": "🌙 Calma para la Ansiedad Nocturna",
        "pillar": "peace_rest_daily",
        "description": "Paz mental para sobrellevar pensamientos acelerados y encontrar descanso profundo.",
        "human_situation": "Lying awake at 2 AM with a racing mind replaying the day's regrets and tomorrow's problems.",
        "central_idea": "The night belongs to God; we can safely surrender the problems we cannot solve while asleep.",
        "hook_badge_text": "CALM IN THE NIGHT",
        "recommended_image": "jesus_praying_gethsemane.jpg",
        "scripture": BIBLICAL_CATALOGUE["night_anxiety"],
        "hashtags": ["#OvercomingAnxiety", "#NightPrayer", "#PeaceOfMind", "#RestInGod"],
        "hooks": [
            "If your mind is racing tonight with thoughts you cannot resolve right now...",
            "When the quiet of the night makes every problem seem twice as loud...",
            "Before you spend another hour staring at the ceiling in worry...",
            "Take a slow breath: you are not required to solve tomorrow at midnight."
        ],
        "perspectives": {
            "prayer": "Lord, quiet the storm of racing thoughts in my mind. You hold the hours of the night in Your hand. Help me release the things I cannot change and receive Your sweet gift of rest.",
            "scripture_reflection": "Paul wrote to the Philippians to present every worry to God with petition and thanksgiving. God's peace does not always explain the storm; it guards our hearts inside it.",
            "heart_comfort": "You do not need to figure out the next five years tonight. God promises grace for one sunrise at a time.",
            "story_lesson": "A shepherd once noted that sheep only lie down when they know their guardian is standing watch. Close your eyes; your Shepherd does not sleep."
        },
        "closings": [
            "May God quiet your thoughts and grant you sweet, restorative rest.",
            "Sleep peacefully; God is watching over your tomorrow.",
            "Let His gentle stillness fill your room tonight."
        ],
        "ctas": [
            "Close your eyes, breathe gently, and let today go.",
            "Save this prayer for whenever the night feels heavy.",
            "Rest in His hands; tomorrow brings fresh mercy."
        ]
    },

    "morning_favor": {
        "title": "🌅 Gratitud y Sabiduría al Iniciar el Día",
        "pillar": "peace_rest_daily",
        "description": "Una perspectiva renovada de propósito, fe y calma para la jornada matutina.",
        "human_situation": "Waking up to a busy morning needing clarity, patience, and spiritual alignment.",
        "central_idea": "Each morning is a fresh gift of mercy; starting in quiet reflection anchors the entire day.",
        "hook_badge_text": "MORNING DEVOTION",
        "recommended_image": "jesus_holy_bible.jpg",
        "scripture": BIBLICAL_CATALOGUE["morning_favor"],
        "hashtags": ["#MorningDevotion", "#DailyWisdom", "#FreshMercy", "#ChristianRoutine"],
        "hooks": [
            "Before the rush of this day begins, pause for one quiet breath.",
            "This sunrise brings a clean slate and fresh mercy designed just for you.",
            "Before your calendar fills up with tasks, anchor your heart in peace.",
            "As you step into today's responsibilities, remember you walk with God."
        ],
        "perspectives": {
            "prayer": "Heavenly Father, guide my words and my decisions today. Guard my heart from impatience, give me eyes to notice who needs encouragement, and let Your steady wisdom lead my footsteps.",
            "scripture_reflection": "Lamentations assures us that God's compassions never fail; they are new every morning. No matter how yesterday ended, today starts with unconditional grace.",
            "heart_comfort": "You do not need to face the challenges of this day in your own strength. Walk quietly, do what is good, and trust God with the results.",
            "story_lesson": "Ancient travelers never started a journey without checking their compass. Take thirty seconds right now to center your soul on Christ."
        },
        "closings": [
            "Step forward with calm confidence; God is making a way for you.",
            "May your day be marked by patience, wisdom, and peace.",
            "Walk in grace today; you are held by an everlasting love."
        ],
        "ctas": [
            "Step forward with peace into the opportunities of today.",
            "Share this morning blessing with someone you cherish.",
            "Keep your heart anchored in His kindness today."
        ]
    },

    "marriage_healing": {
        "title": "💍 Paciencia y Restauración en el Matrimonio",
        "pillar": "family_relationships",
        "description": "Acompañamiento para superar silencios dolorosos, reavivar el afecto y perdonar.",
        "human_situation": "A couple living in polite emotional distance, wishing to bridge the gap with kindness.",
        "central_idea": "Love is sustained not by constant perfection, but by the quiet courage to forgive and rebuild trust.",
        "hook_badge_text": "HEALING IN MARRIAGE",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["marriage_healing"],
        "hashtags": ["#ChristianMarriage", "#ForgivenessInLove", "#HealthyRelationships", "#MarriageMatters"],
        "hooks": [
            "If emotional silence has created distance in your marriage lately...",
            "When daily stress makes patience run thin between two people who love each other...",
            "Before you let resentment settle into a hard wall in your relationship...",
            "To anyone hoping for gentleness and renewed warmth at home..."
        ],
        "perspectives": {
            "prayer": "Lord, soften where things have grown defensive. Give us the courage to speak with kindness, the humility to listen without defending, and the grace to forgive past misunderstandings.",
            "scripture_reflection": "Colossians instructs us to bear with one another and forgive as the Lord forgave us. A strong marriage is built by two imperfect people who refuse to stop extending grace.",
            "heart_comfort": "Reconciliation rarely happens through one grand speech; it grows through small acts of gentleness repeated day after day.",
            "story_lesson": "Gold is refined through heat and careful patience. Even relationships that feel strained can discover deeper maturity on the other side of honesty."
        },
        "closings": [
            "May God restore gentleness and mutual respect in your home.",
            "May peace guard your conversation and your shared journey.",
            "Trust that God is able to heal what feels bruised."
        ],
        "ctas": [
            "Choose kindness in one small conversation today.",
            "May your home be blessed with patience and renewed warmth.",
            "Hold onto grace; restoration begins with a humble heart."
        ]
    },

    "healing_depression": {
        "title": "🌿 Esperanza en Medio del Desánimo y la Tristeza",
        "pillar": "grief_solitude_comfort",
        "description": "Compañía compasiva para quienes sienten cansancio emocional y falta de energía.",
        "human_situation": "Waking up feeling numb, overwhelmed by everyday tasks, and battling quiet despair.",
        "central_idea": "God's love does not demand cheerful performance; He stays near to the weary in the quietest valley.",
        "hook_badge_text": "HOPE IN THE VALLEY",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": BIBLICAL_CATALOGUE["healing_depression"],
        "hashtags": ["#MentalHealthAndFaith", "#GodIsNear", "#QuietHope", "#GentleGrace"],
        "hooks": [
            "If just getting through today felt like a quiet, exhausting battle...",
            "To anyone carrying an emotional heaviness they cannot easily explain...",
            "When sadness feels like a thick fog that words cannot lift...",
            "You do not have to pretend to be strong before God today."
        ],
        "perspectives": {
            "prayer": "Father, You see the tears cried in secret and the fatigue no one notices. Meet me in this quiet place. Be my breath when words fail, and remind my soul that I am held and valued.",
            "scripture_reflection": "David wrote in Psalm 34 that God is close to the brokenhearted. He does not turn away from our weakness; He draws near with gentle comfort.",
            "heart_comfort": "Having a hard season does not mean your faith is broken. Even Elijah sat under the broom tree needing rest and nourishment before continuing his journey.",
            "story_lesson": "Seeds sprout in darkness long before breaking into the sunlight. Trust that quiet healing is taking root even when you cannot feel it."
        },
        "closings": [
            "Take one gentle step at a time; you are never abandoned.",
            "May God's tender presence bring calm to your spirit tonight.",
            "You are deeply loved, exactly as you are today."
        ],
        "ctas": [
            "Be gentle with yourself today; rest in His care.",
            "Save this reminder whenever your spirit needs quiet reassurance.",
            "Take heart; the morning light will return."
        ]
    },

    "job_breakthrough": {
        "title": "💼 Dirección y Paz en la Búsqueda de Empleo",
        "pillar": "faith_hope_trials",
        "description": "Confianza y paciencia ante la incertidumbre laboral, entrevistas y decisiones.",
        "human_situation": "Submitting resumes, waiting on unanswered emails, and questioning professional purpose.",
        "central_idea": "Closed doors can redirect our steps; God's guidance is working even during the silence.",
        "hook_badge_text": "DIRECTION & PURPOSE",
        "recommended_image": "jesus_reaching_hand.jpg",
        "scripture": BIBLICAL_CATALOGUE["job_breakthrough"],
        "hashtags": ["#CareerFaith", "#OpenDoors", "#TrustingGodsPlan", "#WorkWithPurpose"],
        "hooks": [
            "If you have been waiting anxiously on job responses or career direction...",
            "When closed doors make you question your value and abilities...",
            "To anyone striving honestly to find an open opportunity today...",
            "Before frustration convinces you that your efforts are in vain..."
        ],
        "perspectives": {
            "prayer": "Lord, lead me to honest work where my skills can serve and provide. Grant peace in the waiting, protect my mind from discouragement, and order my steps toward the right door.",
            "scripture_reflection": "Proverbs 3 reminds us to trust God with all our heart and lean not on our own understanding. A delay in the natural world is often preparation in the spiritual.",
            "heart_comfort": "Your identity is far greater than your job title. Do what you can with integrity today, and leave what you cannot control with God.",
            "story_lesson": "Many doors that closed in tears later proved to be protections that saved people from wrong paths. Trust the timing of your life."
        },
        "closings": [
            "May God open the right door and grant you peace while you wait.",
            "Walk forward with dignity; your labor in faith is not forgotten.",
            "Trust that guidance is already preparing the road ahead."
        ],
        "ctas": [
            "Keep taking honest steps; do not lose heart.",
            "May your efforts be blessed with clarity and open doors.",
            "Rest tonight knowing your future is in good hands."
        ]
    },

    "lonely_widow": {
        "title": "🕊️ Consuelo en la Soledad y la Pérdida del Cónyuge",
        "pillar": "grief_solitude_comfort",
        "description": "Acompañamiento respetuoso para quienes enfrentan la ausencia de su compañero de vida.",
        "human_situation": "Sitting in an empty living room facing quiet evenings and fond, bittersweet memories.",
        "central_idea": "Though a companion has passed, God's personal covenant of comfort remains unbroken.",
        "hook_badge_text": "COMFORT IN SOLITUDE",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": BIBLICAL_CATALOGUE["lonely_widow"],
        "hashtags": ["#ComfortForGrief", "#GodIsNear", "#GentlePeace", "#SolitudeToSanctuary"],
        "hooks": [
            "If the house feels particularly quiet and empty this evening...",
            "To the faithful heart cherishing precious memories through quiet tears...",
            "When loneliness seems to settle in as the sun goes down...",
            "You are not forgotten, even in the quietest hours of your home."
        ],
        "perspectives": {
            "prayer": "Lord Jesus, fill this quiet room with Your tender presence. Comfort my memories, soothe the ache of missing someone dearly loved, and remind me that Your love never departs.",
            "scripture_reflection": "Scripture repeatedly honors the dignity of those who carry bereavement, assuring that God Himself stands as their defender and closest companion.",
            "heart_comfort": "Grief is love's enduring witness. Give yourself permission to remember with gratitude while leaning into God's quiet companionship today.",
            "story_lesson": "A faithful widow once wrote that when her companion left, she discovered that prayer turned her loneliest chair into a sanctuary of communion with God."
        },
        "closings": [
            "May God's gentle peace warm your home and quiet your soul.",
            "You are cherished and surrounded by eternal compassion.",
            "Rest gently tonight, wrapped in His enduring care."
        ],
        "ctas": [
            "May your heart find sweet peace and gentle rest tonight.",
            "Remember that you walk with an everlasting friend.",
            "Save this prayer whenever quiet moments feel heavy."
        ]
    },

    "addiction_chains": {
        "title": "⛓️ Esperanza y Libertad ante Hábitos Dañinos",
        "pillar": "faith_hope_trials",
        "description": "Ánimo diario para quienes luchan por romper cadenas y reconstruir su vida con sobriedad.",
        "human_situation": "Struggling with repeated relapses, secret guilt, and the desire to break harmful patterns.",
        "central_idea": "Freedom is built one honest decision at a time, backed by God's non-condemning grace.",
        "hook_badge_text": "STEPPING INTO FREEDOM",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["addiction_chains"],
        "hashtags": ["#OvercomingStruggles", "#GraceToHeal", "#DailyRecovery", "#FreedomInChrist"],
        "hooks": [
            "If you fell today and feel tempted to give up on yourself completely...",
            "To anyone fighting a quiet battle against habits they despise...",
            "Before shame convinces you that you are beyond redemption...",
            "True freedom does not require instant perfection; it starts with honesty."
        ],
        "perspectives": {
            "prayer": "Lord, deliver me from the compulsions that bring harm. Strengthen my resolve in moments of vulnerability, surround me with honest support, and give me the grace to choose what brings life.",
            "scripture_reflection": "Jesus said that whoever the Son sets free is free indeed. His grace is not a license to stay trapped, but divine power to begin walking out.",
            "heart_comfort": "A stumble along the journey does not erase the progress you have made. Stand back up, dust off your knees, and take the next right step.",
            "story_lesson": "Chains are not broken by brute force in a single second; they are dismantled link by link through daily humility and community."
        },
        "closings": [
            "May God grant you sober clarity and enduring courage.",
            "You are not defined by past stumbles, but by God's grace to rebuild.",
            "Take heart; one day of victory at a time."
        ],
        "ctas": [
            "Do not carry this in secret; reach out and choose life today.",
            "Take one honest, courageous breath and begin again.",
            "Hold onto grace; your story is not finished."
        ]
    },

    "elderly_parents": {
        "title": "👵 Cuidado y Bendición para Padres Ancianos",
        "pillar": "family_relationships",
        "description": "Amor, paciencia y fortaleza para quienes cuidan a padres mayores o abuelos.",
        "human_situation": "Adult children balancing work while caring for aging parents facing declining memory or mobility.",
        "central_idea": "Honoring our parents in their frailty reflects God's gentle, lifelong covenant with humanity.",
        "hook_badge_text": "HONORING OUR ELDERS",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": BIBLICAL_CATALOGUE["elderly_parents"],
        "hashtags": ["#CaringForAgingParents", "#HonoringElders", "#FamilyDevotion", "#ChristianCaregiving"],
        "hooks": [
            "If you spent today helping an aging parent or grandparent navigate frailty...",
            "When caregiving leaves your own physical energy depleted...",
            "To everyone honoring the generation that once carried and raised them...",
            "Take a quiet moment to remember the sacred value of your daily care."
        ],
        "perspectives": {
            "prayer": "Father, bless our aging parents with dignity, comfort, and peaceful minds. Grant me patience when routine becomes repetitive, and give me a heart that honors their legacy with love.",
            "scripture_reflection": "God promises in Isaiah that even to gray hairs, He is the One who will sustain us. Serving an aging parent is holy service done directly unto Christ.",
            "heart_comfort": "The gentleness you show to an elderly mother or father in their vulnerability writes eternal goodness into your family's story.",
            "story_lesson": "Hands that once worked tirelessly to provide now rest gently in yours. Treasure these quiet moments; they are holy ground."
        },
        "closings": [
            "May God grant peace to your parents and renewed strength to you.",
            "May patience and love fill your home throughout the week.",
            "Rest tonight, knowing your caregiving is seen and blessed."
        ],
        "ctas": [
            "Take care of your own spirit so you can continue to love well.",
            "May grace guide every conversation with your family.",
            "Rest peacefully tonight in God's sustaining grace."
        ]
    },

    "single_parent": {
        "title": "🤱 Fortaleza para la Madre o Padre Soltero",
        "pillar": "family_relationships",
        "description": "Apoyo espiritual para quienes educan y sostienen su hogar con entrega diaria.",
        "human_situation": "Single mothers and fathers shouldering work, meals, discipline, and emotional presence alone.",
        "central_idea": "You may be parenting solo, but you are never without the active partnership of God.",
        "hook_badge_text": "STRENGTH FOR SINGLE PARENTS",
        "recommended_image": "jesus_reaching_hand.jpg",
        "scripture": BIBLICAL_CATALOGUE["single_parent"],
        "hashtags": ["#SingleParenting", "#StrengthForMoms", "#FaithfulFather", "#ParentingGrace"],
        "hooks": [
            "If you put the children to bed tonight completely worn out from doing it all...",
            "When carrying both the provider and caregiver roles feels overwhelming...",
            "To every single mother and father giving everything for their children...",
            "Before you let guilt tell you that you are not doing enough..."
        ],
        "perspectives": {
            "prayer": "Lord, give me strength for today and peaceful trust for tomorrow. Supply what is lacking in my resources, protect my children's hearts, and let them grow up knowing they are deeply loved.",
            "scripture_reflection": "Hagar discovered in the desert that God is 'the One who sees me'. When no other adult shares the load, the Creator Himself watches over your little family.",
            "heart_comfort": "Your children do not need a perfect parent with infinite energy; they need your steady love and the peace that comes from seeing you trust God.",
            "story_lesson": "Loaves and fishes multiplied in hands that offered what little they had. Offer your honest daily effort, and watch God multiply it."
        },
        "closings": [
            "May God renew your energy and guard your precious home tonight.",
            "Rest your mind; your dedication is bearing eternal fruit.",
            "You are doing better than you think; sleep in peace."
        ],
        "ctas": [
            "Breathe, put down the mental checklist, and get some rest.",
            "Save this prayer for days when energy runs low.",
            "Remember that you are cherished and never alone."
        ]
    },

    "sick_grandchild": {
        "title": "🧸 Oración por la Salud de un Nieto o Nieta",
        "pillar": "family_relationships",
        "description": "Súplica tierna y confiada de abuelos por la sanidad y cuidado de los pequeños.",
        "human_situation": "A grandparent praying from afar while a little one deals with fever, surgery, or sickness.",
        "central_idea": "The generational prayers of grandparents weave an enduring canopy of blessing over little lives.",
        "hook_badge_text": "PRAYER FOR A GRANDCHILD",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": BIBLICAL_CATALOGUE["sick_grandchild"],
        "hashtags": ["#GrandparentsPrayer", "#ChildrensHealth", "#FamilyFaith", "#GenerationalGrace"],
        "hooks": [
            "If your heart is aching tonight for a grandchild who is sick or hurting...",
            "To every grandmother and grandfather carrying a little one in prayer...",
            "When you wish you could take their fever or pain away yourself...",
            "Before you sleep, place that precious little life into Jesus' gentle arms."
        ],
        "perspectives": {
            "prayer": "Lord Jesus, You welcomed children with joy. Lay Your gentle hand upon this little child tonight. Cool the fever, ease the pain, bring wise guidance to doctors, and grant peaceful sleep to their parents.",
            "scripture_reflection": "Jesus stopped crowds to blessing small children, reminding us that the kingdom of heaven belongs to such as these. Your prayers for them carry immense weight in heaven.",
            "heart_comfort": "Grandparents carry a unique spiritual mantle. While doctors provide medicine, your prayers surround that child with celestial peace.",
            "story_lesson": "Timothy's unfeigned faith was first nurtured in his grandmother Lois. The faith you invest over your grandchildren will outlast your own lifetime."
        },
        "closings": [
            "May God restore health, laughter, and energy to that precious child.",
            "Rest in the assurance that Jesus watches over their crib tonight.",
            "Peace be upon their little body and upon your faithful heart."
        ],
        "ctas": [
            "Trust that child into the safest hands in the universe.",
            "May your prayers bring comfort to the whole family.",
            "Rest gently tonight, knowing God hears a grandparent's whisper."
        ]
    },

    "court_legal": {
        "title": "⚖️ Paz y Justicia en Procesos Legales o Disputas",
        "pillar": "faith_hope_trials",
        "description": "Serenidad y rectitud para quienes enfrentan litigios, contratos o audiencias.",
        "human_situation": "Waiting on court dates, legal mediation, or dealing with unfair accusations.",
        "central_idea": "Human courts are imperfect, but God's justice and truth ultimately defend the humble.",
        "hook_badge_text": "JUSTICE & INTEGRITY",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["court_legal"],
        "hashtags": ["#PeaceInDisputes", "#IntegrityAndTruth", "#TrustInGod", "#FaithInTrials"],
        "hooks": [
            "If an unresolved legal dispute or paperwork has been keeping you anxious...",
            "When facing unfair treatment or waiting on judicial decisions...",
            "To anyone striving for truth and fairness in an exhausting conflict...",
            "Before worry consumes another evening over legal outcomes..."
        ],
        "perspectives": {
            "prayer": "Lord, You love justice and uphold the humble. Guide attorneys with truth, grant discernment to judges, calm my uneasy heart, and let righteousness prevail in this situation.",
            "scripture_reflection": "Psalm 37 reminds us to commit our way to the Lord; He will bring forth your vindication like the light. We do not have to resort to bitterness to stand for what is right.",
            "heart_comfort": "Legal battles can feel overwhelming, but your peace does not belong to an earthly courtroom. Keep your integrity clean and leave the outcome with God.",
            "story_lesson": "Daniel faced the highest court in Babylon with calm devotion, and God shut the lions' mouths. Truth always outlives false accusations."
        },
        "closings": [
            "May God grant clarity, fair resolution, and quiet peace of mind.",
            "Walk with integrity; God defends those who seek what is honest.",
            "Rest tonight, knowing truth is never abandoned by heaven."
        ],
        "ctas": [
            "Commit the situation into His hands and take a peaceful breath.",
            "Keep doing what is upright, and let peace guard your heart.",
            "May wisdom prevail in every legal step ahead."
        ]
    },

    "restless_sleep": {
        "title": "🛌 Reposo Profundo y Desconexión del Estrés",
        "pillar": "peace_rest_daily",
        "description": "Una invitación a desconectar la mente, soltar el control y descansar en paz.",
        "human_situation": "Physical tiredness combined with mental tension that prevents drifting off to sleep.",
        "central_idea": "Sleep is an act of trust; it acknowledges that God works while we are resting.",
        "hook_badge_text": "PEACEFUL SLEEP",
        "recommended_image": "jesus_praying_gethsemane.jpg",
        "scripture": BIBLICAL_CATALOGUE["restless_sleep"],
        "hashtags": ["#SweetSleep", "#NightPeace", "#RestInChrist", "#BedtimeDevotion"],
        "hooks": [
            "Before you close your eyes carrying the unsolved problems of today...",
            "If your pillow feels like a place of thinking instead of resting tonight...",
            "Take one long, deliberate breath and set down your mental burden.",
            "You have done what was in your power today; now let sleep do its work."
        ],
        "perspectives": {
            "prayer": "Father, I surrender my unfinished tasks into Your care. Relax the tension in my shoulders, quiet my thoughts, and grant me deep, uninterrupted sleep under Your watch.",
            "scripture_reflection": "Psalm 4:8 says: 'In peace I will lie down and sleep, for You alone, Lord, make me dwell in safety.' Sleep is a reminder that we are creatures, not controllers of the universe.",
            "heart_comfort": "Rehearsing tomorrow's meetings or bills in bed changes nothing. Trust that God has already walked into your tomorrow.",
            "story_lesson": "Jesus slept peacefully in the boat during a tempest because His heart was anchored in the Father. Rest in that same quiet assurance tonight."
        },
        "closings": [
            "May your sleep be deep, sweet, and restorative for the morning.",
            "Rest peacefully; God remains awake and watching over your life.",
            "Let gentle silence fill your room and grant you rest."
        ],
        "ctas": [
            "Turn off your screen, take a deep breath, and rest.",
            "May peaceful slumber restore your mind and body.",
            "Goodnight; wake up to fresh mercy tomorrow."
        ]
    },

    "gratitude_harvest": {
        "title": "🌾 Gratitud por las Bendiciones Cotidianas",
        "pillar": "gratitude_wisdom_growth",
        "description": "Reconocer las pequeñas cosas buenas, la fidelidad de Dios y la alegría del corazón.",
        "human_situation": "Rushing through life without pausing to celebrate small victories and everyday provisions.",
        "central_idea": "Gratitude shifts our focus from what is lacking to the quiet abundance already present.",
        "hook_badge_text": "A HEART OF THANKS",
        "recommended_image": "jesus_holy_bible.jpg",
        "scripture": BIBLICAL_CATALOGUE["gratitude_harvest"],
        "hashtags": ["#GratitudeDaily", "#ThankfulHeart", "#CountYourBlessings", "#ChristianJoy"],
        "hooks": [
            "Before today ends, name three simple things that went right.",
            "It is easy to focus on what is missing, but pause to notice what remains.",
            "Take thirty seconds right now to thank God for the gift of another day.",
            "A grateful heart turns an ordinary evening into a celebration of grace."
        ],
        "perspectives": {
            "prayer": "Lord God, thank You for the breath in my lungs, the roof over my head, and the daily mercies I so often take for granted. Teach me to walk with eyes open to Your quiet goodness.",
            "scripture_reflection": "Paul encouraged believers to give thanks in all circumstances. Gratitude is not pretending trials do not exist; it is choosing to remember that God's goodness is bigger.",
            "heart_comfort": "When we count our blessings rather than our complaints, anxiety begins to lose its grip and deep contentment takes its place.",
            "story_lesson": "The traveler who stops to thank the well-keeper drinks with greater joy. Cultivate gratitude; it transforms the ordinary into the sacred."
        },
        "closings": [
            "May your evening be filled with contentment and joy.",
            "Walk forward with a thankful heart that sees God's goodness.",
            "Rest well tonight, thankful for the gift of today."
        ],
        "ctas": [
            "Whisper a quiet thank You before turning out the light.",
            "Share a word of gratitude with someone who blessed your week.",
            "Sleep with a grateful heart tonight."
        ]
    },

    "unspoken_prayer": {
        "title": "🤫 Por la Petición que Nadie Más Conoce",
        "pillar": "peace_rest_daily",
        "description": "Acompañamiento íntimo para oraciones secretas, silencios profundos y cargas personales.",
        "human_situation": "Carrying a burden too private, sensitive, or painful to share even with close friends.",
        "central_idea": "God understands the prayer behind our sighs before we find the words to articulate it.",
        "hook_badge_text": "THE UNSPOKEN BURDEN",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": BIBLICAL_CATALOGUE["unspoken_prayer"],
        "hashtags": ["#GodHearsYou", "#UnspokenPrayer", "#QuietTrust", "#SecretPrayer"],
        "hooks": [
            "If you are carrying a prayer tonight that you cannot say out loud to anyone...",
            "To the heart holding a burden too tender or private to explain...",
            "When words fail and only a quiet sigh can describe how you feel...",
            "You do not have to explain your heart to the One who made it."
        ],
        "perspectives": {
            "prayer": "Lord, You know the thoughts I cannot put into sentences. Read the quiet ache of my heart. Where I am confused, bring light; where I am weary, bring rest; and hold this situation in Your mercy.",
            "scripture_reflection": "Romans 8 assures us that the Spirit Himself intercedes for us with groanings too deep for words. God does not demand articulate speeches; He listens to the posture of the soul.",
            "heart_comfort": "There is profound relief in knowing that the God of the universe knows your entire story and still looks upon you with unconditional kindness.",
            "story_lesson": "Hannah wept silently in the temple, moving her lips without making a sound, and God heard her deepest longing. Your silent prayer is already received."
        },
        "closings": [
            "May God's understanding presence surround you in the quiet.",
            "Rest tonight, knowing that what is hidden is safely held.",
            "Peace be upon your spirit; God is working in secret."
        ],
        "ctas": [
            "Release that silent weight into His care tonight.",
            "You are fully known and deeply loved; rest well.",
            "Save this reminder for moments when words feel too small."
        ]
    },

    "spiritual_warfare": {
        "title": "⚔️ Firmeza y Paz frente al Desánimo y la Opresión",
        "pillar": "faith_hope_trials",
        "description": "Recordatorio de que la victoria espiritual se vive desde la serenidad, la verdad y la fe.",
        "human_situation": "Feeling under heavy emotional assault, persistent discouragement, or spiritual dryness.",
        "central_idea": "Spiritual victory is not panic or shouting; it is standing calm and rooted in the truth of Christ.",
        "hook_badge_text": "STANDING FIRM IN FAITH",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["spiritual_warfare"],
        "hashtags": ["#SpiritualArmor", "#FaithfulStand", "#VictoryInChrist", "#SteadfastSoul"],
        "hooks": [
            "If discouragement has been whispering that your efforts do not matter...",
            "When everyday trials feel like a relentless spiritual opposition...",
            "Before you let defeatist thoughts dictate your mood tomorrow...",
            "Remember who holds your life; no weapon formed against truth can prevail."
        ],
        "perspectives": {
            "prayer": "Lord, put on me the whole armor of God. Guard my mind with truth, protect my heart with righteousness, extinguish every flaming arrow of fear, and let me stand immovable in Your peace.",
            "scripture_reflection": "Ephesians teaches that our strength comes from standing in the Lord's mighty power. Notice the instruction is simply to stand firm, anchored in what Christ has already won.",
            "heart_comfort": "Opposition often appears strongest when you are closest to a breakthrough. Do not give ground to fear; keep doing what is honorable.",
            "story_lesson": "A lighthouse does not fight the storm with noise; it simply keeps its light burning bright. Stand firm and let your faith shine."
        },
        "closings": [
            "May the Lord strengthen your heart and silence every anxious lie.",
            "Stand firm in grace; victory is already anchored in Christ.",
            "Rest securely tonight; God is your shield and defense."
        ],
        "ctas": [
            "Take courage, stand firm in faith, and rest tonight.",
            "Hold onto truth; lies cannot survive in God's light.",
            "May your soul be filled with quiet, victorious peace."
        ]
    },

    "business_blessing": {
        "title": "🏪 Integridad y Prosperidad en el Trabajo y Negocio",
        "pillar": "gratitude_wisdom_growth",
        "description": "Sabiduría para emprender, servir con honestidad y administrar los recursos con fe.",
        "human_situation": "Managing a small business, client relations, and seeking ethical growth with peace.",
        "central_idea": "True prosperity is having enough to provide, bless others, and walk with an uncompromised conscience.",
        "hook_badge_text": "INTEGRITY IN WORK",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["business_blessing"],
        "hashtags": ["#FaithInBusiness", "#HonestLabor", "#KingdomEthics", "#DailyIntegrity"],
        "hooks": [
            "If managing your work or small business brought stress to your shoulders today...",
            "When commercial decisions require wisdom, honesty, and courage...",
            "To every entrepreneur and worker striving to build something honest...",
            "Commit your daily labor to God before planning tomorrow's steps."
        ],
        "perspectives": {
            "prayer": "Lord, bless the work of our hands. Grant creative wisdom in solving problems, integrity in every transaction, kindness toward customers and staff, and fair provision for our families.",
            "scripture_reflection": "Proverbs 16:3 instructs us to commit our work to the Lord, and our plans will be established. When business serves people rather than greed, God's favor attends it.",
            "heart_comfort": "Success in the kingdom of God is measured by faithfulness and generosity, not just balance sheets. Keep serving with excellence.",
            "story_lesson": "Honest craftsmen throughout history left lasting reputations by working as unto the Lord. May your daily vocation reflect His integrity."
        },
        "closings": [
            "May God prosper your honest efforts and grant you wisdom.",
            "Walk with integrity; honest labor always bears good fruit.",
            "Rest tonight, knowing God establishes what is done in truth."
        ],
        "ctas": [
            "Commit tomorrow's projects to God and enjoy your evening.",
            "Keep serving people with honesty and excellence.",
            "May your work bring blessing to your community."
        ]
    },

    "forgiving_past": {
        "title": "🕊️ Sanar y Soltar Heridas del Pasado",
        "pillar": "gratitude_wisdom_growth",
        "description": "Liberación del rencor, reconciliación interior y el poder transformador del perdón.",
        "human_situation": "Remembering an old betrayal or hurt that still stirs anger and robs present peace.",
        "central_idea": "Forgiveness does not excuse what was wrong; it sets the prisoner free and discovers the prisoner was you.",
        "hook_badge_text": "FREEDOM TO FORGIVE",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["forgiving_past"],
        "hashtags": ["#HealingThroughForgiveness", "#LettingGo", "#InnerPeace", "#GraceWins"],
        "hooks": [
            "If an old hurt or bitter memory resurfaced to trouble your heart today...",
            "When carrying resentment feels like holding onto burning embers...",
            "Before you let yesterday's wounds dictate how you love tomorrow...",
            "True emotional freedom begins when we choose to release what hurt us."
        ],
        "perspectives": {
            "prayer": "Lord Jesus, You forgave those who wounded You on the cross. Heal the tender places in my memory. Give me the strength to release resentment, let go of bitterness, and walk in freedom.",
            "scripture_reflection": "Ephesians calls us to be kind and tenderhearted, forgiving each other as God in Christ forgave us. Forgiveness is not saying the offense was acceptable; it is placing justice in God's hands.",
            "heart_comfort": "You do not forgive to please the person who harmed you; you forgive so their mistake no longer controls your peace of mind.",
            "story_lesson": "A closed fist cannot receive new blessings. Open your hands, let the past fall away, and receive God's fresh grace for today."
        },
        "closings": [
            "May God heal your memories and fill your heart with light.",
            "Walk in freedom; your future is not held hostage by your past.",
            "Rest peacefully tonight in the liberty of forgiveness."
        ],
        "ctas": [
            "Release one painful memory into His hands tonight.",
            "Choose freedom and let your heart breathe again.",
            "May quiet healing mend every past wound."
        ]
    },

    "grief_loss": {
        "title": "🖤 Consuelo en el Duelo y la Despedida",
        "pillar": "grief_solitude_comfort",
        "description": "Acompañamiento respetuoso para transitar el luto y recordar con esperanza eterna.",
        "human_situation": "Navigating anniversaries, empty chairs, and the quiet ache of losing a loved one.",
        "central_idea": "Christian hope does not deny tears; it anchors grief in the promise of resurrection and reunion.",
        "hook_badge_text": "COMFORT IN MOURNING",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": BIBLICAL_CATALOGUE["grief_loss"],
        "hashtags": ["#GriefSupport", "#ComfortInChrist", "#EternalHope", "#PreciousMemories"],
        "hooks": [
            "To anyone sitting with an empty chair and a heart full of memories tonight...",
            "When grief catches you unexpectedly in the middle of an ordinary day...",
            "If you have been holding back tears to stay strong for others...",
            "It is okay to weep; Jesus Himself wept at the tomb of His friend."
        ],
        "perspectives": {
            "prayer": "Father of mercies, wrap Your comfort around this grieving heart. When memories bring tears, let them also bring gratitude for the love we shared. Hold us steady until the morning of eternity.",
            "scripture_reflection": "Revelation promises a day when God will wipe away every tear from their eyes, and death shall be no more. Grief is painful, but it is not without eternal hope.",
            "heart_comfort": "Take your time. Healing after great loss does not happen by forgetting; it happens by learning to carry their memory with tender honor.",
            "story_lesson": "Love never dies; it simply changes address into the presence of God. Treasure what was given, and rest in His promises."
        },
        "closings": [
            "May the God of all comfort cradle your tender heart tonight.",
            "May sweet memories bring quiet peace alongside your tears.",
            "Rest gently; those we love in Christ are never truly lost."
        ],
        "ctas": [
            "Be kind to your grieving heart today; rest in His arms.",
            "Save this reflection whenever the ache of loss returns.",
            "May eternal hope sustain your soul through the night."
        ]
    },

    "guidance_direction": {
        "title": "🧭 Sabiduría y Dirección para Tomar Decisiones",
        "pillar": "faith_hope_trials",
        "description": "Claridad y paz cuando nos encontramos en encrucijadas importantes de la vida.",
        "human_situation": "Facing major choices regarding career, family moves, or ethical dilemmas without clear answers.",
        "central_idea": "God guides our steps not by revealing the entire map at once, but by lighting the next step.",
        "hook_badge_text": "WISDOM FOR THE ROAD",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["guidance_direction"],
        "hashtags": ["#DivineGuidance", "#GodsWill", "#WisdomDaily", "#NextSteps"],
        "hooks": [
            "If you are standing at an important crossroads unsure of which path to take...",
            "When big decisions make your mind feel overwhelmed with questions...",
            "Before you let decision fatigue force a hasty or anxious choice...",
            "God does not call you to guess His will; He invites you to walk with Him."
        ],
        "perspectives": {
            "prayer": "Lord, give me clarity of mind and peace in my spirit. Close doors that would bring harm, open pathways aligned with Your truth, and quiet every voice of panic.",
            "scripture_reflection": "Psalm 32:8 promises: 'I will instruct you and teach you in the way you should go.' Guidance comes through daily communion and wise counsel, not anxious calculation.",
            "heart_comfort": "You do not need to see all ten miles ahead; you only need enough light for the step right in front of you. Take it in faith.",
            "story_lesson": "Ancient seafarers navigated by fixed stars, not by the shifting waves. Anchor your decisions on eternal principles of integrity and love."
        },
        "closings": [
            "May God make your path clear and fill your heart with peace.",
            "Step forward with calm confidence; wisdom goes before you.",
            "Rest tonight, knowing your steps are guided by faithful hands."
        ],
        "ctas": [
            "Take one prayerful step at a time; trust the process.",
            "May wisdom illuminate every choice on your horizon.",
            "Sleep peacefully; clarity often arrives with the morning light."
        ]
    },

    "strength_weary": {
        "title": "🦅 Nuevas Fuerzas para el Alma Cansada",
        "pillar": "faith_hope_trials",
        "description": "Renovación espiritual y física cuando la rutina o las cargas han agotado la energía.",
        "human_situation": "Working two jobs, managing chronic fatigue, and feeling physically and emotionally drained.",
        "central_idea": "Human stamina has limits, but the Creator's strength is an inexhaustible spring.",
        "hook_badge_text": "RENEWED STRENGTH",
        "recommended_image": "jesus_reaching_hand.jpg",
        "scripture": BIBLICAL_CATALOGUE["strength_weary"],
        "hashtags": ["#RenewedStrength", "#WearySoul", "#WaitOnTheLord", "#DailyGrace"],
        "hooks": [
            "If your energy is completely running on empty tonight...",
            "When carrying everyone else's needs has left you feeling exhausted...",
            "To the tired soul who kept going today despite feeling depleted...",
            "Before you fall asleep feeling guilty for needing physical rest..."
        ],
        "perspectives": {
            "prayer": "Lord God, You never grow tired or weary. Pour fresh strength into this tired body. Renew my endurance, heal my fatigue, and remind me that rest is holy in Your sight.",
            "scripture_reflection": "Isaiah 40:31 promises that those who wait on the Lord will renew their strength; they will soar on wings like eagles. Waiting on God is quiet replenishment, not passive waiting.",
            "heart_comfort": "Rest is not a reward you earn only after finishing everything; it is a necessity given by God to preserve your life. Receive it with gratitude.",
            "story_lesson": "Even the mightiest eagle rests on high rocks to let the wind lift its wings. Let God's gentle grace carry you tonight."
        },
        "closings": [
            "May God renew your energy and refresh your tired spirit.",
            "Sleep deeply tonight, held in the arms of the Almighty.",
            "Tomorrow carries renewed stamina; rest in peace."
        ],
        "ctas": [
            "Put down your burdens, close your eyes, and rest.",
            "You have done enough today; receive His peace.",
            "May your soul wake up refreshed and renewed."
        ]
    },

    "peace_in_storm": {
        "title": "⚓ Paz en Medio de la Tormenta",
        "pillar": "peace_rest_daily",
        "description": "Serenidad inquebrantable cuando circunstancias externas parecen fuera de control.",
        "human_situation": "Surrounded by unexpected crises, conflict, or sudden instability.",
        "central_idea": "The peace of Christ does not prevent storms from gathering; it prevents the storm from getting inside your heart.",
        "hook_badge_text": "CALM IN THE STORM",
        "recommended_image": "jesus_reaching_hand.jpg",
        "scripture": BIBLICAL_CATALOGUE["peace_in_storm"],
        "hashtags": ["#PeaceInTheStorm", "#AnchorOfHope", "#FaithOverFear", "#CalmSoul"],
        "hooks": [
            "If external circumstances feel chaotic and swirling out of control today...",
            "When sudden bad news tries to shatter your quiet peace...",
            "Before fear convinces you that the ship is about to go down...",
            "Take heart: the Master of wind and waves is in the boat with you."
        ],
        "perspectives": {
            "prayer": "Jesus, speak Your sovereign 'Peace, be still' over my anxious heart. When the wind howls outside, let Your calm reign inside. Anchor my hope on Your unchanging character.",
            "scripture_reflection": "In Mark 4, the disciples panicked in the squall while Jesus slept. When you know who holds the winds, you can rest even while the boat rocks.",
            "heart_comfort": "The depth of an anchor is proven in turbulent waters. Your faith is rooted in the One who created the sea; you will not be swept away.",
            "story_lesson": "Old sailors used to say that a ship cannot sink until the water gets inside. Guard your heart; keep the peace of Christ within."
        },
        "closings": [
            "May the peace of Christ steady your heart and mind tonight.",
            "Rest safely; your Anchor holds firm through every wave.",
            "Sleep in calm assurance; the storm will pass."
        ],
        "ctas": [
            "Breathe out the tension and anchor your soul in Him.",
            "Hold steady; God is sovereign over every storm.",
            "May deep tranquility cover your home tonight."
        ]
    },

    "divine_grace": {
        "title": "✨ La Maravilla de la Gracia Incondicional",
        "pillar": "gratitude_wisdom_growth",
        "description": "El descanso profundo de saber que somos aceptados y amados por amor, no por méritos.",
        "human_situation": "Feeling unspiritual, guilty, or feeling that God is disappointed with our imperfections.",
        "central_idea": "Grace is unearned, unmerited favor; we are loved because of who God is, not because of what we accomplish.",
        "hook_badge_text": "THE GIFT OF GRACE",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": BIBLICAL_CATALOGUE["divine_grace"],
        "hashtags": ["#GraceUponGrace", "#AcceptedInChrist", "#UnconditionalLove", "#ChristianAssurance"],
        "hooks": [
            "If you have been feeling spiritually inadequate or hard on yourself lately...",
            "Before you measure your standing with God by how well you performed today...",
            "To anyone tired of religious performance and striving for approval...",
            "Take a deep breath: God's love for you is not on probation."
        ],
        "perspectives": {
            "prayer": "Father, thank You that Your love is based on Christ's finished work, not my daily perfection. Deliver me from self-condemnation, and let me rest in the assurance of Your adoption.",
            "scripture_reflection": "Hebrews invites us to approach the throne of grace with confidence, not fear. We come not as strangers presenting resumes, but as children welcomed into the Father's house.",
            "heart_comfort": "You do not have to clean up your life before you come to God; His kindness is what transforms us from the inside out.",
            "story_lesson": "Grace is like the sunlight pouring through an open window: it does not demand the room be spotless before it illuminates every corner with warmth."
        },
        "closings": [
            "May the boundless grace of Christ quiet every accusation.",
            "Rest tonight, secure and celebrated in His unconditional love.",
            "You are held in everlasting hands; sleep in peaceful assurance."
        ],
        "ctas": [
            "Receive His gift of grace and let self-judgment go.",
            "May your soul rest completely in His unconditional love.",
            "Sleep peacefully tonight; you are forever accepted in Christ."
        ]
    }
}


# ─── Prompts Visuales Limpios y Coherentes para las 3 Escenas ───────────────

THEME_3SCENE_CONFIGS = {
    "lost_child": {
        "s1": [
            "A concerned parent sitting quietly near a window at dusk looking outside, soft warm interior lighting, balanced 35mm composition",
            "A person holding an open family photo album by warm lamplight, nostalgic reflective atmosphere, cinematic depth of field",
            "An open front doorway illuminated by a gentle porch light overlooking a quiet suburban street at evening"
        ],
        "s2": [
            "A devout Christian praying with folded hands over an open Holy Bible, warm amber candlelight, reverent spiritual atmosphere",
            "A mother and father praying together with heads bowed and quiet faith, soft morning dawn breaking through curtains",
            "Hands gently resting on an open Bible illuminated by soft golden rays, quiet intercession and hope"
        ],
        "s3": [
            "A peaceful family walking together along a sunlit park trail, warm morning sunbeams, restoration and harmony",
            "Jesus Christ extending open welcoming arms in a serene golden landscape, gentle compassionate expression, atmospheric light",
            "A welcoming warm home doorway filled with radiant golden light, peaceful resolution and family grace"
        ]
    },

    "morning_favor": {
        "s1": [
            "Golden morning sunrise streaming through an open window onto a wooden table, steam rising gently from a cup, clean composition",
            "Panoramic dawn over a peaceful misty valley, warm golden morning sunbeams, fresh clean atmosphere",
            "A person opening window shutters to welcome the golden dawn, taking a deep breath of fresh air, serene 35mm photograph"
        ],
        "s2": [
            "An open Holy Bible resting on a wooden desk bathed in pristine morning sunlight, quiet devotion and reflection",
            "A person praying in quiet gratitude with morning light illuminating their face, gentle peaceful expression",
            "A solitary figure walking peacefully along a garden path at sunrise, soft golden hour lighting, quiet communion with God"
        ],
        "s3": [
            "A bright open horizon under a clear morning sky, radiant sunbeams, sense of purpose and fresh beginning",
            "Jesus Christ standing in warm morning sunlight with welcoming open hands, gentle serene expression, divine grace",
            "A sunlit path stretching forward into green pastures, glorious morning light, peaceful victory"
        ]
    },

    "night_anxiety": {
        "s1": [
            "A quiet bedroom at midnight, soft ambient bedside lamp, starry night sky visible through a window, serene 35mm composition",
            "A person sitting on the edge of a bed looking thoughtfully out into the quiet night, soft moonlight, contemplative atmosphere",
            "A silhouette in quiet stillness during the night, moonlight gently resting on a closed Bible on the nightstand"
        ],
        "s2": [
            "A person breathing out tension with closed eyes and relaxed shoulders, illuminated by warm gentle lamplight, quiet prayer",
            "An open Bible on a bedside table illuminated by soft soothing amber glow, atmosphere of sanctuary and peace",
            "Hands folded gently in prayer as dark shadows dissolve into warm golden light, peaceful surrender"
        ],
        "s3": [
            "A person sleeping peacefully in bed, gentle moonlight, tranquil expressions, deep restorative rest",
            "Jesus Christ standing in gentle celestial light with outstretched hands speaking peace, calming aura, serene night sky",
            "A calm glassy lake reflecting starry night skies and gentle moonlight, absolute stillness and peace"
        ]
    }
}


def generate_3scene_prompts_for_script(
    theme_key: Optional[str] = None,
    script_text: str = "",
    custom_topic: Optional[str] = None
) -> Dict[str, str]:
    """
    Genera 3 prompts de imagen coherentes, estructurados y libres de adjetivos vacíos.
    Escena 1: Apertura contextual.
    Escena 2: Mensaje y reflexión.
    Escena 3: Cierre y resolución.
    """
    t_key = theme_key if (theme_key and theme_key in VIRAL_THEMES) else "morning_favor"
    theme = VIRAL_THEMES.get(t_key, VIRAL_THEMES["morning_favor"])

    custom_trans = _translate_topic(custom_topic) if (custom_topic and custom_topic.strip()) else ""
    topic_cue = f", reflecting themes of {custom_trans}" if custom_trans else ""

    if t_key in THEME_3SCENE_CONFIGS:
        cfg = THEME_3SCENE_CONFIGS[t_key]
        raw1 = random.choice(cfg["s1"])
        raw2 = random.choice(cfg["s2"])
        raw3 = random.choice(cfg["s3"])
    else:
        # Generación temática estructurada
        raw1 = f"A person in quiet thoughtful contemplation{topic_cue}, soft natural window light, authentic 35mm composition"
        raw2 = f"Hands praying reverently over an open Holy Bible, warm candlelight, peaceful spiritual atmosphere"
        raw3 = f"A peaceful sunrise landscape with gentle golden rays, quiet hope and serene resolution"

    clean_style1 = "35mm photography, natural morning light, balanced composition, authentic atmosphere"
    clean_style2 = "natural window lighting, warm amber tones, quiet reflective mood, 50mm portrait composition"
    clean_style3 = "golden morning sunlight, serene atmosphere, quiet depth of field, reverent composition"

    p1 = f"{raw1}, {clean_style1} --ar 9:16"
    p2 = f"{raw2}, {clean_style2} --ar 9:16"
    p3 = f"{raw3}, {clean_style3} --ar 9:16"

    return {
        "prompt": p1,
        "scene_1_prompt": p1,
        "scene_2_prompt": p2,
        "scene_3_prompt": p3
    }


def generate_seo_caption(
    theme_title: str,
    prayer_text: str,
    scripture: str,
    cta: str,
    hashtags: List[str]
) -> str:
    """Crea un copy breve: un solo extracto, referencia bíblica y CTA sin duplicar la locución."""
    clean_title = re.sub(r'^[^\w]+', '', theme_title).strip()
    clean_cta = re.sub(r"\s+", " ", cta or "").strip()

    # El llamador proporciona la locución completa. Retira el CTA final antes de
    # elegir el extracto, porque el CTA se añade una sola vez como bloque propio.
    narration = re.sub(r"\s+", " ", prayer_text or "").strip().strip('"“”')
    if clean_cta and narration.casefold().endswith(clean_cta.casefold()):
        narration = narration[:-len(clean_cta)].rstrip(" —–-,:;")

    # No copiar todo el audio a la descripción: deja solo la primera oración.
    excerpt = re.split(r"(?<=[.!?])\s+", narration, maxsplit=1)[0].strip() if narration else ""
    if len(excerpt) > 220:
        excerpt = excerpt[:217].rstrip() + "..."

    tags_str = " ".join((hashtags or [])[:5])
    parts = [f"✝️ {clean_title} ✝️"]
    if excerpt:
        parts.extend(["", f"“{excerpt}”"])
    if scripture:
        parts.extend(["", f"📖 {scripture}"])
    if clean_cta:
        parts.extend(["", f"🕊️ {clean_cta}"])
    if tags_str:
        parts.extend(["", tags_str])
    return "\n".join(parts)


# ─── Generador Interno por Plantillas con Control de Repeticiones ───────────

def generate_internal_template_script(
    theme_key: Optional[str] = None,
    custom_topic: Optional[str] = None,
    mode: str = "deep",
    tone: Optional[str] = None,
    seamless_loop: bool = False
) -> Dict[str, Any]:
    """Genera un guion interno con situaciones humanas concretas, evitando repeticiones recientes."""
    history_mgr = get_history_manager()

    # Si no se pasó theme_key, seleccionar uno rotando para no repetir los últimos 5
    if not theme_key or theme_key not in VIRAL_THEMES:
        recent_themes = history_mgr.get_recent_theme_keys(count=5)
        available_keys = [k for k in VIRAL_THEMES.keys() if k not in recent_themes]
        chosen_key = random.choice(available_keys) if available_keys else random.choice(list(VIRAL_THEMES.keys()))
    else:
        chosen_key = theme_key

    theme = VIRAL_THEMES[chosen_key]
    human_sit = theme.get("human_situation", "")
    central_idea = theme.get("central_idea", "")

    # 1. Gancho (Hook): Elegir uno que no haya sido utilizado recientemente
    hook_candidates = theme.get("hooks", ["Before you close your eyes carrying that quiet worry tonight..."])
    if custom_topic and custom_topic.strip():
        translated = _translate_topic(custom_topic)
        hook_candidates = [
            f"If your heart carries a quiet burden for {translated} today...",
            f"Tonight, as you pray for {translated}, know that God hears you.",
            f"When you are trusting God through {translated}, take heart.",
            f"Before worry regarding {translated} steals your peace tonight..."
        ]

    # Obtener el último gancho registrado para no repetirlo consecutivamente
    recent_records = history_mgr.load_history()
    last_hook = recent_records[-1].get("hook", "") if recent_records else ""

    chosen_hook = None
    for h in random.sample(hook_candidates, len(hook_candidates)):
        is_sim, _ = history_mgr.is_similar_to_recent(h, threshold=0.70)
        if not is_sim:
            chosen_hook = h
            break

    # Si todos los candidatos están en el historial reciente, elegir uno diferente al último registrado
    if not chosen_hook:
        different_candidates = [h for h in hook_candidates if h.strip() != last_hook.strip()]
        chosen_hook = random.choice(different_candidates) if different_candidates else random.choice(hook_candidates)

    # 2. Perspectiva / Desarrollo (Body)
    perspectives = theme.get("perspectives", {})
    available_perspectives = list(perspectives.keys())
    chosen_perspective_key = tone if (tone in available_perspectives) else random.choice(available_perspectives or ["prayer"])
    base_body = perspectives.get(chosen_perspective_key, perspectives.get("prayer", "Lord, cover our home in Your gentle peace."))

    # Adaptar cuerpo según tema personalizado
    if custom_topic and custom_topic.strip():
        topic_phrase = _translate_topic(custom_topic)
        body = f"{base_body} Specifically, Lord, we bring {topic_phrase} into Your loving hands, trusting Your unfailing care."
    else:
        body = base_body

    # 3. Cierre (Closing)
    closings = theme.get("closings", ["May His peace guard your heart and mind tonight."])
    closing = random.choice(closings)

    # 4. CTA Opcional
    ctas = theme.get("ctas", ["May your heart find quiet rest tonight in His hands."])
    cta = random.choice(ctas)

    if seamless_loop and cta:
        loop_bridges = [
            "And always remember that...",
            "Before you close your eyes in sleep tonight, remember that...",
            "Hold onto this promise tonight, and remember that...",
            "As scripture quietly declares..."
        ]
        chosen_bridge = random.choice(loop_bridges)
        cta = f"{cta.rstrip('.! ')} — {chosen_bridge}"

    # Ajuste de duración según modo
    if mode == "micro":
        # Formato corto (~30 palabras)
        sentences = [s.strip() for s in body.split(".") if s.strip()]
        body_short = f"{sentences[0]}." if sentences else body
        full_text = f"{chosen_hook} {body_short} {cta}".strip()
        body_export = body_short
    elif mode == "story":
        # Formato más largo y reflexivo (~70 palabras)
        full_text = f"{chosen_hook} {body} {closing} {cta}".strip()
        body_export = f"{body} {closing}".strip()
    else:  # deep (estándar 18-25s, ~50 palabras)
        full_text = f"{chosen_hook} {body} {closing} {cta}".strip()
        body_export = f"{body} {closing}".strip()

    word_count = len(full_text.split())
    # 2.15 palabras por segundo para locución natural y pausada
    estimated_duration_sec = round(max(15.0, (word_count / 2.15) + 1.2), 1)

    scripture = BIBLICAL_CATALOGUE.get(chosen_key, theme.get("scripture", "Philippians 4:6 — Present your requests to God with thanksgiving."))
    hashtags = theme.get("hashtags", ["#DailyPrayer", "#FaithInGod", "#ChristianLiving"])
    seo_caption = generate_seo_caption(theme["title"], full_text, scripture, cta, hashtags)
    prompts_3s = generate_3scene_prompts_for_script(chosen_key, full_text, custom_topic)

    # Registrar en historial para rotación
    history_mgr.record_script(
        theme_key=chosen_key,
        hook=chosen_hook,
        body=body_export,
        cta=cta,
        scene_prompts=[prompts_3s["scene_1_prompt"], prompts_3s["scene_2_prompt"], prompts_3s["scene_3_prompt"]]
    )

    return {
        "theme_key": chosen_key,
        "theme_title_es": theme["title"],
        "thematic_pillar": theme.get("pillar", "spiritual_growth"),
        "human_situation": human_sit,
        "central_idea": central_idea,
        "hook": chosen_hook,
        "body": body_export,
        "closing": closing,
        "cta": cta,
        "full_text": full_text,
        "word_count": word_count,
        "target_duration_sec": 22.0,
        "estimated_duration_sec": estimated_duration_sec,
        "mode": mode,
        "seamless_loop": seamless_loop,
        "tone": chosen_perspective_key,
        "perspective": chosen_perspective_key,
        "hook_badge_text": theme.get("hook_badge_text", "PRAYER OF FAITH"),
        "micro_cta_text": cta,
        "scripture": scripture,
        "pinned_comment": f"May this prayer bring comfort: \"{closing}\" 🙏",
        "seo_caption": seo_caption,
        "hashtags": hashtags,
        "scene_1_prompt": prompts_3s["scene_1_prompt"],
        "scene_2_prompt": prompts_3s["scene_2_prompt"],
        "scene_3_prompt": prompts_3s["scene_3_prompt"],
        "image_prompt": prompts_3s["prompt"],
        "provider_used": "template"
    }


# ─── Fachada Pública Principal ──────────────────────────────────────────────

def generate_script(
    theme_key: Optional[str] = None,
    custom_topic: Optional[str] = None,
    mode: str = "deep",
    tone: Optional[str] = None,
    seamless_loop: bool = False
) -> Dict[str, Any]:
    """Punto de entrada principal. Delega en el proveedor activo (Ollama / Template / Auto)."""
    from engine.script_provider import get_script_provider
    provider = get_script_provider()
    script_result = provider.generate(
        theme_key=theme_key,
        custom_topic=custom_topic,
        mode=mode,
        tone=tone,
        seamless_loop=seamless_loop
    )
    return script_result.model_dump()


def generate_image_prompt_for_script(theme_key: Optional[str], script_text: str = "") -> str:
    """Retorna el prompt de la escena 1 para compatibilidad."""
    prompts = generate_3scene_prompts_for_script(theme_key, script_text)
    return prompts["prompt"]


def get_themes_list() -> List[Dict]:
    """Retorna los 26 temas disponibles con su pilar temático."""
    return [
        {
            "key": k,
            "title": v["title"],
            "description": v["description"],
            "pillar": v.get("pillar", "general")
        }
        for k, v in VIRAL_THEMES.items()
    ]


def get_card_template_for_theme(theme_key: str) -> Dict[str, str]:
    """Plantilla para tarjetas devocionales 4:5 de Feed."""
    chosen_key = theme_key if (theme_key and theme_key in VIRAL_THEMES) else "lost_child"
    theme = VIRAL_THEMES[chosen_key]

    raw_title = theme.get("hook_badge_text", "PRAYER OF FAITH")
    perspectives = theme.get("perspectives", {})
    body = perspectives.get("prayer", perspectives.get("heart_comfort", "Lord, place a hedge of protection around my home."))
    closing = theme.get("closings", ["May His peace rest upon you."])[0]
    devotional_prayer = f"{body} {closing}".strip()

    scripture = BIBLICAL_CATALOGUE.get(chosen_key, theme.get("scripture", "Philippians 4:19 — And my God will supply every need of yours."))
    hashtags = theme.get("hashtags", ["#DailyPrayer", "#FaithInGod", "#ChristianLiving"])
    rec_img = theme.get("recommended_image", "jesus_healing_miracle.jpg")

    feed_copy = f"""✝️ {raw_title} ✝️

"{devotional_prayer}"

📖 {scripture}

🕊️ Take a quiet breath and rest in God's peace today.

{" ".join(hashtags[:4])}"""

    ai_prompt = generate_3scene_prompts_for_script(chosen_key, devotional_prayer)["scene_1_prompt"].replace("--ar 9:16", "--ar 4:5")

    return {
        "theme_key": chosen_key,
        "theme_title_es": theme["title"],
        "title_english": raw_title,
        "prayer_english": devotional_prayer,
        "scripture": scripture,
        "recommended_image": rec_img,
        "image_prompt": ai_prompt,
        "feed_copy": feed_copy,
        "pinned_comment": f"May this prayer bless your home: \"{closing}\" 🙏"
    }


def get_daily_batch_schedule() -> List[Dict]:
    """
    Planificador de lote diario rotativo:
    Selecciona 3 temas rotando entre diferentes pilares temáticos para no repetir siempre los mismos 3.
    """
    history_mgr = get_history_manager()
    recent = history_mgr.get_recent_theme_keys(count=6)

    # Pilar Mañana: Paz o Gratitud
    morning_candidates = [t for t in THEMATIC_PILLARS["peace_rest_daily"]["themes"] + THEMATIC_PILLARS["gratitude_wisdom_growth"]["themes"] if t not in recent]
    morning_theme = random.choice(morning_candidates) if morning_candidates else "morning_favor"

    # Pilar Mediodía: Fe y Pruebas o Duelo
    midday_candidates = [t for t in THEMATIC_PILLARS["faith_hope_trials"]["themes"] + THEMATIC_PILLARS["grief_solitude_comfort"]["themes"] if t not in recent and t != morning_theme]
    midday_theme = random.choice(midday_candidates) if midday_candidates else "strength_weary"

    # Pilar Noche: Familia o Descanso
    night_candidates = [t for t in THEMATIC_PILLARS["family_relationships"]["themes"] + THEMATIC_PILLARS["peace_rest_daily"]["themes"] if t not in recent and t not in [morning_theme, midday_theme]]
    night_theme = random.choice(night_candidates) if night_candidates else "night_anxiety"

    return [
        {
            "slot": "morning",
            "time_label": "🌅 Mañana (7:00 AM - 8:30 AM EST)",
            "purpose": "Apertura del Día, Sabiduría y Gratitud",
            "theme_key": morning_theme,
            "script": generate_script(morning_theme, mode="deep"),
            "recommended_image": "jesus_holy_bible.jpg",
            "recommended_image_2": "jesus_praying_gethsemane.jpg",
            "recommended_image_3": "jesus_reaching_hand.jpg",
            "recommended_music": "celestial_strings_hope"
        },
        {
            "slot": "midday",
            "time_label": "☀️ Mediodía (12:30 PM - 2:00 PM EST)",
            "purpose": "Fortaleza en Medio de Pruebas y Trabajo",
            "theme_key": midday_theme,
            "script": generate_script(midday_theme, mode="deep"),
            "recommended_image": "jesus_healing_miracle.jpg",
            "recommended_image_2": "jesus_comforting_embrace.jpg",
            "recommended_image_3": "holy_cross_calvary.jpg",
            "recommended_music": "worship_piano_peace"
        },
        {
            "slot": "night",
            "time_label": "🌙 Noche (8:30 PM - 10:00 PM EST)",
            "purpose": "Protección Familiar y Descanso Reparador",
            "theme_key": night_theme,
            "script": generate_script(night_theme, mode="deep"),
            "recommended_image": "jesus_praying_gethsemane.jpg",
            "recommended_image_2": "holy_cross_calvary.jpg",
            "recommended_image_3": "jesus_comforting_embrace.jpg",
            "recommended_music": "midnight_prayer_acoustic"
        }
    ]
