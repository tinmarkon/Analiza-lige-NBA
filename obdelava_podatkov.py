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

sample_player = re.compile( r'<th scope="row" class="right " data-stat="ranker" csk="\d*" >(?P<Stevilka>\d*)</th>'
                            r'<td class="left " data-append-csv="\S*" data-stat="player" csk="\D*" ><a href="/players/\w/\S*.html">(?P<Igralec>\D*)</a></td>'
                            r'.*?<td class="\D* " data-stat="pos" >(?P<Pozicija>\S*)</td>'
                            r'.*?<td class="\D* " data-stat="team_id" ><a href="/teams/\w*\/2021.html\">(?P<ID_ekipe>\w*)</a></td>'
                            r'.*?<td class="\D*" data-stat="fg_per_g" >(?P<FG>\d\.\d)</td>'
                            r'<td class="\D*" data-stat="fga_per_g" >(?P<FGA>\S*)</td>'
                            r'.*?<td class="\D*" data-stat="trb_per_g" >(?P<TRB>\S*)</td>'
                            r'<td class="\D*" data-stat="ast_per_g" >(?P<AST>\S*)</td>'
                            r'<td class="\D*" data-stat="stl_per_g" >(?P<STL>\S*)</td>'
                            r'<td class="\D*" data-stat="blk_per_g" >(?P<BLK>\S*)</td>'
                            r'<td class="\D*" data-stat="tov_per_g" >(?P<TOV>\S*)</td>'
                            r'.*?<td class="\D*" data-stat="pts_per_g" >(?P<PTS>\S*)</td>',
                            flags=re.DOTALL)

sample_team = re.compile(   r'<a href=\'/teams/(?P<ID_ekipe>\w*)\/2021.html\'>(?P<Ekipa>\w*\s\w*\s?\w*?)</a>\*?</td>'
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
            'Stevilka igralca': player.groupdict()['Stevilka'],
            'Igralec': player.groupdict()['Igralec'],
            'Pozicija': player.groupdict()['Pozicija'],
            'ID ekipe': player.groupdict()['ID_ekipe'],
            'FG': float(player.groupdict()['FG']),
            'FGA': float(player.groupdict()['FGA']),
            'Skoki': float(player.groupdict()['TRB']),
            'Asistence': float(player.groupdict()['AST']),
            'Ukradene žoge': float(player.groupdict()['STL']),
            'Blokade': float(player.groupdict()['BLK']),
            'Izgubljene žoge': float(player.groupdict()['TOV']),
            'Tocke': float(player.groupdict()['PTS']),        
        })
    return players

def extract_teams(niz):
    teams = []
    for team in sample_team.finditer(niz):
        teams.append({
            "ID ekipe": team.groupdict()['ID_ekipe'],
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
