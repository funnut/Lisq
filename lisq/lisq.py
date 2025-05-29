
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

from datetime import date
from pathlib import Path
import json, os, sys, ast
import logging
import shlex
import readline

# Konfiguracja log - logging
# logging.basicConfig(
#     level=logging.WARNING, # DEBUG, INFO, WARNING, ERROR, CRITICAL
#     filename="error.log",  # rm by logować na konsolę
#     format="%(asctime)s - %(levelname)s - %(message)s",
# )

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
            key_path = getting("key-path")
            try:
                with open(key_path, "wb") as f:
                    f.write(key)
                print(f"Klucz zapisany w {key_path}")
            except Exception as e:
                logging.error("Nieudany zapis klucza: %s",e,exc_info=True)
                print(f"Nie udało się zapisać klucza: {e}")
                return None

        return Fernet(key)

    except KeyboardInterrupt:
        logging.warning("Przerwane generowanie klucza (Ctrl+C).")
        print("\nPrzerwano przez użytkownika (Ctrl+C).")
        raise SystemExit
    except EOFError:
        logging.warning("Przerwane generowanie klucza (Ctrl+D).")
        print("\nPrzerwano przez użytkownika (Ctrl+D).")
        raise SystemExit
    except FileNotFoundError as e:
        logging.error("Nie znaleziono pliku: %s",e,exc_info=True)
        print(f"Błąd: Nie znaleziono pliku: {e}")
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas generowania klucza: %s",e,exc_info=True)
        print(f"Wystąpił błąd podczas generowania klucza: {e}")


def encrypt(filepath, fernet=None): # - fernet, pathlib
    # """ Szyfrowanie plików """
    logging.info("encrypt (%s,%s)",filepath,fernet)
    from cryptography.fernet import Fernet

    if not filepath:
        return
    if isinstance(filepath,list):
        if filepath[0] == "notes":
            filepath = getting("notes-path")
            fernet = generate_key(confirm=True)
            if not fernet:
                return
        else:
            filepath = Path(filepath[0]).expanduser()
            fernet = generate_key(confirm=True)
            if not fernet:
                return
    keypath = getting("key-path")
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
        logging.error("Nie znaleziono pliku: %s",e,exc_info=True)
        print(f"Błąd: Nie znaleziono pliku: {e}")
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas szyfrowania: %s",e,exc_info=True)
        print(f"Wystąpił błąd podczas szyfrowania: {e}")


def decrypt(filepath, fernet=None): # - fernet, InvalidToken, pathlib
    # """ Odszyfrowanie plików """
    logging.info("decrypt (%s,%s)",filepath,fernet)
    from cryptography.fernet import Fernet, InvalidToken

    if not filepath:
        return
    if isinstance(filepath,list):
        if filepath[0] == "notes":
            filepath = getting("notes-path")
            fernet = generate_key()
        else:
            filepath = Path(filepath[0]).expanduser()
            fernet = generate_key()

    keypath = getting("key-path")
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
        logging.warning("Nieprawidłowy token")
        print("Nieprawidłowy klucz lub plik nie jest zaszyfrowany.")
    except FileNotFoundError as e:
        logging.error("Nie znaleziono pliku: %s",e,exc_info=True)
        print(f"Błąd: Nie znaleziono pliku: {e}")
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas odszyfrowywania: %s",e,exc_info=True)
        print(f"Wystąpił błąd podczas odszyfrowywania: {e}")


def getting(key): # - pathlib, os, json
    # """ Pobiera i zwraca aktualne ustawienia """
    logging.info("  getting(%s)",key)

    def get_env_setting(key="all", env_var="LISQ_SETTINGS"):
        # """Pobiera dane ze zmiennej środowiskowej"""
        raw = os.getenv(env_var, "{}")
        try:
            settings = json.loads(raw)
        except json.JSONDecodeError:
            return None if key != "all" else {}
        if key == "all":
            return settings
        return settings.get(key)
    try:
        if key == "notes-path":
            raw_path = get_env_setting(key)
            if not raw_path:
                return Path.home() / "notesfile.txt"
            path = Path(raw_path).expanduser().with_suffix(".txt")
            if path.parent.is_dir():
                return path
            else:
                logging.warning("Katalog '%s' nie istnieje.",path)
                raise ValueError(f"Katalog {path} nie istnieje. Nie zapisano.")
        elif key == "key-path":
            raw_path = get_env_setting(key)
            if not raw_path:
                script_dir = Path(__file__).parent.resolve()
                default_p = script_dir / "key.lisq"
                return default_p
            path = Path(raw_path).expanduser().with_suffix(".lisq")
            if path.parent.is_dir():
                return path
            else:
                logging.warning("Katalog '%s' nie istnieje.",path)
                raise ValueError(f"Katalog '{path}' nie istnieje. Nie zapisano.")
        elif key == "hist-path":
            raw_path = get_env_setting(key)
            if not raw_path:
                script_dir = Path(__file__).parent.resolve()
                default_p = script_dir / "history.lisq"
                return default_p
            path = Path(raw_path).expanduser().with_suffix(".lisq")
            if path.parent.is_dir():
                return path
            else:
                logging.warning("Katalog '%s' nie istnieje.",path)
                raise ValueError(f"Katalog '{path}' nie istnieje. Nie zapisano.")
        elif key == "encryption":
            value = get_env_setting(key)
            return value.lower() if value and value.lower() in {"on", "set"} else None
        elif key == "editor":
            import shutil
            editor = get_env_setting(key)
            default_editor = "nano"
            if not editor:
                return default_editor
            if shutil.which(editor):
                return editor
            else:
                logging.warning("Edytor '%s' nie widnieje w $PATH.", editor)
                print(f"Edytor '{editor}' nie istnieje w $PATH.")
                print(f"Ustawiono domyślny: '{default_editor}'")
                return default_editor
        elif key == "all":
            settings = {
                "default": {
                    "notes-path": str(getting("notes-path")),
                    "key-path": str(getting("key-path")),
                    "hist-path": str(getting("hist-path")),
                    "editor": getting("editor"),
                    "encryption": getting("encryption")
                    },
                "env": get_env_setting()
            }
            return settings
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas pobierania danych: %s",e,exc_info=True)
        print(f"Wystąpił błąd podczas pobierania danych: {e}")

def clear(args): # - os
    terminal_hight = os.get_terminal_size().lines
    print("\n"*terminal_hight*2)

def help_page(args=None):
    print("""# ABOUT

    From Polish "lisek / foxie" – lisq is a single file note-taking app that work with .txt files.
    Code available under a non-commercial license (see LICENSE file).
    Copyright © funnut www.github.com/funnut

# CLI USAGE

    lisq [command] [arg] [arg1] [...]
    lisq add \"my new note\"

# COMMANDS

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
    * then adding to 'dispatch table'.

# SETTINGS

Default settings:
   * default notes path is ~/notesfile.txt,
   * default key path is set to wherever main __file__ is,
   * default history path is set to wherever the main __file__ is,
   * default editor is set to `nano`,
   * default encryption is set to off.

To change it, set the following variable in your system by adding it to a startup file ~/.bashrc or ~/.zshrc.

: export LISQ_SETTINGS='{
:     "notes-path": "~/path/notesfile.txt",
:     "key-path": "~/path/key.lisq",
:     "hist-path": "~/path/history.lisq",
:     "editor": "nano",
:     "encryption": "set"}'

** source your startup file or restart terminal **

You can check current settings by typing 'settings' (both default and env drawn from LISQ_SETTINGS var).""")


def reiterate(args=None):
    # """ Numerowanie ID notatek """
    logging.info("reiterate(%s)",args)
    try:
        with open(getting("notes-path"), "r", encoding="utf-8") as f:
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
            with open(getting("notes-path"),"w",encoding="utf-8") as f:
                f.writelines(new_lines)
            if args == "usr":
                print(f"Zaktualizowano identyfikatory dla {id_} linii.")
            logging.info(f"Zaktualizowano identyfikatory dla {id_} linii.")
    except FileNotFoundError as e:
        logging.error("Nie znaleziono pliku: %s",e,exc_info=True)
        print(f"Błąd: Nie znaleziono pliku: {e}")
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas numerowania: %s",e,exc_info=True)
        print(f"Wystąpił błąd podczas numerowania: {e}")


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

        with open(getting("notes-path"),"r",encoding="utf-8") as f:
            lines = f.readlines()
        if argo[0] == "all":
            yesno = input("Czy usunąć wszystkie notatki? (y/n): ").strip().lower()
            if yesno in ["yes","y",""]:
                open(getting("notes-path"),"w",encoding="utf-8").close()
                print("Usunięto.")
            else:
                print("Anulowano.")

        elif argo[0] in ["last","l"]:
            yesno = input("Czy usunąć ostatnią notatkę? (y/n): ").strip().lower()
            if yesno in ["y",""]:
                with open(getting("notes-path"),"w",encoding="utf-8") as f:
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
                    with open(getting("notes-path"),"w",encoding="utf-8") as f:
                        f.writelines(new_lines)
                    reiterate()
                    print("Usunięto.")
                else:
                    print("Anulowano.")
            else:
                print("Nie znaleziono pasujących notatek.")

    except FileNotFoundError as e:
        logging.error("Nie znaleziono notatnika: %s",e,exc_info=True)
        print(f"Błąd: Nie znaleziono pliku: {e}")
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas usuwania notatek: %s",e,exc_info=True)
        print(f"Wystąpił błąd podczas usuwania notatek: {e}")


def read_file(args): # - random, os
    # """ Odczyt pliku notatek """ 
    logging.info("read_file(%s)",args)
    terminal_width = os.get_terminal_size().columns
    print(f" .id .date {'.' * (terminal_width - 12)}")
    try:
        args = args if args else "recent"
        found_notes = None
        with open(getting("notes-path"),"r",encoding="utf-8") as f:
            lines = [linia for linia in f.readlines() if linia.strip()]
        if args == "recent":
            to_show = lines[-10:]
        elif isinstance(args[0],int):
            to_show = lines[-int(args[0]):]
        elif args[0] in ["random", "r"]:
            from random import choice
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
        logging.error("Nie znaleziono pliku: %s",e,exc_info=True)
        print(f"Błąd: Nie znaleziono pliku: {e}")
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas czytania danych: %s",e,exc_info=True)
        print(f"Wystąpił błąd podczas czytania danych: {e}")


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
            with open(getting("notes-path"),"r",encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                last_line = lines[-1]
                last_id_number = int(last_line.split()[0][1:])
                id_number = last_id_number + 1
            else:
                id_number = 1
        except FileNotFoundError as e:
            logging.warning("Nie znaleziono pliku: %s",e)
            print("Utworzono nowy notatnik.")
            id_number = 1

        id_ = f"i{str(id_number).zfill(3)}"
        date_ = date.today().strftime("%Y-%m-%d")
        with open(getting("notes-path"),"a",encoding="utf-8") as f:
            f.write(f"{id_} {date_} :: {argo}\n")
        print("Notatka dodana.")

    except Exception as e:
        logging.error("Wystąpił inny błąd podczas pisania danych: %s",e,exc_info=True)
        print(f"Wystąpił błąd podczas pisania danych: {e}")


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
        logging.warning("ValueError: %s | %s",e,sys.argv)
        print(f"Błąd: {e}")
    except Exception as e:
        logging.error("Wystąpił inny błąd: %s", e, exc_info=True)
        print(f"Wystąpił inny błąd: {e}")

    login("out")
    raise SystemExit

def changepass(args):
    # """ Nadpis pliku klucza """
    logging.info("changepass(%s)",args)
    if getting("encryption"):
        generate_key(save_to_file=True, confirm=True)
    else:
        raise ValueError("Szyfrowanie jest wyłączone")

def login(inout="in"): # - readline, pathlib
    # """ Sterowanie szyfrowaniem na wejściach i wyjściach """
    logging.info("login(%s)",inout)

    encryption = getting("encryption")
    notes = getting("notes-path")

    try:
        # Wyjście
        if inout == "out":
            histfile = getting("hist-path")
            readline.write_history_file(histfile)
            if encryption:
                encrypt(notes)
            return

        # Tworzy nowe hasło
        key = getting("key-path")
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
                    print("Nieprawidłowy token.")
            print("Zbyt wiele nieudanych prób. Spróbuj później.")
            raise SystemExit

        # Wejście SET
        elif encryption == "set":
            decrypt(notes)
    except Exception as e:
        logging.error("Wystąpił inny błąd podczas login(%s): %s", inout, e, exc_info=True)
        print(f"Wystąpił błąd podczas logowania: {e}")

def __test_lab__(args):
    print("args:",args,"\n----\n")

    if not args:
        args = ['args', 2, 1, 's', [3, 4, 'dwa']]
        print("args:",args)

    argo = []
    for el in args:
        print(type(el),el)

    print("\n----")

# dispatch table - os
commands = {
    "cmds": lambda args: print(", ".join(commands.keys())),
    "add": write_file,
    "show": read_file,
    "s": read_file,
    "delete": delete,
    "del": delete,
    "edit": lambda args: os.system(f"{getting("editor")} {getting("notes-path")}"),
    "c": clear,
    "reiterate": lambda args: reiterate("usr"),
    "encryption": lambda args: print(f"Encryption is set to: {getting("encryption")}"),
    "changepass": changepass,
    "encrypt": encrypt,
    "decrypt": decrypt,
    "settings": lambda args: print(json.dumps(getting("all"),indent=4)),
    "--help": help_page,
    "-help": help_page,
    "help": help_page,
    "h": help_page,
    "echo": lambda args: echo(" ".join(str(arg) for arg in args)),
    "type": lambda args: type_write(" ".join(args)),
    "test": __test_lab__,
}


# MAIN() - readline - random - shlex - ast - sys
def main():
    logging.info("START main()")

    login()

    if len(sys.argv) > 1:
        handle_CLI()

    histfile = getting("hist-path")
    try:
        if histfile.exists():
            readline.read_history_file(histfile)
    except FileNotFoundError as e:
        logging.error("Nie znaleziono pliku: %s",e,exc_info=True)
        print(f"Błąd: Nie znaleziono pliku: {e}")

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
            if raw in ["quit","q"]:
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
            logging.warning("ValueError: %s", e)
            print(f"Błąd: {e}")
            continue
        except KeyboardInterrupt as e:
            logging.warning("EXIT (Ctrl+C).")
            print("\nWyjście z programu (Ctrl+C).")
            login("out")
            raise SystemExit
        except EOFError as e:
            logging.warning("EXIT (Ctrl+D).")
            print("\nWyjście z programu (Ctrl+D).")
            login("out")
            raise SystemExit
        except Exception as e:
            logging.error("Wystąpił inny błąd: %s", e, exc_info=True)
            print(f"Wystąpił inny błąd: {e}")


if __name__ == "__main__":
    main()


#   _
# _|_  ._ ._   _|_ 
#  ||_|| || ||_||_ 
#       www.github.com/funnut

