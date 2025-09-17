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

# Custom CSS for professional look
st.markdown("""
    <style>
        body {background-color: #fafafa;}
        .stButton>button {
            border-radius: 8px;
            background-color: #2C3E50;
            color: white;
            padding: 8px 16px;
        }
        .stButton>button:hover {
            background-color: #34495E;
        }
        .chat-card {
            background-color:#f9f9f9;
            padding:15px;
            border-radius:10px;
            margin-bottom:10px;
            box-shadow: 1px 1px 4px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

st.header("📄 Chat with your PDFs")

# Initialize session state
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "pdf_processed" not in st.session_state:
    st.session_state.pdf_processed = False
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "doc_stats" not in st.session_state:
    st.session_state.doc_stats = {}

# Sidebar upload
with st.sidebar:
    st.title("Upload & Process PDFs")
    files = st.file_uploader("Upload PDF files", type="pdf", accept_multiple_files=True)
    process_btn = st.button("Process PDFs")
    clear_btn = st.button("Clear Chat")

# Reset state if no files
if not files:
    st.session_state.vector_store = None
    st.session_state.pdf_processed = False
    st.session_state.chat_history = []
    st.session_state.doc_stats = {}

# Clear chat manually
if clear_btn:
    st.session_state.chat_history = []
    st.rerun()

# Process PDFs
if process_btn and files:
    try:
        all_text = ""
        total_pages, total_words = 0, 0
        progress = st.progress(0)

        for idx, file in enumerate(files):
            pdf_reader = PdfReader(file)
            total_pages += len(pdf_reader.pages)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    all_text += page_text
                    total_words += len(page_text.split())
            progress.progress((idx + 1) / len(files))

        if not all_text.strip():
            st.error("❌ No extractable text found in uploaded PDFs. Try another file.")
        else:
            with st.spinner("Processing PDFs..."):
                # Split text
                text_splitter = RecursiveCharacterTextSplitter(
                    separators=["\n"],
                    chunk_size=1000,
                    chunk_overlap=150,
                    length_function=len
                )
                chunks = text_splitter.split_text(all_text)

                # Embeddings + vector store
                embeddings = OpenAIEmbeddings(openai_api_key=OPEN_AI_API_KEY)
                st.session_state.vector_store = FAISS.from_texts(chunks, embeddings)
                st.session_state.pdf_processed = True
                st.session_state.chat_history = []  # reset chat
                st.session_state.doc_stats = {
                    "pages": total_pages,
                    "words": total_words,
                    "chunks": len(chunks)
                }
                st.success("✅ PDFs processed successfully!")

    except Exception as e:
        st.error(f"⚠️ Error while processing PDFs: {e}")

# Document stats
if st.session_state.pdf_processed and st.session_state.doc_stats:
    stats = st.session_state.doc_stats
    st.sidebar.markdown("### 📊 Document Stats")
    st.sidebar.info(f"Pages: {stats.get('pages',0)} | Words: {stats.get('words',0)} | Chunks: {stats.get('chunks',0)}")

# Q&A
if st.session_state.pdf_processed and st.session_state.vector_store:
    user_question = st.text_input("💬 Ask a question about your PDFs:")

    if user_question:
        try:
            with st.spinner("Searching for answers..."):
                match = st.session_state.vector_store.similarity_search(user_question)

                llm = ChatOpenAI(
                    openai_api_key=OPEN_AI_API_KEY,
                    temperature=0,
                    max_tokens=1000,
                    model_name="gpt-4"
                )

                chain = load_qa_chain(llm, chain_type="stuff")
                response = chain.run(input_documents=match, question=user_question)

            # Save Q&A to simple dict history (not LangChain)
            st.session_state.chat_history.append({
                "question": user_question,
                "answer": response
            })

        except Exception as e:
            st.error(f"❌ Chat error: {e}")

# Display chat history (latest first)
if st.session_state.chat_history:
    st.subheader("📌 Chat History (Latest First)")
    for chat in reversed(st.session_state.chat_history):
        st.markdown(
            f"""
            <div class="chat-card">
            <p><strong>Q:</strong> {chat.get('question','')}</p>
            <p><strong>A:</strong> {chat.get('answer','')}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

# Download chat history
if st.session_state.chat_history:
    chat_text = "\n\n".join([f"Q: {c['question']}\nA: {c['answer']}" for c in st.session_state.chat_history])
    st.download_button(
        "⬇️ Download Chat History",
        chat_text,
        file_name="chat_history.txt",
        mime="text/plain"
    )
