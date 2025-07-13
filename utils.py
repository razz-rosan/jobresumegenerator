import os
from PyPDF2 import PdfReader
import docx

def extract_text_from_file(file):
    ext = os.path.splitext(file.name)[1].lower()
    
    if ext == ".pdf":
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text
    
    elif ext == ".docx":
        doc = docx.Document(file)
        return "\n".join([para.text for para in doc.paragraphs])
    
    elif ext == ".txt":
        return file.read().decode("utf-8")

    else:
        raise ValueError("Unsupported file type. Please upload PDF, DOCX, or TXT.")
