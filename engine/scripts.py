import random
from typing import Dict, List, Optional

# =============================================================================
# HYPER-SPECIFIC PAIN POINT THEMES (Meta 2026 Optimized - 26 Categorías)
# Scroll-Stoppers de 4-7 palabras + CTAs de Guardar, Comentar Nombre y Compartir
# =============================================================================

VIRAL_THEMES = {
    "zero_balance": {
        "title": "💸 Milagro Financiero (Facturas / $0 en el banco)",
        "description": "Pánico financiero inmediato y necesidad de provisión urgente.",
        "scripture": "Philippians 4:19 — And my God will supply every need of yours according to his riches in glory.",
        "hashtags": ["#DailyPrayer", "#FinancialMiracle", "#FaithInGod", "#JesusSaves", "#ChristianReels"],
        "pinned_comments": [
            "👇 God sees your exact balance today. Drop your first name below so we can agree in prayer over your bills tonight! Say 'I receive it' 🙏",
            "👇 Don't let financial anxiety steal your peace. Type 'Amen' and leave the first name of your family so we can cover you in prayer."
        ],
        "hook_texts": [
            "YOUR BILLS ARE PAID",
            "STOP SCROLLING. GOD SEES.",
            "A MIRACLE IS COMING",
            "GOD OWNS IT ALL"
        ],
        "hooks": [
            "Stop scrolling. Your bills are paid.",
            "Do not panic over that bank account.",
            "If your bank account is at zero, listen:",
            "God saw the tears over those bills today."
        ],
        "bodies_micro": [
            "Jesus says: I own the cattle on a thousand hills. I am opening doors of provision that no man can shut. Receive your financial breakthrough right now.",
            "Jesus says: Stop stressing over the math. I am moving unexpected resources in your favor before this week ends. Rest in My peace.",
            "Jesus says: Hand the heavy burden of debt to Me. Supernatural provision is rushing into your life today. Believe and walk forward in faith."
        ],
        "bodies_deep": [
            "Jesus says: I see the knot in your stomach and the fear of tomorrow. But the math of this world cannot limit My supernatural abundance. I am turning your scarcity into a testimony. People you don't even know are being positioned right now to release blessings into your hands.",
            "Jesus says: You have carried this financial panic alone for too long. Today, the spirit of lack is broken over your home. I am canceling debts, releasing unexpected checks, and opening doors of favor that no employer or banker can close. Breathe, My child.",
            "Jesus says: Do not let the enemy convince you that you are forgotten. What feels impossible for man is effortless for Me. I am releasing a fresh wave of provision over your family today that will leave you speechless. Your breakthrough is already in motion."
        ],
        "ctas": [
            "Save this prayer for tonight, and drop your first name below so we can pray over your finances.",
            "Save this promise, comment your first name for prayer, and send this to someone fighting financial stress.",
            "Drop your first name below to stand in agreement, and share this with a family believing for a financial miracle."
        ]
    },

    "lost_child": {
        "title": "🚶‍♂️ Por el hijo/hija que se alejó de Dios",
        "description": "Dolor de un padre/madre por un hijo en rebeldía, adicción o lejos de la fe.",
        "scripture": "Luke 15:20 — But while he was still a long way off, his father saw him and was filled with compassion.",
        "hashtags": ["#PrayingParents", "#ProdigalSon", "#FamilyPrayer", "#JesusHeals", "#FaithReels"],
        "pinned_comments": [
            "👇 A parent's prayer has eternal power. Leave the first name or initial of your child below. We are interceding for them tonight! 🙏",
            "👇 God loves your child even more than you do. Type their first name and claim: 'They are coming home to Jesus!' ❤️"
        ],
        "hook_texts": [
            "THEY WILL COME HOME",
            "DO NOT GIVE UP ON THEM",
            "GOD IS CHASING YOUR CHILD",
            "CHAINS ARE BREAKING"
        ],
        "hooks": [
            "Do not give up on your child.",
            "Stop crying over your wandering child.",
            "God is pursuing your son or daughter right now.",
            "Your prayers over your child were heard."
        ],
        "bodies_micro": [
            "Jesus says: I hear every whisper you cry into your pillow. My Spirit is chasing them into the deepest shadows. I am bringing them back home.",
            "Jesus says: Release the guilt. I loved them first. Every chain of rebellion and addiction is snapping. A divine turnaround is coming.",
            "Jesus says: Your child is not too far gone for My grace. I am speaking directly to their conscience today. Stand firm in your faith."
        ],
        "bodies_deep": [
            "Jesus says: I collect every single tear you have shed over their choices. You think they are slipping away, but My angels are surrounding them right now. Even when they reject your words, they cannot escape the holy conviction of My Spirit. The very thing the enemy meant to destroy them will become their greatest ministry.",
            "Jesus says: Lay down the burden of failure. You did not fail them; the spiritual battle is just fierce. But the Blood of Jesus covers your household. I am softening their hardened heart, removing toxic influences, and drawing them back to My altar with cords of unconditional love.",
            "Jesus says: Look with spiritual eyes. The prodigal season is coming to an end. Soon you will see them walk back through the door, restored, healed, and on fire for God. Your tears were seeds of a mighty harvest."
        ],
        "ctas": [
            "Save this prayer, and drop your child's first name below so we can cover them in prayer tonight.",
            "Leave the first name of the child you are praying for below, and share this with another praying parent.",
            "Save this truth, type your child's initial in the comments, and send this to a mother or father who needs hope."
        ]
    },

    "night_anxiety": {
        "title": "🌌 Ansiedad a las 3 AM (Ataques de pánico e insomnio)",
        "description": "Paz de emergencia para mentes aceleradas, ataques de pánico y miedo nocturno.",
        "scripture": "Psalm 4:8 — In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.",
        "hashtags": ["#OvercomingAnxiety", "#NightPrayer", "#PeaceOfGod", "#ChristianHealing", "#MentalPeace"],
        "pinned_comments": [
            "👇 If anxiety woke you up tonight, take a slow breath. You are safe. Drop a '🙏' and your first name so we can pray over your sleep right now.",
            "👇 The Lord gives his beloved sleep. Reply 'I receive God's peace' and let our community hold you in prayer tonight."
        ],
        "hook_texts": [
            "BREATHE RIGHT NOW",
            "ANXIETY ENDS TONIGHT",
            "YOU ARE SAFE WITH JESUS",
            "PEACE TO YOUR MIND"
        ],
        "hooks": [
            "Breathe. God is silencing your anxiety.",
            "Stop overthinking. Tomorrow is in God's hands.",
            "If your chest feels heavy tonight, listen:",
            "Anxiety has no authority over you tonight."
        ],
        "bodies_micro": [
            "Jesus says: Inhale My peace and exhale every fear. You do not have to fight tomorrow's battles in bed tonight. I am guarding your mind.",
            "Jesus says: I command the storm in your thoughts to be still. My perfect love casts out all fear. Close your eyes and rest in My arms.",
            "Jesus says: You are completely safe under the shadow of My wings. No panic attack can steal the peace I have purchased for you tonight."
        ],
        "bodies_deep": [
            "Jesus says: Take a deep breath and let your shoulders drop. The racing thoughts whispering worst-case scenarios are lies from the enemy. I have already gone before you into tomorrow and prepared every answer. Lay down your heavy mind at My feet; I never sleep nor slumber, so you can rest peacefully tonight.",
            "Jesus says: I speak divine stillness into every racing heartbeat right now. Where fear brought darkness, My light is flooding your bedroom. I am posting warrior angels at every corner of your home. You will wake up refreshed, renewed, and filled with My supernatural clarity.",
            "Jesus says: You are not weak for feeling overwhelmed; you are simply weary from carrying burdens meant for Me. Let them go right now. Sleep under the canopy of My unconditional grace. Morning joy is coming."
        ],
        "ctas": [
            "Save this prayer so you can play it whenever anxiety hits, and drop your first name below for peace.",
            "Save this Reel to your favorites for nighttime, comment 'Peace' below, and share with a loved one who struggles to sleep.",
            "Drop your first name below so we can pray over your mind tonight, and send this to someone fighting anxiety."
        ]
    },

    "medical_fear": {
        "title": "🩺 Diagnóstico Médico Aterrorizante (Sanidad y milagro)",
        "description": "Sanidad desesperada frente a enfermedades graves, dolor crónico y reportes médicos.",
        "scripture": "Jeremiah 17:14 — Heal me, Lord, and I will be healed; save me and I will be saved, for you are the one I praise.",
        "hashtags": ["#HealingPrayer", "#MiracleWorker", "#FaithOverFear", "#JesusHeals", "#DivineHealth"],
        "pinned_comments": [
            "👇 The doctor has a report, but Jesus has the final word! Drop the first name of who needs physical healing so we can stand in faith! 🙏",
            "👇 By His stripes you were healed. Type 'I claim my healing' and leave your prayer request below."
        ],
        "hook_texts": [
            "GOD HAS THE FINAL SAY",
            "HEALING IS YOURS TODAY",
            "THE DOCTOR IS NOT GOD",
            "MIRACLE IN YOUR BODY"
        ],
        "hooks": [
            "The doctor gave a report, but God has the final say.",
            "Do not accept the timeline of sickness.",
            "If pain and sickness are exhausting you, hear this:",
            "God is releasing healing into your body right now."
        ],
        "bodies_micro": [
            "Jesus says: I am the Great Physician. By My stripes, supernatural healing is flowing through your bloodstream right now. Stand firm.",
            "Jesus says: Human medicine has limits, but My resurrection power has none. I am reversing bad reports and restoring strength to your body.",
            "Jesus says: Sickness does not get the final chapter in your story. Receive divine restoration and strength from crown to sole today."
        ],
        "bodies_deep": [
            "Jesus says: I walked through that clinic with you, and I felt every tremble of fear in your heart. But medical scans do not define your destiny; My promises do. I am sending creative healing power into every damaged cell, tissue, and organ right now. What the doctors called incurable, I call an opportunity to display My glory.",
            "Jesus says: Rebuke the spirit of infirmity off your life. I carried that sickness on the cross so you wouldn't have to carry it in fear. Sickness must bow to the Name of Jesus. Receive supernatural renewal in your lungs, heart, bones, and mind today. You will live and declare the works of the Lord.",
            "Jesus says: I see the weariness of endless appointments and medications. But your testimony of deliverance is being written right now. Stand tall in unwavering faith; a supernatural breakthrough is turning the tables in your favor."
        ],
        "ctas": [
            "Save this prayer for your healing journey, and drop your first name or loved one's name below for intercession.",
            "Comment the first name of who needs healing below, save this post, and share it with someone fighting illness.",
            "Type 'I claim healing' below, save this declaration, and send it to a friend in need of strength today."
        ]
    },

    "betrayal": {
        "title": "💔 Traición y Corazón Roto (Deslealtad y restauración)",
        "description": "Corazón roto, perdón difícil y justicia divina ante la deslealtad humana.",
        "scripture": "Psalm 147:3 — He heals the brokenhearted and binds up their wounds.",
        "hashtags": ["#BrokenHeartHealed", "#GodIsMyDefender", "#HealingWounds", "#FaithInGod", "#ChristianPeace"],
        "pinned_comments": [
            "👇 People may walk away, but God never abandons you. Drop a '❤️' and your first name so we can pray over your healing today.",
            "👇 God is restoring double for what was taken from you. Type 'I release it to Jesus' in the comments."
        ],
        "hook_texts": [
            "GOD SAW THE BETRAYAL",
            "HE WILL VINDICATE YOU",
            "YOUR HEART WILL HEAL",
            "BETTER DAYS AHEAD"
        ],
        "hooks": [
            "God saw who broke your heart.",
            "Do not chase who walked away from you.",
            "If someone you trusted betrayed you, hear this:",
            "Your broken heart will beat with joy again."
        ],
        "bodies_micro": [
            "Jesus says: I know the sting of betrayal intimately. I removed them because their season in your life was over. Better blessings are coming.",
            "Jesus says: Hand Me your shattered pieces. I will not just mend your heart; I will make it stronger and protect it with My love.",
            "Jesus says: Do not poison your soul with bitterness. Let Me be your defender. I will restore double for every tear you shed."
        ],
        "bodies_deep": [
            "Jesus says: I stood beside you in the room when your heart was shattered. I saw the promises they broke and the coldness of their exit. But remember: their departure does not change your divine worth. I removed them to protect where I am taking you next. What felt like rejection was My divine redirection.",
            "Jesus says: Release the anger and the desire to see them regret what they did. Vengeance is Mine, and healing is yours. I am binding up your silent emotional wounds with balm from heaven. I am preparing a new season surrounded by loyal, godly people who will honor your heart.",
            "Jesus says: You will not live the rest of your life guarded and numb. I am breathing tenderness and radiant joy back into your spirit. The best chapter of your life is starting today."
        ],
        "ctas": [
            "Save this prayer to heal your heart, and drop your first name below so our prayer community can stand with you.",
            "Leave a '❤️' and your first name in the comments, save this Reel, and share with a friend recovering from betrayal.",
            "Save this truth for hard days, comment below, and send it to someone who feels completely discarded today."
        ]
    },

    "morning_favor": {
        "title": "🌅 Bendición y Favor de la Mañana (Comenzar el día en victoria)",
        "description": "Ideal para empezar el día. Oración de puertas abiertas, protección y favor.",
        "scripture": "Lamentations 3:22-23 — The steadfast love of the Lord never ceases; his mercies are new every morning.",
        "hashtags": ["#MorningPrayer", "#DailyBlessing", "#FavorOfGod", "#ChristianDaily", "#JesusFirst"],
        "pinned_comments": [
            "👇 Before you start your day, seal this blessing! Drop a '🙏' and your first name so we can declare favor over your schedule today!",
            "👇 Today is a day of open doors! Type 'I step into favor today' and claim this morning promise."
        ],
        "hook_texts": [
            "TODAY IS BLESSED",
            "DOORS ARE OPENING TODAY",
            "BEFORE YOU STEP OUT",
            "FAVOR IS ON YOUR LIFE"
        ],
        "hooks": [
            "Before you start your day, hear this blessing:",
            "God woke you up today for a divine reason.",
            "Today is not an ordinary day; favor is yours.",
            "Do not walk out the door without this prayer."
        ],
        "bodies_micro": [
            "Jesus says: I go before you today to level the mountains. I am unlocking supernatural favor on your job, family, and steps today. Step out in faith.",
            "Jesus says: My mercies are brand new for you this morning. Yesterday's failures are washed clean. Expect divine appointments today.",
            "Jesus says: No weapon formed against your day shall prosper. My angels are guarding your coming and going. Walk in quiet confidence."
        ],
        "bodies_deep": [
            "Jesus says: Take a deep breath of fresh grace. You did not wake up by accident; your assignment on this earth is vital. I am making crooked paths straight before your feet today. Where people told you no, I am preparing someone to say yes. Where doors were locked, My favor is swinging them wide open.",
            "Jesus says: Cast off the heaviness of yesterday. This day is a clean canvas painted with My mercy. Walk into your workplace, your home, and your community knowing that the King of Glory walks at your right hand. Fear has no place in a day ordained by God.",
            "Jesus says: I am breathing supernatural wisdom into your decisions and peace into your conversations today. Watch Me turn ordinary moments into extraordinary breakthroughs before this evening arrives."
        ],
        "ctas": [
            "Save this morning prayer to start every day in faith, and drop your first name below for God's favor.",
            "Drop your first name below to receive today's blessing, save this Reel, and send it to someone you want to see blessed today.",
            "Save this Reel for tomorrow morning, comment 'Amen' below, and share this blessing with your family."
        ]
    },

    "job_breakthrough": {
        "title": "💼 Empleo y Puertas Laborales (Finanzas y trabajo)",
        "description": "Oración para personas desempleadas, entrevistas laborales o estancamiento profesional.",
        "scripture": "Deuteronomy 28:8 — The Lord will command the blessing on you in your barns and in all that you undertake.",
        "hashtags": ["#JobSearchPrayer", "#CareerBreakthrough", "#GodProvides", "#FaithAtWork", "#ChristianSuccess"],
        "pinned_comments": [
            "👇 Looking for a job or career breakthrough? Leave your first name and the position you're believing for below! Standing with you in faith! 🙏",
            "👇 God opens doors that no resume can guarantee. Type 'I claim my job miracle' below!"
        ],
        "hook_texts": [
            "YOUR JOB DOOR IS OPENING",
            "STOP WORRYING OVER WORK",
            "GOD HAS THE RIGHT DOOR",
            "PROMOTION IS COMING"
        ],
        "hooks": [
            "Your next job is already prepared by God.",
            "If doors keep slamming in your career, listen:",
            "Stop stressing over that job application today.",
            "God is preparing a promotion you didn't see coming."
        ],
        "bodies_micro": [
            "Jesus says: Rejection was just My protection. The right employer will see your value and offer what you deserve. Prepare your hands to work.",
            "Jesus says: Do not lose heart over silence. I am speaking your name in rooms you have never entered. Your job breakthrough is near.",
            "Jesus says: I am the God who promotes the humble. What looked like a career dead-end is turning into a highway of abundance."
        ],
        "bodies_deep": [
            "Jesus says: I know how exhausting it is to send resumes and wait in silence. But your worth does not depend on an interview panel; it is secured in Me. The closed doors were My mercy keeping you from toxic environments. I am opening a position tailored for your gifts where you will thrive, provide for your home, and be valued.",
            "Jesus says: Stand tall with confidence. You are backed by the Creator of the universe. When you walk into your next opportunity, My favor will shine upon your face. Expect unexpected calls, approved interviews, and a salary that brings relief to your home.",
            "Jesus says: Rest from the panic of unemployment. I fed millions in the desert, and I will not leave your table empty. Prepare your spirit; the season of waiting is giving way to a season of fruitful work."
        ],
        "ctas": [
            "Save this prayer for your next interview, and drop your first name below so we can agree in prayer for your job.",
            "Comment the career breakthrough you need below, save this Reel, and share with anyone currently searching for employment.",
            "Save this declaration, drop your first name in the comments, and send it to a friend needing a career miracle."
        ]
    },

    "marriage_crisis": {
        "title": "💍 Matrimonio en Crisis (Restauración y perdón)",
        "description": "Para parejas al borde del divorcio, discusiones constantes o enfriamiento del amor.",
        "scripture": "Mark 10:9 — What therefore God has joined together, let not man separate.",
        "hashtags": ["#MarriageRestoration", "#ChristianMarriage", "#SaveMyMarriage", "#FamilyFirst", "#GodHeals"],
        "pinned_comments": [
            "👇 God can resurrect any marriage that surrenders to Him. Drop both of your first names below so we can pray over your home tonight! 🙏",
            "👇 Fighting for your marriage in private? Type 'God restore our love' and claim peace in your household."
        ],
        "hook_texts": [
            "DO NOT GIVE UP ON YOUR MARRIAGE",
            "GOD IS HEALING YOUR HOME",
            "LOVE WILL RETURN",
            "PEACE IN YOUR HOUSE"
        ],
        "hooks": [
            "Do not give up on your marriage yet.",
            "God can resurrect love that feels dead.",
            "If your home feels cold and divided tonight, listen:",
            "Satan wants your marriage, but God says no."
        ],
        "bodies_micro": [
            "Jesus says: I am stepping into your living room. Every spirit of division and bitterness is breaking. Softness and true love are returning.",
            "Jesus says: Lay down your pride and weapons. I am healing the deep wounds of your spouse and giving you both a supernatural second chance.",
            "Jesus says: What I joined together cannot be destroyed when you invite Me to lead. I am rebuilding your marital covenant stronger than before."
        ],
        "bodies_deep": [
            "Jesus says: I see the silent tears shed in the other room and the walls of silence built between you. But no heart is too hard for My grace to melt. I am rebuking the spirit of divorce, infidelity, and resentment that tried to poison your sacred covenant. I am restoring communication, tenderness, and mutual respect into your marriage.",
            "Jesus says: Start fighting in prayer instead of fighting each other. The enemy wants your children to see a broken home, but I am raising a banner of victory over your marriage. Surrender your hurt to Me; I am pouring the fresh wine of romantic, sacrificial love back into your relationship.",
            "Jesus says: Where contempt ruled, honor is returning. Where anger shouted, My gentle peace will reign. Stand in the gap for your spouse today and watch Me do what human counseling could not achieve."
        ],
        "ctas": [
            "Save this prayer for your marriage, and drop your initials below so our prayer community can intercede for your home.",
            "Comment 'Restore our marriage' below, save this post, and share with a couple fighting for their family.",
            "Save this Reel to listen whenever conflict arises, leave your first name below, and send it to a spouse in need of hope."
        ]
    },

    "silent_depression": {
        "title": "🌧️ Depresión Silenciosa (Sentirse vacío o invisible)",
        "description": "Consuelo para quienes sonríen por fuera pero se están rompiendo por dentro.",
        "scripture": "Psalm 34:18 — The Lord is near to the brokenhearted and saves the crushed in spirit.",
        "hashtags": ["#SilentBattles", "#GodSeesYou", "#OvercomingDepression", "#ChristianHope", "#JesusLovesYou"],
        "pinned_comments": [
            "👇 You are not invisible to God, and you are not alone in this fight. Drop a '🕊️' and your first name so we can pray strength over you today.",
            "👇 The darkness will not win. Type 'I am choosing to live' and let this family surround you with unconditional love."
        ],
        "hook_texts": [
            "YOU ARE NOT INVISIBLE",
            "GOD SEES YOUR SILENT TEARS",
            "THE HEAVINESS IS BREAKING",
            "YOU WILL SMILE AGAIN"
        ],
        "hooks": [
            "You are not invisible to God.",
            "To the one smiling outside while crying inside:",
            "God saw the tears you wiped away in secret.",
            "The heavy cloud over your life is lifting."
        ],
        "bodies_micro": [
            "Jesus says: I see you in the quiet moments when the mask comes off. You are deeply loved, irreplaceable, and your life holds immense purpose.",
            "Jesus says: The spirit of heaviness is leaving your chest. I am giving you beauty for ashes and a garment of praise for despair. Hold on.",
            "Jesus says: Do not believe the lie that no one cares. I gave My life for you. My gentle joy is coming back to fill the empty spaces."
        ],
        "bodies_deep": [
            "Jesus says: You do not have to pretend to be strong around Me. I know how exhausted your soul is from fighting battles nobody else sees. I am sitting right beside you in the quiet corners of your room. You are not a burden, you are not damaged beyond repair, and your story is nowhere near over.",
            "Jesus says: I am breathing holy life back into your tired spirit. The darkness that feels like a suffocating blanket cannot overpower My radiant light. I am breaking the chains of depression, suicidal thoughts, and numbness. You will taste the sweetness of genuine joy and peace again.",
            "Jesus says: Rest in My unconditional embrace. I love you exactly as you are right now. Lean your weary head on My shoulder; I will carry you until you have the strength to run again."
        ],
        "ctas": [
            "Save this prayer for the heavy moments, and drop your first name below so we can pray over your mental health.",
            "Drop a '🕊️' and your first name in the comments, save this Reel, and share it with someone fighting a silent battle.",
            "Save this post to your favorites, comment below to receive prayer, and send it to someone who needs to know they are loved."
        ]
    },

    "spiritual_warfare": {
        "title": "🛡️ Guerra Espiritual y Victoria (Rompiendo cadenas de opresión)",
        "description": "Poder divino y autoridad en Cristo para quebrar ataques demoníacos y opresión.",
        "scripture": "2 Corinthians 10:4 — For the weapons of our warfare are not of the flesh but have divine power to destroy strongholds.",
        "hashtags": ["#SpiritualWarfare", "#VictoryInJesus", "#BloodOfJesus", "#ChainsAreBroken", "#PrayerWarrior"],
        "pinned_comments": [
            "👇 No weapon formed against you shall prosper! Drop your first name below and claim: 'I walk in divine victory in Jesus' Name!' ⚔️🙏",
            "👇 The enemy lost this battle! Type 'The Blood of Jesus protects my home' and leave your prayer request."
        ],
        "hook_texts": [
            "NO WEAPON WILL PROSPER",
            "THE ENEMY CANNOT WIN",
            "CHAINS ARE BREAKING NOW",
            "VICTORY IN JESUS NAME"
        ],
        "hooks": [
            "The enemy tried to break you, but he failed.",
            "No weapon formed against you will prosper.",
            "If spiritual warfare has been intense this week, listen:",
            "God is putting a shield of fire around your life."
        ],
        "bodies_micro": [
            "Jesus says: The roar of the enemy is an empty bluff. I have given you authority to trample over all power of darkness. Stand your ground.",
            "Jesus says: Every chain of witchcraft, oppression, and generational curse is snapping by the power of My Blood. You are completely free.",
            "Jesus says: My angels are drawing swords of light around your family. What the devil meant for evil, I am turning into your greatest triumph."
        ],
        "bodies_deep": [
            "Jesus says: The reason the battle has felt so fierce is because you are on the threshold of your greatest breakthrough. The enemy only attacks territory that is valuable. But remember who holds all authority in heaven and on earth: at My Name, every demon trembles and flees. I have placed a hedge of fire around you, your children, and your home.",
            "Jesus says: Put on the full armor of God and lift your head. You are not fighting for victory; you are fighting from the victory I already secured on the cross. Every spoken curse, every jealous eye, and every demonic trap set against your path is dissolved in My presence.",
            "Jesus says: Lift your praise in the face of the enemy. Your worship is a weapon that dismantles spiritual fortresses. Walk in bold confidence; the Lion of Judah is roaring ahead of you today."
        ],
        "ctas": [
            "Save this warfare prayer to declare over your home, and drop your first name below to join in prayer.",
            "Type 'Victory in Jesus' and your first name in the comments, save this Reel, and share with a prayer warrior.",
            "Save this declaration for spiritual strength, comment below, and send it to someone facing heavy spiritual opposition."
        ]
    },

    "psalm_91_shield": {
        "title": "🏰 Salmo 91: Escudo de Protección Divina (Peligro y maldad)",
        "description": "Cobertura celestial para tu vida, tus hijos y tu hogar contra todo mal.",
        "scripture": "Psalm 91:1-2 — He who dwells in the shelter of the Most High will abide in the shadow of the Almighty.",
        "hashtags": ["#Psalm91", "#DivineProtection", "#HedgeOfAngels", "#CoveredByGrace", "#ChristianReels"],
        "pinned_comments": [
            "👇 Psalm 91 covers your family tonight! Drop the first names of your loved ones below so we can cover them in the shelter of the Most High! 🛡️",
            "👇 No evil shall befall your dwelling. Type 'My family is protected by Psalm 91' in the comments!"
        ],
        "hook_texts": [
            "PSALM 91 OVER YOUR LIFE",
            "YOU ARE UNTOUCHABLE",
            "ANGELS ARE ON GUARD",
            "NO EVIL SHALL TOUCH YOU"
        ],
        "hooks": [
            "Receive the shield of Psalm 91 today.",
            "You and your family are covered by God.",
            "No evil shall touch your dwelling place.",
            "God is sending angels to guard your steps."
        ],
        "bodies_micro": [
            "Jesus says: Dwell under My shadow. A thousand may fall at your side, but danger will not come near you. My angels have you covered.",
            "Jesus says: I will deliver you from every deadly pestilence and hidden snare. My faithfulness is your impenetrable armor. Walk in safety.",
            "Jesus says: Call upon Me and I will answer. I will rescue you, honor you, and show you My supernatural salvation every single day."
        ],
        "bodies_deep": [
            "Jesus says: Under My wings you will find refuge; My truth is your shield and buckler. You do not need to fear the terror by night, nor the arrow that flies by day. I have assigned mighty angels of light with drawn swords to encamp around your house, your vehicles, and everywhere your family walks.",
            "Jesus says: Because you have made the Lord your dwelling place, no plague or destruction shall enter your door. When you walk through dangerous places, My presence will guide your steps so you do not dash your foot against a stone. You are untouchable in My hands.",
            "Jesus says: Rest your heart from anxiety about the future. I am your refuge, your fortress, and your God in whom you trust. Sleep soundly tonight knowing the Almighty Himself is your personal protector."
        ],
        "ctas": [
            "Save this Psalm 91 declaration over your home, and drop your family's first names below for protection.",
            "Leave the first names of your loved ones in the comments, save this Reel, and send it to cover someone you love today.",
            "Save this prayer to your daily routine, comment 'Protected' below, and share with a mother or father."
        ]
    },

    "psalm_23_valley": {
        "title": "🌿 Salmo 23: En el Valle de Sombra de Muerte (El Buen Pastor)",
        "description": "Para quienes atraviesan el momento más oscuro y necesitan el consuelo del Pastor.",
        "scripture": "Psalm 23:4 — Even though I walk through the valley of the shadow of death, I will fear no evil, for you are with me.",
        "hashtags": ["#Psalm23", "#TheGoodShepherd", "#FearNoEvil", "#ValleyOfShadows", "#PeaceInGod"],
        "pinned_comments": [
            "👇 The Good Shepherd is walking through the valley right next to you. Drop your first name below so we can pray over your peace! 🌿",
            "👇 Surely goodness and mercy will follow you all the days of your life. Type 'The Lord is my Shepherd' below."
        ],
        "hook_texts": [
            "THE VALLEY WILL NOT END YOU",
            "THE GOOD SHEPHERD IS HERE",
            "FEAR NO EVIL TODAY",
            "GREEN PASTURES AHEAD"
        ],
        "hooks": [
            "You will not die in this valley.",
            "The Lord is your Shepherd; you lack nothing.",
            "Even in the darkest valley, God is with you.",
            "Look up; green pastures are right ahead."
        ],
        "bodies_micro": [
            "Jesus says: I am your Good Shepherd. I lead you beside quiet waters and restore your soul. You are passing through this valley, not staying.",
            "Jesus says: My rod and My staff comfort you. Even in front of your enemies, I am preparing a lavish table of blessing and joy for you.",
            "Jesus says: Do not fear the shadows; a shadow has no power to harm you. My goodness and unfailing mercy are following every step you take."
        ],
        "bodies_deep": [
            "Jesus says: The valley feels terrifying and long, but remember: you are walking through it, not setting up camp in it. A shadow of death is only a shadow; it has no substance and no authority to stop My plan for your life. I am walking right beside you, matching your pace, holding your trembling hand.",
            "Jesus says: I am preparing a feast of honor, restoration, and abundance for you in the presence of those who mocked or doubted you. I am anointing your head with fresh oil until your cup of joy overflows. Goodness and mercy are pursuing you as your personal bodyguards.",
            "Jesus says: Rest your tired spirit. You do not need to fight for water or bread in this spiritual desert; I am your supernatural provider. Look ahead; the green pastures and peaceful streams are appearing on the horizon."
        ],
        "ctas": [
            "Save this Psalm 23 prayer for when the valley feels dark, and drop your first name below for pastoral prayer.",
            "Comment 'The Lord is my Shepherd' and your first name below, save this Reel, and share with a hurting friend.",
            "Save this comforting truth, leave your first name in the comments, and send it to someone facing grief or loss."
        ]
    },

    "lion_of_judah": {
        "title": "🦁 El León de Judá Ruge por Ti (Dios peleando tus batallas)",
        "description": "Fuerza, coraje y reivindicación divina cuando te sientes acorralado e indefenso.",
        "scripture": "Revelation 5:5 — Behold, the Lion of the tribe of Judah, the Root of David, has conquered.",
        "hashtags": ["#LionOfJudah", "#BattleBelongsToGod", "#CourageInChrist", "#JesusFightsForYou", "#ChristianPower"],
        "pinned_comments": [
            "👇 The Lion of Judah is roaring over your enemies and circumstances today! Drop your first name below to receive bold faith! 🦁🙏",
            "👇 The battle belongs to the Lord! Type 'The Lion of Judah fights for me' in the comments."
        ],
        "hook_texts": [
            "THE LION OF JUDAH ROARS",
            "THE BATTLE IS NOT YOURS",
            "BE STILL AND WATCH GOD WIN",
            "VICTORY IS ALREADY YOURS"
        ],
        "hooks": [
            "The Lion of Judah is roaring for you.",
            "Stop fighting battles meant for God.",
            "When you cannot fight anymore, the Lion steps in.",
            "Your enemies did not see the Lion standing behind you."
        ],
        "bodies_micro": [
            "Jesus says: Be still and know that I am God. The Lion of Judah has conquered. Every giant standing before your family must fall.",
            "Jesus says: You do not need to swing a sword. Hold your peace while I fight for you. The victory is already sealed in My Name.",
            "Jesus says: Rise up in boldness. The same Spirit that raised Me from the dead lives inside your chest. Fear has no place here."
        ],
        "bodies_deep": [
            "Jesus says: You have felt outnumbered, tired, and cornered by circumstances. But you forgot Who stands behind you. I am the Lion of the tribe of Judah. When I roar, the foundations of darkness shake and every enemy scheme is scattered into confusion. The battle belongs to Me; your job is simply to praise Me in the storm.",
            "Jesus says: Stop agonizing over what people are saying or doing against you. They are contending with dust, but they have to answer to the Creator. I am rising to defend your name, your family, and your calling. Watch how swiftly I silence the roar of your accusers.",
            "Jesus says: Put your shoulders back and lift your chin. You are a son or daughter of the King of Kings. Walk with divine authority today; the Lion has conquered, and triumph is your birthright."
        ],
        "ctas": [
            "Save this declaration of victory, and drop your first name below so we can agree in faith for your battle.",
            "Comment 'The Lion fights for me' and your first name below, save this post, and share with someone facing a giant.",
            "Save this Reel to listen before tough challenges, leave a '🦁' below, and send it to a loved one who needs courage."
        ]
    },

    "exhausted_parent": {
        "title": "🤱 Agotamiento Extremo de Mamá o Papá (Fuerzas sobrenaturales)",
        "description": "Para padres desbordados por el cansancio, la crianza y la falta de fuerzas.",
        "scripture": "Isaiah 40:29 — He gives power to the faint, and to him who has no might he increases strength.",
        "hashtags": ["#TiredMomPrayer", "#ChristianParenting", "#StrengthForMoms", "#FaithfulFather", "#FamilyBlessing"],
        "pinned_comments": [
            "👇 To every tired mom and dad reading this: God honors your quiet sacrifices. Drop your first name below for a touch of supernatural strength! ❤️🙏",
            "👇 God will give you strength when yours runs out. Type 'Lord renew my strength' and leave the names of your children below."
        ],
        "hook_texts": [
            "TO THE TIRED MOTHER",
            "STRENGTH IS COMING TO YOU",
            "YOU ARE A WONDERFUL PARENT",
            "GOD SEES YOUR SACRIFICE"
        ],
        "hooks": [
            "To the exhausted mother or father watching this:",
            "God sees how hard you are trying for your kids.",
            "If parenting feels overwhelming today, take a breath:",
            "You are not failing as a parent."
        ],
        "bodies_micro": [
            "Jesus says: I see the countless unseen sacrifices you make every single day. I am pouring fresh supernatural energy into your tired bones right now.",
            "Jesus says: You don't have to be a perfect parent; just lean on My perfect love. My grace is sufficient for you and your household.",
            "Jesus says: Your children are a heritage from Me. I will protect them, guide them, and give you heavenly wisdom for every single day."
        ],
        "bodies_deep": [
            "Jesus says: Take a breath and let the pressure drop. I see how deeply you care, and I know how physically and emotionally drained you feel at the end of the day. But remember: your children do not need a flawless parent; they need a praying parent who rests in My grace. What you lack in energy, I will multiply in love.",
            "Jesus says: When you feel like you are failing, My Spirit is doing the deepest work. The seeds of faith and affection you plant in their little hearts will blossom into a mighty harvest. I am wrapping My peace around your home and lifting the cloud of exhaustion right now.",
            "Jesus says: Rest in My presence tonight. I will watch over your children while you sleep. Tomorrow morning, you will rise with renewed patience, joy, and divine strength."
        ],
        "ctas": [
            "Save this prayer for tough parenting days, and drop your first name below so our community can pray over your family.",
            "Leave the first names of your children in the comments, save this Reel, and share with a tired mom or dad today.",
            "Save this to your favorites, comment below for encouragement, and send it to a parent who needs a reminder of their worth."
        ]
    },

    "break_chains": {
        "title": "⛓️ Rompiendo Cadenas Generacionales (Libertad familiar)",
        "description": "Ruptura de patrones de pobreza, vicios, divorcio o maldiciones familiares.",
        "scripture": "Galatians 5:1 — For freedom Christ has set us free; stand firm therefore, and do not submit again to a yoke of slavery.",
        "hashtags": ["#ChainsAreBroken", "#GenerationalHealing", "#FreedomInChrist", "#NewBeginning", "#ChristianVictory"],
        "pinned_comments": [
            "👇 Generational chains of poverty, addiction, and pain stop with YOU! Drop your family name below to claim total freedom! ⛓️❌🙏",
            "👇 In Jesus' Name, the cycle is broken! Type 'My family is free' and leave your first name below."
        ],
        "hook_texts": [
            "THE CYCLE STOPS WITH YOU",
            "GENERATIONAL CHAINS ARE BROKEN",
            "YOUR FAMILY IS FREE TODAY",
            "A NEW LEGACY BEGINS"
        ],
        "hooks": [
            "The generational curse stops with you.",
            "Your children will not inherit your family's pain.",
            "The chain of addiction and poverty is broken today.",
            "You were chosen to start a new godly lineage."
        ],
        "bodies_micro": [
            "Jesus says: What held your parents or grandparents will not hold your future. By the Blood of Jesus, you are an anointed cycle breaker.",
            "Jesus says: The patterns of divorce, lack, and addiction stop right here. I am writing a brand new story of blessings for your children.",
            "Jesus says: Walk into holy freedom. Whom the Son sets free is free indeed. Rejoice in the liberty purchased for you on the cross."
        ],
        "bodies_deep": [
            "Jesus says: Look back one last time at the cycles of pain, addiction, broken homes, and poverty that haunted your ancestors. Today, the divine line is drawn in the sand by My cross. You were anointed to be the one who turns the tide. The generational curse has no legal right to touch your life or the destiny of your children.",
            "Jesus says: I am healing the deep generational wounds and replacing them with a legacy of spiritual abundance, emotional health, and unwavering faith. Your lineage will be known as blessed, honorable, and devoted to the Lord. The enemy's grip on your last name is completely shattered.",
            "Jesus says: Stand tall in your freedom. Every voice of shame telling you that you are doomed to repeat the past is a lie. Walk forward into the promised land I have prepared for your family."
        ],
        "ctas": [
            "Save this declaration of generational freedom, and drop your family name below so we can seal it in prayer.",
            "Comment 'The cycle is broken' and your first name below, save this post, and share with a family member.",
            "Save this Reel to claim freedom over your children, leave your first name in the comments, and send it to a loved one."
        ]
    },

    "lonely_season": {
        "title": "🕯️ Temporada de Soledad (Dios cerca del corazón quebrantado)",
        "description": "Para quienes sienten que nadie los comprende o que caminan solos por la vida.",
        "scripture": "Hebrews 13:5 — I will never leave you nor forsake you.",
        "hashtags": ["#NeverAlone", "#GodIsNear", "#LonelyHeart", "#ComfortInChrist", "#JesusIsWithYou"],
        "pinned_comments": [
            "👇 You might feel lonely in your room, but you are never alone with Jesus. Drop a '🕯️' and your first name so we can pray with you today! 🙏",
            "👇 The Lord is walking with you step by step. Type 'Jesus is with me' and leave your prayer request."
        ],
        "hook_texts": [
            "YOU ARE NEVER ALONE",
            "JESUS IS IN THE ROOM",
            "GOD WILL NOT FORSAKE YOU",
            "LOVE IS HOLDING YOU"
        ],
        "hooks": [
            "You are not as alone as you feel right now.",
            "When everyone else walked away, Jesus stayed.",
            "If loneliness is aching in your chest tonight, listen:",
            "God is turning your isolation into intimacy with Him."
        ],
        "bodies_micro": [
            "Jesus says: I will never leave you nor forsake you. Even when the world feels empty, My presence is wrapping around you like a warm embrace.",
            "Jesus says: You are seen, heard, and cherished. I know every secret thought of your heart. You are My precious child; rest in My love.",
            "Jesus says: This lonely season is where I am building your strength. Soon I will surround you with godly companions who truly value your heart."
        ],
        "bodies_deep": [
            "Jesus says: I see you eating alone, driving alone, and going to bed with the quiet heaviness of loneliness. But physical solitude does not mean spiritual abandonment. I am closer to you than the air you breathe. In this quiet season, I am clearing out the noise so you can hear the heartbeat of your Creator.",
            "Jesus says: I know what it feels like when all your friends desert you in your hour of need. That is why I promised never to leave you or forsake you. Let My unconditional love fill every empty space in your soul. You are deeply wanted, deeply loved, and deeply protected.",
            "Jesus says: This wilderness of isolation will not last forever. I am preparing your heart for deep, meaningful connections. Trust My timing; you are stepping out of loneliness into divine belonging."
        ],
        "ctas": [
            "Save this prayer for lonely evenings, and drop your first name below so our prayer family can stand with you.",
            "Comment 'Jesus is with me' and your first name below, save this Reel, and share with someone who lives alone.",
            "Save this comforting truth, leave a '❤️' below, and send it to a friend who might be feeling isolated today."
        ]
    },

    "unexpected_doors": {
        "title": "🚪 Puertas Sobrenaturales (Lo que Dios abre nadie lo cierra)",
        "description": "Para quienes han sido rechazados y necesitan un milagro de favor y oportunidad.",
        "scripture": "Revelation 3:8 — Behold, I have set before you an open door, which no one is able to shut.",
        "hashtags": ["#OpenDoors", "#FavorOfGod", "#DivineMiracle", "#BreakthroughSeason", "#FaithUnlocks"],
        "pinned_comments": [
            "👇 What God opens, no human, employer, or enemy can shut! Drop your first name below to claim your open door of favor! 🚪✨🙏",
            "👇 Ready for an unexpected breakthrough? Type 'I receive my open door' in the comments!"
        ],
        "hook_texts": [
            "THE DOOR IS OPENING",
            "NO MAN CAN SHUT IT",
            "UNEXPECTED FAVOR TODAY",
            "YOUR SEASON HAS CHANGED"
        ],
        "hooks": [
            "What God opens, no human can shut.",
            "You are one prayer away from an open door.",
            "Stop crying over closed doors; a bigger one is opening.",
            "God is about to do something unexpected for you."
        ],
        "bodies_micro": [
            "Jesus says: The closed doors were My mercy keeping you from small things. I am opening colossal doors of favor, influence, and blessing right now.",
            "Jesus says: Do not fear the opinions of men. When I release favor on your life, even your critics will have to witness your breakthrough.",
            "Jesus says: Step forward in bold expectation. The season of delay is over. What was held back is being released with double honor."
        ],
        "bodies_deep": [
            "Jesus says: You spent too much time knocking on doors that were meant to remain closed. Wipe your tears; those rejections were My divine redirection. I have set before you an open door that no boss, no banker, and no jealous critic can shut. It is a door of abundance, peace, and spiritual purpose.",
            "Jesus says: When I move in your life, promotions come without manipulation and blessings arrive without toil. I am orchestrating meetings with people in key positions who will favor your cause simply because My hand rests upon you. Keep your character pure and watch My glory manifest.",
            "Jesus says: Your season has shifted. Prepare your mind and expand your vision; what I am about to do in your household will exceed everything you have prayed for. Walk through the open door with bold faith."
        ],
        "ctas": [
            "Save this declaration of open doors, and drop your first name below to seal your breakthrough in prayer.",
            "Comment 'I claim my open door' and your first name below, save this Reel, and share with someone waiting on a miracle.",
            "Save this Reel to your favorites, leave your first name in the comments, and send it to a friend stepping into a new season."
        ]
    },

    "forgive_yourself": {
        "title": "🕊️ Libertad de la Culpa del Pasado (Misericordia y gracia)",
        "description": "Para quienes no logran perdonarse a sí mismos por errores o pecados pasados.",
        "scripture": "Romans 8:1 — There is therefore now no condemnation for those who are in Christ Jesus.",
        "hashtags": ["#NoCondemnation", "#ForgiveYourself", "#GraceOfGod", "#CleanSlate", "#JesusForgives"],
        "pinned_comments": [
            "👇 If God threw your past into the sea of forgetfulness, stop fishing it back out! Drop a '🕊️' and your first name to receive grace! 🙏",
            "👇 There is no condemnation in Christ Jesus! Type 'I am forgiven and free' in the comments."
        ],
        "hook_texts": [
            "FORGIVE YOURSELF TODAY",
            "YOUR PAST IS UNDER THE BLOOD",
            "NO CONDEMNATION IN JESUS",
            "YOU ARE A NEW CREATION"
        ],
        "hooks": [
            "Stop punishing yourself for what God already forgave.",
            "Your past mistake does not define your future.",
            "If guilt is eating you alive today, listen to Jesus:",
            "The enemy remembers your past; God sees your future."
        ],
        "bodies_micro": [
            "Jesus says: My Blood washed away every sin. I threw your past into the sea of forgetfulness. Stop fishing it back out. You are clean.",
            "Jesus says: There is no condemnation for you in My arms. Let go of the shame and accept My boundless grace. Walk with your head high.",
            "Jesus says: You are a new creation; the old has passed away. I am using what broke you to build a powerful testimony of redemption."
        ],
        "bodies_deep": [
            "Jesus says: I hear the whispers of shame replaying your worst moments late at night. But who is the accuser? It is not Me. When you repented, I erased the record of your past completely. If I have justified you, who can condemn you? Stop letting guilt hold you hostage in a prison I already unlocked with My blood.",
            "Jesus says: Look into My eyes and see unconditional love, not disappointment. The mistakes you made did not catch Me by surprise; My mercy was already waiting at the cross. I am taking the shattered fragments of your past and crafting a message of hope that will set others free.",
            "Jesus says: Forgive yourself today. Breathe in My forgiveness and let the heavy stone of regret roll away. Step out of the shadows of yesterday into the radiant sunshine of My calling for your life."
        ],
        "ctas": [
            "Save this prayer to silence shame whenever it attacks, and drop your first name below for grace.",
            "Comment 'I am free' and your first name below, save this Reel, and share with someone struggling with regret.",
            "Save this reminder to your favorites, leave a '🕊️' below, and send it to a friend who needs to know God's grace."
        ]
    },

    "school_children": {
        "title": "🎒 Cobertura para tus Hijos (Protección en la escuela y la calle)",
        "description": "Protección contra violencia, acoso, malas influencias y accidentes para niños y jóvenes.",
        "scripture": "Isaiah 54:13 — All your children shall be taught by the Lord, and great shall be the peace of your children.",
        "hashtags": ["#ProtectOurKids", "#SchoolPrayer", "#CoverTheChildren", "#ChristianMoms", "#AngelicProtection"],
        "pinned_comments": [
            "👇 The Blood of Jesus covers our children everywhere they step! Drop the first names of your kids and grandkids below for divine protection! 🎒🛡️",
            "👇 No weapon formed against our children shall prosper! Type 'My kids are protected by Jesus' in the comments."
        ],
        "hook_texts": [
            "YOUR CHILDREN ARE COVERED",
            "ANGELS PROTECT YOUR KIDS",
            "SAFETY OVER YOUR FAMILY",
            "PEACE OVER THEIR MINDS"
        ],
        "hooks": [
            "Cover your children with this prayer today.",
            "Before your kids walk out that door, hear this:",
            "God is sending angels to guard your children.",
            "Your children are untouchable by the enemy."
        ],
        "bodies_micro": [
            "Jesus says: I am placing an impenetrable hedge of protection around your children at school, on the bus, and on the street. They are safe.",
            "Jesus says: No evil influence or bully can steal their destiny. I am giving them wisdom, moral courage, and favor with teachers and peers.",
            "Jesus says: Rest your motherly or fatherly heart. My angels walk beside them into every classroom. I love them with an everlasting love."
        ],
        "bodies_deep": [
            "Jesus says: As you send your precious children out into the world today, release the grip of anxiety. I am wrapping them in My armor of light. No weapon of violence, no toxic peer pressure, and no hidden danger will prosper against them. I am placing warrior angels at their right hand and their left hand wherever they go.",
            "Jesus says: I am guarding their minds from deception and anxiety. They will shine as bright lights of integrity and kindness among their peers. When they sit in the classroom, divine wisdom and understanding will rest upon them. They are marked with the favor of God.",
            "Jesus says: You can lay your head down in peace tonight knowing your prayers have built an eternal wall of fire around their lives. They will return home safe, sound, and blessed under My care."
        ],
        "ctas": [
            "Save this daily prayer for your kids, and drop their first names below so we can intercede for them tonight.",
            "Leave the first names of your children or grandchildren below, save this Reel, and share with other praying parents.",
            "Save this to your daily routine, comment 'Protected' below, and send it to a mom or dad who loves their children."
        ]
    },

    "restoration_double": {
        "title": "⚖️ El Doble por tu Vergüenza (Restitución divina de lo perdido)",
        "description": "Restauración de años perdidos, bienes robados, oportunidades y dignidad.",
        "scripture": "Isaiah 61:7 — Instead of your shame you shall have a double portion; instead of dishonor they shall rejoice in their lot.",
        "hashtags": ["#DoubleForYourTrouble", "#DivineRestoration", "#GodRestores", "#FaithReels", "#SeasonOfJoy"],
        "pinned_comments": [
            "👇 God is giving you double for every ounce of shame and loss you endured! Drop your first name below to claim your restoration! ⚖️✨🙏",
            "👇 The years the locust ate are being restored! Type 'I receive double for my trouble' in the comments!"
        ],
        "hook_texts": [
            "DOUBLE FOR YOUR TROUBLE",
            "GOD WILL RESTORE IT ALL",
            "YOUR SHAME IS GONE",
            "RESTITUTION IS COMING"
        ],
        "hooks": [
            "God is giving you double for your trouble.",
            "What the enemy stole from you must be returned.",
            "Your season of humiliation is officially over.",
            "God will restore the years the locusts ate."
        ],
        "bodies_micro": [
            "Jesus says: Instead of shame, you will receive a double portion. Instead of humiliation, everlasting joy will be your inheritance. Rejoice.",
            "Jesus says: The thief has been caught. Everything the enemy tried to strip from your family is being returned with divine interest.",
            "Jesus says: Wipe the memories of embarrassment away. I am crowning you with honor and elevating your life in the sight of all."
        ],
        "bodies_deep": [
            "Jesus says: You have walked through seasons where people mocked you, overlooked you, or watched you suffer in silence. But I keep perfect accounting in heaven. Every tear shed in secret is about to be repaid with public favor. I am turning the very place of your shame into the platform of your greatest testimony.",
            "Jesus says: I will restore the years of wasted time, stolen finances, broken relationships, and shattered peace. What was lost is being resurrected in greater glory and abundance. The days of hanging your head low are finished; lift your eyes and prepare to receive your inheritance.",
            "Jesus says: Those who rejoiced at your downfall will soon marvel at My goodness upon your household. Stand firm in praise; the season of double restoration has arrived."
        ],
        "ctas": [
            "Save this restoration declaration, and drop your first name below to claim your double portion in prayer.",
            "Comment 'I receive double' and your first name below, save this post, and share with someone who lost something dear.",
            "Save this Reel to your favorites, leave a '🙌' in the comments, and send it to a friend stepping into restoration."
        ]
    },

    "hard_decisions": {
        "title": "🧭 Sabiduría para Decisiones Difíciles (Confusión y dirección)",
        "description": "Para momentos de encrucijada, elecciones críticas y búsqueda de dirección divina.",
        "scripture": "Proverbs 3:5-6 — Trust in the Lord with all your heart, and do not lean on your own understanding; in all your ways acknowledge him, and he will make straight your paths.",
        "hashtags": ["#DivineGuidance", "#GodsWill", "#WisdomFromAbove", "#TrustGod", "#DirectionInChrist"],
        "pinned_comments": [
            "👇 Facing a heavy choice or crossroads today? Drop your first name below so we can pray for divine clarity and peace over your mind! 🧭🙏",
            "👇 God will direct your steps! Type 'Lord lead my way' and leave your prayer request."
        ],
        "hook_texts": [
            "GOD WILL DIRECT YOUR PATH",
            "STOP CONFUSION TODAY",
            "DIVINE CLARITY IS COMING",
            "TRUST THE PROCESS"
        ],
        "hooks": [
            "God will direct your steps today.",
            "If you are confused about what decision to make, listen:",
            "Stop stressing over the crossroads before you.",
            "God is giving you supernatural clarity right now."
        ],
        "bodies_micro": [
            "Jesus says: Lean not on your own understanding. Acknowledge Me in all your ways, and I will make your crooked paths straight and clear.",
            "Jesus says: I am not the author of confusion, but of peace. The right choice will bring quiet calm to your soul. Follow My peace.",
            "Jesus says: Do not fear making a mistake when your heart seeks Me. I will steer your wheel and keep you on the road of My purpose."
        ],
        "bodies_deep": [
            "Jesus says: Silence the competing voices of fear, pressure, and human opinions. Take a deep breath and listen to the still, small voice of My Spirit within you. When you must make a critical decision, look for My supernatural peace—it is the compass that guides your soul. Confusion is not from Me; clarity is your heritage.",
            "Jesus says: Do not be terrified of stepping into the unknown. Even if you cannot see the full staircase, I ask you to take the first step of faith. I have already mapped out your path, and I will place the right open doors and clear red lights before you at the exact right moment.",
            "Jesus says: Hand the reins of your future over to Me. You will look back on this season and marvel at how every intricate detail worked together for your good and My glory. Walk forward with peaceful certainty."
        ],
        "ctas": [
            "Save this prayer for when you need wisdom, and drop your first name below for divine guidance.",
            "Comment 'Lord lead me' and your first name below, save this Reel, and share with someone making a big life choice.",
            "Save this to your favorites, leave your first name in the comments, and send it to a family member seeking direction."
        ]
    },

    "peace_in_storm": {
        "title": "🌊 Calma en Medio de la Tempestad (No te vas a hundir)",
        "description": "Cuando los problemas se acumulan y parece que la barca se va a hundir.",
        "scripture": "Mark 4:39 — And he awoke and rebuked the wind and said to the sea, 'Peace! Be still!' And the wind ceased, and there was a great calm.",
        "hashtags": ["#PeaceBeStill", "#CalmInTheStorm", "#JesusInTheBoat", "#FaithOverFear", "#ChristianPeace"],
        "pinned_comments": [
            "👇 The storm may be raging, but Jesus is in your boat! You will not sink! Drop your first name below for supernatural peace! 🌊⛵🙏",
            "👇 Jesus commands your storm to be still! Type 'Peace, be still' in the comments to receive calm."
        ],
        "hook_texts": [
            "YOU WILL NOT SINK",
            "PEACE BE STILL TODAY",
            "JESUS IS IN YOUR BOAT",
            "THE STORM IS CALMING"
        ],
        "hooks": [
            "You will not sink in this storm.",
            "The waves look high, but Jesus is in your boat.",
            "If life feels like a hurricane right now, hear this:",
            "God is commanding the winds in your life to be still."
        ],
        "bodies_micro": [
            "Jesus says: Peace, be still. The waves obey My voice, and your life will not capsize. Fix your eyes on Me, not the storm.",
            "Jesus says: I may seem silent, but I am in the boat with you. No wind can overturn a vessel carrying the Lord of Glory. Rest.",
            "Jesus says: The hurricane in your circumstances is bowing to My command right now. A great and supernatural calm is taking over."
        ],
        "bodies_deep": [
            "Jesus says: The water is splashing over the edges of your boat and the wind is howling loud threats into your ears. But why are you so afraid? Do you still not have faith that the Creator of the seas sits right beside you? What cannot sink Me cannot sink you. You are getting to the other side.",
            "Jesus says: I stand at the bow of your life and declare: Peace, be still! To the financial storm, to the family turbulence, to the emotional hurricane—cease your roaring right now! Watch how the churning waves flatten into a mirror of glassy peace under My sovereign authority.",
            "Jesus says: Take a deep breath of tranquility. You will not drown; you will walk on the very waters that threatened to swallow you. Praise Me before the winds die down and watch your miracle unfold."
        ],
        "ctas": [
            "Save this prayer to play whenever life gets stormy, and drop your first name below for peace.",
            "Comment 'Peace be still' and your first name below, save this post, and share with a loved one facing turbulence.",
            "Save this Reel to your favorites, leave a '🌊' below, and send it to someone holding on by a thread today."
        ]
    },

    "hidden_enemies": {
        "title": "🗡️ Defensa contra Enemigos Ocultos y Chismes (Dios es tu juez)",
        "description": "Para quienes sufren ataques a sus espaldas, mentiras, calumnias o envidia.",
        "scripture": "Psalm 35:1 — Contend, Lord, with those who contend with me; fight against those who fight against me.",
        "hashtags": ["#GodIsMyDefender", "#SilencingGossip", "#ProtectedByGod", "#FaithInAction", "#ChristianJustice"],
        "pinned_comments": [
            "👇 God sees the whispering and the traps set in secret. He will vindicate you! Drop your first name below so we can pray over your defense! 🛡️🙏",
            "👇 The Lord will fight for you, and you will hold your peace! Type 'God is my shield' in the comments."
        ],
        "hook_texts": [
            "GOD HEARD THE WHISPERS",
            "HE WILL VINDICATE YOU",
            "THE TRAP WILL CATCH THEM",
            "NO WEAPON WILL STAND"
        ],
        "hooks": [
            "God heard what they whispered behind your back.",
            "Do not defend yourself against their lies.",
            "When people plot against you, God acts as your judge.",
            "The pit they dug for you will become their downfall."
        ],
        "bodies_micro": [
            "Jesus says: Hold your peace. I heard every lie, every slander, and every betrayal. I will vindicate your integrity before everyone.",
            "Jesus says: Do not waste your energy fighting back with human words. Let Me be your lawyer. I will bring your righteousness to light like the noonday sun.",
            "Jesus says: The traps they set in secret will not catch your feet. I am uncovering deception and shielding your reputation with My favor."
        ],
        "bodies_deep": [
            "Jesus says: I saw the smirks, the secret meetings, and the gossip spoken in the dark to undermine your character. But do not lose a wink of sleep trying to clear your name. Vengeance and justice belong to Me. When people throw stones at you, I use those stones to build the foundation of your next promotion.",
            "Jesus says: Bless those who curse you and pray for those who spitefully use you. That is how you disarm the enemy and leave the room for My vengeance. The very pit they dug hoping to see you stumble will become their own undoing, while you will walk forward untarnished and honored.",
            "Jesus says: Rest in My defense. My favor will speak for you in boardrooms, classrooms, and family gatherings where you are not even present. Keep your hands clean and your heart pure; your vindication is already prepared."
        ],
        "ctas": [
            "Save this prayer of vindication, and drop your first name below so our prayer community can stand with you.",
            "Comment 'God defends me' and your first name below, save this post, and share with a friend under attack.",
            "Save this Reel to your favorites, leave your first name in the comments, and send it to someone facing workplace hostility."
        ]
    },

    "business_blessing": {
        "title": "📈 Multiplicación para tu Negocio o Proyecto (Sabiduría y clientes)",
        "description": "Para emprendedores, comerciantes y soñadores que buscan la bendición de Dios en sus finanzas.",
        "scripture": "Proverbs 16:3 — Commit your work to the Lord, and your plans will be established.",
        "hashtags": ["#ChristianEntrepreneur", "#KingdomBusiness", "#BusinessBlessing", "#ProsperInGod", "#FaithAtWork"],
        "pinned_comments": [
            "👇 Believing God for new clients, sales, and breakthrough in your business or dream? Drop the name of your business/project below! Standing in faith with you! 📈🙏",
            "👇 God gives power to create wealth! Type 'Bless the work of my hands' in the comments!"
        ],
        "hook_texts": [
            "BLESSING ON YOUR BUSINESS",
            "NEW CLIENTS ARE COMING",
            "DIVINE MULTIPLICATION TODAY",
            "YOUR PLANS WILL PROSPER"
        ],
        "hooks": [
            "God is about to bless the work of your hands.",
            "If your business or project feels slow, hear this:",
            "Commit your business to God, and watch it thrive.",
            "Divine ideas and right clients are coming to you."
        ],
        "bodies_micro": [
            "Jesus says: I am breathing life into your business. I will draw the right clients, give you creative ideas, and multiply your honest labor.",
            "Jesus says: Do not despise small beginnings. Commit your work to Me, and your plans will be established with supernatural success.",
            "Jesus says: Where you saw stagnation, prepare for overflow. I am releasing wisdom that will outsmart every economic challenge."
        ],
        "bodies_deep": [
            "Jesus says: I gave you the dream, the passion, and the gifts for this enterprise. Do not let economic headlines or slow weeks shake your confidence. When you honor Me in your marketplace, My blessing turns ordinary efforts into extraordinary multiplication. I am sending loyal clients, favorable contracts, and divine connections directly to your door.",
            "Jesus says: Seek My kingdom first and conduct your business with uncompromised integrity. I will give you strategies and creative solutions that human analysts cannot explain. Where others see lack, you will find fertile ground for harvest and kingdom impact.",
            "Jesus says: Expand your tent and prepare your inventory. The season of dry spells is ending. Step out in bold faith and watch Me establish the work of your hands in ways that honor My holy Name."
        ],
        "ctas": [
            "Save this prayer for your business, and drop the name of your company or project below for blessings.",
            "Comment 'Bless my work' and your first name below, save this Reel, and share with a hardworking entrepreneur.",
            "Save this to your favorites, leave your first name in the comments, and send it to a friend chasing their dream."
        ]
    },

    "grief_loss": {
        "title": "🖤 Consuelo en el Duelo y Pérdida (Paz sobrehumana)",
        "description": "Paz y consuelo divino para quienes sufren la dolorosa partida de un ser querido.",
        "scripture": "Matthew 5:4 — Blessed are those who mourn, for they shall be comforted.",
        "hashtags": ["#ComfortInGrief", "#LossOfALovedOne", "#GodHealsGrief", "#EternalHope", "#ChristianComfort"],
        "pinned_comments": [
            "👇 Missing a loved one who went home to be with Jesus? Drop their first name below. We are praying gentle comfort over your heart tonight. 🖤🕊️",
            "👇 Blessed are those who mourn, for they shall be comforted. Type 'Lord wrap me in your peace' below."
        ],
        "hook_texts": [
            "BLESSED ARE THOSE WHO MOURN",
            "GOD IS CLOSE TO YOUR PAIN",
            "YOU WILL SMILE AGAIN",
            "HEAVEN IS NOT FAR"
        ],
        "hooks": [
            "To the heart aching with grief tonight:",
            "God is holding every tear you cry for them.",
            "You will make it through this season of loss.",
            "Heaven feels close when someone you love is there."
        ],
        "bodies_micro": [
            "Jesus says: I am close to your broken heart. Your tears are holy to Me. I am wrapping you in comfort that passes all human understanding.",
            "Jesus says: It is okay to weep. Even in the deepest sorrow, My love will never leave you. Their memory will become a sweet fragrance of peace.",
            "Jesus says: The pain will not destroy you. Lean your heavy chest on Me; I will carry you through every milestone until joy returns."
        ],
        "bodies_deep": [
            "Jesus says: I know how empty the house feels and how sudden waves of memories catch your breath in your throat. You do not have to put on a brave face before Me. I weep with those who weep, and I am gathering every tear in My bottle. You are not walking through this cemetery of grief alone; I am holding your trembling hand.",
            "Jesus says: The pain you feel is a reflection of how deeply you loved, and love never truly ends. I am breathing supernatural comfort into your aching chest tonight. In place of unbearable sorrow, I will give you sweet memories, divine peace, and the blessed hope of eternity.",
            "Jesus says: Allow yourself to rest. You will smile again, you will laugh again, and you will find purpose again. Underneath you are My everlasting arms, holding you firm through the darkest valley."
        ],
        "ctas": [
            "Save this prayer for the tender moments of grief, and drop your first name below for comforting prayer.",
            "Comment the first name of your loved one below, save this Reel, and share with someone walking through bereavement.",
            "Save this to your favorites, leave a '🕊️' below, and send it to a family member needing gentle comfort today."
        ]
    },

    "gratitude_harvest": {
        "title": "🌟 Cosecha de Gratitud y Milagros (Testimonio de bendición)",
        "description": "Oración de acción de gracias por victorias, puertas abiertas y fidelidad de Dios.",
        "scripture": "Psalm 103:2 — Bless the Lord, O my soul, and forget not all his benefits.",
        "hashtags": ["#GratitudePrayer", "#ThankYouJesus", "#GodIsFaithful", "#CountYourBlessings", "#DailyPraise"],
        "pinned_comments": [
            "👇 What is one thing you are thanking God for today? Drop your praise report below so we can celebrate with you! 🎉🙏✨",
            "👇 In everything give thanks! Type 'Thank You, Jesus' and declare His goodness in your life."
        ],
        "hook_texts": [
            "GOD HAS BEEN SO GOOD",
            "GIVE THANKS TODAY",
            "LOOK HOW FAR YOU CAME",
            "YOUR TESTIMONY IS HERE"
        ],
        "hooks": [
            "Stop and thank God for how far you've come.",
            "If God brought you through the storm, hear this praise:",
            "Do not forget all the miracles God did for you.",
            "Before you ask for more, give thanks for today."
        ],
        "bodies_micro": [
            "Jesus says: Remember where you were a year ago. I made a way when you saw no way. Enter My gates with thanksgiving and My courts with praise.",
            "Jesus says: Your gratitude opens the floodgates for even greater miracles. Keep your heart humble and thankful, and watch blessings multiply.",
            "Jesus says: I have heard your prayers, and I am smiling over your faith. Celebrate the harvest of peace and favor in your life today."
        ],
        "bodies_deep": [
            "Jesus says: Pause for just a moment in your busy day and look over your shoulder. Remember the nights you cried yourself to sleep, wondering how you would survive? Look at you now: you are standing, you are breathing, and My grace brought you through every single fire. Not one promise I made to you has failed.",
            "Jesus says: A grateful heart is fertile soil for supernatural miracles. When you choose to praise Me instead of complaining about what's missing, you invite heaven's atmosphere into your home. Count your blessings one by one and watch joy replace your weariness.",
            "Jesus says: You are a living testimony of My faithfulness. Share what I have done in your life with boldness. The best is still ahead of you; continue to walk in thanksgiving and expectancy."
        ],
        "ctas": [
            "Save this prayer of thanksgiving, and drop one thing you are grateful for below so we can rejoice together!",
            "Type 'Thank You, Jesus' and your first name in the comments, save this Reel, and share this blessing with a friend.",
            "Save this to your favorites for your quiet time, leave a '🙌' below, and send it to someone who needs a reminder of God's goodness."
        ]
    }
}

# =============================================================================
# PROCEDURAL CINEMATIC AI IMAGE GENERATION ENGINE (Combinatorial & Unique)
# =============================================================================

SCENARIO_POOLS = {
    "jesus_praying": [
        "Jesus Christ kneeling in deep reverent prayer in the Garden of Gethsemane under a gentle full moon, hands clasped, tear of sacred surrender catching ethereal moonlight, ancient olive trees in background, warm celestial halo, dramatic chiaroscuro masterpiece",
        "Jesus Christ atop an ancient mountain summit at sunrise, arms opened toward the breaking dawn in earnest prayer to the Father, golden morning sunburst illuminating His flowing white garments, peaceful and majestic atmosphere",
        "Intimate cinematic close-up of Jesus Christ praying with closed eyes and serene devotion, soft warm candlelight illuminating His compassionate face, floating golden dust motes, peaceful and deeply sacred"
    ],
    "jesus_comforting": [
        "Jesus Christ gently wiping away the tears of a brokenhearted person, looking with infinite tenderness and love, warm golden celestial glow enveloping both of them, hyper-realistic, emotionally powerful",
        "Jesus Christ with compassionate eyes looking directly into the camera, His hand reaching gently out toward the viewer in loving reassurance and healing peace, soft divine aura, 8k portrait",
        "Jesus Christ standing beside a person praying in tears beside their bed at night, His hand resting tenderly on their shoulder releasing heavenly light that dispels room shadows"
    ],
    "jesus_healing": [
        "Jesus Christ standing in gentle divine light beside a hospital bed, placing His radiant hand over a sleeping patient's heart, heavenly golden rays filling the quiet room with supernatural peace and healing",
        "Jesus Christ lovingly touching the forehead of an earnest believer kneeling in prayer, divine golden luminescence radiating from His touch, tears of miraculous relief, award-winning cinematic shot",
        "Jesus Christ surrounded by an aura of sacred restoration, reaching down with warmth and divine grace to lift up a weary soul, volumetric God-rays, photorealistic masterpiece"
    ],
    "people_praying": [
        "Devout hands tightly clasped in earnest tearful prayer resting upon an open illuminated Holy Bible, warm golden candlelight and heavenly sunbeams streaming through sacred glass, floating dust motes",
        "A humble devout believer kneeling in deep heartfelt prayer in a sunlit sanctuary, head bowed in surrender, brilliant golden shafts of divine light descending from above, atmosphere of awe and peace",
        "A loving praying mother and father with eyes closed, holding hands over their open family Bible in prayer, soft warm amber glow illuminating their faithful expressions, cinematic 35mm photography"
    ],
    "holy_bible": [
        "Extreme macro close-up of an ancient leather-bound Holy Bible open to the Psalms, golden gilded page edges catching warm radiant sunbeams, floating golden dust motes, sacred and reverent",
        "A grand wooden altar with an illuminated Holy Bible open in the center, celestial golden rays streaming directly onto the sacred scripture, soft incense mist, photorealistic masterpiece",
        "An open Holy Bible with a rustic wooden cross resting gently on the pages, warm morning golden-hour light washing over the scripture, deep emotional atmosphere"
    ],
    "holy_cross": [
        "Solemn sacred silhouette of the holy wooden cross with the crown of thorns atop Mount Calvary at golden hour sunrise, brilliant sunburst flaring through the wood, gentle morning mist rolling over ancient hills, reverent cinematic masterpiece",
        "Intimate low-angle view looking up toward the Holy Cross against a breaking dawn sky, warm heavenly colors radiating outward, peaceful, reverent, cinematic 35mm film grain",
        "Dramatic sky with sacred golden clouds parting around the glowing Holy Cross bathed in amber celestial light, shafts of glory pouring onto ancient stones, hyper-realistic 8k"
    ],
    "storm_rescue": [
        "Dramatic low-angle cinematic shot, Jesus Christ standing calmly atop roaring stormy ocean waves, reaching His hand directly out of the screen toward the viewer to pull them from churning waters, dark clouds parting to reveal blinding golden sunbeams",
        "Jesus Christ walking serenely across turbulent dark sea waters amidst lightning, glowing white robe billowing, extending a strong hand of deliverance to the viewer, hyper-detailed, epic composition",
        "Jesus Christ standing on the bow of a wooden boat in a violent storm, raising His hand with divine authority to command the wind and waves to be still, instant calm and celestial light breaking through"
    ],
    "lion_judah": [
        "Epic majestic Lion of Judah standing proudly atop a colossal mountain cliff, glowing golden mane illuminated by dramatic celestial God-rays, dark storm clouds parting in the background, sharp lightning flashes, hyper-realistic, volumetric lighting",
        "Regal golden lion representing Jesus the Lion of Judah, majestic golden eyes looking with authority, sacred divine aura, ancient stone altar, mist and golden dust motes floating, octane render 8k",
        "Powerful dynamic shot of the Lion of Judah walking triumphantly across an ancient biblical plateau, roaring with divine power, supernatural golden dawn breaking over the horizon, cinematic composition"
    ],
    "break_chains": [
        "Heavy rusted iron chains snapping and shattering into glowing golden sparks as radiant divine light bursts through, Jesus Christ standing in triumph in the background, cinematic dramatic contrast",
        "Jesus Christ gently breaking the heavy chains binding a weeping person's hands, shackles dissolving into golden dust, tears of deliverance and freedom, emotional masterpiece",
        "Colossal locked prison doors swinging wide open as the glory and light of Jesus Christ enters the darkness, shackles falling to the floor, triumphant and sacred"
    ],
    "family_blessing": [
        "Jesus Christ standing with a gentle smile, placing His hands of blessing upon the heads of young children and their parents, surrounded by warm golden daylight and peaceful olive trees, heartfelt and comforting",
        "Jesus Christ gently guiding a young child through a field of wild lilies, holding the child's small hand in loving protection, bright sunny sky with soft clouds, heartwarming biblical scene",
        "A Christian family gathered in unity around a dinner table with hands held in prayer, a luminous subtle presence of Jesus Christ standing behind them with outstretched hands of peace and protection"
    ]
}

THEME_TO_SCENARIO_MAP = {
    "zero_balance": ["jesus_comforting", "break_chains", "holy_bible", "jesus_praying"],
    "lost_child": ["family_blessing", "jesus_comforting", "storm_rescue", "people_praying"],
    "night_anxiety": ["jesus_comforting", "storm_rescue", "jesus_praying", "people_praying"],
    "medical_fear": ["jesus_healing", "jesus_comforting", "people_praying", "holy_cross"],
    "betrayal": ["jesus_comforting", "holy_cross", "jesus_praying"],
    "morning_favor": ["jesus_praying", "holy_bible", "holy_cross", "family_blessing"],
    "job_breakthrough": ["break_chains", "jesus_comforting", "holy_bible"],
    "marriage_crisis": ["family_blessing", "jesus_comforting", "people_praying"],
    "silent_depression": ["jesus_comforting", "jesus_healing", "people_praying"],
    "spiritual_warfare": ["lion_judah", "break_chains", "holy_cross"],
    "psalm_91_shield": ["lion_judah", "jesus_comforting", "holy_cross"],
    "psalm_23_valley": ["jesus_praying", "jesus_comforting", "storm_rescue"],
    "lion_of_judah": ["lion_judah", "break_chains", "holy_cross"],
    "exhausted_parent": ["family_blessing", "jesus_comforting", "people_praying"],
    "break_chains": ["break_chains", "lion_judah", "jesus_comforting"],
    "lonely_season": ["jesus_comforting", "jesus_praying", "holy_bible"],
    "unexpected_doors": ["break_chains", "jesus_comforting", "lion_judah"],
    "forgive_yourself": ["holy_cross", "jesus_comforting", "holy_bible"],
    "school_children": ["family_blessing", "jesus_comforting", "people_praying"],
    "restoration_double": ["break_chains", "jesus_comforting", "lion_judah"],
    "hard_decisions": ["jesus_praying", "holy_bible", "people_praying"],
    "peace_in_storm": ["storm_rescue", "jesus_comforting", "jesus_praying"],
    "hidden_enemies": ["lion_judah", "holy_cross", "break_chains"],
    "business_blessing": ["break_chains", "holy_bible", "jesus_comforting"],
    "grief_loss": ["jesus_comforting", "holy_cross", "people_praying"],
    "gratitude_harvest": ["holy_bible", "people_praying", "holy_cross", "family_blessing"]
}

CAMERA_STYLES = [
    "cinematic 35mm film photography, dramatic volumetric chiaroscuro lighting, octane render 8k",
    "hyper-realistic Unreal Engine 5 render, radiant golden hour sunburst, sharp focus, award winning masterpiece",
    "intimate emotional cinematic portrait, anamorphic lens, soft golden bokeh, divine atmosphere, 8k",
    "epic wide-angle panoramic cinematic shot, volumetric God-rays, high contrast, masterpiece composition"
]

CUSTOM_TOPIC_TRANSLATIONS = {
    "hijo": "a beloved child", "deuda": "heavy financial debt", "salud": "physical sickness",
    "ansiedad": "overwhelming panic and anxiety", "soledad": "deep loneliness",
    "matrimonio": "restoring a marriage", "trabajo": "finding an urgent job", "empleo": "a new career door",
    "depresion": "overcoming silent depression", "paz": "supernatural peace", "proteccion": "divine protection"
}


def generate_image_prompt_for_script(theme_key: Optional[str] = None, script_text: str = "", custom_topic: Optional[str] = None) -> str:
    """
    Generador combinatorio procedural que NUNCA repite la misma imagen.
    Selecciona múltiples categorías acordes al tema y combina estilos visuales.
    """
    candidate_pools = THEME_TO_SCENARIO_MAP.get(theme_key, list(SCENARIO_POOLS.keys()))
    chosen_category = random.choice(candidate_pools)
    base_scene = random.choice(SCENARIO_POOLS[chosen_category])
    chosen_style = random.choice(CAMERA_STYLES)

    custom_cue = ""
    if custom_topic and custom_topic.strip():
        clean_topic = custom_topic.strip().lower()
        trans = CUSTOM_TOPIC_TRANSLATIONS.get(clean_topic, clean_topic)
        custom_cue = f", spiritually touching theme of {trans}"

    return f"{base_scene}{custom_cue}, {chosen_style}, dynamic framing, sacred golden light, hyper-detailed, NOT flat, masterpiece"


def generate_seo_caption(theme_key: str, hook: str, body: str, cta: str) -> str:
    theme = VIRAL_THEMES.get(theme_key, VIRAL_THEMES["morning_favor"])
    scripture = theme.get("scripture", "Psalm 34:18 — The Lord is close to the brokenhearted.")
    hashtags = " ".join(theme.get("hashtags", ["#DailyPrayer", "#ChristianReels", "#FaithInGod"]))
    return f"{hook} 🙏✨\n\n📖 Scripture: {scripture}\n\n{cta}\n\n{hashtags}"


def generate_script(theme_key: Optional[str] = None, custom_topic: Optional[str] = None, mode: str = "deep") -> Dict[str, str]:
    """
    Genera un guion optimizado para Meta 2026.
    Soporta dos modalidades de retención:
    - mode="micro" (12-16s): Alta tasa de bucle/finalización, rápido, directo.
    - mode="deep" (25-32s): 4 actos (Gancho -> Dolor/Empatía -> Giro Milagroso -> Llamado de Fe).
    """
    if theme_key and theme_key in VIRAL_THEMES:
        chosen_key = theme_key
    else:
        chosen_key = random.choice(list(VIRAL_THEMES.keys()))

    theme = VIRAL_THEMES[chosen_key]
    hook = random.choice(theme["hooks"])
    hook_text = random.choice(theme["hook_texts"])
    cta = random.choice(theme["ctas"])

    if mode == "micro":
        body = random.choice(theme.get("bodies_micro", theme.get("bodies", ["Jesus says: Stand firm in faith."])))
    else: # deep mode
        body = random.choice(theme.get("bodies_deep", theme.get("bodies", ["Jesus says: Stand firm in faith."])))

    if custom_topic and custom_topic.strip():
        topic = custom_topic.strip().lower()
        clean_topic = CUSTOM_TOPIC_TRANSLATIONS.get(topic, topic)
        hook = f"Stop scrolling if you need a miracle in {clean_topic} today:"

    full_text = f"{hook} {body} {cta}"
    image_prompt = generate_image_prompt_for_script(chosen_key, full_text, custom_topic)
    seo_caption = generate_seo_caption(chosen_key, hook, body, cta)
    pinned_comment = random.choice(theme.get("pinned_comments", ["👇 Let's pray together. How can we pray for you today? Drop your request below."]))

    return {
        "theme": theme["title"],
        "theme_key": chosen_key,
        "mode": mode,
        "hook": hook,
        "body": body,
        "cta": cta,
        "hook_text": hook_text,
        "full_text": full_text,
        "image_prompt": image_prompt,
        "seo_caption": seo_caption,
        "scripture": theme["scripture"],
        "pinned_comment": pinned_comment
    }


def get_themes_list():
    return [{"key": k, "title": v["title"], "description": v["description"]} for k, v in VIRAL_THEMES.items()]
