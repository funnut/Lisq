# lambda argumenty: wyrażenie

# lambda w Pythonie to sposób na zdefiniowanie anonimowej
# funkcji (czyli takiej bez nazwy), zwykle w jednej
# linijce. Używa się jej, gdy potrzebujesz krótkiej
# funkcji „na szybko”, np. jako argument innej funkcji
# lub w słownikach komend.

# Zwykła funkcja
def dodaj(x, y):
    return x + y

# To samo jako lambda
lambda_dodaj = lambda x, y: x + y

print(dodaj(2, 3))        # 5
print(lambda_dodaj(2, 3)) # 5
