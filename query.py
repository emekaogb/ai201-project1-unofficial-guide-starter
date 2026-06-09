"""Query module that combines retrieval and generation."""
from retriever import retrieve
from generator import generate


def ask(question):
    """
    Ask a question and get an answer with sources.

    Args:
        question: User query string

    Returns:
        tuple of (answer, retrieved_chunks)
    """
    retrieved = retrieve(question)
    answer = generate(question, retrieved)
    return answer, retrieved
