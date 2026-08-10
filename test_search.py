"""
SkillRadar - Phase 3, Semantic Search Test
Proves the vector store finds jobs by MEANING, not just exact keywords.
"""

import chromadb
from sentence_transformers import SentenceTransformer

CHROMA_PATH = "chroma_store"

embedder = SentenceTransformer("all-MiniLM-L6-v2")
client = chromadb.PersistentClient(path=CHROMA_PATH)
collection = client.get_or_create_collection("job_postings")


def search(query: str, n_results: int = 5):
    query_embedding = embedder.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )

    print(f"\nQuery: '{query}'\n")
    for i, (doc_id, metadata, distance) in enumerate(zip(
        results["ids"][0], results["metadatas"][0], results["distances"][0]
    )):
        print(f"{i+1}. {metadata['title']} @ {metadata['company']} (distance: {distance:.3f})")


if __name__ == "__main__":
    search("building AI agents with large language models")
    search("backend web development with databases")