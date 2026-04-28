import glob
import json
import os

from PyPDF2 import PdfReader


def split_text(text, chunk_size=1000, chunk_overlap=200):
    chunks = []
    start = 0
    text = " ".join(text.split())

    while start < len(text):
        end = start + chunk_size
        chunks.append(text[start:end])
        if end >= len(text):
            break
        start = end - chunk_overlap

    return chunks


def load_and_split(pdf_path, chunk_size=1000, chunk_overlap=200):
    """Charge un PDF et le decoupe en chunks sans dependances LangChain lourdes."""
    reader = PdfReader(pdf_path)
    docs = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""
        for chunk_index, chunk in enumerate(split_text(text, chunk_size, chunk_overlap)):
            if chunk.strip():
                docs.append({
                    "page_content": chunk,
                    "metadata": {
                        "source": pdf_path,
                        "page": page_number,
                        "chunk": chunk_index,
                    },
                })

    return docs


def ingest_all(data_dir="data", chunks_dir="chunks", chunk_size=1000, chunk_overlap=200):
    """Traite tous les PDFs du dossier data/ et sauvegarde les chunks en JSON."""
    os.makedirs(chunks_dir, exist_ok=True)

    for pdf_path in glob.glob(os.path.join(data_dir, "*.pdf")):
        print(f"Traitement de {pdf_path}...")
        docs = load_and_split(pdf_path, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        output_path = os.path.join(chunks_dir, os.path.basename(pdf_path) + ".json")

        with open(output_path, "w", encoding="utf8") as f:
            json.dump(docs, f, ensure_ascii=False)

        print(f"  OK: {len(docs)} chunks sauvegardes dans {output_path}")


if __name__ == "__main__":
    ingest_all()
    print("\nIngestion terminee !")