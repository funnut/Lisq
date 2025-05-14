def echo(msg):
    print(msg)

def multiply(a, b):
    print(a * b)

commands = {
    "echo": lambda args: echo(" ".join(args)),
    "multiply": lambda args: multiply(int(args[0]), int(args[1]))
}

commands["echo"](["Hello", "world"])
