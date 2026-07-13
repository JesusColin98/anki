import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_cards = [
    # 1. Workplace & Career
    {
        "deck": "English::02_Professional::Interview_Skills",
        "scenario": "Workplace: Job Interview 💼",
        "text": "During the interview, she explained: \"I {{c1::spearheaded the optimization}} of our CI/CD pipelines, which {{c2::streamlined our deployment cycle}} by 40%.\"",
        "explanation": "<strong>Spearhead</strong> is an active, high-impact verb meaning to lead an initiative. **Streamline** means to make a process more efficient by removing bottlenecks.",
        "usage": "Pattern: <code>spearhead the [action] of [system] / streamline [process]</code><ul><li><code>He spearheaded the migration of our legacy systems.</code></li><li><code>We need to streamline our support ticketing process.</code></li></ul>",
        "spanish": "Durante la entrevista, ella explicó: \"Lideré la optimización de nuestros pipelines de CI/CD, lo que simplificó nuestro ciclo de implementación en un 40%\".",
        "tags": ["workplace", "interview", "vocabulary"]
    },
    {
        "deck": "English::02_Professional::IT_Support",
        "scenario": "Workplace: Critical Infrastructure Fault 🖥️",
        "text": "The engineer reported: \"We are experiencing a major {{c1::infrastructure outage}} due to a {{c2::database bottleneck}}, and we are preparing a root cause analysis.\"",
        "explanation": "<strong>Outage</strong> means service downtime. **Bottleneck** refers to a point of congestion in a system that slows down performance. **Root cause analysis (RCA)** is the diagnostic process to find the source of the issue.",
        "usage": "Pattern: <code>experience an outage due to [cause] / conduct a root cause analysis</code><ul><li><code>The network outage was caused by a configuration error.</code></li><li><code>We conducted a root cause analysis to prevent future failures.</code></li></ul>",
        "spanish": "El ingeniero informó: \"Estamos experimentando una interrupción importante de la infraestructura debido a un cuello de botella en la base de datos, y estamos preparando un análisis de causa raíz\".",
        "tags": ["workplace", "it_support", "outage"]
    },
    {
        "deck": "English::02_Professional::Negotiations",
        "scenario": "Workplace: Salary & Contract Negotiation 📑",
        "text": "During the review, he negotiated: \"Based on the {{c1::market rate}} and my contributions, I'd like to adjust my {{c2::compensation package}} to include remote-work fringe benefits.\"",
        "explanation": "<strong>Market rate</strong> is the standard salary for a role. **Compensation package** includes base salary, bonuses, and benefits. **Fringe benefits** are extra benefits (like gym memberships or health insurance).",
        "usage": "Pattern: <code>negotiate a compensation package based on market rate / include fringe benefits</code><ul><li><code>Our company offers an attractive compensation package with great fringe benefits.</code></li><li><code>The offer is below the current market rate for senior developers.</code></li></ul>",
        "spanish": "Durante la revisión, negoció: \"Basándome en la tarifa del mercado y mis contribuciones, me gustaría ajustar mi paquete de compensación para incluir beneficios adicionales de trabajo remoto\".",
        "tags": ["workplace", "negotiation", "compensation"]
    },
    {
        "deck": "English::02_Professional::Giving_Feedback",
        "scenario": "Workplace: Constructive Feedback 📊",
        "text": "During the 1-on-1 meeting, the manager noted: \"While your code is robust, there is {{c1::room for improvement}} in your documentation. {{c2::Going forward}}, let's focus on adding README guides.\"",
        "explanation": "<strong>Room for improvement</strong> is a polite, constructive way to say that something needs development. **Going forward** is a transition phrase meaning 'in the future'.",
        "usage": "Pattern: <code>room for improvement in [area] / going forward, we should [action]</code><ul><li><code>There is room for improvement in our test coverage.</code></li><li><code>Going forward, all code must be reviewed by two peers.</code></li></ul>",
        "spanish": "Durante la reunión 1 a 1, el gerente señaló: \"Aunque tu código es robusto, hay margen de mejora en tu documentación. En el futuro, concentrémonos en agregar guías README\".",
        "tags": ["workplace", "feedback", "communication"]
    },
    {
        "deck": "English::02_Professional::Office_Meetings",
        "scenario": "Workplace: Quarterly Goals Sync ⏱️",
        "text": "During the planning sync, the director shared: \"Our {{c1::financial forecast}} projects new {{c2::revenue streams}} from our enterprise API licensing model.\"",
        "explanation": "<strong>Financial forecast</strong> is a projection of future financial performance. **Revenue streams** refer to different sources of income for a business.",
        "usage": "Pattern: <code>financial forecast projects [metric] / identify new revenue streams</code><ul><li><code>The financial forecast projects a 15% increase in sales.</code></li><li><code>We are exploring new revenue streams to diversify our income.</code></li></ul>",
        "spanish": "Durante la sincronización de planificación, el director compartió: \"Nuestro pronóstico financiero proyecta nuevas fuentes de ingresos a partir de nuestro modelo de licencia de API empresarial\".",
        "tags": ["workplace", "meetings", "financial"]
    },

    # 2. Shopping & Commerce
    {
        "deck": "English::01_Daily_Life::Supermarket",
        "scenario": "Commerce: Returning Defective Items 🛒",
        "text": "At the customer service counter, the customer requested: \"I'd like a {{c1::full refund}} for this tablet because it has a {{c2::faulty charging port}}.\"",
        "explanation": "<strong>Refund</strong> is the return of payment. **Faulty** means defective or not working correctly.",
        "usage": "Pattern: <code>request a refund for [item] / faulty [part]</code><ul><li><code>I need a full refund because the screen is cracked.</code></li><li><code>This laptop has a faulty battery that doesn't charge.</code></li></ul>",
        "spanish": "En el mostrador de servicio al cliente, el cliente solicitó: \"Me gustaría un reembolso completo por esta tableta porque tiene un puerto de carga defectuoso\".",
        "tags": ["commerce", "returns", "shopping"]
    },
    {
        "deck": "English::01_Daily_Life::Supermarket",
        "scenario": "Commerce: Informal Bargaining 🏷️",
        "text": "At the flea market, he bargained: \"Is that your {{c1::best price}}? If you {{c2::throw in the vintage watch}}, we have a deal.\"",
        "explanation": "<strong>Best price</strong> is the lowest price a seller is willing to accept. **Throw in** is a phrasal verb meaning to include something extra for free.",
        "usage": "Pattern: <code>throw in [item] / have a deal</code><ul><li><code>If you throw in free shipping, I'll buy it.</code></li><li><code>We have a deal if you lower the price by ten dollars.</code></li></ul>",
        "spanish": "En el mercado de pulgas, regateó: \"¿Es ese tu mejor precio? Si incluyes el reloj vintage, tenemos un trato\".",
        "tags": ["commerce", "bargaining", "informal"]
    },
    {
        "deck": "English::01_Daily_Life::Supermarket",
        "scenario": "Commerce: Comparing Device Specs 📱",
        "text": "When comparing laptops, he analyzed: \"There are clear {{c1::trade-offs}} in portability, but the developer version gives you the most {{c2::bang for the buck}}.\"",
        "explanation": "<strong>Trade-offs</strong> are compromises made when choosing between two conflicting features. **Bang for the buck** is an idiom meaning value for money spent.",
        "usage": "Pattern: <code>trade-offs between [feature] and [feature] / get the most bang for the buck</code><ul><li><code>There are always trade-offs between battery life and processing power.</code></li><li><code>This budget phone offers the best bang for the buck.</code></li></ul>",
        "spanish": "Al comparar computadoras portátiles, analizó: \"Hay compensaciones claras en la portabilidad, pero la versión para desarrolladores te ofrece la mejor relación calidad-precio\".",
        "tags": ["commerce", "specifications", "value"]
    },
    {
        "deck": "English::01_Daily_Life::Supermarket",
        "scenario": "Commerce: Disputing Bank Charges 💳",
        "text": "On the phone with the bank, she stated: \"I need to {{c1::dispute a double charge}} that appeared on my recent {{c2::billing cycle statement}}.\"",
        "explanation": "<strong>Dispute a charge</strong> is the formal request to investigate an incorrect transaction. **Billing cycle statement** is the monthly bank report.",
        "usage": "Pattern: <code>dispute a charge on [account/statement]</code><ul><li><code>You should dispute the charge immediately with your credit card company.</code></li><li><code>I check my billing cycle statement every month for errors.</code></li></ul>",
        "spanish": "Por teléfono con el banco, ella declaró: \"Necesito impugnar un cargo doble que apareció en el estado de cuenta de mi ciclo de facturación reciente\".",
        "tags": ["commerce", "banking", "dispute"]
    },
    {
        "deck": "English::01_Daily_Life::Supermarket",
        "scenario": "Commerce: Subscription Fine Print 📑",
        "text": "Before subscribing, he asked: \"Is there an {{c1::auto-renewal policy}}? I want to make sure I read the {{c2::fine print}} to avoid hidden fees.\"",
        "explanation": "<strong>Auto-renewal</strong> is the automatic extension of a subscription. **Fine print** refers to the small text in a contract containing crucial restrictions and rules.",
        "usage": "Pattern: <code>auto-renewal policy / read the fine print</code><ul><li><code>Always read the fine print before signing a software license.</code></li><li><code>The auto-renewal policy can be turned off in your account settings.</code></li></ul>",
        "spanish": "Antes de suscribirse, preguntó: \"¿Existe una política de renovación automática? Quiero asegurarme de leer la letra pequeña para evitar cargos ocultos\".",
        "tags": ["commerce", "subscription", "contract"]
    },

    # 3. Storytelling & Anecdotes
    {
        "deck": "English::04_Storytelling_and_Expression",
        "scenario": "Storytelling: Childhood Trip 🗺️",
        "text": "Looking back: \"I {{c1::vividly remember}} visiting the Andes; it was an {{c2::eye-opening experience}} that changed how I saw nature.\"",
        "explanation": "<strong>Vividly remember</strong> means to recall with clear, bright, and detailed memory. **Eye-opening experience** is an event that teaches you something surprising or changes your perspective.",
        "usage": "Pattern: <code>vividly remember [action/event] / eye-opening experience</code><ul><li><code>I vividly remember my first coding project.</code></li><li><code>Working in tech support was an eye-opening experience.</code></li></ul>",
        "spanish": "Mirando hacia atrás: \"Recuerdo vívidamente haber visitado los Andes; fue una experiencia reveladora que cambió mi forma de ver la naturaleza\".",
        "tags": ["storytelling", "childhood", "memories"]
    },
    {
        "deck": "English::04_Storytelling_and_Expression",
        "scenario": "Storytelling: Chaotic Workplace Day 🤯",
        "text": "Recalling his last job: \"I was {{c1::snowed under}} with tickets, and when the server crashed, I was at my {{c2::wit's end}}.\"",
        "explanation": "<strong>Snowed under</strong> is an idiom meaning overwhelmed with work. **At one's wit's end** is an idiom meaning completely stressed out and not knowing what to do next.",
        "usage": "Pattern: <code>be snowed under with [work] / at my wit's end</code><ul><li><code>I'm completely snowed under with homework this semester.</code></li><li><code>I was at my wit's end trying to solve the connection bug.</code></li></ul>",
        "spanish": "Recordando su último trabajo: \"Estaba inundado de tickets, y cuando el servidor se cayó, estaba al borde de la locura (no sabía qué hacer)\".",
        "tags": ["storytelling", "idioms", "stress"]
    },
    {
        "deck": "English::04_Storytelling_and_Expression",
        "scenario": "Storytelling: Meeting a Close Friend 🤝",
        "text": "Telling the story: \"We crossed paths {{c1::out of the blue}} in Berlin, and we {{c2::hit it off}} immediately.\"",
        "explanation": "<strong>Out of the blue</strong> is an idiom meaning completely unexpected. **Hit it off** is a phrasal verb meaning to quickly become friendly or connect with someone.",
        "usage": "Pattern: <code>cross paths out of the blue / hit it off with [someone]</code><ul><li><code>I ran into my former colleague out of the blue.</code></li><li><code>We hit it off during our first meeting at the conference.</code></li></ul>",
        "spanish": "Contando la historia: \"Nos cruzamos por casualidad (de la nada) en Berlín, y congeniamos de inmediato\".",
        "tags": ["storytelling", "relationship", "friendship"]
    },
    {
        "deck": "English::04_Storytelling_and_Expression",
        "scenario": "Storytelling: Minor Health Accident 🏥",
        "text": "Relating the emergency: \"I got a {{c1::minor gash}} on my arm, but the doctor bandaged it and issued a {{c2::medical discharge}} within an hour.\"",
        "explanation": "<strong>Gash</strong> is a long, deep cut or wound in the skin. **Medical discharge** is the official release of a patient from medical care.",
        "usage": "Pattern: <code>gash on [body part] / receive a medical discharge</code><ul><li><code>He had a deep gash on his knee after falling.</code></li><li><code>The hospital prepared his medical discharge papers.</code></li></ul>",
        "spanish": "Relatando la emergencia: \"Me hice un corte menor en el brazo, pero el médico lo vendó y emitió un alta médica en una hora\".",
        "tags": ["storytelling", "health", "accident"]
    },
    {
        "deck": "English::04_Storytelling_and_Expression",
        "scenario": "Storytelling: Learning from Failure 💡",
        "text": "Reflecting on the project: \"In {{c1::hindsight}}, the failed launch was a blessing in disguise because our {{c2::key takeaway}} was the need for automated tests.\"",
        "explanation": "<strong>In hindsight</strong> means looking back at an event in the past. **Blessing in disguise** is an idiom meaning something bad that turns out to have good results. **Takeaway** is the key lesson learned.",
        "usage": "Pattern: <code>in hindsight, [situation] was a blessing in disguise / key takeaway from [event]</code><ul><li><code>In hindsight, losing that client helped us focus on better partners.</code></li><li><code>The key takeaway from the security audit was to rotate keys immediately.</code></li></ul>",
        "spanish": "Reflexionando sobre el proyecto: \"En retrospectiva, el lanzamiento fallido fue una bendición disfrazada porque nuestro principal aprendizaje fue la necesidad de pruebas automatizadas\".",
        "tags": ["storytelling", "lessons", "reflection"]
    },

    # 4. Home & Lifestyle
    {
        "deck": "English::01_Daily_Life::Home_Logistics",
        "scenario": "Lifestyle: Humidity Protection 🏠",
        "text": "Explaining to the landlord: \"The basement has accumulated {{c1::mold and mildew}} due to the high {{c2::moisture levels}}, so we need a dehumidifier.\"",
        "explanation": "<strong>Mold and mildew</strong> refer to fungal growths caused by dampness. **Moisture** refers to wetness or condensation in the air.",
        "usage": "Pattern: <code>accumulate mold due to high moisture / run a dehumidifier</code><ul><li><code>High moisture levels in the bathroom will cause mold and mildew.</code></li><li><code>We bought a dehumidifier to keep the basement dry.</code></li></ul>",
        "spanish": "Explicándole al propietario: \"El sótano ha acumulado moho y humedad debido a los altos niveles de humedad, por lo que necesitamos un deshumidificador\".",
        "tags": ["lifestyle", "home_maintenance", "humidity"]
    },
    {
        "deck": "English::01_Daily_Life::Home_Logistics",
        "scenario": "Lifestyle: Troubleshooting Smart Home Sync 🖥️",
        "text": "Troubleshooting the setup: \"The smart lock has a {{c1::sync issue}} with the hub, so the door sensor doesn't {{c2::trigger the security routine}}.\"",
        "explanation": "<strong>Sync issue</strong> refers to synchronization failure. **Trigger a routine** means to automatically start a sequence of pre-programmed actions.",
        "usage": "Pattern: <code>have a sync issue / trigger a routine based on [event]</code><ul><li><code>My phone is having a sync issue with the server.</code></li><li><code>Connecting the sensor will trigger the alarm routine.</code></li></ul>",
        "spanish": "Resolviendo problemas de la configuración: \"La cerradura inteligente tiene un problema de sincronización con el concentrador, por lo que el sensor de la puerta no activa la rutina de seguridad\".",
        "tags": ["lifestyle", "smart_home", "troubleshooting"]
    },
    {
        "deck": "English::01_Daily_Life::Home_Logistics",
        "scenario": "Lifestyle: Moving House Logistics 📦",
        "text": "Discussing the rent: \"We need to pay the first month's utilities and the {{c1::security deposit}} before we can inspect the {{c2::floor plan}}.\"",
        "explanation": "<strong>Security deposit</strong> is a sum of money paid in advance to protect the landlord against damage. **Floor plan** is the scale diagram showing room layouts.",
        "usage": "Pattern: <code>pay a security deposit / check the floor plan</code><ul><li><code>The landlord returned our security deposit when we moved out.</code></li><li><code>Let's study the floor plan to decide where to put the sofa.</code></li></ul>",
        "spanish": "Discutiendo el alquiler: \"Debemos pagar los servicios del primer mes y el depósito de seguridad antes de poder inspeccionar el plano de distribución de la casa\".",
        "tags": ["lifestyle", "moving", "renting"]
    },
    {
        "deck": "English::01_Daily_Life::Home_Logistics",
        "scenario": "Lifestyle: Espresso Extraction Barista ☕",
        "text": "Instructing the barista: \"If your {{c1::grind size}} is too coarse, it causes {{c2::channeling}}, resulting in a watery crema.\"",
        "explanation": "<strong>Grind size</strong> determines the speed of water flow. **Channeling** occurs when water finds paths of least resistance through the coffee puck instead of extracting evenly.",
        "usage": "Pattern: <code>adjust the grind size / prevent channeling during extraction</code><ul><li><code>If the grind size is too fine, the espresso will extract too slowly.</code></li><li><code>Tamping the coffee evenly prevents channeling.</code></li></ul>",
        "spanish": "Instruyendo al barista: \"Si el tamaño de la molienda es demasiado grueso, causa canalización, lo que resulta en una crema aguada\".",
        "tags": ["lifestyle", "coffee", "barismo"]
    },
    {
        "deck": "English::01_Daily_Life::Home_Logistics",
        "scenario": "Lifestyle: Designing Board Game Rules 🎲",
        "text": "Explaining the game: \"This is a {{c1::turn-based game}} with specific card mechanics, including a roll of dice to resolve any {{c2::tie-breaker}}.\"",
        "explanation": "<strong>Turn-based</strong> denotes a gameplay mechanic where players take turns. **Tie-breaker** is the rule or action that determines a winner when scores are equal.",
        "usage": "Pattern: <code>turn-based game / resolve a tie-breaker</code><ul><li><code>Civilization is a famous turn-based strategy game.</code></li><li><code>The team won the match in a sudden-death tie-breaker.</code></li></ul>",
        "spanish": "Explicando el juego: \"Este es un juego por turnos con mecánicas de cartas específicas, que incluye un lanzamiento de dados para resolver cualquier desempate\".",
        "tags": ["lifestyle", "games", "rules"]
    },

    # 5. Socializing & Leisure
    {
        "deck": "English::03_Socializing::General",
        "scenario": "Socializing: Card Game Rules Complex 🃏",
        "text": "Explaining the game: \"You must follow the {{c1::turn order}}, and all spells placed on the {{c2::stack resolve in reverse order}} of play.\"",
        "explanation": "<strong>Turn order</strong> is the sequence in which players act. **Stack** is a programming/game term where the last card played resolves first (Last-In, First-Out).",
        "usage": "Pattern: <code>follow the turn order / resolve on the stack</code><ul><li><code>Please wait for your turn in the turn order.</code></li><li><code>His counter-spell resolves first because it's on top of the stack.</code></li></ul>",
        "spanish": "Explicando el juego: \"Debes seguir el orden de los turnos, y todos los hechizos colocados en la pila se resuelven en orden inverso al de juego\".",
        "tags": ["socializing", "games", "card_games"]
    },
    {
        "deck": "English::03_Socializing::General",
        "scenario": "Socializing: Football Tactical Debate ⚽",
        "text": "Analyzing the match: \"Our defense kept a {{c1::clean sheet}}, but we failed to capitalize on the {{c2::counter-attack}} opportunities.\"",
        "explanation": "<strong>Clean sheet</strong> is a sports idiom meaning the opponent scored zero goals. **Counter-attack** refers to an immediate, fast attack launched in response to an opponent's offensive move.",
        "usage": "Pattern: <code>keep a clean sheet / launch a counter-attack</code><ul><li><code>The goalkeeper made three saves to keep a clean sheet.</code></li><li><code>We scored the winning goal during a rapid counter-attack.</code></li></ul>",
        "spanish": "Analizando el partido: \"Nuestra defensa mantuvo la portería a cero, pero no logramos capitalizar las oportunidades de contraataque\".",
        "tags": ["socializing", "sports", "football"]
    },
    {
        "deck": "English::03_Socializing::General",
        "scenario": "Socializing: Sci-fi Lore Analysis 🚀",
        "text": "Reviewing the saga: \"The trilogy features incredible {{c1::world-building}}, but the main protagonist's {{c2::character arc}} felt rushed.\"",
        "explanation": "<strong>World-building</strong> is the process of constructing an imaginary, detailed fictional world. **Character arc** is the developmental journey of a character over the course of a story.",
        "usage": "Pattern: <code>immersive world-building / character arc development</code><ul><li><code>Tolkien's novels are famous for their detailed world-building.</code></li><li><code>Her character arc shows a transition from villain to hero.</code></li></ul>",
        "spanish": "Revisando la saga: \"La trilogía presenta una construcción de mundo increíble, pero el arco de personaje del protagonista principal se sintió apresurado\".",
        "tags": ["socializing", "movies", "lore"]
    },
    {
        "deck": "English::03_Socializing::General",
        "scenario": "Socializing: Rejecting Invitations Politely ✉️",
        "text": "Declining the invite: \"I'd love to go, but I'm completely {{c1::swamped with work}} this week, so I'll have to {{c2::take a rain check}}.\"",
        "explanation": "<strong>Swamped with work</strong> means extremely busy. **Take a rain check** is an idiom meaning to politely decline an invitation now but suggest rescheduling for a later date.",
        "usage": "Pattern: <code>be swamped with [tasks] / take a rain check on [event]</code><ul><li><code>I'm completely swamped with work before the release.</code></li><li><code>Can I take a rain check on lunch today? I have a client meeting.</code></li></ul>",
        "spanish": "Rechazando la invitación: \"Me encantaría ir, pero estoy completamente abrumado de trabajo esta semana, así que tendré que dejarlo para otra ocasión\".",
        "tags": ["socializing", "polite_decline", "idioms"]
    },
    {
        "deck": "English::03_Socializing::General",
        "scenario": "Socializing: Consoling Grieving Friend 💖",
        "text": "Comforting the colleague: \"I can't imagine {{c1::what you're going through}}, but please know you can always {{c2::lean on me}} for support.\"",
        "explanation": "<strong>What you're going through</strong> acknowledges their unique pain. **Lean on me** is a comforting idiom meaning to rely on someone for emotional support.",
        "usage": "Pattern: <code>cannot imagine what [someone] is going through / lean on [someone] during [crisis]</code><ul><li><code>I am here for you, I cannot imagine what you're going through.</code></li><li><code>You can lean on me for help with your tasks this week.</code></li></ul>",
        "spanish": "Consolando al colega: \"No puedo imaginar por lo que estás pasando, pero por favor sabe que siempre puedes apoyarte en mí para recibir ayuda\".",
        "tags": ["socializing", "empathy", "comforting"]
    },

    # 6. Intellectual & Academic
    {
        "deck": "English::05_Academic_and_Philosophical",
        "scenario": "Academic: Philosophy Statecraft 📚",
        "text": "Discussing Machiavelli: \"His lectures focus on the harsh realities of {{c1::statecraft}} and the complex {{c2::power dynamics}} between rulers and citizens.\"",
        "explanation": "<strong>Statecraft</strong> refers to the art of government and leadership. **Power dynamics** refer to how power is negotiated and shared within relationships or society.",
        "usage": "Pattern: <code>the study of statecraft / analyze power dynamics</code><ul><li><code>Machiavelli's The Prince is a classic treatise on statecraft.</code></li><li><code>The team analyzed the power dynamics within the organization.</code></li></ul>",
        "spanish": "Discutiendo a Maquiavelo: \"Sus conferencias se centran en las duras realidades del arte de gobernar y la compleja dinámica de poder entre gobernantes y ciudadanos\".",
        "tags": ["academic", "philosophy", "statecraft"]
    },
    {
        "deck": "English::05_Academic_and_Philosophical",
        "scenario": "Academic: Defending Thesis Methodology 🎓",
        "text": "Defending the thesis: \"We gathered {{c1::qualitative data}} from a small {{c2::sample size}} to establish a theoretical framework.\"",
        "explanation": "<strong>Qualitative data</strong> is non-numerical descriptive data (e.g. interviews). **Sample size** is the number of participants/elements in a study.",
        "usage": "Pattern: <code>gather qualitative data from a sample size of [number]</code><ul><li><code>We gathered qualitative data through participant interviews.</code></li><li><code>The small sample size limits the generalization of the study.</code></li></ul>",
        "spanish": "Defendiendo la tesis: \"Reunimos datos cualitativos de una muestra pequeña para establecer un marco teórico\".",
        "tags": ["academic", "thesis_defense", "methodology"]
    },
    {
        "deck": "English::05_Academic_and_Philosophical",
        "scenario": "Academic: AI Deployment Ethics 🤖",
        "text": "Debating the tech: \"The rapid deployment of deep {{c1::neural networks}} raises concerns about algorithmic bias and {{c2::data privacy violations}}.\"",
        "explanation": "<strong>Neural networks</strong> refer to machine learning models inspired by biological brain architectures. **Data privacy violations** involve unauthorized collection or exposure of user information.",
        "usage": "Pattern: <code>raise concerns about algorithmic bias / verify data privacy compliance</code><ul><li><code>We trained deep neural networks for image classification.</code></li><li><code>Data privacy violations can lead to severe legal penalties.</code></li></ul>",
        "spanish": "Debatiendo sobre la tecnología: \"La rápida implementación de redes neuronales profundas plantea preocupaciones sobre el sesgo algorítmico y las violaciones de la privacidad de los datos\".",
        "tags": ["academic", "ai_ethics", "technology"]
    },
    {
        "deck": "English::05_Academic_and_Philosophical",
        "scenario": "Academic: Mass Media Agenda-Setting 📣",
        "text": "Analyzing media: \"Social algorithms create an {{c1::echo chamber}} effect that amplifies {{c2::sensationalism}} and polarizes public opinion.\"",
        "explanation": "<strong>Echo chamber</strong> is a metaphorical description of an environment where a person only encounters information that reflects and reinforces their own beliefs. **Sensationalism** is the use of exciting or shocking stories to provoke public interest.",
        "usage": "Pattern: <code>create an echo chamber / amplify sensationalism in media</code><ul><li><code>Social media feeds often create an echo chamber for users.</code></li><li><code>Sensationalism is commonly used to drive clicks and ad revenue.</code></li></ul>",
        "spanish": "Analizando los medios: \"Los algoritmos sociales crean un efecto de cámara de eco que amplifica el sensacionalismo y polariza la opinión pública\".",
        "tags": ["academic", "media_studies", "sociology"]
    },
    {
        "deck": "English::05_Academic_and_Philosophical",
        "scenario": "Academic: Comparing Abstract Currents 🧠",
        "text": "In the comparison: \"We must analyze the {{c1::nuance}} between these philosophies instead of reducing them to a simple {{c2::dichotomy}}.\"",
        "explanation": "<strong>Nuance</strong> is a subtle difference in meaning, expression, or opinion. **Dichotomy** is a division or contrast between two things that are represented as being opposed or entirely different.",
        "usage": "Pattern: <code>analyze the nuance / reduce [topic] to a simple dichotomy</code><ul><li><code>Understanding the nuance of the contract is essential.</code></li><li><code>The debate simplifies the issue into a false dichotomy.</code></li></ul>",
        "spanish": "En la comparación: \"Debemos analizar los matices entre estas filosofías en lugar de reducirlas a una simple dicotomía\".",
        "tags": ["academic", "philosophy", "comparison"]
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
