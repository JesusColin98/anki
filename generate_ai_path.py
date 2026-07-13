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
    # (CSS and template generation fallback if the model doesn't exist yet)
    # Note: we reuse the same engaging model definition from generate_scenarios.py
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
    <h3>Usage Pattern & Examples</h3>
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

# AI Path Dataset
ai_cards = [
    # Classical ML
    {
        "deck": "AI_Learning_Path::01_Classical_ML",
        "scenario": "Classical ML: Optimization 📉",
        "text": "The Gradient Descent parameter update formula is {{c1::\\(\\theta_{t+1} = \\theta_t - \\eta \\nabla J(\\theta_t)\\)}}",
        "explanation": "This formula iteratively adjusts model parameters (weights) \\(\\theta\\) to minimize the loss function \\(J(\\theta)\\). The gradient \\(\\nabla J(\\theta_t)\\) points in the direction of steepest increase, so subtracting it steps down toward the minimum, scaled by learning rate \\(\\eta\\).",
        "usage": "Core formula breakdown:<ul><li>\\(\\theta\\): Parameter weight vector</li><li>\\(\\eta\\): Learning rate (determines step size)</li><li>\\(J(\\theta)\\): Loss/objective function</li><li>\\(\\nabla J(\\theta_t)\\): Gradient vector at time step t</li></ul>",
        "spanish": "La fórmula de actualización de parámetros en el Descenso de Gradiente es \\(\\theta_{t+1} = \\theta_t - \\eta \\nabla J(\\theta_t)\\)."
    },
    {
        "deck": "AI_Learning_Path::01_Classical_ML",
        "scenario": "Classical ML: Optimization 📉",
        "text": "The Adam optimizer calculates adaptive learning rates by combining {{c1::Momentum}} (moving average of past gradients) and {{c1::RMSProp}} (moving average of past squared gradients).",
        "explanation": "Adam (Adaptive Moment Estimation) tracks both the first moment (mean of gradients, similar to Momentum) and the second moment (uncentered variance of gradients, similar to RMSProp) to scale steps independently for each weight.",
        "usage": "Mathematical concept:<ul><li>Momentum term helps speed up optimization in direction of consistent gradients.</li><li>RMSProp term dampens updates in highly volatile directions, preventing exploding parameters.</li></ul>",
        "spanish": "El optimizador Adam calcula tasas de aprendizaje adaptativas combinando Momentum (promedio móvil de gradientes pasados) y RMSProp (promedio móvil de gradientes pasados al cuadrado)."
    },
    
    # LLM Fundamentals
    {
        "deck": "AI_Learning_Path::02_LLM_Fundamentals",
        "scenario": "LLM Fundamentals: Core Math 🧠",
        "text": "The Scaled Dot-Product Attention is defined mathematically as {{c1::\\(\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V\\)}}",
        "explanation": "This attention formula matches Queries (Q) against Keys (K) to create an attention score matrix. The matrix is divided by scaling factor \\(\\sqrt{d_k}\\) to prevent dot product values from growing too large, which would push the softmax into regions with vanishing gradients.",
        "usage": "Formula component details:<ul><li>\\(Q, K, V\\): Query, Key, and Value matrices.</li><li>\\(d_k\\): Dimensionality of the key vectors.</li><li>\\(\\text{softmax}\\): Normalizes attention weights to sum up to 1.</li></ul>",
        "spanish": "La atención de producto punto escalada se define matemáticamente como \\(\\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V\\)."
    },
    {
        "deck": "AI_Learning_Path::02_LLM_Fundamentals",
        "scenario": "LLM Fundamentals: Optimization 🚀",
        "text": "During auto-regressive decoding, the {{c1::KV Cache}} is used to store past key and value vectors, reducing attention computation time complexity from {{c1::\\(O(N^2)\\)}} to {{c1::\\(O(N)\\)}}.",
        "explanation": "At each decoding step, LLMs generate one token at a time. Instead of recalculating Queries, Keys, and Values for all previous tokens in the sequence, the Key and Value vectors are saved in GPU memory (cached). Only the Query of the new token needs to match against the cached Keys and Values.",
        "usage": "Implications:<ul><li>Saves massive compute during inference.</li><li>Trades compute overhead for high GPU memory consumption.</li><li>Optimized by architectures like Grouped-Query Attention (GQA).</li></ul>",
        "spanish": "Durante la decodificación autorregresiva, el KV Cache se usa para almacenar vectores clave y de valor pasados, reduciendo la complejidad del cálculo de atención de O(N^2) a O(N)."
    },
    
    # Advanced LLM
    {
        "deck": "AI_Learning_Path::03_Advanced_LLM",
        "scenario": "Advanced LLM: Fine-Tuning ⚙️",
        "text": "Low-Rank Adaptation (LoRA) freeze pre-trained weights and represents weight updates via two low-rank matrices as {{c1::\\(\\Delta W = B \\cdot A\\)}}",
        "explanation": "For a weight matrix of size \\(d \\times k\\), updating weights directly is very expensive. LoRA decomposes the update \\(\\Delta W\\) into product of matrices \\(B\\) (size \\(d \\times r\\)) and \\(A\\) (size \\(r \\times k\\)), where rank \\(r \\ll \\min(d, k)\\). Only \\(A\\) and \\(B\\) are updated.",
        "usage": "Core math details:<ul><li>Original Weights \\(W_0\\) remain frozen.</li><li>Forward pass: \\(h = W_0 x + \\Delta W x = W_0 x + B A x\\).</li><li>Reduces active parameter counts during fine-tuning by up to 99%.</li></ul>",
        "spanish": "La adaptación de bajo rango (LoRA) congela los pesos preentrenados y representa las actualizaciones de peso mediante dos matrices de bajo rango como \\(\\Delta W = B \\cdot A\\)."
    },
    {
        "deck": "AI_Learning_Path::03_Advanced_LLM",
        "scenario": "Advanced LLM: Alignment ⚖️",
        "text": "Direct Preference Optimization (DPO) bypasses reinforcement learning by defining a closed-form loss over {{c1::preference pairs}} of chosen and rejected responses.",
        "explanation": "Traditional RLHF requires training a reward model, then optimizing the LLM using complex PPO reinforcement learning. DPO mathematically demonstrates that you can optimize the LLM directly on chosen/rejected preference data, removing the need for a separate reward model or PPO training loop.",
        "usage": "DPO characteristics:<ul><li>More stable and faster to train than PPO.</li><li>Optimizes using a simple binary cross-entropy loss directly on the LLM policy's log probabilities.</li></ul>",
        "spanish": "La optimización de preferencia directa (DPO) evita el aprendizaje por refuerzo definiendo una pérdida de forma cerrada sobre pares de preferencia de respuestas elegidas y rechazadas."
    },
    
    # Agentic Systems
    {
        "deck": "AI_Learning_Path::04_Agentic_Systems",
        "scenario": "Agentic Systems: Planning 🤖",
        "text": "The ReAct framework combines reasoning and acting by generating alternating sequences of {{c1::Thought}}, {{c1::Action}}, and {{c1::Observation}}.",
        "explanation": "ReAct (Reason + Act) prompts the LLM to think step-by-step before executing any actions (such as API calls or tool invocation). The model writes a 'Thought', calls a tool ('Action'), reads the output ('Observation'), and repeats this loop until it reaches a conclusion.",
        "usage": "Example trace:<ul><li><strong>Thought</strong>: I need to find the current weather in Paris.</li><li><strong>Action</strong>: <code>weather_search('Paris')</code></li><li><strong>Observation</strong>: Paris is currently 18°C and raining.</li><li><strong>Thought</strong>: Now I can answer the user...</li></ul>",
        "spanish": "El marco ReAct combina el razonamiento y la acción mediante la generación de secuencias alternas de Pensamiento (Thought), Acción (Action) y Observación (Observation)."
    },
    {
        "deck": "AI_Learning_Path::04_Agentic_Systems",
        "scenario": "Agentic Systems: Memory 🧠",
        "text": "In agentic architectures, {{c1::episodic memory}} records execution histories and user interactions, while {{c1::semantic memory}} represents generalized factual facts, system prompts, or core instructions.",
        "explanation": "Episodic memory refers to specific events and past steps the agent experienced (implemented via vector search of past chat logs). Semantic memory holds permanent generalized concepts, templates, or instructions (stored in the system prompt or static databases).",
        "usage": "Key distinction:<ul><li>Episodic: 'What did I say to this user five steps ago?'</li><li>Semantic: 'What is the system guideline for writing code?'</li></ul>",
        "spanish": "En las arquitecturas de agentes, la memoria episódica registra los historiales de ejecución y las interacciones del usuario, mientras que la memoria semántica representa hechos factuales generalizados, prompts del sistema o instrucciones principales."
    }
]

def create_ai_decks_and_cards():
    ensure_model_exists()
    
    # Unique deck names
    deck_names = set(card['deck'] for card in ai_cards)
    for deck in deck_names:
        print(f"Ensuring deck '{deck}' exists...")
        invoke('createDeck', deck=deck)
        
    print("\nAdding AI/ML cards...")
    notes = []
    for card in ai_cards:
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
            "tags": ["ai_learning_path", card['deck'].split("::")[-1].lower()]
        }
        notes.append(note)
        
    result = invoke('addNotes', notes=notes)
    print(f"\nSuccessfully added {len(result)} AI/ML learning cards!")
    for note_id, card in zip(result, ai_cards):
        print(f" - Added card '{card['text'][:45]}...' (Note ID: {note_id})")

if __name__ == "__main__":
    create_ai_decks_and_cards()
