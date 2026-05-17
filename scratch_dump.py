import pdfplumber
import sys

def dump_lines(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        page = pdf.pages[0]
        text = page.extract_text(layout=True)
        for i, line in enumerate(text.split('\n')):
            print(f"{i:03d}: {line}")

if __name__ == "__main__":
    dump_lines(sys.argv[1])
