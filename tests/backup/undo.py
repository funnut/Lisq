from encrypt import generate_key, decrypt

fernet = generate_key(None)
decrypt('/data/data/com.termux/files/home/kod/5challenge/3_lisq/tests/notatki.txt',fernet)
