import logging
import readline
import os, sys
from pathlib import Path
from datetime import date
from random import choice

# Konfiguracja log - logging
logging.basicConfig(
    level=logging.DEBUG, # DEBUG, INFO, WARNING, ERROR, CRITICAL
#    filename="debug.log",  # rm by logować na konsolę
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Historia poleceń - readline, pathlib
script_dir = Path(__file__).parent.resolve()
histfile = script_dir / "_history"
if histfile.exists():
    readline.read_history_file(histfile)
readline.set_history_length(100)


def NOTES_PATH(): # - pathlib, os
    path = Path("~/_lisq/tests/rebuild/").expanduser() / "notes.txt"
    if path.exists():
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
            logging.info(f"Zaktualizowano identyfikatory dla {id_} linii.")
    except FileNotFoundError:
        logging.error("FileNotFoundError w reiterate()")
        print ("Nie znaleziono notatnika")

def delete(args):
    """Usuwanie notatek."""
    logging.info(f"Start delete({args}){len(args)}")
    try:
        while not args[0]: # delete
            args = input(" - ").strip()
            if ' ' in args:
                print ("Polecenie musi być pojedynczym słowem!")
                args = None
            if args in ["q",""]:
                return

        with open(NOTES_PATH(),"r",encoding="utf-8") as f:
            lines = f.readlines()

        if args[0] == "all": # all
            yesno = input("Czy usunąć wszystkie notatki? (y/n): ").strip().lower()
            if yesno in ["yes","y",""]:
                open(NOTES_PATH(),"w",encoding="utf-8").close()
                print ("Wszystkie notatki zostały usunięte.")
            else:
                print ("Anulowano.")

        elif args[0] in ["last","l"]: # last
            yesno = input("Czy usunąć ostatnią notatkę? (y/n): ").strip().lower()
            if yesno in ["y",""]:
                with open(NOTES_PATH(),"w",encoding="utf-8") as f:
                    f.writelines(lines[:-1])
                print ("Usunięto ostatnią notatkę.")
            else:
                print ("Anulowano.")

        else: # [id]
            new_lines = [line for line in lines if not any(el in line for el in args)]
            found = [arg for arg in args if any(arg in line for line in lines)]
            number = len(lines)-len(new_lines)
            if not all(any(arg in line for line in lines) for arg in args):
                print ("Nie wszystkie elementy zostały znalezione.")
            if number > 0:
                yesno = input(f"Czy usunąć {number} notatki zawierające {found}? (y/n): ").strip().lower()
                if yesno in ["yes","y",""]:
                    with open(NOTES_PATH(),"w",encoding="utf-8") as f:
                        f.writelines(new_lines)
                    reiterate()
                    print ("Usunięto notatkę/i.")
                else:
                    print ("Anulowano.")
            else:
                print ("Nie znaleziono pasujących notatek.")

    except FileNotFoundError:
        logging.error("FileNotFoundError w read_file()")
        print ("Nie znaleziono notatnika.")

def read_file(args):
    """Odczyt pliku notatek""" # - random, os
    logging.info(f"Start read_file({args})")
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

    except FileNotFoundError:
        logging.error("FileNotFoundError w read_file()")
        print ("Nie znaleziono notatnika.")

def write_file(args): # - datetime
    """Zapisywanie notatek do pliku w ustalonym formacie."""
    logging.info(f"Start write_file({args})")
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
    except FileNotFoundError:
        logging.error("FileNotFoundError w write_file()")
        print ("Utworzono nowy notatnik.")
        id_number = 1
    id_ = f"i{str(id_number).zfill(3)}"
    date_ = date.today().strftime("%Y-%m-%d")
    with open(NOTES_PATH(),"a",encoding="utf-8") as f:
        f.write(f"{id_} {date_} :: {' '.join(args)}\n") # args to lista!
    print ("Notatka dodana.")

def echo(text):
    print(text)

def _test(args):
    #print("type(args):",type(args))
    print("args:",args)
    with open(NOTES_PATH(), "r") as f:
        lines = f.readlines()
#    tablica = ["i001","i002","i003","i004", "i005"]
    print (lines,"\n\n")
    czy_any = any(element in line for element in args for line in lines)
    print (czy_any)
    czy_all = all(any(arg in line for line in lines) for arg in args)
    print (czy_all)
    #s = args[0]
    #print("tablica=",eval(f"tablica[{s}]"))

# dispatch table
commands = {
    "edit": lambda args: os.system(f"nano {NOTES_PATH()}"),
    "echo": lambda args: echo(" ".join(args)),
    "test": _test,
    "add": write_file,
    "show": read_file,
    "s": read_file,
    "del": delete,
    "delete": delete,
    "c": clear,
    "reiterate": reiterate,
}

def main(): # - sys
    logging.info("START FUNKCJI main()")
    while True:
        logging.debug("START GŁÓWNEJ PĘTLI")
        try:
            raw = input("> ").strip()
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
            print ("KeyboardInterrupt Error")
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

