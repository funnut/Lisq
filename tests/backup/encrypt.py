import shutil
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
            print(f"Plik nie istnieje: {path}")
            return False
    except Exception as e:
        print(f"Nie udało się usunąć pliku '{path}': {e}")
        return False


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
    elif arg == 'del' and arg1 == 'key':
        path = utils.KEY_PATH()
        print(f"\n{path}")
        yesno = input("\nCzy napewno chcesz usunąć klucz? (t/n): ")
        if yesno.lower() in ['t','']:
            key = utils.KEY_PATH()
            del_file(key)
            print("\nKlucz został usunięty.\n")
        else:
            print("\nAnulowano.\n")
    elif arg == 'new' and arg1 == 'pass':
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
        utils.show_all_settings()
    elif arg == 'open': # cfg open
        editor = utils.EDITOR()
        if not editor:
            print("Błąd: Edytor nie jest ustawiony.")
        else:
            cfg_open(arg1)
    elif arg in ['show','s']: # cfg show
        if not arg1:
            print("\n[show,s] Pokaż ustawienie\n")
            print("keypath, notespath, editor\n")
        elif arg1 == 'keypath':
            path = utils.KEY_PATH()
            print(f"\n{path}\n")
        elif arg1 == 'notespath':
            path = utils.NOTES_PATH()
            print(f"\n{path}\n")
        elif arg1 == 'editor':
            editor = utils.EDITOR()
            print(f"\nEditor is set to: {editor}\n")
    elif arg == '-notespath': # cfg -notespath
        if arg1 == 'del':
            utils.del_setting("notespath")
            path = utils.NOTES_PATH()
            print(f"\nUstawiono ścieżkę domyślną: {path}\n")
        elif arg1 == 'open':
            os.system(f"{utils.EDITOR()} {utils.NOTES_PATH()}")
        else:
            if not arg1: # cfg -notespath
                arg1 = input("Podaj ścieżkę: ")
            path = Path(os.path.expanduser(arg1)).resolve()
            if str(path).endswith(".txt"):
                utils.set_setting("notespath",str(path))
                print(f"\nUstawiono ścieżkę: {path}\n")
            else:
                print("\nBłąd: ścieżka musi prowadzić do pliku.\n")
    elif arg == '-keypath':
        if arg1 == 'unset':
            handle_keypath_unset()
        elif arg1 == 'del':
            handle_keypath_del()
        else:
            handle_keypath_set_interactive()
    elif arg == '-editor':  # cfg -editor
        if not arg1:
            handle_editor()
        elif arg1 == 'open':
            handle_editor_open()
        else:
            if shutil.which(arg1):
                utils.set_setting("editor", arg1)
                print(f"Ustawiono edytor: {arg1}")
            else:
                print(f"Błąd: '{arg1}' nie istnieje w $PATH. Nie zapisano.")
    else:
        command = 'cfg', arg, arg1
        print(f"\n\a{utils.COLORS['bgred']}Nieprawidłowe polecenie.{utils.COLORS['reset']}\n")
        print(f"command: {utils.COLORS['green']}{command}{utils.COLORS['reset']}\n")

# -keypath

def handle_keypath_unset():
    confirm = input("Czy na pewno chcesz usunąć ustawioną ścieżkę? (t/n): ").strip().lower()
    if confirm in ['t', '']:
        utils.del_setting("keypath")
        path = utils.KEY_PATH()
        print(f"\nUstawiona ścieżka została usunięta.\nUstawiono ścieżkę domyślną: {path}\n")
    else:
        print("Anulowano usuwanie.")

def handle_keypath_del():
    path = utils.KEY_PATH()
    print(f"\n{path}")
    confirm = input("Czy na pewno chcesz usunąć klucz? (t/n): ").strip().lower()
    if confirm in ['t', '']:
        if os.path.exists(path):
            os.remove(path)
            print("\nKlucz usunięty.\n")
        else:
            print("Plik nie istnieje.\n")
    else:
        print("Anulowano usuwanie.")

def handle_keypath_set_interactive():
    path = utils.KEY_PATH()
    utils.color_block(["Path is set to:"], bg_color=utils.COLORS["bgblue"])
    print(f"    {path}")
    print("\n-keypath: open, set, del, <ścieżka>, unset\n")

    arg1 = input("Podaj ścieżkę (q - anuluj): ").strip()
    if arg1 == 'q':
        print('')
        return

    path = Path(os.path.expanduser(arg1)).resolve()
    if str(path).endswith(".keylisq"):
        utils.set_setting("keypath", str(path))
        print(f"\nUstawiono ścieżkę: {path}\n")
    else:
        print("\nBłąd: ścieżka musi prowadzić do pliku .keylisq.\n")

# -editor

def handle_editor():
    editor = utils.EDITOR()
    utils.color_block(
        [f"Editor is set to:"],
        bg_color=utils.COLORS["bgblue"])
    print(f"    {editor}")
    print("\n-editor: open, set, <name>\n")

    new_editor = input("Podaj nazwę edytora (q - anuluj): ").strip()
    if new_editor == 'q':
        print('')
        return
    elif shutil.which(new_editor):
        utils.set_setting("editor", new_editor)
        print(f"Ustawiono edytor: {new_editor}\n")
    else:
        print(f"Błąd: '{new_editor}' nie istnieje w $PATH. Nie zapisano.\n")

def handle_editor_open():
    editor = utils.EDITOR()
    if shutil.which(editor):
        os.system(f"{editor}")
    else:
        print(f"Błąd: Edytor '{editor}' nie został znaleziony w $PATH.\n")

def cfg_open(arg1):
    editor = utils.EDITOR()
    try:
        if arg1 in ['-notespath','notes','txt']:
            os.system(f"{editor} '{utils.NOTES_PATH()}'")
        elif arg1 in ['-keypath','key','keylisq','.keylisq']:
            os.system(f"{editor} -v --softwrap '{utils.KEY_PATH()}'")
        elif arg1 == '-editor':
            os.system(f"{editor}")
        else:
            config_path = utils.CONFIG_PATH
            if not os.path.exists(config_path):
                print(f"Błąd: Plik konfiguracyjny nie istnieje: {config_path}")
            else:
                os.system(f"{editor} '{config_path}'")
    except Exception as e:
        print(f"Wystąpił błąd przy otwieraniu edytora: {e}")

