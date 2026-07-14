import json
import os
from generate_books_part1 import save_deck

# ==================== 05_Essentialism (20 cards) ====================
essentialism = [
    {
        "scenario": "Essentialism: The Core Mindset 🎯",
        "text": "The core mindset of an Essentialist is: '{{c1::Less but better}}' (discern the vital few from the trivial many).",
        "explanation": "Essentialism is not about how to get more things done; it's about how to get the right things done. It is a systematic discipline for cataloging and eliminating non-essentials.",
        "usage": "Instead of asking 'How can I fit all these meetings in?', ask 'Which of these meetings is truly vital?'",
        "spanish": "La mentalidad central de un Esencialista es: 'Menos pero mejor' (discernir los pocos vitales de los muchos triviales).",
        "tags": ["books_path", "essentialism", "productivity"]
    },
    {
        "scenario": "Essentialism: Choice 🎯",
        "text": "Essentialists view choice as an {{c1::active action}}, not a passive thing. While you may not control your options, you always control how you choose.",
        "explanation": "When we surrender our ability to choose, we give others permission to choose for us.",
        "spanish": "Los esencialistas ven la elección como una acción activa, no como algo pasivo. Aunque no controles tus opciones, controlas cómo eliges.",
        "tags": ["books_path", "essentialism", "philosophy"]
    },
    {
        "scenario": "Essentialism: Trade-offs 🎯",
        "text": "Instead of asking 'How can I do both?', the Essentialist asks: '{{c1::Which problem do I want to solve?}}', embracing trade-offs as an inherent part of life.",
        "explanation": "We cannot have it all. Making a trade-off is a strategic decision to prioritize one thing over another.",
        "spanish": "En lugar de preguntar '¿Cómo puedo hacer ambas cosas?', el esencialista pregunta: '¿Qué problema quiero resolver?'.",
        "tags": ["books_path", "essentialism", "strategy"]
    },
    {
        "scenario": "Essentialism: Escape 🎯",
        "text": "To discern what is vital, you must design space to {{c1::escape}}—creating uninterrupted time to think, focus, and reflect.",
        "explanation": "If you don't create space to think, the noise of the world will dictate your focus. We need space to look at the big picture.",
        "usage": "Block 1 hour of 'thinking time' on your calendar every day, with no meetings or slack notifications.",
        "spanish": "Para discernir lo que es vital, debes diseñar un espacio para escapar: crear tiempo ininterrumpido para pensar.",
        "tags": ["books_path", "essentialism", "focus"]
    },
    {
        "scenario": "Essentialism: Sleep 🎯",
        "text": "Essentialists protect their assets by protecting their {{c1::sleep}}, viewing it as a prerequisite for high performance rather than a waste of time.",
        "explanation": "One hour of sleep yields multiple hours of high-productivity and clear decision-making capacity during the day.",
        "spanish": "Los esencialistas protegen sus activos protegiendo su sueño, viéndolo como un prerrequisito para el alto rendimiento.",
        "tags": ["books_path", "essentialism", "health"]
    },
    {
        "scenario": "Essentialism: Selection 🎯",
        "text": "The rule of selection in Essentialism states: 'If it isn't a {{c1::clear yes}}, then it's a {{c2::clear no}}'.",
        "explanation": "If you are evaluating an opportunity and feel only moderately excited (e.g. 70/100), reject it. Only accept opportunities that are 90+ score.",
        "spanish": "La regla de selección en el Esencialismo establece: 'Si no es un sí claro, entonces es un no claro'.",
        "tags": ["books_path", "essentialism", "decision_making"]
    },
    {
        "scenario": "Essentialism: Clarify 🎯",
        "text": "Instead of broad mission statements, organizations need an {{c1::essential intent}}—a concrete, inspirational, and measurable goal.",
        "explanation": "An essential intent is both concrete and inspirational. It guides all micro-decisions. Example: 'Get internet access to 100 million rural households by 2028.'",
        "spanish": "En lugar de declaraciones de misión amplias, las organizaciones necesitan una intención esencial: una meta concreta y medible.",
        "tags": ["books_path", "essentialism", "strategy"]
    },
    {
        "scenario": "Essentialism: Dare 🎯",
        "text": "To protect your time, you must learn to say 'No' with {{c1::respect and courage}}, decoupling the refusal from the relationship.",
        "explanation": "People respect those who set clear boundaries. Saying 'No' to a request is saying 'Yes' to your priorities.",
        "usage": "If a manager asks for a task that isn't essential, list your active projects and ask which one should be delayed.",
        "spanish": "Para proteger tu tiempo, debes aprender a decir 'No' con respeto y coraje, separando el rechazo de la relación.",
        "tags": ["books_path", "essentialism", "communication"]
    },
    {
        "scenario": "Essentialism: Uncommit 🎯",
        "text": "To stop throwing good money/time after bad, you must overcome the {{c1::sunk-cost fallacy}}—the bias that makes you continue a failing project because you've already invested in it.",
        "explanation": "Admit mistakes and cut losses immediately. Ask: 'If I wasn't already invested in this project, would I start it today?'",
        "spanish": "Para dejar de desperdiciar tiempo, debes superar la falacia del costo hundido: continuar un proyecto fallido por lo ya invertido.",
        "tags": ["books_path", "essentialism", "psychology"]
    },
    {
        "scenario": "Essentialism: Edit 🎯",
        "text": "A good editor adds value by {{c1::eliminating non-essentials}}, clarifying meaning, and focusing the reader's attention.",
        "explanation": "Editing is not just pruning; it is an active design process to maximize impact by removing distractions.",
        "usage": "Regularly audit your project list, meetings, and codebase to remove legacy clutter.",
        "spanish": "Un buen editor agrega valor al eliminar lo no esencial, aclarando el significado y enfocando la atención.",
        "tags": ["books_path", "essentialism", "refactoring"]
    },
    {
        "scenario": "Essentialism: Limit 🎯",
        "text": "Setting clear {{c1::boundaries}} actually increases your freedom by protecting you from the agendas of others.",
        "explanation": "If you don't set boundaries, you will become a tool for other people's goals. Boundaries keep you focused on your essential intent.",
        "spanish": "Establecer límites claros en realidad aumenta tu libertad al protegerte de las agendas de los demás.",
        "tags": ["books_path", "essentialism", "boundaries"]
    },
    {
        "scenario": "Essentialism: Buffer 🎯",
        "text": "To handle the unexpected, Essentialists design a {{c1::buffer}}—adding 50% extra time or resources to project estimates.",
        "explanation": "The planning fallacy makes us assume things will go perfectly. A buffer protects us from stress and delays.",
        "usage": "If a feature estimate is 10 days, report it as 15 days to build in a buffer for bugs and deployment issues.",
        "spanish": "Para manejar lo inesperado, los Esencialistas diseñan un colchón (buffer): agregar un 50% de tiempo adicional.",
        "tags": ["books_path", "essentialism", "planning"]
    },
    {
        "scenario": "Essentialism: Subtract 🎯",
        "text": "To increase output, focus on {{c1::removing bottlenecks}} and constraints rather than trying to force more resources into the system.",
        "explanation": "Identify the slowest link in the process (the constraint). Removing it yields immediate, systemic progress.",
        "usage": "In coding, identify the slowest database query that blocks the API thread and optimize it first.",
        "spanish": "Para aumentar el rendimiento, enfócate en eliminar los cuellos de botella en lugar de forzar más recursos.",
        "tags": ["books_path", "essentialism", "optimization"]
    },
    {
        "scenario": "Essentialism: Progress 🎯",
        "text": "Essentialists focus on {{c1::small, incremental wins}} rather than big, heroic efforts, as small wins build unstoppable momentum.",
        "explanation": "A series of small, daily progresses creates a positive feedback loop that outperforms massive, erratic pushes.",
        "spanish": "Los esencialistas se enfocan en pequeñas victorias incrementales en lugar de esfuerzos grandes y heroicos.",
        "tags": ["books_path", "essentialism", "momentum"]
    },
    {
        "scenario": "Essentialism: Flow 🎯",
        "text": "To make execution effortless, design a {{c1::routine}} that makes the essential behaviors the default option.",
        "explanation": "Routines conserve mental energy by automating decisions. Once a routine is built, execution becomes automatic.",
        "usage": "Design a morning routine where your first 90 minutes are dedicated entirely to coding without check email.",
        "spanish": "Para que la ejecución sea sin esfuerzo, diseña una rutina que convierta los comportamientos esenciales en la opción predeterminada.",
        "tags": ["books_path", "essentialism", "routines"]
    },
    {
        "scenario": "Essentialism: Focus 🎯",
        "text": "To be truly present, you must ask yourself: '{{c1::What is important right now?}}' (WIN).",
        "explanation": "Do not let your mind get trapped in past mistakes or future worries. Focus on the single action you can take in the present moment.",
        "spanish": "Para estar verdaderamente presente, debes preguntarte: '¿Qué es importante en este momento?' (WIN).",
        "tags": ["books_path", "essentialism", "mindfulness"]
    },
    {
        "scenario": "Essentialism: Non-Essentialist Mindset 🎯",
        "text": "The Non-Essentialist believes: '{{c1::I have to do it all}}', leading to being stretched thin in a mile-wide, inch-deep layout.",
        "explanation": "Non-essentialists say yes to everything, get overwhelmed, and make only millimeter progress in a thousand directions.",
        "spanish": "El No Esencialista cree: 'Tengo que hacerlo todo', lo que lleva a estar disperso en muchas direcciones sin profundidad.",
        "tags": ["books_path", "essentialism", "psychology"]
    },
    {
        "scenario": "Essentialism: Play 🎯",
        "text": "Essentialists view {{c1::play}} as an essential catalyst for creativity, observation, and stress reduction, not as a waste of time.",
        "explanation": "Play opens the mind's diffuse mode, helping us see connections and solutions we missed during focused stress.",
        "spanish": "Los esencialistas ven el juego (play) como un catalizador esencial para la creatividad y la reducción del estrés.",
        "tags": ["books_path", "essentialism", "creativity"]
    },
    {
        "scenario": "Essentialism: The Closet Metaphor 🎯",
        "text": "The book compares organizing your life to {{c1::cleaning a closet}}: you must actively select what to keep, discard the rest, and audit regularly.",
        "explanation": "If you don't actively clean your closet, it fills up with clothes you don't wear. Life fills up with non-essential commitments similarly.",
        "spanish": "El libro compara organizar tu vida con limpiar un armario: debes seleccionar activamente qué conservar y descartar el resto.",
        "tags": ["books_path", "essentialism", "metaphor"]
    },
    {
        "scenario": "Essentialism: Joy of Missing Out 🎯",
        "text": "Instead of FOMO (Fear of Missing Out), Essentialists embrace {{c1::JOMO}} (Joy of Missing Out)—celebrating the choice to reject the trivial.",
        "explanation": "Knowing that you rejected a distraction to focus on a vital priority brings peace and satisfaction.",
        "spanish": "En lugar de FOMO, los esencialistas adoptan JOMO (el placer de perderse las cosas), celebrando la elección de rechazar lo trivial.",
        "tags": ["books_path", "essentialism", "philosophy"]
    }
]

# ==================== 06_Four_Thousand_Weeks (20 cards) ====================
four_thousand_weeks = [
    {
        "scenario": "Four Thousand Weeks: Finite Life ⏳",
        "text": "The core premise of Oliver Burkeman is that the average human lifespan is around {{c1::four thousand weeks}}, making time management a matter of radical prioritization.",
        "explanation": "Accepting your finitude is the key to psychological peace. You will never have time for everything, so choose what to ignore.",
        "spanish": "La premisa central de Oliver Burkeman es que la vida humana promedio es de unas cuatro mil semanas, lo que hace crucial la priorización.",
        "tags": ["books_path", "time", "philosophy"]
    },
    {
        "scenario": "Four Thousand Weeks: The Efficiency Trap ⏳",
        "text": "The {{c1::Efficiency Trap}} states that becoming more efficient at clearing tasks only generates more tasks to fill the space.",
        "explanation": "If you reply to emails faster, you get more replies back. If you clear tasks faster, you get assigned more work. You can't beat the queue.",
        "spanish": "La trampa de la eficiencia establece que volverse más eficiente al completar tareas solo genera más tareas para llenar el espacio.",
        "tags": ["books_path", "time", "productivity"]
    },
    {
        "scenario": "Four Thousand Weeks: Convenience Culture ⏳",
        "text": "Convenience culture makes things frictionless, but it strips away the {{c1::meaning and connection}} of experiences that require time and effort.",
        "explanation": "Frictionless tasks feel easy, but they isolate us and make us lose patience with things that cannot be accelerated (relationships, deep learning).",
        "spanish": "La cultura de la conveniencia elimina la fricción, pero también elimina el significado y la conexión de las experiencias.",
        "tags": ["books_path", "time", "philosophy"]
    },
    {
        "scenario": "Four Thousand Weeks: Procrastination Acceptance ⏳",
        "text": "Instead of trying to avoid procrastination, practice {{c1::active procrastination}}—consciously choosing what to neglect so you can focus on the vital.",
        "explanation": "You will always procrastinate on something. The question is whether you procrastinate on the trivial or the vital.",
        "spanish": "En lugar de intentar evitar la procrastinación, practica la procrastinación activa: elegir conscientemente qué descuidar.",
        "tags": ["books_path", "time", "productivity"]
    },
    {
        "scenario": "Four Thousand Weeks: Limit-Embracing ⏳",
        "text": "Peace comes from living a {{c1::limit-embracing}} life—accepting that you cannot make every choice, read every book, or visit every country.",
        "explanation": "The anxiety of choice disappears when you accept that choosing one thing means rejecting all other options by definition.",
        "spanish": "La paz proviene de vivir una vida que acepta los límites, admitiendo que no puedes elegirlo todo.",
        "tags": ["books_path", "time", "philosophy"]
    },
    {
        "scenario": "Four Thousand Weeks: Attention Economy ⏳",
        "text": "Social media sites are designed to monetize your {{c1::attention}}, distracting you from the finite weeks of your actual life.",
        "explanation": "Your attention is your life. Distraction is a form of robbery of the finite weeks you have on earth.",
        "spanish": "Las redes sociales están diseñadas para monetizar tu atención, distrayéndote de las semanas finitas de tu vida real.",
        "tags": ["books_path", "time", "attention"]
    },
    {
        "scenario": "Four Thousand Weeks: The Joy of Doing Nothing ⏳",
        "text": "To reclaim your time, practice the art of {{c1::doing nothing}}—resting without the pressure of being productive or optimized.",
        "explanation": "We treat rest as a way to recover for more work (utility rest). True leisure has value in itself, not as utility.",
        "spanish": "Para recuperar tu tiempo, practica el arte de no hacer nada: descansar sin la presión de ser productivo.",
        "tags": ["books_path", "time", "leisure"]
    },
    {
        "scenario": "Four Thousand Weeks: The Next-Step Fallacy ⏳",
        "text": "The tendency to view the present moment only as a vehicle to reach some future state or milestone is the {{c1::next-step fallacy}}.",
        "explanation": "If you only live for the next milestone (promotion, vacation, retirement), you lose the ability to experience your life as it actually happens.",
        "spanish": "La tendencia a ver el momento presente solo como un vehículo para llegar a un estado futuro es la falacia del paso siguiente.",
        "tags": ["books_path", "time", "psychology"]
    },
    {
        "scenario": "Four Thousand Weeks: Strategic Under-Commitment ⏳",
        "text": "Keep a {{c1::fixed volume}} limit on your active projects (e.g. maximum of 3), placing all others on a backlog queue until one is finished.",
        "explanation": "Multitasking splits focus and delays all projects. Finishing one project before starting the next speeds up delivery.",
        "usage": "Limit your Kanban board active column to 3 cards maximum.",
        "spanish": "Mantén un límite de volumen fijo en tus proyectos activos (máximo 3), colocando los demás en cola de espera.",
        "tags": ["books_path", "time", "planning"]
    },
    {
        "scenario": "Four Thousand Weeks: Infinite Demands ⏳",
        "text": "The core paradox of productivity is: if you get faster at work, you get more work, because the volume of demands on your time is {{c1::infinite}}.",
        "explanation": "Demands are infinite, but time is finite. Trying to solve the equation by moving faster is mathematically impossible.",
        "spanish": "La paradoja central de la productividad: si trabajas más rápido, obtienes más trabajo, porque las demandas son infinitas.",
        "tags": ["books_path", "time", "productivity"]
    },
    {
        "scenario": "Four Thousand Weeks: The Decisive No ⏳",
        "text": "Every commitment requires a {{c1::decisive sacrifice}} of other possibilities. True commitment means closing off options.",
        "explanation": "If you keep options open, you commit to nothing deeply. Committing to a project or relationship requires letting go of alternatives.",
        "spanish": "Cada compromiso requiere un sacrificio decisivo de otras posibilidades. Comprometerse de verdad exige cerrar opciones.",
        "tags": ["books_path", "time", "philosophy"]
    },
    {
        "scenario": "Four Thousand Weeks: Leisure as an End ⏳",
        "text": "True leisure is an {{c1::autotelic}} activity—something done for its own sake, not to achieve a goal or improve yourself.",
        "explanation": "Playing a game, drawing, or walking just for the joy of it, not to post on social media or get fit.",
        "spanish": "El verdadero ocio es una actividad autotélica: algo que se hace por el placer de hacerlo, no para lograr una meta.",
        "tags": ["books_path", "time", "leisure"]
    },
    {
        "scenario": "Four Thousand Weeks: Impatience Spiral ⏳",
        "text": "Technology has made things so fast that we get caught in an {{c1::impatience spiral}}, getting angry when a web page takes 2 seconds to load.",
        "explanation": "The faster things become, the more painful the remaining friction feels.",
        "spanish": "La tecnología ha hecho que todo sea tan rápido que caemos en una espiral de impaciencia cuando algo tarda unos segundos.",
        "tags": ["books_path", "time", "psychology"]
    },
    {
        "scenario": "Four Thousand Weeks: Staying on the Bus ⏳",
        "text": "To achieve mastery or depth in a career or project, you must practice {{c1::staying on the bus}}—resisting the urge to switch paths when things get boring.",
        "explanation": "Mastery requires pushing past the initial excitement into the plateau of deep practice.",
        "spanish": "Para lograr el dominio en un proyecto, debes practicar 'quedarte en el autobús', resistiendo la tentación de cambiar de rumbo.",
        "tags": ["books_path", "time", "mastery"]
    },
    {
        "scenario": "Four Thousand Weeks: Cosmical Insignificance ⏳",
        "text": "Embrace your {{c1::cosmic insignificance}}—accepting that your life does not need to change the course of human history to be meaningful.",
        "explanation": "Lowers the pressure to be 'extraordinary' and allows you to enjoy simple, daily acts of kindness and connection.",
        "spanish": "Acepta tu insignificancia cósmica, admitiendo que tu vida no necesita cambiar la historia para tener sentido.",
        "tags": ["books_path", "time", "philosophy"]
    },
    {
        "scenario": "Four Thousand Weeks: The Limit of Control ⏳",
        "text": "You do not own your time; you can only {{c1::participate in it}} moment by moment. Trying to control the future causes anxiety.",
        "explanation": "We plan to secure the future, but the future is always uncertain. Live the present.",
        "spanish": "No eres dueño de tu tiempo; solo puedes participar en él momento a momento.",
        "tags": ["books_path", "time", "philosophy"]
    },
    {
        "scenario": "Four Thousand Weeks: Incremental Action ⏳",
        "text": "Burkeman recommends keeping a {{c1::closed list}} of tasks—items you commit to doing today, leaving all others on an open list.",
        "explanation": "An open list is a source of anxiety. A closed list is a boundary that defines success for today.",
        "usage": "Move 5 tasks from your general backlog to your 'Today' list and do not add others.",
        "spanish": "Burkeman recomienda mantener una lista cerrada de tareas: elementos que te comprometes a realizar hoy.",
        "tags": ["books_path", "time", "productivity"]
    },
    {
        "scenario": "Four Thousand Weeks: The Slow-Down Strategy ⏳",
        "text": "When faced with an overwhelming volume of work, the best response is to {{c1::slow down}} and do one task with complete attention.",
        "explanation": "Rushing causes errors and anxiety. Slowing down restores focus and quality.",
        "spanish": "Ante un volumen abrumador de trabajo, la mejor respuesta es reducir la velocidad y hacer una tarea con total atención.",
        "tags": ["books_path", "time", "focus"]
    },
    {
        "scenario": "Four Thousand Weeks: Time Sync ⏳",
        "text": "Time is valuable only when it is shared. Having complete freedom over your schedule is useless if you have no {{c1::shared time}} with friends and family.",
        "explanation": "Solitary time lacks the coordinate rhythm of shared community events.",
        "spanish": "El tiempo solo es valioso cuando se comparte. Tener control total de tu agenda es inútil sin tiempo compartido.",
        "tags": ["books_path", "time", "society"]
    },
    {
        "scenario": "Four Thousand Weeks: Patience ⏳",
        "text": "Patience is the willingness to let things take the time they {{c1::actually require}} rather than trying to force them to fit your schedule.",
        "explanation": "Allows you to engage with difficult tasks like coding complex architectures, reading dense books, or building relationships.",
        "spanish": "La paciencia es la disposición a permitir que las cosas tomen el tiempo que realmente requieren.",
        "tags": ["books_path", "time", "philosophy"]
    }
]

# ==================== 07_How_to_Take_Smart_Notes (20 cards) ====================
how_to_take_smart_notes = [
    {
        "scenario": "Smart Notes: Zettelkasten 🗂️",
        "text": "The core technique in How to Take Smart Notes is the {{c1::Zettelkasten}} (Slip-box) system, developed by German sociologist Niklas Luhmann.",
        "explanation": "A slip-box acts as an external thinking partner. It stores notes as atomic cards that are interconnected through links, creating a web of thought.",
        "spanish": "La técnica central en How to Take Smart Notes es el sistema Zettelkasten (caja de fichas), desarrollado por Niklas Luhmann.",
        "tags": ["books_path", "zettelkasten", "learning"]
    },
    {
        "scenario": "Smart Notes: Fleeting Notes 🗂️",
        "text": "In the slip-box system, {{c1::fleeting notes}} are temporary reminders, ideas, or quick captures that must be processed within a day or two.",
        "explanation": "These are messy notes captured on the go. They are discarded once their content is moved to permanent notes.",
        "usage": "Use a notepad or quick voice memo to write down a sudden idea while walking.",
        "spanish": "En el sistema Zettelkasten, las notas fugaces (fleeting notes) son recordatorios temporales que deben procesarse pronto.",
        "tags": ["books_path", "zettelkasten", "notes"]
    },
    {
        "scenario": "Smart Notes: Literature Notes 🗂️",
        "text": "When reading, you should take {{c1::literature notes}}—summarizing key arguments in your own words, keeping them short and citing the source.",
        "explanation": "Do not copy quotes. Summarizing forces active processing. Keep them in a central index folder.",
        "usage": "Write a 2-sentence summary of a chapter on a card, with reference to page numbers.",
        "spanish": "Al leer, debes tomar notas de literatura (literature notes), resumiendo los argumentos clave en tus propias palabras.",
        "tags": ["books_path", "zettelkasten", "notes"]
    },
    {
        "scenario": "Smart Notes: Permanent Notes 🗂️",
        "text": "The core assets of the slip-box are {{c1::permanent notes}}—atomic, self-contained thoughts written in full sentences that can be understood on their own.",
        "explanation": "Each permanent note contains exactly one idea. They are filed in the slip-box and connected to existing notes.",
        "usage": "Write a note: 'Spaced repetition works by retrieving memories just before they are forgotten.' Connect it to a note on neuroscience.",
        "spanish": "Los activos principales del Zettelkasten son las notas permanentes: pensamientos atómicos escritos con oraciones completas.",
        "tags": ["books_path", "zettelkasten", "notes"]
    },
    {
        "scenario": "Smart Notes: Atomic Principle 🗂️",
        "text": "The atomic principle states that each note must contain {{c1::only one idea}} so that it can be easily linked to other notes in different contexts.",
        "explanation": "If a note contains multiple topics, linking to it becomes confusing and the structure loses flexibility.",
        "spanish": "El principio atómico establece que cada nota debe contener solo una idea para que pueda enlazarse fácilmente.",
        "tags": ["books_path", "zettelkasten", "structure"]
    },
    {
        "scenario": "Smart Notes: Interconnection 🗂️",
        "text": "The value of a slip-box comes not from the number of notes, but from the {{c1::links between them}}.",
        "explanation": "Linking notes replicates the neural structure of the brain. It allows you to discover surprising connections and patterns.",
        "usage": "Use wiki-style links in Obsidian (e.g. [[Spaced Repetition]]) to connect related notes.",
        "spanish": "El valor de un Zettelkasten no proviene del número de notas, sino de los enlaces entre ellas.",
        "tags": ["books_path", "zettelkasten", "links"]
    },
    {
        "scenario": "Smart Notes: Index 🗂️",
        "text": "To find entry points into the web of notes, the slip-box uses an {{c1::index}}—a central document listing keywords and linking to key notes.",
        "explanation": "The index does not catalog everything; it only provides starting points for different topics.",
        "spanish": "Para encontrar puntos de entrada a la red de notas, el Zettelkasten utiliza un índice.",
        "tags": ["books_path", "zettelkasten", "index"]
    },
    {
        "scenario": "Smart Notes: Writing as Thinking 🗂️",
        "text": "The book argues that writing is not the product of thinking; rather, writing is the {{c1::medium in which thinking takes place}}.",
        "explanation": "You don't think first and then write. You think while writing, as the physical act of articulating thoughts exposes errors in logic.",
        "spanish": "El libro sostiene que escribir no es el producto del pensamiento, sino el medio en el que ocurre el pensamiento.",
        "tags": ["books_path", "zettelkasten", "philosophy"]
    },
    {
        "scenario": "Smart Notes: Top-Down vs Bottom-Up 🗂️",
        "text": "Instead of a top-down approach (creating folders and outlines first), the Zettelkasten is a {{c1::bottom-up}} system where structure emerges naturally from the notes.",
        "explanation": "Creating folders first restricts your thinking. Letting notes accumulate and group naturally lets connections guide the outline.",
        "spanish": "En lugar de un enfoque de arriba hacia abajo, el Zettelkasten es un sistema de abajo hacia arriba donde la estructura surge naturalmente.",
        "tags": ["books_path", "zettelkasten", "structure"]
    },
    {
        "scenario": "Smart Notes: Standardized Workflow 🗂️",
        "text": "To minimize cognitive friction, standardizing the {{c1::workflow of note-taking}} is essential, freeing up mental energy for actual thinking.",
        "explanation": "If you have to think about 'where to save this' or 'what template to use' every time, you waste willpower.",
        "usage": "Use a simple workflow: Quick capture on notepad -> convert to Obsidian atomic note at night -> link to 1-2 existing notes.",
        "spanish": "Para minimizar la fricción cognitiva, estandarizar el flujo de trabajo de la toma de notas es esencial.",
        "tags": ["books_path", "zettelkasten", "workflow"]
    },
    {
        "scenario": "Smart Notes: Internal Communication 🗂️",
        "text": "Luhmann described his slip-box as an independent partner with whom he could communicate, because the box often returned {{c1::unexpected connections}}.",
        "explanation": "As the box grows, notes you wrote years ago connect with new inputs, generating novel ideas automatically.",
        "spanish": "Luhmann describió su caja de fichas como un socio independiente con el que podía comunicarse debido a las conexiones inesperadas.",
        "tags": ["books_path", "zettelkasten", "philosophy"]
    },
    {
        "scenario": "Smart Notes: Fleeting Notes Disposal 🗂️",
        "text": "Fleeting notes should be {{c1::deleted or archived}} once they are processed into permanent notes.",
        "explanation": "Keeping messy fleeting notes clutters your inbox and increases cognitive noise.",
        "spanish": "Las notas fugaces deben eliminarse o archivarse una vez que se procesan en notas permanentes.",
        "tags": ["books_path", "zettelkasten", "notes"]
    },
    {
        "scenario": "Smart Notes: Self-Explaining 🗂️",
        "text": "Permanent notes must be written as if for a {{c1::stranger}}, explaining the context fully and using clear, unambiguous sentences.",
        "explanation": "You will forget the context in a few months. If the note is not self-contained, it will become useless.",
        "spanish": "Las notas permanentes deben escribirse como si fueran para un extraño, explicando el contexto por completo.",
        "tags": ["books_path", "zettelkasten", "notes"]
    },
    {
        "scenario": "Smart Notes: Literature Notes Location 🗂️",
        "text": "Keep literature notes separated from permanent notes, using the literature notes as a references list or {{c1::bibliography database}}.",
        "explanation": "Separation keeps the slip-box clean. The slip-box holds ideas; the bibliography holds references.",
        "spanish": "Mantén las notas de literatura separadas de las notas permanentes, utilizándolas como una base de datos bibliográfica.",
        "tags": ["books_path", "zettelkasten", "structure"]
    },
    {
        "scenario": "Smart Notes: Index Entry 🗂️",
        "text": "When adding a note to the slip-box, always search for at least {{c1::one existing note}} to link it to, ensuring it becomes part of the web.",
        "explanation": "An isolated note is a dead note. It will be forgotten because there is no path leading to it.",
        "spanish": "Al agregar una nota al Zettelkasten, busca siempre al menos una nota existente para enlazarla.",
        "tags": ["books_path", "zettelkasten", "links"]
    },
    {
        "scenario": "Smart Notes: Context over Category 🗂️",
        "text": "In a slip-box, focus on the {{c1::context of retrieval}} rather than the category of filing. Ask: 'In what situation will I want to find this note?'",
        "explanation": "Filing by topic (e.g. 'History') is too broad. Filing by use case (e.g. 'Examples of memory palaces') is highly actionable.",
        "spanish": "En un Zettelkasten, enfócate en el contexto de recuperación en lugar de la categoría de archivo.",
        "tags": ["books_path", "zettelkasten", "filing"]
    },
    {
        "scenario": "Smart Notes: Habit of Writing 🗂️",
        "text": "The primary indicator of academic productivity is the habit of daily {{c1::scholarly writing}}, not the volume of reading.",
        "explanation": "Reading without writing is consumer behavior. Writing forces structure and exposes limits of understanding.",
        "spanish": "El indicador principal de la productividad académica es el hábito de escribir diariamente.",
        "tags": ["books_path", "zettelkasten", "writing"]
    },
    {
        "scenario": "Smart Notes: Cognitive Load 🗂️",
        "text": "By offloading the storage of ideas to the slip-box, you reduce {{c1::cognitive load}}, allowing your working memory to focus entirely on reasoning.",
        "explanation": "Similar to GTD (Getting Things Done), externalizing ideas keeps the mind calm and alert.",
        "spanish": "Al transferir el almacenamiento de ideas al Zettelkasten, reduces la carga cognitiva.",
        "tags": ["books_path", "zettelkasten", "productivity"]
    },
    {
        "scenario": "Smart Notes: Luhmann's Card Format 🗂️",
        "text": "Luhmann's physical slip-box used a unique numbering system (e.g., 1, 1a, 1a1) that allowed him to insert new cards {{c1::anywhere in the sequence}}, enabling infinite branching.",
        "explanation": "Digital wikilinks replicate this numbering system without needing physical codes.",
        "spanish": "El Zettelkasten físico de Luhmann usaba un sistema de numeración único que le permitía insertar tarjetas en cualquier parte.",
        "tags": ["books_path", "zettelkasten", "history"]
    },
    {
        "scenario": "Smart Notes: Permanent Notes Rule 🗂️",
        "text": "Every permanent note must have a reference back to the {{c1::literature note}} or source it was derived from.",
        "explanation": "Ensures you can always double-check the source material to prevent misinterpretation or copyright issues.",
        "spanish": "Cada nota permanente debe tener una referencia a la nota de literatura de la que se derivó.",
        "tags": ["books_path", "zettelkasten", "notes"]
    }
]

save_deck("Productivity", "05_Essentialism", essentialism)
save_deck("Productivity", "06_Four_Thousand_Weeks", four_thousand_weeks)
save_deck("Productivity", "07_How_to_Take_Smart_Notes", how_to_take_smart_notes)
