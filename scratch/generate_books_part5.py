import json
import os
from generate_books_part1 import save_deck

# ==================== 10_Fanatical_Prospecting (20 cards) ====================
fanatical_prospecting = [
    {
        "scenario": "Fanatical Prospecting: The 30-Day Rule 📞",
        "text": "The {{c1::30-Day Rule}} in prospecting states that the prospecting you do in the next 30 days will pay off over the next 90 days.",
        "explanation": "If you stop prospecting today, your sales pipeline will go empty in 90 days. Sales is a compounding game.",
        "spanish": "La Regla de los 30 Días en la prospección establece que la prospección que realices en los próximos 30 días dará frutos en los siguientes 90 días.",
        "tags": ["books_path", "sales", "prospecting"]
    },
    {
        "scenario": "Fanatical Prospecting: Law of Replacement 📞",
        "text": "The {{c1::Law of Replacement}} states that you must constantly replace opportunities in your pipeline at a rate equal to or greater than your closing ratio.",
        "explanation": "If your closing ratio is 10%, and you close 1 opportunity, you must add 10 new opportunities to maintain pipeline volume.",
        "spanish": "La Ley de Reemplazo establece que debes reemplazar constantemente las oportunidades en tu cartera a un ritmo igual o mayor que tu tasa de cierre.",
        "tags": ["books_path", "sales", "pipeline"]
    },
    {
        "scenario": "Fanatical Prospecting: The 3 Rules of Prospecting 📞",
        "text": "The first rule of prospecting is that you must be {{c1::disciplined}}—carving out time every single day for prospecting activities without exception.",
        "explanation": "Prospecting is often avoided because it involves rejection. Daily discipline prevents pipeline dry spells.",
        "spanish": "La primera regla de la prospección es que debes ser disciplinado: reservar tiempo todos los días para prospectar.",
        "tags": ["books_path", "sales", "prospecting"]
    },
    {
        "scenario": "Fanatical Prospecting: Prospecting Channels 📞",
        "text": "Fanatical prospectors utilize a {{c1::balanced approach}}—combining telephone, email, social selling, and in-person networking rather than relying on a single channel.",
        "explanation": "Using only one channel limits your reach. Different prospects prefer different channels.",
        "spanish": "Los prospectores fanáticos utilizan un enfoque equilibrado, combinando teléfono, correo electrónico, venta social y redes.",
        "tags": ["books_path", "sales", "prospecting"]
    },
    {
        "scenario": "Fanatical Prospecting: The Telephone 📞",
        "text": "Burkeman argues that the {{c1::telephone}} remains the most effective tool for booking appointments and qualifying prospects quickly.",
        "explanation": "The phone is immediate. Email can be ignored, but a phone call requires a real-time response.",
        "spanish": "Jeb Blount sostiene que el teléfono sigue siendo la herramienta más eficaz para reservar citas y calificar prospectos rápidamente.",
        "tags": ["books_path", "sales", "prospecting"]
    },
    {
        "scenario": "Fanatical Prospecting: Five-Step Telephone Framework 📞",
        "text": "The 5-step telephone prospecting framework consists of: 1. Get attention, 2. Identify yourself, 3. Give a {{c1::reason for the call}}, 4. Ask for the appointment, and 5. Handle objections.",
        "explanation": "Keep calls under 2 minutes. The goal of the prospecting call is to book the meeting, not to sell the product.",
        "spanish": "El marco telefónico de 5 pasos: captar atención, identificarse, dar una razón de la llamada, pedir la cita y manejar objeciones.",
        "tags": ["books_path", "sales", "prospecting"]
    },
    {
        "scenario": "Fanatical Prospecting: Reason for Call 📞",
        "text": "When giving a reason for your call, you must focus on the {{c1::prospect's business value}} rather than your product features.",
        "explanation": "Prospects don't care about your company; they care about their own problems and how you can solve them.",
        "usage": "Say: 'The reason I'm calling is to share a framework that helped Company X reduce server costs by 30%.'",
        "spanish": "Al dar la razón de tu llamada, debes enfocarte en el valor comercial para el cliente en lugar de las características del producto.",
        "tags": ["books_path", "sales", "communication"]
    },
    {
        "scenario": "Fanatical Prospecting: Golden Hour 📞",
        "text": "The {{c1::Golden Hour}} is a blocked period of time dedicated exclusively to cold-calling and emailing, with zero internal distractions or meetings.",
        "explanation": "Protect this hour fiercely. Do not answer internal emails or do admin work during this time.",
        "spanish": "La Hora de Oro (Golden Hour) es un bloque de tiempo dedicado exclusivamente a llamadas en frío y correos, sin distracciones.",
        "tags": ["books_path", "sales", "time_management"]
    },
    {
        "scenario": "Fanatical Prospecting: Rule of 30 📞",
        "text": "The Rule of 30 states that you must make at least {{c1::30 calls}} or outreach attempts during a single prospecting block to build momentum.",
        "explanation": "Making only 2-3 calls results in high anxiety and low flow. Batching calls makes handling rejection easier.",
        "spanish": "La Regla de los 30 establece que debes hacer al menos 30 llamadas o intentos de contacto durante un bloque de prospección.",
        "tags": ["books_path", "sales", "prospecting"]
    },
    {
        "scenario": "Fanatical Prospecting: Email Prospecting 📞",
        "text": "Effective prospecting emails must be short, personalized, and have a {{c1::single, clear call to action}} (CTA) like requesting a 10-minute call.",
        "explanation": "If your email is a wall of text or has multiple links, the prospect will delete it. Keep it under 150 words.",
        "spanish": "Los correos electrónicos de prospección eficaces deben ser cortos, personalizados y tener una única llamada a la acción clara.",
        "tags": ["books_path", "sales", "email"]
    },
    {
        "scenario": "Fanatical Prospecting: Social Selling 📞",
        "text": "Social selling is not about closing deals online; it is about building a {{c1::personal brand}} and initiating conversations with target prospects.",
        "explanation": "Use LinkedIn to share insights, engage with target prospects' posts, and establish authority.",
        "spanish": "La venta social (Social Selling) no se trata de cerrar acuerdos en línea, sino de construir una marca personal.",
        "tags": ["books_path", "sales", "linkedin"]
    },
    {
        "scenario": "Fanatical Prospecting: Relentless Execution 📞",
        "text": "The hallmark of a fanatical prospector is {{c1::relentless execution}}—they prospect when they don't feel like it, and when they are already hitting quota.",
        "explanation": "Success breeds complacency. Prospecting during good times prevents the 'sales roller coaster'.",
        "spanish": "La marca de un prospector fantástico es la ejecución implacable: prospectar incluso cuando ya están alcanzando la cuota.",
        "tags": ["books_path", "sales", "prospecting"]
    },
    {
        "scenario": "Fanatical Prospecting: Gatekeeper 📞",
        "text": "To get past the {{c1::gatekeeper}} (assistant or receptionist), treat them with respect, build trust, and ask for their help navigating the organization.",
        "explanation": "Treating gatekeepers poorly guarantees you will never talk to the decision-maker. They are allies, not obstacles.",
        "spanish": "Para superar al intermediario (gatekeeper), trátalo con respeto, genera confianza y pide su ayuda.",
        "tags": ["books_path", "sales", "communication"]
    },
    {
        "scenario": "Fanatical Prospecting: Qualify 📞",
        "text": "You must ruthlessly {{c1::qualify}} prospects during early outreach to avoid wasting time on accounts that cannot buy or do not fit your profile.",
        "explanation": "A large pipeline of bad leads is a waste of energy. Focus only on high-value targets.",
        "spanish": "Debes calificar despiadadamente a los prospectos durante los primeros contactos para evitar perder el tiempo.",
        "tags": ["books_path", "sales", "pipeline"]
    },
    {
        "scenario": "Fanatical Prospecting: Sales Pipeline 📞",
        "text": "A healthy sales pipeline should be shaped like a {{c1::funnel}}, with a broad mouth of new leads and a steady flow moving towards closing.",
        "explanation": "If your pipeline is a cylinder (few leads, long delays), your sales results will be erratic.",
        "spanish": "Una cartera de ventas saludable debe tener forma de embudo, con una boca amplia de nuevos leads.",
        "tags": ["books_path", "sales", "pipeline"]
    },
    {
        "scenario": "Fanatical Prospecting: Refusal Resilience 📞",
        "text": "The greatest barrier to prospecting is the fear of {{c1::rejection}}, which is a biological response in the brain that equates social exclusion with physical danger.",
        "explanation": "Understanding that rejection is not personal helps build the resilience needed to keep calling.",
        "spanish": "La mayor barrera para la prospección es el miedo al rechazo, una respuesta biológica del cerebro.",
        "tags": ["books_path", "sales", "psychology"]
    },
    {
        "scenario": "Fanatical Prospecting: Target Lists 📞",
        "text": "Before starting a prospecting block, prepare your {{c1::target lists}} in advance so you don't waste calling time on research.",
        "explanation": "Researching while calling breaks flow and is a form of active procrastination.",
        "spanish": "Antes de comenzar un bloque de prospección, prepara tus listas de objetivos con anticipación.",
        "tags": ["books_path", "sales", "planning"]
    },
    {
        "scenario": "Fanatical Prospecting: Objective of Call 📞",
        "text": "The primary objective of a prospecting call is to {{c1::sell the meeting}}, not the product.",
        "explanation": "If you try to explain features or negotiate price on a cold call, the prospect will hang up. Keep the focus on securing the calendar slot.",
        "spanish": "El objetivo principal de una llamada de prospección es vender la reunión, no el producto.",
        "tags": ["books_path", "sales", "prospecting"]
    },
    {
        "scenario": "Fanatical Prospecting: Scripting 📞",
        "text": "Use a {{c1::scripted framework}} rather than reading a rigid script word-for-word, allowing you to sound natural and adapt to the conversation.",
        "explanation": "Rigid scripts sound robotic. A framework keeps you on track while allowing authentic conversation.",
        "spanish": "Utiliza un marco guionizado (scripted framework) en lugar de leer un guion rígido palabra por palabra.",
        "tags": ["books_path", "sales", "communication"]
    },
    {
        "scenario": "Fanatical Prospecting: The Law of Averages 📞",
        "text": "The {{c1::Law of Averages}} states that if you repeat a prospecting behavior often enough, your closing ratio will stabilize and yield predictable results.",
        "explanation": "Sales is a numbers game. Trust the numbers and execute the daily routine.",
        "spanish": "La Ley de los Promedios establece que si repites una conducta de prospección con frecuencia, tus resultados serán predecibles.",
        "tags": ["books_path", "sales", "prospecting"]
    }
]

# ==================== 11_Gap_Selling (20 cards) ====================
gap_selling = [
    {
        "scenario": "Gap Selling: The Gap 📈",
        "text": "The core concept of Gap Selling is the **Gap**—the distance between the prospect's {{c1::Current State}} and their desired {{c2::Future State}}.",
        "explanation": "The size of the sale is determined by the size of the gap. If there is no gap, there is no value, and no sale will occur.",
        "spanish": "El concepto central de Gap Selling es la Brecha (Gap): la distancia entre el Estado Actual y el Estado Futuro deseado.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Current State 📈",
        "text": "To map the **Current State**, you must discover the prospect's facts, environment, problems, impact, and the {{c1::root cause}} of their problems.",
        "explanation": "Do not start pitching until you completely understand the current situation. Discovery is the most important part of sales.",
        "spanish": "Para mapear el Estado Actual, debes descubrir los hechos, el entorno, los problemas, el impacto y la causa raíz.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Future State 📈",
        "text": "The **Future State** represents the prospect's desired environment, outcomes, and the {{c1::business value}} they will achieve once their problems are solved.",
        "explanation": "The future state is not just using your software; it is the business result of using it (e.g. saving 20 hours a week).",
        "spanish": "El Estado Futuro representa el entorno deseado por el prospecto, sus resultados y el valor comercial que logrará.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Business vs Technical Problems 📈",
        "text": "A {{c1::technical problem}} is a breakdown in a tool or process (e.g., slow database), whereas a {{c2::business problem}} is the financial or operational impact of that breakdown (e.g., losing $50k in lost sales).",
        "explanation": "Customers buy solutions to business problems, not technical problems. Always connect technical flaws to business outcomes.",
        "spanish": "Un problema técnico es una falla en una herramienta, mientras que un problema comercial es el impacto financiero de esa falla.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Root Cause 📈",
        "text": "To solve a problem, you must identify its {{c1::root cause}}—the underlying operational or systemic reason why the problem exists.",
        "explanation": "If you don't find the root cause, you will pitch a generic solution that doesn't solve the customer's actual pain.",
        "spanish": "Para resolver un problema, debes identificar su causa raíz: la razón operativa o sistémica subyacente.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Impact 📈",
        "text": "The {{c1::Impact}} is the emotional, financial, or operational cost of the problem if it goes unsolved.",
        "explanation": "Impact creates urgency. If a problem has no negative impact, the customer will choose to do nothing (no decision).",
        "spanish": "El Impacto es el costo emocional, financiero o de rendimiento del problema si no se resuelve.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Value of Solution 📈",
        "text": "The value of your solution is not determined by its features, but by the {{c1::size of the gap}} you can close.",
        "explanation": "A product that costs $10k has massive value if it closes a $1M gap, but zero value if there is no gap.",
        "spanish": "El valor de tu solución no está determinado por sus características, sino por el tamaño de la brecha que puedes cerrar.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Discovery Strategy 📈",
        "text": "During discovery, your primary mindset should be that of a {{c1::doctor diagnosing a patient}}, rather than a salesperson pitching a product.",
        "explanation": "A doctor asks questions, identifies symptoms, finds the root cause, and then prescribes. Pitching early is malpractice.",
        "spanish": "Durante el descubrimiento, tu mentalidad principal debe ser la de un médico que diagnostica a un paciente.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Problem Mapping 📈",
        "text": "Create a {{c1::Problem Map}} connecting the customer's technical problems, the business problems they cause, and the financial impact on the company.",
        "explanation": "This map guides your demo, ensuring you only show features that directly solve the mapped problems.",
        "spanish": "Crea un mapa de problemas que conecte los problemas técnicos del cliente, los problemas comerciales y su impacto financiero.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Status Quo Bias 📈",
        "text": "The customer's biggest competitor is not another vendor, but the {{c1::Status Quo}}—their comfort with doing things the way they always have.",
        "explanation": "Change is risky. If the gap is small, the customer will prefer the safety of the status quo.",
        "spanish": "El mayor competidor del cliente no es otro proveedor, sino el Status Quo: su comodidad con hacer las cosas como siempre.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Validation 📈",
        "text": "At the end of discovery, you must {{c1::validate the gap}} by repeating the current state and future state back to the customer and getting their explicit agreement.",
        "explanation": "Ensures alignment and shows the customer that you truly understand their business.",
        "usage": "Say: 'To make sure I got this right: you are currently losing $10k a month due to database downtime, and your goal is to reduce that to zero. Is that correct?'",
        "spanish": "Al final del descubrimiento, debes validar la brecha repitiendo el estado actual y futuro al cliente.",
        "tags": ["books_path", "sales", "communication"]
    },
    {
        "scenario": "Gap Selling: Solution Fit 📈",
        "text": "Only pitch the specific features of your product that {{c1::directly bridge the validated gap}}, ignoring all other features.",
        "explanation": "Showing features the customer doesn't need creates confusion and makes the product feel overly complex and expensive.",
        "spanish": "Solo presenta las características específicas de tu producto que cierren directamente la brecha validada.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Decision Criteria 📈",
        "text": "Discover the customer's {{c1::decision criteria}}—the specific parameters, budgets, and tests they will use to evaluate solutions.",
        "explanation": "If you don't know how they decide, you cannot guide them through the buying process.",
        "spanish": "Descubre los criterios de decisión del cliente: los parámetros y pruebas que utilizarán para evaluar soluciones.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Buying Process 📈",
        "text": "Map the customer's {{c1::buying process}}—identifying all decision-makers, legal requirements, security checks, and procurement steps.",
        "explanation": "A deal can fail at the finish line if you forget to account for security or procurement times.",
        "spanish": "Mapea el proceso de compra del cliente, identificando a todos los tomadores de decisiones y requisitos legales.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Emotion & Pain 📈",
        "text": "Business decisions are driven by emotion and {{c1::justified by logic}}. The gap represents the pain that drives the emotional desire for change.",
        "explanation": "Find the personal impact on the buyer (e.g. working late, stress) alongside the company impact.",
        "spanish": "Las decisiones comerciales son impulsadas por la emoción y justificadas por la lógica. La brecha representa el dolor.",
        "tags": ["books_path", "sales", "psychology"]
    },
    {
        "scenario": "Gap Selling: Mutual Action Plan 📈",
        "text": "To guide the buyer to the close, collaborate on a {{c1::Mutual Action Plan}} (MAP)—a shared checklist of steps, owners, and dates leading to go-live.",
        "explanation": "Shifts the relationship from vendor-client to collaborative partners working toward a shared goal.",
        "spanish": "Para guiar al comprador al cierre, colabora en un Plan de Acción Mutuo (MAP): una lista de pasos compartidos.",
        "tags": ["books_path", "sales", "project_management"]
    },
    {
        "scenario": "Gap Selling: No Pain, No Sale 📈",
        "text": "If a prospect claims they have no problems and are completely satisfied with their current setup, you must {{c1::disengage or create doubt}} rather than pitching.",
        "explanation": "Without pain, there is no gap, and they will never buy. Do not waste time on happy prospects.",
        "spanish": "Si un prospecto afirma no tener problemas y estar satisfecho, debes retirarte o generar dudas.",
        "tags": ["books_path", "sales", "gap_selling"]
    },
    {
        "scenario": "Gap Selling: Custom Demos 📈",
        "text": "A great demo is not a product tour; it is a {{c1::custom story}} where the prospect is the main character and your product is the tool they use to cross the gap.",
        "explanation": "Only show screens that relate directly to their validated pain points.",
        "spanish": "Una gran demostración no es un recorrido por el producto, sino una historia personalizada.",
        "tags": ["books_path", "sales", "demo"]
    },
    {
        "scenario": "Gap Selling: Pricing Conversations 📈",
        "text": "Do not discuss price until you have {{c1::established the size of the gap}} and the value of closing it.",
        "explanation": "If you state the price early, the customer has no context to evaluate if it is cheap or expensive.",
        "spanish": "No discutas el precio hasta que hayas establecido el tamaño de la brecha y el valor de cerrarla.",
        "tags": ["books_path", "sales", "pricing"]
    },
    {
        "scenario": "Gap Selling: Post-Sale Gap 📈",
        "text": "Customer success starts by review of the {{c1::validated gap}} from the sales cycle, ensuring the implementation team actually delivers the desired future state.",
        "explanation": "Prevents churn by ensuring the customer achieves the business outcomes they bought.",
        "spanish": "El éxito del cliente comienza revisando la brecha validada del ciclo de ventas para asegurar que se logre.",
        "tags": ["books_path", "sales", "customer_success"]
    }
]

# ==================== 12_Objections (20 cards) ====================
objections = [
    {
        "scenario": "Objections: Red Herrings 🙅‍♂️",
        "text": "A {{c1::Red Herring}} is a false objection or distraction thrown out by a prospect to hide their real concern or delay the buying process.",
        "explanation": "Do not get distracted by red herrings. Acknowledge them and redirect the conversation back to the core value.",
        "usage": "If a prospect complains about a minor feature color during a price meeting, acknowledge it and pivot back to the ROI.",
        "spanish": "Una pista falsa (Red Herring) es una objeción falsa o distracción lanzada por un prospecto para ocultar su preocupación real.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: Turnaround Framework 🙅‍♂️",
        "text": "The standard framework for handling objections consists of 4 steps: 1. {{c1::Listen}} completely, 2. {{c2::Acknowledge}} the concern, 3. {{c3::Explore}} the root cause, and 4. {{c4::Respond}} with value.",
        "explanation": "Never argue or react defensively. Listening completely defuses tension, and exploring ensures you address the real objection.",
        "spanish": "El marco estándar para manejar objeciones consta de 4 pasos: Escuchar, Reconocer, Explorar y Responder.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: Micro-Commitment Objections 🙅‍♂️",
        "text": "A {{c1::micro-commitment objection}} is an objection raised during early outreach to avoid booking a meeting (e.g. 'I don't have time').",
        "explanation": "The goal is to get a small commit (time), not to sell the product. Reframe the request to show high value for low commitment.",
        "usage": "Prospect: 'Send me an email.' Response: 'I will, but to make sure I send what's relevant, let's schedule a 5-minute call.'",
        "spanish": "Una objeción de microcompromiso es la que se plantea durante el contacto inicial para evitar reservar una reunión.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: Buying Commitment Objections 🙅‍♂️",
        "text": "A {{c1::buying commitment objection}} occurs at the end of the sales cycle, when the customer faces risk and hesitates to sign the contract.",
        "explanation": "These are real concerns about budget, implementation, or risk. Explore the root fear to solve it.",
        "spanish": "Una objeción de compromiso de compra ocurre al final del ciclo de ventas, cuando el cliente duda en firmar.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: Status Quo Bias 🙅‍♂️",
        "text": "Many objections are driven by {{c1::fear of change}}, as the buyer takes on personal risk inside their organization by championing a new vendor.",
        "explanation": "If your product fails, they might lose their job. Alleviate risk with case studies, guarantees, and clear plans.",
        "spanish": "Muchas objeciones son impulsadas por el miedo al cambio, ya que el comprador asume un riesgo personal al elegir un proveedor.",
        "tags": ["books_path", "sales", "psychology"]
    },
    {
        "scenario": "Objections: Price Objections 🙅‍♂️",
        "text": "A price objection (e.g., 'It's too expensive') is often a symptom of {{c1::lack of perceived value}} rather than lack of budget.",
        "explanation": "If the customer believes the solution will save them $100k, they will find the $10k budget. Re-establish the size of the gap.",
        "spanish": "Una objeción de precio suele ser un síntoma de falta de valor percibido en lugar de falta de presupuesto.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: LAER Framework 🙅‍♂️",
        "text": "The LAER framework for handling objections stands for: {{c1::Listen}}, {{c2::Acknowledge}}, {{c3::Explore}}, and {{c4::Respond}}.",
        "explanation": "Similar to standard frameworks, LAER emphasizes the exploration phase to avoid presenting premature solutions.",
        "spanish": "El marco LAER para manejar objeciones significa: Listen (Escuchar), Acknowledge (Reconocer), Explore (Explorar) y Respond (Responder).",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: Clarifying Objections 🙅‍♂️",
        "text": "Before responding to an objection, you must explore it using {{c1::open-ended questions}} to find the underlying issue.",
        "explanation": "If a prospect says 'This takes too long', ask: 'Can you walk me through your timeline expectations?'",
        "spanish": "Antes de responder a una objeción, debes explorarla utilizando preguntas abiertas para encontrar el problema subyacente.",
        "tags": ["books_path", "sales", "communication"]
    },
    {
        "scenario": "Objections: Acknowledge defuses 🙅‍♂️",
        "text": "Acknowledging an objection does not mean agreeing with it; it means showing the prospect that you {{c1::understand their perspective}}.",
        "explanation": "Defuses defensive walls. Example: 'I understand that budget is tight right now, and that makes total sense.'",
        "spanish": "Reconocer una objeción no significa estar de acuerdo; significa demostrar que entiendes su perspectiva.",
        "tags": ["books_path", "sales", "communication"]
    },
    {
        "scenario": "Objections: Pre-Emptive Strike 🙅‍♂️",
        "text": "A {{c1::pre-emptive objection handler}} involves raising a common objection yourself and resolving it before the prospect has a chance to bring it up.",
        "explanation": "Shows honesty and neutralizes the objection early. Example: 'Now, our migration takes about 2 weeks, and here is how we ensure zero downtime.'",
        "spanish": "Un manejo de objeciones preventivo implica plantear una objeción común tú mismo y resolverla antes que el cliente.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: Sunk Cost Objection 🙅‍♂️",
        "text": "When a prospect says 'We've already spent $50k on our current system, we can't switch', they are exhibiting the {{c1::sunk cost fallacy}}.",
        "explanation": "Reframe the discussion around future returns. The $50k is gone regardless of their decision today.",
        "spanish": "Cuando un cliente dice 'Ya gastamos mucho en nuestro sistema actual', muestra la falacia del costo hundido.",
        "tags": ["books_path", "sales", "psychology"]
    },
    {
        "scenario": "Objections: Requesting vs Demanding 🙅‍♂️",
        "text": "To maintain control of the conversation, treat objections as {{c1::requests for information}} rather than demands or rejections.",
        "explanation": "An objection is an opportunity to educate. It shows they are engaged with the offer.",
        "spanish": "Para mantener el control, trata las objeciones como solicitudes de información en lugar de demandas o rechazos.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: No Budget 🙅‍♂️",
        "text": "When a prospect says 'We have no budget', explore if they have a {{c1::business problem}} that is costing them more than the price of your solution.",
        "explanation": "Budget is flexible if the pain is severe. If you solve a critical problem, they will pull budget from other areas.",
        "spanish": "Cuando un prospecto dice 'No tenemos presupuesto', explora si tienen un problema comercial que les cuesta más.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: The Competitor Objection 🙅‍♂️",
        "text": "When a prospect objects that a competitor is cheaper, reframe the conversation around the {{c1::Total Cost of Ownership}} (TCO) and risk of failure.",
        "explanation": "A cheaper product that fails or requires heavy maintenance costs more in the long run.",
        "spanish": "Cuando un prospecto objeta que un competidor es más barato, enfoca la conversación en el Costo Total de Propiedad (TCO).",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: The Delay Objection 🙅‍♂️",
        "text": "When a prospect says 'Call me back in 6 months', explore what {{c1::business impact}} will occur if they let the problem persist for another half year.",
        "explanation": "Find the cost of delay. If delaying costs $60k, they will want to act now.",
        "spanish": "Cuando un prospecto dice 'Llámame en 6 meses', explora qué impacto tendrá dejar que el problema persista.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: The Silent Objection 🙅‍♂️",
        "text": "The most dangerous objection is the {{c1::silent objection}}—when a prospect has a major concern but doesn't mention it, leading to a stalled deal.",
        "explanation": "Always ask: 'Is there anything else that might prevent us from moving forward with this timeline?'",
        "spanish": "La objeción más peligrosa es la objeción silenciosa: cuando el cliente tiene una duda pero no la menciona.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: Authority Objection 🙅‍♂️",
        "text": "When a prospect says 'I need to talk to my boss', do not view it as a rejection; instead, offer to {{c1::help them build a business case}} for their boss.",
        "explanation": "Help your champion sell internally. Give them slides, ROI sheets, and data.",
        "spanish": "Cuando un prospecto dice 'Necesito hablar con mi jefe', ofrécele ayuda para armar el caso de negocio.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: The Feature Objection 🙅‍♂️",
        "text": "When a prospect objects that you lack a specific feature, explore the {{c1::business goal}} behind that feature to see if you can achieve it in a different way.",
        "explanation": "Often, they ask for a feature because they assume it's the only way to solve a problem. Find the actual problem.",
        "spanish": "Cuando un prospecto objeta que te falta una característica, explora el objetivo comercial detrás de ella.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: The Trust Objection 🙅‍♂️",
        "text": "Objections about your company's size or age are usually {{c1::trust objections}}. Resolve them using case studies, security audits, and references.",
        "explanation": "Alleviate the fear of buying from an unknown vendor by showing credentials and social proof.",
        "spanish": "Las objeciones sobre el tamaño o edad de tu empresa suelen ser de confianza. Resuélvelas con casos de estudio.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Objections: Final Agreement 🙅‍♂️",
        "text": "Once you resolve an objection, always ask for {{c1::confirmation}} that the concern is resolved before moving forward.",
        "explanation": "Prevents the objection from coming back. Example: 'Does that explain how we handle server security to your satisfaction?'",
        "spanish": "Una vez resuelta una objeción, pide siempre confirmación de que la preocupación ha sido resuelta.",
        "tags": ["books_path", "sales", "communication"]
    }
]

save_deck("Sales", "10_Fanatical_Prospecting", fanatical_prospecting)
save_deck("Sales", "11_Gap_Selling", gap_selling)
save_deck("Sales", "12_Objections", objections)
