```
 ___      ___   _______  _______
|   |    |   | |       ||       |
|   |    |   | |  _____||   _   |
|   |    |   | | |_____ |  | |  |
|   |___ |   | |_____  ||  |_|  |
|       ||   |  _____| ||      |
|_______||___| |_______||____||_|
```

From Polish *"lisek / foxie"* – lisq is a [**single file**](https://github.com/funnut/Lisq/blob/main/src/lisq.py) note-taking app that work with `.txt` files.

Lightweight, fast and portable. It's meant to be used as terminal aplication.

Code available under a non-commercial license *(see LICENSE file)*.

Copyright © funnut www.github.com/funnut

---

## INSTALLATION

With installed Python >=3.6,

+ Installation from [PyPI](https://pypi.org/project/lisq/)

```bash
pip install lisq
```
+ Installation from [GitHub](https://github.com/funnut/Lisq.git)

```bash
git clone https://github.com/funnut/Lisq.git
```
Place executable inside $PATH folder.

---

> How to install python packages visit [this site.](https://packaging.python.org/en/latest/tutorials/installing-packages/)

## CLI USAGE

```
lisq [command [arg1] [arg2] ... ]
lisq add "my first note"
```
> [!TIP]
> To type fast use `/` instead of `add` <a class="github-button" href="https://github.com/funnut/Lisq" data-color-scheme="no-preference: light; light: light; dark: dark;" data-icon="octicon-star" aria-label="Star funnut/Lisq on GitHub">⭐</a>

## COMMANDS

### Basic functionality:

To stay simple there are just three base commands to interact with your notes: `add`/`show`/`del`.

```
: [--]version   # show version
: [--]help      # show help page
: quit, q       # exit the program
: clear, c      # clear screen
: cmds      # list of all available commands
: edit      # open the notes file in set editor
:
: add, / <str>  # adds a note (preferably enclosed in quotation marks)
:
: show, s   # show recent notes (default 10)
:      <int>    # show number of recent notes
:      <str>    # show notes containing <string>
:      all      # show all notes
:      random, r    # show a random note
:
: del <str>     # delete notes containing <string>
:     last, l   # delete the last note
:     all   # delete all notes
```

### Additional functionality:

Encrypt your notes or any other file with a URL-safe Base64-encoded 32-byte token (***use with caution!***).
> [!IMPORTANT]
> **This functionality requires the cryptography package.** If it is not already installed via package manager, please run: `pip install -r requirements.txt`

```
: encryption on|off|set     # enables or disables login functionality; 'set' stores the token so it won't be requested again
: changepass    # changes the password (token)
:
: encrypt ~/file.txt    # encrypts any file
: decrypt ~/file.txt    # decrypts any file
:
: settings  # lists all settings
: reiterate     # renumber notes' IDs
: echo <str>    # prints the given text
: type <str>    # types the given text
```
To add your own functions:
   + define them,
   + then add to *dispatch table*.

## SETTINGS

Default settings that can be overwritten are:
   + default notes path is `~/noteslisq.txt`,
   + default key path is set to wherever main ***executable*** is,
   + default history path is set to wherever the main ***executable*** is,
   + default color accent is green,
   + default editor is set to `nano`,
   + default encryption is set to `off`.

To change it, set the following variable in the system by adding it to a startup file (eg. `~/.bashrc`).

```bash
export LISQ_SETTINGS='{
    "notes-path": "~/path/noteslisq.txt",
    "key-path": "~/path/key.lisq",
    "hist-path": "~/path/history.lisq",
    "color-accent": "\\033[34m",
    "editor": "nano",
    "encryption": "set"
    }'
```

> Source startup file or restart terminal.

To check current settings type `settings`.
