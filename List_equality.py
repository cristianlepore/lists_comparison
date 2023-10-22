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

def find_equal_elements(list1, list2):
    # Trova elementi uguali tra due liste
    equal = []
    for element1 in list1:
        for element2 in list2:
            if element1 == element2:
                equal.append((element1))
    return equal

def main():
    file_name_orbis = "OrbisCSV.CSV"
    file_name_pitchbook = "PitchbookCSV.CSV"

    list_orbis = read_file(file_name_orbis)
    list_pitchbook = read_file(file_name_pitchbook)

    equal_elements = find_equal_elements(list_orbis, list_pitchbook)

    # Specifica il nome del file CSV in cui desideri scrivere i dati
    nome_file_csv = "Equal_companies.csv"

    # Apre il file in modalità scrittura
    with open(nome_file_csv, mode='w', newline='') as file_csv:
        writer = csv.writer(file_csv)

        # Scrive i dati nella tabella CSV
        for element in equal_elements:
            writer.writerow([element])

    print(f"Numero di aziende uguali: {len(equal_elements)}")
    print(f"I dati sono stati scritti nel file '{nome_file_csv}'.")

if __name__ == "__main__":
    main()
