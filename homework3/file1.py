# -*- coding: utf-8 -*-
import random
import copy

SIZE = 6
WALL = "wall"
START = "start"
EXIT = "exit"

ROOM_TYPES = ["empty", "chest", "monster", "trap", "key", "portal"]

ICONS = {
    "wall":    "🧱",
    "empty":   "⬜",
    "chest":   "📦",
    "monster": "👹",
    "trap":    "⚠️ ",
    "key":     "🔑",
    "portal":  "🌀",
    "start":   "🏁",
    "exit":    "🚪",
    "player":  "🧍",
    "unknown": "❓",
}

LOOT_POOL = [
    "зелье", "меч", "щит", "золото", "серебро", "карта",
    "свиток", "рубин", "амулет", "лук", "броня", "факел"
]


class Item(object):
    def __init__(self, name, power=0):
        self.name = name
        self.power = power

    def __repr__(self):
        return "%s(%d)" % (self.name, self.power) if self.power else self.name

    def __eq__(self, other):
        return isinstance(other, Item) and self.name == other.name

    def __hash__(self):
        return hash(self.name)


class MazeGame(object):
    def __init__(self):
        self.size = SIZE
        self.health = 100
        self.max_health = 100
        self.inventory = []
        self.visited = []
        self.maze = []
        self.pos = (0, 0)
        self.exit_pos = (SIZE - 1, SIZE - 1)
        self.has_key = False
        self.game_over = False
        self.won = False
        self.room_log = []

    # ---------- генерация ----------
    def generate_maze(self):
        self.maze = []
        self.visited = []
        for i in range(self.size):
            row = []
            visited_row = []
            for j in range(self.size):
                if i == 0 or j == 0 or i == self.size - 1 or j == self.size - 1:
                    room_type = WALL
                else:
                    room_type = random.choice(ROOM_TYPES)

                room = {
                    "type": room_type,
                    "visited": False,
                    "items": self._generate_items(room_type),
                    "locked": room_type == "chest" and random.random() < 0.4,
                    "trap_armed": room_type == "trap",
                }
                row.append(room)
                visited_row.append(False)
            self.maze.append(row)
            self.visited.append(visited_row)

        self.maze[1][1]["type"] = START
        self.maze[self.exit_pos[0]][self.exit_pos[1]]["type"] = EXIT

        free_cells = [
            (i, j)
            for i in range(1, self.size - 1)
            for j in range(1, self.size - 1)
            if (i, j) not in [(1, 1), self.exit_pos]
        ]
        kx, ky = random.choice(free_cells)
        self.maze[kx][ky]["type"] = "key"
        self.maze[kx][ky]["items"] = [Item("ключ")]

        self.pos = (1, 1)
        self.visited[1][1] = True

    def _generate_items(self, room_type):
        if room_type == "chest":
            count = random.randint(0, 3)
            names = random.sample(LOOT_POOL, count)
            return [Item(n, random.randint(1, 10)) for n in names]
        if room_type == "monster":
            return [Item("золото", random.randint(5, 20))]
        return []

    # ---------- отображение ----------
    def show_map(self):
        print("\n" + "=" * 50)
        print("🗺️  ЛАБИРИНТ СПИСКОВ")
        print("=" * 50)
        for i in range(self.size):
            line = ""
            for j in range(self.size):
                if (i, j) == self.pos:
                    line += ICONS["player"] + " "
                elif self.visited[i][j]:
                    t = self.maze[i][j]["type"]
                    line += ICONS.get(t, "? ") + " "
                else:
                    line += ICONS["unknown"] + " "
            print(line)

    def show_status(self):
        print("\n❤️  HP: %d/%d" % (self.health, self.max_health))
        print("🎒 Инвентарь: %s" % (self.inventory if self.inventory else 'пусто'))
        print("🔑 Ключ: %s" % ('ЕСТЬ' if self.has_key else 'НЕТ'))
        print("📍 Позиция: %s" % (self.pos,))

    # ---------- события ----------
    def enter_room(self):
        x, y = self.pos
        room = self.maze[x][y]
        rtype = room["type"]

        if rtype == WALL:
            print("🧱 Здесь стена. Дальше не пройти.")
            return

        if not room["visited"]:
            room["visited"] = True
            self.visited[x][y] = True
            self.room_log.append(rtype)
            print("\n>>> Комната: %s" % rtype)

            if rtype == "monster":
                self.fight_monster()
            elif rtype == "trap":
                self.trigger_trap(room)
            elif rtype == "portal":
                self.use_portal()
            elif rtype == "chest":
                self.open_chest(room)
            elif rtype == "key":
                self.collect_items(room)
                self.has_key = True
                print("🔑 Вы нашли КЛЮЧ! Теперь можно выйти из лабиринта!")
            elif rtype == "exit":
                self.try_exit()
            elif rtype == "empty":
                if room["items"]:
                    self.collect_items(room)
        else:
            print("\nВы уже были здесь (%s)." % rtype)

    def open_chest(self, room):
        if room.get("locked") and not self.has_key:
            print("📦 Сундук заперт! Нужен ключ.")
            return
        if room["locked"] and self.has_key:
            print("📦 Вы открыли сундук ключом!")
            room["locked"] = False

        if not room["items"]:
            print("📦 Сундук пуст...")
            return
        self.collect_items(room)

    def collect_items(self, room):
        items = room["items"]
        if not items:
            return
        print("Найдены предметы: %s" % items)
        choice = input("Собрать? (да/нет): ").strip().lower()
        if choice not in ("да", "д", "y", "yes"):
            return

        if len(items) == 1:
            self.inventory.append(items[0])
            print("➕ Добавлен: %s" % items[0])
        else:
            self.inventory.extend(items)
            print("➕ Добавлены: %s" % items)

        if any(it.name == "ключ" for it in items):
            self.has_key = True
            print("🔑 Ключ добавлен в инвентарь!")

        room["items"] = []

    def fight_monster(self):
        monster_hp = random.randint(20, 40)
        print("👹 Монстр! HP: %d" % monster_hp)

        while monster_hp > 0 and self.health > 0:
            print("\nМонстр: %d HP | Вы: %d HP" % (monster_hp, self.health))
            action = input("1-атака, 2-зелье, 3-бежать: ").strip()

            if action == "1":
                base = random.randint(5, 12)
                swords = [it for it in self.inventory if it.name == "меч"]
                bonus = sum(it.power for it in swords)
                dmg = base + bonus
                monster_hp -= dmg
                print("⚔️  Вы нанесли %d урона (база %d + бонус %d)" % (dmg, base, bonus))

            elif action == "2":
                if self.use_potion():
                    continue
                else:
                    print("Нет зелья!")

            elif action == "3":
                if random.random() < 0.5:
                    print("🏃 Вы сбежали!")
                    return
                print("Не удалось сбежать!")

            if monster_hp > 0:
                hit = random.randint(5, 12)
                self.health -= hit
                print("👹 Монстр бьёт на %d" % hit)

        if monster_hp <= 0:
            print("✅ Монстр побеждён!")
            reward = [Item("золото", random.randint(5, 20))]
            self.inventory.extend(reward)
            print("💰 Получено: %s" % reward)

    def trigger_trap(self, room):
        if not room["trap_armed"]:
            return
        dmg = random.randint(8, 20)
        if any(it.name == "щит" for it in self.inventory):
            dmg //= 2
            print("🛡️  Щит смягчил удар!")
        self.health -= dmg
        room["trap_armed"] = False
        print("⚠️  Ловушка! -%d HP" % dmg)

    def use_portal(self):
        print("🌀 Портал засасывает вас...")
        candidates = [
            (i, j)
            for i in range(1, self.size - 1)
            for j in range(1, self.size - 1)
            if self.maze[i][j]["type"] != WALL and (i, j) != self.pos
        ]
        self.pos = random.choice(candidates)
        print("📍 Вы оказались в %s" % (self.pos,))

    def try_exit(self):
        if self.has_key:
            print("🎉 ВЫ ОТКРЫЛИ ВЫХОД И ПОБЕДИЛИ! 🎉")
            self.won = True
            self.game_over = True
        else:
            print("🚪 Выход заперт. Нужен ключ!")

    def use_potion(self):
        potions = [it for it in self.inventory if it.name == "зелье"]
        if not potions:
            return False
        potion = potions[0]
        self.inventory.remove(potion)
        self.health = min(self.max_health, self.health + 30)
        print("🧪 +30 HP")
        return True

    # ---------- инвентарь ----------
    def inventory_menu(self):
        while True:
            print("\n" + "-" * 40)
            print("🎒 ИНВЕНТАРЬ")
            print("-" * 40)
            print("%s" % (self.inventory if self.inventory else 'пусто'))
            print("\n1 - Сортировать (по имени)")
            print("2 - Сортировать (по силе) + reverse")
            print("3 - Выбросить по имени (remove)")
            print("4 - Выбросить по индексу (pop)")
            print("5 - Найти предмет (index / in)")
            print("6 - Копировать (copy / deepcopy) и изменить")
            print("7 - Срез (slice) первых 3 предметов")
            print("8 - Изменить свойство предмета (усилить меч)")
            print("0 - Назад")

            c = input("Выбор: ").strip()

            if c == "1":
                self.inventory.sort(key=lambda it: it.name)
                print("✅ Отсортировано по имени.")
            elif c == "2":
                self.inventory.sort(key=lambda it: it.power)
                self.inventory.reverse()
                print("✅ Отсортировано по силе (убывание).")
            elif c == "3":
                name = input("Что выбросить? ").strip()
                found = None
                for it in self.inventory:
                    if it.name == name:
                        found = it
                        break
                if found:
                    self.inventory.remove(found)
                    print("🗑️  Удалён: %s" % found)
                else:
                    print("Нет такого предмета.")
            elif c == "4":
                try:
                    idx = int(input("Индекс (0..%d): " % (len(self.inventory) - 1)))
                    removed = self.inventory.pop(idx)
                    print("🗑️  Удалён: %s" % removed)
                except (ValueError, IndexError):
                    print("Неверный индекс.")
            elif c == "5":
                name = input("Что искать? ").strip()
                names = [it.name for it in self.inventory]
                if name in names:
                    idx = names.index(name)
                    print("🔎 Найдено на позиции %d: %s" % (idx, self.inventory[idx]))
                else:
                    print("Не найдено.")
            elif c == "6":
                self.copy_demo()
            elif c == "7":
                print("✂️  Первые 3: %s" % (self.inventory[:3],))
            elif c == "8":
                self.upgrade_item()
            elif c == "0":
                return
            else:
                print("Неверный выбор.")

    def copy_demo(self):
        if not self.inventory:
            print("Инвентарь пуст.")
            return
        print("\n--- Демонстрация копирования ---")
        shallow = self.inventory.copy()
        if shallow:
            shallow[0].power += 100
            print("shallow copy[0] = %s" % shallow[0])
            print("оригинал[0]     = %s  <-- изменился! (общая ссылка)" % self.inventory[0])

        deep = copy.deepcopy(self.inventory)
        if deep:
            deep[0].power += 50
            print("deep copy[0]    = %s" % deep[0])
            print("оригинал[0]     = %s  <-- НЕ изменился" % self.inventory[0])

    def upgrade_item(self):
        swords = [it for it in self.inventory if it.name == "меч"]
        if not swords:
            print("Нет меча для улучшения.")
            return
        sword = swords[0]
        sword.power += 10
        print("⚒️  Меч усилен! Теперь сила = %d" % sword.power)

    # ---------- перемещение ----------
    def move(self, cmd):
        moves = {"w": (-1, 0), "s": (1, 0), "a": (0, -1), "d": (0, 1)}
        if cmd not in moves:
            return False
        dx, dy = moves[cmd]
        nx, ny = self.pos[0] + dx, self.pos[1] + dy
        if 0 <= nx < self.size and 0 <= ny < self.size:
            self.pos = (nx, ny)
        else:
            print("Там стена!")
        return True

    # ---------- главный цикл ----------
    def play(self):
        print("=" * 50)
        print("🏰 ДОБРО ПОЖАЛОВАТЬ В ЛАБИРИНТ СПИСКОВ!")
        print("=" * 50)
        print("Цель: найти ключ 🔑 и добраться до выхода 🚪.")
        print("Управление: w/a/s/d, i — инвентарь, q — выход.")
        print("Периметр — стены 🧱, за них не выйти.\n")

        self.generate_maze()

        while not self.game_over:
            self.show_map()
            self.show_status()
            self.enter_room()

            if self.game_over:
                break
            if self.health <= 0:
                print("\n💀 Вы погибли...")
                break

            cmd = input("\nКоманда (w/a/s/d, i, q): ").strip().lower()
            if cmd == "q":
                print("Выход из игры.")
                break
            elif cmd == "i":
                self.inventory_menu()
            else:
                self.move(cmd)

        if self.won:
            print("\n🏆 ИТОГ: ПОБЕДА!")
            print("Посещено комнат: %d" % len(self.room_log))
            print("Инвентарь на финише: %s" % self.inventory)
        elif self.health <= 0:
            print("\n💀 ИТОГ: ПОРАЖЕНИЕ.")


if __name__ == "__main__":
    game = MazeGame()
    game.play()
