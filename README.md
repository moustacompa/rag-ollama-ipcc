# RAG Ollama IPCC

A local Retrieval-Augmented Generation (RAG) application for asking questions about IPCC report PDFs. The project uses FastAPI for the backend, Streamlit for the user interface, Chroma as the vector database, and Ollama for local embeddings and chat generation.

## Author

- Name: COMPAORE Moustapha
- Email: compaore.moustapha@ine.inpt.ac.ma

## Features

- Extracts text from PDF files in the `data/` folder.
- Splits PDF text into reusable chunks saved in `chunks/`.
- Builds a persistent Chroma vector database in `vectordb/`.
- Uses `nomic-embed-text:latest` for embeddings through Ollama.
- Uses `llama3.2:1b` for local question answering through Ollama.
- Provides a FastAPI `/ask` endpoint.
- Provides a Streamlit interface for interactive questions.

## Project Structure

```text
rag-ollama-ipcc/
+-- app.py              # FastAPI backend
+-- ui_streamlit.py     # Streamlit frontend
+-- ingest.py           # PDF extraction and chunk generation
+-- embeddings.py       # Embedding generation and Chroma persistence
+-- requirements.txt    # Python dependencies
+-- data/               # Source PDF files
+-- chunks/             # Generated JSON chunks
+-- vectordb/           # Generated Chroma vector database
```

## Requirements

- Python 3.11+
- Ollama installed and running
- The following Ollama models:

```powershell
ollama pull nomic-embed-text:latest
ollama pull llama3.2:1b
```

If `ollama` is not available in your PATH on Windows, use:

```powershell
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull nomic-embed-text:latest
& "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe" pull llama3.2:1b
```

## Installation

From the project folder:

```powershell
cd "F:\INPT\INE2\S4\P2\DeepLearning\rag-ollama-ipcc"
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

If you already use the shared environment at `F:\INPT\python-venv\deeplearning`, activate or call that Python directly instead.

## Data Preparation

Place your PDF files inside the `data/` folder.

Then generate chunks:

```powershell
python ingest.py
```

This creates JSON chunk files inside `chunks/`.

## Build the Vector Database

After generating chunks, create the Chroma database:

```powershell
python embeddings.py
```

This creates or updates the `vectordb/` folder.

If you changed the PDFs or ingestion logic, it is recommended to clear or rename the old `chunks/` and `vectordb/` folders before regenerating.

## Run the Backend

```powershell
python -m uvicorn app:app --reload --port 8000
```

The API will be available at:

```text
http://127.0.0.1:8000
```

### API Endpoint

`POST /ask`

Example request:

```json
{
  "question": "What are the main causes of climate change?"
}
```

Example response:

```json
{
  "answer": "...",
  "sources": [
    {
      "source": "data/example.pdf",
      "page": 1,
      "chunk": 0
    }
  ]
}
```

## Run the Streamlit UI

In a separate terminal:

```powershell
streamlit run ui_streamlit.py
```

The UI sends questions to the FastAPI backend at `http://localhost:8000/ask`.

## Troubleshooting

### `model not found`

If Ollama says a model is missing, pull it first:

```powershell
ollama pull llama3.2:1b
ollama pull nomic-embed-text:latest
```

### Too many `I do not know` answers

Try the following:

- Regenerate `chunks/` and `vectordb/` after changing PDFs.
- Ask questions that are likely covered by the loaded IPCC documents.
- Increase retriever `k` in `app.py` if more context is needed.
- Use a stronger chat model if your machine can run it.

### Streamlit timeout

If responses are slow, use a smaller model, reduce retrieved context, or increase the Streamlit request timeout in `ui_streamlit.py`.

## License

This project is intended for educational use.