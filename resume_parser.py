from pathlib import Path
import re


def extract_text(uploaded_file):
    """Extract text from PDF, DOCX, TXT or image. OCR is optional."""
    name = getattr(uploaded_file, "name", "upload").lower()
    raw = uploaded_file.getvalue() if hasattr(uploaded_file, "getvalue") else Path(uploaded_file).read_bytes()
    if name.endswith(".pdf"):
        import fitz
        doc = fitz.open(stream=raw, filetype="pdf")
        text = "\n".join(page.get_text("text") for page in doc).strip()
        if len(text) < 40:
            text = _ocr_pdf(raw)
        if not text.strip():
            raise ValueError("PDF मधून text मिळाला नाही. Scanned PDF साठी Tesseract OCR install करा.")
        return text
    if name.endswith(".docx"):
        from docx import Document
        import io
        doc = Document(io.BytesIO(raw))
        parts = [p.text for p in doc.paragraphs if p.text.strip()]
        for table in doc.tables:
            for row in table.rows:
                parts.append(" | ".join(c.text.strip() for c in row.cells))
        text = "\n".join(parts).strip()
        if not text: raise ValueError("DOCX मध्ये वाचण्यासारखा text आढळला नाही.")
        return text
    if name.endswith(".txt"):
        return raw.decode("utf-8", errors="replace")
    if name.endswith((".png", ".jpg", ".jpeg", ".tif", ".tiff", ".webp")):
        from PIL import Image
        import io
        import pytesseract
        from dotenv import load_dotenv
        import os
        load_dotenv()
        if os.getenv("TESSERACT_CMD"): pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
        return pytesseract.image_to_string(Image.open(io.BytesIO(raw))).strip()
    raise ValueError("Supported formats: PDF, DOCX, TXT, PNG, JPG, JPEG, TIFF, WEBP")


def _ocr_pdf(raw):
    try:
        import fitz, pytesseract, io, os
        from PIL import Image
        from dotenv import load_dotenv
        load_dotenv()
        if os.getenv("TESSERACT_CMD"): pytesseract.pytesseract.tesseract_cmd = os.getenv("TESSERACT_CMD")
        doc = fitz.open(stream=raw, filetype="pdf")
        pages=[]
        for page in doc:
            pix=page.get_pixmap(matrix=fitz.Matrix(1.5,1.5), alpha=False)
            img=Image.open(io.BytesIO(pix.tobytes("png")))
            pages.append(pytesseract.image_to_string(img))
        return "\n".join(pages).strip()
    except Exception:
        return ""


def normalize_text(text):
    text = text.replace("\x00", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def extract_sections(text):
    sections = {"skills": "", "experience": "", "education": "", "projects": "", "certifications": ""}
    lines=text.splitlines()
    current=None
    headers={"skills":"skills|technical skills|core competencies|technologies", "experience":"experience|work experience|employment|internship", "education":"education|academic background|qualifications", "projects":"projects|academic projects|personal projects", "certifications":"certifications|certificates|licenses"}
    for line in lines:
        stripped=line.strip()
        found=None
        for key, pattern in headers.items():
            if re.fullmatch(pattern, stripped.lower().strip(": ")):
                found=key; break
        if found: current=found; continue
        if current and stripped: sections[current] += stripped + "\n"
    return {k:v.strip() for k,v in sections.items()}
