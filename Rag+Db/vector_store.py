from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from rag_mongo import load_mongo_docs

def create_vector():

    docs = load_mongo_docs()

    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    vectorstore = FAISS.from_documents(docs, embeddings)

    vectorstore.save_local("mongo_index")

    print("✅ Vector DB Created")

if __name__ == "__main__":
    create_vector()