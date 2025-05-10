# Lisq

From Polish *"lisek / foxie"* – lisq is a [**single file**](https://github.com/funnut/Lisq/blob/main/lisq/lisq.py) note-taking app that work with `.txt` files.

![Zrzut ekranu](https://raw.githubusercontent.com/funnut/Lisq/refs/heads/dev/screenshot.jpg)

*Code available under a non-commercial license (see LICENSE file).*

**Copyright © funnut**

## Instalation

```bash
pip install lisq
```

then type `lisq`

> How to install Python packages visit [this site.](https://packaging.python.org/en/latest/tutorials/installing-packages/)

---

### Important

+ Default path to your notes is `~/notes.txt`.
+ Default editor is `nano`.

To change it, set the following variables in your system by adding it to `~/.bashrc` or `~/.zshrc`.

```bash
export NOTES_PATH="/file/path/notes.txt"
export NOTES_EDITOR="nano"
```
or type `lisq cfg -notespath ~/path/notes.txt`

## Commands

```
quit, q, exit   # Exit the app  
clear, c        # Clear the screen  

show, s         # Show recent notes (default 10)  
     [int]      # Show [integer] number of recent notes  
     [str]      # Show notes containing [string]  
     all        # Show all notes  
     random, r  # Show a random note  

del  [str]      # Delete notes containing [string]  
     last, l    # Delete the last note  
     all        # Delete all notes  

cfg  open, show, s
cfg -encryption on, off, set, newpass
    -keypath open, unset, del or <path>
    -notespath open, unset or <path>
    -editor open or <editor>

encrypt ~/file.txt  # Encrypting any file
decrypt ~/file.txt  # Decrypting any file

reiterate       # Renumber notes' IDs  
edit            # Open the notes file in editor
```


## CLI Usage

```bash
lisq [command] [argument] [argument-1]
lisq add or / 'sample note text'
```
