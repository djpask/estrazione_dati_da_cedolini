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
        "Premio_Risultato": None,
        "Totale_Lordo": None,
        "Rata_Addizionale_Regionale": None,
        "Rata_Addizionale_Comunale": None,
        "Acconto_Addizionale_Comunale": None,
        "Contributo_INPDAP_8_8": None,
        "Addizionale_INPDAP_1": None,
        "Contributo_Fondo_Credito_0_35": None,
        "Totale_Contributi_Sociali": None,
        "Imponibile_IRPEF": None,
        "IRPEF_Lorda": None,
        "Totale_Trattenute_IRPEF": None,
        "Trattenuta_Sindacale": None,
        "Arrotondamento_Precedente": None,
        "Trattenute_Corpo": None,
        "Totale_Trattenute": None,
        "Arrotondamento_Attuale": None,
        "Netto_Busta": None,
        "Imponibile_INAIL": None,
        "TFR_Mese": None,
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
                        
                # 6. Premio Risultato
                if "PREMIO RIS" in line:
                    match_premio = re.search(r"([\d\.]+,\d{2})\s*$", line.strip())
                    if match_premio and not dati["Premio_Risultato"]:
                        dati["Premio_Risultato"] = match_premio.group(1)

                # 7. Addizionali e Acconti
                if "ADDIZ.REGIONALE" in line or "ADDIZIONALE REGIONALE" in line:
                    match_reg = re.search(r"([\d\.]+,\d{2})\s*$", line.strip())
                    if match_reg and not dati["Rata_Addizionale_Regionale"]:
                        dati["Rata_Addizionale_Regionale"] = match_reg.group(1)
                
                if "ADD.COMUNALE" in line or "ADDIZIONALE COMUNALE" in line:
                    match_com = re.search(r"([\d\.]+,\d{2})\s*$", line.strip())
                    if match_com:
                        if "ACCONTO" in line:
                            dati["Acconto_Addizionale_Comunale"] = match_com.group(1)
                        elif not dati["Rata_Addizionale_Comunale"]:
                            dati["Rata_Addizionale_Comunale"] = match_com.group(1)

                # 7. Contributi
                if "TOTALE CONTRIBUTI SOCIALI" in line:
                    # I valori si trovano tipicamente nella riga successiva
                    if i+1 < len(lines):
                        # La riga successiva contiene i valori: Totale Lordo, Imponibile, Contributo 1, Contributo 2, Contributo 3, ..., Totale Contributi
                        # Es: "        14.162,31 14.162,00  1246,26   94,77   49,57                    1.390,60"
                        matches_contributi = re.findall(r"([\d\.]+,\d{2})", lines[i+1])
                        if len(matches_contributi) >= 6:
                            if not dati["Totale_Lordo"]:
                                dati["Totale_Lordo"] = matches_contributi[0]
                            dati["Contributo_INPDAP_8_8"] = matches_contributi[2]
                            dati["Addizionale_INPDAP_1"] = matches_contributi[3]
                            dati["Contributo_Fondo_Credito_0_35"] = matches_contributi[4]
                            dati["Totale_Contributi_Sociali"] = matches_contributi[-1]

                # 8. IRPEF e Trattenute (blocco contiguo)
                if "IRPEF LORDA TOTALE DETRAZIONI TOTALE TRATTENUTE IRPEF" in line:
                    if i+1 < len(lines):
                        matches_irpef = re.findall(r"([\d\.]+,\d{2})", lines[i+1])
                        if len(matches_irpef) >= 3:
                            dati["Imponibile_IRPEF"] = matches_irpef[0]
                            dati["IRPEF_Lorda"] = matches_irpef[1]
                            dati["Totale_Trattenute_IRPEF"] = matches_irpef[2]
                            
                    if i+2 < len(lines):
                        matches_tratt = re.findall(r"([\d\.]+,\d{2})", lines[i+2])
                        if len(matches_tratt) >= 4:
                            dati["Trattenuta_Sindacale"] = matches_tratt[0]
                            dati["Arrotondamento_Precedente"] = matches_tratt[1]
                            dati["Trattenute_Corpo"] = matches_tratt[2]
                            dati["Totale_Trattenute"] = matches_tratt[3]

                # 9. Netto Busta, Arrotondamento Attuale, Imponibile INAIL, TFR Mese
                if "NETTO BUSTA" in line:
                    for j in range(1, 4):
                        if i+j < len(lines):
                            matches_netto = re.findall(r"([\d\.]+,\d{2})", lines[i+j])
                            if len(matches_netto) == 2:
                                dati["Arrotondamento_Attuale"] = matches_netto[0]
                                dati["Netto_Busta"] = matches_netto[1]
                                
                                # La riga successiva a questa contiene INAIL e TFR alla fine
                                if i+j+1 < len(lines):
                                    matches_inail = re.findall(r"([\d\.]+,\d{2})", lines[i+j+1])
                                    if len(matches_inail) >= 2:
                                        dati["Imponibile_INAIL"] = matches_inail[-2]
                                        dati["TFR_Mese"] = matches_inail[-1]
                                break

                # 10. Totale Lordo (Fallback se non trovato con i contributi)
                if "TOTALE LORDO" in line and not dati["Totale_Lordo"]:
                    for j in range(1, 3):
                        if i+j < len(lines):
                            match_lordo = re.search(r"([\d\.]+,\d{2})", lines[i+j])
                            if match_lordo:
                                dati["Totale_Lordo"] = match_lordo.group(1)
                                break
                                
                # 11. IBAN
                if not dati["IBAN"]:
                    match_iban = re.search(r"(IT\d{2}[A-Z]\d{22})", line)
                    if match_iban:
                        dati["IBAN"] = match_iban.group(1)

    except Exception as e:
        print(f"Errore durante l'elaborazione del file {file_path}: {e}")
        
    return dati
