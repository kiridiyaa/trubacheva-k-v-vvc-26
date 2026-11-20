def calculator(a, b, op):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "/":
        if b == 0:
            return "Ошибка: деление на ноль"
        return a / b
    return "Неизвестная операция"


while True:
    op = input("Введите операцию (+, -, *, /) или 'exit' для выхода: ")
    if op == "exit":
        print("Выход из программы")
        break
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))
    print("Результат:", calculator(a, b, op))
