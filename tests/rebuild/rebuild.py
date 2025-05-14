import logging
import readline
import shutil
from pathlib import Path
from datetime import date
from random import choice


# Konfiguracja log - logging
logging.basicConfig(
    level=logging.DEBUG, # DEBUG, INFO, WARNING, ERROR, CRITICAL
    filename="debug.log",  # rm by logować na konsolę
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Historia poleceń - readline, pathlib
script_dir = Path(__file__).parent.resolve()
histfile = script_dir / "_history"
if histfile.exists():
    readline.read_history_file(histfile)
readline.set_history_length(100)


def delete(args):
    """Usuwanie notatek."""
    logging.info(f"Start delete({args})")
    arg = args[0] if args else None
    try:
        logging.debug(f"arg: {arg}")
        while not arg:
            arg = input("  - ").strip()
            if ' ' in arg:
                print ("must be a single word!")
                arg = None
            if arg in ["q",""]:
                return

        with open("notes.txt","r",encoding="utf-8") as f:
            lines = f.readlines()

        if arg == "all":
            yesno = input("Czy usunąć wszystkie notatki? (y/n): ").strip().lower()
            if yesno in ["yes","y"]:
                open("notes.txt","w",encoding="utf-8").close()
                print ("Wszystkie notatki zostały usunięte.")
            else:
                print ("Anulowano.")

        elif arg in ["last","l"]:
            yesno = input("Czy usunąć ostatnią notatkę? (y/n): ").strip().lower()
            if yesno in ["y",""]:
                with open("notes.txt","w",encoding="utf-8") as f:
                    f.writelines(lines[:-1])
                print ("Usunięto ostatnią notatkę.")
            else:
                print ("Anulowano.")

        else:
            new_lines = [line for line in lines if arg not in line]
            number = len(lines)-len(new_lines)
            if number > 0:
                yesno = input(f"Czy usunąć {number} notatek zawierających '{arg}'? (y/n): ").strip().lower()
                if yesno in ["yes","y",""]:
                    with open("notes.txt","w",encoding="utf-8") as f:
                        f.writelines(new_lines)
                    print ("Usunięto notatkę/i.")
                else:
                    print ("Anulowano.")
            else:
                print ("Nie znaleziono pasujących notatek.")

    except FileNotFoundError:
        logging.error("FileNotFoundError w read_file()")
        print ("Nie znaleziono notatnika.")


def read_file(args):
    """Odczyt pliku notatek""" # - random, shutil
    logging.info(f"Start read_file({args})")
    terminal_width = shutil.get_terminal_size().columns
    print (f" _id _date {'_' * (terminal_width - 12)}")
    try:
        arg = args[0] if args else 'recent'
        logging.debug(f"arg: {arg}")
        with open("notes.txt","r",encoding="utf-8") as f:
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
        args = input("  : ").strip().split()
        if not args:
            return
    try:
        with open("notes.txt","r",encoding="utf-8") as f:
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
    with open("notes.txt","a",encoding="utf-8") as f:
        f.write(f"{id_} {date_} :: {' '.join(args)}\n") # args to lista!
    print ("Notatka dodana.")


def _test(args):
    logging.info(f"Start _test({args})")
    print ("Hello sir!")
    print ("args:",args)
    print ("bool(args):",bool(args))
    print ("type(args):",type(args))

    tablica = ["abc","1","3","cb a", " al i on"]
    print ("tablica=",tablica)
    s = ":-1" # args[80]
    print ("tablica=",eval(f"tablica[{s}]"))

# dispatch table
commands = {
    "test": _test,
    "add": write_file,
    "show": read_file,
    "s": read_file,
    "del": delete,
}

def main():
    logging.info("START FUNKCJI main()")
    while True:
        logging.debug("START GŁÓWNEJ PĘTLI")
        try:
            raw = input(" > ").strip()

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
