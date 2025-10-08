# app/extract.py

import spacy
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

# Load small English NLP model
nlp = spacy.load("en_core_web_sm")

def extract_keywords(text):
    """
    Extracts meaningful keywords and phrases from resume text.
    Focuses on skills, tools, and relevant nouns or noun phrases.
    """
    doc = nlp(text)
    keywords = set()

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip()
        # Keep meaningful multi-word phrases
        if len(phrase.split()) > 1 and not phrase.islower():
            keywords.add(phrase)

    for token in doc:
        # Capture proper nouns or important nouns (e.g., "Python", "AWS", "Manager")
        if token.pos_ in {"PROPN", "NOUN"} and not token.is_stop and len(token.text) > 2:
            keywords.add(token.text.strip())

    # Clean and sort for consistency
    cleaned_keywords = sorted(list(set(kw for kw in keywords if kw.isalpha() or " " in kw)))
    return cleaned_keywords


def extract_text_from_pdf(file_path):
    """
    Safely extracts text from a PDF file.
    Returns extracted text or an error message.
    """
    try:
        text = extract_text(file_path)
        return text.strip() if text else "No readable text found in PDF."
    except (PDFSyntaxError, Exception) as e:
        return f"Error extracting text from PDF: {e}"
