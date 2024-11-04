import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

df = pd.read_csv("./recetas.csv")

# Creamos una lista de documentos de Langchain a partir del contenido de la columna
documents = [
    Document(page_content=f"{row['Título']}\n\n{row['Ingredientes']}\n\n{row['Preparación']}\n\n{row['Consejos']}")
    for _, row in df.iterrows()
]

print(f"Cantidad de documentos cargados: {len(documents)}")

# Crear embeddings
embeddings = OllamaEmbeddings(model="nomic-embed-text", show_progress=True)

# Dividir los documentos en fragmentos usando RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3500,
    chunk_overlap=0,
)

texts = text_splitter.split_documents(documents)

# Crear el almacén vectorial
vectorstore = Chroma.from_documents(
    documents=texts, 
    embedding=embeddings,
    persist_directory="./vector_store"
)

print("Vector store creado con éxito.")
