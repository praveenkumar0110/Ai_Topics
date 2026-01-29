from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from transformers import pipeline


loader = TextLoader("data/About_Ai.txt")
docs = loader.load()


splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)
chunks = splitter.split_documents(docs)


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

db = FAISS.from_documents(chunks, embeddings)
retriever = db.as_retriever()


pipe = pipeline(
    "text2text-generation",
    model="google/flan-t5-base",
    max_new_tokens=200
)
'''

Question → embedding aagudhu (vector number list)

FAISS la already irukura resume chunk vectors oda compare pannudhu

Most similar 4–5 chunks eduthudhu
'''
# mainnn stepss
def rag_chain(question):
    docs = retriever.invoke(question)
    context = "\n\n".join([d.page_content for d in docs])

    prompt = f"""
Answer ONLY from the context.

Context:
{context}

Question: {question}
Answer:
"""

    result = pipe(prompt)[0]["generated_text"]
    return result.strip()



print(rag_chain("Who is the author of this text?"))
print(rag_chain("What is the short form of Praveen Kumar?"))
