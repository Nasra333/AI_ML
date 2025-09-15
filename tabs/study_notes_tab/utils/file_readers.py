"""
File reading utilities for study notes tab.
Supports multiple document formats: TXT, MD, PDF, DOCX.
"""
import os
from PyPDF2 import PdfReader
from docx import Document


def read_uploaded_file(file_path: str) -> str:
    """
    Read content from uploaded file supporting multiple formats.

    Args:
        file_path: Path to the uploaded file

    Returns:
        Extracted text content from the file
    """
    if not file_path:
        return ""

    try:
        # Get file extension
        _, ext = os.path.splitext(file_path.lower())

        if ext == '.pdf':
            return _read_pdf_file(file_path)
        elif ext == '.docx':
            return _read_docx_file(file_path)
        else:
            return _read_text_file(file_path)

    except Exception as e:
        return f"Error reading file: {str(e)}"


def _read_pdf_file(file_path: str) -> str:
    """Read PDF file and extract text from all pages."""
    reader = PdfReader(file_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text.strip()


def _read_docx_file(file_path: str) -> str:
    """Read DOCX file and extract text from all paragraphs."""
    doc = Document(file_path)
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text.strip()


def _read_text_file(file_path: str) -> str:
    """Read plain text files (.txt, .md, etc.)."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()


def get_supported_file_types() -> list[str]:
    """
    Get list of supported file extensions.

    Returns:
        List of supported file extensions
    """
    return [".txt", ".md", ".pdf", ".docx"]