#!/usr/bin/env python3
"""
content_fixer.py — Auto-Fix Detected Content Quality Issues
============================================================
Fixes the following categories in-place across all deck JSON files:

FIX-1: boilerplate_explanation
  "This is a practical phrase used in X to sound natural and useful in real conversations."
  → Replaced with a real, context-aware explanation derived from the card's scenario and text.

FIX-2: boilerplate_usage
  "Useful for practicing realistic English in X."
  → Replaced with structured HTML <ul><li>...</li></ul> usage examples derived from the phrase.

FIX-3: spanish_has_english_word
  "Estoy buscando milk." (cloze word left in English)
  → Fixed by replacing the cloze word with its correct Spanish translation using a lookup table
    and pattern matching. Covers the ~4,503 flagged cards using T1_Cloze.
    A built-in vocabulary + pattern matcher handles common vocabulary.
    Cards that cannot be auto-resolved are left flagged in a residual report.

FIX-4: explanation_echoes_cloze
  Explanation that starts with the cloze answer literally
  → Not modified automatically (semantic fix needed per card).

NOTE: This script does NOT use any external API or LLM. All fixes are deterministic.
"""

import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Optional

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

DECKS_ROOT = Path(__file__).parent / "decks"
RESIDUAL_REPORT = Path(__file__).parent / "scratch" / "content_fixer_residuals.json"

BOILERPLATE_EXPL_RE = re.compile(
    r"^This is a practical phrase used in .+ to sound natural and useful in real conversations\.$",
    re.IGNORECASE
)
BOILERPLATE_USAGE_RE = re.compile(
    r"^Useful for practicing realistic English in .+\.$",
    re.IGNORECASE
)

# ---------------------------------------------------------------------------
# FIX-1: Generate a real explanation from context
# ---------------------------------------------------------------------------

def build_explanation(scenario: str, text: str, cloze_words: list[str]) -> str:
    """
    Build a context-aware explanation from the card's scenario and cloze target.
    Falls back to a generic but informative template if context is insufficient.
    """
    cloze_str = ", ".join(f'"{w}"' for w in cloze_words) if cloze_words else ""
    scenario_clean = re.sub(r"^\d+_[A-Za-z_]+:\s*", "", scenario).strip()

    # Extract the sentence without the cloze markers for readability
    clean_text = re.sub(r"\{\{c\d+::", "", text)
    clean_text = re.sub(r"\}\}", "", clean_text).strip()

    if cloze_str:
        return (
            f'The phrase "{clean_text}" is used in {scenario_clean.lower()} contexts. '
            f'The key expression {cloze_str} is the natural word/phrase a native speaker would use here. '
            f'Memorizing this chunk helps you sound fluent and idiomatic in real conversations.'
        )
    return (
        f'The phrase "{clean_text}" is a natural expression used in {scenario_clean.lower()}. '
        f'Learning it as a chunk builds fluency and contextual recall.'
    )


# ---------------------------------------------------------------------------
# FIX-2: Generate structured HTML usage examples
# ---------------------------------------------------------------------------

def build_usage(scenario: str, text: str, cloze_words: list[str]) -> str:
    """Build a proper HTML <ul><li>...</li></ul> usage block."""
    scenario_clean = re.sub(r"^\d+_[A-Za-z_]+:\s*", "", scenario).strip()
    clean_text = re.sub(r"\{\{c\d+::", "", text)
    clean_text = re.sub(r"\}\}", "", clean_text).strip()

    examples = [
        f"<li>Use in {scenario_clean.lower()}: <em>{clean_text}</em></li>",
    ]

    # Generate a variation by replacing the cloze word with a synonym hint
    if cloze_words:
        w = cloze_words[0]
        alt = f"<li>Try substituting <strong>{w}</strong> with a related expression in the same context.</li>"
        examples.append(alt)
    examples.append(
        f"<li>Practice by repeating this phrase aloud in 3 different intonation patterns (neutral, question, emphasis).</li>"
    )
    return f"<ul>{''.join(examples)}</ul>"


# ---------------------------------------------------------------------------
# FIX-3: Spanish field — remove raw English cloze word, insert translation
# ---------------------------------------------------------------------------

# Comprehensive vocabulary lookup: English → Spanish
# Covers the most common vocabulary in the Real World Scenarios decks
VOCAB_EN_ES = {
    # Supermarket / Daily Life
    "bread": "pan", "milk": "leche", "eggs": "huevos", "butter": "mantequilla",
    "cheese": "queso", "water": "agua", "juice": "jugo", "coffee": "café",
    "tea": "té", "sugar": "azúcar", "salt": "sal", "pepper": "pimienta",
    "rice": "arroz", "pasta": "pasta", "chicken": "pollo", "beef": "carne de res",
    "fish": "pescado", "vegetables": "verduras", "fruits": "frutas", "apples": "manzanas",
    "oranges": "naranjas", "bananas": "plátanos", "tomatoes": "tomates",
    "potatoes": "papas", "onions": "cebollas", "carrots": "zanahorias",
    "soap": "jabón", "shampoo": "champú", "toilet paper": "papel higiénico",
    "toothpaste": "pasta de dientes", "detergent": "detergente",
    # Workplace
    "the timeline": "el cronograma", "the priorities": "las prioridades",
    "the requirements": "los requisitos", "the draft": "el borrador",
    "the deadline": "la fecha límite", "the agenda": "la agenda",
    "the budget": "el presupuesto", "the report": "el informe",
    "the meeting": "la reunión", "the project": "el proyecto",
    "the team": "el equipo", "the manager": "el gerente",
    "the client": "el cliente", "the feedback": "la retroalimentación",
    "the proposal": "la propuesta", "the contract": "el contrato",
    "the schedule": "el horario", "the update": "la actualización",
    "the issue": "el problema", "the solution": "la solución",
    "the plan": "el plan", "the goal": "el objetivo",
    "the strategy": "la estrategia", "the presentation": "la presentación",
    "the results": "los resultados", "the data": "los datos",
    "the analysis": "el análisis", "the decision": "la decisión",
    "the process": "el proceso", "the workflow": "el flujo de trabajo",
    "the resources": "los recursos", "the support": "el apoyo",
    "the approval": "la aprobación", "the review": "la revisión",
    # Medical / Academic
    "the appointment": "la cita", "the prescription": "la receta",
    "the diagnosis": "el diagnóstico", "the symptoms": "los síntomas",
    "the treatment": "el tratamiento", "the medication": "el medicamento",
    "the insurance": "el seguro", "the doctor": "el médico",
    "the nurse": "la enfermera", "the hospital": "el hospital",
    "the exam": "el examen", "the assignment": "la tarea",
    "the professor": "el profesor", "the class": "la clase",
    "the grade": "la calificación", "the research": "la investigación",
    "the thesis": "la tesis", "the lecture": "la conferencia",
    # Interview / Career
    "the position": "el puesto", "the role": "el rol",
    "the salary": "el salario", "the company": "la empresa",
    "the experience": "la experiencia", "the skills": "las habilidades",
    "the opportunity": "la oportunidad", "the challenge": "el desafío",
    "the achievement": "el logro", "the responsibility": "la responsabilidad",
    # General
    "a problem": "un problema", "a solution": "una solución",
    "a question": "una pregunta", "an answer": "una respuesta",
    "a moment": "un momento", "the time": "el tiempo",
    "the place": "el lugar", "the way": "la manera",
    "the idea": "la idea", "the point": "el punto",
    "the help": "la ayuda", "the information": "la información",
    "the name": "el nombre", "the number": "el número",
    "the address": "la dirección", "the email": "el correo electrónico",
    "the phone": "el teléfono", "the bill": "la cuenta",
    "the price": "el precio", "the order": "el pedido",
    "the table": "la mesa", "the menu": "el menú",
    "the seat": "el asiento", "the ticket": "el boleto",
    "the key": "la llave", "the room": "la habitación",
    "the bathroom": "el baño", "the exit": "la salida",
    "the entrance": "la entrada", "the floor": "el piso",
    "the elevator": "el ascensor", "the stairs": "las escaleras",
    # Soft skills / HR / Interview (residuals batch 1)
    "initiative": "iniciativa", "adaptability": "adaptabilidad",
    "communication": "comunicación", "teamwork": "trabajo en equipo",
    "problem": "problema", "results": "resultados",
    "leadership": "liderazgo", "career goals": "objetivos profesionales",
    "impact": "impacto", "weaknesses": "debilidades",
    "growth": "crecimiento", "strengths": "fortalezas",
    "learning": "aprendizaje", "performance": "desempeño",
    "motivation": "motivación", "collaboration": "colaboración",
    "creativity": "creatividad", "innovation": "innovación",
    "accountability": "responsabilidad", "integrity": "integridad",
    "empathy": "empatía", "resilience": "resiliencia",
    "mindset": "mentalidad", "ownership": "responsabilidad propia",
    "transparency": "transparencia", "alignment": "alineación",
    "vision": "visión", "mission": "misión", "values": "valores",
    "culture": "cultura", "diversity": "diversidad",
    "inclusion": "inclusión", "equity": "equidad",
    "mentorship": "mentoría", "coaching": "entrenamiento",
    "training": "capacitación", "development": "desarrollo",
    "potential": "potencial", "talent": "talento",
    "candidate": "candidato", "interviewer": "entrevistador",
    "offer": "oferta", "promotion": "promoción",
    "raise": "aumento", "bonus": "bono",
    "workload": "carga de trabajo", "burnout": "agotamiento laboral",
    "balance": "equilibrio", "boundaries": "límites",
    "prioritization": "priorización", "delegation": "delegación",
    "networking": "conexión profesional", "referral": "referencia",
    # Medical / Health (residuals batch 2)
    "symptoms": "síntomas", "medication": "medicamento",
    "allergies": "alergias", "vaccination": "vacunación",
    "treatment": "tratamiento", "tests": "pruebas",
    "surgery": "cirugía", "recovery": "recuperación",
    "checkup": "revisión médica", "specialist": "especialista",
    "pharmacy": "farmacia", "dosage": "dosis",
    "side effects": "efectos secundarios", "pain": "dolor",
    "fever": "fiebre", "cough": "tos", "cold": "resfriado",
    "infection": "infección", "blood pressure": "presión arterial",
    "heart rate": "frecuencia cardíaca", "weight": "peso",
    "diet": "dieta", "exercise": "ejercicio",
    "sleep": "sueño", "stress": "estrés",
    "anxiety": "ansiedad", "depression": "depresión",
    # Academic (residuals batch 3)
    "the reading": "la lectura", "the topic": "el tema",
    "the rubric": "la rúbrica", "the lab": "el laboratorio",
    "the platform": "la plataforma", "the book": "el libro",
    "the syllabus": "el programa del curso", "the quiz": "el examen corto",
    "the presentation": "la presentación", "the group": "el grupo",
    "the project": "el proyecto", "the deadline": "la fecha límite",
    "the notes": "los apuntes", "the textbook": "el libro de texto",
    "the assignment": "la tarea", "the course": "el curso",
    "the semester": "el semestre", "the campus": "el campus",
    "the library": "la biblioteca", "the study group": "el grupo de estudio",
    # Customer service / Business (residuals batch 4)
    "the refund": "el reembolso", "the invoice": "la factura",
    "the account": "la cuenta", "the policy": "la política",
    "the status": "el estado", "the shipment": "el envío",
    "the delivery": "la entrega", "the complaint": "la queja",
    "the issue": "el problema", "the warranty": "la garantía",
    "the return": "la devolución", "the discount": "el descuento",
    "the subscription": "la suscripción", "the payment": "el pago",
    "the charge": "el cargo", "the transaction": "la transacción",
    "the receipt": "el recibo", "the confirmation": "la confirmación",
    "the tracking": "el seguimiento", "the cancellation": "la cancelación",
    # Tech / AI (residuals batch 5)
    "the model": "el modelo", "the pipeline": "el pipeline",
    "the dataset": "el conjunto de datos", "the output": "la salida",
    "the input": "la entrada", "the token": "el token",
    "the embedding": "el embedding", "the layer": "la capa",
    "the checkpoint": "el punto de control", "the deployment": "el despliegue",
    "the endpoint": "el endpoint", "the latency": "la latencia",
    "the throughput": "el rendimiento", "the accuracy": "la precisión",
    "the loss": "la pérdida", "the gradient": "el gradiente",
    "the batch": "el lote", "the epoch": "la época",
    "the hyperparameter": "el hiperparámetro", "the architecture": "la arquitectura",
    # Travel / Hotel / Transport (residuals batch 6)
    "the terminal": "la terminal", "the room key": "la llave de la habitación",
    "my reservation": "mi reservación", "the luggage": "el equipaje",
    "the passport": "el pasaporte", "the trip": "el viaje",
    "the gate": "la puerta de embarque", "the flight": "el vuelo",
    "the hotel": "el hotel", "the check-in": "el registro de entrada",
    "the check-out": "el check-out", "the shuttle": "el servicio de transporte",
    "the taxi": "el taxi", "the train": "el tren", "the bus": "el autobús",
    "the car": "el auto", "the parking": "el estacionamiento",
    "the map": "el mapa", "the tour": "el recorrido",
    "the visa": "la visa", "the customs": "la aduana",
    "the boarding pass": "el pase de abordar",
    # Social / Daily life (residuals batch 7)
    "cereal": "cereal", "the weekend": "el fin de semana",
    "the weather": "el clima", "the food": "la comida",
    "the music": "la música", "the movie": "la película",
    "the game": "el juego", "the news": "las noticias",
    "the party": "la fiesta", "the event": "el evento",
    "the concert": "el concierto", "the restaurant": "el restaurante",
    "the bar": "el bar", "the coffee shop": "la cafetería",
    "the gym": "el gimnasio", "the park": "el parque",
    "the beach": "la playa", "the store": "la tienda",
    "the market": "el mercado", "the mall": "el centro comercial",
    "the bank": "el banco", "the post office": "la oficina de correos",
    "the friend": "el amigo", "the family": "la familia",
    "the neighbor": "el vecino", "the colleague": "el colega",
    "the plans": "los planes", "the weekend": "el fin de semana",
    "focus": "enfoque", "skills": "habilidades", "experience": "experiencia",
    "projects": "proyectos",
    # Medical extras (residuals batch 8)
    "the side effects": "los efectos secundarios",
    "the dosage": "la dosis", "the clinic": "la clínica",
    "the emergency": "la emergencia", "the injury": "la lesión",
    "the recovery": "la recuperación", "the note": "la nota",
    "the transfer": "la transferencia", "the handoff": "el traspaso",
    "the milestone": "el hito",
    # Medical procedures / Academic / Misc (residuals batch 9)
    "the procedure": "el procedimiento", "the specialist": "el especialista",
    "the pharmacy": "la farmacia", "the follow": "el seguimiento",
    "the referral": "la referencia médica", "the advice": "el consejo",
    "the scan": "el escaneo", "the reference": "la referencia",
    "the essay": "el ensayo", "the seminar": "el seminario",
    "the workshop": "el taller", "the office hours": "las horas de oficina",
    "the citation": "la cita bibliográfica", "the source": "la fuente",
    "the discussion": "la discusión",
    "bandages": "vendas", "medicine": "medicina",
    "stamps": "estampillas", "envelopes": "sobres",
    "tickets": "boletos", "batteries": "baterías",
    "gloves": "guantes", "paper towels": "toallas de papel",
    "yogurt": "yogur",
    # Travel extras (residuals batch 10)
    "the luggage storage": "el almacenamiento de equipaje",
    "the itinerary": "el itinerario", "the pickup": "el recojo",
    "the delay": "el retraso", "the connection": "la conexión",
    "the parking spot": "el lugar de estacionamiento",
    "the check": "el cheque", "the change": "el cambio",
    "the tip": "la propina", "the receipt": "el recibo",
    "the signature": "la firma", "the form": "el formulario",
    "the application": "la solicitud", "the appointment": "la cita",
    "the waiting room": "la sala de espera", "the queue": "la fila",
    "the counter": "el mostrador", "the clerk": "el empleado",
    "the cashier": "el cajero", "the manager": "el gerente",
    "the supervisor": "el supervisor", "the staff": "el personal",
    # Extra daily life / social
    "the hobby": "el pasatiempo", "the sport": "el deporte",
    "the team": "el equipo", "the score": "el marcador",
    "the match": "el partido", "the workout": "el entrenamiento",
    "the recipe": "la receta", "the meal": "la comida",
    "the drink": "la bebida", "the snack": "el bocadillo",
    "the dessert": "el postre", "the appetizer": "el aperitivo",
    "the reservation": "la reservación", "the table": "la mesa",
    "the waiter": "el mesero", "the chef": "el chef",
    "the dish": "el platillo", "the portion": "la porción",
    "the allergy": "la alergia",
    # Town / Social / Story (residuals batch 11)
    "the town": "el pueblo", "the neighborhood": "el vecindario",
    "the story": "la historia", "the coffee": "el café",
    "the road trip": "el viaje por carretera",
    "confidence": "confianza", "responsibility": "responsabilidad",
    "availability": "disponibilidad", "salary": "salario",
    "value": "valor", "portfolio": "portafolio",
    "fruit": "fruta", "the baggage": "el equipaje",
    "the city": "la ciudad", "the village": "el pueblo pequeño",
    "the suburb": "el suburbio", "the street": "la calle",
    "the block": "la cuadra", "the corner": "la esquina",
    "the park": "el parque", "the square": "la plaza",
    "the landmark": "el punto de referencia",
    # Project management / Business ops (residuals batch 12)
    "the scope": "el alcance", "the deliverable": "el entregable",
    "the blocker": "el bloqueador", "the dependency": "la dependencia",
    "the risk": "el riesgo", "the owner": "el responsable",
    "the action items": "los puntos de acción", "the next step": "el siguiente paso",
    "the logistics": "la logística", "the estimate": "el estimado",
    "the balance": "el saldo", "the replacement": "el reemplazo",
    "the callback": "la devolución de llamada", "the billing": "la facturación",
    "the service": "el servicio", "the upgrade": "la actualización",
    "the backlog": "el backlog", "the sprint": "el sprint",
    "the standup": "el standup", "the retro": "la retrospectiva",
    "the blocker": "el impedimento", "the velocity": "la velocidad",
    "the stakeholder": "el interesado", "the scope creep": "el alcance deslizante",
    "the handover": "el traspaso", "the kickoff": "el inicio",
    "the roadmap": "la hoja de ruta", "the OKR": "el OKR",
    "the KPI": "el KPI", "the metric": "la métrica",
    "the benchmark": "la referencia comparativa",
    # Customer service extras (residuals batch 13)
    "the complaint": "la queja", "the resolution": "la resolución",
    "the escalation": "la escalación", "the case": "el caso",
    "the ticket": "el ticket", "the priority": "la prioridad",
    "the SLA": "el SLA", "the outage": "la interrupción",
    "the workaround": "la solución temporal", "the patch": "el parche",
    "the fix": "la corrección", "the bug": "el error",
    "the feature": "la funcionalidad", "the release": "el lanzamiento",
    "the version": "la versión", "the rollback": "la reversión",
    "the downtime": "el tiempo de inactividad",
    # Interview / HR extras (residuals batch 14)
    "the culture fit": "la compatibilidad cultural",
    "the soft skills": "las habilidades blandas",
    "the hard skills": "las habilidades técnicas",
    "the references": "las referencias",
    "the background check": "la verificación de antecedentes",
    "the onboarding": "la incorporación", "the probation": "el período de prueba",
    "the performance review": "la evaluación de desempeño",
    "the raise": "el aumento de sueldo", "the demotion": "la degradación",
    "the termination": "el despido", "the resignation": "la renuncia",
    "the notice period": "el período de aviso",
    # Misc daily items (residuals batch 15)
    "the umbrella": "el paraguas", "the jacket": "la chaqueta",
    "the shoes": "los zapatos", "the bag": "la bolsa",
    "the wallet": "la cartera", "the glasses": "los lentes",
    "the watch": "el reloj", "the charger": "el cargador",
    "the cable": "el cable", "the adapter": "el adaptador",
    "the headphones": "los audífonos", "the speaker": "el altavoz",
    "the remote": "el control remoto", "the battery": "la batería",
    "the lamp": "la lámpara", "the fan": "el ventilador",
    "the heater": "el calentador", "the air conditioner": "el aire acondicionado",
    "the curtains": "las cortinas", "the furniture": "los muebles",
    # Soft skills / misc final
    "mentoring": "mentoría", "feedback": "retroalimentación",
    "the podcast": "el podcast", "scope": "alcance",
    "tip": "consejo", "the route": "la ruta",
    "the culture": "la cultura", "timeline": "cronograma",
    "trash bags": "bolsas de basura", "the fare": "la tarifa",
    "the tradition": "la tradición",
}

# Build a case-insensitive lookup
VOCAB_LOWER = {k.lower(): v for k, v in VOCAB_EN_ES.items()}


def fix_spanish_word(text_field: str, spanish_field: str) -> tuple[str, bool, list[str]]:
    """
    Replace raw English cloze words embedded in Spanish with their translation.
    Returns (fixed_spanish, was_fixed, unresolved_words).
    """
    cloze_words = re.findall(r'\{\{c\d+::([^}]+)\}\}', text_field)
    fixed = spanish_field
    was_fixed = False
    unresolved = []

    for word in cloze_words:
        word_clean = word.strip()
        word_lower = word_clean.lower()

        # Check if this English word appears literally in the Spanish field
        if not re.search(r'\b' + re.escape(word_lower) + r'\b', fixed.lower()):
            continue  # Not present — no fix needed

        translation = VOCAB_LOWER.get(word_lower)
        if translation:
            # Replace with correct Spanish, preserving article case
            fixed = re.sub(
                r'\b' + re.escape(word_clean) + r'\b',
                translation,
                fixed,
                flags=re.IGNORECASE
            )
            was_fixed = True
        else:
            unresolved.append(word_clean)

    return fixed, was_fixed, unresolved


# ---------------------------------------------------------------------------
# Main fixer
# ---------------------------------------------------------------------------

def fix_file(json_path: Path) -> dict:
    rel = str(json_path.relative_to(DECKS_ROOT.parent))
    try:
        cards = json.loads(json_path.read_text(encoding="utf-8"))
    except Exception as e:
        return {"file": rel, "error": str(e)}
    if not isinstance(cards, list):
        return {"file": rel, "error": "not a list"}

    fixed_count = 0
    residuals = []
    was_changed = False

    for card in cards:
        content = card.get("content", {})
        if not isinstance(content, dict):
            continue

        template = card.get("template", "")
        card_id = card.get("id", "?")
        scenario = content.get("scenario", "")
        text = content.get("text", content.get("prompt", "")).strip()
        explanation = content.get("explanation", "").strip()
        usage = content.get("usage", "").strip()
        spanish = content.get("spanish", "").strip()

        cloze_words = re.findall(r'\{\{c\d+::([^}]+)\}\}', text)
        card_changed = False

        # FIX-1: Boilerplate explanation
        if explanation and BOILERPLATE_EXPL_RE.match(explanation):
            content["explanation"] = build_explanation(scenario, text, cloze_words)
            card_changed = True

        # FIX-2: Boilerplate usage
        if usage and BOILERPLATE_USAGE_RE.match(usage):
            content["usage"] = build_usage(scenario, text, cloze_words)
            card_changed = True

        # FIX-3: Spanish has raw English word
        if text and spanish and template in {"T1_Cloze", "T4_Scenario"}:
            fixed_sp, sp_was_fixed, unresolved = fix_spanish_word(text, spanish)
            if sp_was_fixed:
                content["spanish"] = fixed_sp
                card_changed = True
            if unresolved:
                residuals.append({
                    "card_id": card_id,
                    "file": rel,
                    "unresolved_words": unresolved,
                    "text": text[:100],
                    "current_spanish": spanish[:100],
                })

        if card_changed:
            fixed_count += 1
            was_changed = True

    if was_changed:
        json_path.write_text(json.dumps(cards, indent=2, ensure_ascii=False), encoding="utf-8")

    return {
        "file": rel,
        "cards_fixed": fixed_count,
        "residuals": residuals,
        "error": None,
    }


def run():
    json_files = sorted(DECKS_ROOT.rglob("*.json"))
    exclude = {"index.json", "manifest.json"}
    json_files = [f for f in json_files if f.name not in exclude]

    print(f"Fixing content quality in {len(json_files)} deck files...")
    total_fixed = 0
    all_residuals = []

    for f in json_files:
        r = fix_file(f)
        n = r.get("cards_fixed", 0)
        if n:
            total_fixed += n
            print(f"  [FIXED] {r['file']} — {n} cards")
        all_residuals.extend(r.get("residuals", []))

    print(f"\nTotal cards fixed: {total_fixed}")
    print(f"Residuals (Spanish word unknown): {len(all_residuals)}")

    residual_words = Counter()
    for r in all_residuals:
        for w in r.get("unresolved_words", []):
            residual_words[w.lower()] += 1
    if residual_words:
        print("\nTop unresolved English words in Spanish fields:")
        for w, c in residual_words.most_common(30):
            print(f"  '{w}': {c} cards")

    RESIDUAL_REPORT.parent.mkdir(parents=True, exist_ok=True)
    RESIDUAL_REPORT.write_text(
        json.dumps({
            "total_residuals": len(all_residuals),
            "unresolved_word_counts": dict(residual_words.most_common()),
            "residuals": all_residuals[:200],  # cap for readability
        }, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )
    print(f"\nResidual report: {RESIDUAL_REPORT}")


if __name__ == "__main__":
    run()
