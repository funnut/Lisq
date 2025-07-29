#!/usr/bin/env python

def type_write(text, delay=0.05) -> None:
    import time
    import sys
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def echo(text) -> None:
    print(text)

# # # # # # # # # # #__DEFAULT_LISQ_FUNCTIONALITY__# # # # # # # # # # #
#   _
# _|_  ._ ._   _|_
#  ||_|| || ||_||_
#       www.github.com/funnut

from datetime import datetime
from pathlib import Path
import json, os, sys, ast
import shutil
import logging
import shlex
import readline
import subprocess

# Konfiguracja log - logging
logging.basicConfig(
    level=logging.WARNING, # DEBUG, INFO, WARNING, ERROR, CRITICAL
    #filename="lisq.log",  # rm to console log
    format="%(message)s"
)
# logging.disable(logging.CRITICAL)

def generate_key(save_to_file=False, confirm=False): # - getpass, base64, fernet
    """ Tworzenie i zapis klucza """
    logging.info("generate_key(%s,%s)",save_to_file,confirm)
    from cryptography.fernet import Fernet
    import getpass
    import base64
    try:
        if confirm:
            password = getpass.getpass("Ustaw hasło: ").encode("utf-8")
            confirm = getpass.getpass("Powtórz hasło: ").encode("utf-8")
            if password != confirm:
                print("Hasła nie pasują. Spróbuj ponownie.")
                return None
        else:
            password = getpass.getpass("hasło : ").encode("utf-8")

        key = base64.urlsafe_b64encode(password.ljust(32, b'0')[:32])

        if save_to_file:
            key_path = get("key-path")
            try:
                with open(key_path, "wb") as f:
                    f.write(key)
                print(f"Klucz zapisany w {key_path}")
            except Exception as e:
                logging.error("\aNieudany zapis klucza: %s",e,exc_info=True)
                return None

        return Fernet(key)

    except KeyboardInterrupt:
        logging.warning("\n\aPrzerwane generowanie klucza (Ctrl+C).")
        raise SystemExit(1)
    except EOFError:
        logging.warning("\n\aPrzerwane generowanie klucza (Ctrl+D).")
        raise SystemExit(0)
    except FileNotFoundError as e:
        logging.error("%s",e)
    except Exception as e:
        logging.error("\aWystąpił inny błąd podczas generowania klucza: %s",e,exc_info=True)


def encrypt(filepath, fernet=None) -> None: # - fernet, pathlib
    """ Szyfrowanie plików """
    logging.info("encrypt (%s,%s)",filepath,fernet) # bez sensu
    from cryptography.fernet import Fernet

    if not filepath:
        return
    if isinstance(filepath,list):
        if filepath[0] == "notes":
            filepath = get("notes-path")
            fernet = generate_key(confirm=True)
            if not fernet:
                return
        else:
            filepath = Path(filepath[0]).expanduser()
            fernet = generate_key(confirm=True)
            if not fernet:
                return
    keypath = get("key-path")
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

    except FileNotFoundError as e:
        logging.error("\a%s",e)
    except Exception as e:
        logging.error("\aWystąpił błąd podczas szyfrowania: %s",e,exc_info=True)


def decrypt(filepath, fernet=None) -> None: # - fernet, InvalidToken, pathlib
    """ Odszyfrowanie plików """
    logging.info("decrypt (%s,%s)",filepath,fernet)
    from cryptography.fernet import Fernet, InvalidToken

    if not filepath:
        return
    if isinstance(filepath,list):
        if filepath[0] == "notes":
            filepath = get("notes-path")
            fernet = generate_key()
        else:
            filepath = Path(filepath[0]).expanduser()
            fernet = generate_key()

    keypath = get("key-path")
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

        # print("decrypted")

        return True

    except InvalidToken:
        logging.warning("\aNieprawidłowy klucz lub plik nie jest zaszyfrowany.")
    except FileNotFoundError as e:
        logging.error("\a%s",e)
    except Exception as e:
        logging.error("\aWystąpił błąd podczas odszyfrowywania: %s",e,exc_info=True)


def get(setting): # - pathlib, os, json
    """ Pobiera i zwraca aktualne ustawienia """
    logging.info("  get(%s)",setting)
    def get_env_setting(setting="all", env_var="LISQ_SETTINGS"):
        """Pobiera dane ze zmiennej środowiskowej"""
        raw = os.getenv(env_var, "{}")
        try:
            settings = json.loads(raw)
        except json.JSONDecodeError:
            return None if setting != "all" else {}
        if setting == "all":
            return settings
        return settings.get(setting)
    try:
        if setting == "notes-path":
            e_path = get_env_setting(setting)
            if e_path:
                path = Path(e_path).expanduser().with_suffix(".txt")
                if path.parent.is_dir():
                    return path
                else:
                    print(f"\aKatalog {path} nie istnieje. Nie zapisano.")
            d_path = Path.home() / "notesfile.txt"
            return d_path

        elif setting == "key-path":
            e_path = get_env_setting(setting)
            if e_path:
                path = Path(e_path).expanduser().with_suffix(".lisq")
                if path.parent.is_dir():
                    return path
                else:
                    print(f"\aKatalog '{path}' nie istnieje. Nie zapisano.")
            script_dir = Path(__file__).parent.resolve()
            d_path = script_dir / "key.lisq"
            return d_path

        elif setting == "hist-path":
            e_path = get_env_setting(setting)
            if e_path:
                path = Path(e_path).expanduser().with_suffix(".lisq")
                if path.parent.is_dir():
                    return path
                else:
                    print(f"\aKatalog '{path}' nie istnieje. Nie zapisano.")
            script_dir = Path(__file__).parent.resolve()
            d_path = script_dir / "history.lisq"
            return d_path

        elif setting == "encryption":
            value = get_env_setting(setting)
            return value.lower() if value and value.lower() in {"on", "set"} else None

        elif setting == "editor":
            import shutil
            editor = get_env_setting(setting)
            d_editor = "nano"
            if not editor:
                return d_editor
            if shutil.which(editor):
                return editor
            else:
                logging.warning("Edytor '%s' nie widnieje w $PATH.", editor)
                print(f"Ustawiono domyślny: '{d_editor}'")
                return d_editor

        elif setting == "color-accent":
            color_accent = get_env_setting(setting)
            d_color = "\033[1;32m" # default
            if color_accent:
                color_accent = color_accent.encode().decode("unicode_escape")
                return color_accent
            else:
                return d_color

        elif setting == "all":
            settings = {
                "default": {
                    "notes-path": str(get("notes-path")),
                    "key-path": str(get("key-path")),
                    "hist-path": str(get("hist-path")),
                    "editor": get("editor"),
                    "encryption": get("encryption")
                    },
                "LISQ_SETTINGS": get_env_setting()
            }
            return settings

    except ValueError as e:
        logging.warning("\a%s",e)
    except Exception as e:
        logging.error("\aWystąpił błąd podczas pobierania danych: %s",e,exc_info=True)

color = get("color-accent")
reset = "\033[0m"

histfile = get("hist-path")
try:
    if histfile.exists():
        readline.read_history_file(histfile)
except FileNotFoundError as e:
    logging.error("\a%s",e)
readline.set_auto_history(True)
readline.set_history_length(100)

def clear(args) -> None: # - os
    terminal_hight = os.get_terminal_size().lines
    print("\n"*terminal_hight*2)

def help_page(args=None) -> None:
    print(fr"""{color}# CLI USAGE{reset}

lisq [command [arg1] [arg2] ...]
lisq add "sample note"  # alternatively use / instead of add

{color}# COMMANDS{reset}

## Basic functionality:

: quit, q   # exit the program
: clear, c  # clear screen
: cmds      # list of all available commands
: edit      # open the notes file in set editor
: [--]help      # show help page
: [--]version   # show version
:
: add, / <str>  # adds a note (preferably enclosed in quotation marks)
:
: show, s   # show recent notes (default 10)
:      <int>    # show number of recent notes
:      <str>    # show notes containing <string>
:      all      # show all notes
:      random, r    # show a random note
:
: del <str>     # delete notes containing <string>
:     last, l   # delete the last note
:     all   # delete all notes

## Additional functionality:

You can encrypt your notes or any other file with a URL-safe Base64-encoded 32-byte token (*** use with caution! ***).

> This functionality requires the cryptography package. If it is not already installed via package manager, please run: pip install -r requirements.txt

: encryption on|off|set     # enables or disables login functionality; 'set' stores the token so it won't be requested again
: changepass    # changes the password (token)
:
: encrypt ~/file.txt    # encrypts any file
: decrypt ~/file.txt    # decrypts any file
:
: settings  # lists all settings
: reiterate     # renumber notes' IDs
: echo <str>    # prints the given text
: type <str>    # types the given text

You can add your own functions by:
  + defining them,
  + then adding to *dispatch table*.

{color}# SETTINGS{reset}

Default settings are:
  + default notes path is `~/notesfile.txt`,
  + default key path is set to wherever main __file__ is,
  + default history path is set to wherever the main __file__ is,
  + default color accent is green,
  + default editor is set to `nano`,
  + default encryption is set to `off`.

To change it, set the following variable in your system by adding it to a startup file (eg. ~/.bashrc).

export LISQ_SETTINGS='{{
    "notes-path": "~/path/notesfile.txt",
    "key-path": "~/path/key.lisq",
    "hist-path": "~/path/history.lisq",
    "color-accent": "\\033[34m",
    "editor": "nano",
    "encryption": "set"
    }}'

> Source your startup file or restart terminal.

You can check current settings by typing `settings` (both default and environmental drawn from LISQ_SETTINGS var).""")

def reiterate(args=None) -> None:
    """ Numerowanie ID notatek """
    logging.info("reiterate(%s)",args)
    try:
        with open(get("notes-path"), "r", encoding="utf-8") as f:
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
            with open(get("notes-path"),"w",encoding="utf-8") as f:
                f.writelines(new_lines)
            if args == "usr":
                print(f"Zaktualizowano identyfikatory dla {id_} linii.")
            logging.info(f"Zaktualizowano identyfikatory dla {id_} linii.")

    except FileNotFoundError as e:
        logging.error("\a%s",e)
    except Exception as e:
        logging.error("\aWystąpił błąd podczas numerowania: %s",e,exc_info=True)

def delete(args) -> None:
    """ Usuwanie notatek :
        - Wszystkich, pojedynczych lub ostatniej """
    logging.info("delete(%s)",args)
    try:
        if not args:
            raw = input("DEL: ").strip()
            if raw in ["q",""]:
                return

            if ' ' in raw:
                args = raw.split()
            else:
                args = [raw]

        argo = []
        for el in args:
            argo.append(str(el))

        with open(get("notes-path"),"r",encoding="utf-8") as f:
            lines = f.readlines()
        if argo[0] == "all":
            yesno = input("Czy usunąć wszystkie notatki? (y/n): ").strip().lower()
            if yesno in ["yes","y",""]:
                open(get("notes-path"),"w",encoding="utf-8").close()
                print("Usunięto.")
            else:
                print("Anulowano.")

        elif argo[0] in ["last","l"]:
            yesno = input("Czy usunąć ostatnią notatkę? (y/n): ").strip().lower()
            if yesno in ["y",""]:
                with open(get("notes-path"),"w",encoding="utf-8") as f:
                    f.writelines(lines[:-1])
                print("Usunięto.")
            else:
                print("Anulowano.")
        else:
            new_lines = [line for line in lines if not any(el in line for el in argo)]
            found = [arg for arg in argo if any(arg in line for line in lines)]
            number = len(lines)-len(new_lines)
            if not all(any(arg in line for line in lines) for arg in argo) and number:
                print("Nie wszystkie elementy zostały znalezione.")
            if number > 0:
                yesno = input(f"Czy usunąć {number} notatki zawierające {found}? (y/n): ").strip().lower()
                if yesno in ["yes","y",""]:
                    with open(get("notes-path"),"w",encoding="utf-8") as f:
                        f.writelines(new_lines)
                    reiterate()
                    print("Usunięto.")
                else:
                    print("Anulowano.")
            else:
                print("Nie znaleziono pasujących notatek.")

    except FileNotFoundError as e:
        logging.error("\a%s",e)
    except Exception as e:
        logging.error("\aWystąpił błąd podczas usuwania notatek: %s",e,exc_info=True)


def read_file(args) -> None: # - random, os
    """ Odczyt pliku notatek """
    logging.info("read_file(%s)",args)
    terminal_width = shutil.get_terminal_size().columns
    print(f" .id .date {'.' * (terminal_width - 12)}")
    try:
        args = args if args else ["recent"]
        found_notes = None
        with open(get("notes-path"),"r",encoding="utf-8") as f:
            lines = [linia for linia in f.readlines() if linia.strip()]
        if args[0] == "recent":
            to_show = lines[-10:] # Default for `show` command
        elif isinstance(args[0],int):
            to_show = lines[-int(args[0]):]
        elif args[0] in ["random", "r"]:
            from random import choice
            to_show = [choice(lines)]
        elif args[0] == "all":
            to_show = lines
        else:
            found_notes = [line for line in lines if any(str(arg).lower() in line.lower() for arg in args)]
            found_args = [str(arg).lower() for arg in args if any(str(arg).lower() in line.lower() for line in lines)]
            not_found_args = [str(arg).lower() for arg in args if not any(str(arg).lower() in line.lower() for line in lines)]
            if not found_notes:
                print("Nie znaleziono pasujących elementów.")
                return
            else:
                to_show = found_notes
        for line in to_show:
            parts = line.split()
            date_ = "-".join(parts[1].split("-")[1:])
            print(f"{parts[0]} {date_} {color}{" ".join(parts[2:]).strip()}{reset}")
        print('')

        if found_notes:
            print(f"Znaleziono {len(to_show)} notatek zawierających {found_args}")
            if not all(any(str(arg).lower() in line.lower() for line in lines) for arg in args) and len(found_notes) > 0:
                print(f"Nie znaleziono {not_found_args}")
        else:
            print(f"Znaleziono {len(to_show)} pasujących elementów.")

    except FileNotFoundError as e:
        logging.error("\a%s",e)
    except Exception as e:
        logging.error("\aWystąpił błąd podczas czytania danych: %s",e,exc_info=True)


def write_file(args) -> None: # - datetime
    """ Zapisywanie notatek do pliku w ustalonym formacie """
    logging.info("write_file(%s)",args)
    try:
        if not args:
            args = input("ADD: ").strip().split()
            if not args:
                return

        argo = []
        for el in args:
            el = " ".join(str(el).strip().split("\n"))
            if el:
                argo.append(el)

        argo = " ".join(argo)

        try:
            with open(get("notes-path"),"r",encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                last_line = lines[-1]
                last_id_number = int(last_line.split()[0][1:])
                id_number = last_id_number + 1
            else:
                id_number = 1
        except FileNotFoundError:
            print("Utworzono nowy notatnik.")
            id_number = 1

        id_ = f"i{str(id_number).zfill(3)}"
        date_ = datetime.now().strftime("%Y-%m-%d")
        with open(get("notes-path"),"a",encoding="utf-8") as f:
            f.write(f"{id_} {date_} :: {argo}\n")
        print("Notatka dodana.")

    except Exception as e:
        logging.error("\aWystąpił błąd podczas pisania danych: %s",e,exc_info=True)


def handle_CLI() -> None: # - ast
    """ CLI Usage """
    logging.info("handle_CLI(%s)",sys.argv)

    try:
        cmd = sys.argv[1].lower()
        argo = sys.argv[2:]

        args = []
        for arg in argo:
            try:
                val = ast.literal_eval(arg)
            except (ValueError, SyntaxError):
                val = arg
            args.append(val)

        if cmd in commands:
            commands[cmd](args)
        else:
            raise ValueError(f"\aInvalid command: {cmd} {args if args else ''}")

    except ValueError as e:
        logging.warning("\a%s",e)
    except Exception as e:
        logging.error("\aWystąpił błąd: %s", e, exc_info=True)

    login("out")
    raise SystemExit(0)

def changepass(args) -> None:
    """ Nadpis pliku klucza """
    logging.info("changepass(%s)",args)
    if get("encryption"):
        generate_key(save_to_file=True, confirm=True)
    else:
        raise ValueError("\aBłąd: Szyfrowanie jest wyłączone")

def login(mod="in"): # - readline, pathlib
    """ Sterowanie szyfrowaniem na wejściach i wyjściach """
    logging.info("login(%s)",mod)

    encryption = get("encryption")
    notes = get("notes-path")

    try:
        # Wyjście
        if mod == "out":
            histfile = get("hist-path")
            readline.write_history_file(histfile)
            if encryption:
                encrypt(notes)
            return

        # Tworzy nowe hasło
        key = get("key-path")
        if encryption and not key.exists():
            result = generate_key(save_to_file=True, confirm=True)
            if not result:
                raise SystemExit(1)

        # Wejście OFF
        elif not encryption and key.exists():
            decrypt(notes)
            key.unlink()
            logging.info(" usunięto klucz")
            return

        # Wejście ON
        elif encryption == "on":
            for attemt in range(3):
                fernet = generate_key()
                try:
                    result = decrypt(notes,fernet)
                    if result:
                        return
                except ValueError:
                    print("Błąd: Nieprawidłowy token")
            print("\aZbyt wiele nieudanych prób. Spróbuj później.")
            raise SystemExit(0)

        # Wejście SET
        elif encryption == "set":
            decrypt(notes)
    except Exception as e:
        logging.error("\aWystąpił błąd podczas login(%s): %s", mod, e, exc_info=True)

def __test_lab__(args):
    print("args:",args,"\n----\n")

    if not args or args[0] not in ['on','off']:
        print("Give arg on|off")
        return
    else:
        result = subprocess.run(["termux-torch", args[0]])
        print(result)


# dispatch table - os
commands = {
    "cmds": lambda args: print(", ".join(commands.keys())),
    "add": write_file,
    "/": write_file,
    "show": read_file,
    "s": read_file,
    "delete": delete,
    "del": delete,
    "edit": lambda args: subprocess.run([get("editor"),get("notes-path")]),
    "clear": clear,
    "c": clear,
    "reiterate": lambda args: reiterate("usr"),
    "encryption": lambda args: print(f"Encryption is set to: {get("encryption")}"),
    "changepass": changepass,
    "encrypt": encrypt,
    "decrypt": decrypt,
    "settings": lambda args: print(json.dumps(get("all"),indent=4)),
    "--help": help_page,
    "help": help_page,
    "--version": lambda args: print("v2025.6.1-1"),
    "version": lambda args: print("v2025.6.1-1"),
    "echo": lambda args: echo(" ".join(str(arg) for arg in args)),
    "type": lambda args: type_write(" ".join(str(arg) for arg in args)),
    "test": __test_lab__,
}


# MAIN() - readline - random - shlex - ast - sys
def main():
    logging.info("START main()")

    login()

    if len(sys.argv) > 1:
        handle_CLI()

    now = datetime.now().strftime("%H:%M %b %d")
    print(r""" ___      ___   _______  _______
|   |    |   | |       ||       |
|   |    |   | |  _____||   _   |
|   |    |   | | |_____ |  | |  |
|   |___ |   | |_____  ||  |_|  |
|       ||   |  _____| ||      |
|_______||___| |_______||____||_|""")
    print(f"       cmds - help - {now}")

    while True:
        logging.info("START while True")
        try:
            raw = input("> ").strip()

            if not raw:
                write_file(args=None)
                continue
            if raw.lower() in ["quit","q"]:
                logging.info("EXIT (quit, q)")
                login("out")
                return

            parts = shlex.split(raw)
            cmd = parts[0].lower()
            argo = parts[1:]

            args = []
            for arg in argo:
                try:
                    val = ast.literal_eval(arg)
                except (ValueError, SyntaxError):
                    val = arg
                args.append(val)

            if cmd in commands:
                commands[cmd](args)
            else:
                raise ValueError(f"\aInvalid command: {cmd} {args if args else ''}")

        except ValueError as e:
            logging.warning("%s", e)
            continue
        except KeyboardInterrupt:
            logging.warning("EXIT (Ctrl+C)\n")
            login("out")
            raise SystemExit(1)
        except EOFError:
            print("EXIT (Ctrl+D)\n")
            login("out")
            raise SystemExit(0)
        except Exception as e:
            logging.error("\aWystąpił błąd: %s", e, exc_info=True)


if __name__ == "__main__":
    main()


#   _
# _|_  ._ ._   _|_
#  ||_|| || ||_||_
#       www.github.com/funnut
