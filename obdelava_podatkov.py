import os
import re
import csv

### PODATKI O DIREKTORIJU ###
directory = "C:/Users/TinM/Documents/Studij/Programiranje 1/Analiza-lige-NBA"
players_file = "players.html"
teams_file ="teams.html"


### VZORCI ###
sample_block_players = re.compile(  r'<table class="sortable stats_table" id="per_game_stats" data-cols-to-freeze=",2" data-non-qual="1" data-qual-text="" data-qual-label=" When table is sorted, hide non-qualifiers for rate stats">'
                                    r'.*?</table>',
                                    flags=re.DOTALL)

sample_block_teams = re.compile(r'<table class="stats_table sortable " id="per_game-team" data-cols-to-freeze=",2"> <caption>Per Game Stats Table</caption>'
                                r'.*?</table>',
                                flags=re.DOTALL)

sample_player = re.compile( r'<tr class="full_table" >.*?data-stat="player" csk="(?P<Igralec>\S*)"'
                            r'.*?<td class="center " data-stat="pos" >(?P<Pozicija>\S*)</td>'
                            r'.*?<td class="right non_qual" data-stat="fg_per_g" >(?P<FG>\S*)</td>'
                            r'<td class="right non_qual" data-stat="fga_per_g" >(?P<FGA>\S*)</td>'
                            r'.*?<td class="right non_qual" data-stat="trb_per_g" >(?P<Skoki>\S*)</td>'
                            r'<td class="right non_qual" data-stat="ast_per_g" >(?P<Asistence>\S*)</td>'
                            r'<td class="right non_qual" data-stat="stl_per_g" >(?P<Ukradene_žoge>\S*)</td>'
                            r'<td class="right non_qual" data-stat="blk_per_g" >(?P<Blokade>\S*)</td>'
                            r'<td class="right non_qual" data-stat="tov_per_g" >(?P<Izgubljene_žoge>\S*)</td>'
                            r'.*?<td class="right non_qual" data-stat="pts_per_g" >(?P<Tocke>\S*)</td>',
                            flags=re.DOTALL)

sample_team = re.compile(   r'<a href=\'/teams/\w*\/2021.html\'>(?P<Ekipa>\w*\s\w*\s?\w*?)</a>\*?</td>'
                            r'<td class="right " data-stat="g" >(?P<G>\d\d)</td>'
                            r'<td class="right " data-stat="mp" >(?P<MP>\S*)</td>'
                            r'<td class="right " data-stat="fg" >(?P<FG>\S*)</td>'
                            r'<td class="right " data-stat="fga" >(?P<FGA>\S*)</td>'
                            r'.*?<td class="right " data-stat="fg3" >(?P<FG3>\S*)</td>'
                            r'<td class="right " data-stat="fg3a" >(?P<FGA3>\S*)</td>'
                            r'.*?<td class="right " data-stat="ft" >(?P<FT>\S*)</td>'
                            r'<td class="right " data-stat="fta" >(?P<FTA>\S*)</td>'
                            r'.*?<td class="right " data-stat="orb" >(?P<ORB>\S*)</td>'
                            r'<td class="right " data-stat="drb" >(?P<DRB>\S*)</td>'
                            r'.*?<td class="right " data-stat="ast" >(?P<AST>\S*)</td>'
                            r'<td class="right " data-stat="stl" >(?P<STL>\S*)</td>'
                            r'<td class="right " data-stat="blk" >(?P<BLK>\S*)</td>'
                            r'<td class="right " data-stat="tov" >(?P<TOV>\S*)</td>'
                            r'<td class="right " data-stat="pf" >(?P<PF>\S*)</td>'
                            r'<td class="right " data-stat="pts" >(?P<PTS>\S*)</td>',
                            flags=re.DOTALL)


### FUNKCIJE ZA ZAPISOVANJE IN BRANJE DATOTEK ###
def read_file(directory, filename):
    """Funkcija najde datoteko in jo vrne kot niz"""
    with open(os.path.join(directory, filename), 'r', encoding="utf-8") as f:
        string = f.read()
    return string

def make_file(ime_datoteke):
    '''Če še ne obstaja, pripravi prazen imenik za dano datoteko.'''
    imenik = os.path.dirname(ime_datoteke)
    if imenik:
        os.makedirs(imenik, exist_ok=True)

def write_csv(slovarji, imena_polj, ime_datoteke):
    '''Iz seznama slovarjev ustvari CSV datoteko z glavo.'''
    make_file(ime_datoteke)
    with open(ime_datoteke, 'w', encoding='utf-8', newline='') as csv_datoteka:
        writer = csv.DictWriter(csv_datoteka, fieldnames=imena_polj)
        writer.writeheader()
        for slovar in slovarji:
            writer.writerow(slovar)


### FUNKCIJE ZA SLOVARJE ###
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
            'Vkradene žoge': float(player.groupdict()['Ukradene_žoge']),
            'Blokade': float(player.groupdict()['Blokade']),
            'Izgubljene žoge': float(player.groupdict()['Izgubljene_žoge']),
            'Tocke': float(player.groupdict()['Tocke']),        
        })
    return players

def extract_teams(niz):
    teams = []
    for team in sample_team.finditer(niz):
        teams.append({
            'Ekipa': team.groupdict()['Ekipa'],
            'Stevilo tekem': float(team.groupdict()['G']),
            'Igrane minute': float(team.groupdict()['MP']),
            'Zadet met': float(team.groupdict()['FG']),
            'Poskus meta': float(team.groupdict()['FGA']),
            'Zadet met za 3': float(team.groupdict()['FG3']),
            'Poskus meta za 3': float(team.groupdict()['FGA3']),
            'Zadeti prosti meti': float(team.groupdict()['FT']),
            'Poskus prostega meta': float(team.groupdict()['FTA']),
            'Skoki v napadu': float(team.groupdict()['ORB']),
            'Skoki v obrambi': float(team.groupdict()['DRB']),
            'Asistence': float(team.groupdict()['AST']),
            'Ukradene žoge': float(team.groupdict()['STL']),
            'Blokade': float(team.groupdict()['BLK']),
            'Izgubljene žoge': float(team.groupdict()['TOV']),
            'Osebne napake': float(team.groupdict()['PF']),
            'Tocke': float(team.groupdict()['PTS'])
        })
    return teams
        

            


    
### BRANJE PODATKOV ###
players_file = read_file(directory, players_file)
teams_file = read_file(directory, teams_file)


### EKIPE ###
teams_block = re.findall(sample_block_teams, teams_file)[0] ## Najdem kos htmlja v katerem so vse ekipe
teams = extract_teams(teams_block)
write_csv(teams, [header for header in teams[0].keys()], 'teams.csv')

### IGRALCI ###
players_block = re.findall(sample_block_players, players_file)[0]
players = extract_players(players_block)
write_csv(players, [header for header in players[0].keys()], 'players.csv')


#write_csv(players, [glava for glava in players[0].keys()], 'testnic.csv')

### Mislim da nastane problem, ko se igralec ponovi, kaj se zgodi, če že imamo igralca v eni ekipi in potem sredi sezone preneha in začne igrati za neko drugo ekipo? 
### Bi potem gledal uteženo povprečje glede na tekme, ki jih je igral. Mislim da morem te robne primere poloviti v funkciji extract players