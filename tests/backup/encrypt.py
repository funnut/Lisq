from . import utils
from cryptography.fernet import Fernet, InvalidToken
import getpass, base64, os, sys
from pathlib import Path


def generate_key(save_to_file=True):
    password = getpass.getpass(utils.COLORS['bgblue'] + "hasło: " + utils.COLORS['reset']).encode("utf-8")
    key = base64.urlsafe_b64encode(password.ljust(32, b'0')[:32])
#    print ('generate_key()')
    if save_to_file:
#        print ('generate_key()save_to_file')
        with open(utils.KEY_PATH(), "wb") as f:
            f.write(key)
        print(f"Klucz zapisany do: {utils.KEY_PATH()}")
    return Fernet(key)


def encrypt(NOTES_PATH, fernet=None):
    try:
        if fernet:
#            print('encrypt(): używam podanego fernet')
            pass
        else:
#            print('encrypt(): ładuję lub generuję klucz')
            if not utils.KEY_PATH().exists():
#                print(f"Brak pliku z kluczem: {utils.KEY_PATH()}")
                generate_key(save_to_file=True)
            with open(utils.KEY_PATH(), 'rb') as f:
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
        print(f"{utils.COLORS['bgred']}Błąd podczas szyfrowania.{utils.COLORS['reset']}\n{e}")


def decrypt(NOTES_PATH, fernet=None):
    try:
        if fernet:
 #           print('decrypt(): używam podanego fernet')
            pass
        else:
#            print('decrypt(): ładuję klucz z pliku')
            if not utils.KEY_PATH().exists():
#                print(f"Brak pliku z kluczem: {utils.KEY_PATH()}")
                generate_key(save_to_file=True)
            with open(utils.KEY_PATH(), 'rb') as f:
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
        print(f"\n\a{utils.COLORS['bgred']}Niepoprawne hasło.{utils.COLORS['reset']}\nNieprawidłowy token – klucz nie pasuje lub dane są uszkodzone.\n")
        return None
    except Exception as e:
        print(f"\n{utils.COLORS['bgred']}Wystąpił błąd podczas odszyfrowywania: {e}{utils.COLORS['reset']}\n")
        return None


def del_file(path):
    if os.path.exists(path):
            os.remove(path)


def switch(arg,arg1):
    if arg == 'read':
        setting = (utils.get_setting("encryption") or 'OFF').upper()
        print(f"\nEncryption is set to {setting}\n")
    elif arg == 'set':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", "set")
        print("\nEncryption set to SET\n")
    elif arg == 'on':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", "on")
        print("\nEncryption set to ON\n")
    elif arg == 'off':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", None)
        print("\nEncryption set to OFF\n")
    elif arg == 'delkey':
        yesno = input("\nCzy napewno chcesz usunąć klucz? (t/n): ")
        if yesno.lower() in ['t','']:
            key = utils.KEY_PATH()
            del_file(key)
            print("\nKlucz został usunięty.\n")
        else:
            print("\nAnulowano.\n")
    elif arg == 'newpass':
        yesno = input("\nCzy napewno chcesz zmienić hasło? (t/n): ")
        if yesno.lower() in ['t','']:
            key = utils.KEY_PATH()
            del_file(key)
            generate_key(save_to_file=True)
            print("\nHasło zostało zmienione.\n")
        else:
            print("\nAnulowano.\n")
    else:
        command = 'encryption', arg, arg1
        print(f"\n\a{utils.COLORS['bgred']}Nieprawidłowe polecenie.{utils.COLORS['reset']}\n")
        print(f"command: {utils.COLORS['green']}{command}{utils.COLORS['reset']}\n")


def setcfg(arg, arg1):
    arg = arg.lower()
    if arg == 'read':
        print(f"this is {arg}")
    elif arg == 'notespath': # NOTES
        if not arg1 or arg1 in ['show','s']:
            path = utils.NOTES_PATH()
            print(f"\n{path}\n")
        elif arg1 == 'unset':
            utils.del_setting("notespath")
            path = utils.NOTES_PATH()
            print(f"\nUstawiono ścieżkę domyślną: {path}\n")
        else:
            path = Path(os.path.expanduser(arg1)).resolve()
            if str(path).endswith(".txt"):
                utils.set_setting("notespath",str(path))
                print(f"\nUstawiono ścieżkę: {path}\n")
            else:
                print("\nBłąd: ścieżka musi prowadzić do pliku.\n")
    elif arg == 'keypath':  # KEY
        if arg1 in ['show', 's']:
            path = utils.KEY_PATH()
            print(f"\n{path}\n")
        elif arg1 == 'unset':
            utils.del_setting("keypath")
            path = utils.KEY_PATH()
            print(f"\nUstawiono ścieżkę domyślną: {path}\n")
        else:
            if not arg1:
                arg1 = input("Podaj ścieżkę: ")
            path = Path(os.path.expanduser(arg1)).resolve()
            if str(path).endswith(".keylisq"):
                utils.set_setting("keypath", str(path))
                print(f"\nUstawiono ścieżkę: {path}\n")
            else:
                print("\nBłąd: ścieżka musi prowadzić do pliku .keylisq.\n")
    elif arg == 'editor':
        if not arg1 or arg1 in ['show','s']:
            editor = utils.NOTES_EDITOR()
            print(f"\nEditor is set to: {editor}\n")
        else:
            utils.set_setting("editor",arg1)
            print(f"Ustawiono edytor: {arg1}")
    else:
        command = 'set', arg, arg1
        print(f"\n\a{utils.COLORS['bgred']}Nieprawidłowe polecenie.{utils.COLORS['reset']}\n")
        print(f"command: {utils.COLORS['green']}{command}{utils.COLORS['reset']}\n")

