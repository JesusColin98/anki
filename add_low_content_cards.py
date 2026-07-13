import json
import os
import subprocess

base_dir = os.path.dirname(os.path.abspath(__file__))

# Define the new cards to add to each file
additions = {
    "decks/01_Cloud_and_Infrastructure/Cybersecurity/Defense_Evasion/03_Defense_Evasion.json": [
        {
            "deck": "01_Cloud_and_Infrastructure::Cybersecurity::Defense_Evasion::03_Defense_Evasion",
            "scenario": "Security: Evasion (Process Hollowing) 🛡️",
            "text": "To execute covert code in a benign context, malware launches a system process in a suspended state, unmaps its memory, and writes a replacement payload; this is known as {{c1::Process Hollowing}}.",
            "explanation": "Process hollowing evasion unmaps the original executable from a legitimate suspended process's memory space (e.g. svchost.exe) using NtUnmapViewOfSection, and injects a malicious payload into the hollowed section, updating the Thread Entry Point.",
            "usage": "**Symptom**: Unusually high CPU or network activity from a standard system process like svchost.exe.<br>**Root Cause**: Malicious payload executing inside a hollowed-out legitimate process container.<br>**Validation**: Run Sysinternals Process Hacker / Process Explorer and inspect the memory sections or parent-child hierarchy.<br>**Remediation**: Use EDR memory scanning for hollowed processes (detecting mismatch between file-on-disk and memory section headers).",
            "spanish": "Para ejecutar código encubierto en un contexto benigno, el malware inicia un proceso del sistema en estado suspendido, desasigna su memoria y escribe una carga útil de reemplazo; esto se conoce como vaciado de procesos (Process Hollowing).",
            "tags": ["security", "defense_evasion", "rca", "malware"]
        },
        {
            "deck": "01_Cloud_and_Infrastructure::Cybersecurity::Defense_Evasion::03_Defense_Evasion",
            "scenario": "Security: Evasion (Parent PID Spoofing) 🛡️",
            "text": "To evade parent-child process detection rules, malware spoofs its parent process by using the {{c1::UpdateProcThreadAttribute}} API to specify a different Parent PID.",
            "explanation": "EDR and security agents monitor parent-child process relationships (e.g., cmd.exe spawned by word.exe is suspicious). Parent PID Spoofing leverages Windows thread execution attributes to assign a benign parent (like explorer.exe) to a newly created malicious process.",
            "usage": "Example PowerShell/CLI attack pattern:<ul><li>Malware calls <code>InitializeProcThreadAttributeList</code></li><li>Updates attribute with <code>PROC_THREAD_ATTRIBUTE_PARENT_PROCESS</code></li><li>Creates process pointing to benign PPID</li></ul>",
            "spanish": "Para evadir las reglas de detección de procesos padre-hijo, el malware suplanta su proceso padre utilizando la API UpdateProcThreadAttribute para especificar un PID padre diferente.",
            "tags": ["security", "defense_evasion", "code_snippet", "api"]
        }
    ],
    "decks/01_Cloud_and_Infrastructure/Cybersecurity/Reconnaissance/02_Reconnaissance.json": [
        {
            "deck": "01_Cloud_and_Infrastructure::Cybersecurity::Reconnaissance::02_Reconnaissance",
            "scenario": "Security: OS Fingerprinting 🔍",
            "text": "To identify the operating system and running services of a target host, you perform an OS detection scan using Nmap with the {{c1::`-O` flag}}.",
            "explanation": "OS detection (fingerprinting) works by sending a series of TCP and UDP packets to the target host and analyzing the responses (TCP window size, IP ID, TTL, TCP options), comparing them to a database of known signatures.",
            "usage": "Nmap CLI Command: <code>nmap -O -sV <target_ip></code><br>Explanation: <code>-O</code> enables OS detection, and <code>-sV</code> detects service version information.",
            "spanish": "Para identificar el sistema operativo y los servicios en ejecución de un host objetivo, realizas un escaneo de detección de SO usando Nmap con la opción -O.",
            "tags": ["security", "reconnaissance", "nmap", "cli"]
        },
        {
            "deck": "01_Cloud_and_Infrastructure::Cybersecurity::Reconnaissance::02_Reconnaissance",
            "scenario": "Security: Stealth Scan 🔍",
            "text": "To scan a target stealthily without sending packets from your own IP, you can use a zombie host to perform an {{c1::Idle Scan (-sI)}} by monitoring IP ID changes.",
            "explanation": "An Idle Scan exploits a zombie host that has predictable IP ID increment behavior. By querying the zombie's IP ID, sending a spoofed SYN to the target, and querying the zombie again, the attacker infers if the target port is open based on whether the zombie's IP ID incremented by 1 or 2.",
            "usage": "**Symptom**: Scanner IP is invisible in the target's firewall logs; instead, only zombie IP is logged.<br>**Root Cause**: Use of an idle scan exploiting a zombie host's predictable IP ID increment.<br>**Command**: <code>nmap -PN -sI <zombie_ip> <target_ip></code><br>**Remediation**: Configure firewalls to drop incoming packets with spoofed source IPs (unicast Reverse Path Verification - uRPF) and patch OS to use randomized IP IDs.",
            "spanish": "Para escanear un objetivo sigilosamente sin enviar paquetes desde tu propia IP, puedes usar un host zombi para realizar un escaneo inactivo (Idle Scan) mediante el monitoreo de cambios en el IP ID.",
            "tags": ["security", "reconnaissance", "nmap", "rca"]
        }
    ],
    "decks/01_Cloud_and_Infrastructure/Networking/Fundamentals/01_Fundamentals.json": [
        {
            "deck": "01_Cloud_and_Infrastructure::Networking::Fundamentals::01_Fundamentals",
            "scenario": "Networking: Subnet Architecture 🌐",
            "text": "To isolate public-facing resources from private databases, engineers implement a public/private subnet topology where only the public subnet route table directs traffic to the {{c1::Internet Gateway (IGW)}}.",
            "explanation": "A public subnet has a route direct to the Internet Gateway, allowing external incoming connections. A private subnet does not route to the IGW and requires a NAT Gateway in the public subnet to make outbound internet connections.",
            "usage": "VPC Subnet Architecture:\n<div class=\"mermaid\">\ngraph TD\n  User(\"User / Internet\") -->|ports 80/443| IGW[\"Internet Gateway (IGW)\"]\n  IGW --> PublicSubnet[\"Public Subnet (Web Server)\"]\n  PublicSubnet -->|private IP| NAT[\"NAT Gateway\"]\n  PublicSubnet --> PrivateSubnet[\"Private Subnet (Database)\"]\n  PrivateSubnet -->|outbound requests| NAT\n  NAT --> IGW\nend\n</div>",
            "spanish": "Para aislar los recursos públicos de las bases de datos privadas, los ingenieros implementan una topología de subred pública/privada donde solo la tabla de enrutamiento de la subred pública dirige el tráfico a la puerta de enlace de Internet (IGW).",
            "tags": ["networking", "cloud_architecture", "subnet", "topology"]
        },
        {
            "deck": "01_Cloud_and_Infrastructure::Networking::Fundamentals::01_Fundamentals",
            "scenario": "Networking: DNS Resolution Quiz 🌐",
            "text": "During DNS resolution, which server is queried first by the local recursive resolver if the record is not cached? {{c1::Root Nameserver (e.g. A.root-servers.net)}}.",
            "explanation": "If the local recursive resolver does not have the IP in its cache, it queries the Root Nameserver. The Root Nameserver points the resolver to the TLD Nameserver (e.g., .com TLD), which in turn points to the Authoritative Nameserver that holds the actual DNS record.",
            "usage": "**DNS Resolution Hierarchy**:<ul><li><b>Root Server</b>: Points to TLD (e.g. '.com')</li><li><b>TLD Server</b>: Points to Authoritative (e.g. 'google.com')</li><li><b>Authoritative Server</b>: Returns actual IP</li></ul>",
            "spanish": "Durante la resolución de DNS, ¿cuál servidor es consultado primero por el resolvedor recursivo local si el registro no está en caché? El servidor de nombres raíz (Root Nameserver).",
            "tags": ["networking", "dns", "fundamentals", "quiz"]
        }
    ],
    "decks/04_Social_and_Humanities/Philosophy/01_Beginner/01_Classical_Foundations.json": [
        {
            "deck": "04_Social_and_Humanities::Philosophy::01_Beginner::01_Classical_Foundations",
            "scenario": "Philosophy: The Socratic Method 🏛️",
            "text": "The Socratic Method of cooperative argumentative dialogue is primarily used to stimulate critical thinking and expose contradictions in assumptions through {{c1::methodical questioning (Elenchus)}}.",
            "explanation": "Socrates did not lecture; instead, he asked questions that forced his interlocutors to clarify their definitions and recognize the logical limits or contradictions in their beliefs.",
            "usage": "Example Question: What is justice?<ul><li>The interlocutor provides a definition.</li><li>Socrates asks a counter-example question.</li><li>The interlocutor revises the definition.</li></ul>",
            "spanish": "El método socrático de diálogo argumentativo cooperativo se utiliza principalmente para estimular el pensamiento crítico y exponer contradicciones en los supuestos mediante preguntas metódicas (Elenchus).",
            "tags": ["philosophy_path", "classical_foundations", "socrates", "quiz"]
        },
        {
            "deck": "04_Social_and_Humanities::Philosophy::01_Beginner::01_Classical_Foundations",
            "scenario": "Philosophy: Plato's Allegory of the Cave 🏛️",
            "text": "Plato's Allegory of the Cave illustrates that humans mistake sensory appearances for reality, and that true knowledge is obtained only by escaping the cave to perceive the {{c1::Theory of Forms (Mundo de las Ideas)}}.",
            "explanation": "The cave dwellers see only shadows cast on walls by a fire and believe the shadows are real objects. Escaping the cave represents the philosopher's journey of using reason to see the immutable, true essence (Forms) of reality.",
            "usage": "Core teaching: The physical world is a shadow/copy; the world of Ideas is the ultimate, immutable truth.",
            "spanish": "La alegoría de la cueva de Platón ilustra que los humanos confunden las apariencias sensoriales con la realidad, y que el conocimiento verdadero se obtiene únicamente al escapar de la cueva para percibir la Teoría de las Formas.",
            "tags": ["philosophy_path", "classical_foundations", "plato"]
        }
    ],
    "decks/03_Languages/English/01_Daily_Life/Airport.json": [
        {
            "deck": "03_Languages::English::01_Daily_Life::Airport",
            "scenario": "English Phonetics: Airport Gate Connected Speech ✈️",
            "text": "At the gate, the announcement \"We will begin boarding in ten minutes\" blends the last two words via consonant-to-consonant linking, making \"in ten\" sound like {{c1::\"int-ten\" [ɪnˈtɛn]}}.",
            "explanation": "When a word ends in /n/ and the next begins with /t/, the alveolar nasal /n/ assimilates or links directly to the alveolar stop /t/ to allow smooth, rapid articulation, resulting in a single elongated nasal-to-stop transition.",
            "usage": "Phonetic Drill: <code>in ten minutes</code> &rarr; \"in-ten\" [ɪnˈtɛn]<br>Contrastive Practice: Pronounce both 'n' and 't' as a single continuous block without a glottal pause.",
            "spanish": "En la puerta, el anuncio \"We will begin boarding in ten minutes\" fusiona las últimas dos palabras mediante enlace consonante-consonante, haciendo que \"in ten\" suene como \"int-ten\".",
            "tags": ["english_scenario", "airport", "phonetics", "connected_speech"]
        },
        {
            "deck": "03_Languages::English::01_Daily_Life::Airport",
            "scenario": "English Daily Life: Airport Baggage Claim ✈️",
            "text": "At the baggage claim desk, if your luggage is missing, you should report it politely saying: \"Excuse me, my bag {{c1::didn't come out}} on the carousel, and I'd like to {{c2::file a claim}}.\"",
            "explanation": "To \"file a claim\" is the official terminology for registering a lost item report. Saying \"didn't come out\" is the natural phrasal expression for baggage that did not arrive.",
            "usage": "Pattern: <code>file a claim / didn't come out on [carousel]</code><ul><li><code>I need to file a claim for my damaged baggage.</code></li><li><code>My suitcase didn't come out on carousel 4.</code></li></ul>",
            "spanish": "En el mostrador de reclamo de equipaje, si tu maleta se perdió, debes reportarlo diciendo educadamente: \"Excuse me, my bag didn't come out on the carousel, and I'd like to file a claim.\"",
            "tags": ["english_scenario", "airport", "conversation", "vocabulary"]
        }
    ]
}

# Append the cards to each target file
for rel_path, cards_to_add in additions.items():
    file_path = os.path.join(base_dir, rel_path)
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        continue
        
    print(f"Updating {rel_path}...")
    with open(file_path, "r", encoding="utf-8") as f:
        existing_cards = json.load(f)
        
    # Prevent duplicate additions
    existing_texts = {c["text"].strip() for c in existing_cards}
    added = 0
    for c in cards_to_add:
        if c["text"].strip() not in existing_texts:
            existing_cards.append(c)
            added += 1
            
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(existing_cards, f, indent=2, ensure_ascii=False)
    print(f"Added {added} cards to {rel_path}.")

print("Card additions complete. Running migration script...")
subprocess.run(["python", "migrate_to_4level_hierarchy.py"], check=True)
print("Hierarchy updated successfully.")
