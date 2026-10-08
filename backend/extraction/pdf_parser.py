"""Page-aware PDF text extraction using PyMuPDF."""

import pymupdf


def parse_pdf(filepath: str) -> list[dict]:
    """Extract text from each page of a PDF, preserving page numbers.

    Returns:
        List of dicts with 'page' (1-indexed) and 'text' keys.
    """
    doc = pymupdf.open(filepath)
    pages = []
    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text().strip()
        if text:
            pages.append({"page": page_num + 1, "text": text})
    doc.close()
    return pages


def get_full_text(pages: list[dict]) -> str:
    """Combine all pages into a single text with page markers."""
    return "\n\n".join(f"[Page {p['page']}]\n{p['text']}" for p in pages)


def get_page_count(filepath: str) -> int:
    """Return the number of pages in a PDF."""
    doc = pymupdf.open(filepath)
    count = len(doc)
    doc.close()
    return count
