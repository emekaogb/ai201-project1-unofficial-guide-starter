from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)

DISTANCE_THRESHOLD = 0.5


def generate(query, retrieved_chunks):
    """
    Generate a response using retrieved chunks as context.

    Args:
        query: User query string
        retrieved_chunks: List of dicts with 'text', 'metadata', and 'distance' keys

    Returns:
        Generated response string
    """
    # Filter chunks by distance threshold
    relevant_chunks = [
        chunk for chunk in retrieved_chunks
        if chunk["distance"] <= DISTANCE_THRESHOLD
    ]

    # If no relevant chunks, return fallback
    if not relevant_chunks:
        return "I don't have any information on this topic."

    # Format context with filename and distance scores
    context_parts = []
    for i, chunk in enumerate(relevant_chunks, 1):
        metadata = chunk["metadata"]
        distance = chunk["distance"]
        text = chunk["text"]

        context_parts.append(
            f"[Source {i}: {metadata['filename']} | Distance: {distance:.3f}]\n{text}"
        )

    context = "\n\n---\n\n".join(context_parts)

    # Create system prompt
    system_prompt = """You are a helpful assistant for CS students at the University of Maryland.
Answer questions ONLY based on the retrieved context provided below.
If the context doesn't contain information to answer the question, respond with: "I don't have any information on this."

IMPORTANT: Always cite your sources in the answer. When you reference information, include the source filename in parentheses like this:
"According to [description from the context] (source: [filename]), [answer]"

Be concise and direct in your answers."""

    # Create user message
    user_message = f"""Context:
{context}

Question: {query}

Answer based only on the context above. Remember to cite sources in the format: (source: filename)"""

    # Call Groq API
    message = _client.chat.completions.create(
        model=LLM_MODEL,
        max_tokens=1024,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
    )

    return message.choices[0].message.content


if __name__ == "__main__":
    import os
    from ingest import load_documents, chunk_documents
    from retriever import embed_and_store, retrieve
    from config import CHROMA_PATH

    print("Testing Full RAG Pipeline\n")

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

    # Test queries from planning.md
    test_queries = [
        "What is the first course I must take as a CS student at UMD?",
        "What courses will help me with technical interviews?",
        "What upper level course can I take if I'm interested in networking and cloud computing?",
        "Who are the best professors to take for CS courses in general?",
        "What are the easiest 400-level classes to take?",
    ]

    print("\nStep 3: Testing end-to-end retrieval and generation...\n")
    for query in test_queries:
        print(f"\n{'='*70}")
        print(f"Question: {query}")
        print('='*70)

        # Retrieve
        retrieved = retrieve(query)

        # Generate
        if retrieved:
            response = generate(query, retrieved)
            print(f"\nAnswer: {response}")
        else:
            print("No relevant information found.")