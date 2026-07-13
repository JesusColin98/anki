import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_cards = [
    # Social_Skills::04_Customer_Support_Excellence
    {
        "deck": "Social_Skills::04_Customer_Support_Excellence",
        "scenario": "Support Excellence: Empathic Alignment 💖",
        "text": "When handling a frustrated user, a support specialist uses {{c1::affective empathy}} to acknowledge their feelings and {{c2::cognitive empathy}} to understand the logical root of their issue.",
        "explanation": "Affective empathy connects emotionally (e.g., feeling their frustration), while cognitive empathy allows you to intellectually grasp their perspective and problem-solve without getting emotionally overwhelmed.",
        "usage": "Essential for balancing self-care with high-quality support in demanding helpdesk roles.",
        "spanish": "Al tratar con un usuario frustrado, un especialista en soporte utiliza la empatía afectiva para reconocer sus sentimientos y la empatía cognitiva para comprender la raíz lógica de su problema.",
        "tags": ["social_skills", "support_excellence", "empathy"]
    },
    {
        "deck": "Social_Skills::04_Customer_Support_Excellence",
        "scenario": "Support Excellence: De-escalation & Containment 🧯",
        "text": "To prevent an angry customer's issue from escalating, the agent must perform {{c1::de-escalation/containment}} by validating their frustration, taking immediate ownership, and outlining a clear path to resolution.",
        "explanation": "Containment involves managing the customer's emotional state early in the interaction so that logical problem-solving can occur. Validating feelings first reduces the customer's need to fight for attention.",
        "usage": "A critical skill when handling high-severity service outages or billing disputes.",
        "spanish": "Para evitar que el problema de un cliente enojado se intensifique, el agente debe realizar contención validando su frustración, asumiendo la responsabilidad inmediata y delineando un camino claro hacia la resolución.",
        "tags": ["social_skills", "support_excellence", "de_escalation"]
    },
    {
        "deck": "Social_Skills::04_Customer_Support_Excellence",
        "scenario": "Support Excellence: Active Listening 👂",
        "text": "Instead of formulating a response while the user is still speaking, a support professional practices {{c1::active listening}} by waiting, summarizing the issue in their own words, and asking clarifying questions.",
        "explanation": "Active listening ensures the customer feels heard and prevents misdiagnosis of the technical issue. Paraphrasing is the key tool here.",
        "usage": "Avoids premature assumptions and reduces average ticket resolution time.",
        "spanish": "En lugar de formular una respuesta mientras el usuario aún está hablando, un profesional de soporte practica la escucha activa esperando, resumiendo el problema con sus propias palabras y haciendo preguntas aclaratorias.",
        "tags": ["social_skills", "support_excellence", "active_listening"]
    },
    {
        "deck": "Social_Skills::04_Customer_Support_Excellence",
        "scenario": "Support Excellence: Boundary Setting 🚧",
        "text": "When dealing with abusive customers, a successful agent maintains professionalism while setting {{c1::firm boundaries}} by stating what actions they can take and politely requesting a respectful tone.",
        "explanation": "Setting boundaries protects the agent's mental health while keeping the focus on technical troubleshooting. It involves calling out unacceptable behavior calmly and objectively.",
        "usage": "Essential for handling toxic client interactions without losing composure or violating company policy.",
        "spanish": "Al tratar con clientes abusivos, un agente exitoso mantiene el profesionalismo al establecer límites firmes, indicando qué acciones puede tomar y solicitando cortésmente un tono respetuoso.",
        "tags": ["social_skills", "support_excellence", "boundaries"]
    },

    # Social_Skills::05_Call_Habits_and_Etiquette
    {
        "deck": "Social_Skills::05_Call_Habits_and_Etiquette",
        "scenario": "Call Etiquette: Setting the Agenda 📋",
        "text": "At the start of a call, the host establishes trust and structure by {{c1::setting a clear agenda}} and stating the expected outcome of the meeting.",
        "explanation": "Setting the agenda immediately defines the scope of the call, preventing participants from derailing the meeting with off-topic issues.",
        "usage": "A key habit to keep calls concise and productive.",
        "spanish": "Al inicio de una llamada, el anfitrión establece confianza y estructura al definir una agenda clara y declarar el resultado esperado de la reunión.",
        "tags": ["social_skills", "call_etiquette", "agenda"]
    },
    {
        "deck": "Social_Skills::05_Call_Habits_and_Etiquette",
        "scenario": "Call Etiquette: Managing Dead Air 🤫",
        "text": "During a technical support call, instead of leaving uncomfortable silence while looking up information, the agent should {{c1::narrate their actions}} to keep the customer engaged.",
        "explanation": "Narrating your actions (e.g., 'I am checking the server logs right now, this should take about 15 seconds') reduces customer anxiety and maintains connection during pauses.",
        "usage": "Prevents the customer from wondering if the call was dropped or if the agent is inactive.",
        "spanish": "Durante una llamada de soporte técnico, en lugar de dejar un silencio incómodo mientras busca información, el agente debe narrar sus acciones para mantener al cliente involucrado.",
        "tags": ["social_skills", "call_etiquette", "communication"]
    },
    {
        "deck": "Social_Skills::05_Call_Habits_and_Etiquette",
        "scenario": "Call Etiquette: Summarizing Next Steps 📝",
        "text": "To ensure accountability, every productive call must end by {{c1::summarizing next steps}}, specifying who is responsible for each action and by when.",
        "explanation": "Summarizing action items at the end of the call prevents misunderstandings and guarantees that decisions made translate into actual progress.",
        "usage": "The closing ritual of any high-performing support or business meeting.",
        "spanish": "Para garantizar la rendición de cuentas, toda llamada productiva debe finalizar resumiendo los siguientes pasos, especificando quién es responsable de cada acción y para cuándo.",
        "tags": ["social_skills", "call_etiquette", "productivity"]
    },
    {
        "deck": "Social_Skills::05_Call_Habits_and_Etiquette",
        "scenario": "Call Etiquette: Managing Call Duration ⏱️",
        "text": "To prevent call bloat, a support engineer uses {{c1::gentle redirection}} to guide off-topic customers back to the primary troubleshooting goal.",
        "explanation": "Gentle redirection involves validating the customer's tangent but immediately shifting the focus back to the core issue (e.g., 'That sounds interesting, but to make sure we fix your login issue, let's look at...').",
        "usage": "Keeps call handling times (AHT) within targets while maintaining high customer satisfaction.",
        "spanish": "Para evitar que la llamada se alargue innecesariamente, un ingeniero de soporte utiliza la redirección sutil para guiar a los clientes que se desvían del tema de regreso al objetivo principal de resolución de problemas.",
        "tags": ["social_skills", "call_etiquette", "time_management"]
    },

    # English::02_Professional::Support_Empathy_and_Containment
    {
        "deck": "English::02_Professional::Support_Empathy_and_Containment",
        "scenario": "Support English: Validating Frustration 🤝",
        "text": "When a customer is upset about an outage, you can say: \"I completely {{c1::understand how frustrating}} it must be to {{c2::have your workflow disrupted}}.\"",
        "explanation": "This phrase validates the customer's feelings and shows you understand the impact of the issue on their business, which immediately lowers tension.",
        "usage": "Pattern: <code>I understand how frustrating it must be to [action/situation]</code><ul><li><code>I understand how frustrating it must be to lose access during a launch.</code></li><li><code>I understand how frustrating it must be to wait for this update.</code></li></ul>",
        "spanish": "Cuando un cliente está molesto por una interrupción, puedes decir: \"Entiendo completamente lo frustrante que debe ser que se interrumpa tu flujo de trabajo\".",
        "tags": ["english_scenario", "support_english", "empathy"]
    },
    {
        "deck": "English::02_Professional::Support_Empathy_and_Containment",
        "scenario": "Support English: Taking Ownership 🛡️",
        "text": "To reassure a panicked client, use ownership language: \"I'm going to {{c1::take ownership of this issue}} and ensure we {{c2::get this sorted out for you}} as quickly as possible.\"",
        "explanation": "<strong>Take ownership</strong> means accepting personal responsibility for finding a solution. <strong>Get sorted out</strong> is a common idiom meaning to resolve or organize a problem.",
        "usage": "Pattern: <code>take ownership of [issue] / get [something] sorted out</code><ul><li><code>Our team will take ownership of the database migration.</code></li><li><code>Don't worry, we'll get this sorted out by the end of the day.</code></li></ul>",
        "spanish": "Para tranquilizar a un cliente en pánico, utiliza un lenguaje de propiedad: \"Voy a hacerme cargo de este problema y me aseguraré de resolverlo lo antes posible\".",
        "tags": ["english_scenario", "support_english", "de_escalation"]
    },
    {
        "deck": "English::02_Professional::Support_Empathy_and_Containment",
        "scenario": "Support English: Framing Bad News Positive 💡",
        "text": "Instead of saying \"We can't do that,\" frame it constructively: \"While that feature is {{c1::not currently supported}}, what we can do is {{c2::set up a workaround}} using our API.\"",
        "explanation": "<strong>Not currently supported</strong> is a professional way to say 'impossible' or 'no'. **Set up a workaround** means finding an alternative method to achieve the same result.",
        "usage": "Pattern: <code>While [request] is not currently supported, what we can do is [alternative]</code><ul><li><code>While custom domains are not currently supported, what we can do is redirect your URL.</code></li><li><code>Let's set up a workaround until the patch is released.</code></li></ul>",
        "spanish": "En lugar de decir \"No podemos hacer eso\", plantéalo de manera constructiva: \"Aunque esa función no es compatible actualmente, lo que podemos hacer es configurar una solución alternativa utilizando nuestra API\".",
        "tags": ["english_scenario", "support_english", "positive_framing"]
    },
    {
        "deck": "English::02_Professional::Support_Empathy_and_Containment",
        "scenario": "Support English: Expressing Appreciation 🙏",
        "text": "To transition from an apology to appreciation, say: \"Thank you for {{c1::bringing this to our attention}}, and I appreciate your {{c2::patience while we investigate}}.\"",
        "explanation": "<strong>Bring to attention</strong> is the standard way to acknowledge a bug report or complaint. Appreciating patience is much more positive and empowering than repeatedly saying 'sorry'.",
        "usage": "Pattern: <code>Thank you for bringing [issue] to our attention / appreciate your patience while we [action]</code><ul><li><code>Thank you for bringing this rendering bug to our attention.</code></li><li><code>We appreciate your patience while we deploy the fix.</code></li></ul>",
        "spanish": "Para pasar de una disculpa al agradecimiento, di: \"Gracias por llamar nuestra atención sobre esto, y agradezco su paciencia mientras investigamos\".",
        "tags": ["english_scenario", "support_english", "appreciation"]
    },

    # English::02_Professional::Handling_Objections
    {
        "deck": "English::02_Professional::Handling_Objections",
        "scenario": "Handling Objections: Acknowledging and Reframing 🔄",
        "text": "When a client objects to a price increase, you can say: \"I hear your {{c1::concerns regarding the cost}}; however, this new tier {{c2::delivers significant value by}} doubling your API rate limit.\"",
        "explanation": "Acknowledging the objection first shows respect, while 'delivers value by' steers the conversation toward benefits rather than expense.",
        "usage": "Pattern: <code>I hear your concerns regarding [topic]; however, this [solution] delivers value by [benefit]</code><ul><li><code>I hear your concerns regarding the timeline; however, this phase delivers value by securing your data early.</code></li><li><code>We believe this update delivers significant value by reducing server load.</code></li></ul>",
        "spanish": "Cuando un cliente se opone a un aumento de precio, puedes decir: \"Escucho sus inquietudes con respecto al costo; sin embargo, este nuevo nivel ofrece un valor significativo al duplicar su límite de velocidad de API\".",
        "tags": ["english_scenario", "handling_objections", "negotiation"]
    },
    {
        "deck": "English::02_Professional::Handling_Objections",
        "scenario": "Handling Objections: Proposing Alternatives 🔀",
        "text": "If a user rejects a solution, offer options: \"If that option doesn't {{c1::align with your objectives}}, we can {{c2::explore a phased roll-out}} instead.\"",
        "explanation": "<strong>Align with objectives</strong> means to match their goals. **Explore a phased roll-out** means to implement the solution in gradual steps rather than all at once.",
        "usage": "Pattern: <code>If [solution] doesn't align with your objectives, we can explore [alternative]</code><ul><li><code>If the standard plan doesn't align with your objectives, we can explore a custom contract.</code></li><li><code>Let's explore a phased roll-out of the security policy.</code></li></ul>",
        "spanish": "Si un usuario rechaza una solución, ofrece opciones: \"Si esa opción no se alinea con sus objetivos, podemos explorar una implementación gradual en su lugar\".",
        "tags": ["english_scenario", "handling_objections", "alternatives"]
    },
    {
        "deck": "English::02_Professional::Handling_Objections",
        "scenario": "Handling Objections: Clarifying Hesitation 🔍",
        "text": "To uncover the root of a client's hesitation: \"What is your {{c1::primary reservation about}} moving forward with this integration?\"",
        "explanation": "<strong>Primary reservation</strong> refers to the main doubt, worry, or objection holding someone back from making a decision.",
        "usage": "Pattern: <code>What is your primary reservation about [action]?</code><ul><li><code>What is your primary reservation about migrating to the cloud?</code></li><li><code>His primary reservation about the project was the tight deadline.</code></li></ul>",
        "spanish": "Para descubrir la raíz de la vacilación de un cliente: \"¿Cuál es su principal reserva sobre seguir adelante con esta integración?\"",
        "tags": ["english_scenario", "handling_objections", "clarifying"]
    },
    {
        "deck": "English::02_Professional::Handling_Objections",
        "scenario": "Handling Objections: Validating Competitor Claims 🤼",
        "text": "When a customer compares you to a competitor: \"I understand that [Competitor] has {{c1::a lower price point}}, but our platform provides {{c2::enterprise-grade security}} that is not offered elsewhere.\"",
        "explanation": "<strong>Lower price point</strong> is a professional euphemism for 'cheaper'. **Enterprise-grade** denotes high-quality, robust features suited for large, demanding organizations.",
        "usage": "Pattern: <code>understand [competitor] has a lower price point, but our [product] provides [advantage]</code><ul><li><code>I understand they have a lower price point, but our service provides 99.99% uptime.</code></li><li><code>We need enterprise-grade security to satisfy compliance requirements.</code></li></ul>",
        "spanish": "Cuando un cliente te compara con un competidor: \"Entiendo que [Competidor] tiene un precio más bajo, pero nuestra plataforma ofrece seguridad de nivel empresarial que no se ofrece en otros lugares\".",
        "tags": ["english_scenario", "handling_objections", "competitors"]
    },

    # English::02_Professional::Meeting_Efficiency
    {
        "deck": "English::02_Professional::Meeting_Efficiency",
        "scenario": "Meeting Efficiency: Parking Lot / Tabling Topics 🅿️",
        "text": "When a conversation goes off-track, you can say: \"In the interest of time, let's {{c1::park this topic}} and {{c2::circle back to it}} at the end of the meeting.\"",
        "explanation": "<strong>In the interest of time</strong> means to save time. **Park a topic** (or put it in the 'parking lot') means to temporarily postpone discussing it. **Circle back** means to return to a topic later.",
        "usage": "Pattern: <code>In the interest of time, let's park [topic] and circle back to it [time]</code><ul><li><code>In the interest of time, let's park the budget discussion and circle back to it on Friday.</code></li><li><code>I want to circle back to what you said about API keys.</code></li></ul>",
        "spanish": "Cuando una conversación se desvía, puedes decir: \"Por razones de tiempo, guardemos este tema en el tintero y volvamos a él al final de la reunión\".",
        "tags": ["english_scenario", "meeting_efficiency", "time_management"]
    },
    {
        "deck": "English::02_Professional::Meeting_Efficiency",
        "scenario": "Meeting Efficiency: Taking it Offline 📴",
        "text": "If a detailed discussion only concerns a few people: \"This seems to require a deeper dive, so let's {{c1::take this offline}} and let the rest of the team {{c2::get some time back}}.\"",
        "explanation": "<strong>Take this offline</strong> is an idiom meaning to discuss a topic privately outside of the current meeting. **Get some time back** is a polite way to end a meeting early or release people who are not needed.",
        "usage": "Pattern: <code>take this offline / get [amount of] time back</code><ul><li><code>Let's take the database schema discussion offline.</code></li><li><code>If we finish early, everyone gets 10 minutes back.</code></li></ul>",
        "spanish": "Si una discusión detallada solo concierne a unas pocas personas: \"Esto parece requerir un análisis más profundo, así que hablemos de esto fuera de línea y dejemos que el resto del equipo recupere algo de tiempo\".",
        "tags": ["english_scenario", "meeting_efficiency", "time_management"]
    },
    {
        "deck": "English::02_Professional::Meeting_Efficiency",
        "scenario": "Meeting Efficiency: Keeping it High-Level 🏔️",
        "text": "Let's {{c1::keep this discussion high-level}} today, as we only have 15 minutes left on the agenda.",
        "explanation": "<strong>Keep high-level</strong> means to focus on the big picture, summaries, and general strategies rather than getting caught up in minor details or technicalities.",
        "usage": "Pattern: <code>keep this [discussion/sync] high-level</code><ul><li><code>Let's keep this sync high-level and discuss implementation next week.</code></li><li><code>She kept the presentation high-level for the executives.</code></li></ul>",
        "spanish": "Para evitar empantanarse en los detalles: \"Mantengamos esta discusión a un nivel general hoy, ya que solo nos quedan 15 minutos en la agenda\".",
        "tags": ["english_scenario", "meeting_efficiency", "scope"]
    },
    {
        "deck": "English::02_Professional::Meeting_Efficiency",
        "scenario": "Meeting Efficiency: Staying Agenda-Driven 📋",
        "text": "I want to make sure we {{c1::stick to the agenda}} so we can {{c2::cover all the items}} we planned for today.",
        "explanation": "<strong>Stick to the agenda</strong> means to follow the pre-planned list of topics. **Cover items** means to discuss and resolve the topics.",
        "usage": "Pattern: <code>stick to the agenda / cover the items</code><ul><li><code>If we stick to the agenda, we will finish on time.</code></li><li><code>We have a lot of items to cover in today's standup.</code></li></ul>",
        "spanish": "Quiero asegurarme de que nos apeguemos a la agenda para que podamos cubrir todos los temas que planeamos para hoy.",
        "tags": ["english_scenario", "meeting_efficiency", "agenda"]
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
