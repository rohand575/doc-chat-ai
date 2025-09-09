import os
from dotenv import load_dotenv
import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI

# Load environment variables
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

# Streamlit page config
st.set_page_config(page_title="Doc Chat AI", page_icon="📄", layout="wide")
st.header("📄 Chat with your PDFs")

# Initialize session state variables
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Sidebar: PDF upload
with st.sidebar:
    st.title("Upload & Process PDFs")
    files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    process_btn = st.button("Process PDFs")

# Reset everything if no file is uploaded
if not files:
    st.session_state.vector_store = None
    st.session_state.pdf_processed = False
    st.session_state.chat_history = []

# Process PDFs when button clicked
if process_btn and files:
    try:
        all_text = ""
        for file in files:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text

        if not all_text.strip():
            st.error("❌ No extractable text found in uploaded PDFs. Try another file.")
        else:
            with st.spinner("Processing PDFs..."):
                # Split text into chunks
                text_splitter = RecursiveCharacterTextSplitter(
                    separators=["\n"],
                    chunk_size=1000,
                    chunk_overlap=150,
                    length_function=len
                )
                chunks = text_splitter.split_text(all_text)

                # Generate embeddings
                embeddings = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)
                st.session_state.vector_store = FAISS.from_texts(chunks, embeddings)
                st.session_state.pdf_processed = True
                st.session_state.chat_history = []  # Clear chat history on new processing
                st.success("✅ PDFs processed successfully! Now ask your questions below.")

    except Exception as e:
        st.error(f"⚠️ Error while processing PDFs: {e}")

# Question input and answering
if st.session_state.pdf_processed and st.session_state.vector_store:
    user_question = st.text_input("💬 Ask a question about your PDFs:")

    if user_question:
        try:
            with st.spinner("Searching for answers..."):
                # Similarity search
                match = st.session_state.vector_store.similarity_search(user_question)

                # LLM
                llm = ChatOpenAI(
                    openai_api_key=OPEN_AI_API_KEY,
                    temperature=0,
                    max_tokens=1000,
                    model_name="gpt-4"
                )

                # QA chain
                chain = load_qa_chain(llm, chain_type="stuff")
                response = chain.run(input_documents=match, question=user_question)

            # Store in chat history (no source)
            st.session_state.chat_history.append({
                "question": user_question,
                "answer": response
            })

        except Exception as e:
            st.error(f"⚠️ Error while answering your question: {e}")

# Display chat history (latest first) in card-style
if st.session_state.chat_history:
    st.subheader("📌 Chat History (Latest First)")
    for chat in reversed(st.session_state.chat_history):
        st.markdown(
            f"""
            <div style="
                background-color:#f0f2f6;
                padding:15px;
                border-radius:10px;
                margin-bottom:10px;
                box-shadow: 2px 2px 5px rgba(0,0,0,0.1);
            ">
            <p><strong>Q:</strong> {chat.get('question', '')}</p>
            <p><strong>A:</strong> {chat.get('answer', '')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

