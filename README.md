# Lisq

From Polish *"lisek / foxie"* – lisq is a [**single file**](https://github.com/funnut/Lisq/blob/main/lisq/lisq.py) note-taking app that work with `.txt` files.

![Zrzut ekranu](https://raw.githubusercontent.com/funnut/Lisq/refs/heads/dev/screenshot.jpg)

*Code available under a non-commercial license (see LICENSE file).*

Copyright © funnut www.github.com/funnut

---

## Instalation

```bash
pip install lisq
```

then type `lisq`

> How to install Python packages visit [this site.](https://packaging.python.org/en/latest/tutorials/installing-packages/)

## CLI USAGE

```
lisq [command] [arg1] [arg2] ...
lisq add "my new note"
```

## COMMANDS

**The three core commands are `add`/`show`/`del`.**

* Basic functionality:
```
: quit, q   - exit the program
: clear, c  - clear screen
: cmds      - list of all available commands
: edit      - open the notes file in set editor
:
: add, /    - add a note preferably in quotation marks
:
: show, s           - show recent notes (default 10)
: show [int]        - show number of recent notes
: show [str]        - show notes containing [string]
: show all          - show all notes
: show random, r    - show a random note
:
: del [str]      - delete notes containing [string]
: del last, l    - delete the last note
: del all        - delete all notes
```

* Additional functionality:

You can encrypt your notes with a Base64-encoded 32-byte token.
```
: encryption on, off or set - turn on or off login functionality, set - token is stored and not requested
: changepass - changing password (token)
```
Using build in encryption you can encrypt any other file (**Use with caution!**).
```
: encrypt ~/file.txt - encrypting any file
: decrypt ~/file.txt - decrypting any file
```
```
: settings - lists all settings
: reiterate - renumber notes' IDs
:
: echo [str] - echo given text
: type [str] - type given text
```

You can add your own functions by:
+ defining them,
+ then adding to *dispatch table*.

## SETTINGS

Default settings are:
   * default notes path is `~/notesfile.txt`,
   * default key path is set to wherever main __file__ is,
   * default history path is set to wherever the main __file__ is,
   * default color accent is cyan,
   * default editor is set to `nano`,
   * default encryption is set to `off`.

To change it, set the following variable in your system by adding it to a startup file `~/.bashrc` or `~/.zshrc`.

```bash
export LISQ_SETTINGS='{
    "notes-path": "~/path/notesfile.txt",
    "key-path": "~/path/key.lisq",
    "hist-path": "~/path/history.lisq",
    "color-accent": "\\033[34m",
    "editor": "nano",
    "encryption": "set"}'
```

** source your startup file or restart terminal **

You can check current settings by typing `settings` ( both *default* and *env* drawn from *LISQ_SETTINGS* var).
