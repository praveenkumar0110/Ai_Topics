from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_ollama import OllamaLLM

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = FAISS.load_local("mongo_index", embeddings, allow_dangerous_deserialization=True)

retriever = vectorstore.as_retriever(search_kwargs={"k":3})

llm = OllamaLLM(model="llama3")

while True:

    query = input("\nAsk your question: ")

    docs = retriever.invoke(query)

    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
You are a company HR assistant.

Rules:
- Answer ONLY what is asked in the question.
- Do NOT give extra details.
- Do NOT explain.
- Do NOT add project name, dates, priority unless asked.
- Return short direct answer.

Context:
{context}

Question:
{query}

Answer (only requested fields):
"""
    

    response = llm.invoke(prompt)

    print("\nAnswer:", response)