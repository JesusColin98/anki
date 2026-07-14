import json
import os
from generate_books_part1 import save_deck

# ==================== 13_SPIN_Selling (20 cards) ====================
spin_selling = [
    {
        "scenario": "SPIN Selling: SPIN Acronym 🔄",
        "text": "The SPIN selling framework is an acronym that stands for: {{c1::Situation}}, {{c2::Problem}}, {{c3::Implication}}, and {{c4::Need-payoff}} questions.",
        "explanation": "This sequence of questions guides the customer from describing their current state to realizing the urgency and value of your solution.",
        "spanish": "La metodología de venta SPIN es una sigla que significa preguntas de: Situación, Problema, Implicación y Necesidad de recompensa.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Situation Questions 🔄",
        "text": "{{c1::Situation}} questions gather background facts and data about the customer's current setup, processes, and tools.",
        "explanation": "Do not ask too many Situation questions, as they can bore the customer. Do your research in advance.",
        "usage": "Example: 'What software are you currently using to manage your database logs?'",
        "spanish": "Las preguntas de Situación recopilan datos de contexto e información sobre la configuración actual del cliente.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Problem Questions 🔄",
        "text": "{{c1::Problem}} questions explore difficulties, dissatisfactions, and problems the customer is facing with their current setup.",
        "explanation": "These questions uncover implicit needs. Successful sales calls use more Problem questions than unsuccessful ones.",
        "usage": "Example: 'Are you experiencing any performance delays or indexing bottlenecks with your current setup?'",
        "spanish": "Las preguntas de Problema exploran las dificultades y descontentos que enfrenta el cliente con su sistema actual.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Implication Questions 🔄",
        "text": "{{c1::Implication}} questions explore the consequences, effects, and business impact of the customer's problems.",
        "explanation": "Implication questions are the most powerful in SPIN. They help the buyer realize the financial and operational cost of doing nothing.",
        "usage": "Example: 'How does the database delay affect your customer checkout speed and cart abandonment rate?'",
        "spanish": "Las preguntas de Implicación exploran las consecuencias e impacto comercial de los problemas del cliente.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Need-Payoff Questions 🔄",
        "text": "{{c1::Need-payoff}} questions focus the customer's attention on the value, utility, and benefits of solving their problems.",
        "explanation": "These questions ask the buyer to explain the value of the solution in their own words, reducing objection risk.",
        "usage": "Example: 'If we could reduce database delay by 50%, how would that affect your team's support ticket volume?'",
        "spanish": "Las preguntas de Necesidad de Recompensa (Need-payoff) enfocan la atención del cliente en el valor de resolver sus problemas.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Implicit vs Explicit Needs 🔄",
        "text": "An {{c1::implicit need}} is a statement of a problem or difficulty, whereas an {{c2::explicit need}} is a concrete statement of a desire for a solution or action.",
        "explanation": "In large sales, you cannot sell on implicit needs alone. You must develop them into explicit needs using Implication and Need-payoff questions.",
        "spanish": "Una necesidad implícita es una queja de un problema, mientras que una explícita es el deseo de una solución específica.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Features vs Benefits 🔄",
        "text": "A feature describes what a product does. A {{c1::benefit}} shows how a feature meets an explicit need expressed by the customer.",
        "explanation": "Pitching features before developing explicit needs is called 'features dumping' and leads to price objections.",
        "spanish": "Una característica describe lo que hace el producto. Un beneficio muestra cómo responde a una necesidad explícita del cliente.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Large vs Small Sales 🔄",
        "text": "Neil Rackham's research shows that sales techniques that work in small, transactional sales (like pressure closing) actually {{c1::fail}} in large, complex sales.",
        "explanation": "Large sales involve higher risk and longer relationships, making pressure tactics backfire.",
        "spanish": "La investigación de Neil Rackham muestra que las técnicas que funcionan en ventas pequeñas fallan en ventas complejas.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Advances vs Continuation 🔄",
        "text": "In large sales, a successful meeting result is an {{c1::Advance}}—a concrete commitment by the buyer that moves the deal forward (e.g. scheduling a demo), whereas a {{c2::Continuation}} is just a polite agreement to keep talking.",
        "explanation": "Avoid continuations. Always request a clear commitment at the end of every call.",
        "spanish": "En ventas grandes, un resultado exitoso es un Avance (un compromiso concreto), mientras que una Continuación es solo una charla sin acuerdo.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Preventing Objections 🔄",
        "text": "According to SPIN, the best way to handle objections is to {{c1::prevent them}} by developing explicit needs before introducing your solution.",
        "explanation": "If you present a solution too early, the customer will raise price or feature objections because they don't see the value yet.",
        "spanish": "Según SPIN, la mejor manera de manejar las objeciones es prevenirlas desarrollando necesidades explícitas antes de mostrar la solución.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "SPIN Selling: Implication Questions Impact 🔄",
        "text": "Implication questions are especially effective when selling to {{c1::decision-makers}}, as they speak the language of business impact and return on investment.",
        "explanation": "Decision-makers care about financial and operational consequences, not technical features.",
        "spanish": "Las preguntas de implicación son efectivas al vender a tomadores de decisiones, pues hablan de impacto comercial y ROI.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Need-Payoff Impact 🔄",
        "text": "Need-payoff questions reduce objections because they place the buyer in the role of {{c1::explaining the value}} of your product, which convinces them internally.",
        "explanation": "When the customer states the benefits, they believe it. When you state the benefits, they doubt it.",
        "spanish": "Las preguntas de recompensa reducen objeciones porque ponen al comprador en el rol de explicar el valor de tu producto.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: The SPIN Sequence 🔄",
        "text": "The correct order of the SPIN sequence is: Situation &rarr; Problem &rarr; {{c1::Implication}} &rarr; {{c2::Need-payoff}}.",
        "explanation": "This sequence builds a logical case for action, escalating the pain before offering the cure.",
        "spanish": "El orden correcto de la secuencia SPIN es: Situación &rarr; Problema &rarr; Implicación &rarr; Necesidad de Recompensa.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Situation Question Limit 🔄",
        "text": "Over-asking {{c1::Situation}} questions is the hallmark of inexperienced salespeople, as it bores the client and provides little value.",
        "explanation": "Do your background research on the client's company before the meeting.",
        "spanish": "Hacer demasiadas preguntas de Situación es el error de vendedores inexpertos, ya que aburre al cliente.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Uncovering Needs 🔄",
        "text": "In small sales, implicit needs are strongly linked to success, but in large sales, only {{c1::explicit needs}} lead to high closing rates.",
        "explanation": "Large purchases require strong, explicit motivation to justify the risk and budget.",
        "spanish": "En ventas grandes, solo las necesidades explícitas conducen a altas tasas de cierre.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Advantages vs Benefits 🔄",
        "text": "An {{c1::Advantage}} is showing how a product feature can help a customer, but it is not a Benefit unless it addresses a validated explicit need.",
        "explanation": "Advantages can trigger objections if they do not match the customer's active priorities.",
        "spanish": "Una Ventaja muestra cómo una característica del producto puede ayudar, pero no es un Beneficio hasta que responde a una necesidad explícita.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: Pre-Call Planning 🔄",
        "text": "To prepare for a SPIN call, write down at least {{c1::3 potential problems}} the customer might have, and plan Problem questions to explore them.",
        "explanation": "Planning questions in advance ensures you lead a structured, high-value discovery meeting.",
        "spanish": "Para prepararte para una llamada SPIN, escribe al menos 3 problemas potenciales que el cliente pueda tener.",
        "tags": ["books_path", "sales", "planning"]
    },
    {
        "scenario": "SPIN Selling: Trial Closing 🔄",
        "text": "Avoid aggressive closing techniques in large sales. Instead, focus on building {{c1::agreement on needs}} and securing small advances.",
        "explanation": "Closing pressure makes buyers defensive and destroys trust in high-value sales.",
        "spanish": "Evita técnicas de cierre agresivas en ventas grandes. Enfócate en lograr acuerdos sobre las necesidades.",
        "tags": ["books_path", "sales", "spin_selling"]
    },
    {
        "scenario": "SPIN Selling: SPIN Practice 🔄",
        "text": "When learning SPIN, focus on practicing {{c1::one question type at a time}} in your daily conversations before trying to execute the full sequence.",
        "explanation": "Trying to master all four stages at once is overwhelming. Focus on problem questions first.",
        "spanish": "Al aprender SPIN, enfócate en practicar un tipo de pregunta a la vez en tus conversaciones diarias.",
        "tags": ["books_path", "sales", "mastery"]
    },
    {
        "scenario": "SPIN Selling: Explicit Need Goal 🔄",
        "text": "The ultimate goal of the discovery phase in SPIN is to convert implicit needs into {{c1::explicit needs}}.",
        "explanation": "Explicit needs represent the customer's active desire for a solution, making them ready to buy.",
        "spanish": "El objetivo final de la fase de descubrimiento en SPIN es convertir las necesidades implícitas en explícitas.",
        "tags": ["books_path", "sales", "spin_selling"]
    }
]

# ==================== 14_The_Challenger_Sale (20 cards) ====================
the_challenger_sale = [
    {
        "scenario": "Challenger Sale: The 5 Profiles ⚔️",
        "text": "The Challenger Sale study identifies 5 distinct sales profiles: The Relationship Builder, The Hard Worker, The Lone Wolf, The Reactive Problem Solver, and {{c1::The Challenger}}.",
        "explanation": "While Relationship Builders are common, Challengers are by far the most successful in complex sales, especially in difficult economic times.",
        "spanish": "El estudio identifica 5 perfiles de ventas: el constructor de relaciones, el trabajador, el lobo solitario, el solucionador de problemas y el Challenger.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Challenger Profile ⚔️",
        "text": "The Challenger profile is defined by three core capabilities: they {{c1::teach}} for differentiation, {{c2::tailor}} for resonance, and {{c3::take control}} of the sale.",
        "explanation": "Challengers do not win by building smooth relationships; they win by reframing the customer's thinking and pushing them past their comfort zone.",
        "spanish": "El perfil Challenger se define por tres capacidades: enseñar para diferenciar, adaptar para resonar y tomar el control de la venta.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Teach for Differentiation ⚔️",
        "text": "To **Teach**, Challengers deliver {{c1::unique insights}} about the customer's business problems, reframing their thinking rather than asking what they need.",
        "explanation": "Instead of asking 'what keeps you up at night?', tell the customer what *should* be keeping them up at night based on market data.",
        "spanish": "Para Enseñar, los Challengers ofrecen perspectivas únicas sobre los problemas comerciales del cliente, reestructurando su pensamiento.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Commercial Teaching ⚔️",
        "text": "The Challenger sales method uses **Commercial Teaching** to guide the customer to your unique capabilities without pitching them upfront, a process called {{c1::leading to, not leading with}} your solution.",
        "explanation": "First, establish the business problem and reframed insight, then show how your unique capability is the only way to solve it.",
        "spanish": "El método Challenger utiliza la Enseñanza Comercial para guiar al cliente hacia tus capacidades únicas, liderando hacia la solución, no con ella.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Tailor for Resonance ⚔️",
        "text": "To **Tailor**, you must {{c1::customize the sales message}} to the specific goals, metrics, and language of each decision-maker inside the organization.",
        "explanation": "The CFO cares about cash flow; the Head of Engineering cares about deployment reliability. Tailor the message to each stakeholder.",
        "spanish": "Para Adaptar (Tailor), debes personalizar el mensaje a las metas y lenguaje específico de cada tomador de decisiones.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Take Control ⚔️",
        "text": "To **Take Control**, Challengers confidently {{c1::discuss pricing}} and guide the customer through the buying steps, resisting the urge to compromise on discounts.",
        "explanation": "Taking control means standing firm on price because you know the value of your solution, and leading the buying process instead of being passive.",
        "spanish": "Para Tomar el Control, los Challengers discuten el precio con confianza y guían al cliente, sin ceder a descuentos fácilmente.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Constructive Tension ⚔️",
        "text": "Challengers actively build {{c1::constructive tension}} during the sales meeting to challenge the customer's status quo and drive change.",
        "explanation": "Relationship Builders try to eliminate all tension, which leads to no decision. Challengers use tension to highlight the cost of inaction.",
        "spanish": "Los Challengers construyen activamente tensión constructiva durante la reunión para desafiar el statu quo del cliente.",
        "tags": ["books_path", "sales", "psychology"]
    },
    {
        "scenario": "Challenger Sale: The Warm-Up ⚔️",
        "text": "The first step of the Commercial Teaching pitch is the **Warm-Up**, where you build credibility by describing {{c1::common challenges}} faced by similar companies.",
        "explanation": "Shows the customer you understand their world before presenting any data.",
        "spanish": "El primer paso de la presentación de Enseñanza Comercial es la Preparación (Warm-Up), describiendo desafíos comunes.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: The Reframe ⚔️",
        "text": "The second step of Commercial Teaching is the **Reframe**, where you present a {{c1::new, surprising insight}} that changes how the customer views their problem.",
        "explanation": "This is the 'Aha!' moment of the pitch, showing them a root cause they had not considered.",
        "spanish": "El segundo paso es el Reencuadre (Reframe), presentando una perspectiva nueva y sorprendente sobre su problema.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Rational Drowning ⚔️",
        "text": "The third step of Commercial Teaching is **Rational Drowning**, where you deliver {{c1::hard data and ROI calculations}} to validate the reframe.",
        "explanation": "Drown the customer in rational proof so they cannot dismiss the reframe as just an opinion.",
        "spanish": "El tercer paso es el Ahogamiento Racional (Rational Drowning), entregando datos y estadísticas para validar el reencuadre.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Emotional Impact ⚔️",
        "text": "The fourth step of Commercial Teaching is **Emotional Impact**, which makes the customer feel: '{{c1::This is happening to us right now}}'.",
        "explanation": "Connect the data to their daily pain so they have a personal, emotional connection to the problem.",
        "spanish": "El cuarto paso es el Impacto Emocional, haciendo que el cliente sienta que el problema les afecta directamente hoy.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: A Better Way ⚔️",
        "text": "The fifth step of Commercial Teaching is **A Better Way**, where you outline the {{c1::systemic solution}} required to fix the problem, without mentioning your product yet.",
        "explanation": "Get their agreement on the *method* of solution before pitching your specific tool.",
        "spanish": "El quinto paso es Un Camino Mejor, describiendo la solución sistémica necesaria sin mencionar aún tu producto.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Our Solution ⚔️",
        "text": "The sixth and final step of Commercial Teaching is **Our Solution**, showing how your {{c1::unique capability}} is the best way to deliver the agreed-upon solution.",
        "explanation": "This is where you pitch. It fits perfectly because they have already agreed on the problem, the reframe, and the solution model.",
        "spanish": "El sexto paso es Nuestra Solución, demostrando por qué tu capacidad única es la mejor para implementar la solución.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Relationship Builders ⚔️",
        "text": "The sales profile least likely to succeed in complex sales is the {{c1::Relationship Builder}}.",
        "explanation": "Relationship builders focus on keeping the customer happy and avoiding conflict, which means they rarely challenge the status quo or push for commitment.",
        "spanish": "El perfil de ventas con menos probabilidades de éxito en ventas complejas es el Constructor de Relaciones.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Customer Loyalty ⚔️",
        "text": "The study shows that 53% of customer loyalty is driven by the {{c1::sales experience itself}} (the insight and value delivered during the meeting), not by price or brand.",
        "explanation": "How you sell is more important than what you sell. Deliver insight to earn loyalty.",
        "spanish": "El estudio muestra que el 53% de la lealtad del cliente está impulsada por la experiencia de compra en sí.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Sales Manager ⚔️",
        "text": "The key capability of a successful Challenger Sales Manager is {{c1::sales coaching}}—helping reps build insights, tailor messages, and take control.",
        "explanation": "Managers must transition from being super-sellers to coaches who build team capability.",
        "spanish": "La capacidad clave de un exitoso gerente de ventas Challenger es el entrenamiento de ventas (sales coaching).",
        "tags": ["books_path", "sales", "management"]
    },
    {
        "scenario": "Challenger Sale: Challenger Enablement ⚔️",
        "text": "Organizations must support Challengers by providing {{c1::commercial insights}} and marketing collateral that challenge target markets.",
        "explanation": "Marketing must research and generate the reframes; individual sellers cannot build all insights alone.",
        "spanish": "Las organizaciones deben apoyar a los Challengers proporcionando perspectivas comerciales y material de marketing.",
        "tags": ["books_path", "sales", "marketing"]
    },
    {
        "scenario": "Challenger Sale: Price Objection control ⚔️",
        "text": "When faced with a price objection, a Challenger takes control by {{c1::re-focusing on the business value}} rather than immediately offering a discount.",
        "explanation": "If you discount immediately, you validate that your product was overpriced. Defend the value.",
        "spanish": "Ante una objeción de precio, un Challenger toma el control reenfocándose en el valor comercial.",
        "tags": ["books_path", "sales", "objections"]
    },
    {
        "scenario": "Challenger Sale: Lone Wolves ⚔️",
        "text": "The {{c1::Lone Wolf}} profile can be highly successful in sales, but they are difficult to manage because they refuse to follow standard CRM and sales processes.",
        "explanation": "They perform well but are erratic and hard to scale across an organization.",
        "spanish": "El perfil Lobo Solitario (Lone Wolf) puede ser muy exitoso, pero es difícil de manejar porque no sigue procesos estándar.",
        "tags": ["books_path", "sales", "challenger"]
    },
    {
        "scenario": "Challenger Sale: Teaching Goal ⚔️",
        "text": "The ultimate goal of Challenger teaching is to help the customer {{c1::save or make money}} in ways they did not realize were possible.",
        "explanation": "Reframing must always link directly to bottom-line business metrics.",
        "spanish": "El objetivo final de la enseñanza Challenger es ayudar al cliente a ahorrar o ganar dinero de formas que no conocía.",
        "tags": ["books_path", "sales", "challenger"]
    }
]

save_deck("Sales", "13_SPIN_Selling", spin_selling)
save_deck("Sales", "14_The_Challenger_Sale", the_challenger_sale)
