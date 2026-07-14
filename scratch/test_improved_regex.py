import re

lines = [
    '- **The Testing Effect:** Research shows that students...',
    '- **The Paradox of Studying:** Students often...',
    '- **The Self-Portrait Barrier** — How our internal labels...',
    '**¿Por qué es inútil la crítica según Carnegie?**- **Porque pone a la persona...**',
    '**¿Cuál es la única forma de ganar una discusión?**- **Evitándola.**',
    '**Testing Effect** — The empirical finding that...'
]

pattern = r'^(?:-\s+|\*\s+|\d+\.\s+)?\*\*(.*?)\*\*[:\s—–-]*\s*(.*)$'

for line in lines:
    match = re.match(pattern, line)
    if match:
        term = match.group(1).strip()
        # strip trailing colon from term if it was inside the bold tags
        if term.endswith(":"):
            term = term[:-1].strip()
        definition = match.group(2).strip()
        print(f"Matched: {line}")
        print(f"  Term/Q: {term}")
        print(f"  Def/A:  {definition}")
    else:
        print(f"Failed to match: {line}")
