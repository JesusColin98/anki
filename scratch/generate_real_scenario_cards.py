import json
from pathlib import Path

root = Path(r"C:\Users\jesus\anki")
index_path = root / "decks" / "index.json"

with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_paths = {item["path"] for item in data.get("decks", [])}

# Create four large decks with realistic scenario cards.

categories = []

# 1) Daily life
scenarios_daily = [
    ("At the supermarket", "en el supermercado"),
    ("At the bakery", "en la panadería"),
    ("At the pharmacy", "en la farmacia"),
    ("At the bank", "en el banco"),
    ("At the post office", "en la oficina de correos"),
    ("At the farmer's market", "en el mercado"),
    ("At the laundry", "en la lavandería"),
    ("At the gas station", "en la gasolinera"),
    ("At the library", "en la biblioteca"),
    ("At the gym", "en el gimnasio"),
    ("At the coffee shop", "en la cafetería"),
    ("At the doctor's office", "en la consulta del médico"),
    ("At the apartment office", "en la oficina del edificio"),
    ("At the hair salon", "en la peluquería"),
    ("At the dry cleaner", "en la tintorería"),
    ("At the electronics store", "en la tienda de electrónica"),
    ("At the clothing store", "en la tienda de ropa"),
    ("At the school office", "en la oficina escolar"),
    ("At the train station", "en la estación de tren"),
    ("At the bus stop", "en la parada de autobús"),
    ("At the neighborhood shop", "en la tienda del barrio"),
    ("At the pet store", "en la tienda de mascotas"),
    ("At the hardware store", "en la ferretería"),
    ("At the car wash", "en el lavado de coches"),
    ("At the convenience store", "en la tienda de conveniencia"),
]
items_daily = [
    "bread", "milk", "soap", "toilet paper", "coffee", "eggs", "cheese", "apples", "cereal", "shampoo",
    "toothpaste", "bandages", "medicine", "stamps", "envelopes", "tickets", "batteries", "gloves", "detergent", "paper towels",
    "sugar", "salt", "rice", "pasta", "yogurt", "juice", "fruit", "vegetables", "water", "trash bags"
]
patterns_daily = [
    ("Could you help me find {item}?", "¿Podrías ayudarme a encontrar {item}?"),
    ("I’m looking for {item}.", "Estoy buscando {item}."),
    ("Do you have any {item} today?", "¿Tienes {item} hoy?"),
    ("Is this {item} on sale?", "¿Está {item} en oferta?"),
    ("How much is this {item}?", "¿Cuánto cuesta este {item}?"),
    ("I need {item} for tonight.", "Necesito {item} para esta noche."),
    ("Can I get {item}, please?", "¿Puedo conseguir {item}, por favor?"),
    ("Where can I find {item}?", "¿Dónde puedo encontrar {item}?"),
    ("I’m not sure which {item} to choose.", "No estoy seguro de qué {item} elegir."),
    ("Could you point me to the {item}?", "¿Podrías indicarme dónde está {item}?"),
]

# 2) Workplace
scenarios_work = [
    ("In a project kickoff", "en un inicio de proyecto"),
    ("In a status meeting", "en una reunión de estado"),
    ("In a client call", "en una llamada con un cliente"),
    ("In a design review", "en una revisión de diseño"),
    ("In a budget discussion", "en una discusión de presupuesto"),
    ("In an onboarding session", "en una sesión de incorporación"),
    ("In a support escalation", "en una escalación de soporte"),
    ("In a hiring interview", "en una entrevista de contratación"),
    ("In a performance review", "en una revisión de desempeño"),
    ("In a cross-functional sync", "en una reunión entre funciones"),
    ("In an email follow-up", "en un seguimiento por correo"),
    ("During a deadline discussion", "durante una discusión de plazos"),
    ("In a training session", "en una sesión de capacitación"),
    ("In an operations review", "en una revisión operativa"),
    ("In a product demo", "en una demo de producto"),
    ("In a sales negotiation", "en una negociación comercial"),
    ("In a stakeholder update", "en una actualización a stakeholders"),
    ("In a retrospective", "en una retrospectiva"),
    ("In a planning meeting", "en una reunión de planificación"),
    ("During a team stand-up", "durante el stand-up del equipo"),
    ("In a vendor meeting", "en una reunión con proveedores"),
    ("In a launch prep", "en la preparación de un lanzamiento"),
    ("In a risk review", "en una revisión de riesgos"),
    ("In a handoff", "en una transferencia de trabajo"),
    ("In a conflict resolution", "en una resolución de conflictos"),
]
items_work = [
    "the timeline", "the priorities", "the requirements", "the draft", "the budget", "the schedule", "the milestone", "the handoff", "the data", "the report",
    "the proposal", "the scope", "the deliverable", "the blocker", "the dependency", "the risk", "the owner", "the action items", "the feedback", "the decision",
    "the update", "the next step", "the logistics", "the timeline", "the estimate", "the backlog", "the issue", "the version", "the backlog", "the notes"
]
patterns_work = [
    ("Could you share {item} with me?", "¿Podrías compartir {item} conmigo?"),
    ("I’d like to clarify {item} before we proceed.", "Me gustaría aclarar {item} antes de continuar."),
    ("Can we revisit {item} for a moment?", "¿Podemos revisar {item} un momento?"),
    ("I think we should focus on {item} today.", "Creo que deberíamos centrarnos en {item} hoy."),
    ("Could you walk me through {item}?", "¿Podrías explicarme {item}?"),
    ("I need your input on {item}.", "Necesito tu opinión sobre {item}."),
    ("Let’s align on {item} before the meeting ends.", "Alineemos {item} antes de que termine la reunión."),
    ("I want to make sure we agree on {item}.", "Quiero asegurarme de que estemos de acuerdo en {item}."),
    ("What’s your view on {item}?", "¿Cuál es tu opinión sobre {item}?"),
    ("We may need to adjust {item} this week.", "Puede que necesitemos ajustar {item} esta semana."),
]

# 3) Travel and public services
scenarios_travel = [
    ("At the airport", "en el aeropuerto"),
    ("At the hotel reception", "en la recepción del hotel"),
    ("At the taxi stand", "en la parada de taxis"),
    ("At the train platform", "en el andén del tren"),
    ("At the bus terminal", "en la terminal de autobuses"),
    ("At immigration", "en inmigración"),
    ("At the rental car desk", "en el mostrador de alquiler de coches"),
    ("At the check-in desk", "en el mostrador de check-in"),
    ("At the baggage claim", "en la recogida de equipaje"),
    ("At the tourist information desk", "en el puesto de información turística"),
    ("At the metro station", "en la estación de metro"),
    ("At the ferry terminal", "en la terminal de ferry"),
    ("At the embassy", "en la embajada"),
    ("At the hospital reception", "en la recepción del hospital"),
    ("At the pharmacy abroad", "en la farmacia del extranjero"),
    ("At the customer service desk", "en el mostrador de atención al cliente"),
    ("At the local police station", "en la comisaría local"),
    ("At a roadside assistance desk", "en un servicio de asistencia en carretera"),
    ("At the border crossing", "en el paso de frontera"),
    ("At the travel agency", "en la agencia de viajes"),
    ("At the currency exchange", "en el cambio de divisas"),
    ("At the bike rental", "en el alquiler de bicicletas"),
    ("At the station ticket office", "en la taquilla de la estación"),
    ("At the parking office", "en la oficina de aparcamiento"),
    ("At the airport lounge", "en la sala VIP del aeropuerto"),
]
items_travel = [
    "the gate", "my reservation", "the luggage", "the ticket", "the passport", "the address", "the receipt", "the room key", "the terminal", "the platform",
    "the transfer", "the taxi", "the luggage storage", "the refund", "the itinerary", "the visa", "the pickup", "the schedule", "the delay", "the connection",
    "the invoice", "the insurance", "the map", "the parking spot", "the shuttle", "the check-in", "the baggage", "the appointment", "the route", "the fare"
]
patterns_travel = [
    ("Could you tell me where {item} is?", "¿Podrías decirme dónde está {item}?"),
    ("I need help with {item}.", "Necesito ayuda con {item}."),
    ("Is {item} included in the price?", "¿Está {item} incluido en el precio?"),
    ("Can you confirm {item}?", "¿Puedes confirmar {item}?"),
    ("Where do I go for {item}?", "¿Adónde voy para {item}?"),
    ("How long does {item} take?", "¿Cuánto tarda {item}?"),
    ("I’m trying to find {item}.", "Estoy intentando encontrar {item}."),
    ("Do you know if {item} is available?", "¿Sabes si {item} está disponible?"),
    ("Could you explain {item} to me?", "¿Podrías explicarme {item}?"),
    ("I’m not sure about {item}.", "No estoy seguro/a de {item}."),
]

# 4) Social and community
scenarios_social = [
    ("At a neighborhood event", "en un evento del barrio"),
    ("At a birthday party", "en una fiesta de cumpleaños"),
    ("At a dinner with friends", "en una cena con amigos"),
    ("At a school reunion", "en una reunión escolar"),
    ("At a community meeting", "en una reunión comunitaria"),
    ("In a casual conversation", "en una conversación informal"),
    ("At a weekend barbecue", "en una barbacoa de fin de semana"),
    ("At a sports meetup", "en una reunión deportiva"),
    ("At a book club", "en un club de lectura"),
    ("At a volunteering event", "en un evento de voluntariado"),
    ("At a wedding reception", "en una recepción de boda"),
    ("At a coffee catch-up", "en una charla de café"),
    ("At a family gathering", "en una reunión familiar"),
    ("At a local festival", "en un festival local"),
    ("At a networking event", "en un evento de networking"),
    ("At a hobby meetup", "en una reunión de hobbies"),
    ("At a neighborhood barbecue", "en una barbacoa vecinal"),
    ("At a church gathering", "en una reunión religiosa"),
    ("At a school fundraiser", "en una recaudación escolar"),
    ("At a coworking meetup", "en una reunión de coworking"),
    ("At a language exchange", "en un intercambio de idiomas"),
    ("At a museum visit", "en una visita al museo"),
    ("At a park picnic", "en un picnic en el parque"),
    ("At a casual brunch", "en un brunch informal"),
    ("At a holiday gathering", "en una reunión de vacaciones"),
]
items_social = [
    "the plans", "the weekend", "the weather", "the food", "the music", "the trip", "the news", "the project", "the movie", "the book",
    "the game", "the hobby", "the town", "the neighborhood", "the family", "the team", "the event", "the schedule", "the idea", "the story",
    "the concert", "the restaurant", "the coffee", "the road trip", "the party", "the class", "the experience", "the podcast", "the culture", "the tradition"
]
patterns_social = [
    ("How do you feel about {item}?", "¿Qué opinas sobre {item}?"),
    ("Have you heard about {item}?", "¿Has oído hablar de {item}?"),
    ("I’ve been meaning to ask about {item}.", "Tenía ganas de preguntarte sobre {item}."),
    ("What do you think of {item}?", "¿Qué te parece {item}?"),
    ("That reminds me of {item}.", "Eso me recuerda a {item}."),
    ("I’d love to hear more about {item}.", "Me encantaría saber más sobre {item}."),
    ("Do you want to talk about {item}?", "¿Quieres hablar sobre {item}?"),
    ("I was just thinking about {item}.", "Estaba pensando justo en {item}."),
    ("It’s been a while since we talked about {item}.", "Hace tiempo que no hablamos de {item}."),
    ("That sounds like a great idea about {item}.", "Eso suena como una gran idea sobre {item}."),
]

# Helper to add cards to a category list.
def build_cards(scenarios, item_pool, patterns, prefix, tag_base):
    cards = []
    for idx, (scenario, _spanish_context) in enumerate(scenarios):
        for jdx, (pattern, span_pattern) in enumerate(patterns):
            item = item_pool[(idx + jdx) % len(item_pool)]
            english = pattern.format(item=item)
            spanish = span_pattern.format(item=item)
            cards.append({
                "deck": f"03_Languages::English::08_Real_Scenario_Expansion::{prefix}",
                "scenario": f"{prefix}: {scenario}",
                "text": english,
                "explanation": f"This is a practical phrase used in {scenario.lower()} to sound natural and useful in real conversations.",
                "usage": f"Useful for practicing realistic English in {scenario.lower()}.",
                "spanish": spanish,
                "tags": ["english", "real_scenario", tag_base],
            })
    return cards

# Build decks
Daily_cards = build_cards(scenarios_daily, items_daily, patterns_daily, "01_Daily_Life", "daily_life")
Work_cards = build_cards(scenarios_work, items_work, patterns_work, "02_Workplace", "workplace")
Travel_cards = build_cards(scenarios_travel, items_travel, patterns_travel, "03_Travel_and_Public_Services", "travel")
Social_cards = build_cards(scenarios_social, items_social, patterns_social, "04_Social_and_Community", "social")

# Ensure exactly 250 cards each
assert len(Daily_cards) == 250, len(Daily_cards)
assert len(Work_cards) == 250, len(Work_cards)
assert len(Travel_cards) == 250, len(Travel_cards)
assert len(Social_cards) == 250, len(Social_cards)

# Write the files
files = [
    (root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "01_Daily_Life" / "01_Daily_Life.json", Daily_cards),
    (root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "02_Workplace" / "02_Workplace.json", Work_cards),
    (root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "03_Travel_and_Public_Services" / "03_Travel_and_Public_Services.json", Travel_cards),
    (root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "04_Social_and_Community" / "04_Social_and_Community.json", Social_cards),
]

for path, cards in files:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)
        f.write("\n")

# Update the catalog
for path, cards in files:
    rel_path = path.relative_to(root).as_posix()
    if rel_path not in existing_paths:
        data["decks"].append({
            "deck": cards[0]["deck"],
            "path": rel_path,
            "cards_count": len(cards),
        })
        existing_paths.add(rel_path)

# Recompute totals
all_decks = data.get("decks", [])
data["total_cards"] = sum(int(entry.get("cards_count", 0)) for entry in all_decks)
data["total_decks"] = len(all_decks)

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Created 1000 realistic scenario cards across 4 decks and updated the index.")
