import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_cards = [
    {
        "deck": "AI_Learning_Path::04_Agentic_Systems::Agent_Frameworks",
        "scenario": "Agent Toolkits: Graph Orchestration 📊",
        "text": "For complex, cyclical workflows requiring strict reliability, {{c1::LangGraph}} structures agents as a state machine where {{c2::Nodes}} represent actions and {{c2::Edges}} represent transitions.",
        "explanation": "LangGraph is built on top of LangChain. Its core advantage is representing loops (cycles) naturally in a graph, with state persistence (saving checkpoints) and fine-grained control over transitions.",
        "usage": "Ideal for production-grade pipelines where you need human-in-the-loop validation at specific checkpoints (e.g. approving an email draft before sending).",
        "spanish": "Para flujos de trabajo complejos y cíclicos que requieren una fiabilidad estricta, LangGraph estructura a los agentes como una máquina de estados donde los Nodos representan acciones y las Aristas representan transiciones.",
        "tags": ["ai_learning_path", "agent_toolkits", "langgraph"]
    },
    {
        "deck": "AI_Learning_Path::04_Agentic_Systems::Agent_Frameworks",
        "scenario": "Agent Toolkits: Role-Playing Teams 🤝",
        "text": "For organizational task delegation, {{c1::CrewAI}} adopts a role-playing design where developers define agents with specific {{c2::Roles, Goals, and Backstories}}.",
        "explanation": "CrewAI models agents like employees in a company. You define their specialty (role), what they need to achieve (goals), and a narrative (backstory). It supports sequential or hierarchical delegation of tasks automatically.",
        "usage": "Perfect for content generation or market analysis where one agent researches, another drafts, and a manager agent reviews the content.",
        "spanish": "Para la delegación de tareas organizacionales, CrewAI adopta un diseño de juego de roles donde los desarrolladores definen agentes con Roles, Objetivos e Historias de fondo específicos.",
        "tags": ["ai_learning_path", "agent_toolkits", "crewai"]
    },
    {
        "deck": "AI_Learning_Path::04_Agentic_Systems::Agent_Frameworks",
        "scenario": "Agent Toolkits: Conversational Dialogue 💬",
        "text": "To support collaborative problem-solving, Microsoft's {{c1::AutoGen}} defines agents as {{c2::conversable entities}} that interact with each other through structured text-based dialogues.",
        "explanation": "AutoGen focuses on agent-to-agent chat. Multiple agents (e.g., coder, critic, user proxy) converse with each other in a chat room, generating and executing code iteratively to solve complex math or programming problems.",
        "usage": "Useful for joint research, code generation, and iterative debugging tasks where agents need to critique each other's work dynamically.",
        "spanish": "Para apoyar la resolución colaborativa de problemas, AutoGen de Microsoft define a los agentes como entidades conversacionales que interactúan entre sí a través de diálogos estructurados basados en texto.",
        "tags": ["ai_learning_path", "agent_toolkits", "autogen"]
    },
    {
        "deck": "AI_Learning_Path::04_Agentic_Systems::Agent_Frameworks",
        "scenario": "Agent Toolkits: Event-Driven Execution ⚡",
        "text": "In agent development toolkits, an {{c1::event-driven workflow}} triggers agent actions based on custom {{c2::Events}} rather than predefined graph routes.",
        "explanation": "Event-driven agent frameworks (like LlamaIndex Workflows) let agents publish and subscribe to specific event types. When a task publishes an event, any agent listening to that event type triggers its action, making the system highly decoupled.",
        "usage": "Handling multi-source incoming documents where a 'pdf_event' triggers a PDF parser, and a 'txt_event' triggers a text parser asynchronously.",
        "spanish": "En los kits de desarrollo de agentes, un flujo de trabajo impulsado por eventos activa las acciones de los agentes basadas en Eventos personalizados en lugar de rutas de gráficos predefinidas.",
        "tags": ["ai_learning_path", "agent_toolkits", "event_driven"]
    }
]

cards.extend(new_cards)

with open(database_file, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"Successfully appended {len(new_cards)} agent toolkit cards to {database_file}.")
