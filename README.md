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

## Instalation

With installed Python,

+ Copy src/**lisq.py** somewhere inside $PATH folder, then make it executable ( `chmod +x filename` ) and start by typing *filename*.
+ Alternatively you can install Lisq by pip* : `pip install lisq`

\* *Python language Package Manager*

> How to install Python packages visit [this site.](https://packaging.python.org/en/latest/tutorials/installing-packages/)

## CLI USAGE

```
lisq [command [arg1] [arg2] ...]
lisq add "my new note"  # alternatively use / instead of add
```

## COMMANDS

### Basic functionality:

It's design to be simple so there are just three core commands: `add`/`show`/`del`.

```
: quit, q       # exit the program
: clear, c      # clear screen
: cmds      # list of all available commands
: edit      # open the notes file in set editor
: [--]help      # show help page
: [--]version   # show version
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

You can encrypt your notes or any other file with a URL-safe Base64-encoded 32-byte token (***use with caution!***).
> [!WARNING]
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

You can add your own functions by:
   + defining them,
   + then adding to *dispatch table*.

## SETTINGS

Default settings are:
   + default notes path is `~/notesfile.txt`,
   + default key path is set to wherever main __file__ is,
   + default history path is set to wherever the main __file__ is,
   + default color accent is green,
   + default editor is set to `nano`,
   + default encryption is set to `off`.

To change it, set the following variable in your system by adding it to a startup file (eg. `~/.bashrc`).

```bash
export LISQ_SETTINGS='{
    "notes-path": "~/path/notesfile.txt",
    "key-path": "~/path/key.lisq",
    "hist-path": "~/path/history.lisq",
    "color-accent": "\\033[34m",
    "editor": "nano",
    "encryption": "set"
    }'
```

> Source your startup file or restart terminal.

You can check current settings by typing `settings` (both default and environmental drawn from *LISQ_SETTINGS* var).
