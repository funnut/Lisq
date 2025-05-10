import shutil
from . import utils
from cryptography.fernet import Fernet, InvalidToken
import getpass, base64, os, sys
from pathlib import Path
import subprocess


def generate_key(save_to_file=True):
    password = getpass.getpass(utils.COLORS['bold'] + "hasło: " + utils.COLORS['reset']).encode("utf-8")
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

        print("encrypted")

    except Exception as e:
        raise RuntimeError(f"\aBłąd podczas szyfrowania. {e}")


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

#        print("decrypted")
        return True
    except InvalidToken:
        raise ValueError("\aNieprawidłowy klucz lub plik nie jest zaszyfrowany.")
        return None
    except Exception as e:
        raise RuntimeError(f"Nie udało się odszyfrować pliku: {e}")
        return None


def del_file(path):
    try:
        if os.path.exists(path):
            os.remove(path)
            return True
        else:
            return False
    except Exception as e:
        print(f"\aNie udało się usunąć pliku '{path}': {e}")
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
    elif arg in ['open']: # Open
        editor = utils.EDITOR()
        if not editor:
            print("Błąd: Edytor nie jest ustawiony.")
        else:
            handle_cfg_open(arg1)
    elif arg in ['show','s']: # Show
        if not arg1:
            print("[show,s] Pokaż ustawienie: -encryption, -keypath, -notespath, -editor")
        elif arg1 in ['-keypath','keypath']:
            path = utils.KEY_PATH()
            print(f"{path}")
        elif arg1 in ['-notespath','notespath']:
            path = utils.NOTES_PATH()
            print(f"{path}")
        elif arg1 in ['-editor','editor']:
            editor = utils.EDITOR()
            print(f"Editor is set to: {editor}")
        elif arg1 in ['-encryption','encryption']:
            setting = (utils.get_setting("encryption") or 'OFF').upper()
            print(f"Encryption is set to: {setting}")
        else:
            print("Błąd: nie ma takiego ustawienia.")
    elif arg in ['-notespath','notespath']: # cfg -notespath
        if arg1 == 'unset':
            utils.del_setting("notespath")
            path = utils.NOTES_PATH()
            print(f"Ustawiono ścieżkę domyślną: {path}")
        elif arg1 == 'open':
            subprocess.run([utils.EDITOR(),utils.NOTES_PATH()])
        else:
            handle_notespath(arg1)
    elif arg in ['-keypath','keypath']: # cfg -keypath
        if arg1 == 'open':
            subprocess.run([utils.EDITOR(),utils.KEY_PATH()])
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
        raise ValueError("Nieprawidłowe polecenie.")


# -------------------------------------------------

# -notespath

def handle_notespath(arg1=None):
    path = utils.NOTES_PATH()
    utils.color_block(["Notes path is set to:"],
                 bg_color=utils.COLORS["bgblack"])
    print(f"{path}")
    print("\n-NOTESPATH: open, unset, <ścieżka>\n")

    if not arg1:
        arg1 = input("Podaj nową ścieżkę (q - anuluj): ").strip()
    if arg1.lower() == 'q':
        return

    if arg1 == 'open':
        subprocess.run([utils.EDITOR(), utils.NOTES_PATH()])
    if arg1 == 'unset':
        utils.del_setting("notespath")
        path = utils.NOTES_PATH()
        print(f"Ustawiono ścieżkę domyślną: {path}")
    else:
        path = Path(os.path.expanduser(arg1)).resolve()
        if str(path).endswith(".txt"):
            utils.set_setting("notespath",str(path))
            print(f"Ustawiono nową ścieżkę: {path}")
        else:
            print("Błąd: ścieżka musi prowadzić do pliku .txt.")

# -keypath

def handle_keypath_unset():
    confirm = input("Czy na pewno chcesz usunąć ustawioną ścieżkę? (t/n): ").strip().lower()
    print('')
    if confirm in ['t', '']:
        utils.del_setting("keypath")
        path = utils.KEY_PATH()
        print(f"Ustawiona ścieżka została usunięta.\nUstawiono ścieżkę domyślną: {path}")
    else:
        print("Anulowano usuwanie.")

def handle_keypath_del():
    path = utils.KEY_PATH()
    print(f"{path}")
    confirm = input("Czy na pewno chcesz usunąć klucz? (t/n): ").strip().lower()
    print('')
    if confirm in ['t', '']:
        if os.path.exists(path):
            os.remove(path)
            print("Klucz usunięty.")
        else:
            print("Plik nie istnieje.")
    else:
        print("Anulowano usuwanie.")

def handle_keypath(arg1=None):
    path = utils.KEY_PATH()
    utils.color_block(["Key path is set to:"],
               bg_color=utils.COLORS["bgblack"])
    print(f"{path}")
    print("\n-KEYPATH: open, unset, del, <ścieżka>\n")

    if not arg1:
        arg1 = input("Podaj nową ścieżkę (q - anuluj): ").strip()
    if arg1.lower() == 'q':
        return

    expanded_path = Path(os.path.expanduser(arg1)).resolve()

    if not str(expanded_path).endswith(".keylisq"):
        print("Błąd: ścieżka musi prowadzić do pliku .keylisq.")
        return

    utils.set_setting("keypath", str(expanded_path))
    print(f"Ustawiono nową ścieżkę: {expanded_path}")

# -editor

def handle_editor(arg1=None):
    editor = utils.EDITOR()
    utils.color_block(["Editor is set to:"],
            bg_color=utils.COLORS["bgblack"])
    print(f"{editor}")
    print("\n-EDITOR: open, <name>\n")

    if not arg1:
        arg1 = input("Podaj nazwę edytora (q - anuluj): ").strip()
    if arg1 == 'q':
        return

    if arg1 == 'open':
        handle_editor_open()
        return
    if shutil.which(arg1):
        utils.set_setting("editor", arg1)
        print(f"Ustawiono edytor: {arg1}")
    else:
        print(f"Błąd: '{arg1}' nie istnieje w $PATH. Nie zapisano.")

def handle_editor_open():
    editor = utils.EDITOR()
    if shutil.which(editor):
        os.system(f"{editor}")
    else:
        print(f"Błąd: Edytor '{editor}' nie został znaleziony w $PATH.")

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
                print(f"\aBłąd: Plik konfiguracyjny nie istnieje: {plik}")
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
                print(f"\aBłąd: Plik konfiguracyjny nie istnieje: {plik}")
                return
        else:
            print(f"\aBłąd: Nieznana opcja '{arg1}'")
            return

        subprocess.run([editor, str(plik)])

    except Exception as e:
        print(f"\aWystąpił błąd przy otwieraniu edytora: {e}")

# Encryption

def handle_encryption(arg1=None):
    setting = (utils.get_setting("encryption") or 'OFF').upper()
    utils.color_block(["Encryption is set to:"],
                bg_color=utils.COLORS["bgblack"])
    print(f"{setting}")
    print("\n-ENCRYPTION: on, off, set, newpass\n")

    if not arg1:
        arg1 = input("Podaj ustawienie (q - anuluj): ").strip()
    if arg1.lower() == 'q':
        return

    elif arg1 == 'set':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", "set")
        print("Encryption set to SET")
    elif arg1 == 'on':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", "on")
        print("Encryption set to ON")
    elif arg1 == 'off':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", None)
        print("Encryption set to OFF")
    elif arg1 == 'newpass':
        yesno = input("\nCzy napewno chcesz zmienić hasło? (t/n): ")
        if yesno.lower() in ['t','']:
            key = utils.KEY_PATH()
            del_file(key)
            generate_key(save_to_file=True)
            print("Hasło zostało zmienione.")
        else:
            print("Anulowano.")
    else:
        raise ValueError("Nieprawidłowe polecenie.")


from pathlib import Path



def process_file(cmd, arg=None):
    # Określenie ścieżki
    if arg:
        path = Path(arg).expanduser()
    else:
        path = Path(input("Podaj ścieżkę: ")).expanduser()

    # Sprawdzanie istnienia pliku
    if not path.exists():
        print("Ścieżka nie istnieje.")
        return

    if not path.is_file():
        print("To nie jest plik.")
        return

    # Przetwarzanie na podstawie komendy (encrypt lub decrypt)
    try:
        fernet = generate_key(save_to_file=None)

        if cmd == 'encrypt':
            encrypt(path, fernet)
            print(f"\n{path}\n\nfile encrypted")

        elif cmd == 'decrypt':
            decrypt(path, fernet)
            print(f"\n{path}\n\nfile decrypted")

    except Exception as e:
        print(f"Błąd podczas {cmd} pliku: {e}")
    return
