import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.schema import Document

def load_csv(filepath):
    df = pd.read_csv(filepath)
    documents = [
        Document(
            page_content=f"""
            Ingrediente Individuales:
            {row['Ingrediente Individuales']}
            """,
            metadata={
                "Título": row['Título'],
                "Ingredientes": row['Ingredientes'],
                "Preparación": row['Preparación'],
                "Consejos": row['Consejos'],
                "Ingrediente Individuales": row['Ingrediente Individuales']
            }
        )
        for _, row in df.iterrows()
    ]
    print(f"Cantidad de documentos cargados: {len(documents)}")
    return documents

def create_vector_store(documents, model_name="nomic-embed-text", persist_directory="./vector_store"):
    embeddings = OllamaEmbeddings(model=model_name, show_progress=True)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=4000, chunk_overlap=0)
    texts = text_splitter.split_documents(documents)
    vectorstore = Chroma.from_documents(texts, embedding=embeddings, persist_directory=persist_directory)
    print("Vector store creado con éxito.")
    return vectorstore

documents = load_csv("./recetas.csv")
vectorstore = create_vector_store(documents)