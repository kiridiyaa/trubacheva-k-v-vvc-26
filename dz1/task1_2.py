def add(a, b):
    return a + b


def sub(a, b):
    return a - b


def mul(a, b):
    return a * b


def div(a, b):
    if b == 0:
        return "Ошибка: деление на ноль"
    return a / b


a = float(input("Введите первое число: "))
b = float(input("Введите второе число: "))
op = input("Введите операцию (+, -, *, /): ")

if op == "+":
    print("Результат:", add(a, b))
if op == "-":
    print("Результат:", sub(a, b))
if op == "*":
    print("Результат:", mul(a, b))
if op == "/":
    print("Результат:", div(a, b))
