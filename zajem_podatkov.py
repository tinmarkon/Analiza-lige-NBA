import requests
import os


players_link = "https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"
players_file = "players.html"
teams_link = "https://www.basketball-reference.com/leagues/NBA_2021.html"
teams_file = "teams.html"
directory = "C:/Users/TinM/Documents/Studij/Programiranje 1/Analiza-lige-NBA"



def import_data(link):
    """Funkcija sprejme link do strani in vrača niz"""
    try:
        string = requests.get(link)
    except requests.exceptions.ConnectionError as e:
        print(f"Napaka pri povezovanju do: {link}: \n{e}")
    if string.status_code == requests.codes.ok:
        return string.text
    else:
        raise requests.HTTPError(f"Ni ok: {string.status_code}")


def save_text(text, file, directory):
    """Funkcija vzame tekst in zapiše html datoteko, če datoteka"""
    path = os.path.join(directory, file)
    with open(file, mode="w", encoding="utf-8") as f:
        f.write(text)


def save_page(link, file, directory, force=False):
    """Funkcija sprejme link do spletne strani in zapiše html v datoteko"""
    if os.path.isfile(file) and not force:
        print(f"Datoteka {file} že obstaja!")
    else:
        string = import_data(link)
        save_text(string, file, directory)

def main():
    save_page(players_link, players_file, directory)
    save_page(teams_link, teams_file, directory)


if __name__ == "__main__":
    main()