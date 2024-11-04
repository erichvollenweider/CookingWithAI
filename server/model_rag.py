# model_setup.py
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

def load_model():
    # Cargar embeddings si necesitas usarlos en `Chroma`
    embeddings = OllamaEmbeddings(model="nomic-embed-text", show_progress=True)

    # Cargar el vector store desde el directorio persistente
    vectorstore = Chroma(persist_directory="./vector_store", embedding_function=embeddings)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": 3})

    # Configurar el modelo de lenguaje y el prompt
    llm = ChatOllama(model='gemma2:2b', keep_alive="3h", max_tokens=4096, temperature=0)
    template = """<bos><start_of_turn>user\nBusca en el contexto la receta que contenga los ingredientes especificados en la pregunta. Extrae la receta completa sin modificar nada y mantén el formato original para cada sección (Título, Ingredientes, Preparación, Consejos). Copia y pega exactamente todo lo del contexto, no reformules nada. Responde en español.

    CONTEXTO: {context}

    INGREDIENTES SOLICITADOS: {question}

    <end_of_turn>
    <start_of_turn>model\n
    RECETA:"""

    prompt = ChatPromptTemplate.from_template(template)
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
    )

    return rag_chain, retriever
