import json
import os
from generate_books_part1 import save_deck

# ==================== 15_How_to_Develop_a_Brilliant_Memory (20 cards) ====================
how_to_develop_a_brilliant_memory = [
    {
        "scenario": "Brilliant Memory: Dominic System 🔢",
        "text": "The **Dominic System** is a mnemonic system that maps two-digit numbers (00-99) to a person and an action using a specific letter code: {{c1::A=1, B=2, C=3, D=4, E=5, S=6, G=7, H=8, N=9, O=0}}.",
        "explanation": "Developed by 8-time World Memory Champion Dominic O'Brien. For example, 15 is AE (Albert Einstein), action: 'chalking a blackboard'.",
        "spanish": "El Sistema Dominic asocia números de dos dígitos con una persona y una acción usando un código de letras específico (A=1, B=2, C=3, D=4, E=5, S=6, G=7, H=8, N=9, O=0).",
        "tags": ["books_path", "memory", "dominic_system"]
    },
    {
        "scenario": "Brilliant Memory: Letter Code 🔢",
        "text": "In the Dominic System, the letter code for the number 6 is {{c1::S}} and for the number 0 is {{c2::O}}.",
        "explanation": "Mapping: 6 is 'S' (looks like 6/six), 0 is 'O' (looks like 0/zero).",
        "spanish": "En el Sistema Dominic, la letra para el número 6 es S y para el 0 es O.",
        "tags": ["books_path", "memory", "dominic_system"]
    },
    {
        "scenario": "Brilliant Memory: Person-Action-Object 🔢",
        "text": "To encode large numbers (e.g. 4 digits), combine the **Person** of the first 2 digits with the **Action** of the second 2 digits, a technique called {{c1::PA}} (Person-Action).",
        "explanation": "For example, if 15 is Albert Einstein (writing on blackboard) and 80 is Harry Houdini (escaping chains), 1580 is encoded as: Albert Einstein escaping chains.",
        "spanish": "Para codificar números grandes, combina la persona de los primeros dos dígitos con la acción de los segundos dos (técnica Person-Action).",
        "tags": ["books_path", "memory", "pa_system"]
    },
    {
        "scenario": "Brilliant Memory: The Journey Method 🏰",
        "text": "The primary retrieval framework used by Dominic O'Brien is the {{c1::Journey Method}}, which places visual markers along a series of real-world loci.",
        "explanation": "A journey is an ordered sequence of locations (stages) that you know perfectly (e.g. walk to work, park, museum). It guarantees you retrieve items in the correct order.",
        "spanish": "El marco de recuperación principal utilizado por Dominic O'Brien es el Método del Viaje (Journey Method).",
        "tags": ["books_path", "memory", "journey_method"]
    },
    {
        "scenario": "Brilliant Memory: Rule of Association 🧠",
        "text": "The golden rule of memory is {{c1::Association}}—connecting new, unfamiliar information to existing, familiar mental structures.",
        "explanation": "You cannot memorize something in isolation. You must build a bridge between the new data and what you already know.",
        "spanish": "La regla de oro de la memoria es la Asociación: conectar información nueva con estructuras familiares existentes.",
        "tags": ["books_path", "memory", "association"]
    },
    {
        "scenario": "Brilliant Memory: Exaggeration 👁️",
        "text": "Mnemonic images must be {{c1::exaggerated}} in size, quantity, color, or sound to force the brain's attention systems to record them.",
        "explanation": "Our brains discard thousands of ordinary experiences daily. Making an image giant, noisy, or funny triggers long-term storage.",
        "spanish": "Las imágenes mnemotécnicas deben ser exageradas en tamaño o color para captar la atención del cerebro.",
        "tags": ["books_path", "memory", "visualization"]
    },
    {
        "scenario": "Brilliant Memory: Rule of Loci 🏰",
        "text": "When placing images in a journey, ensure they are {{c1::physically interacting}} with the environment of the locus (e.g. a giant apple squashing the sofa).",
        "explanation": "If the image just floats in the air, the connection to the location is weak, making it harder to retrieve.",
        "spanish": "Al colocar imágenes en un viaje, asegúrate de que interactúen físicamente con el entorno del lugar.",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "Brilliant Memory: Review Rule 🔄",
        "text": "To cement a journey in long-term memory, Dominic O'Brien recommends the **Rule of Five**: review the journey after 5 minutes, 1 hour, {{c1::1 day}}, 1 week, and 1 month.",
        "explanation": "A structured spaced repetition review schedule for keeping memory palaces durable.",
        "spanish": "Para consolidar un viaje en la memoria, O'Brien recomienda la Regla de Cinco: revisar tras 5 min, 1 hora, 1 día, 1 semana y 1 mes.",
        "tags": ["books_path", "memory", "spaced_repetition"]
    },
    {
        "scenario": "Brilliant Memory: Remembering Names 👤",
        "text": "To remember names, use the **L.A.S.T.** method: {{c1::Listen}} to the name, {{c2::Associate}} it with a visual marker, {{c3::Store}} it on a feature of the person's face, and {{c4::Test}} yourself immediately.",
        "explanation": "Storing the marker on a prominent facial feature (like a big nose or eyebrows) ensures the cue fires whenever you look at them.",
        "spanish": "Para recordar nombres, usa L.A.S.T.: Escuchar (Listen), Asociar (Associate), Guardar (Store) y Evaluar (Test).",
        "tags": ["books_path", "memory", "names"]
    },
    {
        "scenario": "Brilliant Memory: Card Memorization 🃏",
        "text": "To memorize a deck of cards, map each card to a Dominic System person/action. A deck of 52 cards is memorized along a journey of {{c1::26}} stages using Person-Action combinations.",
        "explanation": "Card 1 (Person) + Card 2 (Action) = 1 stage. Reduces the number of loci needed by half.",
        "spanish": "Para memorizar una baraja de cartas, asocia cada carta con una persona/acción del Sistema Dominic. Se necesitan 26 etapas.",
        "tags": ["books_path", "memory", "cards"]
    },
    {
        "scenario": "Brilliant Memory: Letter Code 🔢",
        "text": "In the Dominic System, the letter code for the number 3 is {{c1::C}} and for the number 8 is {{c2::H}}.",
        "explanation": "Mapping: 3 is 'C' (looks like C), 8 is 'H' (sounds like H/eight).",
        "spanish": "En el Sistema Dominic, las letras para el 3 y el 8 son C y H.",
        "tags": ["books_path", "memory", "dominic_system"]
    },
    {
        "scenario": "Brilliant Memory: Remembering Dates 📅",
        "text": "To memorize historical dates (e.g. 1914), split them into two 2-digit numbers (19 and 14) and encode them as a {{c1::Person-Action}} pair in your journey.",
        "explanation": "19 = SN, 14 = AD. Encode as: Person SN performing Action of AD.",
        "spanish": "Para memorizar fechas históricas, divídelas en dos números de 2 dígitos y codifícalas como un par Persona-Acción.",
        "tags": ["books_path", "memory", "dates"]
    },
    {
        "scenario": "Brilliant Memory: Cognitive Maps 🏰",
        "text": "Dominic O'Brien argues that memory palaces should rely on {{c1::real locations}} you have physically visited, as virtual or imagined spaces are less durable.",
        "explanation": "Real places are deeply encoded in the brain's spatial hardware. Virtual spaces require active energy to maintain.",
        "spanish": "O'Brien sostiene que los palacios de memoria deben basarse en lugares reales que hayas visitado.",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "Brilliant Memory: Spacing 🔄",
        "text": "When reviewing journeys, avoid reviewing the same palace multiple times in a single day, as this causes {{c1::ghost images}} (crossover interference between review sessions).",
        "explanation": "Ghost images happen when old markers haven't decayed before you place new ones in the same location.",
        "spanish": "Al revisar viajes, evita repasar el mismo palacio varias veces al día para evitar imágenes fantasma (interferencia).",
        "tags": ["books_path", "memory", "interference"]
    },
    {
        "scenario": "Brilliant Memory: Focus 🧠",
        "text": "Mnemonic encoding requires absolute {{c1::attention focus}} during the moment of association; if your mind wanders for 1 second, the link fails.",
        "explanation": "Association is a high-attention process. A weak link cannot be retrieved.",
        "spanish": "La codificación mnemotécnica requiere un enfoque de atención absoluto durante el momento de la asociación.",
        "tags": ["books_path", "memory", "focus"]
    },
    {
        "scenario": "Brilliant Memory: Sensory Integration 👁️",
        "text": "Incorporate multiple senses into your markers (e.g., the coldness of ice, the smell of smoke, the sound of breaking glass) to increase the {{c1::density of neural links}}.",
        "explanation": "Multi-sensory memory traces are far more robust than purely visual ones.",
        "spanish": "Incorpora múltiples sentidos en tus marcadores para aumentar la densidad de los enlaces neuronales.",
        "tags": ["books_path", "memory", "sensory"]
    },
    {
        "scenario": "Brilliant Memory: Number peg System 🔢",
        "text": "The Dominic System maps 0-9 to letters, which are then combined to form pairs: 0 = O, 1 = A, 2 = B, 3 = C, 4 = D, 5 = E, 6 = S, 7 = G, 8 = H, 9 = {{c1::N}}.",
        "explanation": "The standard O'Brien letter code mapping.",
        "spanish": "La correspondencia de letras del Sistema Dominic para el 9 es N.",
        "tags": ["books_path", "memory", "dominic_system"]
    },
    {
        "scenario": "Brilliant Memory: Binary Numbers 🔢",
        "text": "To memorize binary numbers (e.g. 110101), group them into {{c1::3-digit or 4-digit blocks}} and convert those blocks to decimal numbers before using the Dominic System.",
        "explanation": "Reduces the number of items to memorize. E.g. binary 110 = decimal 6, which is mapped to a letter or peg.",
        "spanish": "Para memorizar números binarios, agrúpalos en bloques de 3 o 4 dígitos y conviértelos a decimal.",
        "tags": ["books_path", "memory", "binary"]
    },
    {
        "scenario": "Brilliant Memory: Location choice 🏰",
        "text": "A good journey should have clear, distinct stages that follow a {{c1::logical direction}} without backtracking or crossing paths.",
        "explanation": "Backtracking causes confusion during retrieval. Keep the route linear (e.g., room by room, street by street).",
        "spanish": "Un buen viaje debe tener etapas claras que sigan una dirección lógica sin retroceder ni cruzarse.",
        "tags": ["books_path", "memory", "journey_method"]
    },
    {
        "scenario": "Brilliant Memory: Mental Speed 🧠",
        "text": "World Memory Champions achieve high speed by training their brains to make associations instantly, a skill called {{c1::cognitive flexibility}}.",
        "explanation": "Speed comes from trusting your first creative association instead of over-analyzing.",
        "spanish": "La velocidad de memorización se logra entrenando al cerebro para hacer asociaciones de forma instantánea.",
        "tags": ["books_path", "memory", "speed"]
    }
]

# ==================== 16_Memory_Craft (20 cards) ====================
memory_craft = [
    {
        "scenario": "Memory Craft: Lukasa 🪵",
        "text": "In African Luba culture, a **Lukasa** is a handheld {{c1::wooden board covered in beads and shells}} used as a physical memory device to store tribal history and genealogies.",
        "explanation": "The memory performer runs their fingers over the tactile layout of beads to retrieve specific stories and names. Tactile cues are highly durable.",
        "spanish": "En la cultura Luba, un Lukasa es una tabla de madera cubierta de cuentas y conchas utilizada como dispositivo físico de memoria.",
        "tags": ["books_path", "memory", "lukasa"]
    },
    {
        "scenario": "Memory Craft: Songlines 🗺️",
        "text": "Australian Aboriginal peoples use **Songlines**—complex paths across the landscape where geographical features serve as {{c1::sacred memory places}} for storing survival data (water, plants, paths).",
        "explanation": "Songlines combine journey methods with music and performance. Singing the song while walking the path retrieves the survival map.",
        "spanish": "Los pueblos aborígenes australianos utilizan las líneas de canciones (Songlines): rutas donde los accidentes geográficos sirven como lugares de memoria.",
        "tags": ["books_path", "memory", "songlines"]
    },
    {
        "scenario": "Memory Craft: Bestiary 🦁",
        "text": "A medieval **Bestiary** is an illustrated book of beasts used as a memory helper, where each animal's characteristics serve as a {{c1::visual cue}} to store moral or scientific lessons.",
        "explanation": "The strange, often monstrous descriptions of animals made them highly memorable visual markers for monks.",
        "spanish": "Un Bestiario medieval es un libro ilustrado de bestias donde cada animal sirve como clave visual para recordar lecciones.",
        "tags": ["books_path", "memory", "medieval"]
    },
    {
        "scenario": "Memory Craft: Winter Counts 📅",
        "text": "Native American Plains tribes recorded history using **Winter Counts**—pictographs drawn on hide skins representing the {{c1::most memorable event}} of each year.",
        "explanation": "Served as a physical timeline calendar. The keeper of the hide could recite decades of history by pointing to the drawings.",
        "spanish": "Las tribus de las llanuras americanas registraban su historia usando Winter Counts: pictogramas que representan el evento más memorable de cada año.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "Memory Craft: Tactile Cues 🪵",
        "text": "Memory Craft highlights the value of {{c1::tactile and physical cues}} (like touching carved marks or handling beads) alongside visual imagery to double-code memory.",
        "explanation": "Engaging the touch sensors in your hands adds a physical spatial channel of retrieval.",
        "spanish": "Memory Craft destaca el valor de las claves táctiles y físicas junto con las imágenes visuales para codificar el recuerdo.",
        "tags": ["books_path", "memory", "tactile"]
    },
    {
        "scenario": "Memory Craft: Memory Spaces 🏰",
        "text": "Lynne Kelly recommends building small, physical memory spaces (like a {{c1::Memory Tray}} or a decorated walk path in your garden) to memorize facts.",
        "explanation": "You don't need giant journeys; you can populate a small tray of unique objects on your desk to hold 20-30 concepts.",
        "spanish": "Lynne Kelly recomienda construir pequeños espacios físicos de memoria, como una bandeja de memoria (Memory Tray).",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "Memory Craft: The Lukasa Method 🪵",
        "text": "To adapt the Lukasa system, you can use a small, decorated board or a {{c1::handheld clay tablet}} with carved patterns to memorize list data.",
        "explanation": "Running your thumb over physical ridges while recalling names binds the data to a motor action.",
        "spanish": "Para adaptar el sistema Lukasa, puedes usar una pequeña tabla decorada o una tableta de arcilla con patrones tallados.",
        "tags": ["books_path", "memory", "lukasa"]
    },
    {
        "scenario": "Memory Craft: Oral Tradition 🗣️",
        "text": "Indigenous cultures maintain vast catalogs of scientific data without writing by using performance, song, dance, and {{c1::mythology}} as memory tools.",
        "explanation": "Mythological stories are not just religion; they are memory wrappers designed to store environmental safety data.",
        "spanish": "Las culturas indígenas mantienen catálogos científicos sin escritura mediante cantos, bailes y mitología.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "Memory Craft: Vowel pegging 🔢",
        "text": "To store lists, use **vowel pegging** or spelling codes, mapping the first letter of words to a sequence of {{c1::consonants}}.",
        "explanation": "Mnemonic spelling codes allow you to create words from abstract lists.",
        "spanish": "Para almacenar listas, utiliza la asociación de vocales o códigos de ortografía mnemotécnicos.",
        "tags": ["books_path", "memory", "pegs"]
    },
    {
        "scenario": "Memory Craft: The Bestiary Trick 🦁",
        "text": "To memorize classification systems (like biological orders or syntax rules), assign each category to a {{c1::monstrous animal}} with exaggerated features.",
        "explanation": "Medieval scholars used grotesque or funny animal drawings because they knew the brain forgets normal layouts.",
        "spanish": "Para memorizar sistemas de clasificación, asigna cada categoría a un animal monstruoso con rasgos exagerados.",
        "tags": ["books_path", "memory", "medieval"]
    },
    {
        "scenario": "Memory Craft: Songlines Adaptation 🗺️",
        "text": "You can build a personal Songline by mapping concepts to a {{c1::walk through your neighborhood}}, composing a simple rhyme or song that describes each stage.",
        "explanation": "Combining the rhythm of walking, singing, and spatial cues forms an extremely durable memory trace.",
        "spanish": "Puedes construir una Songline personal asignando conceptos a un paseo por tu vecindario y creando una rima.",
        "tags": ["books_path", "memory", "songlines"]
    },
    {
        "scenario": "Memory Craft: Lukasa Beads 🪵",
        "text": "On a Lukasa, a large bead represents a {{c1::major event or ruler}}, while smaller surrounding beads represent details or descendants.",
        "explanation": "A physical hierarchy of data, similar to mind maps but tactile.",
        "spanish": "En un Lukasa, una cuenta grande representa un evento importante, mientras que las pequeñas representan detalles.",
        "tags": ["books_path", "memory", "lukasa"]
    },
    {
        "scenario": "Memory Craft: Hand Mnemonic ✋",
        "text": "The **Hand Mnemonic** involves mapping items to the joints, tips, and folds of your {{c1::fingers and palm}}, providing an instant 20-stage journey that is always with you.",
        "explanation": "Used historically by monks for musical scales and calendar calculations.",
        "spanish": "El mnemónico de la mano implica asignar elementos a las articulaciones, yemas y pliegues de tus dedos.",
        "tags": ["books_path", "memory", "hand_system"]
    },
    {
        "scenario": "Memory Craft: Physical Objects 🏺",
        "text": "Lynne Kelly suggests that historical artifacts like carved stone balls or decorated pottery were not art, but {{c1::portable memory devices}}.",
        "explanation": "Provides a new anthropological framework for understanding prehistory artifacts.",
        "spanish": "Lynne Kelly sugiere que muchos artefactos históricos eran en realidad dispositivos de memoria portátiles.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "Memory Craft: Storytelling Wrapper 🗣️",
        "text": "To prevent data decay over generations, wrap scientific information inside a {{c1::narrative story}} with memorable characters.",
        "explanation": "Stories follow cause-and-effect logic, making them much easier to remember than disconnected facts.",
        "spanish": "Para evitar el deterioro de los datos, envuelve la información científica dentro de una historia narrativa.",
        "tags": ["books_path", "memory", "storytelling"]
    },
    {
        "scenario": "Memory Craft: Landscape Memory 🗺️",
        "text": "For indigenous peoples, the landscape is not just space; it is the {{c1::library}} that holds all tribal knowledge.",
        "explanation": "Without writing, nature itself becomes the memory palace that houses the culture's knowledge.",
        "spanish": "Para los pueblos indígenas, el paisaje es la biblioteca que contiene todo el conocimiento tribal.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "Memory Craft: Sensory Memory Craft 🧠",
        "text": "Combining visual, auditory, and tactile memory channels is called {{c1::multi-sensory encoding}}.",
        "explanation": "The more areas of the brain involved in encoding, the more retrieval paths you create.",
        "spanish": "La combinación de canales de memoria visuales, auditivos y táctiles se llama codificación multisensorial.",
        "tags": ["books_path", "memory", "sensory"]
    },
    {
        "scenario": "Memory Craft: Winter Count Calendar 📅",
        "text": "A Winter Count pictograph acts as an {{c1::anchor cue}} that prompts the memory keeper to recall all the secondary events of that year.",
        "explanation": "One drawing acts as a index key for a whole network of associated memories.",
        "spanish": "Un pictograma de Winter Count actúa como una clave de anclaje para recordar todos los eventos secundarios de ese año.",
        "tags": ["books_path", "memory", "anchoring"]
    },
    {
        "scenario": "Memory Craft: Lukasa Bead Texture 🪵",
        "text": "The beads on a Lukasa differ in size, color, height, and {{c1::texture}} (smooth shell vs rough stone) to create distinct tactile markers.",
        "explanation": "Texture increases the number of sensory distinctions available to the memory performer.",
        "spanish": "Las cuentas de un Lukasa difieren en tamaño, color y textura para crear marcadores táctiles distintos.",
        "tags": ["books_path", "memory", "tactile"]
    },
    {
        "scenario": "Memory Craft: Portable Palaces 🏰",
        "text": "A pocket-sized book, a deck of cards, or a set of keys can serve as a {{c1::portable memory palace}} if you assign a permanent meaning to each item.",
        "explanation": "Allows you to carry complex data packages in your pocket.",
        "spanish": "Un libro de bolsillo, una baraja o un llavero pueden servir como palacio de memoria portátil.",
        "tags": ["books_path", "memory", "loci"]
    }
]

# ==================== 17_Moonwalking_with_Einstein (20 cards) ====================
moonwalking_with_einstein = [
    {
        "scenario": "Moonwalking: PAO System 🔢",
        "text": "The **PAO System** (Person-Action-Object) maps numbers (usually 00-99) to a unique compound image consisting of a {{c1::Person}}, doing a specific {{c2::Action}}, with a physical {{c3::Object}}.",
        "explanation": "Allows you to compress 6 digits into a single mental image. Digit 1-2 = Person, 3-4 = Action, 5-6 = Object.",
        "spanish": "El Sistema PAO (Person-Action-Object) asocia números con una imagen compuesta por una persona, una acción y un objeto.",
        "tags": ["books_path", "memory", "pao_system"]
    },
    {
        "scenario": "Moonwalking: PAO Compression 🔢",
        "text": "To encode the 6-digit number 158099 using PAO, combine the **Person** of 15, the **Action** of 80, and the **Object** of 99 into {{c1::a single compound scene}}.",
        "explanation": "If 15 = Albert Einstein (chalking), 80 = Harry Houdini (escaping chains), and 99 = Darth Vader (holding a lightsaber), the scene is: Albert Einstein (15) escaping chains (80) while holding a lightsaber (99).",
        "spanish": "Para codificar un número de 6 dígitos con PAO, se combina la persona del primer par, la acción del segundo y el objeto del tercero.",
        "tags": ["books_path", "memory", "pao_system"]
    },
    {
        "scenario": "Moonwalking: US Memory Championship 🏆",
        "text": "Joshua Foer's journey from journalist to winner of the {{c1::US Memory Championship}} is the narrative focus of Moonwalking with Einstein.",
        "explanation": "Demonstrates that extraordinary memory is a trained skill, not an innate talent.",
        "spanish": "El viaje de Joshua Foer de periodista a ganador del Campeonato de Memoria de EE.UU. es el foco narrativo del libro.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "Moonwalking: Memory Palace 🏰",
        "text": "The main technique used by mental athletes is the {{c1::Memory Palace}}, which exploits our natural evolutionary brain structures for spatial navigation.",
        "explanation": "Placing bizarre images along a route in a familiar building.",
        "spanish": "La técnica principal utilizada por los atletas mentales es el Palacio de la Memoria.",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "Moonwalking: The Major System 🔢",
        "text": "The Major System maps digits to consonant sounds: 1 = t/d, 2 = n, 3 = m, 4 = r, 5 = l, 6 = sh/ch/j, 7 = k/g, 8 = f/v, 9 = p/b, 0 = {{c1::z/s}}.",
        "explanation": "Standard code used to convert numbers into memorable words.",
        "spanish": "El Sistema Mayor asocia dígitos con sonidos consonánticos (por ejemplo, 1 es t/d, 2 es n, y 0 es z/s).",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "Moonwalking: Synesthesia 🧠",
        "text": "Memory experts often develop a form of artificial {{c1::synesthesia}}—blending visual, auditory, and tactile sensations during encoding.",
        "explanation": "Makes the memory traces multidimensional and easier to retrieve.",
        "spanish": "Los expertos en memoria desarrollan sinestesia artificial, mezclando sensaciones visuales, auditivas y táctiles.",
        "tags": ["books_path", "memory", "sensory"]
    },
    {
        "scenario": "Moonwalking: Forgetting Curve 📈",
        "text": "The **Hermann Ebbinghaus Forgetting Curve** shows that memory decay occurs {{c1::exponentially}} right after learning, unless review sessions are scheduled.",
        "explanation": "You lose up to 60-80% of new information within 24 hours without review.",
        "spanish": "La Curva del Olvido de Ebbinghaus muestra que el deterioro de la memoria ocurre exponencialmente justo después del aprendizaje.",
        "tags": ["books_path", "memory", "ebbinghaus"]
    },
    {
        "scenario": "Moonwalking: Mental Plateau 🧠",
        "text": "To break through a performance plateau in memory training, you must push yourself to practice at a speed {{c1::faster than is comfortable}}, making mistakes deliberately.",
        "explanation": "Similar to typing practice; you must force yourself past the automated, comfortable speed limit to grow new neural capacity.",
        "spanish": "Para superar una meseta de rendimiento en la memoria, debes practicar a una velocidad más rápida de lo cómodo.",
        "tags": ["books_path", "memory", "plateau"]
    },
    {
        "scenario": "Moonwalking: Sensory Anchors 🧠",
        "text": "The brain remembers things that are **grotesque, sexual, or humorous** because these features trigger our evolutionary {{c1::survival and attention circuits}}.",
        "explanation": "The amygdala flags emotionally charged events as highly important for memory consolidation.",
        "spanish": "El cerebro recuerda lo grotesco, sexual o gracioso porque estos rasgos activan los circuitos de supervivencia y atención.",
        "tags": ["books_path", "memory", "visualization"]
    },
    {
        "scenario": "Moonwalking: The OK Plateau 🧠",
        "text": "The {{c1::OK Plateau}} is the state where a skill becomes automated and you stop improving (e.g. typing or driving), which can only be broken by deliberate practice.",
        "explanation": "Automation makes performance easy but prevents progress. Push past comfort to improve.",
        "spanish": "El 'OK Plateau' es el estado en el que una habilidad se automatiza y dejas de mejorar, a menos que uses práctica deliberada.",
        "tags": ["books_path", "memory", "mastery"]
    },
    {
        "scenario": "Moonwalking: S. (Solomon Shereshevsky) 👤",
        "text": "Joshua Foer discusses **S.**, a famous Russian mnemonist who had a virtually {{c1::limitless memory}} due to profound, automatic synesthesia.",
        "explanation": "S. could remember lists of 70 words decades later, but struggled with abstract concepts and metaphors because he couldn't forget details.",
        "spanish": "El libro analiza a S., un mnemonista ruso con una memoria prácticamente ilimitada debido a una sinestesia profunda.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "Moonwalking: The Ribot Law 🧠",
        "text": "The **Ribot Law** of retrograde amnesia states that {{c1::recent memories}} are lost first during brain damage, while oldest memories are most resistant.",
        "explanation": "Older memories have had years to undergo systemic consolidation, building wider networks in the cortex.",
        "spanish": "La Ley de Ribot de la amnesia retrógrada establece que los recuerdos recientes se pierden primero en caso de daño cerebral.",
        "tags": ["books_path", "memory", "neuroscience"]
    },
    {
        "scenario": "Moonwalking: Eidetic Memory Myth 🧠",
        "text": "The book argues that true **eidetic memory** (photographic memory) in adults is a {{c1::myth}}, and all memory champions rely on learned techniques rather than structural brain differences.",
        "explanation": "Scientific testing has failed to find adults who can capture pages of text like a camera without training.",
        "spanish": "El libro sostiene que la verdadera memoria eidética (fotográfica) en adultos es un mito.",
        "tags": ["books_path", "memory", "science"]
    },
    {
        "scenario": "Moonwalking: Spatial Memory 🏰",
        "text": "The brain's grid cells and place cells in the {{c1::hippocampus}} are the biological basis for the effectiveness of the Journey Method.",
        "explanation": "We possess specialized neural hardware dedicated to spatial mapping, which we hijack to store abstract concepts.",
        "spanish": "Las células de red y de lugar en el hipocampo son la base biológica del Método del Viaje.",
        "tags": ["books_path", "memory", "neuroscience"]
    },
    {
        "scenario": "Moonwalking: Chunking 🧠",
        "text": "Joshua Foer explains that {{c1::chunking}} is the process of grouping individual data items into larger, meaningful packages, bypassing working memory limits.",
        "explanation": "Allows chess masters to remember board layouts because they see 'defensive setups' instead of individual pieces.",
        "spanish": "Joshua Foer explica que el chunking es el proceso de agrupar elementos individuales en paquetes significativos.",
        "tags": ["books_path", "memory", "chunking"]
    },
    {
        "scenario": "Moonwalking: Baker/baker Paradox 👤",
        "text": "The **Baker/baker Paradox** shows that the brain remembers the occupation 'baker' much better than the name 'Baker', because the occupation is linked to a rich {{c1::network of visual associations}} (bread, white hat, smell).",
        "explanation": "Names are abstract; occupations are concrete and experiential.",
        "spanish": "La paradoja de Baker/baker muestra que el cerebro recuerda mejor la profesión 'panadero' (baker) que el apellido 'Baker'.",
        "tags": ["books_path", "memory", "association"]
    },
    {
        "scenario": "Moonwalking: The Major System Digit 2 🔢",
        "text": "In the Major System, the digit 2 is represented by the consonant sound {{c1::n}}.",
        "explanation": "Mapping: 2 has two vertical strokes when written, resembling the letter 'n'.",
        "spanish": "En el Sistema Mayor, el dígito 2 se representa por el sonido de la consonante n.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "Moonwalking: Palace Cleanup 🏰",
        "text": "To reuse a memory palace for a new list, you must allow the old visual markers to {{c1::decay / fade away}} over a few days.",
        "explanation": "Prevents cognitive interference. Champions have multiple palaces that they rotate.",
        "spanish": "Para reutilizar un palacio de memoria, debes permitir que los marcadores anteriores se desvanezcan.",
        "tags": ["books_path", "memory", "interference"]
    },
    {
        "scenario": "Moonwalking: Deliberate Practice Rule 🧠",
        "text": "Anders Ericsson defines **Deliberate Practice** as requiring a clear goal, high focus, immediate feedback, and working at the {{c1::edge of your ability}}.",
        "explanation": "You don't improve by repeating what is easy; you improve by targeting mistakes.",
        "spanish": "Anders Ericsson define la práctica deliberada como trabajar en el límite de tu capacidad.",
        "tags": ["books_path", "memory", "mastery"]
    },
    {
        "scenario": "Moonwalking: The Memory Palace Route 🏰",
        "text": "When choosing a route for a memory palace, it is best to follow a {{c1::linear path}} (e.g. clockwise around a room) to ensure no stages are missed.",
        "explanation": "A structured route prevents you from skipping locations during retrieval.",
        "spanish": "Al elegir una ruta para un palacio de memoria, es mejor seguir un camino lineal.",
        "tags": ["books_path", "memory", "journey_method"]
    }
]

save_deck("Memory", "15_How_to_Develop_a_Brilliant_Memory", how_to_develop_a_brilliant_memory)
save_deck("Memory", "16_Memory_Craft", memory_craft)
save_deck("Memory", "17_Moonwalking_with_Einstein", moonwalking_with_einstein)
