import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings

df = pd.read_csv("./recetas.csv")

# Crear documentos de LangChain con metadatos separados para cada columna
documents = [
    Document(
        page_content=f"{row['Ingredientes']}",
        metadata={
            "Título": row['Título'],
            "Ingredientes": row['Ingredientes'],
            "Preparación": row['Preparación'],
            "Consejos": row['Consejos']
        }
    )
    for _, row in df.iterrows()
]

print(f"Cantidad de documentos cargados: {len(documents)}")

# Crear embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Dividir los documentos en fragmentos usando RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,
    chunk_overlap=200,
)

texts = text_splitter.split_documents(documents)

# Crear el almacén vectorial
vectorstore = Chroma.from_documents(
    documents=texts, 
    embedding=embeddings,
    persist_directory="./vector_store"
)

print("Vector store creado con éxito.")
