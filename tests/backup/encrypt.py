from . import utils
from cryptography.fernet import Fernet, InvalidToken
import getpass, base64, os, sys
from pathlib import Path


KEY_PATH = Path.home() / ".keylisq"


def generate_key(save_to_file=True):
    password = getpass.getpass("Podaj hasło: ").encode("utf-8")
    key = base64.urlsafe_b64encode(password.ljust(32, b'0')[:32])
    print ('generate_key()')
    if save_to_file:
        print ('generate_key()save_to_file')
        with open(KEY_PATH, "wb") as f:
            f.write(key)
        print(f"Klucz zapisany do: {KEY_PATH}")
    return Fernet(key)


def encrypt(NOTES_PATH, fernet=None):
    try:
        if fernet:
            print('encrypt(): używam podanego fernet')
        else:
            print('encrypt(): ładuję lub generuję klucz')
            if not KEY_PATH.exists():
                print(f"Brak pliku z kluczem: {KEY_PATH}")
                generate_key(save_to_file=True)
            with open(KEY_PATH, 'rb') as f:
                key = f.read()
            fernet = Fernet(key)

        # Odczyt jako tekst
        with open(NOTES_PATH, 'r', encoding='utf-8') as f:
            plaintext = f.read().encode('utf-8')

        # Szyfrowanie
        encrypted = fernet.encrypt(plaintext)

        # Zapis jako bajty
        with open(NOTES_PATH, 'wb') as f:
            f.write(encrypted)

        print(f"Plik {NOTES_PATH} zaszyfrowany.")

    except Exception as e:
        print(f"Błąd podczas szyfrowania: {e}")


def decrypt(NOTES_PATH, fernet=None):
    try:
        if fernet:
            print('decrypt(): używam podanego fernet')
        else:
            print('decrypt(): ładuję klucz z pliku')
            if not KEY_PATH.exists():
                print(f"Brak pliku z kluczem: {KEY_PATH}")
                generate_key(save_to_file=True)
            with open(KEY_PATH, 'rb') as f:
                key = f.read()
            fernet = Fernet(key)

        with open(NOTES_PATH, 'rb') as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted).decode('utf-8')

        with open(NOTES_PATH, 'w', encoding='utf-8') as f:
            f.write(decrypted)

        print(f"Odszyfrowano notatkę: {NOTES_PATH}")

    except InvalidToken:
        print("Błąd: Nieprawidłowy token – klucz nie pasuje lub dane są uszkodzone.")
    except Exception as e:
        print(f"Wystąpił błąd podczas odszyfrowywania: {e}")


def switch(arg):
    if arg == 'read':
        setting = (utils.get_setting("encryption") or 'OFF').upper()
        print(f'Encryption is set to {setting}')
    elif arg == 'set':
            # del key
        if os.path.exists(KEY_PATH):
            os.remove(KEY_PATH)
        else:
            print("Plik klucza już nie istnieje.")

        if os.path.exists(KEY_PATH):
            os.remove(KEY_PATH)
        else:
            print("Plik klucza już nie istnieje.")

        utils.set_setting("encryption", "set")
        print("Encryption SET")

    elif arg == 'on':
            # del key
        if os.path.exists(KEY_PATH):
            os.remove(KEY_PATH)
        else:
            print("Plik klucza już nie istnieje.")

        utils.set_setting("encryption", "on")
        print("Encryption ON")

    elif arg == 'off':
            # del key
        if os.path.exists(KEY_PATH):
            os.remove(KEY_PATH)
        else:
            print("Plik klucza już nie istnieje.")

        utils.set_setting("encryption", "off")
        print('Encryption OFF')
    elif arg == 'del_key':
        yesno = input('Ta operacja trwale usunie .keylisq czy kontynuować? (y/n): ')
        if yesno.lower() == 'y':
            if os.path.exists(KEY_PATH):
                os.remove(KEY_PATH)
                print('Klucz usunięty')
            else:
                print("Plik klucza już nie istnieje.")
        else:
            print('Anulowano')
    elif arg == 'new_pass':
        yesno = input('Ta operacja zmieni hasło, kontynuować? (y/n): ')
        if yesno.lower() == 'y':
            if os.path.exists(KEY_PATH):
                os.remove(KEY_PATH)
                generate_key(save_to_file=True)
                print('Ustawiono nowe hasło.')
            else:
                print("Plik klucza już nie istnieje.")
        else:
            print('Anulowano.')

    else:
        print('Nieznana komenda:', arg)



