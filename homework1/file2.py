def plus(x, y):
    return x + y

def minus(x, y):
    return x - y

def umn(x, y):
    return x * y

def delit(x, y):
    return x // y

a = int(input())
b = int(input())
op = input()

if op == '+':
    print(plus(a, b))

if op == '-':
    print(minus(a, b))

if op == '*':
    print(umn(a, b))

if op == '/':
    print(delit(a, b))
