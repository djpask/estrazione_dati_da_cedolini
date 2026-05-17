import os
from extractor import estrai_dati

def main():
    print("Inizio programma di estrazione dati dai cedolini...")
    
    # Definizione delle cartelle di input e output
    input_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "input")
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "output")
    
    # Assicurati che le cartelle esistano
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    # TODO: Logica per scorrere i file in input_dir e processarli con estrai_dati()
    print(f"Cartella input: {input_dir}")
    
    print("Elaborazione completata.")

if __name__ == "__main__":
    main()
