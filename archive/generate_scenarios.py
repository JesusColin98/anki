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

# Cards dataset
cards_to_create = [
    # Coffee Shop
    {
        "deck": "English::01_Daily_Life::Coffee_Shop",
        "scenario": "At the Coffee Shop ☕",
        "text": "Could I get a medium latte {{c1::to go}}, please?",
        "explanation": "<strong>to go</strong> is used when you want to take your food or drink out of the shop instead of consuming it there.",
        "usage": "Pattern: <code>Could I get a [size] [drink] to go, please?</code><ul><li><code>Could I get a large Americano to go, please?</code></li><li><code>Could I get a small espresso to go, please?</code></li></ul>",
        "spanish": "¿Me da un latte mediano para llevar, por favor?"
    },
    {
        "deck": "English::01_Daily_Life::Coffee_Shop",
        "scenario": "At the Coffee Shop ☕",
        "text": "I'd like to {{c1::substitute}} whole milk {{c1::with}} oat milk, please.",
        "explanation": "<strong>substitute A with B</strong> means to use B instead of A. This is the standard way to customize food or drink orders.",
        "usage": "Pattern: <code>substitute [original] with [alternative]</code><ul><li><code>Can I substitute white bread with wheat bread?</code></li><li><code>I'd like to substitute fries with a side salad, please.</code></li></ul>",
        "spanish": "Me gustaría cambiar la leche entera por leche de avena, por favor."
    },
    {
        "deck": "English::01_Daily_Life::Coffee_Shop",
        "scenario": "At the Coffee Shop ☕",
        "text": "Do you have any {{c1::sugar-free}} syrup options?",
        "explanation": "<strong>sugar-free</strong> means containing no sugar. Syrups are sweet liquid flavorings added to coffee (like vanilla or caramel).",
        "usage": "Pattern: <code>[adjective]-free</code> (e.g., gluten-free, caffeine-free, tax-free)<ul><li><code>Is this cookie gluten-free?</code></li><li><code>I'd prefer decaf, do you have caffeine-free coffee?</code></li></ul>",
        "spanish": "¿Tienen opciones de jarabe sin azúcar?"
    },
    {
        "deck": "English::01_Daily_Life::Coffee_Shop",
        "scenario": "At the Coffee Shop ☕",
        "text": "Can I {{c1::pay by card}}?",
        "explanation": "<strong>pay by card</strong> means to pay using a credit or debit card rather than cash.",
        "usage": "Pattern: <code>pay by [method]</code> (e.g., pay by card, pay by phone, pay by check) but <code>pay in cash</code><ul><li><code>You can pay by phone using Apple Pay.</code></li><li><code>Is it cheaper if I pay in cash?</code></li></ul>",
        "spanish": "¿Puedo pagar con tarjeta?"
    },
    
    # Supermarket
    {
        "deck": "English::01_Daily_Life::Supermarket",
        "scenario": "At the Supermarket 🛒",
        "text": "Where can I find the {{c1::dairy aisle}}?",
        "explanation": "An <strong>aisle</strong> is a passage between rows of shelves in a supermarket. <strong>dairy</strong> refers to milk-based products (cheese, yogurt, butter).",
        "usage": "Pattern: <code>[category] aisle</code> (e.g., baking aisle, produce aisle, frozen food aisle)<ul><li><code>The sugar is in the baking aisle.</code></li><li><code>Where is the produce aisle? I need some fresh apples.</code></li></ul>",
        "spanish": "¿Dónde puedo encontrar el pasillo de lácteos?"
    },
    {
        "deck": "English::01_Daily_Life::Supermarket",
        "scenario": "At the Supermarket 🛒",
        "text": "Are these apples {{c1::on sale}} this week?",
        "explanation": "<strong>on sale</strong> means available at a reduced price (discounted). *Do not confuse with 'for sale', which just means available to buy.",
        "usage": "Pattern: <code>on sale</code> (discounted) vs <code>for sale</code> (available to buy)<ul><li><code>These shoes are on sale for 20% off.</code></li><li><code>Is that classic car for sale or is it just on display?</code></li></ul>",
        "spanish": "¿Están estas manzanas en oferta esta semana?"
    },
    {
        "deck": "English::01_Daily_Life::Supermarket",
        "scenario": "At the Supermarket 🛒",
        "text": "Is there a limit on how many items I can bring to the {{c1::express lane}}?",
        "explanation": "An <strong>express lane</strong> is a checkout counter reserved for customers buying only a few items (e.g. 10 or less) to speed up service.",
        "usage": "Pattern: <code>express lane</code> (typically labeled '10 items or less' or '15 items or fewer')<ul><li><code>I only have 3 items, so I will use the express lane.</code></li><li><code>You can't go there; the express lane is for quick checkouts.</code></li></ul>",
        "spanish": "¿Hay un límite de cuántos artículos puedo llevar a la caja rápida?"
    },
    
    # Office & Meetings
    {
        "deck": "English::02_Professional::Office_Meetings",
        "scenario": "Office & Meetings 💼",
        "text": "Let's {{c1::touch base}} tomorrow to discuss the updates.",
        "explanation": "<strong>touch base</strong> is a common business idiom meaning to briefly contact or meet with someone to talk about progress.",
        "usage": "Pattern: <code>touch base with [someone] [time]</code><ul><li><code>I need to touch base with my manager before the client call.</code></li><li><code>Let's touch base next week.</code></li></ul>",
        "spanish": "Póngamonos en contacto mañana para discutir las actualizaciones."
    },
    {
        "deck": "English::02_Professional::Office_Meetings",
        "scenario": "Office & Meetings 💼",
        "text": "We need to {{c1::push back}} the meeting to 3 PM.",
        "explanation": "<strong>push back</strong> means to postpone or reschedule an event to a later time or date.",
        "usage": "Pattern: <code>push back [event] to [time/date]</code><ul><li><code>Can we push back the project deadline by two days?</code></li><li><code>They had to push back the launch due to technical issues.</code></li></ul>",
        "spanish": "Necesitamos posponer la reunión para las 3 PM."
    },
    {
        "deck": "English::02_Professional::Office_Meetings",
        "scenario": "Office & Meetings 💼",
        "text": "I'll {{c1::follow up with}} you via email once I get the data.",
        "explanation": "<strong>follow up with</strong> means to contact someone again to provide further information, verify progress, or request updates.",
        "usage": "Pattern: <code>follow up with [someone] on/via [method]</code><ul><li><code>The doctor will follow up with you next month.</code></li><li><code>I will follow up with the client on the contract details tomorrow.</code></li></ul>",
        "spanish": "Le daré seguimiento por correo electrónico una vez que obtenga los datos."
    },
    
    # Dating & Socializing
    {
        "deck": "English::03_Socializing::Dating",
        "scenario": "Dating & Socializing 💬",
        "text": "Would you like to {{c1::grab a drink}} sometime?",
        "explanation": "<strong>grab a drink</strong> is a casual, friendly way to invite someone to go out for a beverage (coffee, beer, or cocktails).",
        "usage": "Pattern: <code>grab a [item]</code> (e.g. grab a coffee, grab a bite to eat, grab lunch)<ul><li><code>Let's grab a coffee this afternoon.</code></li><li><code>Do you want to grab a bite to eat after work?</code></li></ul>",
        "spanish": "¿Te gustaría ir a tomar algo alguna vez?"
    },
    {
        "deck": "English::03_Socializing::Dating",
        "scenario": "Dating & Socializing 💬",
        "text": "I had a great time tonight, we should {{c1::do this again}}.",
        "explanation": "<strong>do this again</strong> is a friendly, low-pressure phrase used at the end of a good social gathering or date to show interest in hanging out again.",
        "usage": "Pattern: <code>we should do this again [sometime/soon]</code><ul><li><code>I really enjoyed the museum. We should do this again sometime!</code></li><li><code>It was great catching up. We should do this again soon.</code></li></ul>",
        "spanish": "La pasé genial esta noche, deberíamos repetir esto."
    }
]

def create_decks_and_cards():
    ensure_model_exists()
    
    # We collect all unique deck names to create them first
    deck_names = set(card['deck'] for card in cards_to_create)
    for deck in deck_names:
        print(f"Ensuring deck '{deck}' exists...")
        invoke('createDeck', deck=deck)
        
    print("\nAdding cards...")
    notes = []
    for card in cards_to_create:
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
            "tags": ["english_scenario", card['deck'].split("::")[-1].lower()]
        }
        notes.append(note)
        
    result = invoke('addNotes', notes=notes)
    print(f"\nSuccessfully added {len(result)} cards!")
    for note_id, card in zip(result, cards_to_create):
        print(f" - Added card '{card['text'][:40]}...' (Note ID: {note_id})")

if __name__ == "__main__":
    create_decks_and_cards()
