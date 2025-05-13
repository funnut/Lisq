def greet():
    print("Cześć! Miło Cię widzieć.")

def help_command():
    print("Dostępne komendy: greet, help, exit")

def exit_program():
    print("Do zobaczenia!")
    exit()

# Słownik komend
commands = {
    "greet": greet,
    "help": help_command,
    "exit": exit_program
}

# Pętla CLI
while True:
    user_input = input("> ").strip()

    if user_input in commands:
        commands[user_input]()  # wywołanie funkcji
    else:
        print("Nieznana komenda. Wpisz 'help'.")

