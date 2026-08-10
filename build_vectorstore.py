"""
SkillRadar - Phase 3, Vector Store
Embeds job postings (title + description) and stores them in ChromaDB
for semantic similarity search - the retrieval half of RAG.
"""

import sqlite3
import chromadb
from sentence_transformers import SentenceTransformer

DB_PATH = "skillradar.db"
CHROMA_PATH = "chroma_store"

# A small, fast, free local embedding model - runs entirely on your CPU
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def load_jobs_from_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT id, title, company, description FROM jobs")
    rows = cursor.fetchall()
    conn.close()
    return rows


def build_vectorstore():
    jobs = load_jobs_from_db()
    print(f"Loaded {len(jobs)} jobs from database")

    client = chromadb.PersistentClient(path=CHROMA_PATH)
    collection = client.get_or_create_collection("job_postings")

    ids = []
    documents = []
    metadatas = []

    for job in jobs:
        text = f"{job['title']}. {job['description'] or ''}"
        ids.append(str(job["id"]))
        documents.append(text)
        metadatas.append({"title": job["title"], "company": job["company"] or ""})

    print("Generating embeddings (this may take a minute on CPU)...")
    embeddings = embedder.encode(documents, show_progress_bar=True).tolist()

    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=documents,
        metadatas=metadatas,
    )

    print(f"Stored {len(ids)} job embeddings in {CHROMA_PATH}")


if __name__ == "__main__":
    build_vectorstore()