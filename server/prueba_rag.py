from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama

from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

# Create embeddingsclear
embeddings = OllamaEmbeddings(model="nomic-embed-text", show_progress=False)

db = Chroma(persist_directory="./vector_store",
            embedding_function=embeddings)

# Create retriever
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs= {"k": 3}
)

# Create Ollama language model - Gemma 2
local_llm = 'gemma2:2b'

llm = ChatOllama(model=local_llm,
                keep_alive="3h",
                max_tokens=4096,
                temperature=0)

# Create prompt template
template = """<bos><start_of_turn>user\nBusca en el contexto la receta que contenga los ingredientes especificados en la pregunta. Extrae la receta completa sin modificar nada y mantén el formato original para cada sección (Título, Ingredientes, Preparación, Consejos). Copia y pega exactamente todo lo del contexto, no reformules nada. Responde en español.

CONTEXTO: {context}

INGREDIENTES SOLICITADOS: {question}

<end_of_turn>
<start_of_turn>model\n
RECETA:"""
prompt = ChatPromptTemplate.from_template(template)

# Create the RAG chain using LCEL with prompt printing and streaming output
rag_chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
)

# Function to ask questions
def ask_question(question):
    print("Respuesta:\n\n", end=" ", flush=True)
    for chunk in rag_chain.stream(question):
        print(chunk.content, end="", flush=True)
    print("\n")

# Example usage
if __name__ == "__main__":
    while True:
        user_question = input("Haz una pregunta (o escribe 'salir' para salir): ")
        if user_question.lower() == 'salir':
            break
        answer = ask_question(user_question)
        # print("\nFull answer received.\n")