import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_cards = [
    # Social_Skills::04_Customer_Support_Excellence::Crisis_Management
    {
        "deck": "Social_Skills::04_Customer_Support_Excellence::Crisis_Management",
        "scenario": "Crisis: Incident Updates (P1/P0) 📢",
        "text": "During a critical P0 incident, the status updates must follow a strict three-part structure: {{c1::Current Impact}}, {{c2::Investigation Focus}}, and {{c3::ETA for Next Update}}.",
        "explanation": "This structure prevents client panic and reduces inbound ticket spikes by establishing a predictable communication heartbeat. Setting an ETA for the next update keeps clients from constantly asking for news.",
        "usage": "A mandatory communication standard for Enterprise Support during major cloud outages.",
        "spanish": "Durante un incidente crítico P0, las actualizaciones de estado deben seguir una estructura estricta de tres partes: Impacto actual, Enfoque de investigación y Tiempo estimado para la próxima actualización.",
        "tags": ["crisis_management", "incident_response", "p0_p1"]
    },
    {
        "deck": "Social_Skills::04_Customer_Support_Excellence::Crisis_Management",
        "scenario": "Crisis: Incident Commander (IC) Role 🧑‍✈️",
        "text": "To maintain focus during a high-pressure crisis bridge, the {{c1::Incident Commander (IC)}} must isolate technical engineers from {{c2::executive noise/updates}} so the engineers can focus exclusively on diagnostics.",
        "explanation": "The Incident Commander controls the bridge. They manage stakeholders and direct communication, ensuring that engineers are not distracted by VPs or customers demanding immediate answers.",
        "usage": "Crucial for managing stress and average resolution times (MTTR) during system outages.",
        "spanish": "Para mantener el enfoque durante un puente de crisis de alta presión, el Comandante de Incidentes (IC) debe aislar a los ingenieros técnicos del ruido o actualizaciones ejecutivas para que los ingenieros puedan concentrarse exclusivamente en el diagnóstico.",
        "tags": ["crisis_management", "incident_commander", "communication"]
    },
    {
        "deck": "Social_Skills::04_Customer_Support_Excellence::Crisis_Management",
        "scenario": "Crisis: Translation of Technical Jargon 🗣️",
        "text": "When translating engineering updates for external clients, the agent must avoid raw logs or system architecture details and instead frame the status in terms of {{c1::business/functional impact}} and {{c2::mitigation steps}}.",
        "explanation": "Clients in a crisis care about what is broken for their users and how to bypass it. Technical jargon about database replication lag or memory leaks should be translated into clear business-level statements.",
        "usage": "Bridging the gap between engineering teams and customer-facing support roles.",
        "spanish": "Al traducir actualizaciones de ingeniería para clientes externos, el agente debe evitar registros sin procesar o detalles de arquitectura del sistema y, en su lugar, enmarcar el estado en términos de impacto comercial/funcional y pasos de mitigación.",
        "tags": ["crisis_management", "jargon_translation", "communication"]
    },
    {
        "deck": "Social_Skills::04_Customer_Support_Excellence::Crisis_Management",
        "scenario": "Written: One-Touch Resolution Mindset 🎯",
        "text": "To achieve a one-touch resolution on complex tickets, the engineer must {{c1::anticipate the next logical question}} and provide the solution or commands for that scenario beforehand.",
        "explanation": "One-touch resolution avoids back-and-forth emails. By thinking ahead (e.g., 'If they have version X, they will need this extra flag'), you save days of delay and boost customer satisfaction.",
        "usage": "A gold standard habit for premium tier async support teams.",
        "spanish": "Para lograr una resolución al primer contacto en tickets complejos, el ingeniero debe anticipar la siguiente pregunta lógica y proporcionar la solución o los comandos para ese escenario de antemano.",
        "tags": ["support_excellence", "async_communication", "one_touch"]
    },
    {
        "deck": "Social_Skills::04_Customer_Support_Excellence::Crisis_Management",
        "scenario": "Written: Formatting for Impact 👁️",
        "text": "When structuring long technical emails for clients in a crisis, engineers should avoid long paragraphs and instead use {{c1::bold callouts for action items}} and {{c2::fenced code blocks for executable commands}}.",
        "explanation": "Clients under stress have short attention spans. Structuring text with bold items and separate code blocks allows them to scan the email and safely execute commands in seconds.",
        "usage": "Best practice for technical support documentation and email communications.",
        "spanish": "Al estructurar correos electrónicos técnicos largos para clientes en crisis, los ingenieros deben evitar los párrafos largos y, en su lugar, usar llamadas en negrita para los elementos de acción y bloques de código delimitados para los comandos ejecutables.",
        "tags": ["support_excellence", "formatting", "readability"]
    },

    # English::02_Professional::Technical_Negotiation_and_RCA
    {
        "deck": "English::02_Professional::Technical_Negotiation_and_RCA",
        "scenario": "Negotiation: Technical Push-back 🧱",
        "text": "When a customer's architectural design is flawed, you can push back gracefully by saying: \"While your setup is functional, it {{c1::introduces a single point of failure}} that could {{c2::compromise high availability}} during peak traffic.\"",
        "explanation": "Pointing out design risks (like single points of failure) using objective technical concepts rather than telling the client they are 'wrong' avoids defensiveness and builds advisory trust.",
        "usage": "Pattern: <code>[Setup] introduces [risk] that could compromise [performance metric]</code><ul><li><code>This setup introduces a single point of failure that could compromise high availability.</code></li><li><code>Using a single DB instance introduces a bottleneck that could compromise throughput.</code></li></ul>",
        "spanish": "Cuando el diseño arquitectónico de un cliente es defectuoso, puedes retroceder con gracia diciendo: \"Aunque su configuración es funcional, introduce un punto único de falla que podría comprometer la alta disponibilidad durante los picos de tráfico\".",
        "tags": ["technical_negotiation", "architecture", "push_back"]
    },
    {
        "deck": "English::02_Professional::Technical_Negotiation_and_RCA",
        "scenario": "Negotiation: Bugs vs. Feature Requests 🐛",
        "text": "To handle a client demanding a new capability as a bug fix, say: \"This behavior {{c1::aligns with current system design}}; however, I will {{c2::advocate for your use case}} directly with our product team.\"",
        "explanation": "\"Aligns with current system design\" is a professional way to state that the system is not broken, while \"advocate for your use case\" shows you are still partner-focused.",
        "usage": "Pattern: <code>[Behavior] aligns with current system design; however, I will advocate for [use case]</code><ul><li><code>The login timeout aligns with current system design; however, I will advocate for your use case of extending it.</code></li><li><code>Not allowing bulk deletions aligns with current system design.</code></li></ul>",
        "spanish": "Para manejar a un cliente que exige una nueva capacidad como si fuera una corrección de errores, di: \"Este comportamiento se alinea con el diseño actual del sistema; sin embargo, defenderé su caso de uso directamente con nuestro equipo de producto\".",
        "tags": ["technical_negotiation", "product_management", "expectations"]
    },
    {
        "deck": "English::02_Professional::Technical_Negotiation_and_RCA",
        "scenario": "RCA: Rebuilding Trust 📑",
        "text": "In a Post-Mortem or Root Cause Analysis (RCA), always close by saying: \"To prevent recurrence, we are {{c1::implementing automated safeguards}} and {{c2::refining our circuit breaker thresholds}}.\"",
        "explanation": "An RCA must culminate in concrete, systemic preventive actions. Explaining the safeguards demonstrates that the organization has learned and adapted to protect the client's operations.",
        "usage": "Pattern: <code>To prevent recurrence, we are implementing [preventative action]</code><ul><li><code>To prevent recurrence, we are implementing automated safeguards and database limits.</code></li><li><code>We are refining our circuit breaker thresholds to prevent cascade failures.</code></li></ul>",
        "spanish": "En un análisis de causa raíz (RCA), siempre cierra diciendo: \"Para evitar que vuelva a ocurrir, estamos implementando salvaguardas automatizadas y refinando los límites de nuestros interruptores automáticos\".",
        "tags": ["technical_negotiation", "rca", "post_mortem"]
    },
    {
        "deck": "English::02_Professional::Technical_Negotiation_and_RCA",
        "scenario": "Written: Scope Boundaries 🚧",
        "text": "To politely refuse debugging custom scripts, say: \"While I can confirm our API is responding normally, {{c1::custom scripts are outside our support scope}}; however, you can reference this {{c2::sample payload}}.\"",
        "explanation": "Clearly states the platform's boundaries (outside our support scope) but remains helpful by providing a reference example to guide the customer.",
        "usage": "Pattern: <code>[Topic] is outside our support scope; however, you can reference [alternative resource]</code><ul><li><code>Debugging custom scripts is outside our support scope; however, you can reference our sample repository.</code></li><li><code>Third-party libraries are outside our support scope.</code></li></ul>",
        "spanish": "Para rechazar cortésmente la depuración de scripts personalizados, di: \"Aunque puedo confirmar que nuestra API está respondiendo normalmente, los scripts personalizados están fuera de nuestro alcance de soporte; sin embargo, puede consultar este ejemplo de carga útil\".",
        "tags": ["technical_negotiation", "scope_boundaries", "written_english"]
    },
    {
        "deck": "English::02_Professional::Technical_Negotiation_and_RCA",
        "scenario": "Negotiation English: Reframing Delays ⏳",
        "text": "Instead of apologizing for a delay, use appreciation to stay assertive: \"Thank you for your patience while we {{c1::conducted a deep-dive review}} into your {{c2::infrastructure configuration}}.\"",
        "explanation": "Saying 'thank you for your patience' validates the wait while asserting that the time was spent on a high-value action (deep-dive review), preserving authority.",
        "usage": "Pattern: <code>Thank you for your patience while we conducted a deep-dive review into [infrastructure/database/setup]</code><ul><li><code>Thank you for your patience while we conducted a deep-dive review into your replication logs.</code></li><li><code>Our team conducted a deep-dive review and resolved the memory leak.</code></li></ul>",
        "spanish": "En lugar de disculparse por un retraso, use el agradecimiento para mantener la asertividad: \"Gracias por su paciencia mientras realizábamos una revisión profunda de la configuración de su infraestructura\".",
        "tags": ["negotiation_english", "appreciation", "professionalism"]
    },
    {
        "deck": "English::02_Professional::Technical_Negotiation_and_RCA",
        "scenario": "Negotiation English: Deflecting Escalations 🛡️",
        "text": "To deflect a premature escalation to management, suggest: \"I want to ensure we {{c1::exhaust all immediate diagnostic paths}} before we {{c2::engage our engineering lead}}, so we can present them with complete data.\"",
        "explanation": "This phrase positions the delay in escalation as a benefit to the customer (ensuring they have complete data first), maintaining control of the troubleshooting flow.",
        "usage": "Pattern: <code>exhaust all immediate diagnostic paths before we engage [lead/expert]</code><ul><li><code>I want to ensure we exhaust all immediate diagnostic paths before we engage our engineering lead.</code></li><li><code>Let's exhaust all immediate diagnostic paths before escalation.</code></li></ul>",
        "spanish": "Para desviar una escalación prematura a la gerencia, sugiera: \"Quiero asegurarme de que agotemos todas las vías de diagnóstico inmediato antes de involucrar a nuestro líder de ingeniería, para que podamos presentarles datos completos\".",
        "tags": ["negotiation_english", "escalation_prevention", "containment"]
    },
    {
        "deck": "English::02_Professional::Technical_Negotiation_and_RCA",
        "scenario": "Negotiation English: Admitting Missed Variables 🎯",
        "text": "To admit an error without losing credibility, state: \"Our initial assessment {{c1::missed X variable}}; we have {{c2::adjusted our troubleshooting path}} to focus on Y to get you back online safely.\"",
        "explanation": "Directly acknowledges the new information (missed variable) and immediately pivots to the updated action plan, projecting competence and responsiveness rather than defensiveness.",
        "usage": "Pattern: <code>Our initial assessment missed [variable]; we have adjusted our troubleshooting path to focus on [focus]</code><ul><li><code>Our initial assessment missed the firewall block; we have adjusted our troubleshooting path to focus on security rules.</code></li><li><code>We adjusted our troubleshooting path to focus on replication delays.</code></li></ul>",
        "spanish": "Para admitir un error sin perder credibilidad, declare: \"Nuestra evaluación inicial pasó por alto la variable X; hemos ajustado nuestro camino de resolución de problemas para enfocarnos en Y para que vuelva a estar en línea de manera segura\".",
        "tags": ["negotiation_english", "error_handling", "containment"]
    },
    {
        "deck": "English::02_Professional::Technical_Negotiation_and_RCA",
        "scenario": "Call Efficiency: Dynamic Time Boxing ⏱️",
        "text": "To pivot a call when time is running out, say: \"We have 15 minutes left on our scheduled block. To make sure we {{c1::lock down next steps}} for your production deployment, let's {{c2::pivot to the action items}}.\"",
        "explanation": "Using \"lock down next steps\" and \"pivot to action items\" focuses the remaining time on outcomes, preventing the meeting from ending without clear deliverables.",
        "usage": "Pattern: <code>We have [time] left on our scheduled block. To make sure we lock down next steps for [goal], let's pivot to [action items]</code><ul><li><code>We have 15 minutes left on our scheduled block. To make sure we lock down next steps for your production migration, let's pivot to the action items.</code></li><li><code>Let's make sure we lock down next steps before the meeting ends.</code></li></ul>",
        "spanish": "Para reorientar una llamada cuando se acaba el tiempo, di: \"Nos quedan 15 minutos en nuestro bloque programado. Para asegurarnos de acordar los próximos pasos para su implementación en producción, pasemos a los elementos de acción\".",
        "tags": ["call_efficiency", "time_boxing", "meeting_management"]
    },
    {
        "deck": "English::02_Professional::Technical_Negotiation_and_RCA",
        "scenario": "Call Efficiency: Handling Hijackers 🛑",
        "text": "To politely interrupt a client repeating the same complaint: \"I hear you, and to ensure we don't {{c1::lose ground on the diagnostic work}}, let's focus on collecting the server logs.\"",
        "explanation": "\"Lose ground on\" means to lose progress already made. This redirect politely signals that repeating the complaint stops active troubleshooting.",
        "usage": "Pattern: <code>I hear you, and to ensure we don't lose ground on [work/diagnostics], let's focus on [next step]</code><ul><li><code>I hear you, and to ensure we don't lose ground on the diagnostic work, let's focus on collecting the server logs.</code></li><li><code>We don't want to lose ground on the replication analysis.</code></li></ul>",
        "spanish": "Para interrumpir cortésmente a un cliente que repite la misma queja: \"Lo escucho, y para asegurarnos de no perder terreno en el trabajo de diagnóstico, concentrémonos en recopilar los registros del servidor\".",
        "tags": ["call_efficiency", "redirection", "difficult_clients"]
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
