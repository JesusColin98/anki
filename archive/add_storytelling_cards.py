import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_cards = [
    # 06_Storytelling_Foundations
    {
        "deck": "Social_Skills::06_Storytelling_Foundations",
        "scenario": "Storytelling: Dan Harmon's Story Circle ⭕",
        "text": "In Dan Harmon's Story Circle, the protagonist's journey follows eight steps: Zone of Comfort, Need, Go into an {{c1::unfamiliar situation}}, Adapt, Get what they wanted, Pay a {{c2::heavy price}}, Return, and change.",
        "explanation": "The Story Circle simplifies the Hero's Journey into a cycle of desire, crossing thresholds, pain, and integration. It focuses on the psychological change of the protagonist as they return to their comfort zone modified by the cost of their journey.",
        "usage": "A powerful structure for formatting personal anecdotes, presentations, and product launch case studies.",
        "spanish": "En el Círculo de la Historia de Dan Harmon, el viaje del protagonista sigue ocho pasos: Zona de confort, Necesidad, Entrar en una situación nueva, Adaptarse, Obtener lo que querían, Pagar un precio alto, Regresar y cambiar.",
        "tags": ["storytelling", "story_circle", "structure"]
    },
    {
        "deck": "Social_Skills::06_Storytelling_Foundations",
        "scenario": "Storytelling: In Media Res Openings 🎬",
        "text": "To immediately hook the listener's attention, the narrative technique {{c1::In Media Res}} bypasses introductory explanations and starts the story directly at the point of {{c2::climax or highest conflict}}.",
        "explanation": "In Media Res (Latin for 'into the middle of things') forces the audience to ask questions (Who? Why? How did we get here?) which creates an immediate psychological open loop. Details about the background are filled in later using brief flashbacks or context.",
        "usage": "Used to replace boring chronologically linear introductions in business pitches or personal storytelling.",
        "spanish": "Para captar inmediatamente la atención del oyente, la técnica narrativa In Media Res omite las explicaciones introductorias y comienza la historia directamente en el punto de clímax o mayor conflicto.",
        "tags": ["storytelling", "openings", "hooks"]
    },
    {
        "deck": "Social_Skills::06_Storytelling_Foundations",
        "scenario": "Storytelling: Nancy Duarte's Sparklines ⚡",
        "text": "Nancy Duarte's Sparklines structure presentations by constantly contrasting {{c1::what is (current reality)}} with {{c2::what could be (future potential)}} to build emotional tension and release.",
        "explanation": "Sparklines create a rhythmic cadence. The gap between the status quo and the ideal future creates a motivational pull, culminating in a clear call to action that defines the new normal.",
        "usage": "The standard template for persuasive speeches, keynote addresses, and investor pitches (e.g. Steve Jobs' iPhone launch).",
        "spanish": "Las Sparklines de Nancy Duarte estructuran las presentaciones contrastando constantemente lo que es (realidad actual) frente a lo que podría ser (potencial futuro) para crear tensión y liberación emocional.",
        "tags": ["storytelling", "presentations", "persuasion"]
    },
    {
        "deck": "Social_Skills::06_Storytelling_Foundations",
        "scenario": "Storytelling: The Ladder of Abstraction 🪜",
        "text": "Effective communicators move smoothly up and down the {{c1::Ladder of Abstraction}}, shifting between high-level conceptual ideas and {{c2::concrete sensory details/examples}}.",
        "explanation": "Staying at the top of the ladder (e.g. 'efficiency', 'synergy') makes communication dry and ambiguous. Staying at the bottom (specific log lines) makes it narrow. Moving between both levels helps the listener understand both the 'why' (abstract) and the 'how' (concrete).",
        "usage": "Crucial for training sessions, product demonstrations, and strategic business writing.",
        "spanish": "Los comunicadores eficaces se mueven con fluidez hacia arriba y hacia abajo en la Escalera de Abstracción, cambiando entre ideas conceptuales de alto nivel y detalles/ejemplos sensoriales concretos.",
        "tags": ["storytelling", "communication", "clarity"]
    },
    {
        "deck": "Social_Skills::06_Storytelling_Foundations",
        "scenario": "Storytelling: Open Loops for Retaining Focus 🌀",
        "text": "An {{c1::Open Loop}} maintains audience engagement by introducing a mystery or unanswered question early in the story and {{c2::delaying the resolution}} until the very end.",
        "explanation": "Open loops leverage the Zeigarnik effect. The human brain dislikes incomplete narratives and experiences mild cognitive tension until the loop is closed, forcing the listener to remain focused.",
        "usage": "Effective for starting speeches, writing newsletters, or managing long corporate presentations.",
        "spanish": "Un bucle abierto mantiene el compromiso de la audiencia al introducir un misterio o una pregunta sin respuesta al principio de la historia y retrasar la resolución hasta el final.",
        "tags": ["storytelling", "open_loops", "retention"]
    },

    # 07_Conversational_Psychology
    {
        "deck": "Social_Skills::07_Conversational_Psychology",
        "scenario": "Psychology: The Zeigarnik Effect 🧠",
        "text": "The {{c1::Zeigarnik Effect}} is the cognitive bias where humans remember {{c2::incomplete or interrupted tasks/stories}} significantly better than completed ones.",
        "explanation": "In conversation and writing, leaving a story unresolved creates mental tension that keeps the listener's brain actively processing the information. Once the story is concluded, the cognitive load is released, and the memory begins to fade.",
        "usage": "Used to design cliffhangers in marketing campaigns, product demos, and narrative hooks.",
        "spanish": "El efecto Zeigarnik es el sesgo cognitivo por el cual los seres humanos recuerdan las tareas o historias incompletas o interrumpidas significativamente mejor que las completadas.",
        "tags": ["psychology", "zeigarnik", "attention"]
    },
    {
        "deck": "Social_Skills::07_Conversational_Psychology",
        "scenario": "Psychology: Status Play in Conversations 🎭",
        "text": "According to Keith Johnstone's Status Play theory, every conversational interaction involves a dynamic exchange where speakers adjust their verbal and physical cues to assert {{c1::high status}} or {{c2::low status}}.",
        "explanation": "Status is not social rank, but behavior. High-status behavior involves relaxed postures, steady eye contact, and slow speech. Low-status behavior involves fidgeting, speaking fast, and apologetic phrasing. Calibrating status prevents intimidating or boring the listener.",
        "usage": "Applied in job interviews, crisis management meetings, and negotiation scenarios.",
        "spanish": "Según la teoría del juego de estatus de Keith Johnstone, cada interacción conversacional implica un intercambio dinámico en el que los hablantes ajustan sus señales verbales y físicas para afirmar un estatus alto o bajo.",
        "tags": ["psychology", "status_play", "rapport"]
    },
    {
        "deck": "Social_Skills::07_Conversational_Psychology",
        "scenario": "Psychology: Calibrated Questions 🔍",
        "text": "To defuse defensiveness and force critical thinking, negotiation specialists use Calibrated Questions, which are open-ended questions beginning with {{c1::\"What\"}} or {{c2::\"How\"}}.",
        "explanation": "Questions starting with 'Why' trigger defensiveness because they sound accusatory. Calibrated questions (e.g. 'How can we solve this?' or 'What is holding us back?') shift the burden of solving the problem to the other party while keeping them collaborative.",
        "usage": "Essential for conflict resolution, client negotiations, and coaching sessions.",
        "spanish": "Para desactivar la actitud defensiva y forzar el pensamiento crítico, los especialistas en negociación utilizan preguntas calibradas, que son preguntas abiertas que comienzan con 'Qué' o 'Cómo'.",
        "tags": ["psychology", "negotiation", "questions"]
    },
    {
        "deck": "Social_Skills::07_Conversational_Psychology",
        "scenario": "Psychology: Designing your Origin Story 🚀",
        "text": "A compelling Origin Story structure is composed of three elements: the {{c1::Status Quo}}, the {{c2::Inciting Incident (Catalyst)}}, and the {{c3::Transformation/Lessons learned}}.",
        "explanation": "When introducing yourself, listing credentials is cold. Sharing your origin story—focusing on the struggle, the pivot point, and the resulting values—builds human connection and establishes immediate professional credibility.",
        "usage": "Used in introductory pitches, networking events, and personal brand building.",
        "spanish": "Una estructura convincente de historia de origen se compone de tres elementos: el statu quo, el incidente incitador (catalizador) y la transformación/lecciones aprendidas.",
        "tags": ["psychology", "origin_story", "introduction"]
    },
    {
        "deck": "Social_Skills::07_Conversational_Psychology",
        "scenario": "Psychology: Oxytocin and Empathy Chemistry 🧪",
        "text": "Sharing a genuine mistake or vulnerability triggers the release of {{c1::oxytocin}} in the listener's brain, which fosters {{c2::interpersonal trust and empathy}}.",
        "explanation": "Perfect, boastful stories trigger envy and distance. Showing relatable flaws signals safety and authenticity, which chemically prompts the listener's brain to form a social bond, making them highly receptive to your ideas.",
        "usage": "Used to rebuild customer relationships after service failures or during leadership updates.",
        "spanish": "Compartir una vulnerabilidad o un error genuino desencadena la liberación de oxitocina en el cerebro del oyente, lo que fomenta la empatía y la confianza interpersonal.",
        "tags": ["psychology", "oxytocin", "empathy"]
    },

    # 03_Presence
    {
        "deck": "Social_Skills::03_Presence",
        "scenario": "Presence: Judicial Pauses 🤫",
        "text": "A {{c1::Judicial Pause}} is a deliberate silence inserted {{c2::immediately after delivering a key point}} to allow the weight of the statement to settle.",
        "explanation": "Rushing to speak after a major revelation dilutes its impact. Pausing for 2-3 seconds gives the listener time to digest the meaning and signals confidence, as the speaker is comfortable holding the silence.",
        "usage": "Applied in public speaking, key meetings, and high-impact negotiations.",
        "spanish": "Una pausa enjuiciadora es un silencio deliberado introducido inmediatamente después de entregar un punto clave para permitir que el peso de la declaración se asiente.",
        "tags": ["presence", "vocal_control", "pauses"]
    },
    {
        "deck": "Social_Skills::03_Presence",
        "scenario": "Presence: Grounding Posture 🧍",
        "text": "To project absolute stability and eliminate anxious swaying, speakers use a {{c1::Grounding Posture}}, placing their feet shoulder-width apart and distributing weight {{c2::equally on both legs}}.",
        "explanation": "Fidgeting or pacing aimlessly signals nervousness. Grounding anchors the lower body, which naturally improves breathing capacity and allows the speaker to use deliberate, calm hand gestures.",
        "usage": "Critical for stage presentations, key pitches, and media interviews.",
        "spanish": "Para proyectar estabilidad absoluta y eliminar el balanceo ansioso, los oradores usan una postura de arraigo, colocando los pies al ancho de los hombros y distribuyendo el peso por igual en ambas piernas.",
        "tags": ["presence", "body_language", "grounding"]
    },
    {
        "deck": "Social_Skills::03_Presence",
        "scenario": "Presence: Selective Eye Contact 👀",
        "text": "In public speaking, instead of scanning the crowd, a presenter practices selective eye contact by holding gaze with {{c1::one specific person}} for the duration of {{c2::a single complete thought/sentence}}.",
        "explanation": "Scanning the room creates visual noise and looks anxious. Holding contact with one individual for 3-5 seconds creates a sense of direct conversation, which builds connection and naturally slows down the presenter's delivery.",
        "usage": "Recommended for large presentations, team updates, and boardrooms.",
        "spanish": "En el hablar en público, en lugar de escanear a la multitud, el presentador practica el contacto visual selectivo al sostener la mirada con una persona específica durante una frase completa.",
        "tags": ["presence", "eye_contact", "body_language"]
    },
    {
        "deck": "Social_Skills::03_Presence",
        "scenario": "Presence: The Triple Nod 🤝",
        "text": "The {{c1::Triple Nod}} is a soft-skills technique where you slowly nod three times while listening, which psychologically encourages the speaker to {{c2::elaborate and share deeper insights}}.",
        "explanation": "Nodding rapidly signals impatience ('hurry up'). Nodding slowly three times in succession signals active processing and validation. It shows you are engaged and prompts the speaker to expand, often revealing core concerns.",
        "usage": "A key active listening tool for user interviews, support containment, and team coaching.",
        "spanish": "El asentimiento triple es una técnica de habilidades blandas en la que asientes lentamente tres veces mientras escuchas, lo que alienta psicológicamente al hablante a profundizar y compartir más detalles.",
        "tags": ["presence", "active_listening", "body_language"]
    },
    {
        "deck": "Social_Skills::03_Presence",
        "scenario": "Presence: Framing Gestures 👐",
        "text": "To emphasize structure and boundary parameters, speakers use {{c1::Framing Gestures}}, placing their hands stable at chest-height as if holding an imaginary {{c2::box or boundary}}.",
        "explanation": "Broad, wild gestures signal excitement or lack of control. Framing gestures focus the audience's visual attention on a defined spatial boundary near the speaker's core, projecting authority and structured, logical thinking.",
        "usage": "Used when laying out business choices, security boundaries, or operational policies.",
        "spanish": "Para enfatizar la estructura y los límites, los oradores usan gestos de enmarcación, colocando sus manos estables a la altura del pecho como si sostuvieran una caja o límite imaginario.",
        "tags": ["presence", "gestures", "body_language"]
    },

    # 09_Advanced_Influence
    {
        "deck": "Social_Skills::09_Advanced_Influence",
        "scenario": "Influence: The \"Yes, And\" Principle 🎭",
        "text": "To deflect resistance and build collaborative momentum, the engineer adopts the improvisation rule {{c1::\"Yes, And...\"}}, which accepts the client's premise and {{c2::builds value on top of it}} instead of contradicting it.",
        "explanation": "Saying 'No, but...' triggers cognitive resistance. 'Yes, and...' doesn't mean agreeing to bad ideas; it means validating their reality (e.g. 'Yes, security is a bottleneck, and that is why we should integrate this automated tool') to move the conversation forward.",
        "usage": "Defusing customer objections, brain-storming sessions, and handling stakeholder push-back.",
        "spanish": "Para desviar la resistencia y crear un impulso colaborativo, el ingeniero adopta la regla de improvisación 'Sí, y...', que acepta la premisa del cliente y añade valor sobre ella en lugar de contradecirla.",
        "tags": ["influence", "improvisation", "collaboration"]
    },
    {
        "deck": "Social_Skills::09_Advanced_Influence",
        "scenario": "Influence: Nested Metaphors Loop 🌀",
        "text": "To embed complex concepts deeply into the listener's subconscious, the speaker uses Nested Metaphors, opening a {{c1::primary narrative}}, nesting a {{c2::secondary story}}, closing the secondary, and finally concluding the primary.",
        "explanation": "This technique (also called concentric loops) bypasses critical analytical resistance. While the listener's conscious mind focuses on tracking the transition between stories, the core message and lessons are absorbed and remembered more easily.",
        "usage": "Used in motivational speaking, advanced coaching, and complex technical trainings.",
        "spanish": "Para integrar conceptos complejos profundamente en el subconsciente del oyente, el orador utiliza metáforas anidadas, abriendo una narrativa principal, anidando una secundaria, cerrando la secundaria y finalmente concluyendo la principal.",
        "tags": ["influence", "nested_metaphors", "training"]
    },
    {
        "deck": "Social_Skills::09_Advanced_Influence",
        "scenario": "Influence: Narrative Inoculation 🛡️",
        "text": "To pre-emptively disarm a customer's objection, the advisor uses {{c1::Narrative Inoculation}} by raising the argument's weak points himself before the interlocutor can exploit them.",
        "explanation": "Borrowing from immunology, inoculation exposes the audience to a weakened form of the opposing argument. By calling out your own flaws first (e.g. 'You might think this migration is too slow...'), you build trust and control how that weakness is explained.",
        "usage": "Essential for sales pitches, technical architecture reviews, and public relations.",
        "spanish": "Para desamar preventivamente la objeción de un cliente, el asesor utiliza la inoculación narrativa al plantear él mismo los puntos débiles de su argumento antes de que el interlocutor pueda explotarlos.",
        "tags": ["influence", "persuasion", "objections"]
    },
    {
        "deck": "Social_Skills::09_Advanced_Influence",
        "scenario": "Influence: Strategic Story-Listening 👂",
        "text": "To align your proposal with the client's worldview, you perform Strategic Story-Listening, identifying the {{c1::core metaphors/analogies}} they use and returning your response using {{c2::that same mental map}}.",
        "explanation": "If a client views their company as a 'sports team', pitching options in terms of a 'military campaign' creates cognitive friction. Listening to their dominant metaphor and matching it (e.g. using sports vocabulary) dramatically increases rapport and adoption.",
        "usage": "Critical for high-value sales, consultant reviews, and executive alignment.",
        "spanish": "Para alinear su propuesta con la visión del cliente, realiza escucha narrativa estratégica, identificando las metáforas principales que usan y respondiendo con su mismo mapa mental.",
        "tags": ["influence", "active_listening", "alignment"]
    },
    {
        "deck": "Social_Skills::09_Advanced_Influence",
        "scenario": "Influence: Narrative Identity 🧬",
        "text": "To drive behavioral change, the leader uses Narrative Identity to help the listener re-evaluate how they see themselves, framing the change around {{c1::who they are (identity)}} rather than {{c2::what they must do (tasks)}}.",
        "explanation": "Telling someone 'You need to write tests' triggers pushback. Framing it as 'Because you are an engineer who cares about craftsmanship, writing tests is standard for you' anchors the behavior to their self-identity, which results in long-term compliance.",
        "usage": "Leadership development, change management, and team alignment.",
        "spanish": "Para impulsar el cambio de comportamiento, el líder utiliza la narrativa identitaria para ayudar al oyente a reevaluar cómo se ve a sí mismo, enmarcando el cambio en torno a quiénes son en lugar de qué deben hacer.",
        "tags": ["influence", "leadership", "identity"]
    }
]

# Avoid adding duplicates
existing_scenarios = {c["scenario"] for c in cards}
added_count = 0

for card in new_cards:
    if card["scenario"] not in existing_scenarios:
        cards.append(card)
        added_count += 1

with open(database_file, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"Successfully added {added_count} new cards. Total cards in database: {len(cards)}.")
