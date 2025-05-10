# from lisq import NOTES_PATH
import base64
import getpass
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

SALT_FILE = 'salt.bin'
NOTES_PATH = 'notatki.txt'

def get_fernet_key():
    password = getpass.getpass("Podaj hasło: ").encode("utf-8")

    if os.path.exists(SALT_FILE):
        with open(SALT_FILE, 'rb') as f:
            salt = f.read()
    else:
        salt = os.urandom(16)
        with open(SALT_FILE, 'wb') as f:
            f.write(salt)

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    key = base64.urlsafe_b64encode(kdf.derive(password))
    return Fernet(key)

def encrypt(fernet):
    with open(NOTES_PATH, 'r', encoding='utf-8') as f:
        plaintext = f.read().encode('utf-8')

    encrypted = fernet.encrypt(plaintext)

    with open(NOTES_PATH, 'w', encoding='utf-8') as f:
        f.write(encrypted.decode('utf-8'))

    print("Zaszyfrowano notatkę.")

def decrypt(fernet):
    try:
        with open(NOTES_PATH, 'r', encoding='utf-8') as f:
            encrypted = f.read().encode('utf-8')

        decrypted = fernet.decrypt(encrypted).decode('utf-8')

        with open(NOTES_PATH, 'w', encoding='utf-8') as f:
            f.write(decrypted)

        print("Odszyfrowano notatkę.")
    except InvalidToken:
        print("Błędne hasło lub uszkodzony plik!")

# --- Wybierz działanie ---
if __name__ == "__main__":
    fernet = get_fernet_key()
    wybor = input("Co chcesz zrobić? [s]zyfruj / [o]dszyfruj: ").strip().lower()
    if wybor == 's':
        encrypt(fernet)
    elif wybor == 'o':
        decrypt(fernet)
    else:
        print("Nieznana opcja.")
