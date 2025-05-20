#!/data/data/com.termux/files/usr/bin/python

###### lisq #######
################### by © funnut https://github.com/funnut

from . import encryption, utils
import os, sys, shlex, re # match() for reiterate()
import shutil # szerokość terminalu
import readline # historia poleceń
from datetime import datetime
from random import randrange, choice
from pathlib import Path
import subprocess

theme = utils.get_theme()
reset = utils.COLORS['reset']

def glowna_funkcja(command):
    cmd, arg, arg1 = command
### ADD
    try:
        if cmd == 'add':
            if not arg:
                arg = input(f"{theme['text']}Wpisz notatkę: {reset}").strip()
                if not arg:
                    print(f"{theme['text']}Anulowano dodawanie – nie podano treści notatki.{reset}")
                    return
            if arg:
                write_file(arg)
            return
### DELETE
        elif cmd == 'del':
            if not arg:
                arg = input(f"{theme['text']}Wpisz ID: {reset}").strip().lower()
                if not arg:
                    print(f"{theme['text']}Anulowano usuwanie – nie podano ID.{reset}")
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
            yesno = input (f"{theme['text']}Czy chcesz reiterować wszystkie notatki? (t/n): {reset}")
            if yesno.lower() in ['y', 'yes','t','tak', '']:
                reiterate()
                print(f"{theme['text']}Reiteracja ukończona.{reset}")
                return
            else:
                print(f"{theme['text']}Reiteracja anulowana.{reset}")
                return
### HELP
        elif cmd in ['help', 'h', 'lisq']:
            print (f"""{theme['header']}# About{reset}

{theme['text']}From Polish \"lisek / foxie\" - lisq is a lightweight note-taking app that work with .txt files.

Code available under a non-commercial license (see LICENSE file).

Copyright © funnut https://github.com/funnut{reset}

{theme['header']}# Commands{reset}

{theme['text']}: quit, q, exit
: clear, c        - clear screen
:
: show, s         - show recent notes (default 10)
:      [int]      - show number of recent notes
:      [str]      - show notes containing [string]
:      all        - show all notes
:      random, r  - show a random note
:
: del  [str]      - delete notes containing [string]
:      last, l    - delete the last note
:      all        - delete all notes
:
: cfg  open, show
: cfg -encryption on, off, set, newpass
:     -keypath open, unset, del or <path>
:     -notespath open, unset or <path>
:     -editor open or <editor>
:
: encrypt ~/file.txt - encrypting any file
: decrypt ~/file.txt - decrypting any file
:
: reiterate   - renumber notes' IDs
: edit        - open the notes file in editor{reset}

{theme['header']}# CLI Usage{reset}

{theme['text']}lisq [command] [argument] [argument-1]
lisq add or / \'sample note text\'{reset}""")
            return
### EDIT
        elif cmd == 'edit':
            print ('')
            subprocess.run([utils.EDITOR(),utils.NOTES_PATH()])
            return
### EXIT
        elif cmd in ['quit', 'q', 'exit']:
            if utils.get_setting("encryption"):
                encryption.encrypt(utils.NOTES_PATH())
            sys.exit()
### SETCFG
        elif cmd == 'cfg':
            utils.setcfg(arg if arg else 'read', arg1)
            return
### ENCRYPT/DECRYPT
        elif cmd == 'encrypt':
            encryption.process_file(cmd,arg if arg else None)
        elif cmd == 'decrypt':
            encryption.process_file(cmd,arg if arg else None)
### INVALID COMMAND
        else:
            raise ValueError(f"{theme['error']}Nieprawidłowe polecenie.{reset}")
    except Exception as e:
        print(f"{theme['error']}Błąd: {e}{reset}")


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
    print(f"{theme['notes-top']} _id _data {'=' * (terminal_width - 12)}{reset}")
    try:
        with open(utils.NOTES_PATH(), 'r', encoding='utf-8') as plik:
            linie = [linia for linia in plik.readlines() if linia.strip()]
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
                    return print(f"{theme['text']}\nNie znaleziono pasujących elementów.{reset}")
            for linia in do_wyswietlenia:
                parts = linia.split()
                formatted_date = "-".join(parts[1].split("-")[1:])  # Usunięcie roku
                print(f"{theme['notes-side']}{parts[0]} {formatted_date}{reset} {theme['notes-text']}{' '.join(parts[2:]).strip()}{reset}")
            print(f"{theme['text']}\nZnaleziono {len(do_wyswietlenia)} pasujących elementów.{reset}")
    except FileNotFoundError:
        print(f"\n{theme['error']}'{utils.NOTES_PATH()}'\n\nPlik nie został znaleziony.{reset}")


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
    data_ = datetime.now().strftime("%Y-%m-%d")
    with open(utils.NOTES_PATH(), 'a', encoding='utf-8') as file:
        file.write(f"{formatted_id} {data_} :: {a}\n")
    print(f"{theme['text']}Notatka została dodana.{reset}")


def delete(arg):
    """Usuwa notatki na podstawie podanego argumentu:
    - 'id' (np. '123') - usuwa notatki zawierające identyfikator,
    - 'l' - usuwa ostatnią notatkę,
    - 'all' - usuwa wszystkie notatki.
    """
    with open(utils.NOTES_PATH(), "r", encoding="utf-8") as plik:
        linie = plik.readlines()
    if arg == "all":
        yesno = input(f"{theme['text']}Ta operacja trwale usunie wszystkie notatki.\nCzy chcesz kontynuować? (t/n): {reset}")
        if yesno.lower() in ['y','yes','t','tak']:
            open(utils.NOTES_PATH(), "w", encoding="utf-8").close()
            print(f"{theme['text']}Wszystkie notatki zostały usunięte.{reset}")
        else:
            print(f"{theme['text']}Operacja anulowana.{reset}")
    elif arg in ["l","last"]:
        if linie:
            yesno = input(f"{theme['text']}Ta operacja trwale usunie ostatnio dodaną notatkę.\nCzy chcesz kontynuować? (t/n): {reset}")
            if yesno.lower() in ['y','yes','t','tak','']:
                with open(utils.NOTES_PATH(), "w", encoding="utf-8") as plik:
                    plik.writelines(linie[:-1])
                print(f"{theme['text']}Ostatnia notatka została usunięta.{reset}")
            else:
                print(f"{theme['text']}Operacja anulowana.{reset}")
        else:
            print(f"{theme['text']}Brak notatek do usunięcia.{reset}")
    else:
        nowe_linie = [linia for linia in linie if arg not in linia]
        numer = len(linie) - len(nowe_linie)
        if numer > 0:
            yesno = input(f"{theme['text']}Ta operacja trwale usunie {numer} notatek zawierających '{arg}'. Czy chcesz kontynuować? (t/n): {reset}")
            if yesno.lower() in ['y','yes','t','tak','']:
                with open(utils.NOTES_PATH(), "w", encoding="utf-8") as plik:
                    plik.writelines(nowe_linie)
                reiterate()
                print(f"{theme['text']}Usunięto {numer} notatki zawierające identyfikator {arg}.{reset}")
            else:
                print(f"{theme['text']}Operacja anulowana.{reset}")
        else:
            print(f"{theme['text']}Nie znaleziono notatek do usunięcia.{reset}")


def reiterate():
    """Przenumerowuje ID wszystkich notatek"""
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
            print(f"{theme['nav']}>> add / del / show"+reset)
            usr_input = shlex.split(input(f"{theme['nav-a']} > {reset}").strip())
            print('')
            glowna_funkcja(sprawdz_input(usr_input))
        except ValueError as e:
            print('')
            print(f"{theme['error']}Błąd składni: str(e){reset}")
            continue
        except EOFError:
            usr_input = []
            if utils.get_setting("encryption"):
                encryption.encrypt(utils.NOTES_PATH())
            else:
                print(theme['text']+"closed"+reset)
            print('')
            break


def main():
    """Interfejs wiersza poleceń"""
    if utils.get_setting("encryption") == 'on':
        for attempt in range(3):
            fernet = encryption.generate_key(save_to_file=False)
            try:
                result = encryption.decrypt(utils.NOTES_PATH(),fernet)
                if result:
                    print(f"{theme['text']}decrypted{reset}")
                    break
            except Exception as e:
                print(f"{theme['error']}Błąd:{reset} {e}")
        else:
            print(f"{theme['text']}\nZbyt wiele nieudanych prób.{reset}")
            sys.exit(1)
    if utils.get_setting("encryption") == 'set':
        encryption.decrypt(utils.NOTES_PATH())
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['add','/']:
            note = " ".join(sys.argv[2:])
            write_file(note)
            if utils.get_setting("encryption"):
                encryption.encrypt(utils.NOTES_PATH())
            sys.exit()
        else:
            usr_input = sys.argv[1:]
            glowna_funkcja(sprawdz_input(usr_input))
            if utils.get_setting("encryption") == 'on':
                encryption.encrypt(utils.NOTES_PATH())
            if utils.get_setting("encryption") == 'set':
                if not os.path.exists(utils.KEY_PATH()):
                    encryption.generate_key(save_to_file=True)
                encryption.encrypt(utils.NOTES_PATH())
            sys.exit()
    else:
        readline.set_history_length(100)
        print(fr"""{theme['intro']}
 _ _
| (_)___  __ _
| | / __|/ _` |
| | \__ \ (_| |
|_|_|___/\__, |
 quit - help|_|{randrange(0,1000)}{reset}""")
        pobierz_input()


