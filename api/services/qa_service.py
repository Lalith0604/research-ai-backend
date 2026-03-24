import os
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings

load_dotenv()

os.environ["USER_AGENT"] = "research-ai-app"

VECTOR_DB_DIR = "vectorstores"


def ask_question(question, index_id):
    # 1. Load embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    # 2. Load vector DB
    path = os.path.join(VECTOR_DB_DIR, index_id)

    if not os.path.exists(path):
        raise Exception("Invalid index_id")

    vectorstore = FAISS.load_local(
        path,
        embeddings,
        allow_dangerous_deserialization=True
    )

    # 3. Retrieve relevant docs
    docs = vectorstore.similarity_search(question, k=4)

    context = "\n\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("source", "") for doc in docs]

    # 4. LLM (Groq)
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0
    )

    prompt = f"""
    Answer the question based ONLY on the context below.

    Context:
    {context}

    Question:
    {question}
    """

    response = llm.invoke(prompt)

    return {
        "answer": response.content,
        "sources": sources
    }