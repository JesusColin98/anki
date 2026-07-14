import json
from pathlib import Path

root = Path(r"C:\Users\jesus\anki")
index_path = root / "decks" / "index.json"

with open(index_path, "r", encoding="utf-8") as f:
    data = json.load(f)

existing_paths = {item["path"] for item in data.get("decks", [])}


def build_deck(prefix, base_name, scenarios, item_pool, patterns, tag_name):
    cards = []
    for idx, scenario in enumerate(scenarios):
        for jdx, (pattern, spanish_pattern) in enumerate(patterns):
            item = item_pool[(idx + jdx) % len(item_pool)]
            english = pattern.format(item=item)
            spanish = spanish_pattern.format(item=item)
            cards.append({
                "deck": f"03_Languages::English::08_Real_Scenario_Expansion::{base_name}",
                "scenario": f"{base_name}: {scenario}",
                "text": english,
                "explanation": f"This is a practical phrase used in {scenario.lower()} to sound natural and useful in real conversations.",
                "usage": f"Useful for practicing realistic English in {scenario.lower()}.",
                "spanish": spanish,
                "tags": ["english", "real_scenario", tag_name],
            })
    return cards

# Category 1: Interviews and Careers
scenarios_careers = [
    "At a job interview", "In a networking event", "In a promotion discussion", "During a salary negotiation",
    "In a performance review", "At a career fair", "In a recruiter call", "At a portfolio review",
    "During onboarding", "In a team handoff", "At a leadership meeting", "In a mentoring session",
    "During a training interview", "At a remote interview", "In a follow-up email conversation",
    "In an internal transfer discussion", "At a consulting pitch", "During a role change discussion",
    "In a freelance client call", "At an employer meetup", "In a job referral conversation",
    "During a professional introduction", "In a career coaching session", "At a skills assessment",
    "In a career development conversation"
]
items_careers = [
    "experience", "strengths", "weaknesses", "career goals", "leadership", "problem-solving", "teamwork",
    "communication", "adaptability", "initiative", "results", "impact", "growth", "learning", "focus",
    "skills", "motivation", "confidence", "responsibility", "availability", "salary", "value", "portfolio",
    "projects", "collaboration", "mentorship", "mentoring", "scope", "timeline", "feedback"
]
patterns_careers = [
    ("I’d like to talk about my {{c1::{item}}}.", "Me gustaría hablar de mi {item}."),
    ("One of my biggest strengths is {{c1::{item}}}.", "Una de mis mayores fortalezas es {item}."),
    ("I’ve developed a lot of {{c1::{item}}} over the past few years.", "He desarrollado mucho {item} en los últimos años."),
    ("My main goal is to grow in {{c1::{item}}}.", "Mi objetivo principal es crecer en {item}."),
    ("I’m especially interested in {{c1::{item}}}.", "Me interesa especialmente {item}."),
    ("I believe my {{c1::{item}}} would be valuable here.", "Creo que mi {item} sería valioso aquí."),
    ("Could you tell me more about the {{c1::{item}}} role?", "¿Podrías contarme más sobre el puesto de {item}?"),
    ("I’d be happy to explain my {{c1::{item}}} approach.", "Me encantaría explicarte mi enfoque de {item}."),
    ("What would success look like in terms of {{c1::{item}}}?", "¿Qué se vería como éxito en términos de {item}?"),
    ("I’m looking for an opportunity to expand my {{c1::{item}}}.", "Estoy buscando una oportunidad para ampliar mi {item}."),
]

# Category 2: Phone Calls and Customer Service
scenarios_calls = [
    "Calling customer support", "Answering a phone call", "Booking an appointment", "Following up on an order",
    "Handling a complaint", "Returning a missed call", "Talking to a hotline", "Speaking to a billing team",
    "Calling a travel agency", "Calling a doctor’s office", "Speaking to a landlord", "Talking to a supplier",
    "Calling a school office", "Contacting a utility company", "Requesting a refund", "Checking an invoice",
    "Asking for a replacement", "Discussing a cancellation", "Confirming a delivery", "Calling about an account",
    "Reporting a problem", "Requesting a callback", "Speaking to a sales rep", "Calling a repair service",
    "Discussing a subscription update"
]
items_calls = [
    "the order", "the appointment", "the refund", "the account", "the invoice", "the policy", "the schedule",
    "the status", "the delivery", "the complaint", "the issue", "the balance", "the plan", "the contract",
    "the replacement", "the callback", "the reservation", "the billing", "the subscription", "the service",
    "the payment", "the cancellation", "the upgrade", "the ticket", "the timeline"
]
patterns_calls = [
    ("I’m calling about {{c1::{item}}}.", "Estoy llamando por {item}."),
    ("Could you help me with {{c1::{item}}}?", "¿Podrías ayudarme con {item}?"),
    ("I’d like to check the status of {{c1::{item}}}.", "Me gustaría comprobar el estado de {item}."),
    ("Can you confirm {{c1::{item}}} for me?", "¿Puedes confirmar {item} por mí?"),
    ("I need to speak to someone about {{c1::{item}}}.", "Necesito hablar con alguien sobre {item}."),
    ("Could you put me through to the team handling {{c1::{item}}}?", "¿Podrías pasarme al equipo que gestiona {item}?"),
    ("I’m afraid there’s a problem with {{c1::{item}}}.", "Me temo que hay un problema con {item}."),
    ("Would it be possible to arrange {{c1::{item}}}?", "¿Sería posible arreglar {item}?"),
    ("I’m trying to resolve {{c1::{item}}} as quickly as possible.", "Estoy intentando resolver {item} lo más rápido posible."),
    ("Can I get an update on {{c1::{item}}}?", "¿Puedo recibir una actualización sobre {item}?"),
]

# Category 3: Health and Emergencies
scenarios_health = [
    "At the doctor’s office", "At the emergency room", "At a pharmacy", "During a medical appointment",
    "Calling emergency services", "At a hospital reception", "Talking to a nurse", "At a health clinic",
    "Discussing symptoms", "At a dental appointment", "At a specialist consultation", "During a follow-up visit",
    "At a vaccination center", "At a wellness check", "In a health insurance call", "At a blood test center",
    "In a hospital discharge", "At a mental health appointment", "During a medication review", "At a rehabilitation center",
    "At an urgent care clinic", "In a medical translation situation", "At a pediatric visit", "During a health emergency",
    "At a telehealth consultation"
]
items_health = [
    "pain", "symptoms", "medication", "allergies", "vaccination", "treatment", "tests", "the diagnosis",
    "the prescription", "the appointment", "the side effects", "the dosage", "the insurance", "the clinic",
    "the emergency", "the injury", "the recovery", "the procedure", "the specialist", "the pharmacy",
    "the follow-up", "the referral", "the advice", "the scan", "the results"
]
patterns_health = [
    ("I’m having trouble with {{c1::{item}}}.", "Estoy teniendo problemas con {item}."),
    ("I’ve been feeling {{c1::{item}}} for the last few days.", "He estado sintiendo {item} durante los últimos días."),
    ("Could you explain the side effects of {{c1::{item}}}?", "¿Podrías explicar los efectos secundarios de {item}?"),
    ("I need to know more about {{c1::{item}}}.", "Necesito saber más sobre {item}."),
    ("Is {{c1::{item}}} serious?", "¿Es {item} serio?"),
    ("Please call someone if {{c1::{item}}} gets worse.", "Por favor, llama a alguien si {item} empeora."),
    ("I need a prescription for {{c1::{item}}}.", "Necesito una receta para {item}."),
    ("Can you tell me when I should take {{c1::{item}}}?", "¿Puedes decirme cuándo debo tomar {item}?"),
    ("I’m concerned about {{c1::{item}}}.", "Estoy preocupado/a por {item}."),
    ("Could you help me with {{c1::{item}}} right away?", "¿Podrías ayudarme con {item} enseguida?"),
]

# Category 4: Education and Academic Contexts
scenarios_education = [
    "In a classroom", "At a professor’s office", "During a group project", "In a study group",
    "At the library", "In an academic advising session", "During a lab session", "At a student services desk",
    "In a seminar", "At a tutoring session", "In a thesis meeting", "At a campus orientation",
    "During a discussion section", "At an exam review", "In a research meeting", "At a student council meeting",
    "During a presentation", "At a workshop", "In a writing center", "In a language class",
    "At a career center", "In a graduation planning meeting", "In a class discussion", "At a school administration office",
    "In a dissertation planning meeting"
]
items_education = [
    "the assignment", "the deadline", "the reading", "the lecture", "the topic", "the rubric", "the grade",
    "the lab", "the thesis", "the project", "the note", "the reference", "the research", "the essay",
    "the exam", "the review", "the seminar", "the workshop", "the schedule", "the syllabus", "the office hours",
    "the feedback", "the citation", "the source", "the discussion"
]
patterns_education = [
    ("I’m trying to understand {{c1::{item}}}.", "Estoy intentando entender {item}."),
    ("Could you explain {{c1::{item}}} one more time?", "¿Podrías explicar {item} otra vez?"),
    ("I’m not sure how to approach {{c1::{item}}}.", "No estoy seguro/a de cómo abordar {item}."),
    ("Would you mind helping me with {{c1::{item}}}?", "¿Te importaría ayudarme con {item}?"),
    ("I need a little more clarification on {{c1::{item}}}.", "Necesito un poco más de aclaración sobre {item}."),
    ("Can we discuss {{c1::{item}}} after class?", "¿Podemos discutir {item} después de clase?"),
    ("I’m worried about {{c1::{item}}} and the deadline.", "Estoy preocupado/a por {item} y la fecha límite."),
    ("Do we need to submit {{c1::{item}}} this week?", "¿Tenemos que entregar {item} esta semana?"),
    ("I think I missed something about {{c1::{item}}}.", "Creo que he perdido algo sobre {item}."),
    ("Could you point me to the resources for {{c1::{item}}}?", "¿Podrías indicarme los recursos para {item}?"),
]

# Build decks
careers_cards = build_deck("05", "05_Interviews_and_Careers", scenarios_careers, items_careers, patterns_careers, "careers")
calls_cards = build_deck("06", "06_Phone_Calls_and_Customer_Service", scenarios_calls, items_calls, patterns_calls, "phone_calls")
health_cards = build_deck("07", "07_Health_and_Emergencies", scenarios_health, items_health, patterns_health, "health")
educ_cards = build_deck("08", "08_Education_and_Academic_Contexts", scenarios_education, items_education, patterns_education, "education")

assert len(careers_cards) == len(scenarios_careers) * len(patterns_careers)
assert len(calls_cards) == len(scenarios_calls) * len(patterns_calls)
assert len(health_cards) == len(scenarios_health) * len(patterns_health)
assert len(educ_cards) == len(scenarios_education) * len(patterns_education)

files = [
    (root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "05_Interviews_and_Careers" / "05_Interviews_and_Careers.json", careers_cards),
    (root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "06_Phone_Calls_and_Customer_Service" / "06_Phone_Calls_and_Customer_Service.json", calls_cards),
    (root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "07_Health_and_Emergencies" / "07_Health_and_Emergencies.json", health_cards),
    (root / "decks" / "03_Languages" / "English" / "08_Real_Scenario_Expansion" / "08_Education_and_Academic_Contexts" / "08_Education_and_Academic_Contexts.json", educ_cards),
]

for path, cards in files:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(cards, f, indent=2, ensure_ascii=False)
        f.write("\n")

for path, cards in files:
    rel_path = path.relative_to(root).as_posix()
    if rel_path not in existing_paths:
        data["decks"].append({
            "deck": cards[0]["deck"],
            "path": rel_path,
            "cards_count": len(cards),
        })
        existing_paths.add(rel_path)

all_decks = data.get("decks", [])
data["total_cards"] = sum(int(entry.get("cards_count", 0)) for entry in all_decks)
data["total_decks"] = len(all_decks)

with open(index_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
    f.write("\n")

print("Created 1000 additional practical scenario cards and updated the index.")
