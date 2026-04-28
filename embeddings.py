# embeddings.py — contenu complet

from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import json, os


def embed_and_store(
    chunks_dir="chunks",
    persist_directory="vectordb",
    embedding_model="nomic-embed-text:latest"
):
    """Produit les embeddings de tous les chunks et les persiste dans Chroma."""
    embedder = OllamaEmbeddings(model=embedding_model)
    documents = []

    for fn in os.listdir(chunks_dir):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(chunks_dir, fn), "r", encoding="utf8") as f:
            items = json.load(f)
        for it in items:
            documents.append(
                Document(
                    page_content=it["page_content"],
                    metadata=it.get("metadata", {})
                )
            )

    print(f"Nombre total de documents à encoder : {len(documents)}")
    vectordb = Chroma.from_documents(
        documents,
        embedding=embedder,
        persist_directory=persist_directory
    )
    print(f"✅ Vector DB persisté dans '{persist_directory}'")
    return vectordb


# Lancer la création des embeddings
vectordb = embed_and_store()


# Test rapide : recherche par similarité
test_query = "What are the main causes of climate change?"
results = vectordb.similarity_search(test_query, k=2)

print(f"Résultats pour : '{test_query}'\n")
for i, doc in enumerate(results):
    print(f"--- Résultat {i+1} ---")
    print(doc.page_content[:300])
    print(f"Métadonnées : {doc.metadata}\n")