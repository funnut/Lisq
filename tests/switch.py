import json
import os

CONFIG_PATH = os.path.expanduser("config.json")

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

def switch(arg):
    if arg == 'read':
        setting = get_setting("encryption")
        print(f'Encryption {setting}')
    elif arg == 'set':
        password = input('Podaj hasło: ')
        set_setting("encryption", "set")
        print("Encryption SET")
    elif arg == 'on':
        password = input('Podaj hasło: ')
        set_setting("encryption", "on")
        print("Encryption ON")
    elif arg == 'off':
        set_setting("encryption", "")
        print('Encryption OFF')
    else:
        print("Nieznana komenda:", arg)

while True:
    arg = input()
    switch(arg)
