from lisq.core import pobierz_input, glowna_funkcja, sprawdz_input, write_file
import sys

def main():
    if len(sys.argv) > 1:
        if sys.argv[1].lower() in ['add','/']:
            note = " ".join(sys.argv[2:])
            write_file(note)
        else:
            usr_input = sys.argv[1:]
            glowna_funkcja(sprawdz_input(usr_input))
    else:
        print(fr"""
 _ _
| (_)___  __ _
| | / __|/ _` |
| | \__ \ (_| |
|_|_|___/\__, |
 quit - help|_|{randrange(0,1000)}
""")
        pobierz_input()
