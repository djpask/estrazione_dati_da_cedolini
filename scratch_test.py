import pdfplumber
import sys

def test_extract(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text(layout=True)
        print("--- EXTRACTED TEXT ---")
        print(text)
        print("----------------------")

if __name__ == "__main__":
    test_extract(sys.argv[1])
