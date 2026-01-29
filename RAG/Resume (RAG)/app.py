import streamlit as st
import os
from rag import ingest_pdf, create_vectorstore, query_resumes

st.set_page_config(page_title="PDF Chatbot using RAG", layout="wide")

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

st.title("RAG (Resume Screening)")
st.write("Upload resumes and ask questions like an HR.")

uploaded_files = st.file_uploader(
    "Upload Resume PDFs",
    type="pdf",
    accept_multiple_files=True
)


if uploaded_files:
    if st.button("Index Resumes"):
        all_chunks = []

        with st.spinner("Processing and indexing resumes..."):
            for file in uploaded_files:
                file_path = os.path.join(TEMP_DIR, file.name)

                with open(file_path, "wb") as f:
                    f.write(file.getbuffer())

                chunks = ingest_pdf(file_path)
                all_chunks.extend(chunks)

            create_vectorstore(all_chunks)

        st.success("Resumes indexed successfully!")

st.divider()


st.subheader("🔎 Ask about candidates")
question = st.text_input("Ask about candidates")
   
if st.button("Search"):
    answer, sources = query_resumes(question)

    st.markdown("### 🤖 Answer")
    st.write(answer)

    if sources:
        st.markdown("### 📄 Matching Resumes")
        for src in sources:
            st.write("-", os.path.basename(src))
