from docx import Document

def load_style_guide(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])
