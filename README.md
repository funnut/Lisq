# Lisq

From Polish *"lisek / foxie"* – lisq is a [**single file**](https://github.com/funnut/Lisq/blob/main/lisq/lisq.py) note-taking app that work with `.txt` files.

![Zrzut ekranu](https://raw.githubusercontent.com/funnut/Lisq/refs/heads/main/screenshot.jpg)

*Code available under a non-commercial license (see LICENSE file).*

**Copyright © funnut**

## Instalation

```bash
pip install lisq
```

then type `lisq`

---

+ Default path to your notes is `~/notes.txt`.
+ Default editor is `nano`.

To change it, set the following variables in your system by adding it to `~/.bashrc` or `~/.zshrc`.

```bash
export NOTES_PATH="/file/path/notes.txt"
export NOTES_EDITOR="nano"
```

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
```
