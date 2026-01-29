import os
import shutil
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_ollama import OllamaEmbeddings, OllamaLLM

DB_PATH = "faiss_resume_index"

embeddings = OllamaEmbeddings(model="nomic-embed-text")
llm = OllamaLLM(model="llama3")


def ingest_pdf(pdf_path):
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    chunks = splitter.split_documents(docs)

    for chunk in chunks:
        chunk.metadata["source"] = pdf_path

    return chunks



def create_vectorstore(chunks):
    # Remove old incompatible index automatically
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)

    vectordb = FAISS.from_documents(chunks, embeddings)
    vectordb.save_local(DB_PATH)



def query_resumes(question):
    if not os.path.exists(DB_PATH):
        return "❗ Please upload and index resumes first.", []

    vectordb = FAISS.load_local(
        DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
#FAISS → search engine aagudhu.
    retriever = vectordb.as_retriever(search_kwargs={"k": 5})
    docs = retriever.invoke(question)

    context = "\n\n".join([d.page_content for d in docs])
    sources = list(set([d.metadata["source"] for d in docs]))

    prompt = f"""
You are an HR assistant.

Using ONLY the resume data below, answer the question.

Resume Data:
{context}

Question:
{question}

Answer clearly and mention candidate strengths.
"""

    response = llm.invoke(prompt)

    return response, sources
