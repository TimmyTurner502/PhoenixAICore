import os
import urllib.request
import base64
import json
import subprocess
import whisper
import warnings
warnings.filterwarnings("ignore")

# 1. PREPARACIÓN DE DIRECTORIOS Y DESCARGA DE MUESTRAS
print("[*] Inicializando Ecosistema Multimodal...")
os.makedirs("muestras", exist_ok=True)

audio_path = "muestras/audio_gerencia.wav"
image_path = "muestras/diagrama_complejo.jpg"

# Descargar un audio de prueba
if not os.path.exists(audio_path):
    print("[*] Descargando audio de prueba...")
    audio_url = "https://www2.cs.uic.edu/~i101/SoundFiles/StarWars3.wav"
    try:
        urllib.request.urlretrieve(audio_url, audio_path)
    except:
        pass

# Descargar una imagen difícil (diagrama arquitectónico)
if not os.path.exists(image_path):
    print("[*] Descargando imagen difícil (diagrama técnico)...")
    image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Microservices_Architecture.png/800px-Microservices_Architecture.png"
    try:
        urllib.request.urlretrieve(image_url, image_path)
    except:
        pass

print("[+] Archivos descargados en la carpeta 'muestras/'.")

# 2. PRUEBA DE AUDICIÓN (WHISPER)
print("\n==================================================")
print(" 🎧 PRUEBA DE AUDICIÓN (OPENAI WHISPER) ")
print("==================================================")
print(f"[*] Cargando modelo Whisper 'tiny' (consumo mínimo de RAM)...")
try:
    modelo_audio = whisper.load_model("tiny")
    print(f"[*] Escuchando el archivo: {audio_path}")
    resultado_audio = modelo_audio.transcribe(audio_path)
    texto_escuchado = resultado_audio["text"]
    print(f"\n[Texto extraído del Audio]:\n\"{texto_escuchado.strip()}\"")
except Exception as e:
    print(f"[!] Error al procesar audio: {e}")

# 3. PRUEBA DE VISIÓN (MOONDREAM)
print("\n==================================================")
print(" 👁️ PRUEBA DE VISIÓN (MOONDREAM 1.8B) ")
print("==================================================")
print(f"[*] Pasando imagen compleja ({image_path}) al nervio óptico de Moondream...")

def analizar_imagen_ollama(ruta_imagen, prompt="Describe detalladamente este diagrama. ¿Qué bloques o textos alcanzas a leer?"):
    with open(ruta_imagen, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    
    payload = {
        "model": "moondream",
        "prompt": prompt,
        "images": [img_base64],
        "stream": False
    }
    
    req = urllib.request.Request("http://localhost:11434/api/generate", data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"})
    try:
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode("utf-8"))
        return result.get("response", "Sin respuesta.")
    except Exception as e:
        return f"Error conectando a Ollama: {e}"

descripcion_imagen = analizar_imagen_ollama(image_path)
print(f"\n[Lo que ve la IA]:\n{descripcion_imagen}")

print("\n==================================================")
print("[+] Prueba Multimodal Finalizada con Éxito.")
