import json
import os

adk_mastery_cards = [
    {
        "scenario": "ADK Architecture: Layered Isolation 🏗️",
        "text": "When debugging ADK agents, isolate issues to three layers: the {{c1::ADK Framework}} coordinates system prompts and memory; the {{c2::Model Context Protocol (MCP)}} manages tool execution; and the {{c3::Agent Engine Runtime}} hosts the Cloud Run container.",
        "explanation": "Isolating the issue to the correct layer prevents wasting time debugging Cloud Run container timeouts when the root cause is a local MCP schema mismatch.",
        "usage": "Layer isolation check:<ul><li>Prompt/Memory -> ADK</li><li>Schema/Tool -> MCP</li><li>Permissions/VPC/Timeout -> Agent Engine Runtime</li></ul>",
        "spanish": "Al depurar agentes de ADK, aísle los problemas en tres capas: ADK Framework coordina prompts y memoria; MCP maneja la ejecución de herramientas; y Agent Engine Runtime aloja el contenedor.",
        "tags": ["adk", "architecture", "agent_engine"]
    },
    {
        "scenario": "ADK Architecture: Tenant Project 🏗️",
        "text": "When you deploy an ADK agent using reasoning_engines.ReasoningEngine.create(), the container is deployed in a Google-managed {{c1::Tenant Project}} linked to your billing account.",
        "explanation": "Because the agent container does not run directly in your User Project, certain low-level startup logs are not written to your project's Cloud Logging.",
        "usage": "Architecture: <code>User Project (GCS/IAM) &larr; VPC-SC/PSC &rarr; Tenant Project (Cloud Run Agent)</code>.",
        "spanish": "Al implementar un agente de ADK, el contenedor se implementa en un Proyecto Inquilino (Tenant Project) administrado por Google.",
        "tags": ["adk", "architecture", "tenant_project"]
    },
    {
        "scenario": "ADK Architecture: Low-Level Debugging 🔍",
        "text": "If your agent fails during container initialization (before it can write logs to your User Project), you must view logs using the {{c1::uCAIP Debug Console}} (go/ucaip-debug-console) or Sherlog.",
        "explanation": "Container startup crashes (e.g. pickle import errors) occur before the user project logging sidecar initializes.",
        "usage": "Tool: <code>go/ucaip-debug-console</code> (Internal Google Console).",
        "spanish": "Si tu agente falla durante la inicialización del contenedor, debes ver los registros usando la consola de depuración de uCAIP (go/ucaip-debug-console).",
        "tags": ["adk", "debugging", "ucaip"]
    },
    {
        "scenario": "ADK Platform: Universal Language Settings 🌐",
        "text": "To prevent {{c1::Piccolo}} routing validation errors when running background tasks, never delete dev roles to bypass ULS blocks; instead, ensure both prod and dev URIs are whitelisted.",
        "explanation": "Whitelisting prod and dev URIs in the processors (e.g. supportability-themes and supportability-themes-dev-jobs) prevents routing blocks.",
        "usage": "Config rule: <code>Never delete dev roles; ensure both URIs are whitelisted in data flow definitions.</code>",
        "spanish": "Para evitar errores de validación de enrutamiento de Piccolo al ejecutar tareas en segundo plano, asegúrese de que tanto el URI de prod como el de dev estén en la lista blanca de ULS.",
        "tags": ["adk", "uls", "piccolo"]
    },
    {
        "scenario": "ADK Networking: Ingress Routing 🔒",
        "text": "To route traffic from the Cloud Run tenant container into your private VPC network securely, Orcas uses {{c1::Private Service Connect Interfaces (PSC-I)}}.",
        "explanation": "If your User Project is inside a VPC Service Controls (VPC-SC) perimeter, PSC-I allows secure ingress crossing the boundary.",
        "usage": "Access configuration: <code>VPC-SC Boundaries -> PSC Interfaces for secure routing.</code>",
        "spanish": "Para enrutar el tráfico del contenedor inquilino de Cloud Run a tu red de VPC privada de forma segura, se utilizan interfaces de Private Service Connect (PSC-I).",
        "tags": ["adk", "networking", "vpc_sc", "psc"]
    },
    {
        "scenario": "ADK Components: Tool Fallback 🛠️",
        "text": "To prevent agent crashes when a primary API is offline, implement robust error handling inside the tool, and define a {{c1::fallback tool}} (like Google Search) to salvage the response.",
        "explanation": "If a primary tool throws a ConnectionError, catching the error and invoking a fallback tool ensures the agent remains functional.",
        "usage": "Code pattern: <code>try: call_primary() except: call_fallback()</code>",
        "spanish": "Para evitar bloqueos del agente cuando una API principal está caída, implementa el manejo de errores e invoca una herramienta de respaldo (como Google Search).",
        "tags": ["adk", "tools", "error_handling"]
    },
    {
        "scenario": "ADK Components: Standalone Auth 🔑",
        "text": "Running standalone scripts that call ADK services requires configuring {{c1::Application Default Credentials (ADC)}} or setting the GOOGLE_APPLICATION_CREDENTIALS variable.",
        "explanation": "If credentials are not explicitly passed or inherited, calls to memory banks or Vertex AI services will fail with Gaia ID not found errors.",
        "usage": "Setup: <code>gcloud auth application-default login</code> or setting <code>os.environ['GOOGLE_APPLICATION_CREDENTIALS']</code>.",
        "spanish": "La ejecución de scripts independientes que llaman a servicios de ADK requiere configurar las Credenciales Predeterminadas de la Aplicación (ADC) o la variable GOOGLE_APPLICATION_CREDENTIALS.",
        "tags": ["adk", "auth", "adc"]
    },
    {
        "scenario": "ADK Components: Tool Confirmation 🔒",
        "text": "In ADK v1.14+, to prevent tool execution from waiting for user confirmation on read-only tools in automated scripts, set {{c1::require_tool_confirmation=False}}.",
        "explanation": "By default, ADK requires user confirmation for tool execution to prevent destructive actions, but this blocks automated background runtimes.",
        "usage": "Agent config: <code>ReasoningEngineAgent(..., require_tool_confirmation=False)</code>",
        "spanish": "En ADK v1.14+, para evitar que la ejecución de herramientas espere la confirmación del usuario para herramientas de lectura, establezca require_tool_confirmation=False.",
        "tags": ["adk", "mcp", "tools"]
    },
    {
        "scenario": "ADK GCS Storage: Path Resolution 🪣",
        "text": "In ADK, `GcsArtifactService` saves user-scoped files under the path `gs://{bucket}/{app}/{user_id}/user/{file}` and session-scoped files under `gs://{bucket}/{app}/{user_id}/{{c1::session_id}}/{file}`.",
        "explanation": "If app_name is omitted, it defaults to a random UUID locally, or GOOGLE_CLOUD_AGENT_ENGINE_ID when deployed, causing path drift.",
        "usage": "Rule: <code>Anchor app_name inside AdkApp configuration to ensure stable GCS path resolution.</code>",
        "spanish": "En ADK, GcsArtifactService guarda los archivos del usuario bajo la ruta con el ID del usuario, y los archivos de sesión bajo el ID de sesión.",
        "tags": ["adk", "gcs", "artifact_drift"]
    },
    {
        "scenario": "ADK Security: Deployed SA IAM 🖼️",
        "text": "To let a deployed agent read GCS images and execute model queries, you must grant the Agent Engine Service Account both {{c1::roles/storage.objectViewer}} and {{c2::roles/aiplatform.user}}.",
        "explanation": "While your local environment uses your user credentials, the deployed container runs under the Agent Engine SA (service-PROJECT_NUMBER@gcp-sa-aiplatform-re.iam.gserviceaccount.com).",
        "usage": "Command: <code>gcloud projects add-iam-policy-binding PROJECT_ID --member=\"serviceAccount:service-...@gcp-sa-aiplatform-re.iam.gserviceaccount.com\" --role=\"roles/...\"</code>",
        "spanish": "Para permitir que un agente implementado lea imágenes de GCS y ejecute consultas, debe otorgar a la Cuenta de Servicio de Agent Engine los roles de storage.objectViewer y aiplatform.user.",
        "tags": ["adk", "iam", "permissions"]
    },
    {
        "scenario": "ADK Security: Cross-Project Function Auth 🗺️",
        "text": "For an agent in Project A to call a private Cloud Function in Project B, Project A's Agent Engine Service Account must be granted the {{c1::roles/cloudfunctions.invoker}} role in Project B.",
        "explanation": "Cloud Functions in different projects require explicit IAM invoker permissions for the caller's service account identity.",
        "usage": "Access control: <code>gcloud functions add-iam-policy-binding function-name --project=project-b --member=serviceAccount:agent-sa-project-a --role=roles/cloudfunctions.invoker</code>",
        "spanish": "Para que un agente del Proyecto A llame a una Cloud Function privada en el Proyecto B, la cuenta de servicio de Agent Engine del Proyecto A debe tener el rol de invoker de Cloud Functions en el Proyecto B.",
        "tags": ["adk", "iam", "cross_project"]
    },
    {
        "scenario": "ADK Models: Endpoint Mismatch 🗺️",
        "text": "To call a global model from a regional Agent Engine instance and avoid endpoint routing errors, instantiate the model passing a custom client with global endpoint override to {{c1::api_client}}.",
        "explanation": "A regional Agent Engine (e.g. us-central1) cannot natively route queries to global model names without an overridden API client.",
        "usage": "Code: <code>global_client = genai.Client(http_options={'api_version': 'v1'}); model = GeminiModel(client=global_client)</code>",
        "spanish": "Para llamar a un modelo global desde una instancia regional de Agent Engine y evitar errores, cree el cliente global e indíquele que lo use en api_client.",
        "tags": ["adk", "models", "endpoints"]
    },
    {
        "scenario": "ADK Persistence: Session Memory 💾",
        "text": "To prevent conversation history loss from stateless container restarts, register the {{c1::VertexAiMemoryBankService}} in your AdkApp configuration.",
        "explanation": "Cloud Run instances are stateless and recycle periodically. Long-term session turn persistence requires a database-backed memory bank.",
        "usage": "Code: <code>app = AdkApp(..., memory_service_builder=lambda: VertexAiMemoryBankService(...))</code>",
        "spanish": "Para evitar la pérdida del historial de conversación por reinicios del contenedor, registre el VertexAiMemoryBankService en AdkApp.",
        "tags": ["adk", "memory", "session_persistence"]
    },
    {
        "scenario": "ADK Multi-Agent: Shared Artifacts 🔗",
        "text": "To avoid exhausting prompt token limits when passing large data between agents, write the data to the shared {{c1::GcsArtifactService}} and let the consumer load it via InvocationContext.",
        "explanation": "Passing huge JSON files directly inside agent-to-agent (A2A) prompt strings consumes excessive tokens and increases cost.",
        "usage": "Flow: <code>ctx.artifact_service.save_artifact(...) &rarr; Consumer loads via ctx.artifact_service.load_artifact(...)</code>",
        "spanish": "Para evitar agotar el límite de tokens al pasar datos grandes entre agentes, escriba los datos en el GcsArtifactService compartido y deje que el consumidor los lea.",
        "tags": ["adk", "multi_agent", "artifacts"]
    },
    {
        "scenario": "ADK Multi-Agent: Handoff Pattern 🤝",
        "text": "To break a monolithic agent into a hierarchical network and improve tool selection, wrap sub-agents inside {{c1::AgentTool}} and register them as tools in the parent agent.",
        "explanation": "A single agent with 20+ tools dilutes context and causes incorrect tool selection. Delegating to specialized sub-agents via AgentTool solves this.",
        "usage": "Code: <code>shop_agent = BaseAgent(..., tools=[AgentTool(agent=research_agent)])</code>",
        "spanish": "Para dividir un agente monolítico y mejorar la selección de herramientas, envuelva los subagentes dentro de AgentTool y regístrelos en el agente padre.",
        "tags": ["adk", "multi_agent", "agent_tool"]
    },
    {
        "scenario": "ADK Components: Dynamic Prompting 🎨",
        "text": "To update system instructions without rebuilding and redeploying the container, load the prompt dynamically from a {{c1::Firestore}} document during initialization.",
        "explanation": "Hardcoding instructions inside the container forces a full deploy cycle for every prompt adjustment. Loading from Firestore enables hot updates.",
        "usage": "Code: <code>instruction = firestore.Client().collection('prompts').document('agent').get().to_dict().get('prompt')</code>",
        "spanish": "Para actualizar las instrucciones del sistema sin reconstruir el contenedor, cargue el prompt dinámicamente desde Firestore.",
        "tags": ["adk", "firestore", "dynamic_prompting"]
    },
    {
        "scenario": "ADK Security: CMEK Coexistence 🔑",
        "text": "To prevent CMEK UI errors like 'default assistant cannot be found', all DataStores within a single App/Engine must {{c1::share the exact same CMEK}} configuration.",
        "explanation": "Mixed CMEK settings (some encrypted Datastores, some unencrypted) within one App will trigger database access and parsing crashes.",
        "usage": "Rule: <code>Verify CMEK configuration from inception; you cannot retroactively mix Datastores.</code>",
        "spanish": "Para evitar errores de CMEK donde no se encuentra el asistente, todos los DataStores dentro de una App deben compartir exactamente la misma configuración de CMEK.",
        "tags": ["adk", "security", "cmek"]
    },
    {
        "scenario": "ADK Security: CMEK Key Restoration 🔑",
        "text": "If a restored KMS key shows 'not ready for use' due to sync lag, the customer should {{c1::Disable and then Enable}} the key version in KMS to force a cache reset.",
        "explanation": "Discovery Engine caches the key status in Spanner. Toggle-disabling/enabling the key version forces the internal monitoring pipeline to refresh.",
        "usage": "Lag recovery: <code>Disable key version &rarr; wait 10 seconds &rarr; Enable key version (note: data reconstruction can take up to 10 hours)</code>",
        "spanish": "Si una clave KMS restaurada se muestra como no lista para usar por retraso de sincronización, el cliente debe Deshabilitar y luego Habilitar la versión.",
        "tags": ["adk", "security", "cmek", "key_issue"]
    },
    {
        "scenario": "ADK Security: WIF Case Sensitivity 🪪",
        "text": "Workforce Identity Federation (WIF) subject matching is strictly {{c1::case-sensitive}}; mismatched casings between IDP tokens (e.g. PascalCase) and Spanner ACL tags cause search blocks.",
        "explanation": "If a user is authenticated as 'Aaron' but documents are tagged with 'aaron', the search engine blocks access. IDP rules must force lowercase.",
        "usage": "Mitigation: <code>IDP transformation rule (.lower()) or Spanner migration to coerce all user identities to lowercase.</code>",
        "spanish": "La coincidencia de sujetos en WIF es estrictamente sensible a mayúsculas y minúsculas; las discrepancias con las etiquetas de Spanner bloquean el acceso.",
        "tags": ["adk", "wif", "identity"]
    },
    {
        "scenario": "ADK Prompts: Constraint Placement 🧠",
        "text": "To protect against prompt injections and ensure the model respects negative constraints, place critical constraints in a block at the {{c1::absolute end}} of the system instructions.",
        "explanation": "If negative constraints are diluted inside a long, early system instruction block, the model's attention is diverted by context.",
        "usage": "Formatting: <code>Place constraint blocks like 'Never share financial data' at the absolute end of instructions.</code>",
        "spanish": "Para protegerse contra inyecciones de prompt y garantizar que el modelo respete las restricciones, colóquelas al final absoluto.",
        "tags": ["adk", "prompts", "constraints"]
    },
    {
        "scenario": "ADK Debugging: Circular Reasoning 🔌",
        "text": "To mitigate circular reasoning loops when tools return empty data, configure a {{c1::max_turns}} limit in the runner or implement Loop Detection in tool parameters.",
        "explanation": "If a tool returns empty data, the model might repeatedly call the same tool trying to find a result, causing an infinite loop.",
        "usage": "Rule: <code>Set max_turns in configuration; track tool call history to break identical consecutive calls.</code>",
        "spanish": "Para mitigar bucles de razonamiento circular cuando las herramientas devuelven datos vacíos, configure max_turns o implemente Loop Detection.",
        "tags": ["adk", "debugging", "loops"]
    }
]

# Ensure the parent directory exists
dir_path = "decks/02_AI_and_Data_Science/Agentic_Systems"
os.makedirs(dir_path, exist_ok=True)
file_path = f"{dir_path}/ADK_Mastery.json"

for card in adk_mastery_cards:
    card['deck'] = "02_AI_and_Data_Science::Agentic_Systems::ADK_Mastery"

with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(adk_mastery_cards, f, indent=2, ensure_ascii=False)

print(f"Successfully generated {len(adk_mastery_cards)} cards in {file_path}")
