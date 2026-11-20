import copy
import random


def create_maze(n, m):
    room_types = ["empty", "chest", "monster", "trap", "empty", "empty"]
    maze = [[random.choice(room_types) for _ in range(m)] for _ in range(n)]
    maze[0][0] = "empty"
    maze[0][m - 1] = "portal"
    maze[n - 1][0] = "portal"
    maze[n // 2][m // 2] = "key"
    maze[n - 1][m - 1] = "exit"
    return maze


def show_map(maze, visited, x, y):
    print("\nКарта лабиринта:")
    for i in range(len(maze)):
        row = []
        for j in range(len(maze[i])):
            if i == x and j == y:
                row.append("P")
            elif visited[i][j]:
                row.append(maze[i][j][0].upper())
            else:
                row.append("?")
        print(" ".join(row))


def manage_inventory(inventory, sword_damage):
    while True:
        print("\nИнвентарь:", inventory)
        print("Текущий урон меча:", sword_damage)
        print("1 - Сортировать (А-Я)")
        print("2 - Перевернуть порядок")
        print("3 - Выбросить предмет по названию")
        print("4 - Выбросить последний предмет")
        print("5 - Найти ключ в инвентаре")
        print("6 - Усилить меч маной (+10 к урону)")
        print("7 - Показать копию инвентаря (срез)")
        print("0 - Закрыть инвентарь")
        cmd = input("Выберите действие: ")

        if cmd == "1":
            inventory.sort()
            print("Инвентарь отсортирован")
        elif cmd == "2":
            inventory.reverse()
            print("Порядок инвентаря изменен")
        elif cmd == "3":
            item = input("Введите название предмета: ")
            if item in inventory:
                inventory.remove(item)
                print("Предмет выброшен:", item)
            else:
                print("Такого предмета нет")
        elif cmd == "4":
            if len(inventory) > 0:
                removed = inventory.pop()
                print("Выброшен последний предмет:", removed)
            else:
                print("Инвентарь пуст")
        elif cmd == "5":
            if "ключ" in inventory:
                pos = inventory.index("ключ")
                print("Ключ найден в инвентаре на позиции:", pos)
            else:
                print("Ключа пока нет в инвентаре")
        elif cmd == "6":
            if "меч" in inventory and "мана" in inventory:
                inventory.remove("мана")
                sword_damage += 10
                print("Меч усилен! Новый урон:", sword_damage)
            else:
                print("Нужны и 'меч', и 'мана' в инвентаре")
        elif cmd == "7":
            inv_slice = inventory[:]
            long_items = [x for x in inv_slice if len(x) > 3]
            print("Срез инвентаря:", inv_slice)
            print("Предметы длиннее 3 букв:", long_items)
        elif cmd == "0":
            break
        else:
            print("Неверная команда")
    return sword_damage


n = 5
m = 5
maze = create_maze(n, m)
maze_backup = copy.deepcopy(maze)
visited = [[False for _ in range(m)] for _ in range(n)]

x = 0
y = 0
visited[x][y] = True
hp = 100
inventory = ["меч"]
sword_damage = 10

print("=== Игра: Лабиринт ===")
print("Найдите ключ и дойдите до выхода!")

while hp > 0:
    show_map(maze, visited, x, y)
    print(f"Координаты: ({x}, {y}) | Здоровье: {hp} | Инвентарь: {inventory}")
    action = input("Ход (w/a/s/d), инвентарь (i), выход (q): ").lower()

    if action == "q":
        print("Вы вышли из игры")
        break

    if action == "i":
        sword_damage = manage_inventory(inventory, sword_damage)
        continue

    new_x = x
    new_y = y
    if action == "w":
        new_x -= 1
    elif action == "s":
        new_x += 1
    elif action == "a":
        new_y -= 1
    elif action == "d":
        new_y += 1
    else:
        print("Неверная команда")
        continue

    if new_x < 0 or new_x >= n or new_y < 0 or new_y >= m:
        print("Стена! Сюда нельзя пройти.")
        continue

    x = new_x
    y = new_y
    visited[x][y] = True
    room = maze[x][y]

    if room == "empty":
        print("Вы зашли в пустую комнату.")

    elif room == "chest":
        print("Вы нашли сундук!")
        loot_type = random.choice(["empty", "one", "many"])
        if loot_type == "empty":
            print("Сундук оказался пустым.")
        elif loot_type == "one":
            inventory.append("мана")
            print("Внутри лежала 'мана'. Добавлено в инвентарь.")
        else:
            inventory.extend(["зелье", "мана"])
            print("Внутри лежали 'зелье' и 'мана'. Добавлены в инвентарь.")
        maze[x][y] = "empty"

    elif room == "monster":
        print("На вас напал монстр!")
        if sword_damage >= 20:
            print("Ваш усиленный меч быстро победил монстра! Потери HP: 5")
            hp -= 5
        else:
            print("Вы победили монстра, но получили ранение. Потери HP: 20")
            hp -= 20
        maze[x][y] = "empty"

    elif room == "trap":
        print("Вы попали в комнату с ловушкой!")
        choice = input("1 - Перепрыгнуть, 2 - Обойти аккуратно: ")
        if choice == "2":
            print("Вы осторожно обошли ловушку без урона.")
        else:
            print("Ловушка сработала! Потери HP: 15")
            hp -= 15
        maze[x][y] = "empty"

    elif room == "key":
        print("Вы нашли комнату с ключом!")
        if "ключ" not in inventory:
            inventory.append("ключ")
            print("Ключ добавлен в инвентарь.")
        maze[x][y] = "empty"

    elif room == "portal":
        print("Вы вошли в портал и перенеслись в другую часть лабиринта!")
        if x == 0 and y == m - 1:
            x = n - 1
            y = 0
        else:
            x = 0
            y = m - 1
        visited[x][y] = True

    elif room == "exit":
        print("Вы нашли выход из лабиринта!")
        if "ключ" in inventory:
            print("Вы открыли дверь ключом и выбрались! Победа!")
            break
        else:
            print("Дверь закрыта. Сначала найдите ключ!")

    if "зелье" in inventory and hp < 50:
        use = input("Здоровье низкое. Использовать зелье (+30 HP)? (y/n): ").lower()
        if use == "y":
            inventory.remove("зелье")
            hp += 30
            print("Здоровье восстановлено до:", hp)

if hp <= 0:
    print("Ваше здоровье закончилось. Вы проиграли.")
    print("Исходная карта комнат была такой:", maze_backup)
