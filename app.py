import os
import gradio as gr
from ingest import load_documents, chunk_documents
from retriever import embed_and_store
from query import ask
from config import CHROMA_PATH


def initialize_db():
    """Initialize the vector database if it doesn't exist."""
    if not os.path.exists(CHROMA_PATH):
        print("Initializing vector database...")
        documents = load_documents()
        chunks = chunk_documents(documents)
        embed_and_store(chunks)
        print("Vector database ready!")


def handle_query(question):
    """Handle user query and return answer with sources."""
    answer, retrieved = ask(question)

    # Format sources
    if retrieved:
        sources_text = ""
        for chunk in retrieved:
            filename = chunk["metadata"]["filename"]
            distance = chunk["distance"]
            sources_text += f"• {filename} (relevance: {distance:.3f})\n"
    else:
        sources_text = "No sources retrieved."

    return answer, sources_text


# Initialize database on startup
initialize_db()

# Create Gradio interface
with gr.Blocks(title="UMD CS Guide Chatbot") as demo:
    gr.Markdown("""
    # UMD Computer Science Guide
    Ask questions about CS courses, requirements, and student experiences at UMD.
    """)

    with gr.Row():
        with gr.Column(scale=2):
            inp = gr.Textbox(label="Your question", placeholder="e.g., What courses help with technical interviews?")
            btn = gr.Button("Ask", variant="primary")
            answer = gr.Textbox(label="Answer", lines=8, interactive=False)

        with gr.Column(scale=1):
            sources = gr.Textbox(label="Retrieved Sources", lines=6, interactive=False)

    gr.Examples(
        examples=[
            "What is the first course I must take as a CS student at UMD?",
            "What courses will help me with technical interviews?",
            "What upper level course can I take if I'm interested in networking and cloud computing?",
        ],
        inputs=inp,
    )

    btn.click(handle_query, inputs=inp, outputs=[answer, sources])
    inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

    gr.Markdown("""
    ---
    **About this chatbot:** This is a Retrieval-Augmented Generation (RAG) system that retrieves information
    from course reviews, schedules, and student guides. All answers are sourced from the knowledge base.
    """)

demo.launch()