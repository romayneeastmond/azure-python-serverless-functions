import docx
import os
import PyPDF2

def get_file_content(file, type):
    content = ""

    if type == "PDF":
        reader = PyPDF2.PdfReader(file)
        
        pages_content = []

        for page_num in range(len(reader.pages)):
            extracted_text = reader.pages[page_num].extract_text()
            content += extracted_text
            pages_content.append(extracted_text.strip())

        return content, len(content.split()), len(reader.pages), pages_content
    elif type == "Word Document":
        my_doc = docx.Document(file)

        full_text = []

        for paragraph in my_doc.paragraphs:
            full_text.append(paragraph.text)

        content = '\n'.join(full_text)

        return content, len(content.split()), -1, []
    elif type in ["Text Document", "Markdown Document"]:
        content = file.read().decode("utf-8")

        return content, len(content.split()), -1, []
    else:
        return "Unknown document"

def get_file_extension(file_path):
    _, ext = os.path.splitext(file_path)
    ext = ext.lower()
    
    if ext == ".pdf":
        return "PDF"
    elif ext in [".doc", ".docx"]:
        return "Word Document"
    elif ext == ".txt":
        return "Text Document"
    elif ext in [".md", ".markdown"]:
        return "Markdown Document"
    else:
        return "Unknown"