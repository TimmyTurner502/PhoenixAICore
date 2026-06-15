# 🧠 Phoenix AI Core: Guía Maestra del Ecosistema (Post-Formateo)

Esta guía documenta la arquitectura definitiva de tu ecosistema de Inteligencia Artificial Local (Multi-Agente + Memoria a Largo Plazo). Úsala para reconstruir tu plataforma después de formatear tu PC.

## 🏛️ La Santísima Trinidad de tu Entorno
1.  **AegisLegacy:** Escudo y ofuscación (Intercepción JS/Kotlin).
2.  **Phoenix V3 (AndroidDecompilator):** Análisis de seguridad, reconstrucción y escaneo.
3.  **Phoenix AI Core (Este repositorio):** El Cerebro. El orquestador que toma decisiones, escribe código y recuerda tu progreso.

---

## 🛠️ 1. Reconstruyendo el "Segundo Cerebro" (Memoria a Largo Plazo)
Para que la IA recuerde todos tus proyectos, reglas y herramientas, usaremos **Obsidian** con capacidades RAG (Retrieval-Augmented Generation).

### Pasos de Instalación:
1.  Descarga e instala [Obsidian](https://obsidian.md/).
2.  Crea una "Bóveda" (Vault) llamada PhoenixKnowledgeBase. Aquí guardarás todos tus .md, ideas, scripts y comandos de Aegis.
3.  Ve a Configuración de Obsidian > **Community Plugins** > Desactiva el Modo Seguro.
4.  Busca e instala el plugin **Smart Connections** (o *Local LLM Hub*).
5.  **Conexión:** En la configuración del plugin, selecciona Ollama como proveedor e ingresa la URL local: http://localhost:11434.
6.  **Resultado:** Ahora puedes abrir el chat lateral en Obsidian. La IA leerá automáticamente todos tus archivos y te responderá teniendo en cuenta todo lo que han construido juntos.

---

## 👥 2. La Mesa Redonda (Panel de Expertos)
En este repositorio tienes el script mesa_redonda.py, construido con **CrewAI**. Este script permite que DeepSeek (Arquitecto) y QwenCoder (Ingeniero) debatan y trabajen secuencialmente.

### Dependencias:
`ash
pip install crewai
`

### Configuración de Modelos (¡Muy Importante!):
Asegúrate de que los nombres de los modelos en el script coincidan exactamente con los que tienes descargados.
Para saber tus nombres exactos, abre una terminal y escribe:
`ash
ollama list
`
Verás algo como deepseek-r1:7b o qwen2.5-coder:7b.
Abre mesa_redonda.py y actualiza estas dos líneas con tus nombres exactos:
`python
llm='ollama/tu-modelo-exacto-deepseek'
llm='ollama/tu-modelo-exacto-qwen'
`

### Ejecución:
`ash
python mesa_redonda.py
`
El script iniciará el debate: DeepSeek diseñará la arquitectura y Qwen escribirá el código.

---

## 🌐 3. Módulo Oráculo (Conexión a Internet)
Si quieres que tu panel de expertos pueda buscar en internet (para superar su fecha de entrenamiento), CrewAI lo hace increíblemente fácil.
1. Instala las herramientas de CrewAI:
   pip install crewai-tools
2. En tu script mesa_redonda.py, añade esto al principio:
   `python
   from crewai_tools import SerperDevTool
   search_tool = SerperDevTool()
   `
3. Asígnalo a tu agente:
   `python
   architect = Agent(
       ...,
       tools=[search_tool]
   )
   `
Ahora, si DeepSeek no sabe algo, automáticamente buscará en Google antes de responderte.

---
*Fin de la guía. Bienvenido al siguiente nivel de la Ingeniería de Software Autónoma.*
