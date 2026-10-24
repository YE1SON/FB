"""
JESUSREELS STUDIO - EDITORIAL CAPTIONS & HASHTAG SYSTEM
Optimización editorial para FaithSpark Daily dirigida a adultos de Estados Unidos.
Implementa:
- Formato A: Breve emocional (~20-40 palabras sin hashtags).
- Formato B: Reflexivo contextual (~50-85 palabras sin hashtags).
- Sistema de 3 estrategias de hashtags: 0, 3 y 5 etiquetas temáticas normalizadas.
- Asignación de grupos experimentales (A1-A3, B1-B3) y matriz de 18 Reels.
"""

import re
from typing import Dict, List, Optional, Any, Tuple

# ─── 1. Catálogo Temático de Hashtags Curados (26 Temas) ──────────────────────
# Hashtags específicos con capitalización CamelCase para alta legibilidad.
# Cada tema tiene 5 etiquetas específicas ordenadas por relevancia temática.

THEMATIC_HASHTAGS: Dict[str, List[str]] = {
    "lost_child": [
        "#PrayingParents", "#ProdigalSon", "#FamilyPrayer", "#ParentingFaith", "#QuietTrust"
    ],
    "family_protection": [
        "#FamilyPrayer", "#PeaceInTheHome", "#HouseholdGrace", "#BedtimeBlessing", "#FaithfulHome"
    ],
    "medical_fear": [
        "#WaitingOnGod", "#MedicalPeace", "#ComfortInTrials", "#TrustGodsTiming", "#HealingGrace"
    ],
    "zero_balance": [
        "#FinancialFaith", "#GodProvides", "#DailyProvision", "#TrustingInHardTimes", "#PeaceOverWorry"
    ],
    "night_anxiety": [
        "#NightPrayer", "#PeaceBeforeSleep", "#AnxietyRelief", "#QuietEvening", "#RestInGod"
    ],
    "morning_favor": [
        "#MorningPrayer", "#DailyGrace", "#StartWithFaith", "#FreshMercies", "#MorningDevotion"
    ],
    "marriage_healing": [
        "#MarriagePrayer", "#GraceInMarriage", "#Reconciliation", "#PatienceAndLove", "#FaithfulMarriage"
    ],
    "healing_depression": [
        "#QuietHope", "#FaithInDarkness", "#GentleGrace", "#BrokenheartedComfort", "#OneDayAtATime"
    ],
    "job_breakthrough": [
        "#JobSearchFaith", "#WorkplaceBlessing", "#OpenDoors", "#TrustGodsPlan", "#CareerGuidance"
    ],
    "lonely_widow": [
        "#GriefAndGrace", "#ComfortInSolitude", "#GodNearTheBroken", "#QuietEvening", "#FaithfulCompanion"
    ],
    "addiction_chains": [
        "#OneStepAtATime", "#FreedomInChrist", "#GraceToOvercome", "#HonestFaith", "#DailyStrength"
    ],
    "elderly_parents": [
        "#CaregiverGrace", "#HonoringParents", "#StrengthForCaregivers", "#QuietPatience", "#FamilyLove"
    ],
    "single_parent": [
        "#SingleParentFaith", "#StrengthForToday", "#ParentingGrace", "#GodOurProvider", "#QuietCourage"
    ],
    "sick_grandchild": [
        "#GrandparentsPrayer", "#PrayingForHealing", "#ComfortForFamily", "#FaithInUncertainty", "#QuietTears"
    ],
    "court_legal": [
        "#PeaceInTrials", "#WisdomForToday", "#TrustGodsJustice", "#FacingUncertainty", "#QuietResolution"
    ],
    "restless_sleep": [
        "#SleepPrayer", "#PeaceTonight", "#QuietMind", "#RestInHisHands", "#RestfulNight"
    ],
    "gratitude_harvest": [
        "#EverydayGratitude", "#ThankfulHeart", "#CountYourBlessings", "#DailyGrace", "#FaithfulWalk"
    ],
    "unspoken_prayer": [
        "#UnspokenPrayer", "#WhenWordsFail", "#TheSpiritIntercedes", "#SilentPrayer", "#GodUnderstands"
    ],
    "spiritual_warfare": [
        "#QuietCourage", "#StandingFirm", "#PeaceOverFear", "#FaithOverAnxiety", "#ArmorOfGod"
    ],
    "business_blessing": [
        "#WorkplaceFaith", "#HonestWork", "#IntegrityInBusiness", "#DailyDirection", "#QuietFaith"
    ],
    "forgiving_past": [
        "#ForgivenessJourney", "#HealingOldHurts", "#LettingGoWithGrace", "#InnerPeace", "#FreedomToHeal"
    ],
    "grief_loss": [
        "#GriefJourney", "#ComfortInLoss", "#HoldingOntoHope", "#QuietMemories", "#GodWipesTears"
    ],
    "guidance_direction": [
        "#SeekingWisdom", "#NextStepsFaith", "#TrustingHisLead", "#ClarityInDecisions", "#FaithfulWalk"
    ],
    "strength_weary": [
        "#GraceForWeary", "#RenewedStrength", "#RestForTiredSouls", "#GentleFaith", "#GodSustains"
    ],
    "peace_in_storm": [
        "#PeaceInTheStorm", "#CalmInChaos", "#SteadfastHope", "#QuietAnchor", "#FaithThroughWaves"
    ],
    "divine_grace": [
        "#GraceForToday", "#FreshStart", "#MercyNewEveryMorning", "#GodNeverGivesUp", "#RestInGrace"
    ]
}

# Hashtags generales de fe para completar la estrategia de 5 tags
GENERAL_FAITH_HASHTAGS: List[str] = [
    "#FaithSparkDaily", "#DailyDevotional", "#ChristianReels", "#FaithInGod", "#DailyPrayer"
]

# ─── 2. Normalización y Deduplicación de Hashtags ─────────────────────────────

def normalize_hashtag(tag: str) -> str:
    """Limpia y normaliza un hashtag preservando CamelCase y eliminando caracteres inválidos."""
    if not tag:
        return ""
    clean = re.sub(r"[^\w#]", "", tag.strip())
    if not clean.startswith("#"):
        clean = "#" + clean
    return clean


def deduplicate_hashtags(tags: List[str]) -> List[str]:
    """Deduplica etiquetas de forma case-insensitive manteniendo el formato original de la primera aparición."""
    seen_lower = set()
    unique = []
    for t in tags:
        norm = normalize_hashtag(t)
        if len(norm) <= 1:
            continue
        lower = norm.lower()
        if lower not in seen_lower:
            seen_lower.add(lower)
            unique.append(norm)
    return unique


def get_theme_hashtags(
    theme_key: str,
    strategy: int = 3,
    custom_tags: Optional[List[str]] = None
) -> List[str]:
    """
    Retorna la lista de hashtags según la estrategia elegida:
    - strategy = 0: [] (sin hashtags)
    - strategy = 3: 3 etiquetas específicas temáticas
    - strategy = 5: 3 etiquetas específicas temáticas + 2 generales de fe
    """
    if strategy == 0:
        return []

    thematic = THEMATIC_HASHTAGS.get(theme_key, [
        "#DailyPrayer", "#FaithInGod", "#ChristianLiving", "#QuietHope", "#GraceForToday"
    ])

    if custom_tags:
        thematic = deduplicate_hashtags(custom_tags + thematic)

    if strategy == 3:
        return thematic[:3]

    if strategy == 5:
        # Combinar las 3 mejores temáticas con las 2 generales más afines
        candidates = thematic[:3] + GENERAL_FAITH_HASHTAGS
        return deduplicate_hashtags(candidates)[:5]

    return thematic[:min(strategy, len(thematic))]


# ─── 3. Generador de Descripciones en Inglés de EE. UU. ─────────────────────────

# Modelos contextuales por tema para Formato A (Breve emocional: ~20-40 palabras)
# Estructura: Situación concreta + consuelo/esperanza + invitación natural y voluntaria.
FORMAT_A_BLUEPRINTS: Dict[str, Dict[str, str]] = {
    "lost_child": {
        "context": "To every parent whispering silent prayers before switching off the light tonight.",
        "message": "Your love has not failed, and your patience is never in vain. May God's quiet peace guard your home and meet your son or daughter wherever they walk.",
        "invitation": "Take a steady breath and rest in hope tonight."
    },
    "family_protection": {
        "context": "When the world outside has felt loud and demanding all day long.",
        "message": "May gentle peace settle inside your home tonight. Leave the stress at the doorway and let grace cover every room and every family member.",
        "invitation": "Rest easy knowing God watches over this household."
    },
    "medical_fear": {
        "context": "While waiting for medical answers or enduring a season of uncertainty.",
        "message": "You do not have to carry tomorrow's results alone tonight. God's compassionate presence stays beside you through every hour of waiting.",
        "invitation": "Hold steady in faith; you are deeply cared for."
    },
    "zero_balance": {
        "context": "When the bills feel heavy and the numbers are hard to balance.",
        "message": "A difficult financial season does not define your worth or your future. Trust that God knows every honest need and provides strength one day at a time.",
        "invitation": "May quiet assurance replace worry upon your pillow tonight."
    },
    "night_anxiety": {
        "context": "When the house is dark and silent, but your mind keeps replaying the day.",
        "message": "You are allowed to rest before everything is figured out. Place each racing thought into God's faithful hands and let sleep find you peacefully.",
        "invitation": "Take a calm breath; tomorrow's grace is waiting."
    },
    "morning_favor": {
        "context": "Before the demands of the day pull your attention in a dozen directions.",
        "message": "Pause for one quiet moment with God. Begin your morning with fresh peace, knowing that His mercy is already walking ahead of you.",
        "invitation": "May this day bring honest encouragement to your steps."
    },
    "marriage_healing": {
        "context": "When sharing a home feels quiet with unspoken hurt between two hearts.",
        "message": "Healing begins with quiet patience and the courage to listen. May God soften old frustrations and restore warmth and mutual kindness between you.",
        "invitation": "Love perseveres through the quiet seasons."
    },
    "healing_depression": {
        "context": "When getting through ordinary hours takes more energy than anyone sees.",
        "message": "A quiet struggle does not mean your faith is small. God stays closest to the brokenhearted, offering steady compassion without demanding perfection.",
        "invitation": "Be gentle with your heart today."
    },
    "job_breakthrough": {
        "context": "After another application submitted and another silent inbox.",
        "message": "Your dignity and calling are never measured by a job rejection. Trust that God sees your honest labor and is preparing the right door in His time.",
        "invitation": "Keep moving forward with quiet dignity."
    },
    "lonely_widow": {
        "context": "When the table has one quiet chair and evenings feel especially still.",
        "message": "Your memories are precious and your love endures. May God's faithful companionship fill your home with deep warmth and gentle peace tonight.",
        "invitation": "You are remembered, loved, and never alone."
    },
    "addiction_chains": {
        "context": "When walking the road to recovery asks for another honest step.",
        "message": "You do not have to fight alone. God's grace meets you right where you are, granting quiet resolve for today without the weight of yesterday.",
        "invitation": "One honest day at a time, held in grace."
    },
    "elderly_parents": {
        "context": "When caring for an aging parent leaves you physically and emotionally worn.",
        "message": "Needing rest does not mean loving them any less. May God replenish your strength and surround your family with patience and tender honor.",
        "invitation": "Rest your tired heart tonight."
    },
    "single_parent": {
        "context": "To the parent carrying the work of two while keeping the house steady.",
        "message": "God sees every unseen sacrifice you make for your children. May His supernatural provision and gentle rest carry you through this evening.",
        "invitation": "You are doing an honorable work; rest well."
    },
    "sick_grandchild": {
        "context": "When you wish you could carry the pain of an unwell grandchild.",
        "message": "Your prayers surround their bedside even from afar. May Jesus wrap your little one in healing comfort and grant your family steady peace.",
        "invitation": "Placing their little hands into the Father's care."
    },
    "court_legal": {
        "context": "Before an important appointment or unresolved legal proceeding.",
        "message": "Do not let anxiety dictate your sleep tonight. Commit your cause to the Lord, trusting in His justice, fairness, and steady guidance.",
        "invitation": "May quiet confidence steady your mind."
    },
    "restless_sleep": {
        "context": "When sleep feels distant and worries keep you turning in bed.",
        "message": "Release the day's unfinished tasks into God's keeping. In His presence there is safety, quietness, and restorative rest for your mind and body.",
        "invitation": "Sleep in peace tonight; God remains on watch."
    },
    "gratitude_harvest": {
        "context": "Looking back on an ordinary day filled with quiet blessings.",
        "message": "Gratitude begins when we notice the simple things that carried us through. Thank God for faithful friends, daily bread, and unfailing mercy.",
        "invitation": "May thanksgiving bring quiet joy to your evening."
    },
    "unspoken_prayer": {
        "context": "When your heart is too full of pain or concern to find formal words.",
        "message": "God hears the prayer beneath your silent sighs. You do not need polished speeches; simply rest in the truth that He understands completely.",
        "invitation": "Rest without words in His gentle presence."
    },
    "spiritual_warfare": {
        "context": "When fear has been loud and doubts try to take ground in your thoughts.",
        "message": "Stand firm in the truth of God's Word. The Lord is faithful to protect, sustain, and give you quiet courage that fear cannot dismantle.",
        "invitation": "Peace is your inheritance in Christ."
    },
    "business_blessing": {
        "context": "After closing up the workplace with unfinished questions on your mind.",
        "message": "Integrity and quiet diligence matter before God. Rest your mind tonight, trusting that the Lord establishes the work of faithful hands.",
        "invitation": "Leave tomorrow's labor with the Lord."
    },
    "forgiving_past": {
        "context": "When an old memory returns and forgiveness feels like an unfinished journey.",
        "message": "Choosing peace over bitterness is an act of spiritual freedom. May God heal the tender places and give you wisdom to walk forward in grace.",
        "invitation": "Release what hurts into God's healing hands."
    },
    "grief_loss": {
        "context": "When grief interrupts your day and missing someone feels acute.",
        "message": "Tears are not a failure of faith; they are love finding its way. The Lord stays close to you in this tender season, offering everlasting comfort.",
        "invitation": "May gentle solace wrap around your heart tonight."
    },
    "guidance_direction": {
        "context": "Standing at a crossroads when the next step feels completely unclear.",
        "message": "You do not need to see the entire road ahead to take the next faithful step. Trust that God's loving counsel will illuminate your path in time.",
        "invitation": "Walk quietly with God, one decision at a time."
    },
    "strength_weary": {
        "context": "When you have been strong for everyone else and now feel completely empty.",
        "message": "Rest is not a luxury; it is God's provision for weary souls. Come as you are, lay down your heavy burdens, and let the Lord renew your spirit.",
        "invitation": "Receive His restorative rest tonight."
    },
    "peace_in_storm": {
        "context": "When sudden news or unexpected turbulence shakes your sense of stability.",
        "message": "The storm may be real, but Christ's authority over the wind is greater still. Anchor your heart in His promises and let His peace guard your mind.",
        "invitation": "Be still and know that He is with you."
    },
    "divine_grace": {
        "context": "When you keep replaying a mistake and feeling unworthy of grace.",
        "message": "One difficult day or stumble does not end God's faithful plan for your life. Come boldly to the throne of grace, where mercy meets you with open arms.",
        "invitation": "Receive fresh grace and begin anew."
    }
}


# Modelos contextuales para Formato B (Reflexivo contextual: ~50-85 palabras)
# Estructura: Situación humana + reflexión contextual + cita bíblica relevante + invitación natural.
FORMAT_B_BLUEPRINTS: Dict[str, Dict[str, str]] = {
    "lost_child": {
        "situation": "When a son or daughter feels distant, worry can quietly take over an entire evening. We replay old conversations, wondering what we could have said differently.",
        "reflection": "Yet love does not stop at the doorway. In Scripture, the father watched the horizon with patience, ready to welcome rather than condemn.",
        "scripture_quote": "Luke 15:20 (NIV) — 'While he was still a long way off, his father saw him and was filled with compassion for him.'",
        "invitation": "Where your voice cannot reach tonight, trust that God's quiet mercy is already at work. Hold steady in faithful hope."
    },
    "family_protection": {
        "situation": "Our homes absorb all the friction and fatigue of demanding workdays and restless schedules.",
        "reflection": "True peace is not the absence of busyness, but the quiet assurance of God's presence dwelling in every room. When we invite Christ to shelter our household, tension gives way to understanding.",
        "scripture_quote": "Psalm 91:11 (NIV) — 'For he will command his angels concerning you to guard you in all your ways.'",
        "invitation": "May deep, restorative rest cover your loved ones tonight as you commit this house into the Father's keeping."
    },
    "medical_fear": {
        "situation": "Waiting for medical answers or managing physical vulnerability can make ordinary hours feel painfully long.",
        "reflection": "It is completely natural to feel uncertain, but uncertainty does not mean you are walking alone. God's strength is made visible not when we feel invincible, but right in the middle of our weakness.",
        "scripture_quote": "2 Corinthians 12:9 (NIV) — 'My grace is sufficient for you, for my power is made perfect in weakness.'",
        "invitation": "Release tomorrow's unknowns into His faithful hands. You are surrounded by prayers and held in unfailing grace tonight."
    },
    "zero_balance": {
        "situation": "When bills arrive faster than paychecks, the pressure can feel overwhelming before bedtime.",
        "reflection": "Financial strain can easily tempt us to question our worth, but your value was never determined by a balance sheet. God knows every honest obligation you face and promises to sustain those who walk faithfully.",
        "scripture_quote": "Philippians 4:19 (NIV) — 'And my God will meet all your needs according to the riches of his glory in Christ Jesus.'",
        "invitation": "Take a calm breath tonight. One hard month does not write your whole story; trust God for tomorrow's provision."
    },
    "night_anxiety": {
        "situation": "The quiet of the night often amplifies worries that stayed hidden during a busy day.",
        "reflection": "Replaying tomorrow's challenges before sleep only drains the strength you need to meet them. Faith invites us to trade our restless calculations for the steady stillness of prayer.",
        "scripture_quote": "Philippians 4:6-7 (NIV) — 'Do not be anxious about anything, but in every situation present your requests to God.'",
        "invitation": "May the peace of God, which surpasses all human understanding, quiet your mind and give you restorative sleep tonight."
    },
    "morning_favor": {
        "situation": "Starting the day with an overcrowded schedule can leave our hearts hurried before we even step out the door.",
        "reflection": "Setting aside even two minutes of quiet reverence anchors our perspective in eternal truth. Today's challenges will come, but so will God's timely mercies.",
        "scripture_quote": "Lamentations 3:22-23 (ESV) — 'The steadfast love of the Lord never ceases; his mercies are new every morning.'",
        "invitation": "Step forward with quiet confidence today, knowing that God's favor and guidance go before you."
    },
    "marriage_healing": {
        "situation": "Two people can share the same roof while feeling miles apart inside their thoughts.",
        "reflection": "Reconciliation rarely happens through dramatic speeches; it is rebuilt through small choices of kindness, patience, and the humility to listen. Christ's forgiveness gives us the pattern to begin again.",
        "scripture_quote": "Colossians 3:13 (NIV) — 'Bear with each other and forgive one another if any of you has a grievance against someone.'",
        "invitation": "May God soften any lingering bitterness and grant you both the grace to rebuild warmth and understanding."
    },
    "healing_depression": {
        "situation": "Some mornings and evenings require a quiet bravery that goes completely unnoticed by those around us.",
        "reflection": "Weariness of the spirit is not a spiritual failure; it is human frailty asking for God's gentle touch. The Lord never looks away from a heavy heart, nor does He rush your healing.",
        "scripture_quote": "Psalm 34:18 (NIV) — 'The Lord is close to the brokenhearted and saves those who are crushed in spirit.'",
        "invitation": "Take life one gentle step at a time today, resting in the certainty that you are deeply and eternally loved."
    },
    "job_breakthrough": {
        "situation": "Enduring repeated job rejections can quietly erode confidence and breed anxiety about the future.",
        "reflection": "A closed door is not a final verdict on your skills or your worth before God. When human understanding falls short, divine guidance is often directing your steps toward a more purposeful alignment.",
        "scripture_quote": "Proverbs 3:5-6 (NIV) — 'Trust in the Lord with all your heart and lean not on your own understanding.'",
        "invitation": "Keep planting honest seeds with perseverance. Trust that the right opportunity is being prepared for you."
    },
    "lonely_widow": {
        "situation": "Quiet evenings can carry a sharp ache when an empty chair reminds you of someone dearly missed.",
        "reflection": "Grief does not follow a timeline, and honoring deep love means allowing yourself to feel both the sorrow and the gratitude. God draws near as a tender defender and faithful companion in the silence.",
        "scripture_quote": "Psalm 68:5 (NIV) — 'A father to the fatherless, a defender of widows, is God in his holy dwelling.'",
        "invitation": "May His living comfort warm your home tonight, reminding you that your loved one is safe and your life still holds purpose."
    },
    "addiction_chains": {
        "situation": "Breaking free from habits and dependencies is rarely an easy, straight road.",
        "reflection": "Real spiritual victory happens in the small, honest choices made every single day. When shame whispers that you cannot change, God's grace declares that true freedom has already been purchased for you.",
        "scripture_quote": "John 8:36 (NIV) — 'So if the Son sets you free, you will be free indeed.'",
        "invitation": "Do not face this battle in isolation. Lean on God's strength and healthy support for the next faithful step."
    },
    "elderly_parents": {
        "situation": "Balancing personal responsibilities while caring for an aging mother or father demands immense emotional stamina.",
        "reflection": "Seeing someone who once guided you now need your assistance is tender and exhausting. God honors every unseen sacrifice of patience, and He promises to sustain our loved ones to the very end.",
        "scripture_quote": "Isaiah 46:4 (NIV) — 'Even to your old age and gray hairs I am he, I am he who will sustain you.'",
        "invitation": "Rest your tired body tonight, knowing that your caregiving is a sacred reflection of God's steadfast love."
    },
    "single_parent": {
        "situation": "Carrying the entire weight of parenting, provision, and household care often leaves little time to catch your breath.",
        "reflection": "When energy is spent and demands continue, God does not ask you to manufacture strength. He promises to lift the weary and walk alongside those who faithfully raise the next generation.",
        "scripture_quote": "Isaiah 40:29 (NIV) — 'He gives strength to the weary and increases the power of the weak.'",
        "invitation": "Release the pressure to do everything perfectly. You are providing a faithful foundation, and God is with you."
    },
    "sick_grandchild": {
        "situation": "Few burdens feel heavier than watching a grandchild face illness while feeling helpless to ease their discomfort.",
        "reflection": "Even when distance or hospital rooms limit what you can do, your prayers are never bound by physical walls. Jesus holds little ones with boundless tenderness and hears every tear shed on their behalf.",
        "scripture_quote": "Matthew 19:14 (NIV) — 'Jesus said, Let the little children come to me, and do not hinder them.'",
        "invitation": "Rest in the gentle hands of the Great Physician tonight, trusting His healing touch and protective care over your grandchild."
    },
    "court_legal": {
        "situation": "Facing formal legal disputes or pending hearings brings heavy anxiety to mind and family.",
        "reflection": "Human systems can feel overwhelming, but God's sovereign justice and wisdom remain steadfast over your life. Committing your steps to Him brings clarity that outlasts legal turbulence.",
        "scripture_quote": "Psalm 37:5-6 (ESV) — 'Commit your way to the Lord; trust in him and he will act.'",
        "invitation": "May truth, fairness, and calm resolve guide every conversation and decision ahead."
    },
    "restless_sleep": {
        "situation": "Tossing and turning with a restless mind steals the restorative rest your body and spirit require.",
        "reflection": "Sleep is an act of trust—surrendering our illusion of control and admitting that God watches over the universe while we rest. You can close your eyes in full peace tonight.",
        "scripture_quote": "Psalm 4:8 (NIV) — 'In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.'",
        "invitation": "Turn off the lights, breathe out anxious thoughts, and allow God's peace to settle upon your heart tonight."
    },
    "gratitude_harvest": {
        "situation": "It is easy to focus on what feels missing or incomplete while overlooking the quiet mercies in our midst.",
        "reflection": "Cultivating daily thanksgiving reshapes how we experience both ordinary days and difficult trials. Gratitude opens our eyes to God's constant goodness in everyday life.",
        "scripture_quote": "1 Thessalonians 5:18 (NIV) — 'Give thanks in all circumstances; for this is God's will for you in Christ Jesus.'",
        "invitation": "Name three simple gifts from today and let quiet gratitude anchor your heart in joy."
    },
    "unspoken_prayer": {
        "situation": "There are times when pain or exhaustion is so deep that finding words to pray feels almost impossible.",
        "reflection": "True prayer is not measured by eloquence. The Holy Spirit searches the deepest chambers of our hearts, translating every silent sigh into a compassionate plea before the Father.",
        "scripture_quote": "Romans 8:26 (NIV) — 'The Spirit helps us in our weakness, interceding with groans that words cannot express.'",
        "invitation": "You do not need an elaborate prayer tonight. Simply resting in God's presence is enough; He knows."
    },
    "spiritual_warfare": {
        "situation": "When self-doubt, fear, and spiritual opposition attempt to erode your confidence in God's goodness.",
        "reflection": "Courage is not the absence of intimidation, but the decision to stand on God's truth regardless of how loud fear sounds. The Lord is your faithful shield and reliable fortress.",
        "scripture_quote": "2 Thessalonians 3:3 (NIV) — 'The Lord is faithful, and he will strengthen you and protect you from the evil one.'",
        "invitation": "Stand firm in the promises of Scripture tonight. Fear has no authority over those who walk with Christ."
    },
    "business_blessing": {
        "situation": "Navigating the demands of commerce, client expectations, and financial risk requires constant wisdom.",
        "reflection": "Operating with uncompromising integrity and diligence honors God in the marketplace. When we commit our business endeavors to His direction, He establishes purposeful and lasting outcomes.",
        "scripture_quote": "Proverbs 16:3 (NIV) — 'Commit to the Lord whatever you do, and he will establish your plans.'",
        "invitation": "May God bless your honest labor, grant you sound discernment, and open doors of fruitful service."
    },
    "forgiving_past": {
        "situation": "Memories of past betrayal or unfair treatment can resurface, tempting us to harbor old resentments.",
        "reflection": "Forgiveness does not mean excusing wrongful actions or removing necessary boundaries; it means releasing the emotional debt so bitterness no longer controls your peace. Christ empowers us to let go.",
        "scripture_quote": "Ephesians 4:32 (NIV) — 'Be kind and compassionate to one another, forgiving each other, just as in Christ God forgave you.'",
        "invitation": "Choose the quiet path of freedom tonight. Release the past into God's hands and walk forward unburdened."
    },
    "grief_loss": {
        "situation": "Walking through the valley of bereavement changes everyday routines and brings sudden waves of sorrow.",
        "reflection": "Grief is sacred because it honors the depth of love shared with someone now in God's presence. Jesus does not hurry your mourning; He meets your tears with tender comfort and eternal hope.",
        "scripture_quote": "Matthew 5:4 (NIV) — 'Blessed are those who mourn, for they will be comforted.'",
        "invitation": "May the peace of Christ embrace your tender heart tonight as you remember with gentle love."
    },
    "guidance_direction": {
        "situation": "Facing major life choices when multiple options carry uncertainty can paralyze our peace of mind.",
        "reflection": "Wisdom is rarely handed down as a complete roadmap; God provides light for the immediate next step. As you seek Him in quiet trust, He promises to direct your thoughts and align your way.",
        "scripture_quote": "Psalm 32:8 (NIV) — 'I will instruct you and teach you in the way you should go; I will counsel you with my loving eye upon you.'",
        "invitation": "Trust that God is already preparing the right path. Move forward with calm and patient discernment."
    },
    "strength_weary": {
        "situation": "Prolonged seasons of responsibility and endurance can drain emotional and physical reserves to the bottom.",
        "reflection": "Human stamina has its natural limits, but God's supply of renewal is never exhausted. Waiting on the Lord does not mean passive inaction; it means placing your reliance squarely on His sustaining power.",
        "scripture_quote": "Isaiah 40:31 (NIV) — 'Those who hope in the Lord will renew their strength. They will soar on wings like eagles.'",
        "invitation": "Set aside your striving tonight. Allow God to replenish your spirit and renew your strength for the days ahead."
    },
    "peace_in_storm": {
        "situation": "When unexpected news or personal upheaval shakes your routine like a sudden squall at sea.",
        "reflection": "The waves may be noisy and turbulent, but Jesus is always present in the boat with you. His word speaks calm to the deepest unrest, reminding us that no circumstance is beyond His sovereign peace.",
        "scripture_quote": "Mark 4:39 (NIV) — 'He got up, rebuked the wind and said to the waves, Quiet! Be still! Then the wind died down.'",
        "invitation": "Fix your eyes on the Savior rather than the storm. Let His quiet assurance steady your heart tonight."
    },
    "divine_grace": {
        "situation": "When guilt over past failures tries to convince you that you have disqualified yourself from God's favor.",
        "reflection": "Grace is never earned by human perfection; it is freely poured out through Christ's sacrifice. No matter where today found you, God invites you to step directly into His presence with humble confidence.",
        "scripture_quote": "Hebrews 4:16 (NIV) — 'Let us approach God's throne of grace with confidence, so that we may receive mercy in time of need.'",
        "invitation": "Receive His unfailing mercy tonight. Yesterday's shortcomings have no power over your tomorrow in Christ."
    }
}


# ─── 4. Generación de las Dos Modalidades de Descripción ──────────────────────

def generate_caption_format_a(
    theme_key: str,
    hook: str,
    body: str,
    cta: str = ""
) -> Tuple[str, int]:
    """
    Formato A — Breve emocional (~20–40 palabras sin hashtags).
    Estructura: situación humana concreta, mensaje de esperanza, invitación natural.
    Retorna (texto_descripcion, conteo_palabras).
    """
    blueprint = FORMAT_A_BLUEPRINTS.get(theme_key)
    if not blueprint:
        # Fallback contextual limpio si el tema no estuviera en el catálogo
        context = "For anyone walking through a quiet, demanding season today."
        message = "May God's gentle peace steady your steps and bring comfort to your home."
        invitation = "Rest in His faithful love tonight."
    else:
        context = blueprint["context"]
        message = blueprint["message"]
        # Si el usuario aprobó un CTA natural en el guion, adaptar invitación
        if cta and len(cta.split()) <= 12 and not any(w in cta.lower() for w in ["amen", "share", "type"]):
            invitation = cta.rstrip(".") + "."
        else:
            invitation = blueprint["invitation"]

    # Construir descripción fluida
    caption_text = f"{context} {message} {invitation}".strip()
    words = len(caption_text.split())

    # Asegurar rango ~20-40 palabras
    if words > 42:
        # Recortar elegantemente a nivel de oración
        sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", caption_text) if s.strip()]
        if len(sentences) >= 2:
            caption_text = " ".join(sentences[:2])
            words = len(caption_text.split())

    return caption_text, words


def generate_caption_format_b(
    theme_key: str,
    hook: str,
    body: str,
    scripture: str = "",
    cta: str = ""
) -> Tuple[str, int]:
    """
    Formato B — Reflexivo contextual (~50–85 palabras sin hashtags).
    Estructura: situación humana, breve reflexión contextual, referencia bíblica pertinente, invitación natural.
    Retorna (texto_descripcion, conteo_palabras).
    """
    blueprint = FORMAT_B_BLUEPRINTS.get(theme_key)
    if not blueprint:
        situation = "When life brings quiet burdens that few people see, fatigue can set in quickly."
        reflection = "God invites us to bring every concern into His presence, where His steady compassion renews our strength."
        scripture_quote = scripture or "Philippians 4:6 (NIV) — 'In every situation present your requests to God.'"
        invitation = "May you experience deep peace and restful assurance tonight."
    else:
        situation = blueprint["situation"]
        reflection = blueprint["reflection"]
        scripture_quote = scripture or blueprint["scripture_quote"]
        if cta and len(cta.split()) <= 14 and not any(w in cta.lower() for w in ["amen", "type"]):
            invitation = cta.rstrip(".") + "."
        else:
            invitation = blueprint["invitation"]

    # Dar formato con saltos limpios para lectura en Facebook Reels
    caption_text = f"{situation}\n\n{reflection}\n\n{scripture_quote}\n\n{invitation}".strip()
    words = len(caption_text.split())

    return caption_text, words


# ─── 5. Ensamblador de Publicación Completa para Facebook Reels ─────────────────

def generate_optimized_social_post(
    theme_key: str,
    hook: str,
    body: str,
    scripture: str = "",
    cta: str = "",
    format_type: str = "A",       # "A" (breve) o "B" (reflexivo)
    hashtag_strategy: int = 3,    # 0, 3 o 5
    custom_tags: Optional[List[str]] = None
) -> Dict[str, Any]:
    """
    Ensambla la publicación completa para Facebook Reels basada en el guion final aprobado.
    Calcula el grupo experimental (A1-A3, B1-B3) y devuelve la estructura lista para copiar y auditar.
    """
    fmt = format_type.upper() if format_type in ["A", "B", "a", "b"] else "A"
    tags_count = int(hashtag_strategy) if hashtag_strategy in [0, 3, 5] else 3

    # Generar cuerpo según formato
    if fmt == "B":
        caption_body, word_count = generate_caption_format_b(theme_key, hook, body, scripture, cta)
    else:
        caption_body, word_count = generate_caption_format_a(theme_key, hook, body, cta)

    # Obtener hashtags
    hashtags = get_theme_hashtags(theme_key, strategy=tags_count, custom_tags=custom_tags)
    tags_str = " ".join(hashtags) if hashtags else ""

    # Determinar identificador de grupo experimental: A1, A2, A3, B1, B2, B3
    group_map = {
        ("A", 0): "A1",
        ("A", 3): "A2",
        ("A", 5): "A3",
        ("B", 0): "B1",
        ("B", 3): "B2",
        ("B", 5): "B3"
    }
    group_id = group_map.get((fmt, tags_count), f"{fmt}{tags_count}")

    # Título limpio en inglés
    from engine.editorial import english_title
    clean_title = english_title(theme_key)

    # Armar texto definitivo de la publicación
    parts = [f"✝️ {clean_title} ✝️", "", caption_body]
    if tags_str:
        parts.extend(["", tags_str])

    full_post_text = "\n".join(parts)

    return {
        "format_type": fmt,
        "hashtag_strategy": tags_count,
        "experiment_group": group_id,
        "title": clean_title,
        "caption_body": caption_body,
        "word_count": word_count,
        "hashtags": hashtags,
        "tags_string": tags_str,
        "full_post_text": full_post_text,
        "theme_key": theme_key
    }


# ─── 6. Matriz de Distribución Inicial para 18 Reels ───────────────────────────

# 3 temáticas clave para la fase inicial de experimentación:
# 1. Oración nocturna (night_anxiety / restless_sleep)
# 2. Padres e hijos adultos (lost_child / family_protection)
# 3. Dificultades económicas (zero_balance / job_breakthrough)

EXPERIMENT_MATRIX_18: List[Dict[str, Any]] = [
    # Ronda 1 (Reels 1 a 6) - Cobertura de las 6 estrategias
    {"slot": 1, "group": "A1", "theme_key": "night_anxiety", "slot_time": "20:30 EST", "format": "A", "tags": 0, "theme_label": "Oración nocturna"},
    {"slot": 2, "group": "A2", "theme_key": "lost_child", "slot_time": "12:30 EST", "format": "A", "tags": 3, "theme_label": "Padres e hijos adultos"},
    {"slot": 3, "group": "A3", "theme_key": "zero_balance", "slot_time": "08:30 EST", "format": "A", "tags": 5, "theme_label": "Dificultades económicas"},
    {"slot": 4, "group": "B1", "theme_key": "restless_sleep", "slot_time": "21:00 EST", "format": "B", "tags": 0, "theme_label": "Oración nocturna"},
    {"slot": 5, "group": "B2", "theme_key": "family_protection", "slot_time": "13:00 EST", "format": "B", "tags": 3, "theme_label": "Padres e hijos adultos"},
    {"slot": 6, "group": "B3", "theme_key": "job_breakthrough", "slot_time": "09:00 EST", "format": "B", "tags": 5, "theme_label": "Dificultades económicas"},

    # Ronda 2 (Reels 7 a 12) - Alternancia de temáticas y estrategias
    {"slot": 7, "group": "B1", "theme_key": "lost_child", "slot_time": "12:30 EST", "format": "B", "tags": 0, "theme_label": "Padres e hijos adultos"},
    {"slot": 8, "group": "B2", "theme_key": "zero_balance", "slot_time": "08:30 EST", "format": "B", "tags": 3, "theme_label": "Dificultades económicas"},
    {"slot": 9, "group": "B3", "theme_key": "night_anxiety", "slot_time": "20:30 EST", "format": "B", "tags": 5, "theme_label": "Oración nocturna"},
    {"slot": 10, "group": "A1", "theme_key": "family_protection", "slot_time": "13:00 EST", "format": "A", "tags": 0, "theme_label": "Padres e hijos adultos"},
    {"slot": 11, "group": "A2", "theme_key": "job_breakthrough", "slot_time": "09:00 EST", "format": "A", "tags": 3, "theme_label": "Dificultades económicas"},
    {"slot": 12, "group": "A3", "theme_key": "restless_sleep", "slot_time": "21:00 EST", "format": "A", "tags": 5, "theme_label": "Oración nocturna"},

    # Ronda 3 (Reels 13 a 18) - Cierre balanceado
    {"slot": 13, "group": "A1", "theme_key": "zero_balance", "slot_time": "08:30 EST", "format": "A", "tags": 0, "theme_label": "Dificultades económicas"},
    {"slot": 14, "group": "A2", "theme_key": "night_anxiety", "slot_time": "20:30 EST", "format": "A", "tags": 3, "theme_label": "Oración nocturna"},
    {"slot": 15, "group": "A3", "theme_key": "lost_child", "slot_time": "12:30 EST", "format": "A", "tags": 5, "theme_label": "Padres e hijos adultos"},
    {"slot": 16, "group": "B1", "theme_key": "job_breakthrough", "slot_time": "09:00 EST", "format": "B", "tags": 0, "theme_label": "Dificultades económicas"},
    {"slot": 17, "group": "B2", "theme_key": "restless_sleep", "slot_time": "21:00 EST", "format": "B", "tags": 3, "theme_label": "Oración nocturna"},
    {"slot": 18, "group": "B3", "theme_key": "family_protection", "slot_time": "13:00 EST", "format": "B", "tags": 5, "theme_label": "Padres e hijos adultos"}
]


def get_next_recommended_experiment(existing_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Determina la siguiente estrategia recomendada según los registros existentes
    para mantener el equilibrio entre los 6 grupos y las 3 temáticas.
    """
    total_completed = len(existing_records or [])
    slot_index = total_completed % len(EXPERIMENT_MATRIX_18)
    return EXPERIMENT_MATRIX_18[slot_index]
