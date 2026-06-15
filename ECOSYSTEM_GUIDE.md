# 🦅 Phoenix AI Core: Guía Maestra del Ecosistema (Versión Final)

Esta es la documentación definitiva que debes leer tras formatear tu PC para levantar tu imperio de Inteligencia Artificial en local desde cero. No necesitas internet para operar, solo para la instalación inicial.

---

## FASE 1: El Motor Cerebral (Ollama)
Ollama es el motor que ejecuta las IAs en tu computadora sin depender de la nube.
1. **Descargar Ollama:** Ve a [ollama.com](https://ollama.com) e instálalo.
2. **Descargar tus Modelos Específicos:** Abre PowerShell y ejecuta los siguientes comandos uno por uno. Estos son los modelos hiper-optimizados que tu hardware (Intel i5, 8GB RAM) puede soportar sin congelarse:
   * ollama pull deepseek-r1:1.5b *(Para razonamiento matemático y arquitectura).*
   * ollama pull qwen2.5-coder:1.5b *(Para escribir código puro).*
   * ollama pull moondream *(Para procesar imágenes y leer documentos visuales).*
   * ollama pull nomic-embed-text *(Para la base de datos de memoria vectorial).*

---

## FASE 2: Segundo Cerebro Personal (Obsidian + IA)
Para tener un "Segundo Cerebro" personal donde la IA converse contigo sobre tus notas:

1. **Descargar Obsidian:** [obsidian.md](https://obsidian.md)
2. **El Secreto del CORS (IMPORTANTE):** Windows bloquea que Obsidian hable con Ollama por seguridad. Para arreglarlo, debes abrir tus variables de entorno en Windows y crear una nueva llamada OLLAMA_ORIGINS con el valor pp://obsidian.md*. Reinicia tu PC tras hacer esto.
3. **Instalar el Plugin 'Smart Connections':**
   * En Obsidian, ve a Configuración > Plugins de la comunidad > Desactiva el "Modo Seguro".
   * Busca e instala **"Smart Connections"**.
   * En su configuración, elige "Ollama" como proveedor y http://localhost:11434 como URL.
   * Selecciona 
omic-embed-text para los embeddings y tu qwen2.5-coder:1.5b para el chat.
4. **Tutorial Recomendado en YouTube:** Si tienes dudas visuales, busca en YouTube: *"How to setup Smart Connections Obsidian Ollama local RAG"*.

---

## FASE 3: Ecosistema Empresarial Autónomo (CrewAI + Multimodal)
Si quieres ir más allá de Obsidian y vender esto a empresas, o crear tus propias apps, usarás los scripts en Python que creamos en este repositorio.

### Instalación de Librerías Base
Abre tu terminal en la carpeta del proyecto y ejecuta:
`ash
pip install crewai langchain langchain-community chromadb openai-whisper pypdf sentence-transformers duckduckgo-search
`

### Arquitectura de los Scripts
* **mesa_redonda.py**: El cerebro estratégico. Conecta a DeepSeek y Qwen en una sala de chat para debatir ideas o escribir código de manera autónoma.
* **memoria_multiformato.py**: El motor RAG. Lee PDFs, Excels (CSV) y TXT, los convierte en matemáticas (ChromaDB) y le da las respuestas precisas a tu IA sin alucinar.
* **prueba_multimodal.py**: El procesador audiovisual. Escucha audios .wav/.mp3 usando **OpenAI Whisper**, y lee diagramas o facturas .jpg usando **Moondream**, para luego pasárselos a la Mesa Redonda.

### Recomendaciones de Software Extra
* Instala **FFmpeg** en Windows (necesario para que Whisper procese los audios). Descárgalo de [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) y agrégalo a tu variable PATH.

---
*Fin de la Documentación. Formatea tranquilo. El Fénix renacerá de sus cenizas en cuanto corras estos comandos.*
