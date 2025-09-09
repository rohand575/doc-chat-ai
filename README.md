# Doc Chat AI

[![Python](https://img.shields.io/badge/python-3.11-blue)](https://www.python.org/) 
[![Streamlit](https://img.shields.io/badge/streamlit-v1.30.0-orange)](https://streamlit.io/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

A Streamlit app to **upload PDFs and chat with them** using OpenAI GPT-4 and LangChain.  
Built with FAISS vector stores and OpenAI embeddings.  
Ideal for research, document analysis, and AI-powered PDF Q&A.

---

## Features (v1.0.0)
- Upload **one or multiple PDFs**
- Process PDFs into embeddings for semantic search
- Ask questions and get answers from your documents
- **Latest-first chat history**
- Clean, **card-style chat UI**
- Easy setup and local run

---

## Screenshots
<!-- Add screenshots of your app here -->
![Upload Screen](docs/screenshots/upload.png)
![Chat Interface](docs/screenshots/chat.png)

---

## Installation

1. **Clone the repo**
```bash
git clone https://github.com/yourusername/doc-chat-ai.git
cd doc-chat-ai
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Add your OpenAI API key**
- Copy `.env.example` to `.env` and add your key:
```env
OPENAI_API_KEY=your_openai_api_key_here
```

5. **Run the app**
```bash
streamlit run main.py
```

---

## Usage
1. Upload PDFs in the sidebar (single or multiple files).  
2. Click **Process PDFs**.  
3. Type your questions in the chat box.  
4. Chat history is displayed **latest-first**, and clears when files are removed.  

---

## Project Structure
```
doc-chat-ai/
│
├─ main.py                  # Streamlit app
├─ requirements.txt         # Python dependencies
├─ README.md                # Project instructions
├─ .gitignore               # Files to ignore in git
├─ .env.example             # Template for API keys
├─ LICENSE                  # MIT License
├─ VERSION                  # Project version file
├─ data/                    # Optional: sample PDFs
└─ docs/                    # Screenshots or diagrams
```

---

## Version
**v1.0.0** – Initial release with core PDF chat functionality

---

## Future Improvements
- v1.1.0: Local embeddings for free usage (no API key required)  
- v1.2.0: Download chat as PDF or TXT  
- v1.3.0: Highlight relevant text from PDFs in answers  
- v2.0.0: Multi-version release with major UI/UX improvements  

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## References
- [Streamlit Documentation](https://docs.streamlit.io/)  
- [LangChain Documentation](https://python.langchain.com/en/latest/)  
- [FAISS Documentation](https://faiss.ai/)  
