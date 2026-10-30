from core.resume_parser import normalize_text, extract_sections

def test_normalize_text():
    assert normalize_text("Hello   world\n\n\nTest") == "Hello world\n\nTest"

def test_extract_sections():
    text="SKILLS\nPython, SQL\nEDUCATION\nBachelor of Engineering"
    sections=extract_sections(text)
    assert "Python" in sections["skills"]
    assert "Bachelor" in sections["education"]
