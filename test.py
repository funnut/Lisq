from random import choice, randrange

notesfilename = '/data/data/com.termux/files/home/notatnik/notatnik.txt'

with open (notesfilename, 'r') as plik:
    do_wyswietlenia = plik.readlines()
    print (choice(do_wyswietlenia))
