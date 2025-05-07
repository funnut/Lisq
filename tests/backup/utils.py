from pathlib import Path
import os, json



def KEY_PATH():
    return Path(get_setting("keypath"))  or Path.home() / ".keylisq"
def NOTES_PATH():
    return Path(get_setting("notespath")) or os.getenv("NOTES_PATH",os.path.expanduser("~/notes.txt"))
def NOTES_EDITOR():
    return get_setting("editor") or os.getenv("NOTES_EDITOR","nano")


# CONFIG

CONFIG_PATH = os.path.expanduser("~/config.json")

def load_config():
    if not os.path.exists(CONFIG_PATH):
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

def cfg_setting(setting):
    raw = (get_setting(setting) or "").upper()
    return None if raw in ("", "OFF") else raw

def del_setting(key):
    config = load_config()
    if key in config:
        del config[key]
        save_config(config)


COLORS = {
    "reset": "\033[0m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "cyan": "\033[36m",
    "bgred": "\033[41m",
    "bgblue": "\033[94m",
    "bgpurple": "\033[45m,"
}
