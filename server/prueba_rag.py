from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough

# Create embeddingsclear
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

db = Chroma(persist_directory="./vector_store",
            embedding_function=embeddings)

# Create retriever
retriever = db.as_retriever(
    search_type="similarity",
    search_kwargs= {"k": 5}
)

# Create Ollama language model - Gemma 2
local_llm = 'gemma2:2b'

llm = ChatOllama(model=local_llm, max_tokens=4096, temperature=0.3, num_predict=3500)

# Create prompt template
template = """<bos><start_of_turn>user
You are a kitchen helper. Search the context for recipes that contain some or all of the ingredients specified in the question. Extract the complete recipe without modifying anything and keep the original formatting for each section (Title, Ingredients, Preparation, Tips). Copy and paste everything exactly from the context, do not rephrase anything. Translate this to Spanish.
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
        user_question = input("Lista de ingredientes (o escribe 'salir' para salir): ")
        if user_question.lower() == 'salir':
            break
        answer = ask_question(user_question)
