import logging
import readline
import os, sys
from pathlib import Path

# Konfiguracja log - logging
logging.basicConfig(
    level=logging.ERROR, # DEBUG, INFO, WARNING, ERROR, CRITICAL
    filename="debug.log",  # rm by logować na konsolę
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Historia poleceń - readline, pathlib
script_dir = Path(__file__).parent.resolve()
histfile = script_dir / "_history"
if histfile.exists():
    readline.read_history_file(histfile)
readline.set_history_length(100)

def type(text, delay=0.05):
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

def NOTES_PATH(): # - pathlib, os
    path = Path("~/_lisq/tests/rebuild/").expanduser() / "notes.txt"
    if path:
        return path
    env_path = os.getenv("NOTES_PATH")
    if env_path:
        return Path(os.path.expandvars(env_path)).expanduser()
    return Path.home() / "notes.txt"

def clear(args): # - os
    terminal_hight = os.get_terminal_size().lines
    print("\n"*terminal_hight*2)

def reiterate(args=None):
    logging.info("Start reiterate()")
    try:
        with open(NOTES_PATH(), "r", encoding="utf-8") as f:
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
            with open(NOTES_PATH(),"w",encoding="utf-8") as f:
                f.writelines(new_lines)
            if not args:
                print (f"Zaktualizowano identyfikatory dla {id_} linii.")
            logging.info(f"Zaktualizowano identyfikatory dla {id_} linii.")
    except FileNotFoundError as e:
        logging.error(f"FileNotFoundError w reiterate()\n%s",e)
        print (f"{NOTES_PATH()}\n\nBłąd: Nie znaleziono notatnika")

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

        with open(NOTES_PATH(),"r",encoding="utf-8") as f:
            lines = f.readlines()
        if args[0] == "all": # all
            yesno = input("Czy usunąć wszystkie notatki? (y/n): ").strip().lower()
            if yesno in ["yes","y",""]:
                open(NOTES_PATH(),"w",encoding="utf-8").close()
                print ("Usunięto.")
            else:
                print ("Anulowano.")
        elif args[0] in ["last","l"]: # last
            yesno = input("Czy usunąć ostatnią notatkę? (y/n): ").strip().lower()
            if yesno in ["y",""]:
                with open(NOTES_PATH(),"w",encoding="utf-8") as f:
                    f.writelines(lines[:-1])
                print ("Usunięto.")
            else:
                print ("Anulowano.")
        else:
            new_lines = [line for line in lines if not any(el in line for el in args)]
            found = [arg for arg in args if any(arg in line for line in lines)]
            number = len(lines)-len(new_lines)
            if not all(any(arg in line for line in lines) for arg in args) and number:
                print ("Nie wszystkie elementy zostały znalezione.")
            if number > 0:
                yesno = input(f"Czy usunąć {number} notatki zawierające {found}? (y/n): ").strip().lower()
                if yesno in ["yes","y",""]:
                    with open(NOTES_PATH(),"w",encoding="utf-8") as f:
                        f.writelines(new_lines)
                    reiterate(True)
                    print ("Usunięto.")
                else:
                    print ("Anulowano.")
            else:
                print ("Nie znaleziono pasujących notatek.")

    except FileNotFoundError as e:
        logging.error("FileNotFoundError w delete()\n%s",e)
        print (f"{NOTES_PATH()}\n\nBłąd: Nie znaleziono notatnika")
    except Exception as e:
        logging.error("Exception w delete()\n%s",e)
        print (f"Wystąpił inny błąd: ",e)

def read_file(args):
    """Odczyt pliku notatek""" # - random, os
    logging.info(f"Start read_file({args})")
    from random import choice
    terminal_width = os.get_terminal_size().columns
    print (f" _id _date {'_' * (terminal_width - 12)}")
    try:
        arg = args[0] if args else 'recent'
        logging.debug(f"arg: {arg}")
        with open(NOTES_PATH(),"r",encoding="utf-8") as f:
            lines = [linia for linia in f.readlines() if linia.strip()]
        if arg == "recent":
            to_show = lines[-10:]
        elif arg.isdigit():
            to_show = lines[-int(arg):]
        elif arg in ["random", "r"]:
            to_show = [choice(lines)]
        elif arg == "all":
            to_show = lines
        else:
            found = [line for line in lines if arg.lower() in line.lower()]
            if not found:
                print ("Nie znaleziono pasujących elementów.")
                return
            else:
                to_show = found

        for line in to_show:
            parts = line.split()
            date_ = "-".join(parts[1].split("-")[1:])
            print (f"{parts[0]} {date_} {" ".join(parts[2:]).strip()}")

        print (f"\nZnaleziono {len(to_show)} pasujących elementów.")

    except FileNotFoundError as e:
        logging.error("FileNotFoundError w read_file()\n%s",e)
        print (f"{NOTES_PATH()}\n\nBłąd: Nie znaleziono notatnika")
    except Exception as e:
        logging.error("Exception w read_file()\n%s",e)
        print (f"Wystąpił inny błąd: {e}")

def write_file(args): # - datetime
    """Zapisywanie notatek do pliku w ustalonym formacie."""
    from datetime import date
    logging.info(f"Start write_file({args})")
    try:
        if not args:
            args = input(" : ").strip().split()
            if not args:
                return
        try:
            with open(NOTES_PATH(),"r",encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                last_line = lines[-1]
                last_id_number = int(last_line.split()[0][1:])
                id_number = last_id_number + 1
            else:
                id_number = 1
        except FileNotFoundError as e:
            logging.error("FileNotFoundError w write_file()\n%s",e)
            print ("Utworzono nowy notatnik.")
            id_number = 1
        id_ = f"i{str(id_number).zfill(3)}"
        date_ = date.today().strftime("%Y-%m-%d")
        with open(NOTES_PATH(),"a",encoding="utf-8") as f:
            f.write(f"{id_} {date_} :: {' '.join(args)}\n") # args to lista!
        print ("Notatka dodana.")
    except Exception as e:
        logging.error("Exception w write_file()\n%s",e)
        print (f"Wystąpił inny błąd: {e}")

def echo(text):
    print(text)

def _test(args):
    print("args:",args)

# dispatch table
commands = {
    "cmds": lambda args: print(", ".join(commands.keys())),
    "edit": lambda args: os.system(f"nano {NOTES_PATH()}"),
    "echo": lambda args: echo(" ".join(args)),
    "type": lambda args: type(" ".join(args)),
    "test": _test,
    "add": write_file,
    "show": read_file,
    "s": read_file,
    "del": delete,
    "delete": delete,
    "c": clear,
    "reiterate": reiterate,
    "spinner": spinner,
}

def main(): # - sys
    logging.info("START FUNKCJI main()")
    if len(sys.argv) > 1:
        """Obsługa CLI"""
        logging.info(f"Start if sys.argv({sys.argv})")
        cmd = sys.argv[1]
        args = sys.argv[2:]
        if cmd in commands:
            commands[cmd](args)
        else:
            print("Nieprawidłowe polecenie.")
        return

    while True:
        logging.debug("START GŁÓWNEJ PĘTLI")
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
                raise ValueError(f"Nieprawidłowe polecenie: {cmd} {' '.join(args) if args else ''}")

        except ValueError as e:
            logging.info("ValueError: %s", e, exc_info=True)
            print ("Nieprawidłowe polecenie.")
        except KeyboardInterrupt as e:
            logging.error("Odebrano KeyboardInterrupt: %s", e, exc_info=True)
            print ("Błąd: KeyboardInterrupt")
            return
        except EOFError as e:
            logging.info("WYJŚCIE Z PROGRAMU - EOFError", exc_info=False)
            readline.write_history_file(histfile)
            print ("Zamknięto")
            return
        except Exception as e:
            logging.error("Inny błąd: %s", e, exc_info=True)
            print (f"Błąd: {e}")


if __name__ == "__main__":
    main()
