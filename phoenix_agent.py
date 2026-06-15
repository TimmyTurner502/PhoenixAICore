import os
import json
import subprocess
import re
import requests

# Configuracion (Apunta a Ollama o LM Studio)
API_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "deepseek-r1:latest" # Cambia esto a tu modelo local

# Carpeta permanente de herramientas
TOOLS_DIR = "tools"
os.makedirs(TOOLS_DIR, exist_ok=True)

SYSTEM_PROMPT = """
Eres Phoenix AI Core, un agente autónomo de ingeniería de software experto en Python.
Tu trabajo es escribir scripts para resolver los problemas del usuario.
Reglas:
1. Solo devuelve código Python dentro de bloques ```python ... ```
2. Escribe código modular, limpio y bien comentado.
3. Si el script requiere librerías externas, menciónalas en los comentarios iniciales.
"""

def query_local_ai(messages):
    """Se comunica con la IA local (Ej: Ollama)"""
    payload = {
        "model": MODEL_NAME,
        "messages": messages,
        "stream": False
    }
    try:
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()
        return response.json()["message"]["content"]
    except Exception as e:
        print(f"\n[!] Error conectando a la IA local en {API_URL}: {e}")
        print("[!] Asegúrate de que Ollama o LM Studio estén corriendo.")
        return None

def extract_python_code(text):
    """Extrae el código Python del formato markdown"""
    match = re.search(r'```python\n(.*?)\n```', text, re.DOTALL)
    if match:
        return match.group(1)
    return None

def execute_script(filepath):
    """Ejecuta el script y captura la salida o los errores"""
    try:
        result = subprocess.run(["python", filepath], capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)

def agent_loop():
    print("==================================================")
    print("        🧠 PHOENIX AI CORE INICIALIZADO 🧠        ")
    print("==================================================")
    print(f"Modelo Objetivo: {MODEL_NAME} | Servidor: {API_URL}")
    print("Escribe 'salir' para terminar.\n")

    conversation = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        user_input = input("\n[Tú]: ")
        if user_input.lower() in ['salir', 'exit', 'quit']:
            break

        conversation.append({"role": "user", "content": user_input})
        
        print("[*] Pensando...")
        ai_response = query_local_ai(conversation)
        
        if not ai_response:
            continue
            
        conversation.append({"role": "assistant", "content": ai_response})
        
        code = extract_python_code(ai_response)
        
        if code:
            print("\n[+] La IA ha generado una herramienta. El código es el siguiente:")
            print("-" * 40)
            print(code)
            print("-" * 40)
            
            tool_name = input("\n[?] Nombra esta herramienta para guardarla (ej. 'ordenar_archivos.py') o presiona ENTER para omitir: ").strip()
            
            if tool_name:
                if not tool_name.endswith('.py'):
                    tool_name += '.py'
                
                filepath = os.path.join(TOOLS_DIR, tool_name)
                
                # Guardar permanentemente
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(code)
                print(f"[+] Herramienta guardada permanentemente en: {filepath}")
                
                run_choice = input("[?] ¿Deseas ejecutar esta herramienta ahora? [Y/n]: ").lower()
                if run_choice in ['', 'y', 'yes']:
                    max_retries = 3
                    retries = 0
                    
                    while retries < max_retries:
                        print(f"\n[*] Ejecutando {tool_name}...")
                        success, output = execute_script(filepath)
                        
                        if success:
                            print(f"[+] ¡ÉXITO! Salida de la herramienta:\n{output}")
                            conversation.append({"role": "user", "content": f"El script funcionó perfectamente. Salida: {output}"})
                            break
                        else:
                            print(f"[-] ERROR en la ejecución:\n{output}")
                            print(f"[*] Re-alimentando el error a la IA (Intento {retries+1}/{max_retries})...")
                            
                            error_prompt = f"El script que escribiste falló al ejecutarse. Aquí está el error:\n{output}\nPor favor, reescribe el código para solucionar este problema."
                            conversation.append({"role": "user", "content": error_prompt})
                            
                            ai_fix = query_local_ai(conversation)
                            if ai_fix:
                                conversation.append({"role": "assistant", "content": ai_fix})
                                new_code = extract_python_code(ai_fix)
                                if new_code:
                                    # Sobrescribir con la versión corregida
                                    with open(filepath, 'w', encoding='utf-8') as f:
                                        f.write(new_code)
                                    print("[+] La IA ha corregido y guardado el script. Reintentando...")
                                    retries += 1
                                else:
                                    print("[-] La IA no devolvió código corregido.")
                                    break
                            else:
                                break
                    
                    if retries == max_retries:
                        print("[-] La IA no pudo arreglar el script después de 3 intentos.")
        else:
            print(f"\n[Phoenix]: {ai_response}")

if __name__ == "__main__":
    agent_loop()
