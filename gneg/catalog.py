"""The terrain, economy and unit catalog shared by the rules and the interface."""

from dataclasses import dataclass

COLS, ROWS = 24, 16
ACTIONS = 3
RESOURCES = ("wood", "stone", "gold", "metal", "food", "platinum")
RESOURCE_NAMES = dict(zip(RESOURCES, ("Дерево", "Камень", "Золото", "Металл", "Провизия", "Платина")))
INITIAL_STOCK = dict(zip(RESOURCES, (65, 25, 75, 15, 35, 0)))
FACTIONS = ("Северный союз", "Южная лига")
TERRAIN = {
    "~": "Море", ".": "Равнина", "f": "Лес", "h": "Холмы", "b": "Чернозём",
    "m": "Горы", "c": "Пещеры", "r": "Руины", "p": "Платиновая жила",
    "v": "Богатая жила",
}

# The opposite shore is the same layout rotated by 180 degrees.
WEST = (
    "~~~~~~~~~~~~",
    "~~~~~~~~~~~~",
    "~~f..~~~~~~~",
    "~.ff..~~~~~~",
    "~fhcm.f~~~~~",
    "~.b.f..~~~~~",
    "~..h...~~~~~",
    "~~f.b..~~~.f",
    "~~..f.~f~~.r",
    "~~~...~.~~~.",
    "~~~~~~.h~~~~",
    "~f.~~~rf~~~~",
    "~p..~~~~~~~~",
    "~~.~~~~~~~~~",
    "~~~~~~~~~~~~",
    "~~~~~~~~~~~~",
)
START_CAPITALS = ((4, 6), (19, 9))
START_YARDS = ((7, 6), (16, 9))
START_SHIPS = ((8, 6), (15, 9))


def make_map():
    terrain = [list(row + WEST[ROWS - 1 - y][::-1]) for y, row in enumerate(WEST)]
    for x, y in ((9, 2), (10, 3), (10, 12), (11, 11), (8, 10)):
        terrain[y][x] = "v" if x == 11 else "h" if x == 10 else "."
        terrain[ROWS - 1 - y][COLS - 1 - x] = terrain[y][x]
    return tuple("".join(row) for row in terrain)


@dataclass(frozen=True)
class PieceType:
    name: str
    description: str
    hp: int
    terrain: str
    cost: tuple = ()
    income: tuple = ()
    sight: int = 2
    claims: int = 0
    speed: int = 0
    reach: int = 0
    damage: int = 0


LAND = ".fhbmcrpv"
PIECES = {
    "capital": PieceType("Столица", "Потеря столицы решает исход партии.", 220, LAND,
                         income=(("wood", 8), ("gold", 23), ("food", 6)), sight=6, claims=3),
    "city": PieceType("Город", "Расширяет границы и приносит золото.", 100, LAND,
                      (("wood", 28), ("gold", 25)), (("gold", 13),), sight=4, claims=2),
    "sawmill": PieceType("Лесопилка", "Заготовляет дерево в лесу.", 65, "f",
                         (("wood", 12), ("gold", 12)), (("wood", 18),)),
    "farm": PieceType("Ферма", "Снабжает поселения и флот провизией.", 55, ".b",
                      (("wood", 14), ("gold", 10)), (("food", 14),)),
    "fishery": PieceType("Рыбный промысел", "Приносит провизию с моря.", 55, "~",
                         (("wood", 14), ("gold", 13)), (("food", 11),)),
    "quarry": PieceType("Каменоломня", "Добывает камень для укреплений.", 70, "hm",
                        (("wood", 18), ("gold", 16)), (("stone", 12),)),
    "mine": PieceType("Рудник", "Снабжает верфи металлом.", 70, "c",
                      (("wood", 22), ("gold", 22)), (("metal", 12),)),
    "platinum": PieceType("Платиновая шахта", "Платина нужна для улучшений III уровня.", 70, "p",
                          (("wood", 26), ("gold", 30)), (("platinum", 5),)),
    "deep_mine": PieceType("Глубокая шахта", "Приносит камень, металл и немного платины.", 82, "v",
                           (("wood", 28), ("gold", 28)), (("stone", 10), ("metal", 8), ("platinum", 2))),
    "shipyard": PieceType("Верфь", "Спускает корабли на воду у причала.", 100, "~",
                          (("wood", 32), ("gold", 32)), sight=4),
    "tower": PieceType("Башня", "Стреляет по ближайшему противнику в конце вашего хода.", 110, LAND,
                       (("wood", 16), ("stone", 28), ("gold", 22)), sight=5, reach=3, damage=32),
    "wall": PieceType("Форт", "Защищает соседние здания в радиусе одной клетки.", 160, LAND,
                      (("stone", 22), ("gold", 14))),
    "lab": PieceType("Академия", "Снижает цену улучшений по золоту вдвое.", 60, "hrp",
                     (("wood", 20), ("gold", 32))),
    "explorer": PieceType("Разведчик", "Разведывает море и позволяет основать город на берегу.", 65, "~",
                          (("wood", 22), ("gold", 20), ("food", 6)), sight=6, claims=1,
                          speed=4, reach=2, damage=22),
    "cruiser": PieceType("Фрегат", "Основной корабль флота. Может двигаться и стрелять за один ход.", 105, "~",
                         (("wood", 34), ("gold", 39), ("metal", 8), ("food", 9)), sight=5,
                         speed=3, reach=4, damage=42),
    "artillery": PieceType("Бомбардир", "Особенно эффективен при обстреле островных укреплений.", 80, "~",
                           (("wood", 30), ("gold", 48), ("metal", 17), ("food", 8)), sight=6,
                           speed=2, reach=6, damage=50),
}

BUILD_GROUPS = {
    "Промыслы": ("city", "sawmill", "farm", "fishery", "quarry", "mine", "platinum", "deep_mine"),
    "Укрепления": ("shipyard", "tower", "wall", "lab"),
    "Флот": ("explorer", "cruiser", "artillery"),
}
