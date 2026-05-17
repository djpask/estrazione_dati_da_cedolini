import pdfplumber
import os

def check_structure():
    input_dir = "data/input"
    for filename in sorted(os.listdir(input_dir)):
        if filename.endswith(".pdf"):
            print(f"--- {filename} ---")
            with pdfplumber.open(os.path.join(input_dir, filename)) as pdf:
                page = pdf.pages[0]
                text = page.extract_text(layout=True)
                lines = text.split('\n')
                for i, line in enumerate(lines):
                    if "IRPEF LORDA" in line or "NETTO BUSTA" in line or "TFR MESE" in line:
                        for j in range(i-1, i+4):
                            if 0 <= j < len(lines):
                                print(f"{j:03d}: {lines[j]}")
                        print("...")
                        
if __name__ == "__main__":
    check_structure()
