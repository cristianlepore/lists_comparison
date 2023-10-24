import os, re, csv

# Set your parameters:
similarity_grade = 0.55
file_name_orbis = "orbisCSV.CSV"
file_name_pitchbook = "PitchbookCSV.CSV"

type_society = ["SRL", "SPA", "SNC", "SA", "SAPA", "SAS", "SCRL", "SCPA", "SS", "SNCA", "SRLS", "SPAA", "SPAR", "SPAP", "SPAPA", "SRC", "LTD", "INC", "CO", "CORP", "LLC", "PLC"]

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

    for society_type in type_society:
        line = re.sub(rf'\b{society_type}\b', f'\n{society_type}\n', line)
    
    line = re.sub('|'.join(map(re.escape, type_society)), substitute_type_society, line)

    return line.strip()

def read_file(file_name):
    # Leggi il file e restituisci una lista di linee processate
    processed_lines = set()
    file_path = get_absolute_path(file_name)

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            for line in file:
                lines = process_line(line)
                for processed_line in lines.split('\n'):
                    processed_line = processed_line.strip()
                    if processed_line:
                        processed_lines.add(processed_line)

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
    #n = int(words_means(element1))
    n = 3

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
    # Lista per elementi di list1 che non passano il test
    different_in_list1 = []
    remaining_list2 = list2[:]

    for element1 in list1:
        found_similar = False
        for element2 in list2:
            similarity = ngram_similarity(element1, element2)
            if similarity >= similarity_grade:
                similar.append((element1+" || "+element2))
                found_similar = True
                # Verifica se l'elemento esiste ancora in remaining_list2
                if element2 in remaining_list2: 
                    remaining_list2.remove(element2)

        if not found_similar:
            different_in_list1.append(element1)

    different_in_list2 = remaining_list2  # Gli elementi rimanenti in list2 sono diversi

    return similar, different_in_list1, different_in_list2

def write_to_file(name_file, elements):
    # Apre il file in modalità scrittura
    with open(name_file, mode='w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        
        # Scrive i dati nella tabella CSV
        for element in elements:
            writer.writerow([element])

def main():
    list_orbis = read_file(file_name_orbis)
    list_pitchbook = read_file(file_name_pitchbook)

    results = find_similarity(list_orbis, list_pitchbook)

    # Specifica il nome del file CSV in cui desideri scrivere i dati
    file_similarity = "Orbis_vs_Pitchbook.csv"
    file_excluded_orbis = "Orbis_excluded.csv"
    file_excluded_pitchbook = "Pitchbook_excluded.csv"

    write_to_file(file_similarity, results[0])
    write_to_file(file_excluded_orbis, results[1])
    write_to_file(file_excluded_pitchbook, results[2])

    print(f"Record simili: {len(results[0])}")    
    print(f"Esclusi Orbis: {len(results[1])}")
    print(f"Esclusi Pitchbook: {len(results[2])}")
    
if __name__ == "__main__":
    main()
