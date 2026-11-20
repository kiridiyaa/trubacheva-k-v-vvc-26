def level_1():
    print("\n--- Уровень 1: Преобразование регистра ---")
    text = "пРиВеТ мИр"
    print("Исходная строка:", text)
    print("1 - upper(), 2 - lower(), 3 - capitalize()")
    choice = input("Выберите метод (1/2/3): ")
    if choice == "1":
        print("Результат:", text.upper())
    elif choice == "2":
        print("Результат:", text.lower())
    elif choice == "3":
        print("Результат:", text.capitalize())
    else:
        print("Неверный выбор")
        return False
    print("Уровень 1 пройден!")
    return True


def level_2():
    print("\n--- Уровень 2: Поиск и замена ---")
    text = "кот спит, кот ест, кот играет"
    print("Исходная строка:", text)
    print("Позиция слова 'спит':", text.find("спит"))
    print("Сколько раз встречается 'кот':", text.count("кот"))
    new_word = input("На какое слово заменить 'кот'?: ")
    result = text.replace("кот", new_word)
    print("Результат:", result)
    print("Уровень 2 пройден!")
    return True


def level_3():
    print("\n--- Уровень 3: Разделение и объединение ---")
    text = "яблоко,банан,груша,киви"
    print("Исходная строка:", text)
    words = text.split(",")
    print("После split(','):", words)
    sep = input("Введите разделитель для join (например, ' - '): ")
    result = sep.join(words)
    print("Результат:", result)
    print("Уровень 3 пройден!")
    return True


def level_4():
    print("\n--- Уровень 4: Проверка и очистка ---")
    raw = "   Python123   "
    print("Исходная строка:", repr(raw))
    print("strip():", repr(raw.strip()))
    print("lstrip():", repr(raw.lstrip()))
    print("rstrip():", repr(raw.rstrip()))
    user_input = input("Введите строку только из цифр: ")
    if user_input.isdigit():
        print("Верно, это цифры!")
    else:
        print("Это не только цифры")
    user_word = input("Введите слово только из букв: ")
    if user_word.isalpha():
        print("Верно, это только буквы!")
    else:
        print("В строке есть не только буквы")
    print("Уровень 4 пройден!")
    return True


def level_5():
    print("\n--- Уровень 5: Комплексная очистка строки ---")
    dirty = " pYtHon;is;AWESome    "
    print("Грязная строка:", repr(dirty))
    input("Нажмите Enter, чтобы очистить строку...")
    cleaned = dirty.strip()
    parts = cleaned.split(";")
    joined = " ".join(parts)
    result = joined.lower().capitalize()
    print("Чистая строка:", result)
    if result == "Python is awesome":
        print("Уровень 5 пройден! Поздравляем с победой!")
        return True
    return False


print("=== Мини-игра: 5 уровней работы со строками ===")
score = 0
if level_1():
    score += 1
if level_2():
    score += 1
if level_3():
    score += 1
if level_4():
    score += 1
if level_5():
    score += 1
print(f"\nИгра окончена. Пройдено уровней: {score} из 5")
