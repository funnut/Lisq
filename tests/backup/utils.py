from pathlib import Path
import os
import json


COLORS = {
    "reset": "\033[0m",
    "bold": "\033[1m",
    "italic": "\033[3m",
    "bitalic": "\033[3m\033e",
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

    # color_block(["  jakiś_tekst"], bg_color=COLORS["bgpurple"])

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

