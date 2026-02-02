import streamlit as st
import fitz
import json
import ollama
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

st.set_page_config(layout="wide")
st.title("🧠 Medical Report Chatbot")

embed_model = SentenceTransformer('all-MiniLM-L6-v2')

# ---------- Extract PDF ----------
def extract_text(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    return "\n".join(page.get_text() for page in doc)

# ---------- Paragraph chunk ----------
def chunk_text(text):
    paras = [p.strip() for p in text.split("\n\n") if len(p.strip()) > 80]
    return paras

# ---------- Build Vector DB ----------
def build_vector_db(chunks):
    texts = chunks
    embeddings = embed_model.encode(texts)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    return texts, index

# ---------- Semantic Search ----------
def retrieve_context(question):
    q_emb = embed_model.encode([question])
    D, I = st.session_state.index.search(np.array(q_emb), 5)
    return "\n\n".join([st.session_state.texts[i] for i in I[0]])

# ---------- Chat Answer ----------
def chat_answer(question, context, history):
    prompt = f"""
You are a medical report assistant.

Conversation so far:
{history}

Relevant report content:
{context}

Answer the user's question from the report.

Question: {question}
"""
    res = ollama.chat(
        model="llama3:8b",
        messages=[{"role": "user", "content": prompt}]
    )
    return res['message']['content']

# ---------- UI ----------
pdf = st.file_uploader("Upload Medical Report PDF", type=["pdf"])

if pdf and st.button("Process Report"):
    text = extract_text(pdf)
    chunks = chunk_text(text)

    texts, index = build_vector_db(chunks)

    st.session_state.texts = texts
    st.session_state.index = index
    st.session_state.chat_history = ""

    st.success("✅ Report Ready for Chat")

# ---------- Chat UI ----------
if "index" in st.session_state:
    st.subheader("Chat with the Medical Report")

    user_q = st.text_input("Ask your question")

    if st.button("Send"):
        context = retrieve_context(user_q)

        answer = chat_answer(
            user_q,
            context,
            st.session_state.chat_history
        )

        # store history
        st.session_state.chat_history += f"\nUser: {user_q}\nAssistant: {answer}\n"

        st.markdown("### 🧑 You")
        st.write(user_q)

        st.markdown("### 🤖 Assistant")
        st.write(answer)
