def type_write(text, delay=0.05): # - time, sys
    import time
    import sys
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def echo(text):
    print(text)

#####################__DEFAULT_LISQ_FUNCTIONALITY__#####################
#   _
# _|_  ._ ._   _|_ 
#  ||_|| || ||_||_ 
#       www.github.com/funnut

from datetime import date
from pathlib import Path
import json, os, sys, ast
import logging
import shlex
import readline

color = "\033[36m"
reset = "\033[0m"

# Konfiguracja log - logging
logging.basicConfig(
    level=logging.WARNING, # DEBUG, INFO, WARNING, ERROR, CRITICAL
    # filename="error.log",  # rm by logować na konsolę
    format="%(message)s", # %(asctime)s - %(levelname)s - 
)

# logging.disable(logging.CRITICAL)

def generate_key(save_to_file=False, confirm=False): # - getpass, base64, fernet
    # """ Tworzenie i zapis klucza """
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
                logging.error("Nieudany zapis klucza: %s",e,exc_info=True)
                return None

        return Fernet(key)

    except KeyboardInterrupt:
        logging.warning("\nPrzerwane generowanie klucza (Ctrl+C).")
        raise SystemExit
    except EOFError:
        logging.warning("\nPrzerwane generowanie klucza (Ctrl+D).")
        raise SystemExit
    except FileNotFoundError as e:
        logging.error("Nie znaleziono pliku: %s",e)
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas generowania klucza: %s",e,exc_info=True)


def encrypt(filepath, fernet=None): # - fernet, pathlib
    # """ Szyfrowanie plików """
    logging.info("encrypt (%s,%s)",filepath,fernet)
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
        logging.error("Nie znaleziono pliku: %s",e)
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas szyfrowania: %s",e,exc_info=True)


def decrypt(filepath, fernet=None): # - fernet, InvalidToken, pathlib
    # """ Odszyfrowanie plików """
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
        logging.warning("Nieprawidłowy klucz lub plik nie jest zaszyfrowany.")
    except FileNotFoundError as e:
        logging.error("Nie znaleziono pliku: %s",e)
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas odszyfrowywania: %s",e,exc_info=True)


def get(setting): # - pathlib, os, json
    # """ Pobiera i zwraca aktualne ustawienia """
    logging.info("  get(%s)",setting)
    def get_env_setting(setting="all", env_var="LISQ_SETTINGS"):
        # """Pobiera dane ze zmiennej środowiskowej"""
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
                    print(f"Katalog {path} nie istnieje. Nie zapisano.")
            d_path = Path.home() / "notesfile.txt"
            return d_path

        elif setting == "key-path":
            e_path = get_env_setting(setting)
            if e_path:
                path = Path(e_path).expanduser().with_suffix(".lisq")
                if path.parent.is_dir():
                    return path
                else:
                    print(f"Katalog '{path}' nie istnieje. Nie zapisano.")
            script_dir = Path(__file__).parent.resolve()
            d_path = script_dir / "setting.lisq"
            return d_path

        elif setting == "hist-path":
            e_path = get_env_setting(setting)
            if e_path:
                path = Path(e_path).expanduser().with_suffix(".lisq")
                if path.parent.is_dir():
                    return path
                else:
                    print(f"Katalog '{path}' nie istnieje. Nie zapisano.")
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

        elif setting == "all":
            settings = {
                "default": {
                    "notes-path": str(get("notes-path")),
                    "key-path": str(get("key-path")),
                    "hist-path": str(get("hist-path")),
                    "editor": get("editor"),
                    "encryption": get("encryption")
                    },
                "env": get_env_setting()
            }
            return settings

    except ValueError as e:
        logging.warning("%s",e)
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas pobierania danych: %s",e,exc_info=True)

def clear(args): # - os
    terminal_hight = os.get_terminal_size().lines
    print("\n"*terminal_hight*2)

def help_page(args=None):

    print(fr"""{color}# ABOUT{reset}

    From Polish "lisek / foxie" – lisq is a single file note-taking app that work with .txt files.
    Code available under a non-commercial license (see LICENSE file).
    Copyright © funnut www.github.com/funnut

{color}# CLI USAGE{reset}

    lisq [command] [arg1] [arg2] ...
    lisq add "my new note"

{color}# COMMANDS{reset}

: quit, q, exit
: c         - clear screen
: cmds      - list of available commands
:
: show, s           - show recent notes (default 10)
: show [int]        - show number of recent notes
: show [str]        - show notes containing [string]
: show all          - show all notes
: show random, r    - show a random note
:
: del [str]      - delete notes containing [string]
: del last, l    - delete the last note
: del all        - delete all notes
:
: encryption on, off or set (password is stored and not requested)
: changepass - changing password    
:
: encrypt ~/file.txt    - encrypting any file
: decrypt ~/file.txt    - decrypting any file
:
: settings    - lists all settings
: reiterate   - renumber notes' IDs
: edit        - open the notes file in set editor
:
: echo [str]    - echo given text
: type [str]    - type given text

You can add your own functions by:
    * defining them,
    * then adding to `dispatch table`.

{color}# SETTINGS{reset}

Default settings:
   * default notes path is `~/notesfile.txt`,
   * default key path is set to wherever main __file__ is,
   * default history path is set to wherever the main __file__ is,
   * default editor is set to `nano`,
   * default encryption is set to `off`.

To change it, set the following variable in your system by adding it to a startup file ~/.bashrc or ~/.zshrc.

: export LISQ_SETTINGS='{{
:     "notes-path": "~/path/notesfile.txt",
:     "key-path": "~/path/key.lisq",
:     "hist-path": "~/path/history.lisq",
:     "editor": "nano",
:     "encryption": "set"}}'

** source your startup file or restart terminal **

You can check current settings by typing `settings` (both default and env drawn from LISQ_SETTINGS var).""")


def reiterate(args=None):
    # """ Numerowanie ID notatek """
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
        logging.error("Nie znaleziono pliku: %s",e)
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas numerowania: %s",e,exc_info=True)

def delete(args):
    # """ Usuwanie notatek :
    #    - Wszystkich, pojedynczych lub ostatniej """
    logging.info("delete(%s)",args)
    try:
        if not args:
            raw = input("    ** ").strip()
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
        logging.error("Nie znaleziono notatnika: %s",e)
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas usuwania notatek: %s",e,exc_info=True)


def read_file(args): # - random, os
    # """ Odczyt pliku notatek """ 
    logging.info("read_file(%s)",args)
    terminal_width = os.get_terminal_size().columns
    print(f"{color} .id .date {'.' * (terminal_width - 12)}{reset}")
    try:
        args = args if args else ["recent"]
        found_notes = None
        with open(get("notes-path"),"r",encoding="utf-8") as f:
            lines = [linia for linia in f.readlines() if linia.strip()]
        if args[0] == "recent":
            to_show = lines[-10:]
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
            print(f"{color}{parts[0]} {date_}{reset} {" ".join(parts[2:]).strip()}")
        print('')

        if found_notes:
            print(f"Znaleziono {len(to_show)} notatek zawierających {found_args}")
            if not all(any(str(arg).lower() in line.lower() for line in lines) for arg in args) and len(found_notes) > 0:
                print(f"Nie znaleziono {not_found_args}")
        else:
            print(f"Znaleziono {len(to_show)} pasujących elementów.")

    except FileNotFoundError as e:
        logging.error("Nie znaleziono pliku: %s",e)
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas czytania danych: %s",e,exc_info=True)


def write_file(args): # - datetime
    # """ Zapisywanie notatek do pliku w ustalonym formacie """
    logging.info("write_file(%s)",args)
    try:
        if not args:
            args = input("   add / ").strip().split()
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
        except FileNotFoundError as e:
            print("Utworzono nowy notatnik.")
            id_number = 1

        id_ = f"i{str(id_number).zfill(3)}"
        date_ = date.today().strftime("%Y-%m-%d")
        with open(get("notes-path"),"a",encoding="utf-8") as f:
            f.write(f"{id_} {date_} :: {argo}\n")
        print("Notatka dodana.")

    except Exception as e:
        logging.error("Wystąpił inny błąd podczas pisania danych: %s",e,exc_info=True)


def handle_CLI(): # - ast
    # """ CLI Usage """
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
            raise ValueError(f"Nieprawidłowe polecenie: {cmd} {args if args else ''}")

    except ValueError as e:
        logging.warning("Błąd: %s",e)
    except Exception as e:
        logging.error("Wystąpił inny błąd: %s", e, exc_info=True)

    login("out")
    raise SystemExit

def changepass(args):
    # """ Nadpis pliku klucza """
    logging.info("changepass(%s)",args)
    if get("encryption"):
        generate_key(save_to_file=True, confirm=True)
    else:
        raise ValueError("Błąd: Szyfrowanie jest wyłączone")

def login(inout="in"): # - readline, pathlib
    # """ Sterowanie szyfrowaniem na wejściach i wyjściach """
    logging.info("login(%s)",inout)

    encryption = get("encryption")
    notes = get("notes-path")

    try:
        # Wyjście
        if inout == "out":
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
                raise SystemExit

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
            print("Zbyt wiele nieudanych prób. Spróbuj później.")
            raise SystemExit

        # Wejście SET
        elif encryption == "set":
            decrypt(notes)
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas login(%s): %s", inout, e, exc_info=True)

def __test_lab__(args):
    print("args:",args,"\n----\n")

#    if not args:
#        args = ['args', 2, 1, 's', [3, 4, 'dwa']]
#        print("args:",args)

    
    def norz(**args):
        print(args)

    norz(arg1=1,arg2=5.7)

    print("\n----")


# dispatch table - os
commands = {
    "cmds": lambda args: print(", ".join(commands.keys())),
    "add": write_file,
    "/": write_file,
    "show": read_file,
    "s": read_file,
    "delete": delete,
    "del": delete,
    "edit": lambda args: os.system(f"{get("editor")} {get("notes-path")}"),
    "c": clear,
    "reiterate": lambda args: reiterate("usr"),
    "encryption": lambda args: print(f"Encryption is set to: {get("encryption")}"),
    "changepass": changepass,
    "encrypt": encrypt,
    "decrypt": decrypt,
    "settings": lambda args: print(json.dumps(get("all"),indent=4)),
    "--help": help_page,
    "-help": help_page,
    "help": help_page,
    "h": help_page,
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

    histfile = get("hist-path")
    try:
        if histfile.exists():
            readline.read_history_file(histfile)
    except FileNotFoundError as e:
        logging.error("Nie znaleziono pliku: %s",e)

    readline.set_auto_history(True)
    readline.set_history_length(100)

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
            print('')
            raw = input("lisq { ").strip()

            if not raw:
                write_file(args=None)
                print('}')
                continue
            if raw.lower() in ["quit","q"]:
                logging.info("EXIT ( quit, q )")
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
                if cmd in ['c','settings']:
                    pass
                else:
                    print('}')
            else:
                raise ValueError(f"Nieprawidłowe polecenie: {cmd} {args if args else ''}")

        except ValueError as e:
            logging.warning("Błąd: %s", e)
            continue
        except KeyboardInterrupt as e:
            logging.warning("EXIT (Ctrl+C).")
            login("out")
            raise SystemExit
        except EOFError as e:
            logging.warning("EXIT (Ctrl+D).")
            login("out")
            raise SystemExit
        except Exception as e:
            logging.error("Wystąpił inny błąd: %s", e, exc_info=True)


if __name__ == "__main__":
    main()

#   _
# _|_  ._ ._   _|_ 
#  ||_|| || ||_||_ 
#       www.github.com/funnut
