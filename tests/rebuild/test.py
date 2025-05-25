import os
import json

# Funkcja a – pobiera konfigurację ze zmiennej środowiskowej
def get_env_config():
    config_str = os.getenv("APP_CONFIG", "{}")
    try:
        return json.loads(config_str)
    except json.JSONDecodeError:
        return {}

# Funkcja b – łączy ustawienia domyślne z tymi ze środowiska
def get_config():
    default_config = {
        "timeout": 10,
        "retries": 1,
        "log_level": "INFO"
    }
    env_config = get_env_config()
    return {**default_config, **env_config}  # nadpisuje domyślne wartości środowiskowymi

# Użycie:
config = get_config()
print(config)
