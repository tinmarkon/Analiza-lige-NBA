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
                            r'.*?<td class="right non_qual" data-stat="fg_per_g" >(?P<FG>\S*)</td>'
                            r'<td class="right non_qual" data-stat="fga_per_g" >(?P<FGA>\S*)</td>'
                            r'.*?<td class="right non_qual" data-stat="trb_per_g" >(?P<Skoki>\S*)</td>'
                            r'<td class="right non_qual" data-stat="ast_per_g" >(?P<Asistence>\S*)</td>'
                            r'<td class="right non_qual" data-stat="stl_per_g" >(?P<Vkradene_žoge>\S*)</td>'
                            r'<td class="right non_qual" data-stat="blk_per_g" >(?P<Blokade>\S*)</td>'
                            r'<td class="right non_qual" data-stat="tov_per_g" >(?P<Izgubljene_žoge>\S*)</td>'
                            r'.*?<td class="right non_qual" data-stat="pts_per_g" >(?P<Tocke>\S*)</td>',
                            flags=re.DOTALL) 

def find_players(niz, vzorec):
    """Funckija vzame niz in vzorec podatkov in vrača podatke o igralcih"""
    match = re.findall(vzorec, niz)
    return (match, len(match))
    

testna_datoteka = read_file(directory, testna_datoteka)


print(find_players(testna_datoteka, sample_player))
