# -*- coding: utf-8 -*-
"""
Catálogo de Variaciones Narrativas y Oraciones Dinámicas para JesusReels Studio.
Garantiza diversidad real de narraciones en cada regeneración de guion para los 26 temas canónicos.
Audencia: Adult US English, tono íntimo, reflexivo, bíblico y consolador.
"""

from typing import Dict, List, Optional
import random

THEME_PRAYER_VARIATIONS: Dict[str, List[str]] = {
    "lost_child": [
        "Lord, You know every step my child takes. Where my voice cannot go, let Your quiet mercy meet them. Protect their life, guard their conscience, and remind them that they remain deeply loved.",
        "Heavenly Father, I place my child into Your faithful hands tonight. Where I cannot see, watch over them. Soften any hardness in their heart, shield them from harm, and draw them gently back to Your peace.",
        "Lord Jesus, no distance can keep my child from Your reach. When they feel lost or alone in the world, speak stillness to their mind and whisper that home is never closed to them.",
        "Father, You understand the quiet ache of a parent waiting by the window. Guard my son and daughter tonight wherever they walk, surround them with godly friends, and let Your grace lead them safely home.",
        "Lord, I release my worry and choose to trust Your unfailing love for my child. Walk beside them in the shadows, protect their steps, and let them know they are forever treasured in Your sight."
    ],
    "family_protection": [
        "Father, place a gentle hedge of peace around this home tonight. Silence anxious thoughts upon our pillows, mend tired tempers with kindness, and let Your quiet rest cover every room.",
        "Lord God, we dedicate our household to Your care this evening. Station Your angels at our doors, drive out all fear and contention, and let everyone under this roof sleep under the shadow of Your wings.",
        "Jesus, be the unseen guest at our table and the peaceful guard at our door tonight. Comfort every weary heart in this home, heal unspoken disagreements, and grant us restorative rest for tomorrow.",
        "Heavenly Father, cover our children and loved ones with Your divine shield tonight. Let no sickness, harm, or restlessness enter our dwelling, but fill each room with Your gentle, comforting presence.",
        "Lord, when the world outside feels turbulent, let our home remain an anchor of quiet grace. Guard our coming and going, keep our minds steadfast on You, and shelter our family in everlasting peace."
    ],
    "medical_fear": [
        "Lord Jesus, You know what it is to walk through human pain. Touch the places that feel exhausted. Grant wisdom to physicians, quiet patience to the heart, and gentle relief for the hours ahead.",
        "Father, when medical test results make tomorrow feel uncertain, anchor my trembling heart in Your love. Calm the racing thoughts, soothe every ache, and remind me that my days are written in Your hands.",
        "Lord, You are the Great Physician who binds up wounds and restores the weary. Breathe Your healing peace through my body right now, replace fear with steadfast faith, and grant me restful sleep tonight.",
        "Heavenly Father, I bring my health and physical limitations to Your throne of grace. Take away the anxiety of what might happen next, give doctors divine insight, and wrap me in Your tender mercy.",
        "Jesus, when my body feels frail, be my strength. Dispel the cold shadow of fear from my thoughts, place Your healing hand over my pain, and grant me courage for every step of this journey."
    ],
    "zero_balance": [
        "Father, You know every practical need in this home. When numbers do not seem to add up, give us wisdom, open honest doors, and deliver us from the fear of tomorrow.",
        "Lord, You feed the birds of the air and clothe the lilies of the field. I place my empty bank balance and overdue bills before You, trusting that You will provide our daily bread one step at a time.",
        "Heavenly Father, relieve the knot of financial worry that weighs on my chest tonight. Guide my hands in honest work, multiply our small resources, and remind me that my worth is secure in You.",
        "Jesus, You walked this earth knowing humble means and daily trust. Open doors of opportunity that no one can shut, give me wisdom to steward each dollar, and grant peace to our household.",
        "Lord, when financial pressure threatens to rob my sleep, I choose to rest in Your faithful promise. You have carried us through difficult seasons before, and You will faithfully sustain us today."
    ],
    "night_anxiety": [
        "Lord, quiet the storm of racing thoughts in my mind. You hold the hours of the night in Your hand. Help me release the things I cannot change and receive Your sweet gift of rest.",
        "Father, as the darkness settles outside, let Your light settle inside my heart. Still the replaying worries of today, quiet every hypothetical fear of tomorrow, and grant me deep, uninterrupted sleep.",
        "Jesus, take this heavy tension from my shoulders and chest. I surrender every unresolved problem into Your hands right now, knowing You neither slumber nor sleep while I rest in Your care.",
        "Heavenly Father, speak 'peace, be still' over my mind tonight. Let Your presence banish the lonely silence of the midnight hour, and let me wake up refreshed by Your morning compassions.",
        "Lord, I breathe out the restlessness of this day and breathe in Your quiet presence. Guard my dreams, protect my thoughts, and wrap my spirit in the comforting warmth of Your grace."
    ],
    "morning_favor": [
        "Heavenly Father, guide my words and my decisions today. Guard my heart from impatience, give me eyes to notice who needs encouragement, and let Your steady wisdom lead my footsteps.",
        "Lord, thank You for the breath in my lungs and the fresh mercies waiting with this sunrise. Align my priorities with Your will, open doors of favor, and let my work bring honor to Your name.",
        "Jesus, walk ahead of me into every meeting, conversation, and challenge today. Clothe me with kindness, grant me discernment in every choice, and let Your peace radiate through my actions.",
        "Father, before the noise of the day begins, I center my soul on Your goodness. Renew my strength, protect my mind from distraction, and let Your blessing rest upon my family and labor.",
        "Lord, establish the work of our hands today. Give me patience with difficult moments, gratitude in ordinary routines, and the quiet joy of knowing You are with me in every hour."
    ],
    "marriage_healing": [
        "Lord Jesus, come and heal what feels broken between us. Remove the walls of resentment, soften our words with gentleness, and teach us how to forgive as You have generously forgiven us.",
        "Father, restore the warmth, patience, and mutual respect that once marked our marriage. Help us listen without defensiveness, heal the wounds of past arguments, and rebuild trust day by day.",
        "Heavenly Father, when misunderstandings cause distance in our home, breathe Your peace into our hearts. Remind us of the covenant we made, and bind our hearts together with Your unconditional love.",
        "Lord, give my spouse and me the courage to choose humility over pride tonight. Silence harsh thoughts, rekindle genuine affection, and let our marriage be a sanctuary of safety and grace.",
        "Jesus, where coldness has crept in, bring Your healing warmth. Teach us to extend grace in moments of irritation, help us speak life to one another, and protect our union from all harm."
    ],
    "healing_depression": [
        "Lord, when getting out of bed feels overwhelming, be my quiet strength. You see the tears that fall in secret, and You understand the exhaustion of my spirit. Meet me with gentle compassion today.",
        "Father, even when hope feels distant and my soul feels heavy, I cling to the truth that You are near the brokenhearted. Lift the gray fog from my mind one moment at a time.",
        "Jesus, You walked through deep sorrow and know the weight of a troubled soul. Do not let me believe the lie that I am alone. Breathe life, dignity, and quiet peace into my weary spirit.",
        "Heavenly Father, give me grace for today without demanding that I solve everything at once. Remind me that struggling does not mean failing, and that Your loving hands are holding me steady.",
        "Lord, shine a gentle ray of light into the dark corners of my heart. Give me strength for the next small step, quiet the self-condemnation, and let Your unconditional love restore my soul."
    ],
    "job_breakthrough": [
        "Father, You see every application sent and every quiet disappointment along the way. Remind me that my worth is not measured by a job title, and open the right door in Your perfect timing.",
        "Lord Jesus, lead me to honest work where my skills can provide for my household and bless others. Give me favor in interviews, grant wisdom to employers, and renew my confidence today.",
        "Heavenly Father, when waiting for an answer tests my endurance, keep my hope steadfast. Provide for our daily needs during this lean season, and guide my steps toward purposeful employment.",
        "Lord, I release anxiety over unanswered emails and closed doors. I trust that what You have prepared for me will not pass me by. Strengthen my resolve and grant me favor in the marketplace.",
        "Father, sustain my dignity as I seek work. Grant me clarity to spot new opportunities, courage to step through unfamiliar doors, and the assurance that You remain my ultimate provider."
    ],
    "lonely_widow": [
        "Lord Jesus, You are the defender of the lonely and the faithful companion of the grieving. When the house feels quiet and the empty chair brings tears, fill this room with Your comforting presence.",
        "Father, thank You for the cherished years and beautiful memories of my loved one. In moments when loneliness feels heavy, wrap me in Your eternal arms and remind me that I am never forsaken.",
        "Heavenly Father, be my comfort in the quiet evenings. Send kind neighbors and loving friends across my path, warm my heart with Your sweet peace, and sustain me with Your daily grace.",
        "Lord, You bottle every tear shed in the stillness of the night. Comfort my heart when longing for companionship aches, and remind me of the eternal joy waiting in Your presence.",
        "Jesus, walk through this home with me today. Let Your peace fill the silence, renew my purpose for tomorrow, and remind me that Your love remains faithful to the very end."
    ],
    "addiction_chains": [
        "Lord Jesus, break the heavy chains that have bound my thoughts and habits. Where human willpower falls short, let Your miraculous grace deliver me. Grant me courage for one clean hour at a time.",
        "Father, I bring my deepest struggle into Your forgiving light. Cleanse the shame from my soul, give me strength to resist temptation, and surround me with people who support my recovery.",
        "Heavenly Father, when old cravings whisper in moments of loneliness or stress, be my immediate refuge. Fill the empty spaces in my heart with Your Holy Spirit and give me victory today.",
        "Lord, You came to set the captives free. Tear down the lies that tell me I cannot change. Renew my mind, heal the underlying pain, and walk with me along this path of authentic freedom.",
        "Jesus, give me the humble strength to take one honest step today. When I feel weak, let Your power be made perfect in my vulnerability, and restore what the years of struggle have stolen."
    ],
    "elderly_parents": [
        "Lord, give me gentle patience and endurance as I care for my aging parents. When physical weariness catches up with me, renew my compassion and help me honor them with dignity and warmth.",
        "Heavenly Father, sustain my mother and father in their golden years. Comfort their physical aches, grant them peace in their minds, and let them feel deeply cherished by our family.",
        "Jesus, You honored Your mother even from the cross. Teach me how to balance daily responsibilities while being present for my parents with kindness, unhurried time, and a servant's heart.",
        "Father, grant wisdom to our family as we make difficult care decisions. Provide the practical resources we need, soothe the grief of watching health decline, and bind our hearts in love.",
        "Lord, let Your gentle peace rest over my elderly parents tonight. Guard their sleep, bless them with peaceful thoughts, and reward their faithful years with Your loving presence."
    ],
    "single_parent": [
        "Lord, You know the heavy load of carrying both roles alone. When energy runs low and the to-do list feels endless, be my supernatural strength, my constant provider, and my quiet peace.",
        "Father, watch over my precious children while I am working hard to provide. Place Your protective shield around their minds, grant me patience during chaotic moments, and let our home be full of laughter.",
        "Heavenly Father, remind me that I am not raising my children alone; You are walking beside us in every room. Multiply our groceries, grant restful sleep tonight, and renew my joy in parenting.",
        "Jesus, when fatigue threatens to make me feel inadequate, whisper that Your grace is sufficient. Bless my children with wisdom and kindness, and let them see Your faithfulness through our home.",
        "Lord, hold my heart steady tonight. Release the guilt of things left undone today, restore my spirit in the stillness of the night, and let tomorrow bring fresh energy and divine favor."
    ],
    "sick_grandchild": [
        "Lord Jesus, You took the little children into Your arms and blessed them. Place Your healing hand upon my precious grandchild right now. Rebuke the fever, restore their strength, and comfort our family.",
        "Father, my heart aches to see my grandchild unwell. Give wisdom to the doctors, peace to their worried parents, and let Your healing touch bring swift relief to their small, precious body.",
        "Heavenly Father, be near the bedside of our little one tonight. Soothe their pain, grant them peaceful sleep, and let them wake with bright eyes, renewed appetite, and a joyful smile.",
        "Jesus, Great Physician, I surrender my worry into Your loving hands. Guard my grandchild's health from all complications, restore full vitality, and fill their room with Your gentle angels.",
        "Lord, we pray for complete recovery and restoration for our grandchild. Comfort their weary parents tonight, strengthen our family's faith, and let this sickness quickly become a testimony of Your grace."
    ],
    "court_legal": [
        "Lord God of justice and truth, I place this legal burden and unresolved proceeding into Your righteous hands. Disclose the truth, silence false accusations, and let fairness prevail.",
        "Father, when legal paperwork and court dates cause anxiety to rise, be my steadfast defense. Grant wisdom and integrity to attorneys, discernment to judges, and peace to my spirit.",
        "Heavenly Father, deliver me from the fear of an unjust outcome. You are the ultimate Judge who sees every hidden motive. Vindicate what is right and bring a peaceful resolution soon.",
        "Jesus, give me dignified calm as I navigate this legal trial. Protect my family from unnecessary harm, provide the financial resources needed, and let Your righteousness shine bright.",
        "Lord, I commit my cause and tomorrow's decisions to You. Silence malicious words, establish truth in the courtroom, and let Your supernatural peace guard my heart and mind through it all."
    ],
    "restless_sleep": [
        "Father, I bring my tired eyes and racing mind to Your altar of peace tonight. Silence the internal chatter, release the muscle tension from my body, and grant me sweet, deep, restorative sleep.",
        "Lord Jesus, You slept peacefully in the middle of a raging storm. Speak that same calm over my restless mind tonight. Let no anxious dream disturb me, but cradle my spirit in Your rest.",
        "Heavenly Father, the day is done and its demands are closed. I leave every unanswered question in Your hands. Cover my bed in Your quiet safety and let me wake with renewed vitality.",
        "Lord, when insomnia tries to steal my strength, remind me that You are watching over my life. Relax my breathing, still my heart, and let Your comforting presence carry me into deep sleep.",
        "Jesus, bless this bedroom with Your heavenly serenity tonight. Send away all restlessness and worry, and let Your enduring peace be the blanket that warms my soul until the dawn."
    ],
    "gratitude_harvest": [
        "Lord, my heart overflows with thanksgiving as I count the blessings of this season. Thank You for the trials that refined my faith, the doors You opened, and the faithful provision that never failed.",
        "Heavenly Father, I pause today simply to say thank You. For daily bread, for family and shelter, and for the quiet ways You protected me from unseen dangers, I give You all the glory.",
        "Jesus, thank You for turning weeping into dancing and sorrow into joy. Help me never forget where You brought me from, and teach me to share Your generous abundance with those in need.",
        "Father, every good and perfect gift comes from Your gracious hand. I celebrate Your goodness today, dedicating the fruit of my labor to Your kingdom, and rejoicing in Your constant love.",
        "Lord, let gratitude be the constant song of my heart. In abundance or in scarcity, You have proven Yourself faithful, and I worship You with a humble, joyful, and thankful spirit today."
    ],
    "unspoken_prayer": [
        "Lord, You know the ache that has no words and the prayer I cannot speak aloud. Read the silent cry of my heart tonight, and let Your Holy Spirit intercede on my behalf with groanings too deep for speech.",
        "Father, when sorrow or perplexity makes my words fail, I rest in the truth that You already understand. Comfort the secret place of my soul, heal what is tender, and grant me Your gentle peace.",
        "Jesus, You see the private burden I carry that nobody else knows about. Where human understanding stops, let Your divine compassion begin. Deliver me, sustain me, and wipe away my secret tears.",
        "Heavenly Father, I sit quietly before You without rehearsed speeches. You know my frame; You remember that I am dust. Pour Your soothing oil over my heart and answer the cry I cannot utter.",
        "Lord, receive the quiet sigh of my spirit tonight. Bring resolution to the situation only You and I know, strengthen my inner man, and assure me that You are already working all things for good."
    ],
    "spiritual_warfare": [
        "Lord Jesus, I stand firm in the authority of Your holy name. Clothe me in the full armor of God tonight: the helmet of salvation, the breastplate of righteousness, and the shield of faith.",
        "Father, rebuke every spiritual attack, every whisper of condemnation, and every scheme of the enemy aimed at my household. Establish Your divine hedge of holy angels around our lives.",
        "Jesus, You disarmed the powers of darkness on the cross and triumph over every fear. We declare that no weapon formed against our family or faith shall prosper, for our protector is the Lord.",
        "Heavenly Father, fill our home with the light of Your Holy Spirit. Break every heavy oppression, shatter fear and doubt, and let the peace of Christ reign supreme over every heart tonight.",
        "Lord, when spiritual resistance feels intense, remind me that greater is He who is in me than he who is in the world. I walk in Your victory, clothed in Your strength, unwavering in faith."
    ],
    "business_blessing": [
        "Father, I dedicate my work, business, and daily enterprise to Your glory. Grant me wisdom to make honest decisions, integrity in dealing with customers, and favor in the marketplace.",
        "Lord Jesus, bless the labor of my hands and the services we offer. Open doors to faithful clients, provide the resources to meet payroll and obligations, and let our business bless our community.",
        "Heavenly Father, when economic uncertainties arise, be our chief counselor. Guide our planning, protect us from deceitful contracts, and grant fruitfulness to our honest, hard work.",
        "Lord, help me honor You in how I lead, work, and treat others each day. Multiply what we plant with diligence, keep our motives pure, and let Your favor rest upon our business journey.",
        "Jesus, You worked as a carpenter with skill and honor. Give me excellence in my craft, resilience during slow seasons, and the quiet assurance that You establish the plans committed to You."
    ],
    "forgiving_past": [
        "Lord Jesus, heal the painful memories and old scars that still sting when remembered. Give me the supernatural grace to release those who hurt me, breaking the hold of bitterness over my heart.",
        "Father, forgiveness is hard, but holding onto resentment is heavier. I choose to open my hands today and entrust the offender to Your righteous judgment, stepping into Your freedom and peace.",
        "Heavenly Father, clean every root of bitterness from my thoughts. Where betrayal left deep wounds, pour the soothing balm of Your love, and help me walk with an unburdened, joyful heart.",
        "Jesus, You forgave those who nailed You to the cross. Teach my heart that same divine mercy. Set me free from replaying past offenses, and let Your peace become my permanent dwelling place.",
        "Lord, I surrender the right to get even. I choose healing over grudge, grace over anger, and love over regret. Thank You for setting my soul completely free today."
    ],
    "grief_loss": [
        "Lord Jesus, You wept at the tomb of Lazarus and You weep with me in this painful loss. Wrap Your everlasting arms around my shattered heart and give me strength to endure this deep grief.",
        "Father, when memories of my loved one bring sudden tears and the empty space feels overwhelming, be my refuge. Remind me of the eternal hope we share through the resurrection of Christ.",
        "Heavenly Father, comfort my family in this season of mourning. Give us grace to remember with gratitude, patience to walk through the waves of sorrow, and faith that love never dies.",
        "Jesus, You promised that blessed are those who mourn, for they shall be comforted. Fulfill that promise in my soul today. Breathe peace into the ache, and sustain me one day at a time.",
        "Lord, hold my hand through the lonely valleys of bereavement. Keep my eyes anchored on eternity, wipe away the bitter tears, and remind me of the joyful reunion waiting in Your presence."
    ],
    "guidance_direction": [
        "Heavenly Father, I stand at a crossroads and need Your divine clarity. Close every door that leads away from Your will, and open wide the path where Your blessing and wisdom dwell.",
        "Lord Jesus, be the lamp to my feet and the light to my path today. Silence conflicting human opinions, quiet my own impulsive desires, and let Your Holy Spirit whisper the right way forward.",
        "Father, when both options seem uncertain, grant me the peace that surpasses understanding as a signpost for my decisions. Give me courage to step out in faith without fear.",
        "Lord, I commit my future plans and tomorrow's steps completely into Your hands. Direct my thoughts, surround me with wise counsel, and establish the steps that honor Your purpose for my life.",
        "Jesus, Good Shepherd, lead me beside still waters and guide my paths for Your name's sake. Keep me from making decisions out of panic, and anchor my heart in Your perfect timing."
    ],
    "strength_weary": [
        "Father, I am running on empty and my physical and emotional strength is spent. Fulfill Your promise to renew the strength of the weary. Help me soar on wings like eagles and walk without fainting.",
        "Lord Jesus, You invited all who are weary and heavy laden to come to You for rest. I bring my exhausted body and burdened mind to Your feet right now. Give me supernatural renewal.",
        "Heavenly Father, when life demands more than I feel capable of giving, be my rock and my fortress. Lift the heavy fatigue from my soul, restore my passion, and grant me restful sleep tonight.",
        "Lord, teach me how to rest in Your grace rather than striving in my own limited power. Quiet my spirit, replenish my inner energy, and let Your joy be my unshakeable strength today.",
        "Jesus, breathe fresh life into my tired bones. Remind me that I do not walk alone, and that Your grace is made perfect in my weakness. Sustain me with Your unfailing hand."
    ],
    "peace_in_storm": [
        "Lord Jesus, when winds of crisis howl and the waves threaten to overwhelm my life, stand tall in my boat and speak 'Peace, be still!' Anchor my soul firmly in Your sovereign control.",
        "Father, though the news around me is shaking and circumstances feel chaotic, I fix my eyes on You. Grant me a tranquil heart, steady hands, and the certainty that You rule above the flood.",
        "Heavenly Father, be my shelter in the time of storm. Hide me under the shadow of Your wings until the calamity passes by, and let Your unshakeable peace guard my thoughts tonight.",
        "Jesus, Prince of Peace, quiet the inner turbulence of fear and anxiety. Remind me that the storm is subject to Your command, and that no circumstance can separate me from Your love.",
        "Lord, I will not be afraid though the earth give way. You are my refuge, my strength, and a very present help in trouble. I rest securely in Your mighty, loving hands today."
    ],
    "divine_grace": [
        "Heavenly Father, I come boldly to Your throne of grace, knowing I am accepted not by my own perfection, but through the finished work of Jesus Christ. Wash away my faults and renew my heart.",
        "Lord Jesus, Your mercy is higher than the heavens and deeper than the sea. When my conscience accuses me of past mistakes, remind me that there is now no condemnation for those in Christ.",
        "Father, thank You that Your love is unconditional and Your forgiveness is complete. Clothe me in Your righteousness today, give me a clean spirit, and let me walk in joyful freedom.",
        "Jesus, when I feel unworthy or broken, Your cross reminds me of my immense worth in Your sight. Help me extend that same lavish grace, patience, and forgiveness to everyone I encounter today.",
        "Lord, let Your grace be my daily dwelling place. Teach me to rely on Your mercy rather than my own efforts, and let my life be a living reflection of Your boundless goodness and love."
    ]
}


def get_candidate_bodies_for_theme(theme_key: str, tone: Optional[str] = None) -> List[str]:
    """
    Retorna la lista completa de oraciones candidatas para una temática.
    Garantiza variedad amplia (~5 variaciones principales) listas para filtrar contra el historial.
    """
    variations = THEME_PRAYER_VARIATIONS.get(theme_key, [])
    if not variations:
        return [
            "Lord, cover our home in Your gentle peace, guard our loved ones, and grant us restorative rest tonight.",
            "Heavenly Father, we place every anxious thought into Your loving hands, trusting Your constant care.",
            "Jesus, be our refuge in the storm, renew our strength, and guide our steps with Your everlasting light."
        ]
    return list(variations)
