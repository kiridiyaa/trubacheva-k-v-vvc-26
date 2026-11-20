def calc(a, b, op):
    if op == '+':
        return a + b
    if op == '-':
        return a - b
    if op == '*':
        return a * b
    if op == '/':
        if b == 0:
            return "Division by zero!"
        else:
            return a / b
    if op == '%':
        if b == 0:
            return "Division by zero!"
        else:
            return a % b
    if op == '//':
        if b == 0:
            return "Division by zero!"
        else:
            return a // b

flag = 0
while flag != 1:
    a = int(input())
    b = int(input())
    op = input()
    print(calc(a, b, op))
