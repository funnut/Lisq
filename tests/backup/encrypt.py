from . import utils
from cryptography.fernet import Fernet
import getpass, base64, os, sys
from pathlib import Path

KEY_PATH = Path.home() / ".keylisq"

def generate_key(save_to_file):
    password = getpass.getpass("Podaj hasło: ").encode("utf-8")
    key = base64.urlsafe_b64encode(password.ljust(32, b'0')[:32])
    print ('generate_key()')
    if save_to_file:
        print ('generate_key()save_to_file')
        with open(KEY_PATH, "wb") as f:
            f.write(key)
        print(f"Klucz zapisany do: {KEY_PATH}")
    return Fernet(key)

def encrypt(NOTES_PATH, fernet):
    if fernet:
        print ('encrypt()if fernet')
        with open(NOTES_PATH, 'r', encoding='utf-8') as f:
            plaintext = f.read().encode('utf-8')

        encrypted = fernet.encrypt(plaintext)

        with open(NOTES_PATH, 'w', encoding='utf-8') as f:
            f.write(encrypted.decode('utf-8'))
        print (f"Plik {NOTES_PATH} zaszyfrowany.")
    else:
        print ('encrypt()else')
        if not KEY_PATH.exists():
            print(f"Brak pliku z kluczem: {KEY_PATH}")
            generate_key(save_to_file=True)
    # Tworzy klucz na podstawie pliku klucza
        with open(KEY_PATH, 'rb') as f:
            key = f.read()
        fernet = Fernet(key)
    # Szyfruje
        with open(NOTES_PATH, 'rb') as f:
            plaintext = f.read()
        encrypted = fernet.encrypt(plaintext)
    # Zapisuje
        with open(NOTES_PATH, 'wb') as f:
            f.write(encrypted)
        print (f"Plik {NOTES_PATH} zaszyfrowany.")


def decrypt(NOTES_PATH,fernet):
#    try:
        if fernet:
        # Odszyfrowuje
            print ('decrypt()if fernet')
            with open(NOTES_PATH, 'r', encoding='utf-8') as f:
                encrypted = f.read().encode('utf-8')
            decrypted = fernet.decrypt(encrypted).decode('utf-8')
        # Zapisuje
            with open(NOTES_PATH, 'w', encoding='utf-8') as f:
                f.write(decrypted)
        else:
            print ('decrypt()else')
            if not KEY_PATH.exists():
                print(f"Brak pliku z kluczem: {KEY_PATH}")
                generate_key(save_to_file=True)
        # Tworzy klucz na podstawie pliku klucza
            with open(KEY_PATH, 'rb') as f:
                key = f.read()
            fernet = Fernet(key)
            decrypted = fernet.decrypt(encrypted).decode('utf-8')
            with open(NOTES_PATH, 'w', encoding='utf-8') as f:
                f.write(decrypted)
            print(f"Odszyfrowano notatkę.\n{NOTES_PATH}")
#    except InvalidToken:
#        print("Błędne hasło lub uszkodzony plik!")
#        return InvalidToken



def switch(arg):
    if arg == 'read':
        setting = (utils.get_setting("encryption") or 'OFF').upper()
        print(f'Encryption is set to {setting}')
    elif arg == 'set':
        utils.set_setting("encryption", "set")
        print("Encryption SET")
    elif arg == 'on':
        utils.set_setting("encryption", "on")
        print("Encryption ON")
    elif arg == 'off':
        utils.set_setting("encryption", "off")
        if os.path.exists(KEY_PATH):
            os.remove(KEY_PATH)
        else:
            print("Plik klucza już nie istnieje.")
        print('Encryption OFF')
    else:
        print("Nieznana komenda:", arg)


