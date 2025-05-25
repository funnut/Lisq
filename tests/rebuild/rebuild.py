import logging
import readline
import os, sys
from pathlib import Path

# Konfiguracja log - logging
logging.basicConfig(
    level=logging.DEBUG, # DEBUG, INFO, WARNING, ERROR, CRITICAL
    filename="debug.log",  # rm by logować na konsolę
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Historia poleceń - readline, pathlib
script_dir = Path(__file__).parent.resolve()
histfile = script_dir / "history.lisq"
if histfile.exists():
    readline.read_history_file(histfile)
readline.set_history_length(100)

def type_write(text, delay=0.05):
    import time
    import sys
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def spinner(args=None):
    import itertools
    import sys
    import time
    spinner = itertools.cycle(['-', '/', '|', '\\'])
    for _ in range(20):
        sys.stdout.write('\r'+next(spinner))
        sys.stdout.flush()
        time.sleep(0.2)

def generate_key(save_to_file=False, confirm_pass=False):
    import getpass
    import base64
    from cryptography.fernet import Fernet

    if confirm_pass:
        password = getpass.getpass("Ustaw hasło: ").encode("utf-8")
        confirm = getpass.getpass("Powtórz hasło: ").encode("utf-8")
        if password != confirm:
            print("Hasła nie pasują. Spróbuj ponownie.")
            return None
    else:
        password = getpass.getpass("hasło : ").encode("utf-8")

    key = base64.urlsafe_b64encode(password.ljust(32, b'0')[:32])

    if save_to_file:
        key_path = GET_SETTING("keypath")
        try:
            with open(key_path, "wb") as f:
                f.write(key)
            print(f"Klucz zapisany w {key_path}")
        except Exception as e:
            print(f"Nie udało się zapisać klucza: {e}")
            return None

    return Fernet(key)

def encrypt(filepath, fernet=None):
    from cryptography.fernet import Fernet

    if not filepath:
        return
    if filepath[0] == "notespath":
        filepath = GET_SETTING("notespath")
        fernet = generate_key(confirm_pass=True)
        if not fernet:
            return
    else:
        filepath = Path(filepath[0]).expanduser()
        fernet = generate_key(confirm_pass=True)
        if not fernet:
            return

    keypath = GET_SETTING("keypath")
    try:
        if fernet:
            pass
        else:
            if not keypath.exists():
                generate_key(save_to_file=True)
            with open(keypath, "rb") as f:
                key = f.read()
            fernet = Fernet(key)

        with open(filepath,"r", encoding="utf-8") as f:
            plaintext = f.read().encode("utf-8")

        encrypted = fernet.encrypt(plaintext)

        with open(filepath,"wb") as f:
            f.write(encrypted)

        print("encrypted")

    except Exception as e:
        raise Exception(f"Błąd podczas szyfrowania: {e!r} {e}")


def decrypt(filepath, fernet=None):
    from cryptography.fernet import Fernet, InvalidToken

    if not filepath:
        return
    if filepath[0] == "notespath":
        filepath = GET_SETTING("notespath")
        fernet = generate_key() # nie tworzy nowego key.lisq
    else:
        filepath = Path(filepath[0]).expanduser()
        fernet = generate_key()

    keypath = GET_SETTING("keypath")
    try:
        if fernet:
            pass
        else:
            if not keypath.exists():
                generate_key(save_to_file=True)
            with open(keypath,'rb') as f:
                key = f.read()
            fernet = Fernet(key)

        with open(filepath,'rb') as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted).decode('utf-8')

        with open(filepath,'w',encoding='utf-8') as f:
            f.write(decrypted)

        print("decrypted")
        return True

    except InvalidToken:
        raise ValueError("Nieprawidłowy klucz lub plik nie jest zaszyfrowany.")
    except Exception as e:
        raise Exception(f"Błąd podczas odszyfrowania: {e!r} {e}")

def GET_SETTING(key): # - pathlib, os
    if key == "notespath":
        raw_path = GET_ENV_SETTING(key)
        if raw_path:
            return Path(raw_path).expanduser()
        else:
            return Path.home() / "yournotes.txt"
    elif key == "keypath":
        raw_path = GET_ENV_SETTING(key)
        if raw_path:
            return Path(raw_path).expanduser()
        else:
            script_dir = Path(__file__).parent.resolve()
            keyfile = script_dir / "key.lisq"
            return keyfile
    elif key == "encryption": # czy uzywać tego?
        value = GET_ENV_SETTING(key)
        return value


def GET_ENV_SETTING(key=None): # - shutil, os
    """Pobiera info ze zmiennej środowiskowej."""
    logging.info("Start GET_ENV_SETTING(%s)",key)
    import os
    import shutil
    settings_env = os.getenv("LISQ_SETTINGS")
    if not settings_env:
        logging.error("Zmienna środowiskowa nie została znaleziona")
        print("Błąd: Zmienna środowiskowa 'LISQ_SETTINGS' nie istnieje.")
        return None

    settings = settings_env.split("--")
    setting = [s for s in settings if key in s]
    
    if not setting:
        logging.info("Ustawienie '%s' nie zostało znalezione",key)
        return None
    try:
        value = setting[0].split("=")[1].strip().strip("'").strip('"')
    except IndexError:
        logging.error("IndexError: nieprawidłowy format: %s",setting[0])
        print(f"Błąd: Nieprawidłowy format ustawienia: {setting[0]}")
        return None

    logging.debug("Zmienna value=%s",value,exc_info=True)
    
    if key == "editor":
        if shutil.which(value):
            return value
        else:
            logging.error("Edytor '%s' nie widnieje w $PATH.",value)
            print(f"Błąd: '{value}' nie istnieje w $PATH. Nie zapisano.")
            return None
    elif key == "notespath":
        return value
    elif key == "encryption":
        return value.lower() if value.lower() in ["set","on"] else None
    else:
        logging.error("Nieznane ustawienie: %s",key)
        print(f"Błąd: Nieznane ustawienie: {key}")
        return None

def clear(args): # - os
    terminal_hight = os.get_terminal_size().lines
    print("\n"*terminal_hight*2)

def help_page(args=None):
    print("""# About    
    From Polish "lisek / foxie" – lisq is a single file note-taking app that work with .txt files.
    Code available under a non-commercial license (see LICENSE file).
    Copyright © funnut https://github.com/funnut

# Commands
: quit, q, exit
: clear, c        - clear screen
:
: show, s         - show recent notes (default 10)
: show [int]      - show number of recent notes
: show [str]      - show notes containing [string]
: show all        - show all notes
: show random, r  - show a random note
:
: del [str]      - delete notes containing [string]
: del last, l    - delete the last note
: del all        - delete all notes

# CLI Usage
    lisq [command] [arg0] [arg1] ...
    lisq add \"my new note\"""")

def reiterate(args=None):
    """Reiteruje ID notatek"""
    logging.info("Start reiterate()")
    try:
        with open(GET_SETTING("notespath"), "r", encoding="utf-8") as f:
            lines = f.readlines()
            id_ = 0
            new_lines = []
            for line in lines:
                id_ += 1
                parts = line.strip().split()
                if not parts:
                    continue
                new_id = f"i{str(id_).zfill(3)}"
                new_line = f"{new_id} {' '.join(parts[1:])}\n"
                new_lines.append(new_line)
            with open(GET_SETTING("notespath"),"w",encoding="utf-8") as f:
                f.writelines(new_lines)
            if not args:
                print(f"Zaktualizowano identyfikatory dla {id_} linii.")
            logging.info(f"Zaktualizowano identyfikatory dla {id_} linii.")
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError w reiterate()\n%s",e)
        print(f"{GET_SETTING("notespath")}\n\nBłąd: Nie znaleziono notatnika")
    except Exception as e:
        logging.error(f"Exception w reiterate({args})\n%s",e,exc_info=True)
        print(f"Wystąpił inny błąd: {e}")

def delete(args):
    """Usuwanie notatek."""
    logging.info(f"Start delete({args}){len(args)}")
    try:
        while not args:
            raw = input(" - ").strip()
            if raw in ["q",""]:
                return
            if ' ' in raw:
                args = raw.split()
            else:
                args = [raw]

        with open(GET_SETTING("notespath"),"r",encoding="utf-8") as f:
            lines = f.readlines()
        if args[0] == "all": # all
            yesno = input("Czy usunąć wszystkie notatki? (y/n): ").strip().lower()
            if yesno in ["yes","y",""]:
                open(GET_SETTING("notespath"),"w",encoding="utf-8").close()
                print("Usunięto.")
            else:
                print("Anulowano.")

        elif args[0] in ["last","l"]: # last
            yesno = input("Czy usunąć ostatnią notatkę? (y/n): ").strip().lower()
            if yesno in ["y",""]:
                with open(GET_SETTING("notespath"),"w",encoding="utf-8") as f:
                    f.writelines(lines[:-1])
                print("Usunięto.")
            else:
                print("Anulowano.")
        else:
            new_lines = [line for line in lines if not any(el in line for el in args)]
            found = [arg for arg in args if any(arg in line for line in lines)]
            number = len(lines)-len(new_lines)
            if not all(any(arg in line for line in lines) for arg in args) and number:
                print("Nie wszystkie elementy zostały znalezione.")
            if number > 0:
                yesno = input(f"Czy usunąć {number} notatki zawierające {found}? (y/n): ").strip().lower()
                if yesno in ["yes","y",""]:
                    with open(GET_SETTING("notespath"),"w",encoding="utf-8") as f:
                        f.writelines(new_lines)
                    reiterate(True)
                    print("Usunięto.")
                else:
                    print("Anulowano.")
            else:
                print("Nie znaleziono pasujących notatek.")

    except FileNotFoundError as e:
        logging.error("FileNotFoundError w delete()\n%s",e)
        print(f"{GET_SETTING("notespath")}\n\nBłąd: Nie znaleziono notatnika")
    except Exception as e:
        logging.error(f"Exception w delete({args})\n%s",e,exc_info=True)
        print(f"Wystąpił inny błąd: ",e)

def read_file(args):
    """Odczyt pliku notatek""" # - random, os
    logging.info(f"Start read_file({args})")
    from random import choice
    terminal_width = os.get_terminal_size().columns
    print(f" .id .date {'.' * (terminal_width - 12)}")
    try:
        args = args if args else "recent"
        found_notes = None
        with open(GET_SETTING("notespath"),"r",encoding="utf-8") as f:
            lines = [linia for linia in f.readlines() if linia.strip()]
        if args == "recent":
            to_show = lines[-10:]
        elif args[0].isdigit():
            to_show = lines[-int(args[0]):]
        elif args[0] in ["random", "r"]:
            to_show = [choice(lines)]
        elif args[0] == "all":
            to_show = lines
        else:
            found_notes = [line for line in lines if any(arg.lower() in line.lower() for arg in args)]
            found_args = [arg.lower() for arg in args if any(arg.lower() in line.lower() for line in lines)]
            not_found_args = [arg.lower() for arg in args if not any(arg.lower() in line.lower() for line in lines)]
            if not found_notes:
                print("Nie znaleziono pasujących elementów.")
                return
            else:
                to_show = found_notes

        for line in to_show:
            parts = line.split()
            date_ = "-".join(parts[1].split("-")[1:])
            print(f"{parts[0]} {date_} {" ".join(parts[2:]).strip()}")
        print('')

        if found_notes:
            print(f"Znaleziono {len(to_show)} notatek zawierających {found_args}")
            if not all(any(arg.lower() in line.lower() for line in lines) for arg in args) and len(found_notes) > 0:
                print(f"Nie znaleziono {not_found_args}")
        else:
            print(f"Znaleziono {len(to_show)} pasujących elementów.")

    except FileNotFoundError as e:
        logging.error("FileNotFoundError w read_file()\n%s",e)
        print(f"{GET_SETTING("notespath")}\n\nBłąd: Nie znaleziono notatnika")
    except Exception as e:
        logging.error(f"Exception w read_file({args})\n%s",e,exc_info=True)
        print(f"Wystąpił inny błąd: {e}")

def write_file(args): # - datetime
    """Zapisywanie notatek do pliku w ustalonym formacie."""
    from datetime import date
    logging.info(f"Start write_file({args})")
    try:
        if not args:
            args = input(" : ").strip().split()
            if not args:
                return
        if len(args) > 1:
            args = [" ".join(args)]
        for element in args:
            args = [" ".join(element.split("\n"))]
        try:
            with open(GET_SETTING("notespath"),"r",encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                last_line = lines[-1]
                last_id_number = int(last_line.split()[0][1:])
                id_number = last_id_number + 1
            else:
                id_number = 1
        except FileNotFoundError as e:
            logging.error("FileNotFoundError w write_file()\n%s",e)
            print("Utworzono nowy notatnik.")
            id_number = 1

        id_ = f"i{str(id_number).zfill(3)}"
        date_ = date.today().strftime("%Y-%m-%d")
        with open(GET_SETTING("notespath"),"a",encoding="utf-8") as f:
            f.write(f"{id_} {date_} :: {' '.join(args)}\n")
        print("Notatka dodana.")
    except Exception as e:
        logging.error(f"Exception w write_file({args})\n%s",e,exc_info=True)
        print(f"Wystąpił inny błąd: {e}")

def echo(text):
    print(text)

def _test(args):
    print("args:",args)

    setting = GET_ENV_SETTING(args[0])
    print(setting)

# dispatch table
commands = {
    "cmds": lambda args: print(", ".join(commands.keys())),
    "add": write_file,
    "show": read_file,
    "s": read_file,
    "delete": delete,
    "del": delete,
    "edit": lambda args: os.system(f"{GET_ENV_SETTING("editor")} {GET_SETTING("notespath")}"), # env
    "c": clear,
    "reiterate": reiterate,
    "help": help_page,
    "echo": lambda args: echo(" ".join(args)),
    "type": lambda args: type_write(" ".join(args)),
    "spinner": spinner,
    "test": _test,
    "encrypt": encrypt,
    "decrypt": decrypt,
    "encryption": lambda args: print(f"Encryption is set to: {GET_ENV_SETTING("encryption")}"),
}

def main(): # - sys, random
    logging.info("START FUNKCJI main()")
    if len(sys.argv) > 1:
        """CLI Usage"""
        logging.info(f"Start if sys.argv({sys.argv})")
        cmd = sys.argv[1].lower()
        args = sys.argv[2:]

        if cmd in commands:
            try:
                commands[cmd](args)
                
            except ValueError as e:
                logging.error("ValueError w komendzie CLI: %s", e)
                print(f"Błąd: {e}")
            except Exception as e:
                logging.error("Nieoczekiwany błąd w komendzie CLI: %s", e, exc_info=True)
                print(f"Inny błąd: {e}")
        else:
            logging.error(f"Nieprawidłowe polecenie: sys.argv={sys.argv}")
            print("Błąd: Nieprawidłowe polecenie.")
        return

    from random import randrange
    print(fr"""
 _ _
| (_)___  __ _
| | / __|/ _` |
| | \__ \ (_| |
|_|_|___/\__, |
 cmds - help|_|{randrange(0,1000)}""")

    while True:
        logging.info("START GŁÓWNEJ PĘTLI")
        try:
            raw = input(f"> ").strip()
            if not raw:
                write_file(args=None)
                continue
            if raw in ["quit","q"]:
                logging.info("WYJŚCIE Z PROGRAMU ( quit, q )")
                readline.write_history_file(histfile)
                return

            parts = raw.split()
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in commands:
                commands[cmd](args)
            else:
                raise ValueError(f"Nieprawidłowe polecenie: {cmd} {args}")

        except ValueError as e:
            logging.error("ValueError: %s", e)
            print(f"Błąd: {e}")
            continue
        except KeyboardInterrupt as e:
            logging.error("Odebrano KeyboardInterrupt: %s", e, exc_info=True)
            print("Błąd: KeyboardInterrupt")
            return
        except EOFError as e:
            logging.info("WYJŚCIE Z PROGRAMU - EOFError", exc_info=False)
            readline.write_history_file(histfile)
            print('')
            return
        except Exception as e:
            logging.error("Inny błąd: %s", e, exc_info=True)
            print(f"Inny błąd: {e}")


if __name__ == "__main__":
    main()

#   _
# _|_  ._ ._   _|_ 
#  ||_|| || ||_||_ 
#       www.github.com/funnut

