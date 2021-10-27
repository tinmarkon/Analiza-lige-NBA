import os
import re

directory = "C:/Users/TinM/Documents/Studij/Programiranje 1/Analiza-lige-NBA"
testna_datoteka = "testni.html"


def read_file(directory, filename):
    """Funkcija najde datoteko in jo vrne kot niz"""
    with open(os.path.join(directory, filename), 'r', encoding="utf-8") as f:
        string = f.read()
    return string


sample_player = re.compile( r'<tr class="full_table" >.*?data-stat="player" csk="(?P<Igralec>\S*)"'
                            r'.*?<td class="center " data-stat="pos" >(?P<Pozicija>\S*)</td>'
                            r'',
                            flags=re.DOTALL) 

def find_players(niz, vzorec):
    match = re.findall(vzorec, niz)
    return (match, len(match))
    

testna_datoteka = read_file(directory, testna_datoteka)


print(find_players(testna_datoteka, sample_player))
