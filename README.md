# PDF Chatbot with LangChain & OpenAI

## Overview
This is an interactive **PDF Chatbot** built using **Streamlit, LangChain, and FAISS**. 
It allows users to upload a PDF File, processs its contents into embeddings, and then ask natural language questions about the doucment. The system uses **OpenAI's GPT Model** to generate accurate, context-aware response.


## Features
- Upload and PDF file and query its contents.
- Uses ** Lanchain's text splitting + embeddings**.
- Vector similarity search with **FAISS**
- Streamlit web interface for easy interaction
- Configurable OpenAI model ( GPT-4 )

## Tech Stack
- **Python 3.13.7**
- [StreamLit](https://streamlit.io/) – Web interface
- [LangChain](https://www.langchain.com/) – LLM framework
- [OpenAI API](https://platform.openai.com/) – LLM models
- [FAISS](https://github.com/facebookresearch/faiss) – Vector database
- [PyPDF2](https://pypi.org/project/pypdf2/) – PDF text extraction