import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_obsidian_cards = [
    # Communication - NVC
    {
        "deck": "Social_Skills::02_Active_Listening",
        "scenario": "Communication: Nonviolent Communication 🤝",
        "text": "The four components of Nonviolent Communication (NVC) are {{c1::Observation}} (stating facts), {{c2::Feelings}} (expressing emotions), {{c3::Needs}} (universal roots), and {{c4::Requests}} (positive actions).",
        "explanation": "These four components allow us to shift from defensive or aggressive reactions to compassionate connection and honest self-expression.",
        "usage": "NVC Core Flow:<ul><li>Observation: Describe what happened without judgment.</li><li>Feelings: Express how you feel (not thoughts).</li><li>Needs: Identify what need is driving the feeling.</li><li>Requests: Ask for concrete actions.</li></ul>",
        "spanish": "Los cuatro componentes de la Comunicación No Violenta (CNV) son la Observación (declarar hechos), los Sentimientos (expresar emociones), las Necesidades (raíces universales) y las Peticiones (acciones positivas).",
        "tags": ["social_skills", "communication", "nvc"]
    },
    # Communication - Radical Candor
    {
        "deck": "English::02_Professional::Giving_Feedback",
        "scenario": "Communication: Radical Candor 📊",
        "text": "According to Kim Scott's Radical Candor framework, effective leadership requires balancing the two dimensions of {{c1::Care Personally}} (Cuidar Personalmente) and {{c2::Challenge Directly}} (Desafiar Directamente).",
        "explanation": "Failing to challenge directly while caring personally leads to 'Empatía Ruinosa' (Ruinous Empathy), which prevents growth. Challenging directly without caring leads to 'Agresión Ofensiva' (Obnoxious Aggression).",
        "usage": "Radical Candor is the 'sweet spot' where you care enough about someone to tell them the uncomfortable truth to help them grow.",
        "spanish": "Según el marco de Sinceridad Radical de Kim Scott, el liderazgo efectivo requiere equilibrar las dos dimensiones de Cuidar Personalmente y Desafiar Directamente.",
        "tags": ["business_english", "professional", "radical_candor", "feedback"]
    },
    
    # Memory - Einstellung Effect
    {
        "deck": "Books_Path::03_Learning_Productivity",
        "scenario": "Memory & Learning: Einstellung Effect 🧠",
        "text": "In A Mind for Numbers, Barbara Oakley explains that the {{c1::Einstellung Effect}} is a mental roadblock where a pre-existing, incorrect idea prevents you from seeing a better solution.",
        "explanation": "Once your brain has paved a neural path for solving a problem, it becomes hard to look at the problem differently unless you step away and switch to the diffuse mode of thinking.",
        "usage": "This commonly happens during exams when you get stuck on a wrong approach and cannot see the obvious solution. Stepping away resets your focus.",
        "spanish": "En A Mind for Numbers, Barbara Oakley explica que el Efecto Einstellung es un obstáculo mental en el que una idea preexistente e incorrecta te impide ver una mejor solución.",
        "tags": ["books_path", "learning_productivity", "einstellung_effect"]
    },
    # Memory - Become a SuperLearner
    {
        "deck": "Books_Path::03_Learning_Productivity",
        "scenario": "Memory: Visual Encoding 👁️",
        "text": "According to Become a SuperLearner, the human brain remembers visual information best because the best markers for long-term memory are {{c1::strange, bizarre, or emotionally connected}} images.",
        "explanation": "Humans evolved with highly robust visual processing for survival (hunting and gathering). Creating detailed, experiential visual markers leads to a higher number of neural connections.",
        "usage": "To remember the name 'Barbara', visualize her holding a giant, glowing 'barbed wire' (strange and highly visual marker).",
        "spanish": "Según Become a SuperLearner, el cerebro humano recuerda mejor la información visual porque los mejores marcadores para la memoria a largo plazo son imágenes extrañas, bizarras o conectadas emocionalmente.",
        "tags": ["books_path", "learning_productivity", "superlearner", "memory_encoding"]
    }
]

cards.extend(new_obsidian_cards)

with open(database_file, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"Successfully appended {len(new_obsidian_cards)} Obsidian cards to {database_file}.")
