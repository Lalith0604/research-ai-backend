import os
import uuid
import requests
from bs4 import BeautifulSoup

from langchain_community.embeddings import FakeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS

VECTOR_DB_DIR = "vectorstores"
os.makedirs(VECTOR_DB_DIR, exist_ok=True)


def fetch_text(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        return soup.get_text()
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""


def process_urls(urls):
    print("STEP 1: Fetching URLs")

    texts = [fetch_text(url) for url in urls]
    combined_text = "\n\n".join(texts)

    print("STEP 2: Splitting")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    docs = splitter.create_documents([combined_text])

    print("STEP 3: Embeddings")

    embeddings = FakeEmbeddings(size=384)

    print("STEP 4: Vector store")

    vectorstore = FAISS.from_documents(docs, embeddings)

    print("STEP 5: Saving")

    index_id = str(uuid.uuid4())
    path = os.path.join(VECTOR_DB_DIR, index_id)
    vectorstore.save_local(path)

    return index_id