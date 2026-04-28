from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(title="RAG IPCC API")

# Charger le vector DB et configurer le retriever
embedding_fn = OllamaEmbeddings(model="nomic-embed-text:latest")
vectordb = Chroma(persist_directory=str(BASE_DIR / "vectordb"), embedding_function=embedding_fn)
retriever = vectordb.as_retriever(search_type="mmr", search_kwargs={"k": 5, "fetch_k": 12})

# LLM
llm = ChatOllama(model="llama3.2:1b", temperature=0.0, num_predict=300)

prompt = PromptTemplate.from_template(
    "You are an IPCC report assistant. Use only the context below, but be helpful: "
    "if the context gives partial evidence, answer with that evidence instead of saying you do not know. "
    "Say 'I do not know from the provided context' only when the context has no relevant information. "
    "Answer in the same language as the question.\n\n"
    "Context:\n{context}\n\nQuestion: {question}\nAnswer:"
)
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


qa = prompt | llm | StrOutputParser()

class QueryIn(BaseModel):
    question: str


@app.get("/")
def root():
    return {"message": "RAG IPCC API is running. POST /ask to query."}


@app.post("/ask")
def ask(q: QueryIn):
    docs = retriever.invoke(q.question)
    answer = qa.invoke({
        "context": format_docs(docs),
        "question": q.question
    })
    return {
        "answer": answer,
        "sources": [doc.metadata for doc in docs]
    }