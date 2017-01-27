import sys

def getAllFilePathsAndCount(sourcePath):

    styles = []
    paths = []
    n = 0  # broj ukupnih slucajeva
    separator = ' = '

    with open(sourcePath) as file:
        data = file.read()
        lines = data.split('\n') # sve linije iz ulaznog fajla

        for id, line in enumerate(lines):
            cols = line.split(separator)
            if(cols[0] == ''): # za svaku liniju, uzmemo njen prvi deo sa putanjom do slike, ako nije prazna linija
                continue
            paths.append(cols[0]) # dodamo u spisak svih putanja i aktuelnu
            if len(cols)>1:
                styles.append(cols[1]) # i napravimo spisak svih stilova
            else:
                styles.append("")

            n += 1 # inkrementiramo ukupan broj slucajeva

    return [paths,n,styles] # vratimo spisak svih  putanja (do slika), i njihov ukupan broj

