import warnings
import logging
import time
import pdfplumber
from config import DOCS_PATH

warnings.filterwarnings("ignore", message=".*FontBBox.*")
logging.getLogger("pdfminer").setLevel(logging.ERROR)

PDF_FILES = [
    "CMSC131 _ PlanetTerp.pdf",
    "CMSC132 _ PlanetTerp.pdf",
    "CMSC216 _ PlanetTerp.pdf",
    "CMSC250 _ PlanetTerp.pdf",
    "CMSC330 _ PlanetTerp.pdf",
    "CMSC351 _ PlanetTerp.pdf",
    "Schedule of Classes - CMSC1XX.pdf",
    "Schedule of Classes - CMSC2XX.pdf",
    "Schedule of Classes - CMSC3XX.pdf",
    "Schedule of Classes - CMSC4XX.pdf",
]
TEXT_FILES = [
    "reddit_guide.txt",
]

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 250


def load_documents():
    """Load and extract text from all documents (PDFs and text files)."""
    documents = []
    start_time = time.time()

    print("Loading documents...")

    # Load PDF files
    for i, filename in enumerate(PDF_FILES, 1):
        filepath = DOCS_PATH + '/' + filename
        try:
            file_start = time.time()
            with pdfplumber.open(filepath) as pdf:
                text = "\n\n".join(
                    page.extract_text()
                    for page in pdf.pages
                    if page.extract_text()
                )
                if text.strip():
                    documents.append({
                        "filename": filename,
                        "text": text
                    })
            elapsed = time.time() - file_start
            print(f"  [{i}/{len(PDF_FILES)}] {filename} ({elapsed:.2f}s, {len(text)} chars)")
        except Exception as e:
            print(f"  Error loading {filename}: {e}")

    # Load text files
    for i, filename in enumerate(TEXT_FILES, 1):
        filepath = DOCS_PATH + '/' + filename
        try:
            file_start = time.time()
            with open(filepath, "r", encoding="utf-8") as f:
                text = f.read()
                if text.strip():
                    documents.append({
                        "filename": filename,
                        "text": text
                    })
            elapsed = time.time() - file_start
            print(f"  [TXT {i}] {filename} ({elapsed:.2f}s, {len(text)} chars)")
        except Exception as e:
            print(f"  Error loading {filename}: {e}")

    total_time = time.time() - start_time
    print(f"Loaded {len(documents)} documents in {total_time:.2f}s\n")
    return documents


def chunk_documents(documents):
    """
    Split documents into overlapping chunks.

    Args:
        documents: List of dicts with 'filename' and 'text' keys

    Returns:
        List of dicts with 'filename', 'chunk_index', and 'text' keys
    """
    chunks = []
    step_size = CHUNK_SIZE - CHUNK_OVERLAP
    start_time = time.time()

    print("Chunking documents...")

    for doc in documents:
        text = doc["text"]
        chunk_index = 0
        doc_chunks = 0

        # Create chunks with overlap
        for start in range(0, len(text), step_size):
            end = start + CHUNK_SIZE
            chunk_text = text[start:end]

            if chunk_text.strip():
                chunks.append({
                    "filename": doc["filename"],
                    "chunk_index": chunk_index,
                    "text": chunk_text
                })
                chunk_index += 1
                doc_chunks += 1

            # Stop if we've reached the end of the document
            if end >= len(text):
                break

        print(f"  {doc['filename']}: {doc_chunks} chunks")

    total_time = time.time() - start_time
    print(f"Created {len(chunks)} total chunks in {total_time:.2f}s\n")
    return chunks


if __name__ == "__main__":
    total_start = time.time()

    documents = load_documents()
    chunks = chunk_documents(documents)

    # Print first chunk as example
    if chunks:
        print("First chunk example:")
        print(f"  Filename: {chunks[0]['filename']}")
        print(f"  Chunk index: {chunks[0]['chunk_index']}")
        print(f"  Text (first 500 chars): {chunks[0]['text'][:500]}...\n")

    total_time = time.time() - total_start
    print(f"Total pipeline time: {total_time:.2f}s")
