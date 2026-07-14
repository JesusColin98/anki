import json
import os
from generate_books_part1 import save_deck

# ==================== 08_Tiny_Habits (20 cards) ====================
tiny_habits = [
    {
        "scenario": "Tiny Habits: Behavior Model 📈",
        "text": "The Fogg Behavior Model states that behavior occurs when three elements converge at the same moment: **B = MAP**, which stands for {{c1::Motivation}}, {{c2::Ability}}, and a {{c3::Prompt}}.",
        "explanation": "If any of these three elements is missing, the behavior will not occur. When a behavior fails, check which element was lacking.",
        "spanish": "El Modelo de Comportamiento de Fogg establece que el comportamiento ocurre cuando convergen tres elementos: Motivación, Habilidad y un Recordatorio (Prompt).",
        "tags": ["books_path", "habits", "fogg"]
    },
    {
        "scenario": "Tiny Habits: Prompt 📈",
        "text": "In the Fogg Behavior Model, the most important element for initiating action immediately is the {{c1::Prompt}} (recordatorio/desencadenante).",
        "explanation": "No behavior happens without a prompt. You can have high motivation and ability, but without a prompt, the action remains inactive.",
        "spanish": "En el Modelo de Comportamiento de Fogg, el elemento más importante para iniciar la acción es el Prompt (recordatorio/desencadenante).",
        "tags": ["books_path", "habits", "fogg"]
    },
    {
        "scenario": "Tiny Habits: Action Line 📈",
        "text": "The Fogg Behavior Grid shows that a behavior will occur if it falls above the {{c1::Action Line}}—meaning the combination of motivation and ability is high enough when the prompt fires.",
        "explanation": "If a task requires high ability (it is very hard) and motivation is low, the prompt will fail because it lies below the Action Line.",
        "spanish": "La cuadrícula de Fogg muestra que un comportamiento ocurrirá si cae por encima de la Línea de Acción.",
        "tags": ["books_path", "habits", "fogg"]
    },
    {
        "scenario": "Tiny Habits: Ability Factor 📈",
        "text": "BJ Fogg argues that the easiest way to make a behavior more likely to occur is to focus on increasing {{c1::Ability}} by making the behavior simpler.",
        "explanation": "Motivation is volatile and unreliable. Simplicity is reliable. If you make the behavior tiny (e.g. floss one tooth), it requires almost zero motivation.",
        "spanish": "BJ Fogg sostiene que la forma más fácil de hacer que ocurra un comportamiento es aumentar la Habilidad (Ability) haciéndolo más simple.",
        "tags": ["books_path", "habits", "fogg"]
    },
    {
        "scenario": "Tiny Habits: Anchor Prompts 📈",
        "text": "An {{c1::Anchor Prompt}} is an existing, solid routine in your daily life (like brushing your teeth or pouring coffee) that you use to trigger your new tiny habit.",
        "explanation": "Instead of relying on digital alarms, anchor your new habit to a behavior you already perform automatically.",
        "usage": "Anchor recipe: 'After I pour my morning coffee (Anchor), I will write down my 3 daily goals (New Tiny Habit).'",
        "spanish": "Un Recordatorio Ancla (Anchor Prompt) es una rutina sólida existente en tu vida que utilizas para activar tu nuevo hábito.",
        "tags": ["books_path", "habits", "recipes"]
    },
    {
        "scenario": "Tiny Habits: Tiny Recipe 📈",
        "text": "A tiny habit recipe follows the formula: 'After I [Anchor], I will [{{c1::Tiny Behavior}}]'.",
        "explanation": "Keep the behavior tiny. It should take less than 30 seconds and require minimal effort.",
        "usage": "Example: 'After I close my bedroom door, I will do 2 push-ups.'",
        "spanish": "Una receta de hábitos diminutos sigue la fórmula: 'Después de [Ancla], haré [Comportamiento Diminuto]'.",
        "tags": ["books_path", "habits", "recipes"]
    },
    {
        "scenario": "Tiny Habits: Celebration 📈",
        "text": "To wire a new habit into your brain, you must perform an immediate {{c1::celebration}} right after completing the tiny behavior, which releases dopamine.",
        "explanation": "Habits are formed by emotions, not by repetition. Feeling successful immediately after the action signals the brain to encode the routine.",
        "usage": "Right after doing 2 pushups, give a fist pump and say 'Awesome!' or smile broadly.",
        "spanish": "Para fijar un nuevo hábito en tu cerebro, debes realizar una celebración inmediata justo después de completar el comportamiento.",
        "tags": ["books_path", "habits", "neuroscience"]
    },
    {
        "scenario": "Tiny Habits: Ability Factors 📈",
        "text": "BJ Fogg identifies 5 factors that affect Ability (the Simplicity Factors): {{c1::Time}}, {{c2::Money}}, {{c3::Physical Effort}}, {{c4::Brain Cycles}}, and {{c5::Social Deviance}}.",
        "explanation": "If a behavior requires too much of any of these factors, it is hard and less likely to happen.",
        "spanish": "BJ Fogg identifica 5 factores de simplicidad que afectan la Habilidad: Tiempo, Dinero, Esfuerzo Físico, Ciclos Mentales y Desviación Social.",
        "tags": ["books_path", "habits", "fogg"]
    },
    {
        "scenario": "Tiny Habits: Golden Behaviors 📈",
        "text": "A {{c1::Golden Behavior}} is an action that is highly effective at achieving your goal, you have the ability to do, and you are naturally motivated to do.",
        "explanation": "Do not force yourself to do behaviors you hate. Find the intersection of impact, ability, and motivation.",
        "spanish": "Un Comportamiento Dorado (Golden Behavior) es una acción efectiva, que tienes la capacidad de hacer y que quieres hacer.",
        "tags": ["books_path", "habits", "decision_making"]
    },
    {
        "scenario": "Tiny Habits: Grow Habits 📈",
        "text": "To grow a habit, start by planting a seed—a tiny version of the habit. As the routine becomes automatic, the habit will {{c1::naturally expand}} to its full size.",
        "explanation": "Once flossing one tooth is automatic, you will naturally start flossing all of them because the friction of starting is gone.",
        "spanish": "Para cultivar un hábito, comienza plantando una semilla (una versión diminuta). El hábito se expandirá naturalmente.",
        "tags": ["books_path", "habits", "growth"]
    },
    {
        "scenario": "Tiny Habits: Pearl Habits 📈",
        "text": "A {{c1::Pearl Habit}} is a routine where you take an annoying, unavoidable cue (like a crying baby, a noisy neighbor, or traffic) and use it as a prompt for a positive behavior.",
        "explanation": "Named after pearls, which are formed around irritating grains of sand. Transforms friction into growth.",
        "usage": "Cue: Siren outside. Routine: Take one deep breath and relax shoulders.",
        "spanish": "Un Hábito Perla (Pearl Habit) es una rutina en la que tomas una señal molesta e inevitable y la usas como recordatorio positivo.",
        "tags": ["books_path", "habits", "recipes"]
    },
    {
        "scenario": "Tiny Habits: Motivation Wave 📈",
        "text": "The {{c1::Motivation Wave}} refers to temporary surges of high motivation that allow you to do hard, one-time behaviors (like buying gym equipment or scheduling a doctor's checkup).",
        "explanation": "Do not build daily habits that rely on the peak of the wave. Use the wave only to build systems and make future habits easier.",
        "spanish": "La Ola de Motivación se refiere a oleadas temporales de alta motivación que te permiten realizar conductas difíciles de una sola vez.",
        "tags": ["books_path", "habits", "fogg"]
    },
    {
        "scenario": "Tiny Habits: Untangling Habits 📈",
        "text": "To stop a bad habit, focus on {{c1::removing the prompt}} rather than trying to resist the behavior with willpower.",
        "explanation": "If you don't receive the trigger, the routine never starts, preserving your willpower.",
        "usage": "If you check your phone too much at work, put the phone in another room (removing the prompt).",
        "spanish": "Para detener un mal hábito, enfócate en eliminar el recordatorio (prompt) en lugar de resistirte con fuerza de voluntad.",
        "tags": ["books_path", "habits", "breaking_habits"]
    },
    {
        "scenario": "Tiny Habits: Celebration Speed 📈",
        "text": "For a celebration to trigger dopamine release and form a habit, it must occur within {{c1::two seconds}} of the behavior.",
        "explanation": "Delaying the celebration breaks the associative learning loop in the brain.",
        "spanish": "Para que una celebración active la dopamina, debe ocurrir dentro de los dos segundos posteriores al comportamiento.",
        "tags": ["books_path", "habits", "neuroscience"]
    },
    {
        "scenario": "Tiny Habits: Super-Bundle 📈",
        "text": "Bundling a new tiny habit with an anchor and an immediate celebration is called creating a {{c1::habit recipe}}.",
        "explanation": "Simple formula for designing behavioral change.",
        "spanish": "Agrupar un nuevo hábito diminuto con un ancla y una celebración inmediata se llama crear una receta de hábitos.",
        "tags": ["books_path", "habits", "recipes"]
    },
    {
        "scenario": "Tiny Habits: Identity Shift 📈",
        "text": "The ultimate goal of Tiny Habits is not just behavior change, but an {{c1::identity shift}}—viewing yourself as the type of person who easily executes these behaviors.",
        "explanation": "Small wins build self-efficacy, which alters your self-image. Once you believe 'I am a healthy person', healthy choices become effortless.",
        "spanish": "El objetivo final de Tiny Habits es un cambio de identidad: verte a ti mismo como el tipo de persona que realiza estas acciones.",
        "tags": ["books_path", "habits", "identity"]
    },
    {
        "scenario": "Tiny Habits: Designing the Prompt 📈",
        "text": "BJ Fogg identifies 3 types of prompts: **Person prompts** (internal urges), **Context prompts** (alarms/notes), and **Action prompts** (existing routines). {{c1::Action prompts}} are the most effective for habit building.",
        "explanation": "Person prompts fail because memory is unreliable. Context prompts fail because they cause alarm fatigue. Action prompts capitalize on existing brain wiring.",
        "spanish": "Fogg identifica 3 tipos de recordatorios: Personales, de Contexto y de Acción. Los de Acción son los más efectivos.",
        "tags": ["books_path", "habits", "fogg"]
    },
    {
        "scenario": "Tiny Habits: The Swarm of Behaviors 📈",
        "text": "To solve a broad goal (like 'reduce stress'), generate a {{c1::swarm of behaviors}} (a list of 20-30 specific, actionable habits) and select the easiest golden behaviors.",
        "explanation": "Broad goals are not actionable. Breaking them down into a swarm of micro-actions lets you pick the path of least resistance.",
        "spanish": "Para resolver un objetivo amplio, genera un enjambre de comportamientos (una lista de 20-30 hábitos específicos) y elige el más fácil.",
        "tags": ["books_path", "habits", "fogg"]
    },
    {
        "scenario": "Tiny Habits: Celebrating Failures 📈",
        "text": "If you forget to do a tiny habit, do not criticize yourself. Instead, adjust the recipe, make it {{c1::even smaller}}, or find a better anchor.",
        "explanation": "Self-criticism activates the threat brain, reducing motivation. Iteration and optimization are the keys to habit success.",
        "spanish": "Si olvidas realizar un hábito diminuto, no te critiques. Ajusta la receta o hazla aún más pequeña.",
        "tags": ["books_path", "habits", "growth"]
    },
    {
        "scenario": "Tiny Habits: Shine 📈",
        "text": "BJ Fogg uses the word {{c1::Shine}} to describe the positive emotional feeling of success and self-efficacy that forms habits.",
        "explanation": "The feeling of 'Shine' acts as a chemical stamp, telling the brain to remember the preceding routine.",
        "spanish": "BJ Fogg usa la palabra 'Shine' (brillo) para describir la sensación emocional positiva de éxito que forma los hábitos.",
        "tags": ["books_path", "habits", "neuroscience"]
    }
]

# ==================== 09_Ultralearning (20 cards) ====================
ultralearning = [
    {
        "scenario": "Ultralearning: Definition 🚀",
        "text": "Scott Young defines {{c1::Ultralearning}} as a strategy for aggressive, self-directed learning of complex skills to achieve high competence in minimal time.",
        "explanation": "It is self-directed (you decide what and how to learn) and aggressive (focused, intensive effort instead of passive, slow study).",
        "spanish": "Scott Young define el Ultralearning como una estrategia para el aprendizaje agresivo y autodirigido de habilidades complejas.",
        "tags": ["books_path", "ultralearning", "learning"]
    },
    {
        "scenario": "Ultralearning: Principle 1 - Metalearning 🚀",
        "text": "The first principle of Ultralearning is {{c1::Metalearning}}—learning how the subject or skill is structured before you start studying.",
        "explanation": "Spend 10% of your total study time researching the field. Map out the concepts, facts, and procedures needed for mastery.",
        "usage": "Before learning a new framework, research which concepts are foundational and what projects are best for practice.",
        "spanish": "El primer principio de Ultralearning es el Meta-aprendizaje: aprender cómo está estructurado el tema antes de estudiar.",
        "tags": ["books_path", "ultralearning", "metalearning"]
    },
    {
        "scenario": "Ultralearning: Principle 2 - Focus 🚀",
        "text": "The second principle is {{c1::Focus}}—carving out dedicated chunks of time to concentrate deeply, avoiding distraction and task-switching.",
        "explanation": "Focus requires defeating procrastination, finding flow, and sustaining attention on cognitive difficulties.",
        "spanish": "El segundo principio es el Enfoque: reservar bloques de tiempo dedicados a concentrarse profundamente.",
        "tags": ["books_path", "focus", "ultralearning"]
    },
    {
        "scenario": "Ultralearning: Principle 3 - Directness 🚀",
        "text": "The third principle is {{c1::Directness}}—learning by doing the actual thing you want to be good at, rather than using transfer applications or theoretical substitutes.",
        "explanation": "If you want to speak a language, speak it immediately. If you want to code, build projects immediately. Theoretical study has very low transfer.",
        "usage": "Build a real web app instead of just watching 50 hours of programming tutorials.",
        "spanish": "El tercer principio es la Directividad: aprender haciendo la actividad real en la que deseas destacar.",
        "tags": ["books_path", "ultralearning", "directness"]
    },
    {
        "scenario": "Ultralearning: Principle 4 - Drill 🚀",
        "text": "The fourth principle is {{c1::Drill}}—isolating your weakest sub-skills, practicing them intensively until they improve, and reintegrating them into the main skill.",
        "explanation": "Identify the bottleneck. If you struggle with CSS layout, spend 3 days doing only CSS drills, then return to full web design.",
        "spanish": "El cuarto principio es el Entrenamiento (Drill): aislar tus subhabilidades más débiles y practicarlas intensamente.",
        "tags": ["books_path", "ultralearning", "drills"]
    },
    {
        "scenario": "Ultralearning: Principle 5 - Retrieval 🚀",
        "text": "The fifth principle is {{c1::Retrieval}}—testing yourself constantly to recall information from memory, which builds stronger neural connections.",
        "explanation": "Active retrieval outperforms review. Use practice tests, write notes from memory, or use flashcards.",
        "spanish": "El quinto principio es la Recuperación: evaluarte a ti mismo constantemente para recordar información de la memoria.",
        "tags": ["books_path", "ultralearning", "retrieval"]
    },
    {
        "scenario": "Ultralearning: Principle 6 - Feedback 🚀",
        "text": "The sixth principle is {{c1::Feedback}}—seeking immediate, objective, and sometimes harsh feedback to correct errors and calibrate performance.",
        "explanation": "Distinguish between outcome feedback (knowing if you failed) and informational feedback (knowing why you failed).",
        "spanish": "El sexto principio es la Retroalimentación (Feedback): buscar retroalimentación inmediata y objetiva.",
        "tags": ["books_path", "ultralearning", "feedback"]
    },
    {
        "scenario": "Ultralearning: Principle 7 - Retention 🚀",
        "text": "The seventh principle is {{c1::Retention}}—understanding why we forget (decay, interference) and building systems to prevent it.",
        "explanation": "Use spaced repetition, active recall, or overlearning to maintain high retention over time.",
        "spanish": "El séptimo principio es la Retención: entender por qué olvidamos y construir sistemas para prevenirlo.",
        "tags": ["books_path", "ultralearning", "retention"]
    },
    {
        "scenario": "Ultralearning: Principle 8 - Intuition 🚀",
        "text": "The eighth principle is {{c1::Intuition}}—developing a deep, structural understanding of concepts by exploring them thoroughly, rather than memorizing surface facts.",
        "explanation": "Ask 'why' things work. Use the Feynman technique (explaining the concept to a child) to expose gaps in your intuition.",
        "spanish": "El octavo principio es la Intuición: desarrollar una comprensión profunda e intuitiva de los conceptos.",
        "tags": ["books_path", "ultralearning", "intuition"]
    },
    {
        "scenario": "Ultralearning: Principle 9 - Experimentation 🚀",
        "text": "The ninth principle is {{c1::Experimentation}}—exploring different materials, methods, and styles to find the best way to apply your skills once you reach a plateau.",
        "explanation": "As you reach intermediate levels, copying others is not enough. You must experiment to find your own unique style and solutions.",
        "spanish": "El noveno principio es la Experimentación: explorar diferentes métodos y estilos para superar mesetas.",
        "tags": ["books_path", "ultralearning", "experimentation"]
    },
    {
        "scenario": "Ultralearning: Overlearning 🚀",
        "text": "To achieve automaticity under stress, you must practice {{c1::overlearning}}—continuing to practice key procedures beyond initial mastery.",
        "explanation": "Builds robust muscle memory or automatic cognitive responses that don't drain working memory slots under pressure.",
        "spanish": "Para lograr la automaticidad bajo estrés, debes practicar el sobreaprendizaje.",
        "tags": ["books_path", "ultralearning", "overlearning"]
    },
    {
        "scenario": "Ultralearning: Feynman Technique 🚀",
        "text": "The {{c1::Feynman Technique}} is a method where you write down an explanation of a concept as if you were teaching it to a complete beginner or a child.",
        "explanation": "Forces you to simplify vocabulary and avoid jargon. If you get stuck or use complex words, it highlights a gap in your own understanding.",
        "usage": "Write a 1-paragraph explanation of 'recursion' without using the word 'stack' or 'function call'.",
        "spanish": "La Técnica Feynman es un método donde escribes una explicación de un concepto como si se lo enseñaras a un niño.",
        "tags": ["books_path", "ultralearning", "feynman"]
    },
    {
        "scenario": "Ultralearning: Transfer 🚀",
        "text": "In education, {{c1::transfer}} is the ability to apply a skill learned in one context to a completely different context. It is notoriously difficult to achieve naturally.",
        "explanation": "Most learning is highly context-dependent. Directness is the only reliable way to ensure transfer.",
        "spanish": "En la educación, la transferencia es la capacidad de aplicar una habilidad aprendida en un contexto a otro diferente.",
        "tags": ["books_path", "ultralearning", "transfer"]
    },
    {
        "scenario": "Ultralearning: Metalearning Map 🚀",
        "text": "When mapping a subject during Metalearning, split the content into three categories: {{c1::Concepts}} (what needs to be understood), {{c2::Facts}} (what needs to be memorized), and {{c3::Procedures}} (what needs to be practiced).",
        "explanation": "Allows you to select the correct learning tool for each category (e.g. Feynman for concepts, Anki for facts, drills for procedures).",
        "spanish": "Al mapear un tema, divide el contenido en tres categorías: Conceptos, Hechos y Procedimientos.",
        "tags": ["books_path", "ultralearning", "metalearning"]
    },
    {
        "scenario": "Ultralearning: The Rule of 10% 🚀",
        "text": "Spend {{c1::10%}} of your total planned project time on Metalearning and planning before you write or study a single card.",
        "explanation": "If your project is 100 hours, spend 10 hours researching resources, mapping the curriculum, and structuring drills.",
        "spanish": "Dedica el 10% del tiempo total planificado del proyecto al meta-aprendizaje antes de empezar a estudiar.",
        "tags": ["books_path", "ultralearning", "planning"]
    },
    {
        "scenario": "Ultralearning: Informational Feedback 🚀",
        "text": "When seeking feedback, focus on {{c1::informational feedback}}—which tells you exactly *what* went wrong and *how* to correct it.",
        "explanation": "Outcome feedback (knowing you got a C on an exam) is not actionable. Informational feedback (knowing you missed a step in the algorithm) guides corrections.",
        "spanish": "Al buscar retroalimentación, enfócate en la retroalimentación informativa, que te dice exactamente qué salió mal.",
        "tags": ["books_path", "ultralearning", "feedback"]
    },
    {
        "scenario": "Ultralearning: Memory Decay 🚀",
        "text": "To prevent memory decay, schedule regular {{c1::refresh sessions}} or integrate the skill into your daily job routines.",
        "explanation": "Use-it-or-lose-it is a biological reality in brain wiring. Spaced repetition maintains the connection.",
        "spanish": "Para prevenir el deterioro de la memoria, programa sesiones de actualización regulares.",
        "tags": ["books_path", "ultralearning", "retention"]
    },
    {
        "scenario": "Ultralearning: Deliberate Difficulty 🚀",
        "text": "Ultralearners seek out {{c1::deliberate difficulty}} by choosing active practice over passive study, even though it feels harder and slower.",
        "explanation": "Because active recall and generation feel difficult, they produce far more durable memory traces.",
        "spanish": "Los ultralearners buscan la dificultad deliberada al elegir la práctica activa sobre el estudio pasivo.",
        "tags": ["books_path", "ultralearning", "recall"]
    },
    {
        "scenario": "Ultralearning: Self-Directed learning 🚀",
        "text": "The core advantage of self-directed learning is that you can {{c1::customize the curriculum}} to fit your specific goals, rather than following a rigid school textbook.",
        "explanation": "You don't waste time on irrelevant side topics, maximizing learning efficiency.",
        "spanish": "La ventaja principal del aprendizaje autodirigido es que puedes personalizar el plan de estudios según tus metas.",
        "tags": ["books_path", "ultralearning", "self_directed"]
    },
    {
        "scenario": "Ultralearning: Drill Strategy 🚀",
        "text": "To execute a drill, use the **Direct-Drill-Direct** loop: practice the direct skill, identify a bottleneck, {{c1::drill the bottleneck isolated}}, and return to direct practice.",
        "explanation": "Keeps drills relevant and ensures they successfully transfer back into the main skill.",
        "spanish": "Para realizar un drill, usa el bucle Direct-Drill-Direct: practica la habilidad, aísla el cuello de botella, entrénalo y regresa.",
        "tags": ["books_path", "ultralearning", "drills"]
    }
]

save_deck("Productivity", "08_Tiny_Habits", tiny_habits)
save_deck("Productivity", "09_Ultralearning", ultralearning)
