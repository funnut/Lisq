import shutil
from . import utils
from cryptography.fernet import Fernet, InvalidToken
import getpass, base64, os, sys
from pathlib import Path
import subprocess

theme = utils.theme

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

        print(theme['sys']+"encrypted"+reset)

    except Exception as e:
        raise RuntimeError(theme['sys']+f"Błąd podczas szyfrowania. {e}"+reset)


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
        raise ValueError(theme['error']+"Nieprawidłowy klucz lub plik nie jest zaszyfrowany."+reset)
        return None
    except Exception as e:
        raise RuntimeError(theme['error']+f"Nie udało się odszyfrować pliku: {e}"+reset)
        return None


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
            print(theme['error']+"Błąd: Edytor nie jest ustawiony."+reset)
        else:
            handle_cfg_open(arg1)
    elif arg in ['show','s']: # Show
        if not arg1:
            print(theme['sys']+"[show,s] Pokaż ustawienie: -encryption, -keypath, -notespath, -editor"+reset)
        elif arg1 in ['-keypath','keypath']:
            path = utils.KEY_PATH()
            print(theme['important']+f"{path}"+reset)
        elif arg1 in ['-notespath','notespath']:
            path = utils.NOTES_PATH()
            print(theme['important']+f"{path}"+reset)
        elif arg1 in ['-editor','editor']:
            editor = utils.EDITOR()
            print(f"{theme['sys']}Editor is set to: {theme['important']}{editor}{reset}")
        elif arg1 in ['-encryption','encryption']:
            setting = (utils.get_setting("encryption") or 'OFF').upper()
            print(f"{theme['sys']}Encryption is set to: {theme['important']}{setting}{reset}")
        else:
            print(theme['error']+"Błąd: nie ma takiego ustawienia."+reset)
    elif arg in ['-notespath','notespath']: # cfg -notespath
        if arg1 == 'unset':
            utils.del_setting("notespath")
            path = utils.NOTES_PATH()
            print(f"{theme['sys']}Ustawiono ścieżkę domyślną: {theme['important']}{path}{reset}")
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
        raise ValueError(theme['error']+"Nieprawidłowe polecenie."+reset)


# -------------------------------------------------

# -notespath

def handle_notespath(arg1=None):
    path = utils.NOTES_PATH()
    utils.color_block(["Notes path is set to:"],
                 bg_color=theme['cfg-topbar'])
    print(theme['important']+f"{path}"+reset)
    print(theme['sys']+"\n-NOTESPATH: open, unset, <ścieżka>\n"+reset)

    if not arg1:
        arg1 = input(theme['sys']+"Podaj nową ścieżkę (q - anuluj): "+reset).strip()
    if arg1.lower() == 'q':
        return

    if arg1 == 'open':
        subprocess.run([utils.EDITOR(), utils.NOTES_PATH()])
    if arg1 == 'unset':
        utils.del_setting("notespath")
        path = utils.NOTES_PATH()
        print(f"{theme['sys']}Ustawiono ścieżkę domyślną: {theme['important']}{path}{reset}")
    else:
        path = Path(os.path.expanduser(arg1)).resolve()
        if str(path).endswith(".txt"):
            utils.set_setting("notespath",str(path))
            print(f"{theme['sys']}Ustawiono nową ścieżkę: {theme['important']}{path}{reset}")
        else:
            print(theme['error']+"Błąd: ścieżka musi prowadzić do pliku .txt."+reset)

# -keypath

def handle_keypath_unset():
    confirm = input(theme['sys']+"Czy na pewno chcesz usunąć ustawioną ścieżkę? (t/n): "+reset).strip().lower()
    print('')
    if confirm in ['t', '']:
        utils.del_setting("keypath")
        path = utils.KEY_PATH()
        print(f"{theme['sys']}Ustawiona ścieżka została usunięta.\nUstawiono ścieżkę domyślną: {theme['important']}{path}{reset}")
    else:
        print(theme['sys']+"Anulowano usuwanie."+reset)

def handle_keypath_del():
    path = utils.KEY_PATH()
    print(theme['important']+f"{path}"+reset)
    confirm = input(theme['sys']+"Czy na pewno chcesz usunąć klucz? (t/n): "+reset).strip().lower()
    print('')
    if confirm in ['t', '']:
        if os.path.exists(path):
            os.remove(path)
            print(theme['sys']+"Klucz usunięty."+reset)
        else:
            print(theme['error']+"Plik nie istnieje."+reset)
    else:
        print(theme['sys']+"Anulowano usuwanie."+reset)

def handle_keypath(arg1=None):
    path = utils.KEY_PATH()
    utils.color_block(["Key path is set to:"],
               bg_color=theme['cfg-topbar'])
    print(theme['important']+f"{path}"+reset)
    print(theme['sys']+"\n-KEYPATH: open, unset, del, <ścieżka>\n"+reset)

    if not arg1:
        arg1 = input(theme['sys']+"Podaj nową ścieżkę (q - anuluj): "+reset).strip()
    if arg1.lower() == 'q':
        return

    expanded_path = Path(os.path.expanduser(arg1)).resolve()

    if not str(expanded_path).endswith(".keylisq"):
        print(theme['error']+"Błąd: ścieżka musi prowadzić do pliku .keylisq."+reset)
        return

    utils.set_setting("keypath", str(expanded_path))
    print(f"{theme['sys']}Ustawiono nową ścieżkę: {theme['important']}{expanded_path}{reset}")

# -editor

def handle_editor(arg1=None):
    editor = utils.EDITOR()
    utils.color_block(["Editor is set to:"],
            bg_color=theme['cfg-topbar'])
    print(theme['important']+f"{editor}"+reset)
    print(theme['sys']+"\n-EDITOR: open, <name>\n"+reset)

    if not arg1:
        arg1 = input(theme['sys']+"Podaj nazwę edytora (q - anuluj): "+reset).strip()
    if arg1 == 'q':
        return

    if arg1 == 'open':
        handle_editor_open()
        return
    if shutil.which(arg1):
        utils.set_setting("editor", arg1)
        print(f"{theme['sys']}Ustawiono edytor: {theme['important']}{arg1}{reset}")
    else:
        print(theme['error']+f"Błąd: '{arg1}' nie istnieje w $PATH. Nie zapisano."+reset)

def handle_editor_open():
    editor = utils.EDITOR()
    if shutil.which(editor):
        os.system(f"{editor}")
    else:
        print(theme['important']+f"Błąd: Edytor '{editor}' nie został znaleziony w $PATH."+reset)

# Open

def handle_cfg_open(arg1):
    editor = utils.EDITOR()
    try:
        if not editor:
            print(theme['error']+"Błąd: Edytor nie został określony."+reset)
            return

        if arg1 is None:
            plik = utils.CONFIG_PATH
            if not Path(plik).exists():
                print(theme['sys']+f"Błąd: Plik konfiguracyjny nie istnieje: {plik}"+reset)
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
                print(theme['error']+f"Błąd: Plik konfiguracyjny nie istnieje: {plik}"+reset)
                return
        else:
            print(theme['error']+f"Błąd: Nieznana opcja '{arg1}'"+reset)
            return

        subprocess.run([editor, str(plik)])

    except Exception as e:
        print(theme['error']+f"\aWystąpił błąd przy otwieraniu edytora: {e}"+reset)

# Encryption

def handle_encryption(arg1=None):
    setting = (utils.get_setting("encryption") or 'OFF').upper()
    utils.color_block(["Encryption is set to:"],
                bg_color=theme['cfg-topbar'])
    print(theme['important']+f"{setting}"+reset)
    print(theme['sys']+"\n-ENCRYPTION: on, off, set, newpass\n"+reset)

    if not arg1:
        arg1 = input(theme['sys']+"Podaj ustawienie (q - anuluj): "+reset).strip()
    if arg1.lower() == 'q':
        return

    elif arg1 == 'set':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", "set")
        print(f"{theme['sys']}Encryption set to {theme['important']}SET"+reset)
    elif arg1 == 'on':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", "on")
        print(f"{theme['sys']}Encryption set to {theme['important']}ON"+reset)
    elif arg1 == 'off':
        key = utils.KEY_PATH()
        del_file(key)
        utils.set_setting("encryption", None)
        print(f"{theme['sys']}Encryption set to {theme['important']}OFF"+reset)
    elif arg1 == 'newpass':
        yesno = input(theme['sys']+"\nCzy napewno chcesz zmienić hasło? (t/n): "+reset)
        if yesno.lower() in ['t','']:
            key = utils.KEY_PATH()
            del_file(key)
            generate_key(save_to_file=True)
            print(theme['sys']+"Hasło zostało zmienione."+reset)
        else:
            print(theme['sys']+"Anulowano."+reset)
    else:
        raise ValueError(theme['error']+"Nieprawidłowe polecenie."+reset)


def process_file(cmd, arg=None):
    # Określenie ścieżki
    if arg:
        path = Path(arg).expanduser()
    else:
        path = Path(input(theme['sys']+"Podaj ścieżkę: "+reset)).expanduser()
    # Sprawdzanie istnienia pliku
    if not path.exists():
        print(theme['error']+"Ścieżka nie istnieje."+reset)
        return

    if not path.is_file():
        print(theme['error']+"To nie jest plik."+reset)
        return
    # Przetwarzanie na podstawie komendy (encrypt lub decrypt)
    try:
        fernet = generate_key(save_to_file=None)

        if cmd == 'encrypt':
            encrypt(path, fernet)
            print(f"\n{theme['important']}{path}\n\n{theme['sys']}file encrypted"+reset)

        elif cmd == 'decrypt':
            decrypt(path, fernet)
            print(f"\n{theme['important']}{path}\n\nfile decrypted"+reset)

    except Exception as e:
        print(theme['error']+f"Błąd podczas {cmd} pliku: {e}"+reset)
    return


