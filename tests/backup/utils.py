from pathlib import Path
import os
import json


COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "italic": "\033[3m",
    "bitalic": "\033[1m\033[3m",
    "underline": "\033[4m",
    "strikethrough": "\033[9m",

    "green": "\033[92m",
    "yellow": "\033[93m",
    "blue": "\033[34m",
    "bgred": "\033[41m",
    "bgblue": "\033[44m",
    "bgpurple": "\033[45m",
    "bgblack": "\033[0;100m",
}

# lisq, matrix, neon
THEMES = {
    "dark": {
        "header": COLORS["bgpurple"],
        "text": COLORS["blue"],
        "important": COLORS["yellow"],
    },
    "light": {
        "header": COLORS["bgblue"],
        "text": COLORS["green"],
        "important": COLORS["bold"],
    }
}


def get_theme():
    theme_name = get_setting("theme", "dark").lower()
    return THEMES.get(theme_name, THEMES["dark"])

# theme = get_theme()
# print(f"{theme['header']}Tytuł{COLORS['reset']}")

# Domyślna ścieżka do config.json
CONFIG_PATH = Path.home() / ".lisq.json"


# Funkcje konfiguracji
def load_config():
    if not CONFIG_PATH.exists():
        return {}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def get_setting(key, default=None):
    return load_config().get(key, default)

def set_setting(key, value):
    config = load_config()
    config[key] = value
    save_config(config)

def del_setting(key):
    config = load_config()
    if key in config:
        del config[key]
        save_config(config)

def cfg_setting(setting):
    raw = (get_setting(setting) or "").upper()
    return None if raw in ("", "OFF") else raw


def color_block(lines, bg_color="\x1b[0;100m"):
    reset = "\x1b[0m"
    width = os.get_terminal_size().columns
    for line in lines:
        print(f"{bg_color}{line.ljust(width)}{reset}")

    # color_block(["tekst"], bg_color=COLORS["bgpurple"])

def show_all_settings():
    try:
        with open(CONFIG_PATH, 'r') as file:
            config = json.load(file)

        color_block(["Aktualne ustawienia:"],
        bg_color=COLORS["bgpurple"])
        print(f"{CONFIG_PATH}\n")

        print("open, show or -encryption, -keypath, -notespath, -editor\n")

        for key, value in config.items():
            print(f"  {key}: {value}")

    except FileNotFoundError:
        print("Plik .lisq.json nie został znaleziony.")
    except json.JSONDecodeError:
        print("Błąd przy wczytywaniu pliku .lisq.json – niepoprawny JSON.")


# Dodatkowe ścieżki

def KEY_PATH():
    return Path(get_setting("keypath") or Path.home() / ".keylisq")

def NOTES_PATH():
    return Path(get_setting("notespath") or os.getenv("NOTES_PATH", os.path.expanduser("~/notes.txt")))

def EDITOR():
    return get_setting("editor") or os.getenv("NOTES_EDITOR", "nano")


# SETCFG

def setcfg(arg, arg1):
    arg = arg.lower()
    if arg == 'read':
        show_all_settings()
    elif arg in ['-encryption','encryption']:
        if arg1:
            arg1 = arg1.lower()
        handle_encryption(arg1)
    elif arg in ['open']: # Open
        editor = EDITOR()
        if not editor:
            print("Błąd: Edytor nie jest ustawiony.")
        else:
            handle_cfg_open(arg1)
    elif arg in ['show','s']: # Show
        if not arg1:
            print("[show,s] Pokaż ustawienie: -encryption, -keypath, -notespath, -editor")
        elif arg1 in ['-keypath','keypath']:
            path = KEY_PATH()
            print(f"{path}")
        elif arg1 in ['-notespath','notespath']:
            path = NOTES_PATH()
            print(f"{path}")
        elif arg1 in ['-editor','editor']:
            editor = EDITOR()
            print(f"Editor is set to: {editor}")
        elif arg1 in ['-encryption','encryption']:
            setting = (get_setting("encryption") or 'OFF').upper()
            print(f"Encryption is set to: {setting}")
        else:
            print("Błąd: nie ma takiego ustawienia.")
    elif arg in ['-notespath','notespath']: # cfg -notespath
        if arg1 == 'unset':
            del_setting("notespath")
            path = NOTES_PATH()
            print(f"Ustawiono ścieżkę domyślną: {path}")
        elif arg1 == 'open':
            subprocess.run([EDITOR(),NOTES_PATH()])
        else:
            handle_notespath(arg1)
    elif arg in ['-keypath','keypath']: # cfg -keypath
        if arg1 == 'open':
            subprocess.run([EDITOR(),KEY_PATH()])
        elif arg1 == 'unset':
            handle_keypath_unset()
        elif arg1 == 'del':
            handle_keypath_del()
        else:
            handle_keypath(arg1)
    elif arg in ['-editor','editor']:  # cfg -editor
        if arg1 == 'open':
            handle_editor_open()
        else:
            handle_editor(arg1)
    else:
        raise ValueError("Nieprawidłowe polecenie.")


# -------------------------------------------------

# -notespath

def handle_notespath(arg1=None):
    path = NOTES_PATH()
    color_block(["Notes path is set to:"],
                 bg_color=COLORS["bgblack"])
    print(f"{path}")
    print("\n-NOTESPATH: open, unset, <ścieżka>\n")

    if not arg1:
        arg1 = input("Podaj nową ścieżkę (q - anuluj): ").strip()
    if arg1.lower() == 'q':
        return

    if arg1 == 'open':
        subprocess.run([EDITOR(), NOTES_PATH()])
    if arg1 == 'unset':
        del_setting("notespath")
        path = NOTES_PATH()
        print(f"Ustawiono ścieżkę domyślną: {path}")
    else:
        path = Path(os.path.expanduser(arg1)).resolve()
        if str(path).endswith(".txt"):
            set_setting("notespath",str(path))
            print(f"Ustawiono nową ścieżkę: {path}")
        else:
            print("Błąd: ścieżka musi prowadzić do pliku .txt.")

# -keypath

def handle_keypath_unset():
    confirm = input("Czy na pewno chcesz usunąć ustawioną ścieżkę? (t/n): ").strip().lower()
    print('')
    if confirm in ['t', '']:
        del_setting("keypath")
        path = KEY_PATH()
        print(f"Ustawiona ścieżka została usunięta.\nUstawiono ścieżkę domyślną: {path}")
    else:
        print("Anulowano usuwanie.")

def handle_keypath_del():
    path = KEY_PATH()
    print(f"{path}")
    confirm = input("Czy na pewno chcesz usunąć klucz? (t/n): ").strip().lower()
    print('')
    if confirm in ['t', '']:
        if os.path.exists(path):
            os.remove(path)
            print("Klucz usunięty.")
        else:
            print("Plik nie istnieje.")
    else:
        print("Anulowano usuwanie.")

def handle_keypath(arg1=None):
    path = KEY_PATH()
    color_block(["Key path is set to:"],
               bg_color=COLORS["bgblack"])
    print(f"{path}")
    print("\n-KEYPATH: open, unset, del, <ścieżka>\n")

    if not arg1:
        arg1 = input("Podaj nową ścieżkę (q - anuluj): ").strip()
    if arg1.lower() == 'q':
        return

    expanded_path = Path(os.path.expanduser(arg1)).resolve()

    if not str(expanded_path).endswith(".keylisq"):
        print("Błąd: ścieżka musi prowadzić do pliku .keylisq.")
        return

    set_setting("keypath", str(expanded_path))
    print(f"Ustawiono nową ścieżkę: {expanded_path}")

# -editor

def handle_editor(arg1=None):
    editor = EDITOR()
    color_block(["Editor is set to:"],
            bg_color=COLORS["bgblack"])
    print(f"{editor}")
    print("\n-EDITOR: open, <name>\n")

    if not arg1:
        arg1 = input("Podaj nazwę edytora (q - anuluj): ").strip()
    if arg1 == 'q':
        return

    if arg1 == 'open':
        handle_editor_open()
        return
    if shutil.which(arg1):
        set_setting("editor", arg1)
        print(f"Ustawiono edytor: {arg1}")
    else:
        print(f"Błąd: '{arg1}' nie istnieje w $PATH. Nie zapisano.")

def handle_editor_open():
    editor = EDITOR()
    if shutil.which(editor):
        os.system(f"{editor}")
    else:
        print(f"Błąd: Edytor '{editor}' nie został znaleziony w $PATH.")

# Open

def handle_cfg_open(arg1):
    editor = EDITOR()
    try:
        if not editor:
            print("Błąd: Edytor nie został określony.")
            return

        if arg1 is None:
            plik = CONFIG_PATH
            if not Path(plik).exists():
                print(f"Błąd: Plik konfiguracyjny nie istnieje: {plik}")
                return
            subprocess.run([editor, str(plik)])
            return

        if arg1 in ['-notespath', 'notes', 'txt']:
            plik = NOTES_PATH()
        elif arg1 in ['-keypath', 'key', 'keylisq', '.keylisq']:
            plik = KEY_PATH()
        elif arg1 == '-editor':
            subprocess.run([editor])
            return
        elif arg1 in ['-config', 'config', '.lisq']:
            plik = CONFIG_PATH
            if not Path(plik).exists():
                print(f"Błąd: Plik konfiguracyjny nie istnieje: {plik}")
                return
        else:
            print(f"Błąd: Nieznana opcja '{arg1}'")
            return

        subprocess.run([editor, str(plik)])

    except Exception as e:
        print(f"\aWystąpił błąd przy otwieraniu edytora: {e}")

# Encryption

def handle_encryption(arg1=None):
    setting = (get_setting("encryption") or 'OFF').upper()
    color_block(["Encryption is set to:"],
                bg_color=COLORS["bgblack"])
    print(f"{setting}")
    print("\n-ENCRYPTION: on, off, set, newpass\n")

    if not arg1:
        arg1 = input("Podaj ustawienie (q - anuluj): ").strip()
    if arg1.lower() == 'q':
        return

    elif arg1 == 'set':
        key = KEY_PATH()
        del_file(key)
        set_setting("encryption", "set")
        print("Encryption set to SET")
    elif arg1 == 'on':
        key = KEY_PATH()
        del_file(key)
        set_setting("encryption", "on")
        print("Encryption set to ON")
    elif arg1 == 'off':
        key = KEY_PATH()
        del_file(key)
        set_setting("encryption", None)
        print("Encryption set to OFF")
    elif arg1 == 'newpass':
        yesno = input("\nCzy napewno chcesz zmienić hasło? (t/n): ")
        if yesno.lower() in ['t','']:
            key = KEY_PATH()
            del_file(key)
            generate_key(save_to_file=True)
            print("Hasło zostało zmienione.")
        else:
            print("Anulowano.")
    else:
        raise ValueError("Nieprawidłowe polecenie.")

