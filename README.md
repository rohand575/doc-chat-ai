# Doc Chat AI

## Overview
Doc Chat AI is a Streamlit-based application that allows users to upload PDF documents and ask questions interactively. It leverages OpenAI embeddings and FAISS for similarity search and uses a language model to generate answers.

## Features
- Upload one or multiple PDF files (up to 5 at a time, 10MB each).
- Extract and process text from PDFs.
- Generate embeddings and build a vector store for similarity search.
- Ask questions about the documents using AI.
- Display chat history in latest-first order.
- Clear chat history with a button.
- Download chat history as a text file.
- Display document statistics (pages, words, chunks) in the sidebar.
- Minimalistic and professional UI.

## Requirements
- Python 3.10+
- Streamlit
- PyPDF2
- LangChain
- FAISS
- OpenAI Python SDK
- python-dotenv

## Installation
1. Clone the repository:
```bash
git clone <repo_url>
```
2. Navigate to the project directory:
```bash
cd doc-chat-ai
```
3. Create a virtual environment:
```bash
python -m venv venv
```
4. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- macOS/Linux: `source venv/bin/activate`
5. Install dependencies:
```bash
pip install -r requirements.txt
```
6. Create a `.env` file in the root directory with your OpenAI API key:
```bash
OPENAI_API_KEY=your_openai_api_key
```

## Usage
Run the application:
```bash
streamlit run main.py
```
- Upload PDFs via the sidebar.
- View document statistics.
- Ask questions in the main interface.
- Clear or download chat history as needed.

## Project Structure
```
doc-chat-ai/
│   main.py
│   README.md
│   requirements.txt
│   .env
```

## Versioning
- Current version: 1.2.0
- Changelog is maintained in `CHANGELOG.md`.

## License
This project is open-source and available under the MIT License.

