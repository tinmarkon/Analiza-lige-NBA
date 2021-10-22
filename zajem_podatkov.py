import requests
import re
import os


test_link = "https://www.basketball-reference.com/leagues/NBA_2021_per_game.html"
testna_datoteka = "testni.html"
directory = "C:/Users/TinM/Documents/Studij/Programiranje 1/Analiza-lige-NBA"
path = os.path.join(directory, testna_datoteka)


def import_data(link):
    """Funkcija sprejme link do strani in vrača string"""
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


def save_page(link, file, directory):
    """Funkcija sprejme link do spletne strani in zapiše html v datoteko"""
    string = import_data(link)
    save_text(string, file, directory)







def main(redownload=True, reparse=True):
    ### Naredim request in shranim v html datoteko ###
    save_page(test_link, testna_datoteka, directory)
    
    ### TODO priredi funckijo main, da ne bo potrebno vsakič downloadat in/ali parsat datoteke





if __name__ == "__main__":
    main()