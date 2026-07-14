import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_english_cards = [
    # Beginner (A1/A2)
    {
        "deck": "English::01_Daily_Life::Ordering_Food",
        "scenario": "English Beginner: Ordering Food 🍔",
        "text": "Can I get a cheeseburger and {{c1::a side of}} fries, please?",
        "explanation": "<strong>a side of</strong> is the standard, natural collocation to order an additional side portion of food alongside your main dish.",
        "usage": "Pattern: <code>a side of [food]</code><ul><li><code>I'd like a steak with a side of mashed potatoes.</code></li><li><code>Can I get a side of ranch dressing?</code></li></ul>",
        "spanish": "¿Me da una hamburguesa con queso y una porción de papas fritas, por favor?",
        "tags": ["english_scenario", "beginner", "ordering_food"]
    },
    {
        "deck": "English::01_Daily_Life::Asking_Directions",
        "scenario": "English Beginner: Asking for Directions 🗺️",
        "text": "Excuse me, could you tell me how to {{c1::get to}} the nearest train station?",
        "explanation": "<strong>get to</strong> is the most common conversational phrasal verb meaning to reach or arrive at a destination.",
        "usage": "Pattern: <code>get to [place]</code><ul><li><code>How do I get to the museum from here?</code></li><li><code>It takes 20 minutes to get to the office.</code></li></ul>",
        "spanish": "Disculpe, ¿podría decirme cómo llegar a la estación de tren más cercana?",
        "tags": ["english_scenario", "beginner", "directions"]
    },
    
    # Intermediate (B1/B2)
    {
        "deck": "English::01_Daily_Life::Airport",
        "scenario": "English Intermediate: Airport Check-in ✈️",
        "text": "I would like to check in this suitcase, and I have one {{c1::carry-on bag}} to bring into the cabin.",
        "explanation": "A <strong>carry-on bag</strong> (or hand luggage) is the small suitcase or backpack that passengers are permitted to bring onto the plane with them rather than checking it.",
        "usage": "Pattern: <code>carry-on bag / carry-on luggage</code><ul><li><code>Make sure your carry-on bag fits in the overhead bin.</code></li><li><code>I only travel with a carry-on bag to save time.</code></li></ul>",
        "spanish": "Me gustaría registrar esta maleta, y tengo una maleta de mano para llevar en la cabina.",
        "tags": ["english_scenario", "intermediate", "airport"]
    },
    {
        "deck": "English::01_Daily_Life::Hotel",
        "scenario": "English Intermediate: Hotel Check-in 🏨",
        "text": "I have a reservation under the name Perez, and I'd like to check if my room is {{c1::ready for check-in}}.",
        "explanation": "<strong>ready for check-in</strong> means that the hotel room has been cleaned, inspected, and is fully prepared for the guest to enter and receive their key.",
        "usage": "Pattern: <code>ready for check-in</code><ul><li><code>Is my room ready for check-in? Standard check-in is at 3 PM.</code></li><li><code>The front desk agent told me the room is not ready yet.</code></li></ul>",
        "spanish": "Tengo una reservación a nombre de Pérez, y me gustaría verificar si mi habitación está lista para registrarme.",
        "tags": ["english_scenario", "intermediate", "hotel"]
    },
    
    # Advanced (C1/C2)
    {
        "deck": "English::02_Professional::Negotiations",
        "scenario": "English Advanced: Contract Negotiation 📑",
        "text": "We cannot agree to these terms unless you include a {{c1::termination clause}} for convenience.",
        "explanation": "A <strong>termination clause</strong> is a contract provision that defines the conditions under which the agreement can be ended. <strong>For convenience</strong> means it can be terminated without needing a specific cause or breach.",
        "usage": "Pattern: <code>termination clause / terminate for convenience</code><ul><li><code>The contract contains a 30-day termination clause.</code></li><li><code>Either party may terminate the agreement for convenience with written notice.</code></li></ul>",
        "spanish": "No podemos aceptar estos términos a menos que incluya una cláusula de rescisión por conveniencia.",
        "tags": ["english_scenario", "advanced", "negotiations"]
    },
    {
        "deck": "English::02_Professional::Conflict_Resolution",
        "scenario": "English Advanced: Conflict Resolution 🤝",
        "text": "I appreciate your perspective, so let's find a {{c1::middle ground}} that addresses both of our concerns.",
        "explanation": "<strong>middle ground</strong> is a common idiom meaning a compromise or a set of mutual concessions between two opposing viewpoints.",
        "usage": "Pattern: <code>find a middle ground / reach a middle ground</code><ul><li><code>After hours of debate, we finally found a middle ground.</code></li><li><code>It is difficult to reach a middle ground on this budget issue.</code></li></ul>",
        "spanish": "Aprecio tu perspectiva, así que busquemos un punto medio que aborde ambas preocupaciones.",
        "tags": ["english_scenario", "advanced", "conflict_resolution"]
    }
]

cards.extend(new_english_cards)

with open(database_file, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"Successfully appended {len(new_english_cards)} English cards to {database_file}.")
