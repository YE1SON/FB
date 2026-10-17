import random
import re
from typing import Dict, List, Optional

# =============================================================================
# JESUS REELS STUDIO v4.0 - ADVANCED NARRATIVE SCRIPT GENERATOR
# =============================================================================
# 26 Temas Espirituales y Emocionales con Variaciones Narrativas Reales:
# - Estructura Narrativa de 4 Partes: Gancho -> Reflexión/Oración -> Cierre -> CTA
# - 4 Tonos Emocionales: Intimate, Hopeful, Reflective, Narrative
# - 3 Modos de Duración: Micro (15-20s), Deep (25-35s), Story (40-50s)
# - Soporte Activo de Tema Personalizado (Español e Inglés)
# - Libre de promesas médicas falsas o cebo de comentarios forzado.
# =============================================================================

CUSTOM_TOPIC_TRANSLATIONS = {
    "hijo": "a child wandering far from peace",
    "hijos": "our children and the next generation",
    "hija": "a beloved daughter needing guidance",
    "nieto": "a precious grandchild",
    "nietos": "our grandchildren's future and protection",
    "familia": "restoring peace and unity within a family",
    "deuda": "the heavy pressure of unpaid bills and financial strain",
    "deudas": "financial struggle and breaking through debt",
    "dinero": "financial provision and stability for the home",
    "trabajo": "finding an honest job and an open door",
    "empleo": "career direction and breakthrough in employment",
    "negocio": "blessing and integrity in a small business",
    "salud": "physical weariness, illness, and body healing",
    "enfermedad": "facing illness and finding strength in God",
    "cancer": "walking through a frightening medical trial with faith",
    "dolor": "chronic pain and finding daily endurance",
    "ansiedad": "overwhelming anxiety, racing thoughts, and panic",
    "panico": "calming panic attacks in the quiet of the night",
    "insomnio": "sleepless nights and restoring sweet peace to the mind",
    "soledad": "deep loneliness and knowing God has not abandoned you",
    "depresion": "silent emotional heaviness and finding light in darkness",
    "matrimonio": "healing a strained marriage and rebuilding trust",
    "pareja": "reconciliation, patience, and love between partners",
    "divorcio": "healing a broken heart after painful separation",
    "duelo": "grieving the loss of someone dearly missed",
    "luto": "comforting a soul walking through bereavement",
    "perdon": "letting go of resentment and forgiving past wounds",
    "adiccion": "breaking chains of habit, dependency, and addiction",
    "juicio": "fairness, truth, and peace in legal battles",
    "abuela": "comfort and strength for an aging grandmother",
    "abuelo": "health and honoring an aging grandfather",
    "padres": "peace, health, and blessing over aging parents",
    "madre soltera": "sustaining grace and provision for a single mother",
    "padre soltero": "daily strength and wisdom for a single father",
    "fuerza": "renewed strength when completely exhausted",
    "fe": "strengthening faint faith in a quiet season",
    "paz": "the peace of God that surpasses all human understanding"
}

VIRAL_THEMES: Dict[str, Dict] = {
    "lost_child": {
        "title": "🚶‍♂️ Por el hijo/hija que se alejó de Dios",
        "description": "Oración intercesora por un hijo, hija o ser querido que atraviesa rebeldía o dolor.",
        "target_time_slot": "night",
        "hook_badge_text": "PRAYER FOR YOUR CHILDREN",
        "recommended_image": "jesus_reaching_hand.jpg",
        "scripture": "Luke 15:20 — While he was still a long way off, his father saw him and was filled with compassion.",
        "hashtags": ["#PrayingParents", "#FaithInGod", "#ChristianFamily", "#ProdigalChild", "#DailyPrayer"],
        "hooks": [
            "If your heart aches tonight for a child who feels distant or lost...",
            "Before you close your eyes carrying that quiet worry for your son or daughter...",
            "To every parent who has whispered prayers through tears for their family...",
            "When words don't seem to reach them, remember that God's presence can."
        ],
        "reflections": {
            "intimate": "Lord, You know where my words cannot reach. Wrap Your unseen arms around my child tonight. Quiet their silent struggles, protect their path from unseen harm, and remind them that they are forever loved.",
            "hopeful": "Father, no distance is too far for Your grace. Lead their wandering steps toward safety, surround them with wise voices, and let them feel the warmth of Your steady mercy guiding them back home.",
            "reflective": "We often carry the weight of those we love in silence. But what we cannot control, God can gently restore. Trust that every heartfelt prayer planted in faith continues to watch over their steps.",
            "narrative": "A father once stood at the edge of the road, looking out every evening, waiting for his child. God looks upon your family with that same unwavering love, keeping watch even in the dark."
        },
        "closings": [
            "May God's peace guard their mind and yours tonight.",
            "Rest in the assurance that God watches over those you love.",
            "Tomorrow carries fresh mercy; trust their tomorrow into His hands.",
            "His love is pursuing them even when you cannot see it."
        ],
        "ctas": [
            "If this spoke to your heart, take a quiet breath and rest in Him tonight.",
            "Keep their name lifted in faith; love never gives up.",
            "Share this quiet prayer with a parent who might need hope today.",
            "Whisper Amen if you trust God with your family's future."
        ],
        "pinned_comments": [
            "What is the first name of the child or loved one you are lifting in prayer tonight? We stand with you in faith. 🙏",
            "No prayer for our children is ever wasted. Drop a heart ❤️ if you are trusting God for your family today.",
            "I am joining my faith with every mother and father here tonight. You are not praying alone."
        ]
    },

    "family_protection": {
        "title": "🛡️ Protección y Paz sobre tu Hogar y Familia",
        "description": "Cobertura de paz y resguardo sobre tu casa, tus seres queridos y tu descanso.",
        "target_time_slot": "night",
        "hook_badge_text": "PROTECTION OVER YOUR HOME",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": "Psalm 91:11 — He will command his angels concerning you to guard you in all your ways.",
        "hashtags": ["#FamilyPrayer", "#Psalm91", "#PeaceInTheHome", "#ChristianLiving", "#NightPrayer"],
        "hooks": [
            "Tonight, let peace settle inside the walls of your home.",
            "If the world felt heavy today, step into the safety of God's presence.",
            "Before you turn off the lights, invite the peace of Christ into every room.",
            "Your home is meant to be a sanctuary of rest and comfort tonight."
        ],
        "reflections": {
            "intimate": "Father, place a gentle shield of peace over this household. Guard our door from discord, silence every anxious thought upon our pillows, and fill our rooms with Your calming presence.",
            "hopeful": "Lord, we dedicate our home to You. May Your angels stand watch over every window, bless our going out and our coming in, and keep our loved ones safe beneath Your wings.",
            "reflective": "Safety is not the absence of storms outside, but the presence of Christ inside. When you place your family in God's hands, fear loses its grip on your home.",
            "narrative": "In ancient times, homes covered in faith were safe through the darkest nights. That same covenant of grace surrounds your loved ones today."
        },
        "closings": [
            "May your sleep be deep and your household sheltered in grace.",
            "Rest easy knowing God neither slumbers nor sleeps.",
            "His presence is the strongest wall around your family.",
            "Peace be upon this house, and upon all who dwell within."
        ],
        "ctas": [
            "Whisper Amen and claim this shelter of peace over your home.",
            "Share this blessing with someone whose family is on your heart.",
            "Take a deep breath and let go of today's burdens.",
            "May your heart find rest tonight under His protection."
        ],
        "pinned_comments": [
            "Drop your family's initial below so we can speak a prayer of protection over your household tonight! 🕊️",
            "May God's peace fill every corner of your home tonight. Type 'AMEN' in faith.",
            "Who in your family needs extra comfort and peace tonight? We are lifting them up with you."
        ]
    },

    "medical_fear": {
        "title": "🩺 Fortaleza en Momentos de Enfermedad o Dolor",
        "description": "Consuelo, serenidad y fortaleza divina para quienes enfrentan diagnósticos o debilidad física.",
        "target_time_slot": "midday",
        "hook_badge_text": "STRENGTH IN WEAKNESS",
        "recommended_image": "jesus_healing_miracle.jpg",
        "scripture": "2 Corinthians 12:9 — My grace is sufficient for you, for my power is made perfect in weakness.",
        "hashtags": ["#HealingGrace", "#FaithOverFear", "#ComfortInChrist", "#JesusHeals", "#DailyStrength"],
        "hooks": [
            "If your body feels weary and medical worries are clouding your mind...",
            "When health challenges make tomorrow feel uncertain and heavy...",
            "To anyone sitting in a quiet room waiting on news or managing pain...",
            "Take heart today: your strength is sustained by a compassionate God."
        ],
        "reflections": {
            "intimate": "Jesus, You walked among the hurting with gentle hands. Touch the places in this body that feel weak and exhausted. Grant wisdom to the doctors, peace to this heart, and renewed endurance for each new morning.",
            "hopeful": "Father, breathe new life into every tired breath. When medicine feels limited, Your comfort has no boundaries. Strengthen this spirit, calm every fear, and let healing peace flow from head to toe.",
            "reflective": "Facing physical weakness teaches us that we do not walk alone. Even in moments of pain, Christ draws near, offering grace that carries us through one hour at a time.",
            "narrative": "A woman once reached through a pressing crowd just to touch the hem of His garment, and found immediate peace. Reach out in quiet faith today; He is listening."
        },
        "closings": [
            "May His healing peace sustain you in body, mind, and spirit.",
            "You are held securely in hands that never fail.",
            "One day at a time, His grace is more than enough.",
            "May comfort meet you in this very moment."
        ],
        "ctas": [
            "If your body needs strength today, whisper Amen and receive His comfort.",
            "Send this quiet prayer to someone in your life walking through a health trial.",
            "Breathe in His peace; exhale the fear of the unknown.",
            "Keep holding onto faith; you are not fighting this battle alone."
        ],
        "pinned_comments": [
            "If you or a loved one is facing health challenges, drop a first name below so we can lift you in prayer. 🕊️",
            "God sees every tear shed in quiet waiting rooms. Type 'LORD STRENGTHEN ME' if you receive this today.",
            "Standing in agreement for peace, endurance, and restoration for everyone hurting here today."
        ]
    },

    "zero_balance": {
        "title": "💸 Provisión, Paz y Alivio en Momentos de Escasez",
        "description": "Fe, sabiduría y confianza en la provisión de Dios ante deudas y presiones económicas.",
        "target_time_slot": "midday",
        "hook_badge_text": "GOD OUR PROVIDER",
        "recommended_image": "jesus_holy_bible.jpg",
        "scripture": "Philippians 4:19 — And my God will meet all your needs according to the riches of his glory in Christ Jesus.",
        "hashtags": ["#GodProvides", "#FaithOverWorry", "#FinancialPeace", "#ChristianLiving", "#JehovahJireh"],
        "hooks": [
            "If you opened your bills today feeling that tight knot of worry in your chest...",
            "When the numbers don't add up and you wonder how you'll make it through...",
            "Before you let financial stress rob you of your peace tonight...",
            "Remember that your worth and your tomorrow are never defined by a bank balance."
        ],
        "reflections": {
            "intimate": "Lord, You know the quiet stress of unpaid debts and honest obligations. Open honorable doors of provision, grant wisdom for every decision, and replace anxiety with the steady assurance that You care for this family.",
            "hopeful": "Father, You feed the birds of the air and clothe the fields with beauty. We trust You for breakthrough, unexpected favor, and the dignity of having our needs met through Your faithful hands.",
            "reflective": "Financial pressure can feel like a heavy cage, but worry never paid a single bill. Place your honest labor into God's hands and watch how He creates a path where there seemed to be none.",
            "narrative": "A widow once had nothing left in her house except a single jar of oil, yet God multiplied it until every vessel was full. He is the same God of provision today."
        },
        "closings": [
            "May unexpected blessings meet you before this week ends.",
            "Rest in the truth that God provides for His children.",
            "Hold your head up high; help is closer than you think.",
            "His faithfulness has brought you this far, and He will not leave you now."
        ],
        "ctas": [
            "Whisper Amen if you trust God to provide for your home.",
            "Share this encouragement with a family working hard to get ahead.",
            "Take heart today; God sees your hard work and your integrity.",
            "Drop your worries at His feet and rest tonight."
        ],
        "pinned_comments": [
            "If you are trusting God for a breakthrough in your finances, type 'GOD WILL PROVIDE' below! 💸",
            "We are praying for open doors, wisdom, and provision for every working family here.",
            "Drop a 🙏 if you believe God is preparing a way forward for you right now."
        ]
    },

    "night_anxiety": {
        "title": "🌌 Ansiedad a las 3 AM (Insomnio y Ataques de Pánico)",
        "description": "Paz sobrenatural para mentes saturadas de miedo, pensamientos intrusivos y desvelo.",
        "target_time_slot": "night",
        "hook_badge_text": "PEACE IN THE NIGHT",
        "recommended_image": "jesus_praying_gethsemane.jpg",
        "scripture": "Psalm 4:8 — In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.",
        "hashtags": ["#NightPrayer", "#PeaceOfMind", "#OvercomingAnxiety", "#SleepInPeace", "#ChristianCalm"],
        "hooks": [
            "If you are wide awake at 3 AM with racing thoughts that won't quiet down...",
            "Tonight, when the house is still but your mind is running in circles...",
            "To the tired soul staring at the ceiling, feeling overwhelmed by tomorrow...",
            "Breathe slowly right now. You are safe in the hands of Jesus."
        ],
        "reflections": {
            "intimate": "Jesus, step into this quiet room. Calm the storm within this chest, silence the racing fears of tomorrow, and blanket this tired mind in heavenly stillness until the dawn arrives.",
            "hopeful": "Father, You give Your beloved sleep. Dispel the shadows of anxiety, remind this heart that tomorrow is already in Your care, and grant sweet, unbroken rest to every tired muscle.",
            "reflective": "Nighttime often magnifies our fears, making small shadows feel like giants. But God's presence is closer than the rhythm of your breath. Let go of what you cannot solve tonight.",
            "narrative": "In the middle of a midnight gale on the Sea of Galilee, Jesus stood up and whispered: 'Peace, be still.' That same voice speaks over your restless thoughts right now."
        },
        "closings": [
            "Sleep peacefully; God is keeping watch through the night.",
            "May quietness and confidence be your strength until morning.",
            "Every racing thought bows to the quiet peace of Christ.",
            "You are sheltered, you are safe, and you are deeply loved."
        ],
        "ctas": [
            "Close your eyes, breathe gently, and whisper Amen.",
            "Save this quiet prayer for whenever nighttime feels overwhelming.",
            "Share this with a friend who struggles with sleep or anxiety.",
            "Rest tonight; morning will bring brand new grace."
        ],
        "pinned_comments": [
            "If anxiety woke you up tonight, leave a '🙏' below and let us stand with you in prayer right now.",
            "You are not fighting this dark hour alone. Drop your first name and we will pray for your peace.",
            "Breathe in God's peace. Type 'AMEN' and let your heart rest."
        ]
    },

    "morning_favor": {
        "title": "🌅 Bendición y Favor de la Mañana",
        "description": "Comenzar el día coronado de gracia, sabiduría, enfoque y puertas abiertas.",
        "target_time_slot": "morning",
        "hook_badge_text": "MORNING BLESSING & FAVOR",
        "recommended_image": "jesus_holy_bible.jpg",
        "scripture": "Lamentations 3:22-23 — His mercies never come to an end; they are new every morning.",
        "hashtags": ["#MorningPrayer", "#DailyDevotional", "#NewMercies", "#GodsFavor", "#BlessedDay"],
        "hooks": [
            "As this new day begins, start it anchored in the goodness of God.",
            "Before you check your phone or rush into your morning tasks...",
            "This sunrise brings a clean slate and fresh mercy just for you.",
            "May your footsteps today be guided by divine wisdom and peace."
        ],
        "reflections": {
            "intimate": "Heavenly Father, thank You for the gift of breath this morning. Guide my words, order my steps, and let Your kindness shine through me to everyone I meet today.",
            "hopeful": "Lord, we step into today expecting Your favor. Open doors that need to be opened, close doors that lead to harm, and grant us courage to walk in faith and joy.",
            "reflective": "Yesterday's mistakes belong to the past; today is wrapped in fresh grace. Walk forward with quiet confidence, knowing that God goes before you into every situation.",
            "narrative": "Every morning, the sun faithfully rises without hesitation. In that same dependable way, God's faithfulness greets you at the dawn of this day."
        },
        "closings": [
            "Walk boldly today; the Lord is on your side.",
            "May your day be filled with unexpected joy and light.",
            "His grace will sustain you through every hour ahead.",
            "Go in peace, knowing you are blessed and favored."
        ],
        "ctas": [
            "Type Amen to receive this morning blessing over your day.",
            "Send this sunrise prayer to someone you cherish today.",
            "Step forward with faith; God is making a way for you.",
            "Dedicate your morning to Him and watch how He leads."
        ],
        "pinned_comments": [
            "Claim your morning blessing before stepping out! Type 'I RECEIVE IT' and have a blessed day! 🌅",
            "What is one thing you are thanking God for this morning? Let's start the day with gratitude! 🙌",
            "Lifting up everyone heading out to work or school today. May God bless your hands and mind."
        ]
    },

    "marriage_healing": {
        "title": "💍 Restauración y Paciencia en el Matrimonio",
        "description": "Reconciliación, superación de amarguras y reencuentro del amor y el respeto mutuo.",
        "target_time_slot": "night",
        "hook_badge_text": "HEALING IN MARRIAGE",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": "1 Corinthians 13:7 — Love bears all things, believes all things, hopes all things, endures all things.",
        "hashtags": ["#MarriagePrayer", "#ChristianMarriage", "#LoveAndRespect", "#RestorationInGod", "#DailyFaith"],
        "hooks": [
            "If silence and frustration have built walls inside your marriage...",
            "When words were spoken in anger and you miss the warmth you once shared...",
            "To every couple fighting silent battles to keep their covenant strong...",
            "Love isn't the absence of conflict; it's the willingness to forgive and heal."
        ],
        "reflections": {
            "intimate": "Lord, soften the hardened places in our hearts. Replace bitterness with understanding, heal quiet wounds, and rekindle the tender love and patience that first brought us together.",
            "hopeful": "Father, what was fractured by misunderstandings can be rebuilt with Your grace. Teach us to listen with compassion, to speak with kindness, and to stand united against every challenge.",
            "reflective": "A lasting marriage is made of two imperfect people choosing grace day after day. When you invite Christ into your conversation, pride gives way to genuine restoration.",
            "narrative": "A three-strand cord is not easily broken. When God is the center strand of your home, no storm is strong enough to tear your bond apart."
        },
        "closings": [
            "May peace and gentleness return to your home tonight.",
            "Healing takes time; trust God with the process of restoration.",
            "Grace can rebuild what pride almost destroyed.",
            "May your love grow deeper and more patient with each passing day."
        ],
        "ctas": [
            "Whisper Amen and choose grace for your spouse today.",
            "Keep praying for your home; God specializes in restoration.",
            "Share this blessing with a couple walking through a tough season.",
            "Take the first step toward peace with a kind word tonight."
        ],
        "pinned_comments": [
            "Every marriage covered in prayer has hope. Type your initials below so we can pray for your home! ❤️",
            "Standing in agreement for restoration, peace, and mutual love in every home represented here.",
            "Drop a 🙏 if you believe God is capable of healing and renewing your marriage."
        ]
    },

    "healing_depression": {
        "title": "🌧️ Alivio ante la Depresión Silenciosa y el Desánimo",
        "description": "Luz en la oscuridad, compañía divina y renovación del deseo de vivir para el alma abatida.",
        "target_time_slot": "night",
        "hook_badge_text": "LIGHT IN THE SHADOWS",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": "Psalm 34:18 — The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
        "hashtags": ["#HopeInChrist", "#MentalHealthFaith", "#GodHearsYou", "#OvercomingDepression", "#HealingHeart"],
        "hooks": [
            "If smiling feels exhausting and you feel an unseen heaviness inside today...",
            "To the heart that feels hollow and tired of trying to stay strong...",
            "When the world moves fast around you but your soul feels frozen in sadness...",
            "It is okay not to be okay right now; you don't have to carry this alone."
        ],
        "reflections": {
            "intimate": "Jesus, You wept at the graveside and You know the ache of deep sorrow. Draw near to this weary spirit. Lift the dark fog, remind this soul of its infinite value, and whisper that brighter days are ahead.",
            "hopeful": "Father, You are the Lifter of our heads. Breathe fresh purpose into this heart, silence the inner voices of despair, and rekindle the quiet joy of simply being alive in Your love.",
            "reflective": "Depression often whispers that nobody cares, but that is a lie. God counts every quiet tear, and His presence sits beside you in the stillness without judgment.",
            "narrative": "Even the prophet Elijah once sat under a tree and wished he could give up. But God didn't scold him; He sent an angel with food, rest, and a gentle whisper of hope."
        },
        "closings": [
            "You are deeply needed, you are cherished, and your story is not finished.",
            "May light gently break through the clouds of your spirit today.",
            "Hold on through this night; joy comes with the morning light.",
            "God holds you close, exactly as you are right now."
        ],
        "ctas": [
            "Whisper Amen and let yourself rest in His gentle presence.",
            "Send this gentle message to someone who might be struggling in silence.",
            "Take today one single breath at a time; you are not forgotten.",
            "You matter deeply to God; never let the darkness tell you otherwise."
        ],
        "pinned_comments": [
            "If you are carrying a heavy heart today, drop a 🤍 below. We are surrounding you in prayer and love.",
            "Your life has purpose and beauty ahead. Type 'HOLD ON' as a reminder for your spirit today.",
            "You are loved beyond measure. Never walk through dark valleys alone."
        ]
    },

    "job_breakthrough": {
        "title": "🚪 Puertas Abiertas para Desempleo y Trabajo",
        "description": "Dignidad, provisión y nuevas oportunidades laborales para quien busca sustento.",
        "target_time_slot": "morning",
        "hook_badge_text": "CAREER & JOB FAVOR",
        "recommended_image": "jesus_holy_bible.jpg",
        "scripture": "Revelation 3:8 — See, I have placed before you an open door that no one can shut.",
        "hashtags": ["#JobSearchFaith", "#OpenDoors", "#GodsProvision", "#CareerBreakthrough", "#BlessedWork"],
        "hooks": [
            "If you've sent application after application and silence is all you've received...",
            "When closed doors make you question your worth and your future...",
            "Before you walk into that interview or send another resume today...",
            "Remember: man's rejection is often God's redirection to something better."
        ],
        "reflections": {
            "intimate": "Lord, You see the honest desire of this heart to work, provide, and serve. Open the right doors that no human can shut, connect this person with people of integrity, and renew their confidence today.",
            "hopeful": "Father, grant divine favor in every interview and application. Let their skills shine, provide a workplace of dignity and peace, and supply every need according to Your riches.",
            "reflective": "Waiting on a job can test our patience, but seasons of preparation are never wasted. Trust that God is preparing an opportunity that aligns with your gifts.",
            "narrative": "Joseph went from a forgotten prison cell to leading a nation's resources in a single day. God can change your circumstances in moments you never anticipated."
        },
        "closings": [
            "The right door will open at the exact right moment.",
            "Walk into today with your head held high and your faith steady.",
            "Your gifts will make room for you in due season.",
            "May favor go before you and peace follow behind you."
        ],
        "ctas": [
            "Type Amen and claim an open door of opportunity today.",
            "Share this encouragement with someone seeking employment right now.",
            "Keep applying, keep preparing, and keep trusting His timing.",
            "May your hard work be rewarded with honor and peace."
        ],
        "pinned_comments": [
            "Drop your field of work or first name below! We are agreeing with you for an open door this week. 💼",
            "What kind of job are you praying for? Type it below so our community can stand with you!",
            "God knows your needs before you ask. Type 'AMEN' in faith for new employment."
        ]
    },

    "lonely_widow": {
        "title": "🕊️ Consuelo para Quien Atraviesa Soledad o Duelo",
        "description": "Amor entrañable, compañía divina y fortaleza para viudas, viudos y almas solitarias.",
        "target_time_slot": "night",
        "hook_badge_text": "COMFORT IN LONELINESS",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": "Psalm 68:5 — A father to the fatherless, a defender of widows, is God in his holy dwelling.",
        "hashtags": ["#ComfortInGrief", "#NeverAlone", "#GodOurComfort", "#PeaceInSolitude", "#ChristianFaith"],
        "hooks": [
            "If the silence in your home feels louder and heavier tonight...",
            "When an empty chair or a quiet hallway brings back memories and tears...",
            "To the precious soul feeling overlooked or forgotten by the world...",
            "God sees you in your solitude, and you are precious in His sight."
        ],
        "reflections": {
            "intimate": "Jesus, sit beside this dear soul tonight. In the quiet hours when loneliness aches the most, fill this room with Your comforting presence and wrap this heart in tender love.",
            "hopeful": "Father, You are the defender of the lonely and the faithful companion of the brokenhearted. Send caring community, bring warm memories that bring smiles, and give strength for each new sunrise.",
            "reflective": "Being alone in a room does not mean being abandoned by God. His spirit fills the empty spaces with a warmth and assurance that no earthly voice can match.",
            "narrative": "Ruth and Naomi walked through deep loss together, yet God wrote a story of redemption and family that blessed generations. He is writing your story of hope even now."
        },
        "closings": [
            "You are never truly alone; Christ walks with you through every room.",
            "May sweet memories bring peace and comfort to your soul tonight.",
            "His love is an anchor that holds through every quiet season.",
            "Rest gently in the knowledge that you are cherished by God."
        ],
        "ctas": [
            "Whisper Amen and let His comfort rest upon your shoulders.",
            "Send this gentle prayer to someone who lives alone or lost a spouse.",
            "Take comfort tonight; your life continues to have value and beauty.",
            "May tomorrow bring a reminder that you are loved."
        ],
        "pinned_comments": [
            "Sending a warm hug and heartfelt prayers to anyone feeling lonely tonight. Leave a ❤️ below.",
            "You are not forgotten by God or by this community. We are holding you in prayer tonight.",
            "Drop a 🙏 if you are asking God for peace and comfort in a quiet house tonight."
        ]
    },

    "addiction_chains": {
        "title": "⛓️ Rompimiento de Hábitos Ocultos y Cadenas",
        "description": "Fuerza, sobriedad y libertad en Cristo para vencer patrones destructivos y dependencias.",
        "target_time_slot": "night",
        "hook_badge_text": "FREEDOM & SOBRIETY",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": "John 8:36 — If the Son sets you free, you will be free indeed.",
        "hashtags": ["#FreedomInChrist", "#BreakingChains", "#RecoveryFaith", "#SobrietyThroughGrace", "#DailyOvercoming"],
        "hooks": [
            "If you are fighting a quiet habit that leaves you feeling guilty and trapped...",
            "When you promised yourself you wouldn't fall again, but stumbled today...",
            "To anyone carrying a secret battle they are ashamed to admit to others...",
            "Condemnation will not heal you, but the grace of Christ can set you free."
        ],
        "reflections": {
            "intimate": "Lord, You see the struggle behind closed doors. Break the power of cravings, heal the underlying pain driving this habit, and grant the courage to reach out for help and walk in light.",
            "hopeful": "Father, where sin and weakness abounded, Your grace abounds all the more. Strengthen this resolve, provide trustworthy accountability, and restore self-control and clear peace to this mind.",
            "reflective": "Recovery is won one day, one prayer, and one choice at a time. Do not let one stumble define your journey; get back up, for the righteous fall seven times and rise again.",
            "narrative": "Peter once denied knowing Jesus in a moment of fear, yet Christ met him on the shore, restored his dignity, and called him to lead. Your past does not disqualify your future."
        },
        "closings": [
            "Stand strong; freedom is a journey of grace step by step.",
            "His power is made perfect in your moments of deepest weakness.",
            "You are not a captive to your past; tomorrow is a fresh start.",
            "May His strength be your shield when temptations arise."
        ],
        "ctas": [
            "Type Amen if you are choosing to walk toward freedom today.",
            "Share this with someone fighting a quiet battle for their life.",
            "Take courage; tomorrow morning is a clean page waiting for you.",
            "Keep standing; victory belongs to those who never stop getting back up."
        ],
        "pinned_comments": [
            "Drop a 'FREEDOM' below if you are choosing to take one step toward recovery and grace today! 🕊️",
            "No judgment here, only prayer and support. Drop your initial so we can pray for your strength.",
            "One day at a time, through Christ who strengthens us. Type AMEN in faith."
        ]
    },

    "elderly_parents": {
        "title": "👵 Bendición y Cuidado de Padres Ancianos",
        "description": "Gratitud, salud y protección sobre nuestros padres y abuelos en sus años dorados.",
        "target_time_slot": "morning",
        "hook_badge_text": "HONORING AGING PARENTS",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": "Isaiah 46:4 — Even to your old age and gray hairs I am he, I am he who will sustain you.",
        "hashtags": ["#AgingParents", "#HonoringFamily", "#EldersBlessing", "#FaithfulGod", "#DailyPrayer"],
        "hooks": [
            "To every son and daughter watching their parents grow fragile with age...",
            "If you cherish the hands that once held yours when you were small...",
            "Take a moment today to cover your aging mother or father in prayer...",
            "Those who gave us our foundation deserve our gentlest love and honor."
        ],
        "reflections": {
            "intimate": "Lord, preserve the strength, memory, and dignity of our aging parents. Protect their steps from falls, ease their daily aches, and fill their golden years with peace, joy, and loving care.",
            "hopeful": "Father, thank You for the sacrifices they made to raise us. Bless their homes with warmth, surround them with attentive family, and grant us patience and gentleness as we care for them.",
            "reflective": "Aging is a sacred chapter of life. Even when memory fades or footsteps slow down, the soul remains precious and fully seen by God.",
            "narrative": "God promised to carry His people even until gray hairs cover their heads. That same divine faithfulness walks with your parents every single day."
        },
        "closings": [
            "May their days be peaceful and their hearts full of joy.",
            "God's loving hands sustain them through every season.",
            "May they feel honored, valued, and deeply loved today.",
            "Peace and gentle health over your family's elders."
        ],
        "ctas": [
            "Whisper Amen and send a loving message to your parents today.",
            "Share this prayer to honor the fathers and mothers who sacrificed for us.",
            "Call them, hug them, and let them know they are cherished.",
            "May your family be blessed for honoring those who came before."
        ],
        "pinned_comments": [
            "Drop the first name of your parents or grandparents below so we can bless them in prayer today! ❤️",
            "Typing 'HONOR' to celebrate every loving parent and grandparent walking in grace today.",
            "May God protect and comfort our elders across the world today. Type AMEN."
        ]
    },

    "single_parent": {
        "title": "🤱 Fuerza y Provisión para Madres y Padres Solteros",
        "description": "Fuerzas renovadas, sabiduría y sustento para quienes crían a sus hijos sin ayuda.",
        "target_time_slot": "night",
        "hook_badge_text": "STRENGTH FOR SINGLE PARENTS",
        "recommended_image": "jesus_reaching_hand.jpg",
        "scripture": "Isaiah 40:29 — He gives strength to the weary and increases the power of the weak.",
        "hashtags": ["#SingleMomStrong", "#SingleDadFaith", "#ParentingGrace", "#GodProvides", "#DailyPrayer"],
        "hooks": [
            "To the single parent who collapses into bed exhausted after doing it all alone...",
            "When you carry the emotional and financial weight of both roles every single day...",
            "If you ever wonder if you are doing enough for your children...",
            "Take heart: God sees every hidden sacrifice you make with love."
        ],
        "reflections": {
            "intimate": "Father, You see the quiet tears behind closed doors when the kids are asleep. Multiply my energy, provide for every bill, and let my children grow up knowing they are deeply cherished and protected.",
            "hopeful": "Lord, be the co-parent in this home. When my patience wears thin, grant me wisdom; when resources seem small, multiply them; and let peace reign in our living room.",
            "reflective": "Doing the work of two is heavy, but God's strength is made strong in your weariness. Your children will one day look back and call you blessed for your faithful love.",
            "narrative": "Hagar was alone in the desert with her child and ran out of water, but God opened her eyes to a spring of fresh water. He is 'the God who sees you' in every dry season."
        },
        "closings": [
            "You are doing an extraordinary job; do not lose heart.",
            "May tonight bring deep, restful sleep to your tired body.",
            "Your children are blessed because of your faithful love.",
            "God is fighting beside you in every single battle."
        ],
        "ctas": [
            "Whisper Amen and let God carry the weight tonight.",
            "Send this to a single mother or father who deserves encouragement today.",
            "Rest your mind; tomorrow is another day to shine.",
            "You are stronger than you realize through Christ."
        ],
        "pinned_comments": [
            "To every single mom and dad reading this: you are our heroes. Drop a 🤍 so we can cover you in prayer!",
            "You are not raising your family alone; God is in your home. Type 'AMEN' in faith.",
            "Lifting up every single-parent household tonight for peace, wisdom, and abundance."
        ]
    },

    "sick_grandchild": {
        "title": "👶 Oración de Abuelos por la Salud de sus Nietos",
        "description": "Intercesión tierna y amorosa por la salud, protección y bienestar de los nietos.",
        "target_time_slot": "morning",
        "hook_badge_text": "PRAYER FOR GRANDCHILDREN",
        "recommended_image": "jesus_reaching_hand.jpg",
        "scripture": "Proverbs 17:6 — Children’s children are a crown to the aged, and parents are the pride of their children.",
        "hashtags": ["#PrayingGrandparents", "#GrandchildrenBlessing", "#FamilyFaith", "#HealingPrayer", "#DailyFaith"],
        "hooks": [
            "There is no love quite like the tender heart of a praying grandparent...",
            "If your grandchild is on your mind and in your prayers today...",
            "Before you start your day, speak a blessing over the generation to come...",
            "When grandparents pray, heaven listens with tender care."
        ],
        "reflections": {
            "intimate": "Lord Jesus, place Your gentle hands upon my precious grandchildren. Guard their bodies from sickness, protect their innocent hearts from harm, and surround their schools and homes in peace.",
            "hopeful": "Father, let health, wisdom, and joy overflow in their young lives. Guide their steps into purpose, keep them grounded in truth, and let them know the beauty of Your faithful love.",
            "reflective": "The prayers of a grandmother and grandfather create a spiritual canopy that outlives generations. Never underestimate the power of your quiet blessings.",
            "narrative": "Timothy’s sincere faith first lived in his grandmother Lois and his mother Eunice. Your prayers are planting seeds of faith that will flourish for decades to come."
        },
        "closings": [
            "May your grandchildren grow strong, healthy, and blessed.",
            "God's angels are encamped around your family's little ones.",
            "Your prayers are the greatest gift you could ever give them.",
            "Peace and protection upon every child in your family line."
        ],
        "ctas": [
            "Type Amen and send a blessing to your grandchildren today.",
            "Share this with a proud grandmother or grandfather.",
            "Keep speaking life and faith over your family's future.",
            "May your family rejoice in health and laughter together."
        ],
        "pinned_comments": [
            "Grandparents: what are the first names of your grandchildren? We are blessing each one in prayer today! 👶",
            "Type 'GOD BLESS MY GRANDKIDS' to cover them in faith and protection today!",
            "Praying for every grandchild represented here to walk in health, wisdom, and joy."
        ]
    },

    "court_legal": {
        "title": "⚖️ Justicia, Favor y Paz en Procesos Legales",
        "description": "Serenidad, discernimiento y favor divino en trámites judiciales, contratos y audiencias.",
        "target_time_slot": "midday",
        "hook_badge_text": "FAVOR IN LEGAL MATTERS",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": "Psalm 37:5-6 — Commit your way to the Lord; trust in him and he will act: he will bring forth your justice as the light.",
        "hashtags": ["#JusticeInGod", "#LegalFavor", "#FaithOverFear", "#TruthPrevails", "#DailyPrayer"],
        "hooks": [
            "If legal paperwork, hearings, or disputes are causing you sleepless nights...",
            "When you feel powerless against unfair systems or difficult adversaries...",
            "Before you enter that court room or sign those important documents...",
            "Remember that the ultimate Judge of all the earth is committed to truth."
        ],
        "reflections": {
            "intimate": "Lord, You know the truth of my situation. Dispel false accusations, grant wisdom to my counsel, and let honesty and fairness prevail over every paper and proceeding.",
            "hopeful": "Father, grant supernatural favor before judges, mediators, and officials. Settle what was contentious, bring an honorable resolution, and restore peace to my mind and home.",
            "reflective": "Legal battles can feel draining and intimidating, but God is your advocate. Walk with integrity and truth, for truth has a quiet power that outlasts every storm.",
            "narrative": "Daniel stood before envious accusers and unjust decrees, yet God silenced the lions and vindicated his righteousness in the sight of all. He is the same defender today."
        },
        "closings": [
            "May clarity, justice, and peace be granted to you.",
            "God goes before you into every legal meeting and room.",
            "Rest your mind; truth will stand tall in the end.",
            "May a peaceful resolution bring this chapter to a close."
        ],
        "ctas": [
            "Whisper Amen and trust God to advocate for your case.",
            "Share this prayer with someone fighting an exhausting legal battle.",
            "Stand firm in honesty; integrity always wins in the end.",
            "May God grant you peace in the midst of the process."
        ],
        "pinned_comments": [
            "If you have an upcoming court date or legal battle, drop a '⚖️' so we can agree for truth and favor.",
            "Praying for fairness, peace, and victory for everyone facing legal disputes right now. Type AMEN.",
            "God is your defender. Stand in faith and peace today."
        ]
    },

    "restless_sleep": {
        "title": "🛌 Descanso Profundo y Sueño Reparador",
        "description": "Desconexión de preocupaciones del día y descanso tranquilo durante toda la noche.",
        "target_time_slot": "night",
        "hook_badge_text": "DEEP REST & SLEEP",
        "recommended_image": "jesus_praying_gethsemane.jpg",
        "scripture": "Proverbs 3:24 — When you lie down, you will not be afraid; when you lie down, your sleep will be sweet.",
        "hashtags": ["#SweetSleep", "#NightPeace", "#RestInGod", "#SleepWell", "#ChristianNight"],
        "hooks": [
            "Tonight, put down the tasks you couldn't finish today...",
            "Your mind was not created to carry 24 hours of worry without sleep...",
            "Before your head touches the pillow, breathe out every burden...",
            "Sleep is God's gift to human beings; receive it in peace tonight."
        ],
        "reflections": {
            "intimate": "Jesus, quiet my thoughts as the day comes to an end. Release the tension in my shoulders, calm my breathing, and let my heart rest safely in Your constant care.",
            "hopeful": "Father, grant me sweet, deep, and uninterrupted sleep. Recharge my mind, restore my body, and let me wake up with gratitude and clear vision for tomorrow.",
            "reflective": "Trusting God means admitting that the world continues to turn while you sleep. Give Him the controls of your life and let yourself truly rest tonight.",
            "narrative": "Jesus slept peacefully in the back of the boat while the waves were roaring, because His soul was anchored in His Father's love. Rest in that same calm tonight."
        },
        "closings": [
            "May your sleep be peaceful, restorative, and sweet tonight.",
            "Leave tomorrow's cares for tomorrow; tonight is for resting.",
            "You are guarded by the God who never sleeps.",
            "May your morning begin with refreshed energy and peace."
        ],
        "ctas": [
            "Whisper Amen, turn off your screen, and rest peacefully.",
            "Save this quiet bedtime prayer for whenever you need calm.",
            "Share this with someone who has been having trouble sleeping.",
            "Let peace be your blanket tonight."
        ],
        "pinned_comments": [
            "Goodnight and sweet dreams in Jesus. Type 'REST IN PEACE' and sleep well tonight. 🛌",
            "Dropping a prayer of deep sleep and peaceful dreams over everyone here tonight.",
            "May God's angels guard your bedside. Type AMEN and rest."
        ]
    },

    "gratitude_harvest": {
        "title": "🌾 Cosecha de Agradecimiento y Alabanza",
        "description": "Reconocer las bondades cotidianas de Dios y cultivar un corazón lleno de alegría.",
        "target_time_slot": "morning",
        "hook_badge_text": "HEART OF GRATITUDE",
        "recommended_image": "jesus_holy_bible.jpg",
        "scripture": "1 Thessalonians 5:18 — Give thanks in all circumstances; for this is God’s will for you in Christ Jesus.",
        "hashtags": ["#GratitudeDaily", "#ThankYouJesus", "#BlessedAndGrateful", "#PraiseGod", "#JoyfulHeart"],
        "hooks": [
            "What if you woke up today with only the things you thanked God for yesterday?",
            "Gratitude turns what we have into more than enough.",
            "Before complaining about what's missing, let's celebrate what remains.",
            "A thankful heart is the secret to unbroken peace in every season."
        ],
        "reflections": {
            "intimate": "Lord, thank You for the breath in my lungs, the roof over my head, and the simple blessings I so easily overlook. Teach me to see Your goodness in every ordinary moment.",
            "hopeful": "Father, we praise You for doors You opened, trials You brought us through, and the quiet ways You care for our family every single day. Our hearts are full of thanksgiving.",
            "reflective": "Complaining magnifies our problems, but praise magnifies our God. When you shift your gaze to gratitude, joy naturally returns to your heart.",
            "narrative": "Ten lepers were cleansed on the road, but only one returned to fall at Jesus' feet and say thank you. Let us be the one who pauses to say: Thank You, Lord."
        },
        "closings": [
            "May thanksgiving fill your home with light and joy today.",
            "Count your blessings, and you will soon lose count.",
            "A grateful spirit is an unstoppable force of joy.",
            "May your day overflow with smiles and genuine praise."
        ],
        "ctas": [
            "Type 'THANK YOU JESUS' in the comments to praise His name!",
            "Share one blessing you are grateful for today.",
            "Send this gratitude reminder to someone who brings joy to your life.",
            "Celebrate today; life is a precious gift from God."
        ],
        "pinned_comments": [
            "Name ONE thing you are genuinely thankful for today! Let's fill the comments with gratitude! 🙌",
            "Typing 'THANK YOU JESUS' for life, health, and grace today!",
            "Praise turns ordinary days into extraordinary blessings. Amen!"
        ]
    },

    "unspoken_prayer": {
        "title": "🤫 Por la Petición Secreta del Corazón",
        "description": "Oración por aquel anhelo o herida profunda que no le has contado a nadie.",
        "target_time_slot": "night",
        "hook_badge_text": "UNSPOKEN PRAYER",
        "recommended_image": "jesus_praying_gethsemane.jpg",
        "scripture": "Romans 8:26 — The Spirit himself intercedes for us through wordless groans.",
        "hashtags": ["#UnspokenPrayer", "#GodKnowsYourHeart", "#SecretPetitions", "#FaithInTheDark", "#DailyIntercession"],
        "hooks": [
            "This prayer is for the secret burden you haven't told a single soul...",
            "God hears the prayers you are unable to put into words tonight...",
            "For the silent tears cried into a pillow when nobody was looking...",
            "You don't need eloquent words for God to understand your heart."
        ],
        "reflections": {
            "intimate": "Jesus, You know every detail of this unspoken ache. You know what was hurt, what is needed, and what cannot be spoken aloud. Meet this soul in the quietest chamber of their heart with gentle grace.",
            "hopeful": "Father, hear the silent sigh of this weary spirit. Work behind the scenes on what seems impossible, bring healing where shame once hid, and reveal Your faithful love.",
            "reflective": "Sometimes the deepest prayers are simply sitting before God in silence, letting Him look upon your heart with love. He understands what you cannot explain.",
            "narrative": "Hannah wept silently in the temple, moving her lips without making a sound, yet God heard her heart and answered her with joy. He hears your silent whisper too."
        },
        "closings": [
            "God knows, God cares, and God is already working.",
            "Rest easy; your silent prayer has been received in heaven.",
            "You are fully seen, fully understood, and never judged.",
            "May quiet peace settle over your unspoken petition tonight."
        ],
        "ctas": [
            "Just whisper Amen; God knows every detail.",
            "Save this prayer as a reminder that your tears are never ignored.",
            "Share this with someone who carries their battles quietly.",
            "Sleep in peace tonight; God has heard your heart."
        ],
        "pinned_comments": [
            "No words needed. Just leave a '🕊️' or '🙏' below, and we will agree in prayer for your unspoken request.",
            "God knows your heart's petition tonight. Type 'HE KNOWS' in faith.",
            "Lifting every silent prayer and heavy heart to the Lord tonight. You are not alone."
        ]
    },

    "spiritual_warfare": {
        "title": "⚔️ Armadura de Dios y Fortaleza Espiritual",
        "description": "Firmeza en la fe, discernimiento y victoria espiritual sobre ataques de duda y temor.",
        "target_time_slot": "morning",
        "hook_badge_text": "ARMOR OF GOD",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": "Ephesians 6:11 — Put on the full armor of God, so that you can take your stand against the devil’s schemes.",
        "hashtags": ["#ArmorOfGod", "#SpiritualVictory", "#FaithOverFear", "#MightyInGod", "#ChristianWarrior"],
        "hooks": [
            "If you felt spiritual resistance, doubt, and heaviness hitting you today...",
            "The battle in your mind is real, but the victory of Christ is greater...",
            "Put on the armor of God before you face the challenges of this day...",
            "Stand firm; the enemy only attacks what carries divine purpose."
        ],
        "reflections": {
            "intimate": "Lord Jesus, I take my stand in Your finished work. Clothe my mind in the helmet of salvation, guard my heart with righteousness, and let the shield of faith extinguish every fiery dart of fear.",
            "hopeful": "Father, no weapon formed against our home will prosper. We speak peace where confusion tries to enter, and we declare that light triumphs over darkness in our family.",
            "reflective": "Spiritual warfare is not fought with loud arguments, but with quiet, unshakable faith in God's promises. When you submit to God and resist fear, peace takes over.",
            "narrative": "David stood before Goliath with nothing but a sling and the name of the Lord of Hosts. When God is on your side, giants fall before your faith."
        },
        "closings": [
            "Walk in victory today; Christ has overcome the world.",
            "No weapon of fear can prevail against God's promises.",
            "You are more than a conqueror through Christ who loves you.",
            "May the peace of God stand guard over your mind."
        ],
        "ctas": [
            "Type Amen and stand firm in faith today!",
            "Share this with someone fighting a hard spiritual battle.",
            "Do not back down; your breakthrough is closer than you think.",
            "Walk with bold confidence in the Lord today."
        ],
        "pinned_comments": [
            "Type 'VICTORY IN JESUS' to declare your faith over fear today! 🛡️",
            "Standing together in the armor of God. No weapon formed against us shall prosper. Amen!",
            "Drop a ⚔️ if you are standing firm in faith today!"
        ]
    },

    "business_blessing": {
        "title": "💼 Bendición, Integridad y Crecimiento en el Trabajo",
        "description": "Sabiduría comercial, honestidad y puertas abiertas para emprendedores y trabajadores.",
        "target_time_slot": "morning",
        "hook_badge_text": "FAVOR IN WORK & BUSINESS",
        "recommended_image": "jesus_holy_bible.jpg",
        "scripture": "Deuteronomy 28:8 — The Lord will send a blessing on your barns and on everything you put your hand to.",
        "hashtags": ["#FaithInBusiness", "#ChristianEntrepreneur", "#HonestWork", "#KingdomFavor", "#DailyProverbs"],
        "hooks": [
            "Before you open your store, start your shift, or meet your clients today...",
            "If you are working hard to build a business with integrity and faith...",
            "May God's favor accompany the honest labor of your hands today...",
            "Success rooted in integrity and service brings lasting peace."
        ],
        "reflections": {
            "intimate": "Lord, bless the work of my hands today. Grant me creative wisdom, fair dealing with every customer, and favor with clients, employees, and partners.",
            "hopeful": "Father, we dedicate our enterprise to Your glory. May our work be a blessing to our community, provide honorable wages, and reflect Your goodness in the marketplace.",
            "reflective": "Doing business with faith means placing service above greed and integrity above shortcuts. God honors honest weights and diligent effort.",
            "narrative": "Lydia of Philippi was a hardworking businesswoman whose home and heart became a center of generosity and gospel light. May your work shine just as brightly."
        },
        "closings": [
            "May your business flourish and bless many families.",
            "May divine wisdom guide every contract and decision today.",
            "Favor, integrity, and prosperity over your honest labor.",
            "May your work bring glory to God and peace to your home."
        ],
        "ctas": [
            "Type Amen to claim divine favor over your work today.",
            "Share this blessing with a small business owner you respect.",
            "Keep serving with excellence; God sees your dedication.",
            "May your efforts yield an abundant and honorable harvest."
        ],
        "pinned_comments": [
            "Drop the name of your business, craft, or job below! We want to pray over your work today. 💼",
            "May God bless every hardworking hand here today. Type 'AMEN' in faith!",
            "Praying for favor, honesty, and financial breakthrough for your projects."
        ]
    },

    "forgiving_past": {
        "title": "🕊️ Liberación del Rencor y Sanidad del Pasado",
        "description": "Paz interior, soltar el resentimiento y sanar memorias dolorosas a través del perdón.",
        "target_time_slot": "night",
        "hook_badge_text": "FREEDOM THROUGH FORGIVENESS",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": "Colossians 3:13 — Bear with each other and forgive one another... Forgive as the Lord forgave you.",
        "hashtags": ["#ForgivenessHeals", "#LetGoAndLetGod", "#InnerPeace", "#GraceWins", "#DailyFaith"],
        "hooks": [
            "If holding onto past hurt is drinking poison and expecting the other person to suffer...",
            "Forgiveness does not excuse what they did; it frees you from carrying their weight...",
            "Tonight, choose to release the bitterness that has chained your heart...",
            "True peace begins when you stop replaying old wounds in your mind."
        ],
        "reflections": {
            "intimate": "Lord, I hand You the hurt that cut deep. Heal the scar, release me from the need for revenge, and give me the grace to release them into Your hands so I may walk freely.",
            "hopeful": "Father, You forgave me when I had nothing to offer. Cleanse my heart from resentment, replace bitter memories with Your love, and let my future be unburdened by yesterday.",
            "reflective": "Forgiving someone is an act of courage, not weakness. When you surrender the right to get even, God steps in and becomes your healer and defender.",
            "narrative": "Joseph wept and embraced the brothers who once sold him into slavery, saying: 'You intended to harm me, but God intended it for good.' Forgiveness turns pain into redemption."
        },
        "closings": [
            "May freedom and light fill your heart as you let go.",
            "You deserve the peace that only forgiveness can unlock.",
            "Leave the verdict to God; take your peace and walk forward.",
            "A lighter heart and sweet rest are waiting for you tonight."
        ],
        "ctas": [
            "Whisper Amen and let the heavy weight drop from your chest.",
            "Choose freedom tonight; your heart is too precious to hold grudges.",
            "Share this message of healing with someone carrying old pain.",
            "May God's tender mercy heal your deepest memories."
        ],
        "pinned_comments": [
            "Type 'I CHOOSE PEACE' if you are releasing past hurts into God's hands tonight. 🕊️",
            "Forgiveness is a gift you give to yourself. Praying for healing hearts tonight.",
            "Leave a ❤️ if you are choosing to walk forward in grace."
        ]
    },

    "grief_loss": {
        "title": "🕯️ Consuelo ante la Pérdida de un Ser Querido",
        "description": "Abrazo celestial, esperanza eterna y fortaleza en el proceso de duelo.",
        "target_time_slot": "night",
        "hook_badge_text": "COMFORT IN GRIEF",
        "recommended_image": "jesus_comforting_embrace.jpg",
        "scripture": "Revelation 21:4 — He will wipe every tear from their eyes. There will be no more death or mourning or crying or pain.",
        "hashtags": ["#ComfortInGrief", "#HopeInHeaven", "#GriefSupport", "#GodComforts", "#ChristianHope"],
        "hooks": [
            "To the heart aching tonight over someone dearly loved and sorely missed...",
            "When grief hits in quiet waves and the world expects you to just move on...",
            "Tears are not a sign of weak faith; they are sacred tributes of deep love...",
            "Jesus wept with grieving friends, and He sits right beside you tonight."
        ],
        "reflections": {
            "intimate": "Jesus, You know the hollow ache of missing someone who meant the world. Comfort this wounded spirit, hold this heart when the waves of grief roll in, and anchor us in the hope of eternal reunion.",
            "hopeful": "Father, thank You for the precious gift of their life and the love they shared. Grant us strength to honor their memory, peace in our quiet hours, and assurance that they rest in Your light.",
            "reflective": "Grief changes shape over time, but God's compassion never fades. Allow yourself to mourn without guilt, knowing that God holds every tear in His bottle.",
            "narrative": "At Lazarus's tomb, before performing a miracle, Jesus stopped and wept with Mary and Martha. He shares in your sorrow and promises that death never has the final word."
        },
        "closings": [
            "May the peace of heaven hold your heart together tonight.",
            "Their memory is a treasure; God's comfort is your companion.",
            "You are held by the God who promises to wipe away every tear.",
            "Rest gently tonight, surrounded by divine comfort."
        ],
        "ctas": [
            "Whisper Amen and let yourself be held by His grace tonight.",
            "Send this gentle comfort to someone who recently lost a loved one.",
            "Take your time to heal; God is walking every step with you.",
            "May warm memories bring a gentle smile to your soul."
        ],
        "pinned_comments": [
            "If you are missing a loved one tonight, leave their first name below. We honor their memory and pray for your peace. 🕯️",
            "Lifting up every grieving family tonight. You are not alone in your sorrow.",
            "May the God of all comfort wrap you in His loving arms. Type AMEN."
        ]
    },

    "guidance_direction": {
        "title": "🧭 Sabiduría y Dirección ante Decisiones Difíciles",
        "description": "Claridad mental, discernimiento espiritual y confianza en el camino correcto.",
        "target_time_slot": "morning",
        "hook_badge_text": "DIVINE GUIDANCE & WISDOM",
        "recommended_image": "jesus_holy_bible.jpg",
        "scripture": "Proverbs 3:5-6 — Trust in the Lord with all your heart... and he will make your paths straight.",
        "hashtags": ["#DivineGuidance", "#GodsWill", "#WisdomFromAbove", "#TrustingGod", "#DailyDirection"],
        "hooks": [
            "If you are standing at a crossroads, unsure of which path to take...",
            "When so many voices give advice that your mind feels confused and loud...",
            "Before you make that life-altering choice or sign that agreement...",
            "Ask for the quiet wisdom that comes from above."
        ],
        "reflections": {
            "intimate": "Lord, silence the noise of worldly opinions. Give me clarity of mind, peace in my spirit, and the courage to take the next faithful step according to Your will.",
            "hopeful": "Father, Your word is a lamp to my feet and a light to my path. Make the crooked places straight, remove confusion, and confirm the right road with Your unmistakable peace.",
            "reflective": "God rarely gives a ten-year roadmap; He gives daily light for the next step. Walk in obedience with what you know today, and tomorrow will unfold in His timing.",
            "narrative": "God guided the Israelites with a pillar of cloud by day and a pillar of fire by night. He will never leave you wandering in the wilderness without His direction."
        },
        "closings": [
            "May divine clarity replace every doubt in your mind.",
            "Trust the process; God is ordering your steps.",
            "When God guides, He always provides.",
            "Walk forward in peace; your tomorrow is secure."
        ],
        "ctas": [
            "Type Amen and ask for divine wisdom over your decisions today.",
            "Share this with someone facing a major life crossroad.",
            "Be patient with yourself; God is leading you with love.",
            "May your choices bring lasting peace and honor."
        ],
        "pinned_comments": [
            "If you are asking God for guidance in a decision, type 'LEAD ME LORD' below! 🧭",
            "Praying for clarity, discernment, and peace for everyone at a crossroads today.",
            "Trust in the Lord with all your heart. Drop a 🙏 in agreement."
        ]
    },

    "strength_weary": {
        "title": "⚡ Renovación de Fuerzas para el Cansado y Agotado",
        "description": "Energía renovada, descanso espiritual y aliento para quien siente que ya no puede más.",
        "target_time_slot": "midday",
        "hook_badge_text": "RENEWED STRENGTH",
        "recommended_image": "jesus_reaching_hand.jpg",
        "scripture": "Isaiah 40:31 — Those who hope in the Lord will renew their strength. They will soar on wings like eagles.",
        "hashtags": ["#RenewedStrength", "#WingsLikeEagles", "#NeverGiveUp", "#GodOurRefuge", "#DailyEncouragement"],
        "hooks": [
            "If you are doing your best, but your emotional tank is running on empty...",
            "When being strong for everyone else has left you completely drained...",
            "To the exhausted heart that wonders how it will finish this week...",
            "You were never meant to carry this mountain in your own strength."
        ],
        "reflections": {
            "intimate": "Jesus, I lay my fatigue at Your feet. Recharge my spirit, breathe fresh energy into my weary body, and let Your supernatural power be made visible in my weakness.",
            "hopeful": "Father, You do not grow faint or weary. Lift this soul above the storm on wings like eagles. Grant patience for today and renewed hope for tomorrow.",
            "reflective": "Rest is not quitting; it is an act of trust. Taking a moment to pause and surrender your burdens allows God to renew what striving could never accomplish.",
            "narrative": "Moses' hands grew heavy during battle, so Aaron and Hur held up his hands until sunset and victory was won. God surrounds you with grace to hold you up today."
        },
        "closings": [
            "May fresh vigor and peaceful strength enter your soul.",
            "You are stronger than you feel, because Christ lives in you.",
            "Tomorrow's strength will meet you when tomorrow comes.",
            "Rest in His hands; you do not have to do this alone."
        ],
        "ctas": [
            "Whisper Amen and let Him be your strength today.",
            "Send this to someone who carries heavy loads for their family.",
            "Take a deep breath and give yourself permission to pause.",
            "May joy return to your steps before this day ends."
        ],
        "pinned_comments": [
            "Drop a '⚡' or type 'RENEW MY STRENGTH' if your spirit needed this today!",
            "Praying for renewed energy, joyful hope, and peaceful rest for every tired soul here.",
            "God is your strength in moments of weakness. Type AMEN in faith."
        ]
    },

    "peace_in_storm": {
        "title": "⛈️ Paz en Medio de la Tormenta y la Crisis",
        "description": "Ancla de fe y serenidad cuando las circunstancias externas parecen salirse de control.",
        "target_time_slot": "night",
        "hook_badge_text": "PEACE IN THE STORM",
        "recommended_image": "jesus_praying_gethsemane.jpg",
        "scripture": "Mark 4:39 — He got up, rebuked the wind and said to the waves, 'Quiet! Be still!' Then the wind died down.",
        "hashtags": ["#PeaceInTheStorm", "#JesusCalmsTheSea", "#FaithOverFear", "#AnchorOfHope", "#DailyPeace"],
        "hooks": [
            "When circumstances around you feel like crashing waves that won't stop...",
            "If unexpected crisis has shaken the ground beneath your feet...",
            "Do not look at the height of the waves; look at the One in your boat...",
            "Peace is not a calm sea; peace is a Savior who commands the winds."
        ],
        "reflections": {
            "intimate": "Lord Jesus, the storm is loud, but Your voice is sovereign. Speak 'Peace, be still' over my racing heart. Anchor my soul so that panic cannot wash away my trust in You.",
            "hopeful": "Father, though the winds howl, our foundation is built upon the rock of Christ. We will not be moved. Bring order to the chaos and guide us safely through this trial.",
            "reflective": "A boat does not sink because there is water around it; it only sinks if water gets inside. Keep the fear of the storm out of your heart by fixing your eyes on Christ.",
            "narrative": "The disciples thought they were drowning while Jesus was sleeping in the stern. With three words, the tempest turned into glassy calm. He has the same power in your life."
        },
        "closings": [
            "May calm waters and clear skies meet you soon.",
            "You will outlast this storm because Jesus holds your hand.",
            "His peace is deeper than the deepest sea.",
            "Stand firm; the winds must obey His command."
        ],
        "ctas": [
            "Type Amen and claim stillness over your storm today.",
            "Share this anchor of hope with someone facing a crisis.",
            "Hold onto faith; this storm will pass.",
            "May supernatural calm settle over your life right now."
        ],
        "pinned_comments": [
            "If you are in the middle of a storm right now, leave a '⚓' below. We are anchoring with you in prayer.",
            "Jesus is in your boat; you will not sink. Type 'PEACE BE STILL' in faith!",
            "Lifting up everyone facing sudden family or financial storms today. God is faithful."
        ]
    },

    "divine_grace": {
        "title": "✝️ La Gracia Incondicional y el Amor de Jesús",
        "description": "Recordar que el amor de Dios no depende de nuestras obras, sino de Su misericordia eterna.",
        "target_time_slot": "morning",
        "hook_badge_text": "UNCONDITIONAL GRACE",
        "recommended_image": "holy_cross_calvary.jpg",
        "scripture": "Ephesians 2:8 — For it is by grace you have been saved, through faith—and this is not from yourselves, it is the gift of God.",
        "hashtags": ["#AmazingGrace", "#LovedByJesus", "#UnconditionalLove", "#ChristianFaith", "#GospelTruth"],
        "hooks": [
            "If shame has been telling you that you are too broken for God to love...",
            "You do not have to perform or earn your way into God's mercy...",
            "His love is not based on your best days, and it doesn't leave on your worst...",
            "Grace means the debt is paid and the welcome is forever."
        ],
        "reflections": {
            "intimate": "Jesus, thank You that Your cross covered all my shame and failure. Help me lay down the burden of trying to be perfect, and teach me to rest in the beauty of Your unmerited favor.",
            "hopeful": "Father, Your grace is a fountain that never runs dry. Because of Christ, we can boldly approach Your throne of mercy with open hands and joyful hearts.",
            "reflective": "Religion says: 'If you change, God will love you.' The Gospel says: 'God loves you, and His love will gently transform you.' Walk in that freedom today.",
            "narrative": "The prodigal son rehearsed a speech asking to be treated like a hired servant, but before he could finish, his father ran, embraced him, and gave him the best robe. That is grace."
        },
        "closings": [
            "Walk with freedom today; you are forgiven and deeply loved.",
            "His grace is greater than your deepest regret.",
            "Nothing can separate you from the love of God in Christ Jesus.",
            "May His tender love be the melody of your heart today."
        ],
        "ctas": [
            "Type Amen and celebrate the gift of His amazing grace today!",
            "Share this message of hope with someone burdened by guilt.",
            "Receive His forgiveness and forgive yourself today.",
            "Walk boldly in the light of His unconditional love."
        ],
        "pinned_comments": [
            "Drop an 'AMEN' if you are thankful for the grace and mercy of Jesus today! ✝️",
            "You are loved, you are valued, and you are His. Leave a ❤️ in celebration of grace.",
            "Praising God for His unfailing kindness toward us every single day."
        ]
    }
}

# Image pool mappings
THEME_TO_SCENARIO_MAP: Dict[str, List[str]] = {
    "lost_child": ["family_blessing", "jesus_comforting", "people_praying"],
    "family_protection": ["family_blessing", "holy_cross", "jesus_comforting"],
    "medical_fear": ["jesus_comforting", "people_praying", "holy_bible"],
    "zero_balance": ["holy_bible", "family_blessing", "jesus_comforting"],
    "night_anxiety": ["jesus_comforting", "people_praying", "holy_bible"],
    "morning_favor": ["holy_bible", "family_blessing", "jesus_comforting"],
    "marriage_healing": ["family_blessing", "jesus_comforting", "people_praying"],
    "healing_depression": ["jesus_comforting", "people_praying", "holy_bible"],
    "job_breakthrough": ["holy_bible", "family_blessing", "jesus_comforting"],
    "lonely_widow": ["jesus_comforting", "people_praying", "holy_bible"],
    "addiction_chains": ["holy_cross", "jesus_comforting", "people_praying"],
    "elderly_parents": ["family_blessing", "jesus_comforting", "people_praying"],
    "single_parent": ["family_blessing", "jesus_comforting", "people_praying"],
    "sick_grandchild": ["jesus_comforting", "people_praying", "family_blessing"],
    "court_legal": ["holy_cross", "holy_bible", "jesus_comforting"],
    "restless_sleep": ["jesus_comforting", "people_praying", "holy_bible"],
    "gratitude_harvest": ["holy_bible", "family_blessing", "jesus_comforting"],
    "unspoken_prayer": ["people_praying", "jesus_comforting", "holy_bible"],
    "spiritual_warfare": ["holy_cross", "jesus_comforting", "holy_bible"],
    "business_blessing": ["holy_bible", "family_blessing", "holy_cross"],
    "forgiving_past": ["jesus_comforting", "holy_cross", "people_praying"],
    "grief_loss": ["jesus_comforting", "people_praying", "holy_bible"],
    "guidance_direction": ["holy_bible", "jesus_comforting", "people_praying"],
    "strength_weary": ["jesus_comforting", "people_praying", "holy_bible"],
    "peace_in_storm": ["jesus_comforting", "holy_cross", "people_praying"],
    "divine_grace": ["holy_cross", "jesus_comforting", "holy_bible"]
}

SCENARIO_POOLS: Dict[str, List[str]] = {
    "jesus_comforting": [
        "Jesus Christ with compassionate loving eyes, gentle smile, holy warm golden light",
        "Jesus placing His hand gently upon a person's shoulder, divine golden aura, sacred emotional atmosphere",
        "Jesus walking beside family members on a tranquil path, bathed in divine golden hour sunlight"
    ],
    "people_praying": [
        "A devout Christian praying fervently with closed eyes and folded hands, soft candle light",
        "Warm Christian family praying together around a rustic wooden table, peaceful evening glow",
        "A mother holding a worn Bible, looking out the window in heartfelt faith and serenity"
    ],
    "holy_bible": [
        "Open ancient holy Bible with golden rays of sunlight illuminating the sacred pages, 8k",
        "Wooden table with an open Bible beside a warm coffee mug, peaceful morning devotion atmosphere",
        "Close-up of holy scripture illuminated by gentle morning dawn light, majestic and reverent"
    ],
    "holy_cross": [
        "Majestic wooden cross standing on a peaceful hill against a warm golden sunset sky, cinematic",
        "Silhouette of the holy cross with divine volumetric rays piercing through soft clouds",
        "Golden glowing cross surrounded by gentle ethereal mist and celestial dawn lighting"
    ],
    "family_blessing": [
        "Warm family sanctuary in a peaceful home at twilight, soft glowing candlelight, tranquility",
        "Loving family embracing with smiles, bathed in golden hour radiant sunshine, serene joy",
        "Quiet porch with green rolling hills in the background, peaceful morning atmosphere"
    ]
}

CAMERA_STYLES = [
    "cinematic 35mm photography, dramatic volumetric chiaroscuro lighting, masterpiece 8k",
    "hyper-realistic Unreal Engine 5 render, radiant golden hour sunburst, sharp focus",
    "intimate emotional portrait, anamorphic lens, soft golden bokeh, divine atmosphere",
    "epic wide-angle panoramic cinematic shot, volumetric God-rays, high contrast"
]


def _translate_topic(topic: str) -> str:
    """Normalize and translate common Spanish/English topics into natural English phrasing."""
    clean = topic.strip().lower()
    for k, v in CUSTOM_TOPIC_TRANSLATIONS.items():
        if k in clean:
            return v
    return topic.strip()


def generate_image_prompt_for_script(
    theme_key: Optional[str] = None,
    script_text: str = "",
    custom_topic: Optional[str] = None
) -> str:
    """Genera un prompt hiperrealista para IA de imagen acorde al tema y guion."""
    t_key = theme_key if (theme_key and theme_key in THEME_TO_SCENARIO_MAP) else "lost_child"
    candidate_pools = THEME_TO_SCENARIO_MAP.get(t_key, list(SCENARIO_POOLS.keys()))
    chosen_cat = random.choice(candidate_pools)
    base_scene = random.choice(SCENARIO_POOLS.get(chosen_cat, SCENARIO_POOLS["jesus_comforting"]))
    style = random.choice(CAMERA_STYLES)

    custom_cue = ""
    if custom_topic and custom_topic.strip():
        trans = _translate_topic(custom_topic)
        custom_cue = f", spiritually touching theme of {trans}"

    return f"{base_scene}{custom_cue}, {style}, dynamic framing, sacred golden light, hyper-detailed, masterpiece --ar 9:16"


def generate_3scene_prompts_for_script(
    theme_key: Optional[str] = None,
    script_text: str = "",
    custom_topic: Optional[str] = None
) -> Dict[str, str]:
    """Genera 3 prompts sincronizados para las 3 tomas del Reel."""
    t_key = theme_key if (theme_key and theme_key in VIRAL_THEMES) else "morning_favor"
    theme = VIRAL_THEMES.get(t_key, VIRAL_THEMES["morning_favor"])
    topic_str = f" for {_translate_topic(custom_topic)}" if (custom_topic and custom_topic.strip()) else ""

    p1 = f"Cinematic atmospheric opening: an open Holy Bible on a wooden table beside gentle morning light{topic_str}, warm golden glow, award-winning photography --ar 9:16"
    p2 = f"Emotional intercession: a faithful person in quiet heartfelt prayer{topic_str}, dramatic volumetric chiaroscuro lighting, deep reverence, 8k --ar 9:16"
    p3 = f"Jesus Christ with compassionate outstretched hands, golden hour celestial aura, divine peace and victory{topic_str}, masterpiece --ar 9:16"

    return {
        "prompt": generate_image_prompt_for_script(theme_key, script_text, custom_topic),
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
    tags_str = " ".join(hashtags)
    clean_title = re.sub(r'^[^\w]+', '', theme_title).strip()
    return (
        f"✝️ {clean_title.upper()} ✝️\n\n"
        f"\"{prayer_text}\"\n\n"
        f"📖 SCRIPTURE TODAY:\n\"{scripture}\"\n\n"
        f"🕊️ {cta}\n\n"
        f"{tags_str}"
    )


def generate_script(
    theme_key: Optional[str] = None,
    custom_topic: Optional[str] = None,
    mode: str = "deep",
    tone: Optional[str] = None
) -> Dict[str, str]:
    """
    Genera un guion estructurado con variaciones reales según tema, modo y tema personalizado.
    Estructura de 4 Partes:
      1. Gancho (Hook): Situación o pregunta relatable.
      2. Desarrollo (Body): Oración y reflexión espiritual profunda.
      3. Cierre (Closing): Declaración de paz y verdad bíblica.
      4. CTA: Invitación natural y respetuosa.
    Modos:
      - 'micro' (15-20s): 28-36 palabras
      - 'deep' (25-35s): 48-62 palabras
      - 'story' (40-50s): 75-95 palabras
    """
    chosen_key = theme_key if (theme_key and theme_key in VIRAL_THEMES) else random.choice(list(VIRAL_THEMES.keys()))
    theme = VIRAL_THEMES[chosen_key]

    valid_tones = ["intimate", "hopeful", "reflective", "narrative"]
    chosen_tone = tone if (tone in valid_tones) else random.choice(valid_tones)

    # 1. Gancho (Hook)
    if custom_topic and custom_topic.strip():
        translated_topic = _translate_topic(custom_topic)
        hook_options = [
            f"If your heart is carrying a quiet burden for {translated_topic} today...",
            f"Tonight, as you pray for {translated_topic}, know that God hears you.",
            f"When you are trusting God through {translated_topic}, take heart.",
            f"Before you let worry over {translated_topic} overwhelm your mind tonight..."
        ]
        hook = random.choice(hook_options)
    else:
        hook = random.choice(theme.get("hooks", [
            "Before you close your eyes carrying that quiet worry tonight...",
            "If your heart feels weary and you are seeking God's peace today..."
        ]))

    # 2. Desarrollo (Body) según Tono
    reflections = theme.get("reflections", {})
    base_reflection = reflections.get(chosen_tone, reflections.get("hopeful", "Lord, cover our home in Your gentle peace."))

    # Personalizar cuerpo si hay custom_topic
    if custom_topic and custom_topic.strip():
        topic_phrase = _translate_topic(custom_topic)
        body_custom = f"Lord, we lift up {topic_phrase} into Your loving hands. Bring peace where there is fear, grant wisdom in every choice, and let Your steady grace sustain us through every step."
        if mode == "micro":
            body = f"Lord, we place {topic_phrase} in Your hands; let Your peace guard our home tonight."
        elif mode == "story":
            body = f"{base_reflection} We specifically bring {topic_phrase} before Your throne today. What seems too heavy for us to carry alone is held safely in Your loving presence."
        else:  # deep
            body = f"{base_reflection} Father, we place {topic_phrase} under Your wings of mercy, trusting Your unfailing care."
    else:
        if mode == "micro":
            # Extraer 1-2 oraciones clave para duración breve (~30 palabras)
            sentences = [s.strip() for s in base_reflection.split(".") if s.strip()]
            body = f"{sentences[0]}." if sentences else base_reflection
        elif mode == "story":
            narrative_body = reflections.get("narrative", base_reflection)
            reflective_body = reflections.get("reflective", "")
            body = f"{narrative_body} {reflective_body}".strip()
        else:  # deep
            body = base_reflection

    # 3. Cierre (Closing)
    closing = random.choice(theme.get("closings", [
        "May His peace guard your heart and mind tonight.",
        "You are held securely in hands of endless grace."
    ]))

    # 4. CTA
    cta = random.choice(theme.get("ctas", [
        "Whisper Amen if you receive this peace today.",
        "Rest in His promise tonight; tomorrow brings fresh mercy."
    ]))

    # Ensamblar texto completo según el modo
    if mode == "micro":
        full_text = f"{hook} {body} {cta}".strip()
    elif mode == "story":
        full_text = f"{hook} {body} {closing} {cta}".strip()
    else:  # deep (default)
        full_text = f"{hook} {body} {closing} {cta}".strip()

    # Cálculo preciso de duración estimada (~130 palabras por minuto / ~2.15 palabras por segundo)
    word_count = len(full_text.split())
    estimated_duration_sec = round(max(15.0, (word_count / 2.15) + 1.5), 1)

    hook_badge = theme.get("hook_badge_text", "PRAYER OF FAITH")
    scripture = theme.get("scripture", "Philippians 4:6 — In every situation, by prayer and petition, present your requests to God.")
    hashtags = theme.get("hashtags", ["#DailyPrayer", "#FaithInGod", "#ChristianFamily"])
    pinned = random.choice(theme.get("pinned_comments", [
        "What is the first name of the person you are praying for today? Drop it below! 🙏"
    ]))

    seo_caption = generate_seo_caption(theme["title"], full_text, scripture, cta, hashtags)
    prompts_3s = generate_3scene_prompts_for_script(chosen_key, full_text, custom_topic)

    return {
        "theme_key": chosen_key,
        "theme_title_es": theme["title"],
        "hook": hook,
        "body": f"{body} {closing}".strip(),
        "cta": cta,
        "full_text": full_text,
        "word_count": word_count,
        "estimated_duration_sec": estimated_duration_sec,
        "mode": mode,
        "tone": chosen_tone,
        "hook_badge_text": hook_badge,
        "micro_cta_text": cta,
        "scripture": scripture,
        "pinned_comment": pinned,
        "seo_caption": seo_caption,
        "hashtags": hashtags,
        "scene_1_prompt": prompts_3s["scene_1_prompt"],
        "scene_2_prompt": prompts_3s["scene_2_prompt"],
        "scene_3_prompt": prompts_3s["scene_3_prompt"],
        "image_prompt": prompts_3s["prompt"]
    }


def get_card_template_for_theme(theme_key: str) -> Dict[str, str]:
    """Genera plantilla devocional para tarjeta 4:5 de Feed en inglés con tipografía noble."""
    chosen_key = theme_key if (theme_key and theme_key in VIRAL_THEMES) else "lost_child"
    theme = VIRAL_THEMES[chosen_key]

    raw_title = theme.get("hook_badge_text", "PRAYER OF FAITH")
    reflections = theme.get("reflections", {})
    body = reflections.get("intimate", reflections.get("hopeful", "Lord, place a hedge of protection around my home."))
    closing = theme.get("closings", ["May His peace rest upon you."])[0]
    devotional_prayer = f"{body} {closing}".strip()

    scripture = theme.get("scripture", "Philippians 4:19 — And my God will supply every need of yours.")
    hashtags = theme.get("hashtags", ["#DailyPrayer", "#FaithInGod", "#ChristianFamily"])
    rec_img = theme.get("recommended_image", "jesus_healing_miracle.jpg")

    feed_copy = f"""✝️ {raw_title} ✝️

"{devotional_prayer}"

📖 {scripture}

🕊️ If you receive this prayer into your heart and home today, type "AMEN" and share it with someone who needs God's peace right now. 

{" ".join(hashtags)}"""

    return {
        "theme_key": chosen_key,
        "theme_title_es": theme["title"],
        "title_english": raw_title,
        "prayer_english": devotional_prayer,
        "scripture": scripture,
        "recommended_image": rec_img,
        "feed_copy": feed_copy,
        "pinned_comment": theme.get("pinned_comments", ["Drop your first name below so we can cover you in prayer! 🙏"])[0]
    }


def get_themes_list() -> List[Dict]:
    return [
        {"key": k, "title": v["title"], "description": v["description"]}
        for k, v in VIRAL_THEMES.items()
    ]
