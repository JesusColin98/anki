# Guía de Calidad de Tarjetas, Patrones de Prompts y Plantillas de Anki

Esta guía documenta los criterios deterministas para detectar tarjetas de baja calidad ("thin/poor cards"), las estrategias y patrones de prompts para invocar a los agentes generadores, la taxonomía de casos de uso y las propuestas de nuevas plantillas avanzadas para maximizar el uso de Anki.

---

## 1. Detección y Diagnóstico de Tarjetas de Baja Calidad ("Thin / Low-Quality Cards")

Una tarjeta de baja calidad degrada la retención en memoria espacial (SRS) y viola las **20 Reglas de Formulación de Conocimiento de Wozniak**.

### 1.1 Señales de Tarjeta Deficiente:
1. **Falta de Contexto o Escenario Vacío**: Tarjetas que solo tienen traducción literal o definición plana sin campo `Scenario` claro.
2. **Cloze Deletions Ambiguas o Múltiples Excesivas**:
   - Clozes donde la respuesta se infiere sin entender el concepto.
   - Clozes sin el indicador `{{c1::...}}` bien balanceado.
3. **Falta de Explicación Intuitiva**: El campo `Explanation` es una copia exacta de la oración frontal sin desglosar el "Por qué" o la intuición subyacente.
4. **Ejemplos de Uso Inexistentes o Pobres**: El campo `Usage_Examples` está vacío o carece de formato estructurado (`<ul><li>...</li></ul>`).
5. **Diagramas o Código Malformados**:
   - Flechas de Mermaid con sintaxis inválida (e.g., `->|label|` en lugar de `-->|label|`).
   - Bloques de MathJax desbalanceados (e.g., `\[` sin `\]`).

### 1.2 Algoritmo de Diagnóstico y Auto-Reparación (`card_validator.py`):
```python
def validate_and_enrich(card: dict) -> tuple[bool, list[str]]:
    issues = []
    if len(card.get("explanation", "").strip()) < 20:
        issues.append("EXPLANATION_TOO_SHORT")
    if not card.get("scenario") or card.get("scenario") == "General":
        issues.append("MISSING_SCENARIO")
    if "{{c1::" not in card.get("text", "") and "cloze" in card.get("template", "").lower():
        issues.append("INVALID_CLOZE_TAGS")
    return (len(issues) == 0, issues)
```

---

## 2. Invocación de Agentes y Patrones de Prompts Específicos

Para expandir, reparar o generar tarjetas ricas desde cualquier fuente de texto o código, se deben usar los siguientes patrones de prompt basados en el marco de **5 Arquetipos**:

### 2.1 Prompt Pattern 1: Enriquecimiento e Imputación de Tarjetas "Thin"
**Objetivo**: Convertir notas planas en tarjetas Cloze & Scenario enriquecidas con contexto y traducción.

```text
ROL: [Analyst & Producer Mode] - Anki Pedagogical Engine
INPUT: Tarjeta plana o concepto sin contexto.
TAREA: Transforma la siguiente nota plana en una tarjeta atómica de alta calidad según la plantilla T1_Cloze / T4_Scenario.

REGLAS DE SALIDA (JSON Estricto):
{
  "deck": "<Pillars::Category::Subcategory::DeckName>",
  "scenario": "<Categoría Corta>: <Contexto o Situación con Emoji>",
  "text": "Oración principal con exactamente un {{c1::<Concepto Clave>}} enfocado.",
  "explanation": "Desglose conceptual intuitivo de 2 a 3 oraciones respondiendo por qué funciona.",
  "usage": "<ul><li><b>Punto clave 1</b>: ...</li><li><b>Punto clave 2</b>: ...</li></ul>",
  "spanish": "Traducción completa y natural al español.",
  "tags": ["tag1", "tag2"]
}
```

### 2.2 Prompt Pattern 2: Descomposición Map-Reduce para Libros / Documentación (`adk_orchestrator.py`)
**Objetivo**: Procesar documentos extensos o capítulos en ventanas deslizantes de 4,000 caracteres.

```text
ROL: [Scholar & Architect Mode] - ADK Document Processor
VENTANA DE ENTRADA: Chunks de 4,000 caracteres.
INSTRUCCIÓN:
1. Extrae únicamente hechos independientes de alto valor (1 hecho = 1 tarjeta).
2. Asigna cada hecho al pilar de la jerarquía de 6 niveles correspondiente:
   - 01_Cloud_and_Infrastructure
   - 02_AI_and_Data_Science
   - 03_Languages
   - 04_Social_and_Humanities
   - 05_Soft_Skills_and_Leadership
   - 06_Business_and_Productivity
3. Aplica el motor de plantillas T1 a T6 según la naturaleza del hecho.
```

---

## 3. Matriz de Mapeo de Casos de Uso y Plantillas Existentes

| Plantilla | Caso de Uso Principal | Ejemplo de Contenido |
| :--- | :--- | :--- |
| **T1_Cloze** | Vocabulario, terminología técnica, leyes y definiciones directas. | `The {{c1::Gradient Descent}} parameter update...` |
| **T2_DualCoding** | Algoritmos, flujos de trabajo y arquitecturas con diagramas Mermaid. | Diagrama de flujo de decisión en el reverso. |
| **T3_CodeSnippet** | Patrones de código, comandos CLI, funciones y regex. | Bloques de código formateados con explicación sintáctica. |
| **T4_Scenario** | Habilidades blandas, oratoria, negociación y soporte al cliente. | Frases de contención empática y resolución de conflictos. |
| **T5_MathJax** | Fórmulas matemáticas, estadísticas, físicas y modelos de costo. | \(\\theta_{t+1} = \\theta_t - \\eta \\nabla J(\\theta_t)\) |
| **T6_Quiz** | Preguntas de opción múltiple con justificación detallada. | Preguntas de certificación con análisis de distractores. |

---

## 4. Reflexión y Propuesta de Nuevas Plantillas Avanzadas

Para aprovechar Anki al máximo en entornos de ingeniería de software, arquitectura de nube e inteligencia artificial, se propone incorporar las siguientes **3 Nuevas Plantillas Avanzadas**:

### 4.1 Plantilla T7: `T7_SystemTopology` (Topología y Arquitecturas de Nube)
- **Caso de Uso**: Mapeo visual de servicios en la nube, flujos de datos distribuidos y comunicación RPC entre microservicios.
- **Estructura del Reverso**:
  - Renderizado automático de diagrama Graphviz DOT / Mermaid (`graph TB`).
  - Tabla comparativa de Latencia, Throughput y Puntos de Fallo (SPOF).
  - Comandos CLI de inspección (`gcloud`, `kubectl`, `stubby`).

### 4.2 Plantilla T8: `T8_DiagnosticRCA` (Matriz de Diagnóstico y Root Cause Analysis)
- **Caso de Uso**: Debugging de producción, resolución de códigos de error HTTP (e.g., 429, 502, 504), bucles de enrutamiento ULS y kernel panics.
- **Estructura Frontal**: Síntoma / Log de error de producción.
- **Estructura del Reverso**:
  - **Causa Raíz (RCA)**: Por qué ocurrió la falla.
  - **Comando de Verificación**: Script o consulta de logs para confirmar la hipótesis.
  - **Remediación**: Acción quirúrgica paso a paso.

### 4.3 Plantilla T9: `T9_ContrastivePhonetics` (Phonetics & Bi-Lingual Nuances)
- **Caso de Uso**: Aprendizaje avanzado de fonética, pares mínimos en inglés/idiomas (e.g., Connected Speech, Vowel Shift).
- **Estructura del Reverso**:
  - Transcripción Fonética IPA (`/ˈwɑːtər/`).
  - Comparativa de pronunciación vs. errores comunes de hablantes hispanos.
  - Enlace o tag para reproductor de audio sintético (`Audio` tag).

---

## 5. Instrucciones para los Agentes en el Workspace

1. **Jerarquía Evolutiva**: Los agentes deben verificar siempre que cada nueva tarjeta pertenezca a uno de los **6 Pilares** y mantenga exactamente **profundidad de 4 niveles**.
2. **Auto-Validación Obligatoria**: Antes de guardar cualquier tarjeta JSON en `decks/`, ejecutar `card_validator.validate_card(data)` para garantizar que no existan campos vacíos o sintaxis malformada.
3. **Indexación Automática**: Tras cualquier inserción, ejecutar `migrate_to_4level_hierarchy.py` o regenerar `decks/index.json`.
