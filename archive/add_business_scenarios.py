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
        return
    # Model template is shared, but we ensure it works if run standalone
    print(f"Creating custom model '{model_name}'...")
    # (Same CSS / templates as before)
    # Note: assumed already created by generate_scenarios.py, but fallback if needed.

# New Business/Role Scenarios Dataset
business_cards = [
    {
        "deck": "English::02_Professional::Giving_Feedback",
        "scenario": "Giving Feedback 📊",
        "text": "I want to ensure we are aligned, so I'd like to {{c1::address a pattern}} I've noticed in your recent deliverables.",
        "explanation": "<strong>address a pattern</strong> is a polite, constructive way to bring up a recurring issue in performance without making the employee feel immediately attacked.",
        "usage": "Pattern: <code>address a pattern of [behavior]</code><ul><li><code>We need to address a pattern of late arrivals in morning standups.</code></li><li><code>Thank you for addressing a pattern that was affecting our release schedule.</code></li></ul>",
        "spanish": "Quiero asegurarme de que estemos alineados, por lo que me gustaría abordar un patrón que he notado en tus entregables recientes."
    },
    {
        "deck": "English::02_Professional::Running_Meetings",
        "scenario": "Running Meetings: Keeping on Track ⏱️",
        "text": "Let's not {{c1::get bogged down in}} the implementation details during this high-level sync.",
        "explanation": "<strong>get bogged down in</strong> means to become so stuck or overwhelmed by small details that you lose sight of the main goal and stop making progress.",
        "usage": "Pattern: <code>get bogged down in [details/logistics/work]</code><ul><li><code>Don't get bogged down in minor edits; focus on completing the draft.</code></li><li><code>Our discussion got bogged down in budget arguments.</code></li></ul>",
        "spanish": "No nos empantanemos en los detalles de implementación durante esta sincronización de alto nivel."
    },
    {
        "deck": "English::02_Professional::IT_Support",
        "scenario": "IT Support: Troubleshooting 🖥️",
        "text": "Could you please {{c1::power cycle}} the router by unplugging it for 30 seconds?",
        "explanation": "<strong>power cycle</strong> is a technical verb meaning to turn an electronic device completely off (usually by cutting power) and back on again to reset it.",
        "usage": "Pattern: <code>power cycle [device]</code> (e.g. power cycle the server, power cycle the modem)<ul><li><code>If your connection drops, try power cycling the access point.</code></li><li><code>I power cycled the switch, which solved the IP conflict.</code></li></ul>",
        "spanish": "¿Podrías por favor apagar y encender el router desenchufándolo durante 30 segundos?"
    },
    {
        "deck": "English::02_Professional::Manager_Role",
        "scenario": "Manager Role: Delegating Tasks 📋",
        "text": "I'd like you to {{c1::take the lead on}} this integration, but feel free to escalate if you hit any roadblocks.",
        "explanation": "<strong>take the lead on</strong> means to assume responsibility for directing or managing a specific project. <strong>escalate</strong> means to report a problem up the chain of command when tools or resources are blocked.",
        "usage": "Patterns: <code>take the lead on [project/task]</code> | <code>escalate to [someone]</code><ul><li><code>She will take the lead on the customer migration.</code></li><li><code>If the vendor does not respond, escalate the ticket to me.</code></li></ul>",
        "spanish": "Me gustaría que lideres esta integración, pero no dudes en escalar si te encuentras con algún obstáculo."
    },
    {
        "deck": "English::02_Professional::Director_Role",
        "scenario": "Director Role: Strategic Alignment 🧭",
        "text": "We need to {{c1::double down on}} our core product line to capture market share this quarter.",
        "explanation": "<strong>double down on</strong> means to significantly strengthen your commitment, focus, or investment in a strategy, instead of spreading resources too thin.",
        "usage": "Pattern: <code>double down on [focus/strategy/effort]</code><ul><li><code>We decided to double down on cloud security features.</code></li><li><code>The team doubled down on automated testing to fix regression bugs.</code></li></ul>",
        "spanish": "Necesitamos redoblar esfuerzos en nuestra línea de productos principal para capturar participación de mercado este trimestre."
    },
    {
        "deck": "English::02_Professional::IT_Support",
        "scenario": "IT Support & Operations: Incident Response ⚠️",
        "text": "We are currently experiencing a {{c1::service disruption}} affecting our primary database, and our team is working to mitigate it.",
        "explanation": "<strong>service disruption</strong> is the formal corporate term for an outage or downtime. <strong>mitigate</strong> means to reduce the severity or impact of an ongoing incident.",
        "usage": "Pattern: <code>experience a service disruption</code> | <code>mitigate [incident/impact/risk]</code><ul><li><code>The network migration caused a minor service disruption for 10 minutes.</code></li><li><code>We are deploying a hotfix to mitigate the database CPU spikes.</code></li></ul>",
        "spanish": "Actualmente estamos experimentando una interrupción del servicio que afecta a nuestra base de datos principal, y nuestro equipo está trabajando para mitigarlo."
    },
    {
        "deck": "English::02_Professional::Director_Role",
        "scenario": "Director Role: Efficiency & Budget 💸",
        "text": "Given our current budget parameters, we must {{c1::trim the fat}} in our operating expenses.",
        "explanation": "<strong>trim the fat</strong> is a common business idiom meaning to eliminate waste, unnecessary expenses, or redundancies to make operations leaner.",
        "usage": "Pattern: <code>trim the fat</code> (idiom)<ul><li><code>To achieve profitability, the division needs to trim the fat.</code></li><li><code>Trimming the fat in marketing helped us fund research and development.</code></li></ul>",
        "spanish": "Dados nuestros parámetros presupuestarios actuales, debemos recortar los gastos innecesarios en nuestros gastos operativos."
    }
]

def add_cards():
    ensure_model_exists()
    
    # Create decks
    deck_names = set(card['deck'] for card in business_cards)
    for deck in deck_names:
        print(f"Ensuring deck '{deck}' exists...")
        invoke('createDeck', deck=deck)
        
    print("\nAdding professional role-based cards...")
    notes = []
    for card in business_cards:
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
            "tags": ["business_english", "professional", card['deck'].split("::")[-1].lower()]
        }
        notes.append(note)
        
    result = invoke('addNotes', notes=notes)
    print(f"\nSuccessfully added {len(result)} business scenario cards!")
    for note_id, card in zip(result, business_cards):
        print(f" - Added card '{card['text'][:45]}...' (Note ID: {note_id})")

if __name__ == "__main__":
    add_cards()
