import os, re, csv

type_society = ["SRL", "SPA", "SNC", "SAPA", "SAS", "SCRL", "SCPA", "SS", "SNCA", "SRLS", "SPAA", "SPAR", "SPAP", "SPAPA", "SRC", "LTD", "INC", "CO", "CORP", "LLC", "PLC"]

def get_absolute_path(file_name):
    # Ottieni il percorso assoluto del file
    return os.path.abspath(file_name)

def substitute_type_society(match):
    sigla = match.group()
    return ''

def process_line(line):
    # Applica le trasformazioni alla linea
    line = line.upper()
    line = ' '.join(re.sub(r'\.', '', word) for word in re.findall(r'[a-zA-Z0-9.]+', line))
    line = re.sub(r'\s+', ' ', line)
    line = re.sub('|'.join(map(re.escape, type_society)), substitute_type_society, line)
    return line.strip()

def read_file(file_name):
    # Leggi il file e restituisci una lista di linee processate
    processed_lines = set()
    file_path = get_absolute_path(file_name)

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                line = process_line(line)
                if line:
                    processed_lines.add(line)

    return sorted(list(processed_lines))

def generate_ngrams(text, n):
    # Aggiungi spazi alle estremità del testo per considerare gli spazi
    text = f" {text}"
    ngrams = []
    for i in range(len(text) - n + 1):
        ngram = text[i:i + n]
        ngrams.append(ngram)
    return ngrams

def words_means(str):
    # Dividi la stringa in parole
    parole = str.split()
    
    # Inizializza una variabile per la somma delle lunghezze delle parole
    sum = 0
    
    # Calcola la somma delle lunghezze delle parole
    for word in parole:
        sum += len(word)
    
    # Calcola il numero medio di caratteri per parola
    if len(parole) > 0:
        numero_medio = sum / len(parole)
    else:
        numero_medio = 0
    
    return numero_medio

def ngram_similarity(element1, element2):

    # Definisco il parametro n
    n = int(words_means(element1))

    ngrams_element1 = generate_ngrams(element1, n)
    ngrams_element2 = generate_ngrams(element2, n)
    
    # Calcola l'intersezione tra i trigrammi dei due testi
    intersection = len(set(ngrams_element1).intersection(ngrams_element2))
    
    # Calcola la similarità basata sugli n-gram
    similarity = intersection / (len(ngrams_element1) + len(ngrams_element2) - intersection)
    
    return similarity

def find_similarity(list1, list2):
    # Trova elementi simili tra due liste
    similar = []
    for element1 in list1:
        for element2 in list2:
            similarity = ngram_similarity(element1, element2)
            if similarity >= 0.55:
                similar.append((element1+" || "+element2))
    return similar

def main():
    file_name_orbis = "OrbisCSV.CSV"
    file_name_pitchbook = "PitchbookCSV.CSV"

    list_orbis = read_file(file_name_orbis)
    list_pitchbook = read_file(file_name_pitchbook)

    similar_elements = find_similarity(list_orbis, list_pitchbook)

    # Specifica il nome del file CSV in cui desideri scrivere i dati
    nome_file_csv = "Similar_companies.csv"

    # Apre il file in modalità scrittura
    with open(nome_file_csv, mode='w', newline='') as file_csv:
        writer = csv.writer(file_csv)

        # Scrive i dati nella tabella CSV
        for element in similar_elements:
            writer.writerow([element])

    print(f"Numero di aziende simili: {len(similar_elements)}")
    print(f"I dati sono stati scritti nel file '{nome_file_csv}'.")

if __name__ == "__main__":
    main()
