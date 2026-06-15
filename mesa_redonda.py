from crewai import Agent, Task, Crew, Process
import sys
import os

# CrewAI usa LiteLLM por debajo. Le decimos que apunte al localhost de Ollama.
os.environ["OLLAMA_API_BASE"] = "http://localhost:11434"

print("[*] Conectando a Ollama local...")

# ==========================================
# DEFINICIÓN DE LOS AGENTES (LOS EXPERTOS)
# ==========================================
# Se usa el prefijo "ollama/" para que LiteLLM sepa qué motor usar.
architect = Agent(
    role='Arquitecto de Sistemas Senior',
    goal='Diseñar la arquitectura teórica paso a paso para sistemas complejos.',
    backstory='Eres un visionario de la tecnología. No te limitas por lo que es "posible". Piensas en arquitecturas innovadoras y seguras.',
    verbose=True,
    allow_delegation=False,
    llm='ollama/deepseek-r1:1.5b'
)

coder = Agent(
    role='Ingeniero de Software Élite',
    goal='Escribir código de producción impecable basado en las instrucciones del arquitecto.',
    backstory='Eres un experto mundial en Python y Java. Escribes código eficiente, seguro y bien comentado. Confías ciegamente en la teoría del arquitecto.',
    verbose=True,
    allow_delegation=False,
    llm='ollama/qwen2.5-coder:1.5b'
)

# ==========================================
# DEFINICIÓN DE LAS TAREAS (LA MESA REDONDA)
# ==========================================
print("\n[+] Definiendo la misión para el panel de expertos...")

# Tarea 1: Solo para DeepSeek
task1 = Task(
    description='Queremos crear un servidor web HTTP mínimo incrustado en una aplicación Android para servir archivos estáticos sin internet. Explica la arquitectura teórica de cómo lograr esto de la forma más ligera posible.',
    expected_output='Una explicación teórica y arquitectónica en español, detallando los pasos lógicos.',
    agent=architect
)

# Tarea 2: Solo para QwenCoder (Espera a que termine DeepSeek)
task2 = Task(
    description='Lee atentamente la explicación arquitectónica generada por el Arquitecto. Basado estrictamente en sus ideas, escribe el código inicial (puede ser Java o Kotlin) para levantar ese servidor web local.',
    expected_output='Bloque de código bien estructurado y comentado.',
    agent=coder
)

# ==========================================
# ORQUESTACIÓN (CREW)
# ==========================================
# CrewAI se encarga de que trabajen secuencialmente (Process.sequential)
crew = Crew(
    agents=[architect, coder],
    tasks=[task1, task2],
    process=Process.sequential,
    verbose=True
)

print("\n==================================================")
print(" 🏛️ INICIANDO LA MESA REDONDA DE PHOENIX AI CORE 🏛️ ")
print("==================================================\n")
print("Cediendo la palabra a DeepSeek R1 (El Arquitecto)...")

try:
    # kickkoff() inicia el debate y el paso de información automático
    result = crew.kickoff()
    
    print("\n==================================================")
    print("                 🎉 RESULTADO FINAL 🎉                ")
    print("==================================================")
    print(result)
    
except Exception as e:
    print(f"\n[-] La mesa redonda colapsó. Error: {e}")
    print("[!] Verifica que tus modelos de Ollama estén respondiendo y los nombres coincidan.")
