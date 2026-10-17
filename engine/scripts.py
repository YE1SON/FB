import random
import re
from typing import Dict, List, Optional

# =============================================================================
# HYPER-SPECIFIC PAIN POINT THEMES (Meta 2026 Optimized - 26 Categorías)
# Estructura Estricta: In Media Res (0.0s), 38-46 Palabras, Intercesión Familiar,
# 3 Prompts de Escena 9:16, Comentario Magnético y Doble Insignia Superior.
# =============================================================================

VIRAL_THEMES = {
    "lost_child": {
        "title": "🚶‍♂️ Por el hijo/hija que se alejó de Dios",
        "description": "Oración intercesora de un padre/madre por un hijo en rebeldía o dolor.",
        "target_time_slot": "night",
        "hook_badge_text": "PRAYER FOR YOUR CHILDREN",
        "micro_cta_text": "💬 Leave their first name below",
        "script_english": "Lord, place a hedge of protection around my children and grandchildren tonight. Silence every anxious thought, guard their steps, and cover their homes in peace. What was meant to bring worry, turn into praise. Send this covering to someone you love, and whisper Amen.",
        "scene_1_prompt": "Photorealistic emotional close-up: an open Bible beside a warm coffee mug on a rustic wooden table, soft evening sunlight casting long shadows, 8k resolution, cinematic lighting --ar 9:16",
        "scene_2_prompt": "Cinematic visual of a mother praying quietly by a window, golden hour atmospheric haze, warm tones, high detail --ar 9:16",
        "scene_3_prompt": "Jesus walking gently beside family members on a tranquil path, bathed in divine golden hour light, peaceful, photorealistic --ar 9:16",
        "scripture": "Luke 15:20 — But while he was still a long way off, his father saw him and was filled with compassion.",
        "pinned_comment": "I am lifting up every son and daughter represented here tonight. What is the first name or initial of the child you want me to pray for right now? 🙏",
        "hashtags": ["#PrayingParents", "#FaithInGod", "#Psalm91", "#ChristianFamily", "#ProdigalChild"]
    },

    "family_protection": {
        "title": "🛡️ Muro de Fuego sobre tu Hogar y Familia",
        "description": "Cobertura angelical contra ataques, peligros y discordias familiares.",
        "target_time_slot": "night",
        "hook_badge_text": "PROTECTION OVER YOUR FAMILY",
        "micro_cta_text": "💬 Type your family's initial",
        "script_english": "Father, station warrior angels around my family's home tonight. Cancel every assignment of sickness, shield our doorway from harm, and fill our bedrooms with holy serenity. No weapon formed against us shall prosper. Send this protection to your family, and whisper Amen.",
        "scene_1_prompt": "Warm glowing home living room at twilight, peaceful family sanctuary, soft candlelight, photorealistic cinematic 8k --ar 9:16",
        "scene_2_prompt": "Golden angelic presence gently guarding over a sleeping house under a starry sky, ethereal volumetric light, hyper-detailed --ar 9:16",
        "scene_3_prompt": "Jesus with hands outstretched blessing a loving family embracing in peace, radiant divine gold aura, award-winning lighting --ar 9:16",
        "scripture": "Psalm 91:11 — For he will command his angels concerning you to guard you in all your ways.",
        "pinned_comment": "Every home covered in prayer is unbreakable. Type your family's last name or initial below so we can stand in agreement for complete protection tonight! ❤️",
        "hashtags": ["#FamilyPrayer", "#Psalm91", "#AngelsGuarding", "#ChristianHome", "#DailyPrayer"]
    },

    "medical_fear": {
        "title": "🩺 Miedo a Diagnósticos Médicos y Dolores Físicos",
        "description": "Sanidad milagrosa inmediata en cuerpo, órganos y mente.",
        "target_time_slot": "midday",
        "hook_badge_text": "HEALING OVER YOUR BODY",
        "micro_cta_text": "💬 Drop a name for healing",
        "script_english": "Jesus, touch the place in this body that feels exhausted, inflamed, and afraid today. Infuse divine strength into every cell, reverse medical reports, and breathe supernatural life from head to toe. What doctors call impossible, You redeem. Send this healing to someone hurting, and whisper Amen.",
        "scene_1_prompt": "Quiet room with morning sunlight streaming through sheer curtains, gentle atmosphere of rest, medical report on table beside a cross --ar 9:16",
        "scene_2_prompt": "Caring Christian elder with eyes closed in fervent, heartfelt prayer, soft warm lighting, deep emotion, hyper-realistic --ar 9:16",
        "scene_3_prompt": "Jesus gently placing His glowing hand upon a weary person's shoulder, radiant healing warmth, joyful restoration, photorealistic 8k --ar 9:16",
        "scripture": "Isaiah 53:5 — By his wounds we are healed.",
        "pinned_comment": "Sickness does not have the final say. Drop the first name of anyone needing physical or emotional healing today so we can lift them up! 🕊️",
        "hashtags": ["#HealingPrayer", "#MiracleWorker", "#ByHisStripes", "#FaithOverFear", "#JesusHeals"]
    },

    "zero_balance": {
        "title": "💸 Provisión Sobrenatural y Deudas Canceladas",
        "description": "Ruptura de escasez, angustia bancaria y puertas abiertas de bendición.",
        "target_time_slot": "night",
        "hook_badge_text": "FINANCIAL BREAKTHROUGH TODAY",
        "micro_cta_text": "💬 Claim God's provision below",
        "script_english": "Lord, You see the unpaid bills, the heavy numbers, and the silent tightness in this chest. Break the spirit of financial lack right now, unlock unexpected favor, and restore honorable abundance to this household. Send this promise to a family needing breakthrough, and whisper Amen.",
        "scene_1_prompt": "A worn wooden desk with bills and a glowing open Bible, warm cinematic desk lamp light, authentic atmosphere of perseverance --ar 9:16",
        "scene_2_prompt": "Hands folded tightly in desperate prayer over an open ledger, warm golden tears, emotional photorealism --ar 9:16",
        "scene_3_prompt": "Jesus smiling with open hands releasing radiant golden light and abundance into a humble home, divine majesty, masterpiece --ar 9:16",
        "scripture": "Philippians 4:19 — And my God will supply every need of yours according to his riches in glory.",
        "pinned_comment": "God owns the cattle on a thousand hills. If you are trusting God for a financial miracle before this week ends, drop your first name below! 💸",
        "hashtags": ["#FinancialMiracle", "#DebtFreeInJesus", "#GodProvides", "#FaithOverWorry", "#KingdomFavor"]
    },

    "night_anxiety": {
        "title": "🌌 Ansiedad a las 3 AM (Insomnio y Ataques de Pánico)",
        "description": "Paz sobrenatural para mentes saturadas de miedo en la madrugada.",
        "target_time_slot": "night",
        "hook_badge_text": "PEACE TO YOUR MIND",
        "micro_cta_text": "💬 Drop a '🙏' for calm",
        "script_english": "Jesus, step into this quiet bedroom and calm every racing thought tormenting this exhausted mind. Dispel the darkness of midnight panic, wrap this soul in heavenly safety, and grant sweet, unbroken rest until morning light. Send this tranquil peace to someone fighting anxiety, and whisper Amen.",
        "scene_1_prompt": "A quiet bedroom lit only by soft moonlight through an open window, delicate night air, tranquil cinematic atmosphere --ar 9:16",
        "scene_2_prompt": "A person sitting peacefully on edge of bed taking a deep breath of relief, moonlight falling on their hands --ar 9:16",
        "scene_3_prompt": "Jesus standing gently beside the bed, radiating comforting celestial peace and golden aura, whispering tranquility, 8k --ar 9:16",
        "scripture": "Psalm 4:8 — In peace I will lie down and sleep, for you alone, Lord, make me dwell in safety.",
        "pinned_comment": "If you woke up carrying heavy thoughts tonight, breathe. You are safe in Jesus. Drop a '🙏' below so our night prayer team can cover you right now.",
        "hashtags": ["#NightPrayer", "#PeaceOfGod", "#OvercomingAnxiety", "#SleepInPeace", "#MentalCalm"]
    },

    "morning_favor": {
        "title": "🌅 Bendición y Favor de la Mañana",
        "description": "Comenzar el día coronado de gracia, misericordia y puertas abiertas.",
        "target_time_slot": "morning",
        "hook_badge_text": "MORNING BLESSING & FAVOR",
        "micro_cta_text": "💬 Receive this morning blessing",
        "script_english": "Heavenly Father, as this morning sun rises, anoint my family with fresh grace, favor, and divine wisdom. Guard our tongues, guide our steps, and open doors of opportunity that no human can shut today. Send this sunrise blessing to someone you cherish, and whisper Amen.",
        "scene_1_prompt": "Golden sunrise over misty green hills, rays of sunlight piercing through clouds, majestic dawn, photorealistic landscape --ar 9:16",
        "scene_2_prompt": "Open Bible on a rustic porch with warm morning coffee, steam rising into golden sunlight, peaceful devotion --ar 9:16",
        "scene_3_prompt": "Jesus walking at daybreak with open arms, surrounded by brilliant morning light and birds, welcoming a victorious new day --ar 9:16",
        "scripture": "Lamentations 3:22-23 — His mercies never come to an end; they are new every morning.",
        "pinned_comment": "Claim your morning victory before you step out the door. Type 'I RECEIVE IT' below and dedicate your day to God! 🌅",
        "hashtags": ["#MorningPrayer", "#DailyDevotional", "#NewMercies", "#GodsFavor", "#BlessedDay"]
    },

    "marriage_healing": {
        "title": "💍 Restauración y Sanidad en el Matrimonio",
        "description": "Reconciliación de parejas, perdón mutuo y disipación de la amargura.",
        "target_time_slot": "midday",
        "hook_badge_text": "HEALING IN YOUR MARRIAGE",
        "micro_cta_text": "💬 Pray for your marriage below",
        "script_english": "Lord, pour healing balm over this marriage where distance and weariness have crept in. Soften hardened hearts, rekindle the gentle laughter of first love, and unite this couple under Your unbreakable covenant. Send this restoration to a couple fighting for their marriage, and whisper Amen.",
        "scene_1_prompt": "Two wedding bands resting on an open worn Bible, warm candlelight, deep reverence and solemn beauty --ar 9:16",
        "scene_2_prompt": "Husband and wife gently holding hands with heads bowed together in quiet tearful prayer, warm kitchen table, photorealistic --ar 9:16",
        "scene_3_prompt": "Jesus placing His hands over the joined hands of a couple, golden cords of divine unity glowing, radiant restoration --ar 9:16",
        "scripture": "Colossians 3:14 — And over all these virtues put on love, which binds them all together in perfect unity.",
        "pinned_comment": "God can resurrect what seems broken beyond repair. Leave your initials below so we can intercede for your marriage and family tonight. ❤️",
        "hashtags": ["#MarriagePrayer", "#ChristianCouples", "#HealingRelationships", "#CovenantLove", "#FaithfulGod"]
    },

    "healing_depression": {
        "title": "🌤️ Salir de la Depresión y el Cansancio del Alma",
        "description": "Renovación de gozo, fuerza interior y esperanza para el alma abatida.",
        "target_time_slot": "midday",
        "hook_badge_text": "JOY RESTORED IN JESUS",
        "micro_cta_text": "💬 You are not alone, comment below",
        "script_english": "Jesus, lift the heavy fog suffocating this precious soul today. When simple tasks feel overwhelming, become their breath, steady anchor, and living hope. Crown their head with joy and turn weeping into morning songs. Send this lifeline to a friend fighting battles, and whisper Amen.",
        "scene_1_prompt": "A person sitting quietly in a warm garden as dawn breaks, golden sunlight warming their face, authentic emotional peace --ar 9:16",
        "scene_2_prompt": "Close-up of hands releasing dry withered leaves, and fresh green sprouts emerging, metaphor of renewed life --ar 9:16",
        "scene_3_prompt": "Jesus embracing a weary person with tender compassionate love, lifting their head, wiping a tear away with golden divine light --ar 9:16",
        "scripture": "Psalm 30:5 — Weeping may stay for the night, but rejoicing comes in the morning.",
        "pinned_comment": "Your story is not over. If your soul feels heavy today, leave a small heart '❤️' below so our community can pray over your strength today.",
        "hashtags": ["#HopeInChrist", "#OvercomingDepression", "#JoyComes", "#MentalHealthFaith", "#JesusCares"]
    },

    "job_breakthrough": {
        "title": "💼 Nueva Puerta de Empleo y Trabajo Digno",
        "description": "Favor en entrevistas, contratación rápida y dignificación laboral.",
        "target_time_slot": "morning",
        "hook_badge_text": "DOORS ARE OPENING TODAY",
        "micro_cta_text": "💬 Claim your employment breakthrough",
        "script_english": "Father, crown this job search with supernatural favor before hiring managers today. Unlock the open door destined for their gifts, provide honorable income, and restore dignity to their labor. What was shut down, turn into promotion. Send this faith to someone seeking work, and whisper Amen.",
        "scene_1_prompt": "A person dressed professionally pausing before a door with hand on heart in silent prayer, soft morning light --ar 9:16",
        "scene_2_prompt": "A large ancient door unlocking with warm golden light spilling through the doorway, photorealistic cinematic lighting --ar 9:16",
        "scene_3_prompt": "Jesus leading a faithful worker forward through open doors into bright honorable future, radiant blessing --ar 9:16",
        "scripture": "Revelation 3:8 — See, I have placed before you an open door that no one can shut.",
        "pinned_comment": "God prepares the table where others saw only closed doors. Drop your first name below if you are praying for a career or job breakthrough this week! 💼",
        "hashtags": ["#JobPrayer", "#OpenDoors", "#CareerBreakthrough", "#GodIsMyProvider", "#WorkplaceBlessing"]
    },

    "lonely_widow": {
        "title": "🕯️ Consuelo para la Soledad y Pérdida de un Ser Querido",
        "description": "Compañía divina en una casa silenciosa, abrazo del Salvador.",
        "target_time_slot": "night",
        "hook_badge_text": "GOD SEES YOUR TEARS",
        "micro_cta_text": "💬 Share your beloved's initial",
        "script_english": "Precious Lord, sit beside the one who walks into a silent house tonight feeling unseen and aching from grief. Be their companion, wrap Your tender arms around their fragile heart, and remind them they are never abandoned. Send this comfort to someone grieving, and whisper Amen.",
        "scene_1_prompt": "A comfortable armchair beside an open window at sunset, a warm blanket, a single candle burning steadily --ar 9:16",
        "scene_2_prompt": "Elderly woman sitting peacefully holding a framed photo to her heart, eyes closed in gentle remembrance --ar 9:16",
        "scene_3_prompt": "Jesus sitting gently beside her on the bench, putting an arm around her shoulder with divine golden warmth, everlasting comfort --ar 9:16",
        "scripture": "Psalm 34:18 — The Lord is close to the brokenhearted and saves those who are crushed in spirit.",
        "pinned_comment": "You are never truly alone. If your heart misses someone deeply tonight, type their initial below and let us hold you in loving prayer. 🕊️",
        "hashtags": ["#GriefSupport", "#GodComforts", "#NeverAlone", "#HealingHeart", "#FaithInLoss"]
    },

    "addiction_chains": {
        "title": "⛓️ Rompiendo Cadenas de Vicios y Adicciones",
        "description": "Liberación espiritual de alcohol, sustancias, pornografía o hábitos destructivos.",
        "target_time_slot": "midday",
        "hook_badge_text": "CHAINS ARE BREAKING NOW",
        "micro_cta_text": "💬 Claim freedom in Jesus' name",
        "script_english": "Almighty God, sever every invisible chain of addiction and shame binding this beloved soul today. Fill the empty ache with Your Spirit, shatter the power of secret relapse, and establish their feet upon solid rock. Send this freedom to someone fighting for sobriety, and whisper Amen.",
        "scene_1_prompt": "Heavy iron chains wrapped around hands falling apart and shattering into golden dust, dramatic cinematic chiaroscuro --ar 9:16",
        "scene_2_prompt": "A person kneeling before a wooden cross in a dimly lit chapel, tears of breakthrough and surrender --ar 9:16",
        "scene_3_prompt": "Jesus standing victorious with hands raised, breaking chains off a free person who stands tall in bright sunlight --ar 9:16",
        "scripture": "John 8:36 — So if the Son sets you free, you will be free indeed.",
        "pinned_comment": "There is no chain that the blood of Jesus cannot snap. Drop a first name below for total freedom and restoration from addictions. ⛓️✨",
        "hashtags": ["#FreedomInChrist", "#ChainsBroken", "#SobrietyPrayer", "#Deliverance", "#JesusSaves"]
    },

    "elderly_parents": {
        "title": "👵 Por la Salud y Fuerza de Padres Ancianos",
        "description": "Cuidado tierno, lucidez mental y fortaleza para los abuelos y padres mayores.",
        "target_time_slot": "midday",
        "hook_badge_text": "PRAYER FOR AGING PARENTS",
        "micro_cta_text": "💬 Leave your parent's first name",
        "script_english": "Lord Jesus, preserve the minds, bones, and fragile steps of my aging parents and grandparents today. Spare them from falls, fill their golden years with sweet dignity, and surround them with honoring love. Send this tender prayer to someone cherishing their parents, and whisper Amen.",
        "scene_1_prompt": "Elderly hands with wedding ring resting gently on a worn Bible, warm sunlight, photorealistic portrait --ar 9:16",
        "scene_2_prompt": "Adult child holding the hand of an elderly mother in a sunlit garden, peaceful smile, heartwarming --ar 9:16",
        "scene_3_prompt": "Jesus walking beside an elderly parent, supporting their arm with great tenderness and golden celestial aura --ar 9:16",
        "scripture": "Isaiah 46:4 — Even to your old age and gray hairs I am he, I am he who will sustain you.",
        "pinned_comment": "Our parents carried us, now we carry them in prayer. Drop the first name of your mother, father, or grandparent below so we can bless them today. 👴👵",
        "hashtags": ["#AgingParents", "#HonoringParents", "#ElderlyCare", "#FamilyBlessing", "#FaithfulGeneration"]
    },

    "single_parent": {
        "title": "👩‍👧 Fortaleza Sobrenatural para Madres/Padres Solteros",
        "description": "Paz cuando las fuerzas se agotan al criar a los hijos sin apoyo.",
        "target_time_slot": "night",
        "hook_badge_text": "STRENGTH FOR SINGLE PARENTS",
        "micro_cta_text": "💬 You are seen, leave your name",
        "script_english": "Father, be the helper to the weary parent carrying the burden of family alone tonight. Multiply their physical energy, provide for every school bill, and let their children rise up and call them blessed. Send this empowerment to a dedicated single parent, and whisper Amen.",
        "scene_1_prompt": "A quiet kitchen late at night, lunchboxes lined up neatly, mother sitting with tired smile looking at children's drawings --ar 9:16",
        "scene_2_prompt": "Mother hugging her young child tightly with deep maternal love, warm golden evening light, emotional cinematic --ar 9:16",
        "scene_3_prompt": "Jesus standing behind the single parent, placing His hands on their shoulders with divine strength and radiant honor --ar 9:16",
        "scripture": "Psalm 68:5 — A father to the fatherless, a defender of widows, is God in his holy dwelling.",
        "pinned_comment": "You are doing an incredible job, and God sees every sacrifice. Leave your first name below so we can cover you and your children in prayer tonight! 💕",
        "hashtags": ["#SingleMomStrong", "#SingleDadLife", "#GodProvides", "#ParentingByFaith", "#SupernaturalStrength"]
    },

    "sick_grandchild": {
        "title": "👶 Sanidad Urgente para un Nieto o Bebé Enfermo",
        "description": "Intercesión de abuelos por la recuperación de fiebre, virus o enfermedad infantil.",
        "target_time_slot": "midday",
        "hook_badge_text": "HEALING FOR YOUR GRANDCHILD",
        "micro_cta_text": "💬 Drop your grandchild's name",
        "script_english": "Lord, rebuke the fever, breathe life into weak lungs, and command rapid healing over this sick child today. Restore color to their cheeks, restore peaceful sleep to their parents, and let vitality overflow their body. Send this urgent covering to a praying grandparent, and whisper Amen.",
        "scene_1_prompt": "Child's bedside with gentle teddy bear, soft ambient night light, serene atmosphere of prayer --ar 9:16",
        "scene_2_prompt": "Grandmother kneeling in prayer beside a crib with tearful eyes full of faith, warm photorealistic --ar 9:16",
        "scene_3_prompt": "Jesus standing over a peaceful sleeping child, gently laying His radiant hand upon their forehead, divine healing glow --ar 9:16",
        "scripture": "Matthew 19:14 — Jesus said, 'Let the little children come to me, and do not hinder them, for the kingdom of heaven belongs to such as these.'",
        "pinned_comment": "A grandparent's prayer builds an iron shield. Drop the first name of your grandchild below so we can declare health and recovery over them right now! 🙏",
        "hashtags": ["#GrandparentsPray", "#ChildHealing", "#FaithOverFear", "#JesusLovesKids", "#MiraclesHappen"]
    },

    "court_legal": {
        "title": "⚖️ Victoria en Batallas Legales, Custodias o Juicios",
        "description": "Intervención del Juez Supremo para que la verdad y la justicia prevalezcan.",
        "target_time_slot": "morning",
        "hook_badge_text": "VICTORY IN YOUR BATTLE",
        "micro_cta_text": "💬 Claim God's justice below",
        "script_english": "Righteous Judge, step into every courtroom, legal document, and contentious meeting facing this family today. Expose every deceitful voice, soften the hearts of judges, and release a ruling wrapped in undeniable truth and peace. What enemies plotted for ruin, turn into victory, and whisper Amen.",
        "scene_1_prompt": "Wooden gavel resting on legal documents next to a small pocket Bible, dramatic courtroom lighting --ar 9:16",
        "scene_2_prompt": "Person holding hands in prayer with attorney or family member in hallway before courtroom doors --ar 9:16",
        "scene_3_prompt": "Jesus standing tall as divine advocate with golden light defending a faithful family, majestic justice, cinematic --ar 9:16",
        "scripture": "Psalm 37:6 — He will make your righteous reward shine like the dawn, your vindication like the noonday sun.",
        "pinned_comment": "God is your greatest advocate in every trial. Type 'AMEN' and leave your first name below so we can stand in agreement for complete victory and favor! ⚖️",
        "hashtags": ["#GodOfJustice", "#LegalBreakthrough", "#DivineAdvocate", "#TruthPrevails", "#VictoryInJesus"]
    },

    "restless_sleep": {
        "title": "🛌 Sueño Dulce y Descanso Reparador",
        "description": "Romper el ciclo de agotamiento crónico y despertar con nueva energía.",
        "target_time_slot": "night",
        "hook_badge_text": "DEEP REST TONIGHT",
        "micro_cta_text": "💬 Receive peaceful sleep tonight",
        "script_english": "Lord, quiet the storm of worries and nervous exhaustion pressing against this heart tonight. Station angels of peace beside this bed, calm breathing, and grant refreshing, dreamless sleep that restores strength for tomorrow. Send this peaceful rest to someone who cannot sleep, and whisper Amen.",
        "scene_1_prompt": "Quiet bedroom with cozy warm quilt, soft moonlight pouring across the floor, tranquil atmosphere --ar 9:16",
        "scene_2_prompt": "Person breathing out a long sigh of relief, sinking into pillows with serene peaceful expression --ar 9:16",
        "scene_3_prompt": "Jesus gently watching over the bed, extending His hands to smooth the air with soft golden peaceful light --ar 9:16",
        "scripture": "Proverbs 3:24 — When you lie down, you will not be afraid; when you lie down, your sleep will be sweet.",
        "pinned_comment": "Tonight you will sleep without fear. Type 'I RECEIVE REST' below and release every burden of the day into God's hands. 🛌✨",
        "hashtags": ["#SweetSleep", "#NightPrayer", "#PeacefulNight", "#RestInGod", "#SleepWell"]
    },

    "gratitude_harvest": {
        "title": "🌾 Gratitud por Bendiciones y Oraciones Respondidas",
        "description": "Celebración de la fidelidad de Dios y multiplicación de la cosecha espiritual.",
        "target_time_slot": "morning",
        "hook_badge_text": "THANK YOU JESUS TODAY",
        "micro_cta_text": "💬 Share one blessing you have",
        "script_english": "Lord Jesus, with joyful tears, I pause to thank You for fighting unseen battles and sustaining breath in my lungs. Multiply every harvest of blessing, keep my heart humble, and let my story bring hope. Send this praise to someone, and whisper Amen.",
        "scene_1_prompt": "Golden wheat field swaying under bright morning sun, rays of light illuminating the harvest, majestic nature --ar 9:16",
        "scene_2_prompt": "Person standing outdoors with open hands and joyful face lifted toward warm sunlight in thankful praise --ar 9:16",
        "scene_3_prompt": "Jesus smiling with deep love and joy, welcoming a grateful soul into a radiant field of heavenly flowers --ar 9:16",
        "scripture": "Psalm 107:1 — Give thanks to the Lord, for he is good; his love endures forever.",
        "pinned_comment": "Gratitude unlocks the next miracle. Comment 'THANK YOU JESUS' below and share one thing you are grateful for today! 🙌",
        "hashtags": ["#PraiseTheLord", "#GratefulHeart", "#AnsweredPrayers", "#FaithHarvest", "#ThankYouJesus"]
    },

    "unspoken_prayer": {
        "title": "🤫 Por la Petición Secreta que Nadie Sabe",
        "description": "La oración que no se puede decir en voz alta pero Dios conoce en lo secreto.",
        "target_time_slot": "night",
        "hook_badge_text": "GOD HEARS YOUR HEART",
        "micro_cta_text": "💬 Drop a '🙏' for your secret prayer",
        "script_english": "Father, You hear the secret groan of this heart that words cannot articulate. Answer the unspoken cry whispered into the pillow, remove the hidden shame, and bring a breakthrough proving You were listening all along. Send this comfort to someone hurting, and whisper Amen.",
        "scene_1_prompt": "A quiet chapel corner with solitary candle flickering softly in the evening shadows, sacred peace --ar 9:16",
        "scene_2_prompt": "Person sitting alone in reverence, holding their heart with a tear rolling down their cheek, sincere faith --ar 9:16",
        "scene_3_prompt": "Jesus sitting close, whispering gently into their ear, surrounded by soft divine halo and sacred presence --ar 9:16",
        "scripture": "Romans 8:26 — The Spirit himself intercedes for us through wordless groans.",
        "pinned_comment": "You don't have to explain it to us; God already knows every detail. Just drop a '🙏' below to stand in silent agreement with thousands of believers. 🕊️",
        "hashtags": ["#UnspokenPrayer", "#GodKnows", "#SilentTears", "#SecretMiracle", "#FaithfulFather"]
    },

    "spiritual_warfare": {
        "title": "⚔️ Rompiendo Opresiones Espirituales y Ataques Ocultos",
        "description": "Autoridad en el nombre de Jesús sobre pesadillas, opresión y miedo.",
        "target_time_slot": "night",
        "hook_badge_text": "ANGELS SURROUND YOUR HOME",
        "micro_cta_text": "💬 Declare victory in Jesus' name",
        "script_english": "In the mighty name of Jesus, I command every spirit of dread, confusion, and spiritual oppression to flee this home right now. We plead the blood of Jesus over our doorway, family, and future. No darkness can withstand Your light. Send this covering, and whisper Amen.",
        "scene_1_prompt": "Radiant glowing cross standing tall against dark storm clouds, piercing darkness with brilliant golden light --ar 9:16",
        "scene_2_prompt": "Believer standing bold in prayer with Bible held firmly, surrounded by golden shield of faith --ar 9:16",
        "scene_3_prompt": "Jesus in radiant armor and white robe, standing as mighty protector over a peaceful home, majestic authority --ar 9:16",
        "scripture": "James 4:7 — Resist the devil, and he will flee from you.",
        "pinned_comment": "No weapon formed against you shall stand. Declare 'VICTORY IN JESUS' below and claim total authority over your home tonight! ⚔️🛡️",
        "hashtags": ["#SpiritualWarfare", "#BloodOfJesus", "#ArmorOfGod", "#VictoryInChrist", "#MightyDeliverer"]
    },

    "business_blessing": {
        "title": "💼 Bendición en Negocios y Emprendimientos",
        "description": "Multiplicación de clientes, honestidad y prosperidad en las ventas.",
        "target_time_slot": "morning",
        "hook_badge_text": "FAVOR ON YOUR WORK",
        "micro_cta_text": "💬 Pray for your business below",
        "script_english": "Lord, bless the work of these hands, bring faithful clients, and give supernatural wisdom to manage transactions with integrity. Let this business become a fountain of blessing for family, protected from economic drought. Send this favor to a hardworking entrepreneur you know, and whisper Amen.",
        "scene_1_prompt": "Small business storefront at dawn with warm lights turning on, fresh start of a blessed workday --ar 9:16",
        "scene_2_prompt": "Business owner bowing head over workspace in brief morning dedication prayer, warm sunrise lighting --ar 9:16",
        "scene_3_prompt": "Jesus placing His hands over the hands of a hardworking tradesperson/entrepreneur, divine blessing overflowing --ar 9:16",
        "scripture": "Deuteronomy 28:8 — The Lord will send a blessing on your barns and on everything you put your hand to.",
        "pinned_comment": "God wants to bless the work of your hands so you can be a blessing to others. Leave your business or trade name below for prayer! 💼",
        "hashtags": ["#BusinessBlessing", "#FaithInBusiness", "#ChristianEntrepreneur", "#KingdomWealth", "#DailyFavor"]
    }
}

# Scenario Pools for Image Generation
SCENARIO_POOLS = {
    "holy_bible": [
        "Photorealistic close-up of an ancient open Holy Bible resting on a rustic wooden table, morning sunlight, golden dust motes",
        "Worn leather-bound Bible open to Psalms with a soft candlelight glow, reverent and peaceful atmosphere",
        "Hands gently resting upon an open illuminated scripture, warm golden volumetric sunbeams, hyper-detailed"
    ],
    "people_praying": [
        "A loving grandmother with tearful eyes of faith holding her hands in prayer, soft warm window light, 8k portrait",
        "A humble father kneeling by an open window in deep heartfelt intercession, morning golden hour haze",
        "A devoted mother gently comforting her sleeping child with a hand on their head in prayer, peaceful nursery"
    ],
    "jesus_comforting": [
        "Jesus Christ with compassionate warm eyes placing His gentle hands on a weeping person's shoulder, radiant aura",
        "Jesus walking beside a weary family along a tranquil sunlit path, divine golden hour glow, cinematic 8k",
        "Jesus extending His luminous sacred hands forward to embrace the viewer, majestic and holy presence"
    ],
    "family_blessing": [
        "A multi-generational family holding hands around a humble dinner table in grateful prayer, warm cinematic light",
        "A mother and daughter walking in a sun-drenched flower meadow, peaceful divine protection, photorealistic",
        "A father reading scripture to his attentive young children before bedtime, cozy warm bedroom atmosphere"
    ],
    "break_chains": [
        "Heavy iron chains bursting into glowing golden dust in mid-air, dramatic volumetric God-rays, high contrast",
        "A glowing golden cross on a rugged mountain peak at dawn, breaking through dark storm clouds",
        "A person standing tall with hands lifted in victorious praise as heavenly light streams down from open skies"
    ]
}

THEME_TO_SCENARIO_MAP = {
    "lost_child": ["family_blessing", "people_praying", "jesus_comforting"],
    "family_protection": ["family_blessing", "jesus_comforting", "holy_bible"],
    "medical_fear": ["jesus_comforting", "people_praying", "holy_bible"],
    "zero_balance": ["holy_bible", "people_praying", "break_chains"],
    "night_anxiety": ["jesus_comforting", "people_praying", "holy_bible"],
    "morning_favor": ["holy_bible", "jesus_comforting", "family_blessing"],
    "marriage_healing": ["family_blessing", "jesus_comforting", "people_praying"],
    "healing_depression": ["jesus_comforting", "break_chains", "people_praying"],
    "job_breakthrough": ["holy_bible", "break_chains", "jesus_comforting"],
    "lonely_widow": ["jesus_comforting", "people_praying", "holy_bible"],
    "addiction_chains": ["break_chains", "jesus_comforting", "people_praying"],
    "elderly_parents": ["family_blessing", "jesus_comforting", "people_praying"],
    "single_parent": ["family_blessing", "jesus_comforting", "people_praying"],
    "sick_grandchild": ["jesus_comforting", "people_praying", "family_blessing"],
    "court_legal": ["break_chains", "holy_bible", "jesus_comforting"],
    "restless_sleep": ["jesus_comforting", "people_praying", "holy_bible"],
    "gratitude_harvest": ["holy_bible", "family_blessing", "jesus_comforting"],
    "unspoken_prayer": ["people_praying", "jesus_comforting", "holy_bible"],
    "spiritual_warfare": ["break_chains", "jesus_comforting", "holy_bible"],
    "business_blessing": ["holy_bible", "family_blessing", "break_chains"]
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
    Genera un prompt hiperrealista para DALL-E / Flux que coincide con el guion.
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

    return f"{base_scene}{custom_cue}, {chosen_style}, dynamic framing, sacred golden light, hyper-detailed, masterpiece --ar 9:16"


def generate_seo_caption(theme_key: str, prayer_text: str, scripture: str, cta: str, hashtags: List[str]) -> str:
    tags_str = " ".join(hashtags)
    return (
        f"⚡ PRAYER COVERING FOR YOUR HOME TODAY\n\n"
        f"{prayer_text}\n\n"
        f"📖 SCRIPTURE TODAY:\n\"{scripture}\"\n\n"
        f"👇 COMMENT BELOW:\n"
        f"Drop your first name or initial so our community can agree with you in prayer tonight.\n\n"
        f"{tags_str}"
    )


def generate_script(theme_key: Optional[str] = None, custom_topic: Optional[str] = None, mode: str = "deep") -> Dict[str, str]:
    """
    Genera un guion de 38 a 46 palabras cumpliendo las reglas estrictas de retención:
    - Sin palabras prohibidas (No 'Stop scrolling', No 'Wait', No 'Don't scroll').
    - In Media Res: 0.0s inicio inmediato dirigiéndose a Dios o al dolor familiar.
    - Gatillo de intercesión familiar para compartir por Messenger.
    - 3 Prompts de Escena para el pipeline de 3 tomas.
    """
    if theme_key and theme_key in VIRAL_THEMES:
        chosen_key = theme_key
    else:
        chosen_key = random.choice(list(VIRAL_THEMES.keys()))

    theme = VIRAL_THEMES[chosen_key]
    script_english = theme["script_english"]

    # Separar para los campos del editor de la UI
    sentences = [s.strip() for s in script_english.split(".") if s.strip()]
    hook = f"{sentences[0]}." if len(sentences) > 0 else script_english
    if len(sentences) > 2:
        body = ". ".join(sentences[1:-1]) + "."
        cta = f"{sentences[-1]}."
    elif len(sentences) == 2:
        body = f"{sentences[1]}."
        cta = "Whisper Amen, and send this covering to someone you love."
    else:
        body = script_english
        cta = "Whisper Amen, and send this to someone you love."

    hook_badge_text = theme.get("hook_badge_text", "PRAYER FOR YOUR HOME")
    micro_cta_text = theme.get("micro_cta_text", "💬 Leave their first name below")
    scripture = theme.get("scripture", "Psalm 91:11 — He will command his angels concerning you to guard you.")
    hashtags = theme.get("hashtags", ["#DailyPrayer", "#FaithInGod", "#ChristianFamily", "#Psalm91"])

    copy_seo = generate_seo_caption(chosen_key, script_english, scripture, cta, hashtags)
    pinned_comment = theme.get("pinned_comment", "What is the first name of the person you want us to pray for right now? Drop it below! 🙏")

    scene_1_prompt = theme.get("scene_1_prompt", generate_image_prompt_for_script(chosen_key, script_english))
    scene_2_prompt = theme.get("scene_2_prompt", generate_image_prompt_for_script(chosen_key, script_english))
    scene_3_prompt = theme.get("scene_3_prompt", generate_image_prompt_for_script(chosen_key, script_english))

    return {
        "theme": theme["title"],
        "theme_key": chosen_key,
        "target_time_slot": theme.get("target_time_slot", "morning"),
        "hook_badge_text": hook_badge_text,
        "micro_cta_text": micro_cta_text,
        "script_english": script_english,
        "hook": hook,
        "body": body,
        "cta": cta,
        "hook_text": hook_badge_text,
        "full_text": script_english,
        "scene_1_prompt": scene_1_prompt,
        "scene_2_prompt": scene_2_prompt,
        "scene_3_prompt": scene_3_prompt,
        "image_prompt": scene_1_prompt,
        "scripture": scripture,
        "pinned_comment": pinned_comment,
        "copy_seo": copy_seo,
        "seo_caption": copy_seo
    }


def generate_3scene_prompts_for_script(theme_key: Optional[str] = None, script_text: str = "", custom_topic: Optional[str] = None) -> Dict[str, str]:
    """
    Genera 3 prompts cinematográficos complementarios para el video:
    - Escena 1: Apertura / Gancho de impacto visual (0-3.2s)
    - Escena 2: Punto de inflexión / Intercesión / Oración ferviente (3.2s-10s)
    - Escena 3: Victoria / Paz / Promesa divina cumplida (10s al final)
    """
    if theme_key and theme_key in VIRAL_THEMES and not custom_topic:
        theme = VIRAL_THEMES[theme_key]
        p1 = theme.get("scene_1_prompt", "")
        p2 = theme.get("scene_2_prompt", "")
        p3 = theme.get("scene_3_prompt", "")
        if p1 and p2 and p3:
            return {"scene_1_prompt": p1, "scene_2_prompt": p2, "scene_3_prompt": p3}

    base_prompt = generate_image_prompt_for_script(theme_key, script_text, custom_topic)
    clean_base = re.sub(r'--ar\s+[0-9:]+', '', base_prompt).strip()

    p1 = f"{clean_base}, dramatic cinematic opening shot, emotional realism, volumetric God-rays --ar 9:16"
    p2 = f"Jesus Christ placing loving hands in prayer and intercession, warm sacred golden glow, intimate emotional realism --ar 9:16"
    p3 = f"Jesus Christ walking victorious in brilliant morning light, open welcoming arms, peace and divine glory, 8k --ar 9:16"

    return {"scene_1_prompt": p1, "scene_2_prompt": p2, "scene_3_prompt": p3}



def get_themes_list():
    return [{"key": k, "title": v["title"], "description": v["description"]} for k, v in VIRAL_THEMES.items()]
