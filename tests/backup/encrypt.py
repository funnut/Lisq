import shutil
from . import utils
from cryptography.fernet import Fernet, InvalidToken
import getpass, base64, os, sys
from pathlib import Path
import subprocess


def generate_key(save_to_file=True):
    password = getpass.getpass(utils.COLORS['blue'] + "hasło: " + utils.COLORS['reset']).encode("utf-8")
    key = base64.urlsafe_b64encode(password.ljust(32, b'0')[:32])
#    print ('generate_key()')
    if save_to_file:
#        print ('generate_key()save_to_file')
        with open(utils.KEY_PATH(), "wb") as f:
            f.write(key)
#        print(f"Klucz zapisany do: {utils.KEY_PATH()}")
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
        with open(utils.NOTES_PATH(), 'r', encoding='utf-8') as f:
            plaintext = f.read().encode('utf-8')

        # Szyfrowanie
        encrypted = fernet.encrypt(plaintext)

        # Zapis jako bajty
        with open(utils.NOTES_PATH(), 'wb') as f:
            f.write(encrypted)

        print("encrypted")
#        print(f"Plik {utils.NOTES_PATH()} zaszyfrowany.")

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

        with open(utils.NOTES_PATH(), 'rb') as f:
            encrypted = f.read()

        decrypted = fernet.decrypt(encrypted).decode('utf-8')

        with open(utils.NOTES_PATH(), 'w', encoding='utf-8') as f:
            f.write(decrypted)

        print("decrypted")
#        print(f"Odszyfrowano notatkę: {utils.NOTES_PATH()}")
        return True
    except InvalidToken:
        print(f"\n\a{utils.COLORS['bgred']}Niepoprawne hasło.{utils.COLORS['reset']}\nNieprawidłowy token – klucz nie pasuje lub dane są uszkodzone.\n")
        return None
    except Exception as e:
        print(f"\n{utils.COLORS['bgred']}Wystąpił błąd podczas odszyfrowywania: {e}{utils.COLORS['reset']}\n")
        return None


def del_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
#            print(f"Plik nie istnieje: {path}")
            return False
    except Exception as e:
        print(f"Nie udało się usunąć pliku '{path}': {e}")
        return False

# SETCFG

def setcfg(arg, arg1):
    arg = arg.lower()
    if arg == 'read':
        utils.show_all_settings()
    elif arg in ['-encryption','encryption']:
        if arg1:
            arg1 = arg1.lower()
        handle_encryption(arg1)
    elif arg in ['open','o']: # Open
        editor = utils.EDITOR()
        if not editor:
            print("Błąd: Edytor nie jest ustawiony.")
        else:
            handle_cfg_open(arg1)
    elif arg in ['show','s']: # Show
        if not arg1:
            print("\n[show,s] Pokaż ustawienie")
            print("encryption, keypath, notespath, editor\n")
        elif arg1 == 'keypath':
            path = utils.KEY_PATH()
            print(f"\n{path}\n")
        elif arg1 == 'notespath':
            path = utils.NOTES_PATH()
            print(f"\n{path}\n")
        elif arg1 == 'editor':
            editor = utils.EDITOR()
            print(f"\nEditor is set to: {editor}\n")
        elif arg1 == 'encryption':
            setting = (utils.get_setting("encryption") or 'OFF').upper()
            print(f"\nEncryption is set to: {setting}\n")
        else:
            print("\nBłąd: nie ma takiego ustawienia.\n")
    elif arg in ['-notespath','notespath']: # cfg -notespath
        if arg1 == 'unset':
            utils.del_setting("notespath")
            path = utils.NOTES_PATH()
            print(f"\nUstawiono ścieżkę domyślną: {path}\n")
        elif arg1 == 'open':
            os.system(f"{utils.EDITOR()} {utils.NOTES_PATH()}")
        else:
            handle_notespath(arg1)
    elif arg in ['-keypath','keypath']: # cfg -keypath
        if arg1 == 'open':
            os.system(f"{utils.EDITOR()} {utils.KEY_PATH()}")
        elif arg1 == 'unset':
            handle_keypath_unset()
        elif arg1 == 'del':
            handle_keypath_del()
        else:
            handle_keypath(arg1)
    elif arg in ['-editor','editor']:  # cfg -editor
        if arg1 == 'open':
            handle_editor_open()
        else:
            handle_editor(arg1)
    else:
        command = 'cfg', arg, arg1
        print(f"\n\a{utils.COLORS['bgred']}Nieprawidłowe polecenie.{utils.COLORS['reset']}\n")
        print(f"command: {utils.COLORS['green']}{command}{utils.COLORS['reset']}\n")


# -------------------------------------------------

# -notespath

def handle_notespath(arg1=None):
    path = utils.NOTES_PATH()
    utils.color_block(["\nNotes path is set to:"],
                 bg_color=utils.COLORS["bgblack"])
    print(f"{path}")
    print("\n-NOTESPATH: open, unset, <ścieżka>\n")

    if not arg1:
        arg1 = input("Podaj nową ścieżkę (q - anuluj): ").strip()
    if arg1.lower() == 'q':
        print('')
        return

    if arg1 == 'open':
        os.system(f"{utils.EDITOR()} {utils.NOTES_PATH()}")
    if arg1 == 'unset':
        utils.del_setting("notespath")
        path = utils.NOTES_PATH()
        print(f"\nUstawiono ścieżkę domyślną: {path}\n")
    else:
        path = Path(os.path.expanduser(arg1)).resolve()
        if str(path).endswith(".txt"):
            utils.set_setting("notespath",str(path))
            print(f"Ustawiono nową ścieżkę: {path}\n")
        else:
            print("Błąd: ścieżka musi prowadzić do pliku .txt.\n")

# -keypath

def handle_keypath_unset():
    confirm = input("\nCzy na pewno chcesz usunąć ustawioną ścieżkę? (t/n): ").strip().lower()
    if confirm in ['t', '']:
        utils.del_setting("keypath")
        path = utils.KEY_PATH()
        print(f"\nUstawiona ścieżka została usunięta.\nUstawiono ścieżkę domyślną: {path}\n")
    else:
        print("\nAnulowano usuwanie.\n")

def handle_keypath_del():
    path = utils.KEY_PATH()
    print(f"\n{path}")
    confirm = input("Czy na pewno chcesz usunąć klucz? (t/n): ").strip().lower()
    if confirm in ['t', '']:
        if os.path.exists(path):
            os.remove(path)
            print("\nKlucz usunięty.\n")
        else:
            print("\nPlik nie istnieje.\n")
    else:
        print("\nAnulowano usuwanie.\n")

def handle_keypath(arg1=None):
    path = utils.KEY_PATH()
    utils.color_block(["\nKey path is set to:"],
               bg_color=utils.COLORS["bgblack"])
    print(f"{path}")
    print("\n-KEYPATH: open, unset, del, <ścieżka>\n")

    if not arg1:
        arg1 = input("Podaj nową ścieżkę (q - anuluj): ").strip()
    if arg1.lower() == 'q':
        print('')
        return

    expanded_path = Path(os.path.expanduser(arg1)).resolve()

    if not str(expanded_path).endswith(".keylisq"):
        print("\nBłąd: ścieżka musi prowadzić do pliku .keylisq.\n")
        return

    utils.set_setting("keypath", str(expanded_path))
    print(f"Ustawiono nową ścieżkę: {expanded_path}\n")

# -editor

def handle_editor(arg1=None):
    editor = utils.EDITOR()
    utils.color_block(["\nEditor is set to:"],
            bg_color=utils.COLORS["bgblack"])
    print(f"{editor}")
    print("\n-EDITOR: open, <name>\n")

    if not arg1:
        arg1 = input("Podaj nazwę edytora (q - anuluj): ").strip()
    if arg1 == 'q':
        print('')
        return
    if arg1 == 'open':
        handle_editor_open()
        print('')
        return
    if shutil.which(arg1):
        utils.set_setting("editor", arg1)
        print(f"Ustawiono edytor: {arg1}\n")
    else:
        print(f"Błąd: '{arg1}' nie istnieje w $PATH. Nie zapisano.\n")

def handle_editor_open():
    editor = utils.EDITOR()
    if shutil.which(editor):
        os.system(f"{editor}")
    else:
        print(f"Błąd: Edytor '{editor}' nie został znaleziony w $PATH.\n")

# Open

def handle_cfg_open(arg1):
    editor = utils.EDITOR()
    try:
        if not editor:
            print("Błąd: Edytor nie został określony.")
            return

        if arg1 is None:
            plik = utils.CONFIG_PATH
            if not Path(plik).exists():
                print(f"Błąd: Plik konfiguracyjny nie istnieje: {plik}\n")
                return
            subprocess.run([editor, str(plik)])
            return

        if arg1 in ['-notespath', 'notes', 'txt']:
            plik = utils.NOTES_PATH()
        elif arg1 in ['-keypath', 'key', 'keylisq', '.keylisq']:
            plik = utils.KEY_PATH()
        elif arg1 == '-editor':
            subprocess.run([editor])
            return
        elif arg1 in ['-config', 'config', '.lisq']:
            plik = utils.CONFIG_PATH
            if not Path(plik).exists():
                print(f"Błąd: Plik konfiguracyjny nie istnieje: {plik}\n")
                return
        else:
            print(f"\nBłąd: Nieznana opcja '{arg1}'\n")
            return

        subprocess.run([editor, str(plik)])

    except Exception as e:
        print(f"Wystąpił błąd przy otwieraniu edytora: {e}\n")

# Encryption

def handle_encryption(arg1=None):
    setting = (utils.get_setting("encryption") or 'OFF').upper()
    utils.color_block(["\nEncryption is set to:"],
                bg_color=utils.COLORS["bgblack"])
    print(f"{setting}")
    print("\n-ENCRYPTION: on, off, set, newpass\n")

    if not arg1:
        arg1 = input("Podaj ustawienie (q - anuluj): ").strip()
    if arg1.lower() == 'q':
        print('')
        return

    elif arg1 == 'set':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", "set")
        print("\nEncryption set to SET\n")
    elif arg1 == 'on':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", "on")
        print("\nEncryption set to ON\n")
    elif arg1 == 'off':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", None)
        print("\nEncryption set to OFF\n")
    elif arg1 == 'newpass':
        yesno = input("Czy napewno chcesz zmienić hasło? (t/n): ")
        if yesno.lower() in ['t','']:
            key = utils.KEY_PATH()
            del_file(key)
            generate_key(save_to_file=True)
            print("\nHasło zostało zmienione.\n")
        else:
            print("\nAnulowano.\n")
    else:
        command = 'cfg', 'encryption', arg1
        print(f"\n\a{utils.COLORS['bgred']}Nieprawidłowe polecenie.{utils.COLORS['reset']}\n")
        print(f"command: {utils.COLORS['green']}{command}{utils.COLORS['reset']}\n")
