# 🧠 Phoenix AI Core

Una plataforma autónoma (ReAct Agent) diseñada para conectar tu Inteligencia Artificial local (DeepSeek, Qwen) directamente a tu sistema operativo.

## 📌 ¿Qué hace?
En lugar de ser un simple chat, Phoenix AI Core actúa como un ingeniero de software autónomo. Le pides una herramienta, la IA programa el script en Python, te pide permiso para ejecutarlo, y si el script falla, la IA lee el error de la terminal y se corrige a sí misma hasta que funcione.

## 🚀 Instalación y Uso

1. **Requisito Local:** Asegúrate de tener Ollama o LM Studio corriendo en tu PC. (Por defecto, el script busca la API en http://localhost:11434/api/chat).
2. **Dependencias:** Instala la librería de peticiones web:
   pip install requests
3. **Ejecución:**
   Abre una terminal en esta carpeta y ejecuta:
   python phoenix_agent.py
4. **Interacción:** Escribe lo que necesitas. Ejemplo: *"Crea un script que lea todos los archivos .txt de mi escritorio y los junte en uno solo"*.

## 🛡️ Seguridad (Human-in-the-Loop)
Los scripts generados por la IA **NUNCA** se ejecutan sin tu permiso. La plataforma los guarda en la carpeta 	ools/ y te pregunta [Y/n] antes de correrlos.

## 🔁 Auto-Sanación (Auto-Healing)
Si apruebas un script y este arroja un error en la consola (ej. falta una librería o hay un error de sintaxis), Phoenix AI Core atrapa ese error rojo y se lo envía automáticamente de vuelta a la IA diciéndole *"Falló por esto, arréglalo"*. La IA reescribirá el código y volverá a intentarlo hasta 3 veces.
