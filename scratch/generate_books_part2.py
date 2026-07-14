import json
import os
from generate_books_part1 import save_deck

# ==================== 02_Become_a_SuperLearner (20 cards) ====================
become_a_superlearner = [
    {
        "scenario": "Become a SuperLearner: Visual Markers 👁️",
        "text": "The primary memory technique in Become a SuperLearner is creating {{c1::visual markers}}—highly detailed, bizarre, and emotionally charged mental images to represent concepts.",
        "explanation": "Human brains evolved to remember visual inputs and spatial layouts far better than abstract words or numbers. A boring image is forgotten quickly, but a strange or shocking one stick.",
        "usage": "If you want to remember that a client's name is 'Arthur', picture him sitting on a throne wearing a giant glowing crown (King Arthur).",
        "spanish": "La técnica de memoria principal en Become a SuperLearner es la creación de marcadores visuales: imágenes mentales altamente detalladas, extrañas y cargadas emocionalmente.",
        "tags": ["books_path", "memory", "superlearner"]
    },
    {
        "scenario": "Become a SuperLearner: Reading Speed vs Comprehension 📚",
        "text": "To increase reading speed without losing comprehension, you must reduce or eliminate {{c1::subvocalization}}—the habit of silently pronouncing each word in your mind as you read.",
        "explanation": "Subvocalization limits your reading speed to your speaking speed (around 150-250 words per minute). The brain can process visual symbols much faster without pronouncing them.",
        "usage": "Use a pointer (like a finger or pen) to guide your eyes and force them to move faster than your inner voice can speak.",
        "spanish": "Para aumentar la velocidad de lectura sin perder la comprensión, debes reducir o eliminar la subvocalización: el hábito de pronunciar silenciosamente cada palabra.",
        "tags": ["books_path", "speed_reading", "superlearner"]
    },
    {
        "scenario": "Become a SuperLearner: Regression 📚",
        "text": "Another major obstacle to speed reading is {{c1::regression}}—the unconscious habit of letting your eyes skip backward to re-read words or sentences you have already passed.",
        "explanation": "Regression wastes time and disrupts the flow of comprehension. It is often caused by lack of focus or lack of confidence in one's reading.",
        "usage": "Use a card or index card to cover the lines you have already read to physically prevent your eyes from skipping backward.",
        "spanish": "Otro obstáculo importante para la lectura rápida es la regresión: el hábito inconsciente de dejar que los ojos retrocedan para volver a leer palabras.",
        "tags": ["books_path", "speed_reading", "superlearner"]
    },
    {
        "scenario": "Become a SuperLearner: Saccades 📚",
        "text": "Speed readers train their eyes to make wider {{c1::saccades}}—the rapid movements of the eyes between fixation points—capturing whole groups of words at once.",
        "explanation": "Untrained readers fixate on every single word. Trained readers make fewer jumps and capture chunks of text using their peripheral vision.",
        "usage": "Practice looking at the center of a line and using your peripheral vision to read the words on the left and right sides.",
        "spanish": "Los lectores rápidos entrenan sus ojos para realizar movimientos sacádicos más amplios (los movimientos rápidos de los ojos entre puntos de fijación).",
        "tags": ["books_path", "speed_reading", "superlearner"]
    },
    {
        "scenario": "Become a SuperLearner: Memory Palace 🏰",
        "text": "A {{c1::Memory Palace}} (or Method of Loci) is a spatial memory technique where you place visual markers along a familiar route or location in your mind.",
        "explanation": "This technique leverages our highly developed evolutionary sense of navigation and spatial memory to order and retrieve information.",
        "usage": "Visualize your childhood home. Map out a path through 10 distinct furniture pieces, placing one concept image on each piece.",
        "spanish": "Un Palacio de la Memoria (o Método de Loci) es una técnica de memoria espacial en la que colocas marcadores visuales a lo largo de una ruta familiar.",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "Become a SuperLearner: The Number-Peg System 🔢",
        "text": "The {{c1::Number-Peg System}} maps numbers to specific visual objects (pegs) so that numerical data can be easily associated with other concepts.",
        "explanation": "Numbers are abstract and hard to remember. Assigning a permanent image to each number (e.g. 1 = candle, 2 = swan) allows you to link them to lists.",
        "usage": "To remember that you need to buy milk first, picture a swan (2) swimming in a lake of milk.",
        "spanish": "El Sistema de Clavijas Numéricas asocia números con objetos visuales específicos para que los datos numéricos puedan recordarse fácilmente.",
        "tags": ["books_path", "memory", "peg_system"]
    },
    {
        "scenario": "Become a SuperLearner: Creative Thinking 🧠",
        "text": "To create effective visual markers, you must practice {{c1::divergent thinking}}, allowing your brain to make absurd, humorous, or bizarre associations.",
        "explanation": "The more logical and normal an association is, the harder it is to remember. The brain pays attention to the unexpected.",
        "usage": "To remember the word 'hyperbole', visualize a giant hyperactive bowl of soup bouncing around the kitchen screaming.",
        "spanish": "Para crear marcadores visuales efectivos, debes practicar el pensamiento divergente, permitiendo que tu cerebro haga asociaciones absurdas o graciosas.",
        "tags": ["books_path", "memory", "creativity"]
    },
    {
        "scenario": "Become a SuperLearner: Pre-Reading 📚",
        "text": "Before reading a book or chapter, you should spend a few minutes {{c1::pre-reading}}—scanning headings, diagrams, and summaries to create a mental framework.",
        "explanation": "Pre-reading primes your brain. It acts like looking at the cover of a jigsaw puzzle before putting the pieces together.",
        "usage": "Spend 2-3 minutes scanning the table of contents and chapter summaries before starting a new technical manual.",
        "spanish": "Antes de leer un libro o capítulo, debes pasar unos minutos haciendo prelectura: escaneando títulos, diagramas y resúmenes.",
        "tags": ["books_path", "speed_reading", "prereading"]
    },
    {
        "scenario": "Become a SuperLearner: Habit Loops 🔄",
        "text": "Developing learning skills requires building new habits. A habit loop consists of three parts: a {{c1::cue}}, a {{c2::routine}}, and a {{c3::reward}}.",
        "explanation": "To build a reading habit, associate it with a cue (e.g., morning coffee), perform the routine (read for 20 minutes), and give yourself a reward.",
        "usage": "Cue: Sitting down on the bus. Routine: Open Kindle instead of social media. Reward: A piece of chocolate or positive self-talk.",
        "spanish": "Desarrollar habilidades de aprendizaje requiere construir nuevos hábitos. Un bucle de hábito consta de tres partes: una señal, una rutina y una recompensa.",
        "tags": ["books_path", "habits", "productivity"]
    },
    {
        "scenario": "Become a SuperLearner: Focused Attention 🧠",
        "text": "The quality of your learning is directly proportional to your {{c1::focus}} and the elimination of cognitive task-switching.",
        "explanation": "Every time you check your phone or switch tabs, you incur a 'cognitive switching cost' that slows down learning and drains mental energy.",
        "usage": "Study in a dedicated environment with all notifications silenced and tabs closed.",
        "spanish": "La calidad de tu aprendizaje es directamente proporcional a tu enfoque y a la eliminación del cambio de tareas cognitivas.",
        "tags": ["books_path", "focus", "productivity"]
    },
    {
        "scenario": "Become a SuperLearner: Intersecting Fields 🧠",
        "text": "To deepen understanding, you should look for connections between different fields, a concept known as {{c1::cross-pollination}} of ideas.",
        "explanation": "Innovations often occur at the intersection of two separate disciplines. Linking new ideas to fields you already master accelerates consolidation.",
        "usage": "If you are a musician learning to code, draw analogies between musical notation and coding structures (loops, variables).",
        "spanish": "Para profundizar en la comprensión, debes buscar conexiones entre diferentes campos, un concepto conocido como polinización cruzada de ideas.",
        "tags": ["books_path", "learning", "synthesis"]
    },
    {
        "scenario": "Become a SuperLearner: Active Learning 🧠",
        "text": "Instead of being a passive recipient of information, you must practice {{c1::active learning}} by questioning the author and making predictions.",
        "explanation": "Active engagement forces deeper cognitive processing. Passive reading is low-retention.",
        "usage": "Stop at the end of a section and ask: 'How does this apply to my current project? What would happen if this constraint changed?'",
        "spanish": "En lugar de ser un receptor pasivo de información, debes practicar el aprendizaje activo cuestionando al autor y haciendo predicciones.",
        "tags": ["books_path", "learning", "active_learning"]
    },
    {
        "scenario": "Become a SuperLearner: Visualization Rule 👁️",
        "text": "The book recommends the rule of **SEE**: {{c1::Sensory}}, {{c2::Exaggerated}}, {{c3::Energized}} images to create durable memory markers.",
        "explanation": "Sensory means involving smell, touch, sound. Exaggerated means making it giant or tiny. Energized means making the image move or explode.",
        "usage": "To remember the password 'apple5', visualize a giant, exploding apple (exaggerated, energized) smelling like sour candy (sensory) crushing a giant number 5.",
        "spanish": "El libro recomienda la regla de 'SEE': imágenes sensoriales, exageradas y energizadas para crear marcadores de memoria duraderos.",
        "tags": ["books_path", "memory", "visualization"]
    },
    {
        "scenario": "Become a SuperLearner: The Major System 🔢",
        "text": "The {{c1::Major System}} is a phonetic system that converts numbers into consonant sounds, which can then be turned into words and visual markers.",
        "explanation": "By mapping digits to consonants (e.g. 1 = t/d, 2 = n, 3 = m), you can convert any number (e.g. 12 = 'tin') into a visual object.",
        "usage": "Code digits into sounds, pad with vowels to make words, then place those word-images in your memory palace.",
        "spanish": "El Sistema Mayor es un sistema fonético que convierte números en sonidos consonánticos, que luego pueden convertirse en palabras.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "Become a SuperLearner: Sleep Quality 💤",
        "text": "Poor sleep quality directly impairs the process of {{c1::memory consolidation}}, which is the transfer of information from temporary storage (hippocampus) to permanent storage (cortex).",
        "explanation": "Sleep is when the brain replays and organizes the day's experiences, discarding noise and solidifying useful neural pathways.",
        "spanish": "La mala calidad del sueño perjudica directamente el proceso de consolidación de la memoria.",
        "tags": ["books_path", "learning", "sleep"]
    },
    {
        "scenario": "Become a SuperLearner: Cognitive Reserve 🧠",
        "text": "Regular mental exercise, physical activity, and healthy diet build {{c1::cognitive reserve}}, which protects the brain against aging and cognitive decline.",
        "explanation": "Learning complex skills (like languages or coding) creates a denser network of synapses, making the brain more resilient.",
        "spanish": "El ejercicio mental regular, la actividad física y una dieta saludable desarrollan la reserva cognitiva.",
        "tags": ["books_path", "health", "neuroscience"]
    },
    {
        "scenario": "Become a SuperLearner: Dual-Coding Theory 📊",
        "text": "Dual-coding theory states that learning is enhanced when information is presented in both {{c1::verbal}} and {{c2::visual}} formats simultaneously.",
        "explanation": "The brain processes words and images through separate channels, creating two independent pathways to retrieve the same concept.",
        "usage": "Use diagrams, flowcharts, or mind maps alongside text notes when studying complex code architectures.",
        "spanish": "La teoría de la codificación dual establece que el aprendizaje mejora cuando la información se presenta en formatos tanto verbales como visuales.",
        "tags": ["books_path", "learning", "dual_coding"]
    },
    {
        "scenario": "Become a SuperLearner: Contextual Cues 🧠",
        "text": "Retrieval of information is highly dependent on {{c1::contextual cues}}—environmental or internal states that were present when the memory was encoded.",
        "explanation": "If you study while stressed, you will recall the information best when stressed. If you study with music, that music becomes a retrieval cue.",
        "spanish": "La recuperación de información depende en gran medida de las señales contextuales presentes cuando se codificó la memoria.",
        "tags": ["books_path", "memory", "context"]
    },
    {
        "scenario": "Become a SuperLearner: Chunking Text 📚",
        "text": "To read faster, train your eyes to read chunks of text instead of individual words, focusing on the {{c1::spaces between words}} or the center of word groups.",
        "explanation": "Your brain can easily read and synthesize words in your peripheral vision if you don't look directly at each letter.",
        "spanish": "Para leer más rápido, entrena tus ojos para leer bloques de texto en lugar de palabras individuales.",
        "tags": ["books_path", "speed_reading", "chunking"]
    },
    {
        "scenario": "Become a SuperLearner: Chunking Numbers 🔢",
        "text": "When memorizing long digit strings, group them into {{c1::3-digit or 4-digit chunks}} instead of trying to remember them individually.",
        "explanation": "This maps to the working memory constraint of about 4 items. It's easier to remember '192 - 168 - 100' than '192168100'.",
        "spanish": "Al memorizar largas cadenas de dígitos, agrúpalas en fragmentos de 3 o 4 dígitos.",
        "tags": ["books_path", "memory", "chunking"]
    }
]

# ==================== 03_Make_It_Stick (20 cards) ====================
make_it_stick = [
    {
        "scenario": "Make It Stick: Retrieval Practice 📚",
        "text": "The cornerstone of effective learning is {{c1::retrieval practice}}—the act of recalling facts, concepts, or events from memory rather than re-reading them.",
        "explanation": "Retrieval forces the brain to search its memory network, which consolidates neural pathways and makes the information more accessible in the future.",
        "usage": "Use flashcards or write down everything you remember from a lecture on a blank sheet of paper.",
        "spanish": "La piedra angular del aprendizaje efectivo es la práctica de recuperación: el acto de recordar hechos, conceptos o eventos de la memoria.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Spaced Retrieval 📚",
        "text": "Retrieval practice is most effective when it is {{c1::spaced out}} over time, allowing some forgetting to occur between sessions.",
        "explanation": "When retrieval is slightly difficult because of forgetting, the cognitive effort required to recall the information strengthens the memory trace much more.",
        "usage": "Wait a few days before reviewing your notes, rather than studying them repeatedly on the same day.",
        "spanish": "La práctica de recuperación es más efectiva cuando se espacia a lo largo del tiempo, permitiendo que ocurra cierto olvido.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Interleaved Practice 📚",
        "text": "Instead of block practice, you should use {{c1::interleaved practice}}—alternating between different topics or skills during a single study session.",
        "explanation": "Interleaving helps your brain learn to identify the differences between problems and select the correct strategy.",
        "usage": "If practicing coding algorithms, mix array traversal, string formatting, and sorting problems in the same session.",
        "spanish": "En lugar de practicar en bloque, debes usar la práctica intercalada: alternar entre diferentes temas o habilidades.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Varied Practice 📚",
        "text": "Practicing a skill in {{c1::different contexts}} or varying the parameters of practice improves your ability to transfer the skill to new situations.",
        "explanation": "Varied practice builds a broader, more flexible schema in the brain, rather than a rigid, single-use habit.",
        "usage": "Write code in different IDEs, on different operating systems, or solve database design tasks for different industries.",
        "spanish": "Practicar una habilidad en diferentes contextos o variar los parámetros de la práctica mejora tu capacidad para transferir la habilidad.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Generation 📚",
        "text": "The process of trying to solve a problem before being shown the solution or explanation is called {{c1::generation}}.",
        "explanation": "Even if you fail or make mistakes, the cognitive struggle of trying to generate a solution primes your brain to learn and retain the correct explanation.",
        "usage": "Try to write a function or solve a puzzle yourself before looking at the tutorial or documentation.",
        "spanish": "El proceso de intentar resolver un problema antes de que se te muestre la solución o explicación se llama generación.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Elaboration 📚",
        "text": "Connecting new information to what you already know by putting it in your own words or finding real-world applications is called {{c1::elaboration}}.",
        "explanation": "Elaboration builds links between the new concepts and your existing mental framework, making the new memory trace much stronger.",
        "usage": "Explain a complex coding pattern to a non-technical friend or write a metaphor for it.",
        "spanish": "Conectar nueva información con lo que ya sabes poniéndola en tus propias palabras se llama elaboración.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Calibration 📚",
        "text": "To align your subjective sense of what you know with objective reality, you must use {{c1::calibration}}—using objective tests and feedback to identify blind spots.",
        "explanation": "Without objective feedback, you are highly vulnerable to the illusion of competence and overconfidence.",
        "usage": "Use quizzes, practice tests, or peer reviews to verify your actual skill level.",
        "spanish": "Para alinear tu sentido subjetivo de lo que sabes con la realidad objetiva, debes usar la calibración: usar pruebas objetivas.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Growth Mindset 📚",
        "text": "Embracing challenges and viewing mistakes as opportunities to grow neural connections is the hallmark of a {{c1::growth mindset}}.",
        "explanation": "Intelligence is not fixed. The brain is plastic and grows stronger when pushing through difficult cognitive challenges.",
        "usage": "When stuck on a bug, tell yourself: 'This struggle is helping my brain grow and learn new patterns.'",
        "spanish": "Adoptar desafíos y ver los errores como oportunidades para desarrollar conexiones neuronales es la marca de una mentalidad de crecimiento.",
        "tags": ["books_path", "psychology", "growth_mindset"]
    },
    {
        "scenario": "Make It Stick: Desirable Difficulties 📚",
        "text": "Short-term struggles that make learning feel slower and more difficult but lead to much stronger long-term retention are called {{c1::desirable difficulties}}.",
        "explanation": "Easy learning is often quickly forgotten. Cognitive effort during encoding and retrieval leads to deep learning.",
        "usage": "Examples of desirable difficulties: active recall, spaced repetition, generation, and interleaving.",
        "spanish": "Las dificultades a corto plazo que hacen que el aprendizaje parezca más lento pero conducen a una mayor retención se llaman dificultades deseables.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Reflection 📚",
        "text": "Taking a few minutes to review what you did, asking what worked, and identifying areas for improvement is the practice of {{c1::reflection}}.",
        "explanation": "Reflection combines retrieval practice and elaboration, helping you consolidate lessons and plan future strategies.",
        "usage": "At the end of a sprint or coding project, review the code and write down 3 things you learned or would do differently.",
        "spanish": "Tomarse unos minutos para revisar lo que hiciste, preguntar qué funcionó e identificar áreas de mejora es la práctica de la reflexión.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Illusions of Knowing 📚",
        "text": "The cognitive bias where you mistake familiarity with a text for mastery of the underlying concepts is called the {{c1::illusion of knowing}}.",
        "explanation": "Familiarity is passive. True mastery is the ability to retrieve and apply the concepts dynamically.",
        "usage": "Avoid simply highlighting and rereading. Instead, quiz yourself or apply the concepts.",
        "spanish": "El sesgo cognitivo en el que confundes la familiaridad con un texto con el dominio de los conceptos subyacentes se llama ilusión de conocimiento.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Mental Models 📚",
        "text": "A {{c1::mental model}} is a structured representation of external reality that your brain builds to understand how things work and make predictions.",
        "explanation": "As you practice, your brain groups chunks of related rules into overarching mental models, allowing you to solve complex, novel problems quickly.",
        "usage": "Build mental models of software design (e.g. MVC, Microservices) to guide your engineering decisions.",
        "spanish": "Un modelo mental es una representación estructurada de la realidad externa que tu cerebro construye para entender cómo funcionan las cosas.",
        "tags": ["books_path", "learning", "mental_models"]
    },
    {
        "scenario": "Make It Stick: Consolidating Memory 📚",
        "text": "The physical process in the brain where temporary memory traces are reorganized and stabilized into long-term storage is called {{c1::consolidation}}.",
        "explanation": "Consolidation takes hours or days. It requires neural processing during sleep and rest, which is why spacing study sessions is essential.",
        "spanish": "El proceso físico en el cerebro donde los rastros de memoria temporales se reorganizan y estabilizan se llama consolidación.",
        "tags": ["books_path", "learning", "neuroscience"]
    },
    {
        "scenario": "Make It Stick: Reconsolidation 📚",
        "text": "When you retrieve a memory, it becomes unstable and open to change. The process of modifying and restoring it back into long-term storage is {{c1::reconsolidation}}.",
        "explanation": "Reconsolidation allows you to update existing memories with new context, elaboration, or corrections.",
        "usage": "Every time you review a card and add new connections, you reconsolidate that memory.",
        "spanish": "Cuando recuperas un recuerdo, se vuelve inestable. El proceso de modificarlo y volver a almacenarlo se llama reconsolidación.",
        "tags": ["books_path", "learning", "neuroscience"]
    },
    {
        "scenario": "Make It Stick: Massed Practice 📚",
        "text": "Cramming or repeating the same skill over and over in a single session is called {{c1::massed practice}}, which leads to quick short-term performance but rapid long-term forgetting.",
        "explanation": "Massed practice feels productive because you see rapid improvement, but it doesn't build durable memory traces.",
        "usage": "Avoid 8-hour cram sessions before exams. Use daily 1-hour sessions instead.",
        "spanish": "Estudiar intensamente o repetir la misma habilidad una y otra vez en una sola sesión se llama práctica masiva.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Cognitive Map 📚",
        "text": "To navigate complex tasks, the brain constructs a {{c1::cognitive map}}—a mental layout of the task's rules, structures, and goals.",
        "explanation": "Elaborative study methods help build high-fidelity cognitive maps, allowing you to find alternative paths when obstacles arise.",
        "spanish": "Para navegar por tareas complejas, el cerebro construye un mapa cognitivo: un diseño mental de las reglas y estructuras.",
        "tags": ["books_path", "learning", "psychology"]
    },
    {
        "scenario": "Make It Stick: Structured Learning 📚",
        "text": "Effective learners practice {{c1::structure building}}—extracting the core rules and structure from new material and discarding irrelevant details.",
        "explanation": "Structure builders can quickly place new facts into their proper context. Low structure builders get overwhelmed by details.",
        "spanish": "Los estudiantes efectivos practican la construcción de estructuras: extraer las reglas y la estructura central del material.",
        "tags": ["books_path", "learning", "make_it_stick"]
    },
    {
        "scenario": "Make It Stick: Explanatory Power 📚",
        "text": "A key method of elaboration is trying to explain the {{c1::underlying principles}} of a concept rather than just memorizing definitions.",
        "explanation": "Understanding 'why' a system behaves a certain way gives you the power to troubleshoot and adapt.",
        "spanish": "Un método clave de elaboración es intentar explicar los principios subyacentes de un concepto en lugar de memorizar definiciones.",
        "tags": ["books_path", "learning", "elaboration"]
    },
    {
        "scenario": "Make It Stick: Calibration Blind Spot 📚",
        "text": "The tendency to overestimate your own competence is called the {{c1::Dunning-Kruger effect}}, which is corrected by calibrating against objective benchmarks.",
        "explanation": "Incompetent people lack the metacognitive skills to evaluate their own lack of competence. Feedback is the only cure.",
        "spanish": "La tendencia a sobreestimar tu propia competencia se llama efecto Dunning-Kruger.",
        "tags": ["books_path", "psychology", "calibration"]
    },
    {
        "scenario": "Make It Stick: Rule Learning 📚",
        "text": "In learning, distinguishing between **example learning** and **rule learning** is crucial: {{c1::rule learning}} allows you to apply the concept to completely new scenarios.",
        "explanation": "Example learning is shallow. Rule learning extracts the underlying pattern.",
        "usage": "Don't just copy code templates. Master the design rules so you can write them from scratch.",
        "spanish": "En el aprendizaje, distinguir entre el aprendizaje de ejemplos y el aprendizaje de reglas es crucial: el de reglas permite aplicar el concepto a nuevos escenarios.",
        "tags": ["books_path", "learning", "make_it_stick"]
    }
]

# ==================== 04_Building_a_Second_Brain (20 cards) ====================
building_a_second_brain = [
    {
        "scenario": "Second Brain: Definition 🗂️",
        "text": "Tiago Forte defines a {{c1::Second Brain}} as an external, digital system to capture, organize, and retrieve information to free up cognitive capacity for creativity.",
        "explanation": "The human brain is optimized for processing, creating, and connecting ideas, not for storing thousands of files and tasks. Offloading memory to a digital tool reduces stress and boosts creativity.",
        "usage": "Use note-taking apps (Obsidian, Notion) as your external database.",
        "spanish": "Tiago Forte define un Segundo Cerebro como un sistema digital externo para capturar, organizar y recuperar información.",
        "tags": ["books_path", "second_brain", "productivity"]
    },
    {
        "scenario": "Second Brain: CODE Framework 🗂️",
        "text": "The operational workflow of the Second Brain is the **CODE** framework: {{c1::Capture}}, {{c2::Organize}}, {{c3::Distill}}, and {{c4::Express}}.",
        "explanation": "These four steps represent the lifecycle of information as you collect it and transform it into useful output.",
        "usage": "Capture notes -> Organize using PARA -> Distill using Progressive Summarization -> Express by sharing your work.",
        "spanish": "El flujo de trabajo operativo del Segundo Cerebro es el marco 'CODE': Capture, Organize, Distill, y Express.",
        "tags": ["books_path", "second_brain", "productivity"]
    },
    {
        "scenario": "Second Brain: PARA Method 🗂️",
        "text": "To organize information by actionability, Tiago Forte created the **PARA** method: {{c1::Projects}}, {{c2::Areas}}, {{c3::Resources}}, and {{c4::Archives}}.",
        "explanation": "Instead of organizing by subject, PARA organizes by when the information will be used. This ensures your notes are always ready for action.",
        "usage": "Folder structure: 1. Projects (active tasks with deadlines), 2. Areas (ongoing responsibilities), 3. Resources (topics of interest), 4. Archives (inactive items).",
        "spanish": "Para organizar la información por su nivel de acción, Tiago Forte creó el método 'PARA': Projects, Areas, Resources, y Archives.",
        "tags": ["books_path", "second_brain", "para"]
    },
    {
        "scenario": "Second Brain: Projects 🗂️",
        "text": "Under PARA, a {{c1::Project}} is a series of tasks linked to a goal, with a specific deadline or completion criteria.",
        "explanation": "Projects are highly actionable and require immediate focus. Examples: 'Launch website', 'Submit tax return'.",
        "spanish": "Bajo PARA, un Proyecto (Project) es una serie de tareas vinculadas a una meta, con una fecha límite o criterio de finalización específico.",
        "tags": ["books_path", "second_brain", "para"]
    },
    {
        "scenario": "Second Brain: Areas 🗂️",
        "text": "Under PARA, an {{c1::Area}} is a sphere of activity with a standard to be maintained over time, without a final deadline.",
        "explanation": "Areas represent ongoing responsibilities. Examples: 'Health', 'Finance', 'Product management', 'Home maintenance'.",
        "spanish": "Bajo PARA, un Área (Area) es una esfera de actividad con un estándar a mantener a lo largo del tiempo, sin una fecha límite final.",
        "tags": ["books_path", "second_brain", "para"]
    },
    {
        "scenario": "Second Brain: Resources 🗂️",
        "text": "Under PARA, a {{c1::Resource}} is a topic or theme of ongoing interest, research, or utility.",
        "explanation": "Resources contain information that might be useful for future projects. Examples: 'Python coding tips', 'Web design templates', 'Travel options'.",
        "spanish": "Bajo PARA, un Recurso (Resource) es un tema de interés continuo, investigación o utilidad.",
        "tags": ["books_path", "second_brain", "para"]
    },
    {
        "scenario": "Second Brain: Archives 🗂️",
        "text": "Under PARA, {{c1::Archives}} contain inactive items from the other three categories that you want to keep for future reference.",
        "explanation": "Moving completed projects or outdated responsibilities to Archives keeps your active space clean and focused, preventing digital clutter.",
        "spanish": "Bajo PARA, los Archivos (Archives) contienen elementos inactivos de las otras tres categorías que deseas conservar para referencia futura.",
        "tags": ["books_path", "second_brain", "para"]
    },
    {
        "scenario": "Second Brain: Capture Criteria 🗂️",
        "text": "When capturing information, you should only save things that resonate with you or have immediate utility, a concept called the {{c1::Resonance Test}}.",
        "explanation": "If you try to capture everything, you will get overwhelmed. Capture only what feels surprising, useful, or inspiring.",
        "usage": "Ask yourself: 'Does this inspire me? Is this highly unique? Is this useful for an active project?'",
        "spanish": "Al capturar información, solo debes guardar lo que resuene contigo o tenga utilidad inmediata, conocido como el test de resonancia.",
        "tags": ["books_path", "second_brain", "capture"]
    },
    {
        "scenario": "Second Brain: Progressive Summarization 🗂️",
        "text": "To distill notes without losing context, use {{c1::Progressive Summarization}}—layering highlights over time based on when you review the note.",
        "explanation": "Allows you to compress the note's core value progressively, so you can read it in 10 seconds in the future.",
        "usage": "Layers: Layer 1 (raw text), Layer 2 (bold key phrases), Layer 3 (highlight key sentences), Layer 4 (executive summary at the top).",
        "spanish": "Para destilar notas sin perder el contexto, utiliza la resumación progresiva: aplicar capas de resaltado a lo largo del tiempo.",
        "tags": ["books_path", "second_brain", "distill"]
    },
    {
        "scenario": "Second Brain: Intermediate Packets 🗂️",
        "text": "To make expression easier, break projects down into {{c1::Intermediate Packets}}—small, reusable chunks of work (like code templates, meeting notes, or checklists).",
        "explanation": "Instead of starting every project from scratch, you assemble it using existing blocks from your Second Brain.",
        "usage": "Save a clean boilerplate of an API router as an Intermediate Packet in your Resources folder.",
        "spanish": "Para facilitar la expresión, divide los proyectos en paquetes intermedios (Intermediate Packets): pequeños fragmentos de trabajo reutilizables.",
        "tags": ["books_path", "second_brain", "express"]
    },
    {
        "scenario": "Second Brain: Divergence and Convergence 🗂️",
        "text": "Creative work alternates between {{c1::divergence}} (opening up options, gathering resources, researching) and {{c2::convergence}} (narrowing focus, editing, and producing the final product).",
        "explanation": "CODE maps to this cycle: Capture/Organize are divergent; Distill/Express are convergent. Don't try to edit while researching.",
        "spanish": "El trabajo creativo alterna entre la divergencia (abrir opciones, investigar) y la convergencia (reducir el enfoque, producir).",
        "tags": ["books_path", "second_brain", "creativity"]
    },
    {
        "scenario": "Second Brain: Archipelago of Ideas 🗂️",
        "text": "Before writing or coding, gather all your reference notes and place them in a document to create an {{c1::Archipelago of Ideas}}, which serves as a draft outline.",
        "explanation": "Prevents writer's block by ensuring you never start with a blank screen. You just connect the existing dots.",
        "usage": "Copy-paste relevant snippets, links, and code examples into a temporary file before writing a technical post.",
        "spanish": "Antes de escribir, reúne tus notas de referencia en un documento para crear un Archipiélago de Ideas, que sirve como borrador.",
        "tags": ["books_path", "second_brain", "express"]
    },
    {
        "scenario": "Second Brain: Cathedral Effect 🗂️",
        "text": "The psychological finding that physical space impacts thinking is the {{c1::Cathedral Effect}}: high ceilings promote abstract creativity, while low ceilings promote detail-oriented focus.",
        "explanation": "Digital environments behave similarly. A cluttered desktop causes cognitive load and limits creative thinking.",
        "usage": "Keep your desktop and active folders clean. Archive everything that isn't active.",
        "spanish": "El hallazgo de que el espacio físico influye en el pensamiento se llama Efecto Catedral: los techos altos promueven la creatividad abstracta.",
        "tags": ["books_path", "productivity", "psychology"]
    },
    {
        "scenario": "Second Brain: Slow Burns 🗂️",
        "text": "Instead of 'heavy lifts' (working on a project in one giant, exhausting session), use {{c1::slow burns}}—working on it incrementally over days or weeks in the background.",
        "explanation": "Slow burns allow your diffuse mode of thinking to work in the background, making the creative process effortless.",
        "usage": "Capture ideas for a new feature over a week, instead of sitting down to design it all in one night.",
        "spanish": "En lugar de esfuerzos pesados en una sola sesión, utiliza quemas lentas (slow burns): trabajar en proyectos de forma incremental.",
        "tags": ["books_path", "second_brain", "productivity"]
    },
    {
        "scenario": "Second Brain: Weekly Review 🗂️",
        "text": "The maintenance ritual of clearing your inbox, organizing files into PARA, and planning the next week's focus is the {{c1::Weekly Review}}.",
        "explanation": "Keeps your digital workspace from deteriorating into chaos. It rebuilds trust in your system.",
        "usage": "Set aside 30 minutes every Friday to clear downloads, review active projects, and clean up active notes.",
        "spanish": "El ritual de mantenimiento para limpiar bandejas de entrada, organizar archivos en PARA y planificar es la Revisión Semanal.",
        "tags": ["books_path", "second_brain", "productivity"]
    },
    {
        "scenario": "Second Brain: Digital Clutter 🗂️",
        "text": "Search features in modern software make heavy hierarchical folder structures obsolete. Instead, rely on {{c1::search and tags}} for retrieval.",
        "explanation": "Filing notes into deep subfolders takes time and increases friction. A flat folder structure combined with good search is faster.",
        "usage": "Keep PARA folders shallow. Use tags for topics and search index for finding specific words.",
        "spanish": "Las funciones de búsqueda hacen que las estructuras de carpetas profundas sean obsoletas. Confía en la búsqueda y las etiquetas.",
        "tags": ["books_path", "second_brain", "search"]
    },
    {
        "scenario": "Second Brain: Information Overload 🗂️",
        "text": "To prevent info-obesity, shift from being an **information consumer** to an {{c1::information producer}}, focusing on projects and output.",
        "explanation": "Consuming content without creating anything leads to stress and lack of focus. Actionable learning is the cure.",
        "usage": "Only capture information that is relevant to an active project or area of responsibility.",
        "spanish": "Para prevenir la sobrecarga de información, cambia de ser un consumidor de información a ser un productor de información.",
        "tags": ["books_path", "second_brain", "productivity"]
    },
    {
        "scenario": "Second Brain: Knowledge Assets 🗂️",
        "text": "Your notes are not just reminders; they are {{c1::knowledge assets}}—compounded intellectual capital that increases in value over time.",
        "explanation": "A well-maintained note collection serves as a personalized search engine that grows more valuable as you add connections.",
        "spanish": "Tus notas no son solo recordatorios; son activos de conocimiento (knowledge assets) que aumentan su valor con el tiempo.",
        "tags": ["books_path", "second_brain", "assets"]
    },
    {
        "scenario": "Second Brain: Habit of Capture 🗂️",
        "text": "The habit of immediately offloading ideas and tasks from your mind to a digital inbox is the practice of {{c1::externalization}}.",
        "explanation": "If you don't capture an idea immediately, your brain wastes cognitive energy trying to hold onto it, causing anxiety.",
        "usage": "Use a quick-capture widget on your phone to jot down ideas instantly.",
        "spanish": "El hábito de descargar inmediatamente ideas y tareas de tu mente a una bandeja de entrada digital es la práctica de externalización.",
        "tags": ["books_path", "second_brain", "capture"]
    },
    {
        "scenario": "Second Brain: Progressive Summarization Rule 🗂️",
        "text": "When distilling notes, the most important rule is to {{c1::not highlight everything}}, as this defeats the purpose of compression.",
        "explanation": "If everything is highlighted, nothing is highlighted. Only bold or highlight 10-20% of the text at each layer.",
        "spanish": "Al destilar notas, la regla más importante es no resaltar todo, ya que esto anula el propósito de la compresión.",
        "tags": ["books_path", "second_brain", "distill"]
    }
]

save_deck("Productivity", "02_Become_a_SuperLearner", become_a_superlearner)
save_deck("Productivity", "03_Make_It_Stick", make_it_stick)
save_deck("Productivity", "04_Building_a_Second_Brain", building_a_second_brain)
