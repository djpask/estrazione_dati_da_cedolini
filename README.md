# Estrazione Dati da Cedolini

Un piccolo progetto in Python per estrarre informazioni e dati utili dai cedolini (buste paga).

## Struttura del Progetto

- `src/`: Contiene il codice sorgente dell'applicazione.
- `tests/`: Contiene i test unitari.
- `data/input/`: Inserisci qui i file dei cedolini da elaborare (i file qui sono ignorati da git, tranne `.gitkeep`).
- `data/output/`: I risultati dell'estrazione verranno salvati qui (i file qui sono ignorati da git, tranne `.gitkeep`).

## Requisiti e Installazione

1. Crea un ambiente virtuale (consigliato):
   ```bash
   python -m venv venv
   source venv/bin/activate  # Su Linux/Mac
   # venv\Scripts\activate   # Su Windows
   ```

2. Installa le dipendenze:
   ```bash
   pip install -r requirements.txt
   ```

## Utilizzo

```bash
python src/main.py
```
