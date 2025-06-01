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
```
: quit, q, exit
: c         - clear screen
: cmds      - list of available commands
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
:
: encryption on, off or set (password is stored and not requested)
: changepass - changing password    
:
: encrypt ~/file.txt    - encrypting any file
: decrypt ~/file.txt    - decrypting any file
:
: settings    - lists all settings
: reiterate   - renumber notes' IDs
: edit        - open the notes file in set editor
:
: echo [str]    - echo given text
: type [str]    - type given text
```
You can add your own functions by:
+ defining them,
+ then adding to *dispatch table*.

## SETTINGS

Default settings:
   * default notes path is `~/notesfile.txt`,
   * default key path is set to wherever main __file__ is,
   * default history path is set to wherever the main __file__ is,
   * default editor is set to `nano`,
   * default encryption is set to `off`.

To change it, set the following variable in your system by adding it to a startup file `~/.bashrc` or `~/.zshrc`.

```bash
export LISQ_SETTINGS='{
    "notes-path": "~/path/notesfile.txt",
    "key-path": "~/path/key.lisq",
    "hist-path": "~/path/history.lisq",
    "editor": "nano",
    "encryption": "set"}'
```

> source your startup file or restart terminal

You can check current settings by typing `settings` ( both *default* and *env* drawn from *LISQ_SETTINGS* var).
