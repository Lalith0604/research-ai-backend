import os
import uuid
import ssl
from dotenv import load_dotenv


from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import  WebBaseLoader
from langchain_community.vectorstores import FAISS

ssl._create_default_https_context = ssl._create_unverified_context

load_dotenv()
os.environ["USER_AGENT"] = "research-ai-app"






# Folder to store vector DBs
VECTOR_DB_DIR = "vectorstores"
os.makedirs(VECTOR_DB_DIR, exist_ok=True)


def process_urls(urls):
    print("STEP 1: Loading URLs")

    loader = WebBaseLoader(urls)
    data = loader.load()

    print("STEP 2: Splitting")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    docs = splitter.split_documents(data)

    print("STEP 3: Embeddings")

    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2"
    )

    print("STEP 4: Vector store")

    vectorstore = FAISS.from_documents(docs, embeddings)

    print("STEP 5: Saving")

    index_id = str(uuid.uuid4())
    path = os.path.join(VECTOR_DB_DIR, index_id)
    vectorstore.save_local(path)

    return index_id