import os
import csv
from langchain_community.document_loaders import CSVLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import warnings
warnings.filterwarnings("ignore")

# 1. GENERACIÓN DE ARCHIVOS DE PRUEBA EMPRESARIALES
print("[*] Generando archivos de la empresa (CSV y TXT)...")
os.makedirs("datos_empresa", exist_ok=True)

# Archivo 1: CSV de Ventas
csv_path = "datos_empresa/ventas_trimestre.csv"
with open(csv_path, 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["ID_Empleado", "Nombre", "Departamento", "Ventas_Totales_USD", "Bono_Autorizado"])
    writer.writerow(["EMP001", "Roberto Gomez", "Ventas Corporativas", "45000", "Sí"])
    writer.writerow(["EMP002", "Lucia Fernandez", "Retail", "12000", "No"])
    writer.writerow(["EMP003", "Sistema Automatizado X-9", "Digital", "890000", "Sí"])

# Archivo 2: Documento de Políticas (TXT simulando un PDF/DOC extraído)
txt_path = "datos_empresa/politica_bonos.txt"
with open(txt_path, 'w', encoding='utf-8') as f:
    f.write("""MEMORÁNDUM INTERNO - RECURSOS HUMANOS
Fecha: Junio 2026
Asunto: Política de Bonos de Desempeño.

Se establece que cualquier empleado o sistema que supere los 50,000 USD en ventas trimestrales recibirá un bono del 10% sobre sus ventas. 
Excepción crítica: El 'Sistema Automatizado X-9' no recibe el bono en efectivo, sino que sus fondos se destinan a mantenimiento de servidores. Lucia Fernandez está en plan de mejora.""")

# 2. LECTURA Y PARSEO DE DOCUMENTOS (LOADERS)
print("[*] Leyendo y parseando documentos...")
docs = []
docs.extend(CSVLoader(csv_path).load())
docs.extend(TextLoader(txt_path, encoding='utf-8').load())

# 3. DIVISIÓN EN TROZOS (CHUNKING)
print("[*] Troceando información para la base de datos vectorial...")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
splits = text_splitter.split_documents(docs)

# 4. INGESTA EN CHROMADB (EMBEDDINGS LOCALES)
print("[*] Inicializando motor de Embeddings (all-MiniLM-L6-v2) y ChromaDB...")
# Usamos un modelo de HuggingFace muy ligero y rápido que corre 100% en local sin internet
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = Chroma.from_documents(
    documents=splits, 
    embedding=embeddings, 
    persist_directory="./chroma_db_empresarial"
)

# 5. CREACIÓN DEL RECUPERADOR (RETRIEVER)
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# 6. CONEXIÓN AL LLM LOCAL (OLLAMA)
print("[*] Conectando a Ollama (qwen2.5-coder:1.5b)...")
# Usamos el modelo que tienes instalado localmente
llm = Ollama(model="qwen2.5-coder:1.5b")

# 7. DEFINICIÓN DEL PROMPT DE RAG (INSTRUCCIONES ESTRICTAS)
template = """Usa EXCLUSIVAMENTE los siguientes fragmentos de contexto recuperados de los documentos de la empresa para responder a la pregunta. 
Si no sabes la respuesta o no está en los documentos, di "No tengo información en los documentos de la empresa para responder esto", no inventes nada.

Contexto de la empresa:
{context}

Pregunta del gerente: {question}

Respuesta profesional:"""
custom_rag_prompt = PromptTemplate.from_template(template)

# Función auxiliar para unir los documentos recuperados
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

# 8. CONSTRUCCIÓN DE LA CADENA RAG (PIPELINE)
rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | custom_rag_prompt
    | llm
    | StrOutputParser()
)

# 9. PRUEBA DE FUEGO (CONSULTA)
print("\n==================================================")
print(" 🏢 SISTEMA DE MEMORIA EMPRESARIAL INICIADO 🏢 ")
print("==================================================\n")

pregunta = "¿Cuánto vendió el Sistema Automatizado X-9 y qué pasa con su bono autorizado según la política?"
print(f"[Gerente]: {pregunta}")
print("\n[Buscando en ChromaDB y procesando con IA Local...]")

respuesta = rag_chain.invoke(pregunta)

print(f"\n[IA de la Empresa]:\n{respuesta}")
print("\n==================================================")
print("[+] Prueba Finalizada con Éxito.")
