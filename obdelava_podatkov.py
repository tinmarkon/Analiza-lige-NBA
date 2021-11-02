import os
import re
import csv

directory = "C:/Users/TinM/Documents/Studij/Programiranje 1/Analiza-lige-NBA"
testna_datoteka = "testni.html"

sample_block = re.compile(  r'<tr class="full_table" >.*?'
                            r'</td></tr>',
                            flags=re.DOTALL)

# Ideja je da prvo preberem vzorec bloka za enega igralca, potem nadaljujem in za vsako postavko naredim svoj vzorec za določen atribut igralca
# Dodati je potrebno še datoteko ekip z ustreznimi podatki, potem vsako posebej zapisati kot csv datoteko
# Naslednji korak je s pomočjo Pandas knjižnice narediti ananlizo in jo vizualizirati
# TODO vprašaj ali se splača vzeti kaj drugega in narediti bolj temeljito analizo

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

def read_file(directory, filename):
    """Funkcija najde datoteko in jo vrne kot niz"""
    with open(os.path.join(directory, filename), 'r', encoding="utf-8") as f:
        string = f.read()
    return string

def find_players(niz, vzorec):
    """Funckija vzame niz in vzorec podatkov in vrača podatke o igralcih"""
    match = re.findall(vzorec, niz)
    return (match, len(match))

def extract_players(niz):
    players = []
    for player in sample_player.finditer(niz):
        players.append({
            'Igralec': player.groupdict()['Igralec'],
            'Pozicija': player.groupdict()['Pozicija'],
            'FG': float(player.groupdict()['FG']),
            'FGA': float(player.groupdict()['FGA']),
            'Skoki': float(player.groupdict()['Skoki']),
            'Asistence': float(player.groupdict()['Asistence']),
            'Vkradene žoge': float(player.groupdict()['Vkradene_žoge']),
            'Blokade': float(player.groupdict()['Blokade']),
            'Izgubljene žoge': float(player.groupdict()['Izgubljene_žoge']),
            'Tocke': float(player.groupdict()['Tocke']),        
        })
    return players
            

def pripravi_imenik(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def write_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    pripravi_imenik(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)
    

testna_datoteka = read_file(directory, testna_datoteka)


print(len(extract_players(testna_datoteka)))

### Mislim da nastane problem, ko se igralec ponovi, kaj se zgodi, če že imamo igralca v eni ekipi in potem sredi sezone preneha in začne igrati za neko drugo ekipo? 
### Bi potem gledal uteženo povprečje glede na tekme, ki jih je igral. Mislim da morem te robne primere poloviti v funkciji extract players