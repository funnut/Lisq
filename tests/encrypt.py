from cryptography.fernet import Fernet, InvalidToken
from lisq import NOTES_PATH
import getpass, base64, os

NOTES_PATH = 'notatki.txt'

def generate_key():
    password = getpass.getpass("Podaj hasło: ").encode("utf-8")
    key = base64.urlsafe_b64encode(password.ljust(32, b'0')[:32])
    return Fernet(key)


def encrypt(fernet):
    with open(NOTES_PATH, 'r', encoding='utf-8') as f:
        plaintext = f.read().encode('utf-8')

    encrypted = fernet.encrypt(plaintext)

    with open(NOTES_PATH, 'w', encoding='utf-8') as f:
        f.write(encrypted.decode('utf-8'))

    print("Zaszyfrowano notatkę.\n")


def decrypt(fernet):
    try:
        with open(NOTES_PATH, 'r', encoding='utf-8') as f:
            encrypted = f.read().encode('utf-8')

        decrypted = fernet.decrypt(encrypted).decode('utf-8')

        with open(NOTES_PATH, 'w', encoding='utf-8') as f:
            f.write(decrypted)

        print("Odszyfrowano notatkę.\n")
    except InvalidToken:
        print("Błędne hasło lub uszkodzony plik!")


def switch(arg):
    if arg == 'read':
        setting = get_setting("encryption")
        print(f'Encryption {setting}')
    elif arg == 'set':
        password = input('Podaj hasło: ')
        set_setting("encryption", "set")
        print("Encryption SET")
    elif arg == 'on':
        password = input('Podaj hasło: ')
        set_setting("encryption", "on")
        print("Encryption ON")
    elif arg == 'off':
        set_setting("encryption", "")
        print('Encryption OFF')
    else:
        print("Nieznana komenda:", arg)


decrypt(generate_key())

