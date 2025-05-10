#!/data/data/com.termux/files/usr/bin/python

###### lisq #######
################### by © funnut https://github.com/funnut

from . import encrypt, utils
import os, sys, shlex, re # match() for reiterate()
import shutil # szerokość terminalu
import readline # historia poleceń
from datetime import datetime
from random import randrange, choice
from pathlib import Path


def glowna_funkcja(command):
    cmd, arg, arg1 = command
### ADD
    try:
        if cmd == 'add':
            if not arg:
                arg = input("Wpisz notatkę: ").strip()
                if not arg:
                    print ("Anulowano dodawanie – nie podano treści notatki.")
                    return
            if arg:
                write_file(arg)
            return
### DELETE
        elif cmd == 'del':
            if not arg:
                arg = input("Wpisz ID: ").strip().lower()
                if not arg:
                    print("Anulowano usuwanie – nie podano ID.")
                    return
            delete(arg)
            return
### SHOW
        elif cmd in ['show', 's']:
            read_file(arg if arg else 'last')
            return
### CLEAR SCREEN
        elif cmd in ['clear', 'c']:
            print ("\n" * 50)
            return
### REITERATE
        elif cmd == 'reiterate':
            yesno = input (f'Czy chcesz reiterować wszystkie notatki? (t/n): ')
            if yesno.lower() in ['y', 'yes','t','tak', '']:
                reiterate()
                print ('Reiteracja ukończona.')
                return
            else:
                print ('Reiteracja anulowana.')
                return
### HELP
        elif cmd in ['help', 'h', 'lisq']:
            print (f"{utils.COLORS['bgpurple']}# About{utils.COLORS['reset']}\n\n"
                "From Polish \"lisek / foxie\" - lisq is a lightweight note-taking app that work with .txt files.\n\n"
                "Code available under a non-commercial license (see LICENSE file).\n\n"
                "Copyright © funnut\n"
                "https://github.com/funnut\n\n"
                f"{utils.COLORS['bgpurple']}# Commands{utils.COLORS['reset']}\n\n"
                ": quit, q, exit\n"
                ": clear, c        - clear screen\n"
                ":\n"
                ": show, s         - show recent notes (default 10)\n"
                ":      [int]      - show number of recent notes\n"
                ":      [str]      - show notes containing [string]\n"
                ":      all        - show all notes\n"
                ":      random, r  - show a random note\n"
                ":\n"
                ": del  [str]      - delete notes containing [string]\n"
                ":      last, l    - delete the last note\n"
                ":      all        - delete all notes\n"
                ":\n"
                ": cfg  open, show\n"
                ": cfg -encryption on, off, set, newpass\n"
                ":     -keypath open, unset, del or <path>\n"
                ":     -notespath open, unset or <path>\n"
                ":     -editor open or <editor>\n"
                ":\n"
                ": encrypt ~/file.txt - encrypting any file\n"
                ": decrypt ~/file.txt - decrypting any file\n"
                ":\n"
                ": reiterate   - renumber notes' IDs\n"
                ": edit        - open the notes file in editor\n\n"
                f"{utils.COLORS['bgpurple']}# CLI Usage{utils.COLORS['reset']}\n\n"
                "lisq [command] [argument] [argument-1]\n"
                "lisq add or / \'sample note text\'")
            return
### EDIT
        elif cmd == 'edit':
            print ('')
            os.system(f"{utils.EDITOR()} {utils.NOTES_PATH()}")
            return
### EXIT
        elif cmd in ['quit', 'q', 'exit']:
            if utils.cfg_setting("encryption"):
                encrypt.encrypt(utils.NOTES_PATH())
            sys.exit()
### SETCFG
        elif cmd == 'cfg':
            encrypt.setcfg(arg if arg else 'read', arg1)
            return
### ENCRYPT/DECRYPT
        elif cmd == 'encrypt':
            encrypt.process_file(cmd,arg if arg else None)
        elif cmd == 'decrypt':
            encrypt.process_file(cmd,arg if arg else None)
### INVALID COMMAND
        else:
            raise ValueError("Nieprawidłowe polecenie.")
    except Exception as e:
        print(f"\aBłąd: {e}")


def sprawdz_input(usr_input):
    """Przetwarzanie wejścia od użytkownika na polecenie i argument."""
    if not usr_input:
        return ('add', None, None)
    elif len(usr_input) == 1:
        return (usr_input[0].lower(), None, None)
    elif len(usr_input) == 2:
        return (usr_input[0].lower(), usr_input[1], None)
    else:
        return (usr_input[0].lower(), usr_input[1], usr_input[2])


def read_file(a):
    """Odczytuje plik i wyświetla notatki."""
    terminal_width = shutil.get_terminal_size().columns
    print(f"{utils.COLORS['yellow']} _id _data","=" * (terminal_width-12),utils.COLORS['reset'])
    try:
        with open(utils.NOTES_PATH(), 'r', encoding='utf-8') as plik:
            linie = plik.readlines()
            if a == 'all':
                do_wyswietlenia = linie
            elif a == 'last':
                do_wyswietlenia = linie[-10:] # sets nr of lines shown by 'show'
            elif a in ['random', 'r']:
                do_wyswietlenia = [choice(linie)]
            elif a.isdigit():
                do_wyswietlenia = linie[-int(a):]
            else:
                znalezione = [linia for linia in linie if a.lower() in linia.lower()]
                if znalezione:
                    do_wyswietlenia = znalezione
                else:
                    return print("\nNie znaleziono pasujących elementów.")
            for linia in do_wyswietlenia:
                parts = linia.split()
                formatted_date = "/".join(parts[1].split("/")[1:])  # Usunięcie roku
                print(f"{utils.COLORS['yellow']}{parts[0]} {formatted_date}{utils.COLORS['reset']} {utils.COLORS['green']}{' '.join(parts[2:]).strip()}{utils.COLORS['reset']}")
            print(f"\nZnaleziono {len(do_wyswietlenia)} pasujących elementów.")
    except FileNotFoundError:
        print(f"\a\n'{utils.NOTES_PATH()}'\n\nPlik nie został znaleziony.")


def write_file(a):
    """Dodaje nową notatkę do pliku."""
    try:
        with open(utils.NOTES_PATH(), 'r', encoding='utf-8') as file:
            lines = file.readlines()
        if lines:
            last_line = lines[-1]
            last_id = int(last_line.split()[0][1:])  # Extract the numeric part of the ID (after 'id')
            id_ = last_id + 1
        else:
            id_ = 1
    except FileNotFoundError:
        id_ = 1
    formatted_id = f"i{str(id_).zfill(3)}"
    data_ = datetime.now().strftime("%Y/%m/%d")
    with open(utils.NOTES_PATH(), 'a', encoding='utf-8') as file:
        file.write(f"{formatted_id} {data_} :: {a}\n")
    print("Notatka została dodana.")


def delete(arg):
    """Usuwa notatki na podstawie podanego argumentu:
    - 'id' (np. '123') - usuwa notatki zawierające identyfikator,
    - 'l' - usuwa ostatnią notatkę,
    - 'all' - usuwa wszystkie notatki.
    """
    with open(utils.NOTES_PATH(), "r", encoding="utf-8") as plik:
        linie = plik.readlines()
    if arg == "all":
        yesno = input("Ta operacja trwale usunie wszystkie notatki.\nCzy chcesz kontynuować? (t/n): ")
        if yesno.lower() in ['y','yes','t','tak']:
            open(utils.NOTES_PATH(), "w", encoding="utf-8").close()
            print("Wszystkie notatki zostały usunięte.")
        else:
            print("Operacja anulowana.")
    elif arg in ["l","last"]:
        if linie:
            yesno = input("Ta operacja trwale usunie ostatnio dodaną notatkę.\nCzy chcesz kontynuować? (t/n): ")
            if yesno.lower() in ['y','yes','t','tak','']:
                with open(utils.NOTES_PATH(), "w", encoding="utf-8") as plik:
                    plik.writelines(linie[:-1])
                print("Ostatnia notatka została usunięta.")
            else:
                print("Operacja anulowana.")
        else:
            print("Brak notatek do usunięcia.")
    else:
        nowe_linie = [linia for linia in linie if arg not in linia]
        numer = len(linie) - len(nowe_linie)
        if numer > 0:
            yesno = input(f"Ta operacja trwale usunie {numer} notatek zawierających '{utils.COLORS["yellow"]}{arg}{utils.COLORS["reset"]}'. Czy chcesz kontynuować? (t/n): ")
            if yesno.lower() in ['y','yes','t','tak','']:
                with open(utils.NOTES_PATH(), "w", encoding="utf-8") as plik:
                    plik.writelines(nowe_linie)
                reiterate()
                print(f"Usunięto {numer} notatki zawierające identyfikator {arg}.")
            else:
                print("Operacja anulowana.")
        else:
            print("Nie znaleziono notatek do usunięcia.")


def reiterate():
    with open(utils.NOTES_PATH(), "r", encoding="utf-8") as f:
        linie = f.readlines()
    nowy_numer = 1
    poprawione_linie = []
    for linia in linie:
        dopasowanie = re.match(r"i\d{1,}", linia)
        if dopasowanie:
            nowa_linia = f"i{nowy_numer:03d}{linia[dopasowanie.end():]}"
            nowy_numer += 1
        else:
            nowa_linia = linia  # Zachowaj linię bez zmian
        poprawione_linie.append(nowa_linia)
    with open(utils.NOTES_PATH(), "w", encoding="utf-8") as f:
        f.writelines(poprawione_linie)


def pobierz_input():
    """Pobiera polecenie użytkownika w trybie interaktywnym."""
    while True:
        try:
            print('')
            print(">> add / del / show")
            usr_input = shlex.split(input(">> ").strip())
            print('')
            glowna_funkcja(sprawdz_input(usr_input))
        except ValueError as e:
            print('')
            print("Błąd składni: ", e)
            continue
        except EOFError:
            usr_input = []
            if utils.cfg_setting("encryption"):
                encrypt.encrypt(utils.NOTES_PATH())
            else:
                print("closed")
            print('')
            break


def main():
    """Interfejs wiersza poleceń"""
    if utils.cfg_setting("encryption") == 'ON':
        while True:
            fernet = encrypt.generate_key(save_to_file=True)
            result = encrypt.decrypt(utils.NOTES_PATH(),fernet)
            if result is not None:
                break
    if utils.cfg_setting("encryption") == 'SET':
        encrypt.decrypt(utils.NOTES_PATH())
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['add','/']:
            note = " ".join(sys.argv[2:])
            write_file(note)
            if utils.cfg_setting("encryption"):
                encrypt.encrypt(utils.NOTES_PATH())
            sys.exit()
        else:
            usr_input = sys.argv[1:]
            glowna_funkcja(sprawdz_input(usr_input))
            if utils.cfg_setting("encryption") == 'ON':
                encrypt.encrypt(utils.NOTES_PATH())
            if utils.cfg_setting("encryption") == 'SET':
                if not os.path.exists(utils.KEY_PATH()):
                    encrypt.generate_key(save_to_file=True)
                encrypt.encrypt(utils.NOTES_PATH())
            sys.exit()
    else:
        readline.set_history_length(100)
        print(fr""" _ _
| (_)___  __ _
| | / __|/ _` |
| | \__ \ (_| |
|_|_|___/\__, |
 quit - help|_|{randrange(0,1000)}""")
        pobierz_input()

