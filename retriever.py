import chromadb
from chromadb.utils import embedding_functions
from config import CHROMA_COLLECTION, CHROMA_PATH, EMBEDDING_MODEL, N_RESULTS

_ef = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name=EMBEDDING_MODEL
)
_client = chromadb.PersistentClient(path=CHROMA_PATH)
_collection = _client.get_or_create_collection(
    name=CHROMA_COLLECTION,
    embedding_function=_ef,
    metadata={"hnsw:space": "cosine"},
)


def get_collection():
    """Get the ChromaDB collection."""
    return _collection


def embed_and_store(chunks):
    """
    Embed chunks and store them in ChromaDB.

    Args:
        chunks: List of dicts with 'filename', 'chunk_index', and 'text' keys
    """
    ids = []
    documents = []
    metadatas = []

    for chunk in chunks:
        chunk_id = f"{chunk['filename']}_{chunk['chunk_index']}"
        ids.append(chunk_id)
        documents.append(chunk["text"])
        metadatas.append({
            "filename": chunk["filename"],
            "chunk_index": chunk["chunk_index"]
        })

    _collection.add(
        ids=ids,
        documents=documents,
        metadatas=metadatas
    )

    print(f"Stored {len(chunks)} chunks in ChromaDB collection '{CHROMA_COLLECTION}'")


def retrieve(query, n_results=N_RESULTS):
    """
    Retrieve top-k chunks most similar to the query.

    Args:
        query: Query text
        n_results: Number of results to retrieve (default: 5)

    Returns:
        List of dicts with 'text', 'metadata', and 'distance' keys
    """
    results = _collection.query(
        query_texts=[query],
        n_results=n_results
    )

    retrieved = []
    if results["documents"] and len(results["documents"]) > 0:
        for i, doc in enumerate(results["documents"][0]):
            retrieved.append({
                "text": doc,
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i]
            })
    
    for chunk in retrieved:
        print(f"[{chunk['metadata']}] (dist: {chunk['distance']:.3f}) {chunk['text'][:80]}...")

    return retrieved


if __name__ == "__main__":
    import os
    from ingest import load_documents, chunk_documents

    print("Testing RAG Pipeline\n")

    # Check if ChromaDB already exists
    if os.path.exists(CHROMA_PATH):
        print(f"Found existing ChromaDB at {CHROMA_PATH}. Skipping ingestion.\n")
    else:
        # Ingest and store documents
        print("Step 1: Ingesting and chunking documents...")
        documents = load_documents()
        chunks = chunk_documents(documents)

        print("\nStep 2: Embedding and storing in ChromaDB...")
        embed_and_store(chunks)

    # Test retrieval
    test_queries = [
        "What is the first course I must take as a CS student at UMD?",
        "What courses will help me with technical interviews?",
        "What upper level course can I take if I'm interested in networking and cloud computing?",
        "Who are the best professors to take for CS courses in general?",
        "What are the easiest 400-level classes to take?",
    ]

    print("\nStep 3: Testing retrieval...\n")
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Query: {query}")
        print('='*70)
        results = retrieve(query)
        if not results:
            print("No results found.")