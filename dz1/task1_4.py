from abc import ABC, abstractmethod


class AbstractCalculator(ABC):
    def __init__(self, name):
        self.name = name
        self.last_result = None
        self.history = []

    @abstractmethod
    def add(self, a, b):
        pass

    @abstractmethod
    def sub(self, a, b):
        pass

    @abstractmethod
    def mul(self, a, b):
        pass

    @abstractmethod
    def div(self, a, b):
        pass


class SimpleCalculator(AbstractCalculator):
    def add(self, a, b):
        self.last_result = a + b
        self.history.append(f"{a} + {b} = {self.last_result}")
        return self.last_result

    def sub(self, a, b):
        self.last_result = a - b
        self.history.append(f"{a} - {b} = {self.last_result}")
        return self.last_result

    def mul(self, a, b):
        self.last_result = a * b
        self.history.append(f"{a} * {b} = {self.last_result}")
        return self.last_result

    def div(self, a, b):
        if b == 0:
            return "Ошибка: деление на ноль"
        self.last_result = a / b
        self.history.append(f"{a} / {b} = {self.last_result}")
        return self.last_result

    def calculate(self, a, b, op):
        if op == "+":
            return self.add(a, b)
        if op == "-":
            return self.sub(a, b)
        if op == "*":
            return self.mul(a, b)
        if op == "/":
            return self.div(a, b)
        return "Неизвестная операция"


calc = SimpleCalculator("Обычный калькулятор")
print(calc.name)
while True:
    op = input("Введите операцию (+, -, *, /), 'history' или 'exit': ")
    if op == "exit":
        break
    if op == "history":
        print(calc.history)
        continue
    a = float(input("Введите первое число: "))
    b = float(input("Введите второе число: "))
    print("Результат:", calc.calculate(a, b, op))
