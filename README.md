# Lisq

From Polish *"lisek / foxie"* – lisq is a [**single file**](https://github.com/funnut/Lisq/blob/main/lisq/lisq.py) note-taking app that work with `.txt` files.

It's meant to use as terminal aplication. Text file is where information is stored.

*Code available under a non-commercial license (see LICENSE file).*

Copyright © funnut www.github.com/funnut

---

## Instalation

You can copy **lisq/lisq.py** somewhere in your $PATH *(remeber to make it executable)* or install by pip* : 

```bash
pip install lisq
```

then type `lisq`

\* *python language package manager*
> How to install Python packages visit [this site.](https://packaging.python.org/en/latest/tutorials/installing-packages/)

## CLI USAGE

```
lisq [command [arg1] [arg2] ...]
lisq add "my new note" // alternatively use / instead of add
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
: add, / [str]   - adds a note (preferably enclosed in quotation marks)
:
: show, s           - show recent notes (default 10)
:      [int]        - show number of recent notes
:      [str]        - show notes containing [string]
:      all          - show all notes
:      random, r    - show a random note
:
: del [str]      - delete notes containing [string]
:     last, l    - delete the last note
:     all        - delete all notes
```

* Additional functionality:

You can encrypt your notes or any other file with a URL-safe Base64-encoded 32-byte token (***use with caution!***).
```
: encryption on|off|set - enables or disables login functionality; 'set' stores the token so it won't be requested again
: changepass    - changes the password (token)
:
: encrypt ~/file.txt    - encrypts any file
: decrypt ~/file.txt    - decrypts any file
:
: settings - lists all settings
: reiterate - renumber notes' IDs
: echo [str] - prints the given text
: type [str] - types the given text
```

> You can add your own functions by:
> + defining them,
> + then adding to *dispatch table*.

## SETTINGS

Default settings are:
   * default notes path is `~/notesfile.txt`,
   * default key path is set to wherever main __file__ is,
   * default history path is set to wherever the main __file__ is,
   * default color accent is cyan,
   * default editor is set to `nano`,
   * default encryption is set to `off`.

To change it, set the following variable in your system by adding it to a startup file (eg. `~/.bashrc`).

```bash
export LISQ_SETTINGS='{
    "notes-path": "~/path/notesfile.txt",
    "key-path": "~/path/key.lisq",
    "hist-path": "~/path/history.lisq",
    "color-accent": "\\033[34m",
    "editor": "nano",
    "encryption": "set"}'
```

> Source your startup file or restart terminal.

You can check current settings by typing `settings` ( both default and environmental drawn from *LISQ_SETTINGS* var).
