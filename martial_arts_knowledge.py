"""
Martial Arts Coaching Manual Knowledge Base
This file contains detailed instructional documents for the AI Martial Arts Coach's vector database.
"""

KNOWLEDGE_DOCUMENTS = [
    # 1. Muay Thai Fundamentals
    (
        "MUAY THAI FUNDAMENTALS: THE ART OF EIGHT LIMBS\n"
        "The foundation of Muay Thai begins with the stance. Unlike boxing, a Muay Thai stance is more squared up to the opponent, "
        "allowing for rapid checking of kicks and efficient use of all eight weapons: fists, elbows, knees, and shins. "
        "Your weight should be distributed roughly 60/40 on the back leg, with the lead foot light and ready to 'teep' or check. "
        "The guard is high, with palms facing outward to catch kicks and parry punches. The jab and cross remain essential, "
        "but in Muay Thai, they often serve to set up the more powerful roundhouse kick or clinch entry. "
        "The roundhouse kick is delivered with the lower part of the shin, not the foot. It requires a full hip rotation, "
        "stepping off the center line and swinging the leg like a baseball bat. Elbow strikes are short-range weapons, "
        "often used in the clinch or as a counter to a lunging opponent. Knee strikes can be delivered from long range (spear knees) "
        "or within the clinch (circle knees). Clinch work is a distinct phase of Muay Thai, involving a 'plum' or double-collar tie "
        "to control the opponent's posture and deliver devastating knees while neutralizing their striking options. "
        "Proper guard positioning is dynamic; you must be ready to transition from a long guard to a high guard as the range closes."
    ),
    
    # 2. Boxing Fundamentals
    (
        "BOXING FUNDAMENTALS: PRECISION AND FOOTWORK\n"
        "In the 'Sweet Science,' everything starts from the feet. A proper boxing stance is narrower than Muay Thai, "
        "providing a smaller target and enabling explosive lateral movement. The lead foot points towards the opponent, "
        "while the rear foot is at a 45-degree angle. Footwork is the engine: you move by stepping with the foot closest "
        "to the direction of travel, never crossing your legs. The jab is the most important punch, used to find range, "
        "distract, and set up the power of the cross. The hook and uppercut add variety and can bypass a tight guard. "
        "Defensive maneuvers like the slip, roll, and parry are critical. Slipping involves moving the head just off the "
        "line of a punch, while rolling allows you to duck under hooks and counter with hooks of your own. "
        "Parrying uses the palms to redirect straight shots. Effective combinations, such as the classic 1-2 (jab-cross) "
        "or the 1-2-3 (jab-cross-hook), must be practiced until they are fluid and instinctive. "
        "Defense is not passive; every defensive move should be an opportunity to launch a counter-attack. "
        "Maintaining a high, tight guard with the chin tucked behind the shoulder is non-negotiable for safety."
    ),
    
    # 3. Kickboxing Fundamentals
    (
        "KICKBOXING FUNDAMENTALS: BLENDING THE STYLES\n"
        "Kickboxing is the seamless integration of Western boxing and powerful kicking techniques. "
        "The primary challenge is the transition: throwing a punch and immediately following with a kick, or vice versa. "
        "A common combination is the 'low kick finish,' where a punch combination forces the opponent's guard up, "
        "opening their legs for a devastating roundhouse to the thigh. Switch kicks are essential for changing the angle "
        "and catching an opponent off guard. By quickly switching your feet, you can launch a powerful lead-leg kick "
        "without a telltale step. Body kicks are used to drain an opponent's energy and damage the ribs. "
        "Spinning techniques, such as the spinning backfist or spinning back kick, are high-risk but high-reward, "
        "requiring precise timing and spatial awareness. The stance in kickboxing is a hybrid—slightly more bladed "
        "than Muay Thai for better punch reach, but squared enough to check kicks. Managing the distance is key; "
        "you must be comfortable at punching range, kicking range, and the transition zone between them. "
        "Practicing 'blind' kicks—kicking while the opponent's vision is obscured by your punches—is a hallmark "
        "of high-level kickboxing strategy."
    ),
    
    # 4. Training Programming
    (
        "TRAINING PROGRAMMING: BUILDING THE COMBAT ATHLETE\n"
        "Effective training requires a balance of skill work, conditioning, and recovery, often organized through periodization. "
        "Periodization involves dividing the training year into cycles (macro, meso, and micro) to ensure peak performance "
        "for a specific date while avoiding burnout. For a beginner, the focus should be 80% technique and 20% light conditioning. "
        "A typical beginner week might include three sessions of fundamental classes, emphasizing shadow boxing and heavy bag drills. "
        "Intermediate students should incorporate controlled sparring and more intense pad work, training 4-5 times per week. "
        "Advanced athletes follow a rigorous schedule: morning runs for aerobic base, afternoon technical sessions, "
        "and evening sparring or strength and conditioning. Sparring should be conducted with clear guidelines—70% technical "
        "sparring (light touch) and only occasional hard sparring to prepare for competition. Bag work is for power and endurance, "
        "while pad work with a coach develops timing, accuracy, and fight-specific reactions. Shadow boxing is the most "
        "underrated tool, allowing the athlete to visualize opponents and refine form without external pressure. "
        "Rest days are as important as training days; the body adapts and grows stronger during periods of inactivity."
    ),
    
    # 5. Fighter Nutrition
    (
        "FIGHTER NUTRITION: FUELING THE GRIND\n"
        "Nutrition for combat sports is about maximizing performance and recovery while managing weight. "
        "Pre-training meals should be consumed 2-3 hours before a session, focusing on complex carbohydrates (like oats or brown rice) "
        "and moderate protein to provide sustained energy without digestive distress. A small, fast-digesting carb snack "
        "(like a banana) can be taken 30 minutes before training. Post-training nutrition is critical for muscle repair and glycogen replenishment. "
        "A 2:1 ratio of carbohydrates to protein is ideal within the first hour after training. Hydration is a constant process; "
        "fighters should aim for at least 3-4 liters of water daily, increasing intake during heavy training sessions to replace lost electrolytes. "
        "Weight cutting should be handled professionally, focusing on a gradual 'fat loss' phase followed by a short, "
        "monitored 'water load' and 'water cut' near the fight date. Avoid highly processed sugars, excessive caffeine, "
        "and fried foods, which cause inflammation and energy crashes. Meal timing should be consistent to stabilize blood sugar levels. "
        "Recovery foods like tart cherry juice for inflammation and high-quality proteins like eggs, chicken, and fish "
        "should be staples in every fighter's diet. Sleep is the ultimate supplement; aim for 8-9 hours during hard training camps."
    ),
    
    # 6. Injury Prevention and Common Injuries
    (
        "INJURY PREVENTION: THE CONSERVATIVE PATH TO LONGEVITY\n"
        "Longevity in striking sports depends on proactive injury prevention. It starts with proper equipment: "
        "never strike a bag without hand wraps. Hand wrapping supports the small bones of the hand and stabilizes the wrist. "
        "A thorough warm-up routine—including dynamic stretching and light shadow boxing—is essential to prepare the joints "
        "and muscles for high-impact activity. Common injuries include knuckle bruising, wrist sprains from poor punch technique, "
        "and shin splints or hematomas from checking kicks. If an injury occurs, follow the RICE method: Rest, Ice, Compression, "
        "and Elevation for the first 48-72 hours. Overtraining is a significant risk; signs include persistent fatigue, "
        "decreased performance, irritability, and frequent minor illnesses. Listen to your body; 'training through the pain' "
        "often leads to chronic issues. Know when to rest—a missed week is better than a missed year due to surgery. "
        "Conditioning the shins is a slow process of heavy bag work and pad work; never use hard objects to 'deaden' the nerves. "
        "Proactive recovery, such as foam rolling, massage, and mobility work, should be integrated into your weekly routine "
        "to maintain tissue health and range of motion."
    ),
    
    # 7. Mental Game and Mindset
    (
        "MENTAL GAME: THE WARRIOR'S MINDSET\n"
        "The greatest battle in martial arts is fought within the mind. Bruce Lee's philosophy of 'being like water'—adaptable, "
        "fluid, and capable of both crashing and flowing—is the pinnacle of combat mindset. Dealing with fear is not about "
        "eliminating it, but about acknowledging it and acting anyway. Fear is a natural response to the stress of combat; "
        "breathwork and visualization can help manage the physiological arousal. Consistency is far more valuable than motivation. "
        "Motivation is a feeling that fades, while consistency is a habit that builds champions. "
        "Ego is the enemy in the gym; a student who is afraid to look bad will never learn. You must be willing to fail, "
        "be swept, and be outclassed in training to identify and fix your weaknesses. Visualization involves mentally "
        "rehearsing techniques and fight scenarios, which has been shown to improve actual performance by strengthening "
        "neural pathways. Stay grounded in the present moment—if you are thinking about the last round or the next one, "
        "you are not in the current one. The path of mastery is a lifelong journey, requiring humility, patience, "
        "and an unwavering commitment to self-improvement both inside and outside the gym."
    )
]
