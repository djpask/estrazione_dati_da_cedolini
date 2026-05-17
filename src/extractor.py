import pdfplumber
import re
import os

def estrai_dati(file_path):
    """
    Estrae i dati da un singolo cedolino in formato PDF.
    
    Args:
        file_path (str): Il percorso del file del cedolino (PDF nativo).
        
    Returns:
        dict: I dati estratti organizzati in un dizionario.
    """
    dati = {
        "File": os.path.basename(file_path),
        "Mese_Retribuito": None,
        "Nome_Dipendente": None,
        "Codice_Fiscale": None,
        "Matricola": None,
        "Data_Assunzione": None,
        "Livello": None,
        "Qualifica": None,
        "Paga_Base": None,
        "Totale_Lordo": None,
        "Totale_Trattenute": None,
        "Netto_Busta": None,
        "IBAN": None
    }
    
    try:
        with pdfplumber.open(file_path) as pdf:
            if not pdf.pages:
                return dati
                
            page = pdf.pages[0]
            # Usa layout=True per preservare gli spazi orizzontali in modo che 
            # possiamo affidarci all'incolonnamento visuale.
            text = page.extract_text(layout=True)
            
            if not text:
                print(f"Attenzione: Nessun testo estratto da {file_path}. Il PDF potrebbe essere una scansione (immagine).")
                return dati
                
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                # 1. Ricerca del Mese Retribuito
                # Spesso è nella riga con "FEBBRAIO        2026"
                if not dati["Mese_Retribuito"]:
                    match_mese = re.search(r"(GENNAIO|FEBBRAIO|MARZO|APRILE|MAGGIO|GIUGNO|LUGLIO|AGOSTO|SETTEMBRE|OTTOBRE|NOVEMBRE|DICEMBRE)\s+(\d{4})", line, re.IGNORECASE)
                    if match_mese:
                        dati["Mese_Retribuito"] = f"{match_mese.group(1).upper()} {match_mese.group(2)}"

                # 2. Matricola e Nome Dipendente
                # Formato tipico riga: "FEBBRAIO 2026 1 1 7042040915 10776098 1116 DI GENNARO PASQUALE 01/09/09"
                # o vicinanze. Cerchiamo la matricola come un numero lungo 10 cifre
                if not dati["Matricola"]:
                    match_mat = re.search(r"1\s+([0-9]{10})\s+[0-9]{8}", line)
                    if match_mat:
                        dati["Matricola"] = match_mat.group(1)
                
                # Cerchiamo il nome "DI GENNARO PASQUALE" tra la matricola/codici e la data
                if not dati["Nome_Dipendente"]:
                    match_nome = re.search(r"\d{4}\s+([A-Z\s\']+?)\s+\d{2}/\d{2}/\d{2}", line)
                    if match_nome:
                        dati["Nome_Dipendente"] = match_nome.group(1).strip()
                
                # 3. Data Assunzione
                if not dati["Data_Assunzione"]:
                    match_ass = re.search(r"(\d{2}/\d{2}/\d{2})$", line.strip())
                    if match_ass: # Rafforziamo per evitare falsi positivi
                        # controlliamo che la riga contenga parole (probabilmente il nome)
                        if re.search(r"[A-Z]{3,}", line):
                            dati["Data_Assunzione"] = match_ass.group(1)

                # 4. Codice Fiscale
                if not dati["Codice_Fiscale"]:
                    match_cf = re.search(r"\b([A-Z]{6}\d{2}[A-Z]\d{2}[A-Z]\d{3}[A-Z])\b", line)
                    if match_cf:
                        dati["Codice_Fiscale"] = match_cf.group(1)
                        
                # 5. Paga Base, Qualifica e Livello
                # Riga tipica: "        12.903,50 40 Funzionario                                7          5                         49         50                            162,50 26"
                if not dati["Qualifica"] and "Funzionario" in line:
                    match_qual = re.search(r"([\d\.]+,\d{2})\s+\d+\s+([A-Za-z]+)", line)
                    if match_qual:
                        dati["Paga_Base"] = match_qual.group(1)
                        dati["Qualifica"] = match_qual.group(2)
                    
                    # Cerca il livello (di solito verso la fine, es. 50)
                    match_liv = re.search(r"\s+(\d{2})\s+[\d\.]+\s+\d+$", line.strip())
                    if match_liv:
                        dati["Livello"] = match_liv.group(1)
                        
                # 6. Totale Lordo
                if "TOTALE LORDO" in line:
                    # Di solito i valori si trovano 1 o 2 righe sotto
                    for j in range(1, 3):
                        if i+j < len(lines):
                            match_lordo = re.search(r"([\d\.]+,\d{2})", lines[i+j])
                            if match_lordo:
                                dati["Totale_Lordo"] = match_lordo.group(1)
                                break
                                
                # 7. Totale Trattenute
                if "TOTALE TRATTENUTE" in line:
                    for j in range(1, 3):
                        if i+j < len(lines):
                            match_tratt = re.search(r"([\d\.]+,\d{2})\s*$", lines[i+j])
                            if match_tratt:
                                dati["Totale_Trattenute"] = match_tratt.group(1)
                                break
                                
                # 8. Netto Busta
                if "NETTO BUSTA" in line:
                    for j in range(1, 4):
                        if i+j < len(lines):
                            match_netto = re.search(r"([\d\.]+,\d{2})\s*$", lines[i+j])
                            if match_netto:
                                dati["Netto_Busta"] = match_netto.group(1)
                                break
                                
                # 9. IBAN
                if not dati["IBAN"]:
                    match_iban = re.search(r"(IT\d{2}[A-Z]\d{22})", line)
                    if match_iban:
                        dati["IBAN"] = match_iban.group(1)

    except Exception as e:
        print(f"Errore durante l'elaborazione del file {file_path}: {e}")
        
    return dati
