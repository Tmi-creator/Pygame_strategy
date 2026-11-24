"""Research definitions. The catalog drives both the tree and its prerequisites."""

from dataclasses import dataclass

BEACONS = ((10, 3), (13, 12))
CONTROL_TURNS = 3
INITIAL_SCIENCE = 3


@dataclass(frozen=True)
class Technology:
    key: str
    name: str
    effect: str
    cost: int
    requires: str | None = None


@dataclass(frozen=True)
class ResearchBranch:
    name: str
    colour: tuple[int, int, int]
    technologies: tuple[Technology, ...]


BRANCHES = (
    ResearchBranch("Экономика", (232, 190, 112), (
        Technology("workshops", "Мастерские",
                   "Лесопилки, каменоломни и рудники дают ещё 4 единицы своего ресурса.", 3),
        Technology("free_ports", "Вольные порты",
                   "Города дают ещё 6 золота и расширяют границы на одну клетку.", 5, "workshops"),
        Technology("mobilization", "Мобилизация",
                   "Начинайте ход с четырьмя действиями, пока у вас есть два города.", 8, "free_ports"),
    )),
    ResearchBranch("Флот", (111, 207, 218), (
        Technology("charts", "Морские карты",
                   "Корабли видят на клетку дальше. Разведчики ходят на пять клеток.", 3),
        Technology("long_guns", "Дальнобойные орудия",
                   "Фрегаты и бомбардиры могут атаковать на клетку дальше.", 5, "charts"),
        Technology("formation", "Эскадренный огонь",
                   "Корабль наносит ещё 12 урона, если в двух клетках есть союзный корабль.", 8, "long_guns"),
    )),
    ResearchBranch("Оборона", (229, 151, 128), (
        Technology("masonry", "Каменная кладка",
                   "Форты поглощают 20 урона по соседним зданиям вместо 12.", 3),
        Technology("field_service", "Полевые мастерские",
                   "Ремонт даёт до 60 ОЗ. Корабли можно чинить и внутри своих границ.", 5, "masonry"),
        Technology("crossfire", "Перекрёстный огонь",
                   "Башни бьют на клетку дальше и раз за ход врага перехватывают корабль после манёвра.",
                   8, "field_service"),
    )),
)
TECHNOLOGIES = {tech.key: tech for branch in BRANCHES for tech in branch.technologies}
CAPSTONES = {branch.technologies[-1].key for branch in BRANCHES}
