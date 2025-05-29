import shutil, subprocess
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

    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "purple": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",

    "bold-black": "\033[1;30m",
    "bold-red": "\033[1;31m",
    "bold-green": "\033[1;32m",
    "bold-yellow": "\033[1;33m",
    "bold-blue": "\033[1;34m",
    "bold-purple": "\033[1;35m",
    "bold-cyan": "\033[1;36m",
    "bold-white": "\033[1;37m",

    "underline-black": "\033[4;30m",
    "underline-red": "\033[4;31m",
    "underline-green": "\033[4;32m",
    "underline-yellow": "\033[4;33m",
    "underline-blue": "\033[4;34m",
    "underline-purple": "\033[4;35m",
    "underline-cyan": "\033[4;36m",
    "underline-white": "\033[4;37m",

    "bg-black": "\033[40m",
    "bg-red": "\033[41m",
    "bg-green": "\033[42m",
    "bg-yellow": "\033[43m",
    "bg-blue": "\033[44m",
    "bg-purple": "\033[45m",
    "bg-cyan": "\033[46m",
    "bg-white": "\033[47m",

    "high-black": "\033[90m",
    "high-red": "\033[91m",
    "high-green": "\033[92m",
    "high-yellow": "\033[93m",
    "high-blue": "\033[94m",
    "high-purple": "\033[95m",
    "high-cyan": "\033[96m",
    "high-white": "\033[97m",

    "bold-high-black": "\033[1;90m",
    "bold-high-red": "\033[1;91m",
    "bold-high-green": "\033[1;92m",
    "bold-high-yellow": "\033[1;93m",
    "bold-high-blue": "\033[1;94m",
    "bold-high-purple": "\033[1;95m",
    "bold-high-cyan": "\033[1;96m",
    "bold-high-white": "\033[1;97m",

    "bg-high-black": "\033[0;100m",
    "bg-high-red": "\033[0;101m",
    "bg-high-green": "\033[0;102m",
    "bg-high-yellow": "\033[0;103m",
    "bg-high-blue": "\033[0;104m",
    "bg-high-purple": "\033[0;105m",
    "bg-high-cyan": "\033[0;106m",
    "bg-high-white": "\033[0;107m",

}

THEMES = {
    "lisq": {
        "intro": COLORS["reset"],
        "nav": COLORS["reset"],
        "nav-a": COLORS["cyan"],
        "header": COLORS["cyan"],
        "text": COLORS["reset"],
        "important": COLORS["cyan"],
        "password": COLORS["white"],
        "error": COLORS["high-red"],
        "notes-text": COLORS["reset"],
        "notes-top": COLORS["cyan"],
        "notes-side": COLORS["cyan"],
        "cfg-main-topbar": COLORS["bold-white"],
        "cfg-topbar": COLORS["bold-white"],
    },
    "custom": {
        "intro": COLORS["white"],
        "nav": COLORS["white"],
        "nav-a": COLORS["yellow"],
        "header": COLORS["yellow"],
        "text": COLORS["white"],
        "important": COLORS["yellow"],
        "password": COLORS["white"],
        "error": COLORS["red"],
        "notes-text": COLORS["white"],
        "notes-top": COLORS["yellow"],
        "notes-side": COLORS["yellow"],
        "cfg-main-topbar": COLORS["bold-white"],
        "cfg-topbar": COLORS["bold-white"],
    },
    "matrix": {
        "intro": COLORS["green"],
        "nav": COLORS["green"],
        "nav-a": COLORS["green"],
        "header": COLORS["bold-high-green"],
        "text": COLORS["green"],
        "important": COLORS["bold-high-green"],
        "password": COLORS["white"],
        "error": COLORS["red"],
        "notes-text": COLORS["high-green"],
        "notes-top": COLORS["green"],
        "notes-side": COLORS["green"],
        "cfg-main-topbar": COLORS["bold-green"],
        "cfg-topbar": COLORS["bold-green"],
    },
    "modern": {
        "intro": COLORS["white"],
        "nav": COLORS["white"],
        "nav-a": COLORS["cyan"],
        "header": COLORS["bg-purple"],
        "text": COLORS["white"],
        "important": COLORS["bold-white"],
        "password": COLORS["blue"],
        "error": COLORS["bg-red"],
        "notes-text": COLORS["high-green"],
        "notes-top": COLORS["high-yellow"],
        "notes-side": COLORS["high-yellow"],
        "cfg-main-topbar": COLORS["bg-purple"],
        "cfg-topbar": COLORS["bg-high-black"],
    }

}

THEMES["cli-text"] = {key: COLORS["reset"] for key in THEMES["lisq"].keys()}
THEMES["yellow"] = {key: COLORS["yellow"] for key in THEMES["lisq"].keys()}

def get_theme():
    theme_name = get_setting("theme", "lisq").lower()
    return THEMES.get(theme_name, THEMES["lisq"])

# theme = get_theme()
# print(f"{theme['header']}Tytuł{COLORS['reset']}")

def color_block(lines, bg_color="\x1b[0;100m"):
    reset = "\x1b[0m"
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80  # fallback
    for line in lines:
        print(f"{bg_color}{line.ljust(width)}{reset}")

    # color_block(["tekst"], bg_color=COLORS["bgpurple"])


# Domyślna ścieżka do config.json
CONFIG_PATH = Path.home() / ".lisq.cfg"


# Funkcje konfiguracji
def load_config():
    if not CONFIG_PATH.exists():
        return {}
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

def get_setting(key, default=None):
    key = key.lower()
    config = {k.lower(): v for k, v in load_config().items()}
    return config.get(key, default)

def set_setting(key, value):
    config = load_config()
    config[key] = value
    save_config(config)

def del_setting(key):
    config = load_config()
    if key in config:
        del config[key]
        save_config(config)

def set_theme(name):
    if name.lower() in THEMES:
        set_setting("theme", name.lower())
        print(f"{theme['text']}Motyw ustawiony na: {theme['important']}{name}{reset}")
    else:
        print(f"{theme['error']}Nieznany motyw. Dostępne:", ", ".join(THEMES.keys())+reset)

def show_all_settings():
    try:
        with open(CONFIG_PATH, 'r') as file:
            config = json.load(file)

        color_block(["AKTUALNE USTAWIENIA:"],
        bg_color=theme["cfg-main-topbar"])
        print(f"{theme['text']}{theme['important']}{CONFIG_PATH}{reset}\n")

        print(f"{theme['text']}open, show or -encryption, -keypath, -notespath, -theme, -editor{reset}\n")

        print(f"{theme['important']}.lisq.json{reset}")
        for key, value in config.items():
            print(f"   {theme['text']}{key}: {theme['important']}{value}{reset}")

    except FileNotFoundError:
        print(f"{theme['error']}Plik .lisq.json nie został znaleziony.{reset}")
    except json.JSONDecodeError:
        print(f"{theme['error']}Błąd przy wczytywaniu pliku .lisq.json – niepoprawny JSON.{reset}")

def del_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False
    except Exception as e:
        print(f"{theme['error']}Nie udało się usunąć pliku '{path}': {e}{reset}")
        return False

# Dodatkowe ścieżki

def KEY_PATH():
    return Path(get_setting("keypath") or Path.home() / ".keylisq")

def NOTES_PATH():
    return Path(get_setting("notespath") or os.getenv("LISQ_NOTES_PATH", os.path.expanduser("~/notes.txt")))

def EDITOR():
    return get_setting("editor") or os.getenv("NOTES_EDITOR", "nano")


# SETCFG

def setcfg(arg, arg1):
    arg = arg.lower()
    reset = COLORS['reset']
    if arg in ['-theme','theme']:
        setting = get_setting('theme','lisq')
        color_block(["Theme is set to:"],
                 bg_color=theme['cfg-topbar'])
        print(f"{theme['important']}{setting}{reset}")

        print(f"\n{theme['text']}Dostępne motywy:", ", ".join(THEMES.keys())+f"{reset}\n")

        if not arg1:
            arg1 = input(f"{theme['text']}Podaj nowy theme (q): {reset}").strip()
        if arg1.lower() in ['q','']:
            return

        set_theme(arg1)

    elif arg == 'read':
        show_all_settings()
    elif arg in ['-encryption','encryption']:
        if arg1:
            arg1 = arg1.lower()
        handle_encryption(arg1)
    elif arg in ['open']: # Open
        editor = EDITOR()
        if not editor:
            print(f"{theme['error']}Błąd: Edytor nie jest ustawiony.{reset}")
        else:
            handle_cfg_open(arg1)
    elif arg in ['show','s']: # Show
        if not arg1:
            print(f"{theme['text']}[show,s] Pokaż ustawienie: -encryption, -keypath, -notespath, -theme, -editor{reset}")
        elif arg1 in ['-keypath','keypath']:
            path = KEY_PATH()
            print(f"{theme['text']}{theme['important']}{path}{reset}")
        elif arg1 in ['-notespath','notespath']:
            path = NOTES_PATH()
            print(f"{theme['text']}{theme['important']}{path}{reset}")
        elif arg1 in ['-editor','editor']:
            editor = EDITOR()
            print(f"{theme['text']}Editor is set to: {theme['important']}{editor}{reset}")
        elif arg1 in ['-theme','theme']:
            setting = get_setting("theme","lisq")
            print(f"{theme['text']}Theme is set to: {theme['important']}{setting}{reset}")
        elif arg1 in ['-encryption','encryption']:
            setting = get_setting("encryption").upper()
            print(f"{theme['text']}Encryption is set to: {theme['important']}{setting}{reset}")
        else:
            print(f"{theme['error']}Błąd: nie ma takiego ustawienia.{reset}")
    elif arg in ['-notespath','notespath']: # cfg -notespath
        if arg1 == 'unset':
            del_setting("notespath")
            path = NOTES_PATH()
            print(f"{theme['text']}Ustawiono ścieżkę domyślną: {theme['important']}{path}{reset}")
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
        raise ValueError(f"{theme['error']}Nieprawidłowe polecenie.{reset}")


# -------------------------------------------------

# -notespath

def handle_notespath(arg1=None):
    path = NOTES_PATH()
    color_block(["Notes path is set to:"],
                 bg_color=theme['cfg-topbar'])
    print(f"{theme['important']}{path}{reset}")
    print(f"\n{theme['text']}-NOTESPATH: open, unset, <ścieżka>{reset}\n")

    if not arg1:
        arg1 = input(f"{theme['text']}Podaj nową ścieżkę (q): {reset}").strip()
    if arg1.lower() in ['q','']:
        return

    if arg1 == 'open':
        subprocess.run([EDITOR(), NOTES_PATH()])
    if arg1 == 'unset':
        del_setting("notespath")
        path = NOTES_PATH()
        print(f"{theme['text']}Ustawiono ścieżkę domyślną: {theme['important']}{path}{reset}")
    else:
        path = Path(os.path.expanduser(arg1)).resolve()
        if str(path).endswith(".txt"):
            set_setting("notespath",str(path))
            print(f"{theme['text']}Ustawiono nową ścieżkę: {theme['important']}{path}{reset}")
        else:
            print(f"{theme['error']}Błąd: ścieżka musi prowadzić do pliku .txt.{reset}")

# -keypath

def handle_keypath_unset():
    confirm = input(f"{theme['text']}Czy na pewno chcesz usunąć ustawioną ścieżkę? (t/n): {reset}").strip().lower()
    print('')
    if confirm in ['t', '']:
        del_setting("keypath")
        path = KEY_PATH()
        print(f"{theme['text']}Ustawiona ścieżka została usunięta.\nUstawiono ścieżkę domyślną: {theme['important']}{path}{reset}")
    else:
        print(f"{theme['text']}Anulowano usuwanie.{reset}")

def handle_keypath_del():
    path = KEY_PATH()
    print(f"{theme['text']}{theme['important']}{path}{reset}")
    confirm = input(f"{theme['text']}Czy na pewno chcesz usunąć klucz? (t/n): {reset}").strip().lower()
    print('')
    if confirm in ['t', '']:
        if os.path.exists(path):
            os.remove(path)
            print(f"{theme['text']}Klucz usunięty.{reset}")
        else:
            print(f"{theme['error']}Plik nie istnieje.{reset}")
    else:
        print(f"{theme['text']}Anulowano usuwanie.{reset}")

def handle_keypath(arg1=None):
    path = KEY_PATH()
    color_block(["Key path is set to:"],
               bg_color=theme['cfg-topbar'])
    print(f"{theme['important']}{path}{reset}")

    print(f"{theme['text']}\n-KEYPATH: open, unset, del, <ścieżka>{reset}\n")

    if not arg1:
        arg1 = input(f"{theme['text']}Podaj nową ścieżkę (q): {reset}").strip()
    if arg1.lower() in ['q','']:
        return

    expanded_path = Path(os.path.expanduser(arg1)).resolve()
    if not str(expanded_path).endswith(".keylisq"):
        print(f"{theme['error']}Błąd: ścieżka musi prowadzić do pliku .keylisq.{reset}")
        return

    set_setting("keypath", str(expanded_path))

    print(f"{theme['text']}Ustawiono nową ścieżkę: {theme['important']}{expanded_path}{reset}")

# -editor

def handle_editor(arg1=None):
    editor = EDITOR().upper()
    color_block(["EDITOR IS SET TO:"],
            bg_color=theme['cfg-topbar'])
    print(f"{theme['important']}{editor}{reset}")

    print(f"\n{theme['text']}-editor: open, DODAC UNSET <name>{reset}\n")

    if not arg1:
        arg1 = input(f"{theme['text']}Podaj nową nazwę edytora (q): {reset}").strip()
    if arg1 in ['q','']:
        return

    if arg1 == 'open':
        handle_editor_open()
        return
    if shutil.which(arg1):
        arg1 = arg1.lower()
        set_setting("editor", arg1)
        print(f"{theme['text']}Ustawiono edytor: {theme['important']}{arg1}{reset}")
    else:
        print(f"{theme['error']}Błąd: '{arg1}' nie istnieje w $PATH. Nie zapisano.{reset}")

def handle_editor_open():
    editor = EDITOR()
    if shutil.which(editor):
        subprocess.run([editor])
    else:
        print(f"{theme['error']}Błąd: Edytor '{editor}' nie został znaleziony w $PATH.{reset}")

# Open

def handle_cfg_open(arg1):
    editor = EDITOR()
    try:
        if not editor:
            print(f"{theme['error']}Błąd: Edytor nie został określony.{reset}")
            return

        if arg1 is None:
            plik = CONFIG_PATH
            if not Path(plik).exists():
                print(f"{theme['error']}Błąd: Plik konfiguracyjny nie istnieje: {plik}{reset}")
                return
            subprocess.run([editor, str(plik)])
            return

        if arg1 in ['-notespath', 'notespath']:
            plik = NOTES_PATH()
        elif arg1 in ['-keypath','keypath', 'key', '.keylisq']:
            plik = KEY_PATH()
        elif arg1 in ['-editor','editor']:
            subprocess.run([editor])
            return
        elif arg1 in ['-config', 'config', '.lisq.json']:
            plik = CONFIG_PATH
            if not Path(plik).exists():
                print(f"{theme['error']}Błąd: Plik konfiguracyjny nie istnieje: {plik}{reset}")
                return
        else:
            print(f"{theme['error']}Błąd: Nieznana opcja '{arg1}'{reset}")
            return

        subprocess.run([editor, str(plik)])

    except Exception as e:
        print(f"{theme['error']}Wystąpił błąd przy otwieraniu edytora: {e}{reset}")

# Encryption

def handle_encryption(arg1=None):
    setting = (get_setting("encryption") or 'OFF').upper()
    color_block(["ENCRYPTION IS SET TO:"],
                bg_color=theme['cfg-topbar'])
    print(f"{theme['important']}{setting}{reset}")

    print(f"\n{theme['text']}-encryption: on, off, set, newpass{reset}\n")

    if not arg1:
        arg1 = input(f"{theme['text']}Podaj ustawienie (q): {reset}").strip()
    if arg1.lower() in ['q','']:
        return

    elif arg1 == 'set':
        key = KEY_PATH()
        del_file(key)
        set_setting("encryption", "set")
        print(f"{theme['text']}Encryption set to {theme['important']}SET"+reset)
    elif arg1 == 'on':
        key = KEY_PATH()
        del_file(key)
        set_setting("encryption", "on")
        print(f"{theme['text']}Encryption set to {theme['important']}ON"+reset)
    elif arg1 == 'off':
        key = KEY_PATH()
        del_file(key)
        set_setting("encryption", None)
        print(f"{theme['text']}Encryption set to {theme['important']}OFF"+reset)
    elif arg1 == 'newpass':
        yesno = input(f"\n{theme['text']}Czy napewno chcesz zmienić hasło? (t/n): {reset}")
        if yesno.lower() in ['t','']:
            key = KEY_PATH()
            del_file(key)
            generate_key(save_to_file=True)
            print(f"{theme['text']}Hasło zostało zmienione.{reset}")
        else:
            print(f"{theme['text']}Anulowano.{reset}")
    else:
        raise ValueError(f"{theme['error']}Nieprawidłowe polecenie.{reset}")


theme = get_theme()
reset = COLORS['reset']
