import os
import csv
from extractor import estrai_dati

def main():
    print("Inizio programma di estrazione dati dai cedolini...")
    
    # Definizione delle cartelle di input e output
    base_dir = os.path.dirname(os.path.dirname(__file__))
    input_dir = os.path.join(base_dir, "data", "input")
    output_dir = os.path.join(base_dir, "data", "output")
    
    # Assicurati che le cartelle esistano
    os.makedirs(input_dir, exist_ok=True)
    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Cerco i file PDF in: {input_dir}")
    
    tutti_i_dati = []
    
    # Scorre tutti i file nella cartella di input
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            file_path = os.path.join(input_dir, filename)
            print(f"Elaborazione in corso: {filename} ...")
            
            dati = estrai_dati(file_path)
            tutti_i_dati.append(dati)
            
    if tutti_i_dati:
        print(f"\nEstrazione completata per {len(tutti_i_dati)} file.")
        
        csv_path = os.path.join(output_dir, "risultati_cedolini.csv")
        
        # Estrarre i nomi delle colonne dalle chiavi del primo dizionario
        fieldnames = list(tutti_i_dati[0].keys())
        
        with open(csv_path, mode='w', newline='', encoding='utf-8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames, delimiter=';')
            writer.writeheader()
            for row in tutti_i_dati:
                writer.writerow(row)
                
        print(f"\nDati salvati in: {csv_path}")
        
        # Stampa riepilogativa a schermo
        print("\nRiepilogo Dati Estratti:")
        header_str = " | ".join(fieldnames)
        print("-" * len(header_str))
        print(header_str)
        print("-" * len(header_str))
        for row in tutti_i_dati:
             row_str = " | ".join(str(row.get(col, '')) for col in fieldnames)
             print(row_str)
            
    else:
        print("Nessun file PDF trovato nella cartella data/input/.")

    print("\nElaborazione completata con successo.")

if __name__ == "__main__":
    main()
