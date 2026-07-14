import json
import os

database_file = "anki_cards_database.json"

if not os.path.exists(database_file):
    print(f"Error: {database_file} not found.")
    exit(1)

with open(database_file, "r", encoding="utf-8") as f:
    cards = json.load(f)

new_cards = [
    # 01_AI_Agents_Autonomy
    {
        "deck": "Tech_Map_2026::01_AI_Agents_Autonomy",
        "scenario": "AI Agents: Multi-Agent Collaboration 🤝",
        "text": "For distributed task execution, multi-agent systems rely on {{c1::shared-state memory}} or {{c2::blackboard architectures}} to share intermediate results and prevent agents from executing redundant operations.",
        "explanation": "A blackboard architecture is a common pattern where agents read from and write to a global, central workspace (the blackboard). This decoupling lets specialized agents react dynamically to updates without direct agent-to-agent coupling.",
        "usage": "Used in complex orchestration setups where researchers, writers, and checkers need to share an audit log.",
        "spanish": "Para la ejecución de tareas distribuidas, los sistemas multi-agente dependen de la memoria de estado compartido o de arquitecturas de pizarra para compartir resultados intermedios y evitar operaciones redundantes.",
        "tags": ["agents", "multi_agent", "blackboard_architecture"]
    },
    {
        "deck": "Tech_Map_2026::01_AI_Agents_Autonomy",
        "scenario": "AI Agents: Claude Code CLI 💻",
        "text": "Anthropic's {{c1::Claude Code}} operates autonomously on local repositories by directly parsing system diffs, running tests, and executing shell commands using a {{c2::read-eval-print-loop (REPL)}} model.",
        "explanation": "Claude Code is a command-line interface tool that gives Claude agentic access to your local filesystem. It executes developer tasks (like bug fixing or refactoring) by suggesting patches, applying them, running verification tests, and iterating until the tests pass.",
        "usage": "Ideal for command-line-driven codebase exploration, test-driven debugging, and automated git commits.",
        "spanish": "Claude Code de Anthropic opera de forma autónoma en repositorios locales al analizar directamente diferencias del sistema, ejecutar pruebas y comandos de shell utilizando un modelo REPL.",
        "tags": ["agents", "claude_code", "cli"]
    },
    {
        "deck": "Tech_Map_2026::01_AI_Agents_Autonomy",
        "scenario": "AI Agents: Antigravity Framework 🪐",
        "text": "The agentic framework {{c1::Antigravity}} ensures reliability by executing user code in a {{c2::sandboxed environment}} with granular tool permissions and state checkpointing.",
        "explanation": "Antigravity provides developer environments with safe agent runtimes. By checkpointing the execution state, the framework allows long-running agent workflows to pause, seek user approval (Human-in-the-Loop), and safely resume without losing intermediate progress.",
        "usage": "Perfect for enterprise tasks where agents make external API calls or write files that require strict verification.",
        "spanish": "El framework agéntico Antigravity garantiza la confiabilidad al ejecutar código de usuario en un entorno aislado con permisos de herramientas granulares y puntos de control de estado.",
        "tags": ["agents", "antigravity", "sandboxing"]
    },
    {
        "deck": "Tech_Map_2026::01_AI_Agents_Autonomy",
        "scenario": "AI Agents: LLM-as-a-Judge ⚖️",
        "text": "To automate validation in agentic pipelines, {{c1::LLM-as-a-Judge}} implements a multi-model evaluation where a supervisor LLM grades outputs using {{c2::rubric-based scoring}} to calculate alignment.",
        "explanation": "LLM-as-a-Judge uses an LLM (typically a larger, frontier model) to evaluate the quality, tone, or compliance of another LLM's output. By defining strict scoring rubrics and structured JSON schemas, it reduces the need for slow, expensive human evaluations.",
        "usage": "Widely deployed in CI/CD pipelines to measure prompt regression and semantic drift.",
        "spanish": "Para automatizar la validación en flujos agénticos, LLM-as-a-Judge implementa una evaluación multi-modelo donde un LLM supervisor califica las salidas utilizando puntuaciones basadas en rúbricas.",
        "tags": ["agents", "evaluation", "llm_judge"]
    },
    {
        "deck": "Tech_Map_2026::01_AI_Agents_Autonomy",
        "scenario": "AI Agents: LangGraph Cyclic State 🔄",
        "text": "Unlike linear pipelines, {{c1::LangGraph}} models agents as a cyclic state machine where nodes represent actions and edges determine transitions based on the current {{c2::StateGraph object}}.",
        "explanation": "LangGraph is designed for agent workflows that require loops (e.g. an agent writes code, compiles it, encounters an error, and loops back to fix it). It uses a centralized StateGraph that persists checkpoints, enabling human-in-the-loop interventions.",
        "usage": "Used for building highly complex, iterative pipelines where agents must review and correct their own work.",
        "spanish": "A diferencia de los pipelines lineales, LangGraph modela a los agentes como una máquina de estados cíclica donde los nodos representan acciones y las aristas determinan las transiciones según el StateGraph.",
        "tags": ["agents", "langgraph", "state_machine"]
    },

    # 02_Reasoning_LLMs
    {
        "deck": "Tech_Map_2026::02_Reasoning_LLMs",
        "scenario": "Next-Gen LLMs: Test-Time Compute 🧠",
        "text": "Reasoning models increase accuracy during inference by using {{c1::Test-Time Compute}}, letting the model explore reasoning trees using techniques like {{c2::Monte Carlo Tree Search (MCTS)}}.",
        "explanation": "Test-Time Compute shifts complexity from model training to inference. Instead of generating a single output immediately, the model generates internal thought tokens, analyzes multiple alternative paths, and selects the most logical route before printing the final answer.",
        "usage": "Essential for complex mathematics, logical reasoning, code synthesis, and scientific proofs.",
        "spanish": "Los modelos de razonamiento aumentan la precisión en inferencia al usar cómputo en tiempo de prueba, permitiendo al modelo explorar árboles de razonamiento mediante técnicas como MCTS.",
        "tags": ["llm", "test_time_compute", "mcts"]
    },
    {
        "deck": "Tech_Map_2026::02_Reasoning_LLMs",
        "scenario": "Next-Gen LLMs: Vibecoding Paradigm 🎸",
        "text": "In the {{c1::Vibecoding}} paradigm, developers step back from writing physical code syntax and instead act as {{c2::system architects}} directing autonomous agents via iterative natural language prompts.",
        "explanation": "Vibecoding refers to a coding style where the human programmer writes zero code directly, relying entirely on agentic IDEs to implement features, fix bugs, and refactor codebases while the human reviews the changes conceptually.",
        "usage": "Highly effective for rapid prototyping and full-stack web application development.",
        "spanish": "En el paradigma de Vibecoding, los desarrolladores dejan de escribir sintaxis física de código y actúan como arquitectos de sistemas que dirigen agentes autónomos mediante instrucciones de lenguaje natural.",
        "tags": ["llm", "vibecoding", "software_development"]
    },
    {
        "deck": "Tech_Map_2026::02_Reasoning_LLMs",
        "scenario": "Next-Gen LLMs: LlamaIndex Workflows 🧬",
        "text": "For event-driven agentic architectures, {{c1::LlamaIndex Workflows}} uses Python decorators like {{c2::@step}} to trigger asynchronous methods based on custom event classes.",
        "explanation": "LlamaIndex Workflows provides an event-driven framework where step functions subscribe to specific event types, process data, and publish new events. This decouples the agent logic, making it easy to create complex, parallel agent execution paths.",
        "usage": "Used to ingest multi-source documents where raw text, tables, and images are routed to different parsing pipelines asynchronously.",
        "spanish": "Para arquitecturas agénticas impulsadas por eventos, LlamaIndex Workflows utiliza decoradores de Python como @step para activar métodos asíncronos basados en clases de eventos personalizados.",
        "tags": ["llm", "llamaindex", "workflows"]
    },
    {
        "deck": "Tech_Map_2026::02_Reasoning_LLMs",
        "scenario": "Next-Gen LLMs: Small Language Models (SLMs) 📱",
        "text": "To run reasoning tasks locally on edge devices, developers apply {{c1::quantization (e.g., GGUF, AWQ)}} to compress Large Language Models into high-performance {{c2::Small Language Models (SLMs)}}.",
        "explanation": "SLMs (typically under 14B parameters) can run locally on laptops or mobile phones. Quantization reduces the precision of the model weights (e.g. from 16-bit float to 4-bit integer), massively decreasing memory consumption while maintaining high performance.",
        "usage": "Essential for privacy-first applications, offline environments, and low-latency local interactions.",
        "spanish": "Para ejecutar tareas de razonamiento localmente en dispositivos periféricos, los desarrolladores aplican cuantización (GGUF, AWQ) para comprimir LLMs en SLMs de alto rendimiento.",
        "tags": ["llm", "slm", "quantization"]
    },
    {
        "deck": "Tech_Map_2026::02_Reasoning_LLMs",
        "scenario": "Next-Gen LLMs: Dynamic Context Attention 🔍",
        "text": "To support long-context windows efficiently, models use {{c1::Prefix Caching}} and optimized attention runtimes like {{c2::FlashAttention-3}} to avoid recomputing Key-Value (KV) matrices.",
        "explanation": "Dynamic context windows allow models to ingest millions of tokens. FlashAttention-3 optimizes the compute-heavy attention step on modern GPUs by reducing memory reads/writes. Prefix Caching stores past conversations in GPU memory, avoiding redundant computation.",
        "usage": "Crucial for codebases or documents that span millions of tokens, enabling agents to parse complete source trees in one request.",
        "spanish": "Para soportar ventanas de contexto largo de manera eficiente, los modelos usan caché de prefijos y optimizaciones como FlashAttention-3 para evitar calcular de nuevo las matrices KV.",
        "tags": ["llm", "flash_attention", "context_window"]
    },

    # 03_Advanced_RAG
    {
        "deck": "Tech_Map_2026::03_Advanced_RAG",
        "scenario": "Advanced RAG: Multimodal Retrieval 🖼️",
        "text": "Instead of extracting plain text from complex documents, multimodal RAG uses models like {{c1::ColPali}} to generate vector embeddings directly from {{c2::rendered document images}}.",
        "explanation": "Traditional RAG struggles with charts, tables, and PDFs because the parsing step loses structural layouts. ColPali represents pages as images and extracts semantic visual-textual patches, embedding them directly into vector spaces for highly accurate visual document retrieval.",
        "usage": "Highly recommended for reading financial statements, engineering blueprints, and slides.",
        "spanish": "En lugar de extraer texto plano de documentos complejos, el RAG multimodal utiliza modelos como ColPali para generar embeddings vectoriales directamente a partir de imágenes renderizadas de los documentos.",
        "tags": ["rag", "multimodal", "colpali"]
    },
    {
        "deck": "Tech_Map_2026::03_Advanced_RAG",
        "scenario": "Advanced RAG: Hybrid Search 🔀",
        "text": "Industrial RAG applications implement hybrid search by combining semantic {{c1::dense vector retrieval}} with keyword-based {{c2::sparse BM25 retrieval}} and merging results using Reciprocal Rank Fusion (RRF).",
        "explanation": "Dense vectors capture general concept meanings but miss exact keyword match strings (like serial codes or product names). Sparse retrieval (BM25) targets keyword precision. Combining both via RRF yields optimal search recall and accuracy.",
        "usage": "Standard production search architecture for enterprise wikis and code search tools.",
        "spanish": "Las aplicaciones RAG industriales implementan búsquedas híbridas combinando la recuperación de vectores densos con la recuperación de palabras clave BM25, uniendo los resultados mediante RRF.",
        "tags": ["rag", "hybrid_search", "rrf"]
    },
    {
        "deck": "Tech_Map_2026::03_Advanced_RAG",
        "scenario": "Advanced RAG: GraphRAG 🕸️",
        "text": "To capture global, high-level summaries of massive text datasets, {{c1::GraphRAG}} builds knowledge graphs using LLMs and clusters them with algorithms like {{c2::Leiden community detection}}.",
        "explanation": "GraphRAG extracts structured entities and relations from texts to construct a Knowledge Graph. It then groups nodes into hierarchical communities. When a user asks a global query (e.g., 'What are the main issues in this repository?'), the model summarizes the clusters instead of performing keyword searches.",
        "usage": "Perfect for broad corpus summaries, compliance audits, and architectural mapping.",
        "spanish": "Para capturar resúmenes globales de conjuntos de datos masivos, GraphRAG construye gráficos de conocimiento con LLMs y los agrupa mediante algoritmos como la detección de comunidades de Leiden.",
        "tags": ["rag", "graphrag", "knowledge_graphs"]
    },
    {
        "deck": "Tech_Map_2026::03_Advanced_RAG",
        "scenario": "Advanced RAG: Corrective RAG (CRAG) 🧯",
        "text": "{{c1::Corrective RAG (CRAG)}} adds a self-correction loop where a evaluator agent assesses search result quality; if quality falls below a threshold, it triggers a fallback search using {{c2::external web APIs}}.",
        "explanation": "If retrieved documents are irrelevant, traditional RAG outputs incorrect answers (hallucinations). CRAG inserts a logic gate: if the retrieved context is classified as 'incorrect' or 'irrelevant', the system triggers Tavily or Google Search to fetch verified web documentation.",
        "usage": "Critical for dynamic, high-stakes support pipelines where stale documentation causes system failures.",
        "spanish": "Corrective RAG (CRAG) añade un ciclo de autoconrección donde un agente evaluador califica los resultados de búsqueda; si la calidad es baja, activa una búsqueda alternativa en APIs web externas.",
        "tags": ["rag", "crag", "web_search"]
    },
    {
        "deck": "Tech_Map_2026::03_Advanced_RAG",
        "scenario": "Advanced RAG: Semantic Chunking 📑",
        "text": "To prevent context loss, {{c1::Semantic Chunking}} splits documents by measuring the {{c2::cosine distance}} of embeddings between consecutive sentences, creating boundaries when semantic flow shifts.",
        "explanation": "Traditional chunking splits documents by arbitrary token counts, often cutting sentences or paragraphs in half. Semantic chunking calculates embeddings for every sentence and groups them into a chunk until the semantic similarity between adjacent blocks drops below a threshold.",
        "usage": "Essential for preprocessing lengthy technical guidelines, legal contracts, and novels.",
        "spanish": "Para evitar la pérdida de contexto, el fragmentado semántico divide los documentos midiendo la distancia de coseno entre oraciones consecutivas, creando límites cuando cambia el flujo semántico.",
        "tags": ["rag", "semantic_chunking", "preprocessing"]
    },

    # 04_Agentic_Dev_IDEs
    {
        "deck": "Tech_Map_2026::04_Agentic_Dev_IDEs",
        "scenario": "Agentic IDEs: Codebase Rules and Config 📐",
        "text": "Next-generation IDEs like Cursor customize agent behavior using root configuration files called {{c1::.cursorrules}} to define development standards and enforce local styling.",
        "explanation": ".cursorrules files sit at the root of a project. They instruct Cursor's codebase agent on specific architectural choices (e.g. 'Use Next.js Server Actions, prefer Tailwind, do not use library X'), preventing the AI from generating obsolete patterns.",
        "usage": "Best practice for onboarding teams and keeping LLM code outputs consistent across microservices.",
        "spanish": "Los IDEs de próxima generación como Cursor personalizan el comportamiento de los agentes mediante archivos de configuración en la raíz llamados .cursorrules para establecer estándares y estilos.",
        "tags": ["ide", "cursorrules", "configuration"]
    },
    {
        "deck": "Tech_Map_2026::04_Agentic_Dev_IDEs",
        "scenario": "Agentic IDEs: Windsurf Shared Terminal 🖥️",
        "text": "The agentic editor {{c1::Windsurf}} uses a shared state model called 'Flows', allowing the AI to read your open file contexts, suggest edits, and directly execute commands in the {{c2::integrated terminal}}.",
        "explanation": "Windsurf breaks the boundary of conversational chats by integrating the IDE terminal, file system, and chat context. The agent does not just print code blocks; it compiles, tests, and reads the output directly, resolving issues iteratively.",
        "usage": "Perfect for complex debugging sessions where the agent needs to compile and test code in real time.",
        "spanish": "El editor agéntico Windsurf utiliza un modelo de estado compartido llamado 'Flows', permitiendo a la IA leer los archivos abiertos, sugerir ediciones y ejecutar comandos en la terminal integrada.",
        "tags": ["ide", "windsurf", "flows"]
    },
    {
        "deck": "Tech_Map_2026::04_Agentic_Dev_IDEs",
        "scenario": "Agentic IDEs: In-Browser Sandboxes 🌐",
        "text": "Web-based development platforms like Bolt.new run complete Node.js development servers inside the browser using WebAssembly-driven {{c1::WebContainers}}.",
        "explanation": "WebContainers allow full-stack environments (Vite, Express, etc.) to run directly in the browser's sandbox without installing Node locally. This allows AI agents to instantly provision, preview, and build applications securely in seconds.",
        "usage": "Used in text-to-app tools for instant frontend/backend preview and code generation.",
        "spanish": "Las plataformas de desarrollo basadas en web como Bolt.new ejecutan servidores de desarrollo Node.js completos dentro del navegador utilizando WebContainers basados en WebAssembly.",
        "tags": ["ide", "webcontainers", "bolt_new"]
    },
    {
        "deck": "Tech_Map_2026::04_Agentic_Dev_IDEs",
        "scenario": "Agentic IDEs: Copilot Workspace Specs 📝",
        "text": "In {{c1::Copilot Workspace}}, the agent creates a structured {{c2::Task Specification Plan}} before making codebase edits, allowing the developer to review and refine the changes before execution.",
        "explanation": "Instead of immediately writing code, Copilot Workspace forces the agent to write a step-by-step design spec plan first. The developer audits this plan, adjusts the logic, and then clicks approve to let the agent apply edits across multiple files in the repository.",
        "usage": "Useful for managing complex feature requests and PR code reviews in GitHub workflows.",
        "spanish": "En Copilot Workspace, el agente crea una especificación de plan de tareas estructurada antes de editar el código, lo que permite al desarrollador revisar y refinar los cambios antes de su ejecución.",
        "tags": ["ide", "copilot_workspace", "planning"]
    },
    {
        "deck": "Tech_Map_2026::04_Agentic_Dev_IDEs",
        "scenario": "Agentic IDEs: Automated Agentic Auditing 🛡️",
        "text": "To secure CI/CD pipelines, modern teams deploy {{c1::Agentic Auditing}} where autonomous LLM panels review pull requests for vulnerabilities (SAST) and enforce {{c2::architectural compliance}}.",
        "explanation": "Traditional linters check syntax, but agentic auditors check logic. An agentic auditor evaluates pull requests by simulating attack vectors, checking for API design violations, and auditing database query efficiencies before code is merged.",
        "usage": "Integrating LLM safety checkers into GitHub Actions or GitLab CI workflows.",
        "spanish": "Para asegurar los pipelines CI/CD, los equipos despliegan auditorías agénticas donde paneles de LLM revisan solicitudes de extracción (PR) buscando vulnerabilidades y haciendo cumplir el diseño arquitectónico.",
        "tags": ["ide", "auditing", "cicd"]
    },

    # 05_Infrastructure_Science
    {
        "deck": "Tech_Map_2026::05_Infrastructure_Science",
        "scenario": "Frontier Tech: Sovereign Clouds & Residency ☁️",
        "text": "Due to strict privacy laws and geopolitics, enterprise AI uses {{c1::Geopatriation}} to migrate data and models from public global clouds to {{c2::sovereign, air-gapped infrastructure}}.",
        "explanation": "Geopatriation is the process of moving compute and database workloads back into local, country-specific clouds or private datacenters. This ensures that sensitive business intellectual property and customer data are not exposed to foreign jurisdictions during LLM processing.",
        "usage": "Common in healthcare, banking, and government sectors deploying high-security LLMs.",
        "spanish": "Debido a leyes de privacidad estrictas y geopolítica, la IA empresarial utiliza la geopatriación para migrar datos y modelos de nubes públicas globales a infraestructuras soberanas y aisladas.",
        "tags": ["infrastructure", "geopatriation", "privacy"]
    },
    {
        "deck": "Tech_Map_2026::05_Infrastructure_Science",
        "scenario": "Frontier Tech: Post-Quantum Cryptography (PQC) 🔐",
        "text": "To protect encrypted assets from future quantum computers, organizations are migrating to lattice-based cryptography standards like {{c1::ML-KEM}} for key encapsulation and {{c2::ML-DSA}} for digital signatures.",
        "explanation": "Standard encryption algorithms like RSA and ECC are vulnerable to quantum computing decryption using Shor's algorithm. NIST has standardized ML-KEM and ML-DSA, which are post-quantum cryptosystems based on the hardness of mathematical lattice problems.",
        "usage": "Standard practice for modern TLS handshakes, banking transactions, and security keys.",
        "spanish": "Para proteger activos cifrados de futuras computadoras cuánticas, las organizaciones están migrando a estándares como ML-KEM para encapsulado de claves y ML-DSA para firmas digitales.",
        "tags": ["infrastructure", "pqc", "quantum_security"]
    },
    {
        "deck": "Tech_Map_2026::05_Infrastructure_Science",
        "scenario": "Frontier Tech: AI in Material Discovery 🔬",
        "text": "AI databases like Google's GNoME accelerate material discovery by using {{c1::graph neural networks (GNNs)}} to predict crystal stability and screen alternatives for {{c2::solid-state sodium batteries}}.",
        "explanation": "Discovering new materials historically took decades of laboratory trial-and-error. DeepMind's GNoME uses Graph Neural Networks to predict the stability of millions of crystal structures, immediately identifying candidate materials for next-generation sodium batteries and superconductors.",
        "usage": "Accelerating research in green energy storage, materials engineering, and physics.",
        "spanish": "Las bases de datos de IA como GNoME aceleran el descubrimiento de materiales al usar redes neuronales gráficas para predecir la estabilidad de cristales e investigar alternativas para baterías de estado sólido.",
        "tags": ["science", "gnome", "materials_science"]
    },
    {
        "deck": "Tech_Map_2026::05_Infrastructure_Science",
        "scenario": "Frontier Tech: Autonomous Digital Twins 🏭",
        "text": "Industrial facilities deploy {{c1::Autonomous Digital Twins}} combining real-time IoT telemetry with {{c2::Physics-Informed Neural Networks (PINNs)}} to predict equipment fatigue and automate maintenance.",
        "explanation": "A digital twin is a virtual model of a physical asset. By combining real-time telemetry with PINNs—neural networks that embed physical laws (like thermodynamics or fluid dynamics) into their loss functions—the digital twin can predict physical structural failure before it happens.",
        "usage": "Deployed in smart factories, aerospace operations, and offshore wind turbines.",
        "spanish": "Las instalaciones industriales despliegan gemelos digitales autónomos que combinan telemetría IoT con redes neuronales informadas por la física para predecir fallas y programar mantenimiento.",
        "tags": ["science", "digital_twins", "pinns"]
    },
    {
        "deck": "Tech_Map_2026::05_Infrastructure_Science",
        "scenario": "Frontier Tech: Wetware & Biocomputing 🧠",
        "text": "In frontier biocomputing, researchers interface living cells with silicon chips, creating {{c1::Wetware Computers}} that use biological neurons to process inputs via {{c2::microelectrode arrays (MEAs)}}.",
        "explanation": "Wetware computing (or organic computing) merges biological brain organoids or engineered networks with hardware. The microelectrode arrays send electrical stimulation to the cells and record their responses, using the natural learning capabilities of biological systems to process data with extremely low energy consumption.",
        "usage": "Experimental research into neuromorphic computing and biological neural network simulations.",
        "spanish": "En biocomputación de frontera, los investigadores conectan células vivas con chips de silicio, creando computadoras húmedas que procesan señales con neuronas biológicas a través de matrices de microelectrodos.",
        "tags": ["science", "biocomputing", "wetware"]
    },

    # 06_MLOps_Guardrails
    {
        "deck": "Tech_Map_2026::06_MLOps_Guardrails",
        "scenario": "MLOps: Agentic Observability 🔍",
        "text": "Observability tools like LangSmith track agent workflows by recording nested traces, calculating token usage, and visualizing {{c1::spans}} that represent {{c2::tool executions}}.",
        "explanation": "Agentic workflows are non-deterministic and call multiple models and APIs in loops. Observability platforms capture traces (the execution path) and break them into spans (individual API calls or tool executions), making it easy to isolate where an agent crashed, hallucinated, or wasted tokens.",
        "usage": "Standard monitoring stack for debugging prompt latency and diagnosing failing agent agents.",
        "spanish": "Las herramientas de observabilidad como LangSmith rastrean los flujos agénticos al registrar trazas anidadas y visualizar 'spans' que representan las ejecuciones de herramientas.",
        "tags": ["mlops", "observability", "langsmith"]
    },
    {
        "deck": "Tech_Map_2026::06_MLOps_Guardrails",
        "scenario": "MLOps: Guardrails and Input Control 🛡️",
        "text": "NVIDIA's {{c1::NeMo Guardrails}} enforces safety policies in LLM responses by using a domain-specific language called {{c2::Colang}} to define disallowed topics and dialog flows.",
        "explanation": "Guardrail frameworks sit between the user and the LLM. Using Colang, developers define patterns for user input and model output. If the guardrail system detects a jailbreak attempt, or if the model tries to answer questions outside its defined scope, the interaction is blocked.",
        "usage": "Required for building public-facing enterprise chatbots that must avoid controversial topics.",
        "spanish": "NeMo Guardrails de NVIDIA hace cumplir políticas de seguridad en respuestas de LLMs utilizando un lenguaje específico de dominio llamado Colang para bloquear temas no deseados.",
        "tags": ["mlops", "guardrails", "nemo"]
    },
    {
        "deck": "Tech_Map_2026::06_MLOps_Guardrails",
        "scenario": "MLOps: Prompt Caching Mechanics ⚡",
        "text": "Prompt Caching reduces inferencing cost and latency by storing the {{c1::Key-Value (KV) cache}} of long system prompts and reusing them for queries that share the same {{c2::prefix context}}.",
        "explanation": "For long-context queries (e.g. documentation, books, system templates), computing the KV matrix at every turn is slow and expensive. Prompt caching flags identical prefix tokens in GPU memory. Reusing this precomputed KV cache reduces Time-To-First-Token (TTFT) and cuts input costs.",
        "usage": "Highly effective for multi-turn conversational agents with massive system rules or documents.",
        "spanish": "El almacenamiento en caché de prompts reduce los costos e inferencia y la latencia al guardar el KV cache de prompts del sistema largos y reutilizarlos para consultas con el mismo prefijo.",
        "tags": ["mlops", "prompt_caching", "inference"]
    },
    {
        "deck": "Tech_Map_2026::06_MLOps_Guardrails",
        "scenario": "MLOps: vLLM & Inference Runtimes 🚀",
        "text": "To maximize GPU throughput, inference engines like vLLM implement {{c1::PagedAttention}}, which dynamically allocates KV cache memory in non-contiguous physical spaces, preventing {{c2::memory fragmentation}}.",
        "explanation": "Static allocation of GPU memory for KV caches leads to severe fragmentation and limits batch sizes. PagedAttention borrows paging concepts from operating systems, dividing the KV cache into pages that can be stored anywhere in physical memory, boosting serving capacity.",
        "usage": "The standard open-source stack for serving LLMs at high concurrency.",
        "spanish": "Para maximizar el rendimiento de la GPU, los motores de inferencia como vLLM implementan PagedAttention, que asigna dinámicamente la memoria KV en bloques no contiguos para evitar la fragmentación.",
        "tags": ["mlops", "vllm", "inference_optimization"]
    },
    {
        "deck": "Tech_Map_2026::06_MLOps_Guardrails",
        "scenario": "MLOps: Reinforcement Learning from AI Feedback (RLAIF) 🤖",
        "text": "Instead of relying on human labelers, models are aligned using {{c1::RLAIF}}, where a supervisor model generates preference labels that are optimized using algorithms like {{c2::Direct Preference Optimization (DPO)}}.",
        "explanation": "Traditional RLHF requires thousands of hours of human labeling, which is slow and hard to scale. RLAIF uses another LLM acting under a 'Constitution' to critique outputs. The preference data is then fed directly into DPO, which adjusts model weights directly without separate reward model training.",
        "usage": "Used to align model safety, formatting compliance, and reasoning paths at scale.",
        "spanish": "En lugar de depender de etiquetadores humanos, los modelos se alinean usando RLAIF, donde un modelo supervisor genera etiquetas de preferencia optimizadas mediante algoritmos como DPO.",
        "tags": ["mlops", "rlaif", "dpo"]
    }
]

# Avoid adding duplicates
existing_scenarios = {c["scenario"] for c in cards}
added_count = 0

for card in new_cards:
    if card["scenario"] not in existing_scenarios:
        cards.append(card)
        added_count += 1

with open(database_file, "w", encoding="utf-8") as f:
    json.dump(cards, f, indent=2, ensure_ascii=False)

print(f"Successfully added {added_count} new cards. Total cards in database: {len(cards)}.")
