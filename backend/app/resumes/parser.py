import io
import pdfplumber
import docx
import re
from typing import List

def parse_pdf(file_bytes: bytes) -> str:
    text = ""
    try:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error parsing PDF: {e}")
    return text

def parse_docx(file_bytes: bytes) -> str:
    text = ""
    try:
        doc = docx.Document(io.BytesIO(file_bytes))
        for para in doc.paragraphs:
            text += para.text + "\n"
    except Exception as e:
        print(f"Error parsing DOCX: {e}")
    return text

def extract_skills_from_text(text: str) -> List[str]:
    """
    Very basic skill extraction based on a hardcoded list for v1.
    """
    text_lower = text.lower()
    # Simple list of common skills for MVP
    common_skills = [
        "python", "java", "javascript", "react", "node.js", "c++",
        "sql", "machine learning", "data science", "fastapi", "django",
        "docker", "kubernetes", "aws", "azure", "gcp", "git", "linux",
        "html", "css", "typescript", "postgres", "mongodb"
    ]
    
    extracted = []
    for skill in common_skills:
        # Simple word boundary regex
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            extracted.append(skill)
            
    return extracted
