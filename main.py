import streamlit as st
import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain_community.chat_models import ChatOpenAI


# Load environment variables
load_dotenv()
OPEN_AI_API_KEY = os.getenv("OPENAI_API_KEY")

# Upload PDF Files
st.header("Ask DOCS")

with st.sidebar:
    st.title("Your Documents")
    file = st.file_uploader("Upload your PDF file and ask questions.", type="pdf")


# Extract the text
if file is not None:
    pdf_reader = PdfReader(file)
    text = ""
    for page in pdf_reader.pages:
        text+=page.extract_text()
        # st.write(text)

    # Break into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        separators="\n",
        chunk_size = 1000,
        chunk_overlap = 150,
        length_function = len
    )

    chunks = text_splitter.split_text(text)

    # Generating Embeddings
    embeddings = OpenAIEmbeddings(openai_api_key = OPEN_AI_API_KEY)

    # # Creating vector store - FAISS
    vector_store = FAISS.from_texts(chunks, embeddings)

    # Get User Question
    user_question = st.text_input("Type your question here..")

    # Do similarity search 
    if user_question:
        match = vector_store.similarity_search(user_question)
        
        # define the LLM
        llm = ChatOpenAI(
            openai_api_key = OPEN_AI_API_KEY,
            temperature = 0,
            max_tokens = 1000,
            model_name = "gpt-4"
        )

        # Output Results
        chain = load_qa_chain(llm, chain_type="stuff")
        response = chain.run(input_documents = match, question=user_question)
        st.write(response)

# TODO: Change layout