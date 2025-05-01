# Lisq

From Polish *"lisek / foxie"* – lisq is a **single file** note-taking app that work with `.txt` files.

![Zrzut ekranu](screenshot.jpg)

*Code available under a non-commercial license (see LICENSE file).*

**Copyright © funnut**

## Instalation

`pip install git+https://github.com/funnut/Lisq.git`

then type `lisq`

In [__main__.py](lisq/__main__.py) (`pip show lisq` look for Location) you can change default '~/notesdata.txt' path.

## Commands

```bash
quit, q, exit   # Exit the app  
clear, c        # Clear the screen  

show, s         # Show recent notes (default 10)  
show [int]      # Show [integer] number of recent notes  
show [str]      # Show notes containing [string]  
show all        # Show all notes  
show random, r  # Show a random note  

del [str]       # Delete notes containing [string]  
del last, l     # Delete the last note  
del all         # Delete all notes  

reiterate       # Renumber notes' IDs  
path            # Show the path to the notes file  
edit            # Open the notes file in editor
```


## CLI Usage

```bash
lisq [command] [argument]
lisq / 'sample note text'
lisq add 'sample note text'
~/.bashrc:
alias lisq='python /file/path/lisq.py'
```
