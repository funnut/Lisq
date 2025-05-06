from . import utils
from cryptography.fernet import Fernet, InvalidToken
import getpass, base64, os, sys
from pathlib import Path


KEY_PATH = Path.home() / ".keylisq"
COLORS = {
    "reset": "\033[0m",
    "green": "\033[92m",
    "yellow": "\033[93m",
    "cyan": "\033[36m",
    "bgred": "\033[41m",
    "bgblue": "\033[94m",
}


def generate_key(save_to_file=True):
    password = getpass.getpass(f"{COLORS['bgblue']}Podaj hasło:{COLORS['reset']} ").encode("utf-8")
    key = base64.urlsafe_b64encode(password.ljust(32, b'0')[:32])
#    print ('generate_key()')
    if save_to_file:
#        print ('generate_key()save_to_file')
        with open(KEY_PATH, "wb") as f:
            f.write(key)
#        print(f"Klucz zapisany do: {KEY_PATH}")
    return Fernet(key)


def encrypt(NOTES_PATH, fernet=None):
    try:
        if fernet:
#            print('encrypt(): używam podanego fernet')
            pass
        else:
#            print('encrypt(): ładuję lub generuję klucz')
            if not KEY_PATH.exists():
#                print(f"Brak pliku z kluczem: {KEY_PATH}")
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

        print("encrypted")
#        print(f"Plik {NOTES_PATH} zaszyfrowany.")

    except Exception as e:
        print(f"{COLORS['bgred']}Błąd podczas szyfrowania: {e}{COLORS['reset']}")


def decrypt(NOTES_PATH, fernet=None):
    try:
        if fernet:
 #           print('decrypt(): używam podanego fernet')
            pass
        else:
#            print('decrypt(): ładuję klucz z pliku')
            if not KEY_PATH.exists():
#                print(f"Brak pliku z kluczem: {KEY_PATH}")
                generate_key(save_to_file=True)
            with open(KEY_PATH, 'rb') as f:
                key = f.read()
            fernet = Fernet(key)

        with open(NOTES_PATH, 'rb') as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted).decode('utf-8')

        with open(NOTES_PATH, 'w', encoding='utf-8') as f:
            f.write(decrypted)

        print("decrypted")
#        print(f"Odszyfrowano notatkę: {NOTES_PATH}")
        return True
    except InvalidToken:
        print(f"\n\a{COLORS['bgred']}Niepoprawne hasło.{COLORS['reset']}\nNieprawidłowy token – klucz nie pasuje lub dane są uszkodzone.\n")
        return None
    except Exception as e:
        print(f"\n{COLORS['bgred']}Wystąpił błąd podczas odszyfrowywania: {e}{COLORS['reset']}\n")
        return None


def delkey(KEY_PATH):
    if os.path.exists(KEY_PATH):
            os.remove(KEY_PATH)


def switch(arg):
    if arg == 'read':
        setting = (utils.get_setting("encryption") or 'OFF').upper()
        print(f"\nEncryption is set to {setting}\n")
    elif arg == 'set':
        delkey(KEY_PATH)
        utils.set_setting("encryption", "set")
        print("\nEncryption set to SET\n")
    elif arg == 'on':
        delkey(KEY_PATH)
        utils.set_setting("encryption", "on")
        print("\nEncryption set to ON\n")
    elif arg == 'off':
        delkey(KEY_PATH)
        utils.set_setting("encryption", "off")
        print("\nEncryption set to OFF\n")
    elif arg == 'delkey':
        yesno = input("\nCzy napewno chcesz usunąć klucz? (t/n): ")
        if yesno.lower() in ['t','']:
            delkey(KEY_PATH)
            print("\nKlucz został usunięty.\n")
        else:
            print("\nAnulowano.\n")
    elif arg == 'newpass':
        yesno = input("\nCzy napewno chcesz zmienić hasło? (t/n): ")
        if yesno.lower() in ['t','']:
            if os.path.exists(KEY_PATH):
                os.remove(KEY_PATH)
            generate_key(save_to_file=True)
            print("\nHasło zostało zmienione.\n")
        else:
            print("\nAnulowano.\n")
    else:
        print(f"\n\a{COLORS['bgred']}Nieprawidłowe polecenie.{COLORS['reset']}\n")
        print(f"command: {COLORS['green']}('encryption', '{arg}'){COLORS['reset']}\n")


