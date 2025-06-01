import utils
from cryptography.fernet import Fernet, InvalidToken
import getpass, base64, sys
from pathlib import Path

theme = utils.get_theme()
reset = utils.COLORS['reset']

def generate_key(save_to_file=True):
    password = getpass.getpass(theme['password'] + "hasło: " + reset).encode("utf-8")
    key = base64.urlsafe_b64encode(password.ljust(32, b'0')[:32])
    if save_to_file:
        with open(utils.KEY_PATH(), "wb") as f:
            f.write(key)
    return Fernet(key)

def encrypt(NOTES_PATH, fernet=None):
    try:
        if fernet:
            pass
        else:
            if not utils.KEY_PATH().exists():
                generate_key(save_to_file=True)
            with open(utils.KEY_PATH(), 'rb') as f:
                key = f.read()
            fernet = Fernet(key)

        # Odczyt jako tekst
        with open(utils.NOTES_PATH(), 'r', encoding='utf-8') as f:
            plaintext = f.read().encode('utf-8')

        # Szyfrowanie
        encrypted = fernet.encrypt(plaintext)

        # Zapis jako bajty
        with open(utils.NOTES_PATH(), 'wb') as f:
            f.write(encrypted)

        print(f"{theme['text']}encrypted{reset}")

    except Exception as e:
        raise RuntimeError(f"{theme['error']}Błąd podczas szyfrowania. {e}{reset}")

def decrypt(NOTES_PATH, fernet=None):
    try:
        if fernet:
            pass
        else:
            if not utils.KEY_PATH().exists():
                generate_key(save_to_file=True)
            with open(utils.KEY_PATH(), 'rb') as f:
                key = f.read()
            fernet = Fernet(key)

        with open(utils.NOTES_PATH(), 'rb') as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted).decode('utf-8')

        with open(utils.NOTES_PATH(), 'w', encoding='utf-8') as f:
            f.write(decrypted)

#        print(f"{theme['text']}decrypted{reset}")
        return True
    except InvalidToken:
        raise ValueError(f"{theme['error']}Nieprawidłowy klucz lub plik nie jest zaszyfrowany.{reset}")
        return None
    except Exception as e:
        raise RuntimeError(f"{theme['error']}Nie udało się odszyfrować pliku: {e}{reset}")
        return None

def process_file(cmd, arg=None):
    # Określenie ścieżki
    if arg:
        path = Path(arg).expanduser()
    else:
        path = Path(input(f"{theme['text']}Podaj ścieżkę: {reset}")).expanduser()
    # Sprawdzanie istnienia pliku
    if not path.exists():
        print(f"{theme['error']}Ścieżka nie istnieje.{reset}")
        return

    if not path.is_file():
        print(f"{theme['error']}To nie jest plik.{reset}")
        return
    # Przetwarzanie na podstawie komendy (encrypt lub decrypt)
    try:
        fernet = generate_key(save_to_file=None)

        if cmd == 'encrypt':
            encrypt(path, fernet)
            print(f"{theme['text']}{path}\n\nfile encrypted{reset}")

        elif cmd == 'decrypt':
            decrypt(path, fernet)
            print(f"{theme['text']}{path}\n\nfile decrypted{reset}")

    except Exception as e:
        print(f"{theme['error']}Błąd podczas {cmd} pliku: {e}{reset}")
    return

