import os
import shutil
import gc
import time

# 1. DEFINIR CARPETAS DE TRABAJO (BATCH PROCESSING)
DIR_ENTRADA = "Bandeja_Entrada"
DIR_PROCESADOS = "Bandeja_Procesados"

os.makedirs(DIR_ENTRADA, exist_ok=True)
os.makedirs(DIR_PROCESADOS, exist_ok=True)

# 2. GENERAR ARCHIVOS FALSOS PARA LA PRUEBA (Si no hay nada)
archivos_en_entrada = os.listdir(DIR_ENTRADA)
if not archivos_en_entrada:
    print("[*] La Bandeja de Entrada está vacía. Generando 3 archivos de prueba...")
    for i in range(1, 4):
        with open(os.path.join(DIR_ENTRADA, f"documento_prueba_{i}.txt"), 'w') as f:
            f.write(f"Contenido del documento empresarial numero {i}")

def procesar_archivo_con_ia(ruta_archivo):
    """
    Aquí es donde tu modelo (DeepSeek, Qwen o Whisper) lee el archivo.
    Simularemos que la IA lo lee para no hacer una prueba de 20 minutos, 
    pero la arquitectura RAM está aplicada.
    """
    print(f"   [>] IA leyendo: {ruta_archivo}")
    # Simulación de carga pesada en RAM
    memoria_ficticia = [0] * (10 ** 7) # Simula consumo de RAM
    time.sleep(2)
    # Aquí iría: resultado = modelo.transcribe() o modelo.invoke()
    return "Procesado Correctamente."

# 3. EL BUCLE SECUENCIAL (EL SALVAVIDAS DE LA RAM)
archivos_a_procesar = os.listdir(DIR_ENTRADA)

if not archivos_a_procesar:
    print("[!] No hay archivos nuevos para procesar.")
else:
    print(f"\n==================================================")
    print(f" ⚙️ ORQUESTADOR SECUENCIAL INICIADO ")
    print(f" Archivos en cola: {len(archivos_a_procesar)}")
    print(f"==================================================\n")

    for nombre_archivo in archivos_a_procesar:
        ruta_origen = os.path.join(DIR_ENTRADA, nombre_archivo)
        ruta_destino = os.path.join(DIR_PROCESADOS, nombre_archivo)
        
        # PASO A: Procesar
        print(f"[*] Iniciando procesamiento de: {nombre_archivo}...")
        resultado = procesar_archivo_con_ia(ruta_origen)
        print(f"   [+] Resultado: {resultado}")
        
        # PASO B: Mover (Evita duplicidad y borrado accidental)
        print(f"   [>] Moviendo '{nombre_archivo}' a la Bandeja de Procesados para resguardo...")
        # Si el archivo ya existe en procesados, le añade un timestamp para no sobrescribir
        if os.path.exists(ruta_destino):
            nombre_sin_ext, ext = os.path.splitext(nombre_archivo)
            ruta_destino = os.path.join(DIR_PROCESADOS, f"{nombre_sin_ext}_{int(time.time())}{ext}")
            
        shutil.move(ruta_origen, ruta_destino)
        
        # PASO C: ¡LIMPIAR LA MEMORIA RAM! (CRÍTICO PARA LAPTOPS)
        print("   [!] Liberando Memoria RAM...")
        gc.collect() 
        print("   --------------------------------------------------\n")

    print("[+] Todos los archivos fueron procesados y guardados de forma segura en 'Bandeja_Procesados'.")
