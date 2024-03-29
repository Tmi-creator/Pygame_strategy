class Building():  # родительский класс здания
    def __init__(self, x, y, landscape_before, hp, cost, income, landscape, resource, level):
        self.hp = hp  # int
        self.x = x  # int
        self.y = y  # int
        self.cost = cost  # [wood, gold]
        self.income = income  # [+, -]
        self.resource = resource  # [res1, res2]
        self.landscape = landscape  # где стаивтся, ['lanscape1', 'landscape2']
        self.level = level  # int
        self.landscape_before = landscape_before  # где поставили, str
        self.max_hp = hp

    def destroy(self):  # бабах
        return self.landscape_before


# cost [wood, gold]
# внизу просто классы зданий
class Capital(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y, landscape_before, 50, [0, 0], [50, -5],
                          ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                          ['gold', 'food'], 1)

    def __str__(self):
        return f'{self.x}, {self.y}'


class City(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y, landscape_before, 500, [0, 0], [25, -5],
                          ['1', '2', '3', '4', '5', '6', '7', '8', '9'],
                          ['gold', 'food'], 1)


class Sawmill(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y, landscape_before, 200, [0, 0], [25, -5], ['2'], ['wood', 'gold'], 1)


class Farm(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        self.income = [25 * (int(landscape_before) // 2 + int(landscape_before) % 2), -5]
        Building.__init__(self, x, y, landscape_before, 200, [0, 0], self.income, ['1', '4'], ['food', 'gold'], 1)


class FishFarm(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y, landscape_before, 300, [0, 0], [15, -5], ['0'], ['food', 'gold'], 1)


class StoneMine(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        self.income = [10 * int(landscape_before), -10]
        Building.__init__(self, x, y, landscape_before, 400, [0, 0], self.income, ['3', '5'], ['stone', 'gold'], 1)


class MetalMine(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y, landscape_before, 400, [0, 0], [50, -15], ['6'], ['metal', 'gold'], 1)


class PlatinumMine(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y, landscape_before, 400, [0, 0], [10, -50], ['9'], ['platinum', 'gold'], 1)


class SuperMine(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y, landscape_before, 400, [0, 0], [75, 50, 100], ['7'], ['stone', 'metal', 'gold'], 1)


class Shipyard(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y, landscape_before, 50, [0, 0], [-15], ['0'], ['gold'], 1)


class Tower(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y, landscape_before, 500, [0, 0], [-10], ['1', '2', '3', '4', '5', '6', '7', '8', '9'], ['gold'],
                          1)
        self.atk = 50
        self.range = 5
        self.target = 'none'
        self.can_attack = True

    def attack(self):
        if abs(self.target.x - self.x) <= self.range and abs(self.target.y - self.y) <= self.range:
            self.target.hp -= self.atk
            if self.target.hp <= 0:
                self.target = 'none'


class Wall(Building):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Building.__init__(self, x, y,landscape_before, 1200, [0, 0], [-5], ['1', '2', '3', '4', '5', '6', '7', '8', '9'], ['gold'], 1)


class Lab(Building):
    def __init__(self, x = -1000, y = -1000, landscape_before = -1):
        Building.__init__(self, x, y, landscape_before, 250, [0, 0], [-20], ['8'], ['gold'], 1)


class Unit():  # родительский класс юнита
    def __init__(self, x, y, hp, cost, income, atk, speed, range, level, landscape_before, can_move=True, can_attack=True):
        self.hp = hp  # int
        self.x = x  # int
        self.y = y  # int
        self.cost = cost  # [wood, gold, metal]
        self.income = income  # [int], сколько кушает юнит
        self.resource = ['gold']
        self.atk = atk  # int
        self.speed = speed  # int
        self.level = level  # int
        self.landscape_before = landscape_before  # str, на какой клетке стоит юнит. нужен, чтобы не уничтожать землю своим присутствием
        self.range = range  # int
        self.can_move = can_move
        self.can_attack = can_attack
        self.max_hp = hp
        self.landscape = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def attack(self, target):  # бьем кого-то
        if abs(target.x - self.x) <= self.range and abs(target.y - self.y) <= self.range:
            target.hp -= self.atk

    def destroy(self):  # кнопка самоуничтожения должна быть у всех
        return self.landscape_before

    # def move(x1, y1):
    #     if abs(x1 - self.x) <= self.speed and abs(y1 - self.y) <= self.speed:
    #         self.x = x1
    #         self.y = y1


# cost [wood, gold, metal]

class Cruiser(Unit):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        self.landscape_before = landscape_before
        Unit.__init__(self, x, y, 150, [0, 0, 0], [-25], 75, 3, 4, 1, landscape_before)


class Explorer(Unit):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Unit.__init__(self, x, y, 50, [0, 0, 0], [-50], 50, 4, 2, 1, landscape_before)
        self.landscape_before = landscape_before


class Artillery(Unit):
    def __init__(self, x=-1000, y=-1000, landscape_before=-1):
        Unit.__init__(self, x, y, 100, [0, 0, 0], [-50], 100, 2, 7, 1, landscape_before)
        self.landscape_before = landscape_before
