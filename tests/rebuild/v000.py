# v000 Ogólna struktura programu

import logging

logging.basicConfig(
    level=logging.INFO, # DEBUG, INFO, WARNING, ERROR, CRITICAL
#    filename="debug.log",  # rm by logować na konsolę
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def _test(args):
    logging.info("Start _test(args)")
    print ("Hello sir!")
    print (args)
    print (bool(args))
    print (type(args))


# dispatch table
commands = {
    "test": _test,
}

def main():
    logging.info("START FUNKCJI main()")
    while True:
        logging.info("START GŁÓWNEJ PĘTLI")
        try:
            raw = input("> ").strip()
            if not raw:
                continue
            if raw in ["quit","q"]:
                logging.info("WYJŚCIE Z PROGRAMU ( quit, q )")
                return

            parts = raw.split()
            cmd = parts[0].lower()
            args = parts[1:]

            if cmd in commands:
                commands[cmd](args)
            else:
                raise ValueError(f"Nieprawidłowe polecenie: {cmd} {' '.join(args) if args else ''}")

        except ValueError as e:
            logging.error("ValueError: %s", e, exc_info=True)
            print ("Nieprawidłowe polecenie.")
        except KeyboardInterrupt as e:
            logging.error("Odebrano KeyboardInterrupt: %s", e, exc_info=True)
            print ("KeyboardInterrupt Error")
            return
        except EOFError as e:
            logging.error("WYJŚCIE Z PROGRAMU EOFError: %s", e, exc_info=True)
            print ("Zamknięto")
            return
        except Exception as e:
            logging.error("Inny błąd: %s", e, exc_info=True)
            print (f"Błąd: {e}")


if __name__ == "__main__":
    main()
