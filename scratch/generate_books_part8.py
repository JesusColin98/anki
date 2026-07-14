import json
import os
from generate_books_part1 import save_deck

# ==================== 18_The_Art_Of_Memory (20 cards) ====================
the_art_of_memory = [
    {
        "scenario": "The Art of Memory: Simonides of Ceos 🏛️",
        "text": "The legendary inventor of the art of memory is **Simonides of Ceos**, who identified the bodies of banquet victims by recalling {{c1::where they were sitting}}.",
        "explanation": "This event established the fundamental principle that memory is organized spatially (loci) and visually (imagines).",
        "spanish": "El inventor legendario del arte de la memoria es Simónides de Ceos, quien identificó a las víctimas de un banquete recordando dónde estaban sentadas.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "The Art of Memory: Giulio Camillo 🏛️",
        "text": "Renaissance scholar Giulio Camillo designed a **Memory Theater**—a physical wooden structure where the spectator stands on the stage and looks at the auditorium, which represents {{c1::the entire universe of knowledge}}.",
        "explanation": "The theater was a physical memory palace. By standing in the center and looking at the paintings and drawers, the scholar could retrieve all human knowledge.",
        "spanish": "Giulio Camillo diseñó un Teatro de la Memoria: una estructura física que representa todo el universo del conocimiento.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "The Art of Memory: Giordano Bruno 🏛️",
        "text": "Giordano Bruno created complex memory systems based on {{c1::astrological wheels}} and concentric rings, combining Lullist logic with classical mnemonics.",
        "explanation": "Bruno's wheels rotated to generate new combinations of ideas, acting as a cognitive computer to synthesize concepts.",
        "spanish": "Giordano Bruno creó complejos sistemas de memoria basados en ruedas astrológicas y anillos concéntricos.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "The Art of Memory: Classical Mnemonics 🏛️",
        "text": "The classical memory system described in the Roman text **Ad Herennium** recommends using distinct, quiet, and well-lit locations spaced about {{c1::thirty feet}} apart.",
        "explanation": "Proper spacing between loci prevents visual markers from overlapping or causing confusion during retrieval.",
        "spanish": "El sistema clásico de memoria descrito en 'Ad Herennium' recomienda usar lugares espaciados a unos treinta pies de distancia.",
        "tags": ["books_path", "memory", "ad_herennium"]
    },
    {
        "scenario": "The Art of Memory: Imagines Agentes 🏛️",
        "text": "In Latin mnemonics, the visual markers placed in loci are called **imagines agentes**, which translates to {{c1::active / moving images}}.",
        "explanation": "A static image is easily forgotten. The images must be doing actions, experiencing pain, or performing dramatic scenes.",
        "spanish": "En la mnemotecnia latina, los marcadores visuales se llaman 'imagines agentes' (imágenes activas o en movimiento).",
        "tags": ["books_path", "memory", "ad_herennium"]
    },
    {
        "scenario": "The Art of Memory: Lullism 🏛️",
        "text": "The philosophical memory system developed by Ramon Llull (Lullism) used {{c1::concentric paper wheels}} containing letters representing concepts to calculate and prove theological truths.",
        "explanation": "Unlike the classical journey method, Lullism focused on logical synthesis and combinatorics, serving as a precursor to computer logic.",
        "spanish": "El sistema desarrollado por Ramon Llull (Lulismo) usaba ruedas de papel concéntricas para calcular verdades teológicas.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "The Art of Memory: Memory and Rhetoric 🏛️",
        "text": "In ancient Rome, memory was considered one of the **five pillars of rhetoric**, alongside Invention, Arrangement, Style, and {{c1::Delivery}}.",
        "explanation": "Orators had to deliver 3-hour speeches entirely from memory without notes. They did this by walking through memory palaces during their speeches.",
        "spanish": "En la antigua Roma, la memoria era considerada uno de los cinco pilares de la retórica.",
        "tags": ["books_path", "memory", "rhetoric"]
    },
    {
        "scenario": "The Art of Memory: Dialectical Memory 🏛️",
        "text": "During the Reformation, Ramists attacked the classical memory system, replacing visual images with {{c1::logical hierarchies and outlines}}.",
        "explanation": "Ramus argued that visual palaces were occult and messy, preferring structured textual tables (early mind maps).",
        "spanish": "Durante la Reforma, los ramistas atacaron el sistema clásico, reemplazando las imágenes visuales por esquemas lógicos.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "The Art of Memory: The Corporeal Similitude 🏛️",
        "text": "Thomas Aquinas recommended the use of **corporeal similitudes**—concrete physical images—to remember abstract {{c1::theological concepts}}.",
        "explanation": "Christianized the classical memory system, making it a tool for remembering virtues, vices, and scripture.",
        "spanish": "Tomás de Aquino recomendó el uso de similitudes corporales (imágenes físicas concretas) para recordar conceptos teológicos abstractos.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "The Art of Memory: Spatial Continuity 🏛️",
        "text": "To ensure correct retrieval order, a memory palace must preserve {{c1::spatial continuity}}—a single, unbroken path through the building.",
        "explanation": "Teleporting between rooms or crossing paths causes retrieval failures.",
        "spanish": "Para asegurar el orden correcto, un palacio de memoria debe preservar la continuidad espacial.",
        "tags": ["books_path", "memory", "journey_method"]
    },
    {
        "scenario": "The Art of Memory: Memory for Words 🏛️",
        "text": "Classical texts distinguish between **memoria rerum** (memory for things/concepts) and **memoria verborum** ({{c1::memory for words}}), warning that word-for-word memory is much harder.",
        "explanation": "Memoria rerum uses 1 image per concept. Memoria verborum requires an image for every single word, which is slow and rarely useful.",
        "spanish": "Los textos clásicos distinguen entre memoria rerum (de conceptos) y memoria verborum (de palabras).",
        "tags": ["books_path", "memory", "ad_herennium"]
    },
    {
        "scenario": "The Art of Memory: Hermetic Memory 🏛️",
        "text": "In the Renaissance, memory systems became linked to **Hermeticism**—the belief that by representing the universe in your mind, you could gain {{c1::magical control}} over it.",
        "explanation": "Giordano Bruno's systems were designed to internalize the astral patterns of the cosmos to unlock divine power.",
        "spanish": "En el Renacimiento, los sistemas de memoria se vincularon al Hermetismo, buscando control sobre el universo.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "The Art of Memory: Quiet Loci 🏛️",
        "text": "The places (loci) selected for a memory palace must be quiet and free from crowds, as {{c1::visual noise}} and human traffic erase the mental markers.",
        "explanation": "Avoid using active, crowded spaces like busy markets as locations.",
        "spanish": "Los lugares seleccionados para un palacio de memoria deben ser tranquilos y libres de multitudes.",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "The Art of Memory: Difference in Loci 🏛️",
        "text": "Each location in your memory palace must be {{c1::highly distinct}} in shape, size, and features, to prevent your mind from confusing different stages.",
        "explanation": "If all rooms or columns look identical (e.g. a long corridor of white doors), you will misplace your images.",
        "spanish": "Cada ubicación en tu palacio de memoria debe ser muy distinta para evitar confusiones.",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "The Art of Memory: Memory and Print 🏛️",
        "text": "The invention of the **printing press** in the 15th century eventually led to the {{c1::decline}} of the art of memory as an essential scholarly skill.",
        "explanation": "Once books became cheap and accessible, the need to hold libraries of data inside one's head disappeared.",
        "spanish": "La invención de la imprenta en el siglo XV provocó el declive del arte de la memoria como habilidad esencial.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "The Art of Memory: Memory for Things 🏛️",
        "text": "The Ad Herennium suggests that for **memoria rerum** (things), we should create images that represent the {{c1::actions or core arguments}} of the speech.",
        "explanation": "A single symbol (e.g. a sword for a battle, a scales for a trial) is enough to recall a whole section.",
        "spanish": "Ad Herennium sugiere que para memoria rerum creamos imágenes que representen las acciones de nuestro discurso.",
        "tags": ["books_path", "memory", "ad_herennium"]
    },
    {
        "scenario": "The Art of Memory: Cabalistic Memory 🏛️",
        "text": "Renaissance magi like Pico della Mirandola combined classical mnemonics with the **Cabala**, using Hebrew letters as {{c1::numerical and conceptual pegs}}.",
        "explanation": "Synthesized Jewish mysticism with classical memory architectures.",
        "spanish": "Magos del Renacimiento como Pico della Mirandola combinaron la mnemotecnia con la Cábala.",
        "tags": ["books_path", "memory", "history"]
    },
    {
        "scenario": "The Art of Memory: Simonides' Logic 🏛️",
        "text": "Simonides realized that the sense of {{c1::sight}} is the most powerful of all human senses, and that memory is order combined with visual images.",
        "explanation": "Foundational logic of all modern memory techniques.",
        "spanish": "Simónides se dio cuenta de que el sentido de la vista es el más poderoso y que la memoria es orden más imágenes.",
        "tags": ["books_path", "memory", "philosophy"]
    },
    {
        "scenario": "The Art of Memory: Loci Creation 🏛️",
        "text": "If you run out of real locations, classical authors suggest you can create {{c1::imagined / virtual places}} in your mind, provided they are structured logically.",
        "explanation": "Known as 'loci ficti'. Real spaces are preferred, but virtual architecture works if detailed.",
        "spanish": "Si te quedas sin ubicaciones reales, los autores clásicos sugieren que puedes crear lugares imaginados.",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "The Art of Memory: Memory and Ethics 🏛️",
        "text": "In the Middle Ages, memorizing the virtues and vices was considered a moral duty, making memory a key part of {{c1::ethics}} rather than just rhetoric.",
        "explanation": "Having the rules of behavior instantly accessible in memory was crucial for resisting temptation.",
        "spanish": "En la Edad Media, memorizar las virtudes y vicios se consideraba un deber moral y parte de la ética.",
        "tags": ["books_path", "memory", "history"]
    }
]

# ==================== 19_The_Memory_Book (20 cards) ====================
the_memory_book = [
    {
        "scenario": "The Memory Book: Link System 🔗",
        "text": "The **Link System** is a memory technique where you associate the first item in a list to the second, the second to the third, and so on, creating a {{c1::chain of associations}}.",
        "explanation": "Useful for short lists. If you lose one link, however, you risk losing the rest of the chain, which is its main weakness.",
        "spanish": "El Sistema de Enlace (Link System) es una técnica donde asocias el primer elemento de una lista con el segundo, y así sucesivamente.",
        "tags": ["books_path", "memory", "link_system"]
    },
    {
        "scenario": "The Memory Book: Peg System 🔗",
        "text": "The **Peg System** uses a pre-memorized list of target words (pegs) mapped to numbers, allowing you to associate new items to these pegs to remember them in {{c1::any order}}.",
        "explanation": "Unlike the link system, if you forget item 4, you can still recall item 5 because it is anchored to peg 5.",
        "spanish": "El Sistema de Clavijas (Peg System) utiliza una lista de palabras clave asociadas a números para recordar elementos en cualquier orden.",
        "tags": ["books_path", "memory", "peg_system"]
    },
    {
        "scenario": "The Memory Book: Major System Digit 3 🔢",
        "text": "In the phonetic Major System, the digit 3 is represented by the consonant sound {{c1::m}}.",
        "explanation": "Mapping: The letter 'm' has three downstrokes.",
        "spanish": "En el Sistema Mayor, el dígito 3 está representado por la letra m.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "The Memory Book: Major System Digit 4 🔢",
        "text": "In the phonetic Major System, the digit 4 is represented by the consonant sound {{c1::r}}.",
        "explanation": "Mapping: The word 'four' ends with the letter 'r'.",
        "spanish": "En el Sistema Mayor, el dígito 4 está representado por la letra r.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "The Memory Book: Major System Digit 5 🔢",
        "text": "In the phonetic Major System, the digit 5 is represented by the consonant sound {{c1::l}}.",
        "explanation": "Mapping: Roman numeral L represents 50. Hold out 5 fingers and the thumb/index make an 'L'.",
        "spanish": "En el Sistema Mayor, el dígito 5 está representado por la letra l.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "The Memory Book: Action-Link 🔗",
        "text": "To link two items, make the association {{c1::illogical and action-oriented}} (e.g. instead of a pencil lying on a book, picture a giant pencil writing on a book that is screaming).",
        "explanation": "Action and bizarre events capture attention. Logical images are ignored by the brain.",
        "spanish": "Para enlazar dos elementos, haz la asociación ilógica y orientada a la acción.",
        "tags": ["books_path", "memory", "visualization"]
    },
    {
        "scenario": "The Memory Book: Major System Digit 1 🔢",
        "text": "In the Major System, the digit 1 is represented by the consonant sounds {{c1::t or d}}.",
        "explanation": "Mapping: 't' and 'd' have a single vertical stroke.",
        "spanish": "En el Sistema Mayor, el dígito 1 se representa por los sonidos t o d.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "The Memory Book: Major System Digit 8 🔢",
        "text": "In the Major System, the digit 8 is represented by the consonant sounds {{c1::f or v}}.",
        "explanation": "Mapping: Script 'f' has two loops, resembling an 8.",
        "spanish": "En el Sistema Mayor, el dígito 8 se representa por los sonidos f o v.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "The Memory Book: Substitute Word 🧠",
        "text": "To memorize abstract names or foreign words, use the **Substitute Word System**—replacing the abstract word with a concrete word that {{c1::sounds similar}}.",
        "explanation": "For example, to remember 'Maryland', substitute with 'marry land' (visualize a wedding on a plot of grass).",
        "spanish": "Para memorizar nombres abstractos, usa el Sistema de Palabras Sustitutas, reemplazando la palabra por otra que suene similar.",
        "tags": ["books_path", "memory", "substitute_word"]
    },
    {
        "scenario": "The Memory Book: Remembering Names 👤",
        "text": "When meeting someone, look for an **outstanding feature** on their face (e.g. hairline, nose, chin) and link your {{c1::name-association image}} directly to that feature.",
        "explanation": "The face itself becomes the trigger. When you look at them, the outstanding feature prompts the image, which recalls the name.",
        "spanish": "Al conocer a alguien, busca un rasgo destacado en su rostro y vincula la imagen de asociación de su nombre a ese rasgo.",
        "tags": ["books_path", "memory", "names"]
    },
    {
        "scenario": "The Memory Book: Remembering Cards 🃏",
        "text": "To memorize playing cards, map suits to consonants: Spades = S, Clubs = C, Diamonds = D, Hearts = H. The card 2 of Diamonds (2D) becomes consonant pair N-D, which can be peg-word {{c1::Nod}}.",
        "explanation": "Digit + suit mapping turns cards into standard Major System peg words.",
        "spanish": "Para memorizar cartas, asocia los palos con consonantes y usa el Sistema Mayor.",
        "tags": ["books_path", "memory", "cards"]
    },
    {
        "scenario": "The Memory Book: Peg Word 1-10 🔗",
        "text": "The standard number-rhyme peg list for 1-3 is: 1 = {{c1::run}}, 2 = {{c2::shoe}}, 3 = {{c3::tree}}.",
        "explanation": "Rhyming pegs are easy to learn for beginners.",
        "spanish": "La lista de clavijas por rima para 1-3 es: 1 = run (correr), 2 = shoe (zapato), 3 = tree (árbol).",
        "tags": ["books_path", "memory", "peg_system"]
    },
    {
        "scenario": "The Memory Book: Memory and Age 🧠",
        "text": "Harry Lorayne argues that memory does not naturally decline with age; rather, it declines due to {{c1::lack of mental exercise}} and focus.",
        "explanation": "The brain preserves its neuroplasticity if challenged with active learning tasks.",
        "spanish": "Harry Lorayne sostiene que la memoria no disminuye naturalmente con la edad, sino por falta de ejercicio mental.",
        "tags": ["books_path", "memory", "health"]
    },
    {
        "scenario": "The Memory Book: Major System Digit 7 🔢",
        "text": "In the Major System, the digit 7 is represented by the consonant sounds {{c1::k or g}} (hard sounds).",
        "explanation": "Mapping: A capital 'K' can be formed by two 7s.",
        "spanish": "En el Sistema Mayor, el dígito 7 está representado por los sonidos k o g (fuertes).",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "The Memory Book: Major System Digit 9 🔢",
        "text": "In the Major System, the digit 9 is represented by the consonant sounds {{c1::p or b}}.",
        "explanation": "Mapping: Mirror image of 9 is 'P', and upside down is 'b'.",
        "spanish": "En el Sistema Mayor, el dígito 9 está representado por los sonidos p o b.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "The Memory Book: Remembering Numbers 🔢",
        "text": "To memorize telephone numbers or PINs, convert the digits into Major System words and {{c1::link them in a story}}.",
        "explanation": "A story links the digits in the correct order.",
        "spanish": "Para memorizar números de teléfono o PINs, convierte los dígitos en palabras y enlázalas en una historia.",
        "tags": ["books_path", "memory", "numbers"]
    },
    {
        "scenario": "The Memory Book: Observation 🧠",
        "text": "To remember anything, you must first observe it. The authors state: 'Original observation is the {{c1::first step of memory}}'.",
        "explanation": "If you don't focus your attention during encoding, there is no memory trace to retrieve. Most 'forgetting' is actually a failure to observe.",
        "spanish": "Para recordar algo, primero debes observarlo. La observación original es el primer paso de la memoria.",
        "tags": ["books_path", "memory", "focus"]
    },
    {
        "scenario": "The Memory Book: Key Word System 🗂️",
        "text": "To memorize articles or speeches, select a {{c1::Key Word}} from each paragraph and link them sequentially using the Link System.",
        "explanation": "One keyword serves as a retrieval cue for the entire paragraph concept.",
        "spanish": "Para memorizar artículos o discursos, selecciona una Palabra Clave de cada párrafo y enlázalas.",
        "tags": ["books_path", "memory", "rhetoric"]
    },
    {
        "scenario": "The Memory Book: Major System Digit 6 🔢",
        "text": "In the Major System, the digit 6 is represented by the consonant sounds {{c1::j, ch, sh, or soft g}}.",
        "explanation": "Phonetic mapping for sibilant consonants.",
        "spanish": "En el Sistema Mayor, el dígito 6 está representado por los sonidos j, ch, sh o g suave.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "The Memory Book: Association Rule 🧠",
        "text": "When making an association, ensure the two items are {{c1::touching / interacting}} rather than just side-by-side.",
        "explanation": "Physical interaction binds the two visual markers in the brain's visual processor.",
        "spanish": "Al hacer una asociación, asegúrate de que los dos elementos estén tocándose o interactuando.",
        "tags": ["books_path", "memory", "visualization"]
    }
]

# ==================== 20_Unlimited_Memory (20 cards) ====================
unlimited_memory = [
    {
        "scenario": "Unlimited Memory: TRUST Acronym 🔒",
        "text": "The framework for memory development in Unlimited Memory is **TRUST**: {{c1::Think}}, {{c2::Record}}, {{c3::Undertake}}, {{c4::Synergize}}, and {{c5::Track}}.",
        "explanation": "Kevin Horsley's 5-step model for training concentration, encoding, and practice.",
        "spanish": "El marco para el desarrollo de la memoria en Unlimited Memory es 'TRUST': Think, Record, Undertake, Synergize y Track.",
        "tags": ["books_path", "memory", "unlimited_memory"]
    },
    {
        "scenario": "Unlimited Memory: Think 🔒",
        "text": "In the TRUST framework, **Think** refers to clearing your mind, training your {{c1::concentration}}, and eliminating internal distractions before encoding.",
        "explanation": "If your mind is full of worries, your attention is divided and you cannot form durable memory traces.",
        "spanish": "En el marco TRUST, 'Think' se refiere a despejar tu mente, entrenar tu concentración y eliminar distracciones.",
        "tags": ["books_path", "memory", "focus"]
    },
    {
        "scenario": "Unlimited Memory: Record 🔒",
        "text": "In the TRUST framework, **Record** refers to the physical act of {{c1::encoding information using mnemonic tools}} like memory palaces or peg systems.",
        "explanation": "Active encoding creates structured hooks for retrieval.",
        "spanish": "En el marco TRUST, 'Record' se refiere al acto físico de codificar información utilizando herramientas mnemotécnicas.",
        "tags": ["books_path", "memory", "encoding"]
    },
    {
        "scenario": "Unlimited Memory: Concentration 🧠",
        "text": "Kevin Horsley defines concentration as {{c1::excluding all other thoughts}} to focus on a single task, a skill that must be trained like a muscle.",
        "explanation": "Concentration is the prerequisite for memory. If you don't concentrate, you don't encode.",
        "spanish": "Kevin Horsley define la concentración como la exclusión de todos los demás pensamientos para enfocarse en una sola tarea.",
        "tags": ["books_path", "memory", "focus"]
    },
    {
        "scenario": "Unlimited Memory: Memory Palaces 🏰",
        "text": "Unlimited Memory recommends using **your own body** or your **car** as a quick, {{c1::portable 10-stage journey}} for short-term lists.",
        "explanation": "Your body parts (feet, knees, hips, etc.) follow a natural order and are always accessible.",
        "spanish": "Unlimited Memory recomienda usar tu propio cuerpo o tu coche como un viaje rápido de 10 etapas.",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "Unlimited Memory: Self-Discipline 🧠",
        "text": "To achieve extraordinary memory, you must take {{c1::personal responsibility}} for your mind's focus, refusing to make excuses about having a 'bad memory'.",
        "explanation": "Believing you have a bad memory is a self-fulfilling prophecy. Memory is a trained capacity.",
        "spanish": "Para lograr una memoria extraordinaria, debes asumir la responsabilidad personal del enfoque de tu mente.",
        "tags": ["books_path", "memory", "psychology"]
    },
    {
        "scenario": "Unlimited Memory: Association Rule 🧠",
        "text": "Mnemonic associations must be **SEE**: {{c1::Senses}}, {{c2::Exaggeration}}, {{c3::Energy}}.",
        "explanation": "Similar to Jonathan Levi's model, SEE outlines the three attributes of a durable visual marker.",
        "spanish": "Las asociaciones mnemotécnicas deben ser 'SEE': Senses (Sentidos), Exaggeration (Exageración) y Energy (Energía).",
        "tags": ["books_path", "memory", "visualization"]
    },
    {
        "scenario": "Unlimited Memory: Peg System 🔗",
        "text": "A **Peg System** acts like a {{c1::mental wardrobe}} with permanent hangers (pegs) where you can hang new information as it arrives.",
        "explanation": "Allows you to store and retrieve lists in any order.",
        "spanish": "Un sistema de clavijas (Peg System) funciona como un armario mental con perchas permanentes.",
        "tags": ["books_path", "memory", "peg_system"]
    },
    {
        "scenario": "Unlimited Memory: Spacing 🔄",
        "text": "To prevent memory decay, review your memory palaces using a spaced schedule: after 10 minutes, 1 hour, {{c1::1 day}}, 3 days, and 1 week.",
        "explanation": "An optimal review timeline to solidify information in the cortex.",
        "spanish": "Para prevenir el deterioro de la memoria, revisa tus palacios utilizando un programa espaciado.",
        "tags": ["books_path", "memory", "spaced_repetition"]
    },
    {
        "scenario": "Unlimited Memory: Focus Barrier 🧠",
        "text": "The biggest barrier to concentration is {{c1::multitasking}}, which splits cognitive attention and makes deep encoding impossible.",
        "explanation": "Every time you multitask, you reduce your memory capacity.",
        "spanish": "La mayor barrera para la concentración es la multitarea (multitasking).",
        "tags": ["books_path", "memory", "focus"]
    },
    {
        "scenario": "Unlimited Memory: Word Pegs 1-10 🔗",
        "text": "The phonetic Major System peg word for 1 is {{c1::tie}} (consonant sound t) and for 2 is {{c2::Noah}} (consonant sound n).",
        "explanation": "Standard Major System word peg mappings.",
        "spanish": "La palabra clave del Sistema Mayor para el 1 es tie y para el 2 es Noah.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "Unlimited Memory: Word Pegs 1-10 🔗",
        "text": "The Major System peg word for 3 is {{c1::Ma}} (consonant m) and for 4 is {{c2::rye}} (consonant r).",
        "explanation": "Standard Major System word peg mappings.",
        "spanish": "La palabra clave del Sistema Mayor para el 3 es Ma y para el 4 es rye.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "Unlimited Memory: Word Pegs 1-10 🔗",
        "text": "The Major System peg word for 5 is {{c1::law}} (consonant l) and for 6 is {{c2::shoe}} (consonant sh).",
        "explanation": "Standard Major System word peg mappings.",
        "spanish": "La palabra clave del Sistema Mayor para el 5 es law y para el 6 es shoe.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "Unlimited Memory: Word Pegs 1-10 🔗",
        "text": "The Major System peg word for 7 is {{c1::key}} (consonant k) and for 8 is {{c2::ivy}} (consonant v).",
        "explanation": "Standard Major System word peg mappings.",
        "spanish": "La palabra clave del Sistema Mayor para el 7 es key y para el 8 es ivy.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "Unlimited Memory: Word Pegs 1-10 🔗",
        "text": "The Major System peg word for 9 is {{c1::bee}} (consonant b) and for 10 is {{c2::toes}} (consonants t-s).",
        "explanation": "Standard Major System word peg mappings.",
        "spanish": "La palabra clave del Sistema Mayor para el 9 es bee y para el 10 es toes.",
        "tags": ["books_path", "memory", "major_system"]
    },
    {
        "scenario": "Unlimited Memory: Active Memory 🧠",
        "text": "Memory is not a passive container; it is an {{c1::active process}} of construction and reconstruction.",
        "explanation": "You don't download memories; you build them using attention and association.",
        "spanish": "La memoria no es un contenedor pasivo, sino un proceso activo de construcción.",
        "tags": ["books_path", "memory", "philosophy"]
    },
    {
        "scenario": "Unlimited Memory: Concentrated Reading 📚",
        "text": "To remember what you read, stop at the end of every page and write down a {{c1::one-word summary}} or draw a visual symbol of the main concept.",
        "explanation": "Forces you to pay attention and process the text actively.",
        "spanish": "Para recordar lo que lees, detente al final de cada página y escribe un resumen de una sola palabra.",
        "tags": ["books_path", "memory", "reading"]
    },
    {
        "scenario": "Unlimited Memory: Trusting memory 🧠",
        "text": "You must learn to {{c1::trust your memory}} during recall, rather than second-guessing yourself or using notes prematurely.",
        "explanation": "Searching your mind build search pathways. Giving up early weakens recall strength.",
        "spanish": "Debes aprender a confiar en tu memoria durante el recuerdo, sin dudar de ti mismo.",
        "tags": ["books_path", "memory", "psychology"]
    },
    {
        "scenario": "Unlimited Memory: Spatial Anchoring 🏰",
        "text": "When using a journey, always place the visual markers at {{c1::eye-level}} and make them the same size as the environment to keep the layout realistic.",
        "explanation": "Keeps the spatial mapping stable in your mind.",
        "spanish": "Al usar un viaje, coloca siempre los marcadores visuales a la altura de los ojos.",
        "tags": ["books_path", "memory", "loci"]
    },
    {
        "scenario": "Unlimited Memory: Overcoming Boredom 🧠",
        "text": "Boredom is a signal that your brain is not fully engaged. To overcome it, increase the {{c1::absurdity and sensory detail}} of your visual markers.",
        "explanation": "If the images are boring, your mind will wander. Make them spectacular.",
        "spanish": "El aburrimiento es una señal de falta de compromiso. Aumenta el absurdo de tus imágenes.",
        "tags": ["books_path", "memory", "focus"]
    }
]

save_deck("Memory", "18_The_Art_Of_Memory", the_art_of_memory)
save_deck("Memory", "19_The_Memory_Book", the_memory_book)
save_deck("Memory", "20_Unlimited_Memory", unlimited_memory)
