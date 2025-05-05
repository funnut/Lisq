import os, json

CONFIG_PATH = os.path.expanduser("~/config.json")

# CONFIG
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

def cfg_encryption_setting():
    raw = (get_setting("encryption") or "").upper()
    return None if raw in ("", "OFF") else raw
