import json
import urllib.request
import urllib.error
import sys

def invoke(action, **params):
    payload = {'action': action, 'version': 6}
    if params:
        payload['params'] = params
    req_data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request('http://127.0.0.1:8765', data=req_data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as response:
            res = json.loads(response.read().decode('utf-8'))
            if res.get('error') is not None:
                raise Exception(res['error'])
            return res['result']
    except urllib.error.URLError as e:
        print(f"Error connecting to AnkiConnect. Is Anki running?", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

def ensure_model_exists():
    model_name = "Engaging_Cloze_Model"
    models = invoke('modelNames')
    if model_name in models:
        print(f"Model '{model_name}' already exists.")
        return
    
    print(f"Creating custom model '{model_name}'...")
    css_content = """
.card {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    font-size: 19px;
    line-height: 1.6;
    color: #2D3748;
    background-color: #F7FAFC;
    padding: 24px;
    max-width: 550px;
    margin: 0 auto;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.cloze {
    font-weight: bold;
    color: #4F46E5;
    background-color: #EEF2FF;
    padding: 2px 8px;
    border-radius: 6px;
}

.scenario-badge {
    display: inline-block;
    font-size: 12px;
    font-weight: bold;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #718096;
    background-color: #EDF2F7;
    padding: 4px 12px;
    border-radius: 9999px;
    margin-bottom: 16px;
}

hr {
    border: none;
    border-top: 1px solid #E2E8F0;
    margin: 20px 0;
}

.sentence-front {
    font-size: 22px;
    font-weight: 500;
    color: #1A202C;
    margin: 12px 0;
}

.explanation-section {
    background-color: #FFFFFF;
    border-left: 4px solid #4F46E5;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 16px;
    text-align: left;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.explanation-section h3 {
    margin: 0 0 6px 0;
    font-size: 13px;
    color: #4F46E5;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.examples-section {
    background-color: #FFFFFF;
    border-left: 4px solid #10B981;
    padding: 12px 16px;
    border-radius: 0 8px 8px 0;
    margin-bottom: 16px;
    text-align: left;
    box-shadow: 0 1px 3px rgba(0,0,0,0.02);
}

.examples-section h3 {
    margin: 0 0 6px 0;
    font-size: 13px;
    color: #10B981;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.examples-section ul {
    margin: 0;
    padding-left: 20px;
    color: #4A5568;
}

.examples-section li {
    margin-bottom: 6px;
}

.examples-section code {
    background-color: #ECFDF5;
    color: #047857;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: monospace;
    font-size: 14px;
}

details {
    background-color: #EDF2F7;
    padding: 10px 14px;
    border-radius: 8px;
    margin-top: 16px;
    font-size: 15px;
    color: #4A5568;
    cursor: pointer;
    text-align: left;
    transition: background-color 0.2s;
}

details:hover {
    background-color: #E2E8F0;
}

details summary {
    font-weight: 600;
    outline: none;
    user-select: none;
}

details p {
    margin: 8px 0 0 0;
    color: #2D3748;
}

/* Night Mode support */
.nightMode .card {
    color: #E2E8F0;
    background-color: #1A202C;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.nightMode .cloze {
    color: #818CF8;
    background-color: #312E81;
}

.nightMode .scenario-badge {
    color: #A0AEC0;
    background-color: #2D3748;
}

.nightMode hr {
    border-top: 1px solid #2D3748;
}

.nightMode .sentence-front {
    color: #F7FAFC;
}

.nightMode .explanation-section {
    background-color: #2D3748;
    border-left: 4px solid #818CF8;
}

.nightMode .explanation-section h3 {
    color: #818CF8;
}

.nightMode .examples-section {
    background-color: #2D3748;
    border-left: 4px solid #34D399;
}

.nightMode .examples-section h3 {
    color: #34D399;
}

.nightMode .examples-section code {
    background-color: #065F46;
    color: #A7F3D0;
}

.nightMode details {
    background-color: #2D3748;
    color: #A0AEC0;
}

.nightMode details:hover {
    background-color: #4A5568;
}

.nightMode details p {
    color: #E2E8F0;
}
"""

    front_template = """<div class="scenario-badge">{{Scenario}}</div>
<div class="sentence-front">{{cloze:Text}}</div>"""

    back_template = """<div class="scenario-badge">{{Scenario}}</div>
<div class="sentence-front">{{cloze:Text}}</div>
<hr>
<div class="explanation-section">
    <h3>Meaning & Context</h3>
    {{Explanation}}
</div>
<div class="examples-section">
    <h3>Key Takeaways & Examples</h3>
    {{Usage_Examples}}
</div>
<details>
    <summary>Show Spanish Translation</summary>
    <p>{{Spanish_Translation}}</p>
</details>
{{Audio}}"""

    invoke(
        'createModel',
        modelName=model_name,
        inOrderFields=["Text", "Scenario", "Explanation", "Usage_Examples", "Spanish_Translation", "Audio"],
        isCloze=True,
        cardTemplates=[{
            "Name": "Cloze Template",
            "Front": front_template,
            "Back": back_template
        }],
        css=css_content
    )
    print("Model created successfully.")

# Books Path Dataset
books_cards = [
    # Business Strategy
    {
        "deck": "Books_Path::01_Business_Strategy",
        "scenario": "Business Strategy: 7 Powers 📊",
        "text": "The Hamilton Helmer strategy model defines 'Power' as the ability to maintain higher profit margins than competitors, which requires both a {{c1::Benefit}} (value/cash flow) and a {{c1::Barrier}} (competitor prevention).",
        "explanation": "A business attribute only grants 'Power' if it improves cash flow (Benefit) and creates a barrier (Barrier) that prevents competitors from copying or eroding that benefit over time.",
        "usage": "The 7 Powers described in the book are:<ul><li>Scale Economies, Network Economies, Counter-Positioning, Switching Costs, Branding, Cornered Resource, and Process Power.</li></ul>",
        "spanish": "El modelo de estrategia de Hamilton Helmer define 'Poder' como la capacidad de mantener márgenes de ganancia más altos que los competidores, lo que requiere tanto un Beneficio (valor/flujo de caja) como una Barrera (prevención de competidores)."
    },
    {
        "deck": "Books_Path::01_Business_Strategy",
        "scenario": "Business Strategy: The Innovator's Dilemma 💡",
        "text": "The Innovator's Dilemma occurs because successful companies focus on {{c1::sustaining innovations}} (improving products for current clients) and ignore {{c1::disruptive innovations}} until it is too late.",
        "explanation": "Incumbents listen to their high-value customers and invest in sustaining innovations. They ignore cheaper, low-performance disruptive technologies because they have lower profit margins, allowing startups to improve those technologies until they capture the mainstream market.",
        "usage": "Key lessons:<ul><li>Disruptive technologies usually target new, lower-end, or niche markets initially.</li><li>Incumbents rarely pivot fast enough due to structural profit constraints.</li></ul>",
        "spanish": "El dilema del innovador ocurre porque las empresas exitosas se enfocan en innovaciones sostenibles (mejorar productos para clientes actuales) e ignoran las innovaciones disruptivas hasta que es demasiado tarde."
    },
    {
        "deck": "Books_Path::01_Business_Strategy",
        "scenario": "Business Management: High Output Management 🏢",
        "text": "Andy Grove's core principle of management is that a manager's output is the output of the {{c1::organizational units}} under their supervision or influence.",
        "explanation": "A manager should focus their time on high-leverage activities—actions that multiply the efficiency and output of their team (like delegation, training, and planning) rather than performing tasks as an individual contributor.",
        "usage": "Management Leverage concepts:<ul><li>High Leverage: training a team, designing a clear schedule, running an aligned sync.</li><li>Negative Leverage: micromanagement, unorganized meetings, delaying decisions.</li></ul>",
        "spanish": "El principio fundamental de gestión de Andy Grove es que el rendimiento de un gerente es el rendimiento de las unidades organizacionales bajo su supervisión o influencia."
    },
    
    # Communication & Influence
    {
        "deck": "Books_Path::02_Communication_Influence",
        "scenario": "Communication & Sales: Never Split the Difference 🗣️",
        "text": "In negotiation, Chris Voss recommends using {{c1::calibrated questions}} (starting with 'How' or 'What') to give the counterpart the illusion of control while making them solve your problem.",
        "explanation": "Calibrated questions avoid aggressive triggers like 'Why' (which makes people defensive) and force the other party to think about your constraints and propose solutions themselves.",
        "usage": "Standard examples of calibrated questions:<ul><li><code>How am I supposed to do that?</code> (politely pushes back on unreasonable demands)</li><li><code>What about this is important to you?</code> (uncovers hidden motives)</li></ul>",
        "spanish": "En la negociación, Chris Voss recomienda usar preguntas calibradas (que comienzan con 'Cómo' o 'Qué') para dar a la contraparte la ilusión de control mientras hacen que resuelvan tu problema."
    },
    
    # Learning & Productivity
    {
        "deck": "Books_Path::03_Learning_Productivity",
        "scenario": "Productivity & Habits: Atomic Habits 🔄",
        "text": "James Clear argues that the most effective way to change habits is to focus on {{c1::identity-based habits}} (who you want to become) rather than outcome-based habits (what you want to achieve).",
        "explanation": "True behavior change is identity change. You start a habit by deciding the type of person you want to be, and prove it to yourself with small wins. Every action is a vote for your identity.",
        "usage": "Examples of shifting mindsets:<ul><li>Outcome-based: 'I want to read a book a week.'</li><li>Identity-based: 'I am a reader.'</li></ul>",
        "spanish": "James Clear sostiene que la forma más efectiva de cambiar los hábitos es enfocarse en hábitos basados en la identidad (quién quieres llegar a ser) en lugar de hábitos basados en resultados (qué quieres lograr)."
    },
    {
        "deck": "Books_Path::03_Learning_Productivity",
        "scenario": "Learning Mastery: A Mind for Numbers 🧠",
        "text": "Learning requires toggling between the {{c1::focused mode}} (concentrated attention on details) and the {{c1::diffuse mode}} (relaxed, wandering state that allows for creative connections).",
        "explanation": "When you get stuck on a difficult technical problem, continuing to focus intensely can cause the 'Einstellung effect' (blocking a better solution). Relaxing the mind allows the diffuse mode to find new neural pathways.",
        "usage": "How to toggle:<ul><li>Focused: Intensive studying, coding, or calculating.</li><li>Diffuse: Taking a walk, sleeping, or exercising right after intensive work.</li></ul>",
        "spanish": "El aprendizaje requiere alternar entre el modo enfocado (atención concentrada en detalles) y el modo difuso (estado relajado y errante que permite conexiones creativas)."
    },
    {
        "deck": "Books_Path::03_Learning_Productivity",
        "scenario": "Learning Mastery: Make It Stick 📚",
        "text": "The most effective study techniques are {{c1::active retrieval}} (testing yourself) and {{c1::spaced repetition}}, whereas highlighting and re-reading create an {{c1::illusion of competence}}.",
        "explanation": "Memory is strengthened when the brain has to work to retrieve information. Re-reading feels easy, which tricks the brain into thinking it knows the material when it does not.",
        "usage": "Best practices:<ul><li>Use flashcards (Anki) for active retrieval.</li><li>Space review sessions over increasing intervals (days, then weeks).</li></ul>",
        "spanish": "Las técnicas de estudio más efectivas son la recuperación activa (evaluarte a ti mismo) y la repetición espaciada, mientras que subrayar y volver a leer crean una ilusión de competencia."
    },
    {
        "deck": "Books_Path::03_Learning_Productivity",
        "scenario": "Productivity & Focus: Deep Work 🔒",
        "text": "Cal Newport defines {{c1::Deep Work}} as professional activities performed in a state of distraction-free concentration that push cognitive capabilities to their limit and create new value.",
        "explanation": "Deep work is increasingly rare and valuable in our digital economy. Shallow work (emails, meetings, logistics) does not create unique value and is easily replicated.",
        "usage": "Core rules of Deep Work:<ul><li>Work deeply, embrace boredom, quit social media, and minimize shallow tasks.</li></ul>",
        "spanish": "Cal Newport define el Trabajo Profundo como actividades profesionales realizadas en un estado de concentración libre de distracciones que empujan las capacidades cognitivas a su límite."
    },
    
    # AI Engineering
    {
        "deck": "Books_Path::04_AI_Engineering",
        "scenario": "AI Engineering: RAG vs Fine-Tuning 🤖",
        "text": "Chip Huyen states that for foundation models, {{c1::RAG is for facts}} (retrieving dynamic, contextual data) and {{c1::fine-tuning is for form}} (adjusting style, tone, and output formatting).",
        "explanation": "Retrieval-Augmented Generation (RAG) updates the model's knowledge with live, external documents without retraining. Fine-tuning adjusts the model's behavioral patterns, syntax, or tone.",
        "usage": "Examples:<ul><li>Use RAG to query customer database records.</li><li>Use fine-tuning to train a model to output strict JSON according to a specific schema.</li></ul>",
        "spanish": "Chip Huyen afirma que para los modelos fundacionales, RAG es para los hechos (recuperar datos dinámicos y contextuales) y el ajuste fino es para la forma (ajustar el estilo, el tono y el formato)."
    },
    {
        "deck": "Books_Path::04_AI_Engineering",
        "scenario": "AI Engineering: Agentic Pillars 🤖",
        "text": "Valentina Alto defines an AI Agent as an LLM brain supported by three core pillars: {{c1::Planning}} (subtask decomposition), {{c1::Memory}} (context retention), and {{c1::Tools}} (API execution).",
        "explanation": "An agent uses reasoning loops (like ReAct) to plan steps, queries short-term (context window) or long-term (vector database) memory, and calls external tools to interact with the environment.",
        "usage": "Key pillars in action:<ul><li>Planning: Decomposes a goal into subtasks.</li><li>Memory: Stores conversation logs and facts.</li><li>Tools: Executes external APIs or code.</li></ul>",
        "spanish": "Valentina Alto define un Agente de IA como un cerebro de LLM respaldado por tres pilares: Planificación (descomposición de subtareas), Memoria (retención de contexto) y Herramientas (ejecución de APIs)."
    },
    
    # Philosophy & Meaning
    {
        "deck": "Books_Path::05_Philosophy_Meaning",
        "scenario": "Philosophy: Meaning of Life ☀️",
        "text": "Viktor Frankl's Logotherapy asserts that humanity's primary motivational force is the {{c1::search for meaning}} rather than pleasure or power.",
        "explanation": "Even in extreme suffering (like concentration camps), finding meaning—whether in work, love, or the courage to endure suffering—enables psychological survival.",
        "usage": "Core quote:<ul><li>'He who has a why to live can bear almost any how' (Nietzsche, quoted by Frankl).</li></ul>",
        "spanish": "La Logoterapia de Viktor Frankl afirma que la principal fuerza motivadora de la humanidad es la búsqueda de sentido en lugar del placer o el poder."
    },
    {
        "deck": "Books_Path::05_Philosophy_Meaning",
        "scenario": "Philosophy: Strategy & Power ⚔️",
        "text": "Robert Greene's core strategic advice is to remain {{c1::formless}} (adaptable and unpredictable) so that competitors cannot target or plan against you.",
        "explanation": "By not having a fixed shape or visible strategy, you keep others off-balance and remain highly adaptable to changing circumstances.",
        "usage": "Greene's Laws of Power:<ul><li>Law 4: Always say less than necessary.</li><li>Law 48: Assume formlessness.</li></ul>",
        "spanish": "El consejo estratégico central de Robert Greene es permanecer sin forma (adaptable e impredecible) para que los competidores no puedan atacarte ni planificar en tu contra."
    },
    {
        "deck": "Books_Path::05_Philosophy_Meaning",
        "scenario": "Philosophy: Liberation & Pedagogy 📖",
        "text": "Paulo Freire critiques the {{c1::banking concept of education}} (where students are passive depositories for the teacher's knowledge) and advocates for {{c1::problem-posing education}}.",
        "explanation": "The banking model reinforces oppression by treating students as empty objects to be filled. Problem-posing education encourages dialogue, critical consciousness (conscientização), and liberation.",
        "usage": "Core pedagogical advice:<ul><li>Real learning comes from mutual dialogue between teacher and student, analyzing real-world problems.</li></ul>",
        "spanish": "Paulo Freire critica el concepto bancario de la educación (donde los estudiantes son depositarios pasivos del conocimiento del maestro) y aboga por la educación problematizadora."
    }
]

def create_books_decks_and_cards():
    ensure_model_exists()
    
    # Unique deck names
    deck_names = set(card['deck'] for card in books_cards)
    for deck in deck_names:
        print(f"Ensuring deck '{deck}' exists...")
        invoke('createDeck', deck=deck)
        
    print("\nAdding book-based cards...")
    notes = []
    for card in books_cards:
        note = {
            "deckName": card['deck'],
            "modelName": "Engaging_Cloze_Model",
            "fields": {
                "Text": card['text'],
                "Scenario": card['scenario'],
                "Explanation": card['explanation'],
                "Usage_Examples": card['usage'],
                "Spanish_Translation": card['spanish'],
                "Audio": ""
            },
            "options": {
                "allowDuplicate": True
            },
            "tags": ["books_path", card['deck'].split("::")[-1].lower()]
        }
        notes.append(note)
        
    result = invoke('addNotes', notes=notes)
    print(f"\nSuccessfully added {len(result)} book-based cards!")
    for note_id, card in zip(result, books_cards):
        print(f" - Added card '{card['text'][:45]}...' (Note ID: {note_id})")

if __name__ == "__main__":
    create_books_decks_and_cards()
