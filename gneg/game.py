"""Authoritative match state. The AI and UI use exactly the same commands."""

from collections import deque
from dataclasses import dataclass
from typing import Literal

from .catalog import (
    ACTIONS, COLS, FACTIONS, INITIAL_STOCK, PIECES, RESOURCES, ROWS, START_CAPITALS,
    START_SHIPS, START_YARDS, TERRAIN, make_map,
)
from .research import BEACONS, CAPSTONES, CONTROL_TURNS, INITIAL_SCIENCE, TECHNOLOGIES

Position = tuple[int, int]
Mode = Literal["solo", "hotseat"]


def distance(a: Position, b: Position) -> int:
    return max(abs(a[0] - b[0]), abs(a[1] - b[1]))


def inside(pos: Position) -> bool:
    return 0 <= pos[0] < COLS and 0 <= pos[1] < ROWS


def area(pos: Position, radius: int):
    x, y = pos
    for yy in range(max(0, y - radius), min(ROWS, y + radius + 1)):
        for xx in range(max(0, x - radius), min(COLS, x + radius + 1)):
            yield xx, yy


@dataclass
class Piece:
    kind: str
    owner: int
    pos: Position
    hp: int
    level: int = 1
    moved: bool = False
    fired: bool = False
    repaired: bool = False
    intercepted: bool = False

    @property
    def spec(self):
        return PIECES[self.kind]

    @property
    def max_hp(self):
        return self.spec.hp + (self.level - 1) * (self.spec.hp // 4)

    @property
    def damage(self):
        return self.spec.damage + (self.level - 1) * (self.spec.damage // 4)


@dataclass(frozen=True)
class Event:
    text: str
    audience: tuple[int, ...]
    origin: Position | None = None
    target: Position | None = None
    effect: str = ""


REPAIR_COST = (("wood", 10), ("gold", 12))
WORKSHOP_RESOURCES = {"sawmill": "wood", "quarry": "stone", "mine": "metal"}


class Game:
    def __init__(self, mode: Mode):
        self.mode = mode
        self.map = make_map()
        self.pieces: dict[Position, Piece] = {}
        self.stock = [INITIAL_STOCK.copy(), INITIAL_STOCK.copy()]
        self.seen: list[set[Position]] = [set(), set()]
        self.visible: list[set[Position]] = [set(), set()]
        self.territory: dict[Position, int] = {}
        self.events: list[Event] = []
        self.active = 0
        self.round = 1
        self.actions = ACTIONS
        self.turn_capacity = ACTIONS
        self.science = [INITIAL_SCIENCE, INITIAL_SCIENCE]
        self.researched: list[set[str]] = [set(), set()]
        self.control = [0, 0]
        self.win_reason = ""
        self.winner: int | None = None
        for owner in range(2):
            self._spawn("capital", owner, START_CAPITALS[owner])
            self._spawn("shipyard", owner, START_YARDS[owner])
            self._spawn("cruiser", owner, START_SHIPS[owner])
        self._update_map()
        self._record("Флот готов к выходу в море.", (0, 1))

    def terrain_at(self, pos: Position) -> str:
        return self.map[pos[1]][pos[0]]

    def _spawn(self, kind: str, owner: int, pos: Position) -> Piece:
        piece = Piece(kind, owner, pos, PIECES[kind].hp)
        self.pieces[pos] = piece
        return piece

    def _update_map(self, *, announce=True):
        previous = [self.owned_beacons(side) for side in range(2)]
        claims: list[dict[Position, int]] = [{}, {}]
        self.visible = [set(), set()]
        for piece in self.pieces.values():
            self.visible[piece.owner].update(area(piece.pos, self.sight(piece)))
            claims_radius = piece.spec.claims + int(piece.kind == "city" and self.has_tech(piece.owner, "free_ports"))
            if claims_radius:
                for pos in area(piece.pos, claims_radius):
                    strength = claims_radius + 1 - distance(piece.pos, pos)
                    own = claims[piece.owner]
                    own[pos] = max(own.get(pos, 0), strength)
        self.territory = {}
        for pos in claims[0].keys() | claims[1].keys():
            left, right = (side.get(pos, 0) for side in claims)
            if left != right:
                self.territory[pos] = int(right > left)
        for owner in range(2):
            self.seen[owner].update(self.visible[owner])
        if announce:
            self._update_control(previous)

    def has_tech(self, side: int, key: str) -> bool:
        return key in self.researched[side]

    def owned_beacons(self, side: int):
        return tuple(pos for pos in BEACONS if self.territory.get(pos) == side)

    def has_academy(self, side: int) -> bool:
        return any(p.kind == "lab" and p.owner == side for p in self.pieces.values())

    def science_income(self, side: int) -> int:
        return 1 + int(self.has_academy(side)) + len(self.owned_beacons(side))

    def research_error(self, key: str, side: int) -> str:
        if key not in TECHNOLOGIES:
            return "Неизвестная технология."
        if self.has_tech(side, key):
            return "Уже изучено."
        tech = TECHNOLOGIES[key]
        if tech.requires and not self.has_tech(side, tech.requires):
            return "Требуется: " + TECHNOLOGIES[tech.requires].name + "."
        if key in CAPSTONES:
            if self.researched[side] & CAPSTONES:
                return "Специализация уже выбрана."
            if not self.has_academy(side):
                return "Нужна академия."
        if self.science[side] < tech.cost:
            return "Недостаточно науки."
        if side != self.active:
            return "Исследование доступно в свой ход."
        return self.can_act()

    def research(self, key: str) -> str:
        if error := self.research_error(key, self.active):
            return error
        tech = TECHNOLOGIES[key]
        self.science[self.active] -= tech.cost
        self.researched[self.active].add(key)
        self._spend()
        self._update_map()
        self._record(f"Исследование завершено · {tech.name}.", (self.active,), effect="research")
        return ""

    def sight(self, piece: Piece) -> int:
        return piece.spec.sight + int(bool(piece.spec.speed) and self.has_tech(piece.owner, "charts"))

    def speed(self, piece: Piece) -> int:
        return piece.spec.speed + int(piece.kind == "explorer" and self.has_tech(piece.owner, "charts"))

    def reach(self, piece: Piece) -> int:
        bonus = (piece.kind in ("cruiser", "artillery") and self.has_tech(piece.owner, "long_guns")) or (
            piece.kind == "tower" and self.has_tech(piece.owner, "crossfire")
        )
        return piece.spec.reach + int(bonus)

    def firepower(self, piece: Piece) -> int:
        supports = piece.spec.speed and self.has_tech(piece.owner, "formation") and any(
            ally is not piece and ally.owner == piece.owner and ally.spec.speed and distance(ally.pos, piece.pos) <= 2
            for ally in self.pieces.values()
        )
        return piece.damage + (12 if supports else 0)

    def _update_control(self, previous):
        for side in range(2):
            current = self.owned_beacons(side)
            if len(current) < len(BEACONS):
                self.control[side] = 0
            if current != previous[side]:
                self._record(f"{FACTIONS[side]} · маяки под контролем: {len(current)}/{len(BEACONS)}.", (0, 1))

    def _record(self, text, audience, origin=None, target=None, effect=""):
        self.events.append(Event(text, tuple(audience), origin, target, effect))
        if len(self.events) > 80:
            del self.events[:-80]

    def can_act(self) -> str:
        if self.winner is not None:
            return "Партия завершена."
        if not self.actions:
            return "Действия закончились. Передайте ход."
        return ""

    def afford(self, cost) -> bool:
        return all(self.stock[self.active][key] >= value for key, value in cost)

    def _spend(self, cost=()):
        for key, value in cost:
            self.stock[self.active][key] -= value
        self.actions -= 1

    def build_error(self, kind: str, pos: Position) -> str:
        if error := self.can_act():
            return error
        if kind not in PIECES or kind == "capital":
            return "Этот объект нельзя построить."
        if pos not in self.visible[self.active]:
            return "Эту клетку нужно разведать."
        if pos in self.pieces:
            return "Клетка занята."
        if pos in BEACONS:
            return "Маяк занимает эту клетку. Расширьте границы до маяка, чтобы взять его под контроль."
        spec = PIECES[kind]
        terrain = self.terrain_at(pos)
        if terrain not in spec.terrain:
            return "Подходит местность: " + ", ".join(TERRAIN[key].lower() for key in spec.terrain) + "."
        if spec.speed:
            if not any(
                piece.owner == self.active and piece.kind == "shipyard" and
                abs(piece.pos[0] - pos[0]) + abs(piece.pos[1] - pos[1]) == 1
                for piece in self.pieces.values()
            ):
                return "Выберите свободное море рядом со своей верфью."
        elif self.territory.get(pos) != self.active:
            return "Строить можно в своих границах. Разведчик помогает основать город на новом берегу."
        elif kind == "shipyard" and not any(
            self.terrain_at(cell) != "~" for cell in area(pos, 1)
            if abs(cell[0] - pos[0]) + abs(cell[1] - pos[1]) == 1
        ):
            return "Верфь строится в море у берега."
        if not self.afford(spec.cost):
            return "Не хватает ресурсов."
        return ""

    def build(self, kind: str, pos: Position) -> str:
        if error := self.build_error(kind, pos):
            return error
        piece = self._spawn(kind, self.active, pos)
        self._spend(piece.spec.cost)
        self._update_map()
        self._record(f"{piece.spec.name}: строительство завершено.", (self.active,), target=pos, effect="build")
        return ""

    def reachable(self, piece: Piece) -> dict[Position, int]:
        """Shortest water routes, with occupied cells and corners blocking passage."""
        speed = self.speed(piece)
        depth = {piece.pos: 0}
        queue = deque([piece.pos])
        while queue:
            here = queue.popleft()
            steps = depth[here] + 1
            if steps > speed:
                continue
            for pos in self.water_neighbors(here, piece):
                if pos in depth:
                    continue
                depth[pos] = steps
                queue.append(pos)
        del depth[piece.pos]
        return depth

    def water_neighbors(self, here, piece):
        for pos in area(here, 1):
            if pos == here or (pos != piece.pos and not self.open_water(pos, piece.owner)):
                continue
            x, y = pos
            if x != here[0] and y != here[1] and not (
                self.open_water((here[0], y), piece.owner) or self.open_water((x, here[1]), piece.owner)
            ):
                continue
            yield pos

    def open_water(self, pos, owner):
        return self.terrain_at(pos) == "~" and (pos not in self.pieces or pos not in self.visible[owner])

    def move(self, start: Position, end: Position) -> str:
        if error := self.can_act():
            return error
        piece = self.pieces.get(start)
        if piece is None or piece.owner != self.active or not piece.spec.speed:
            return "Выберите свой корабль."
        if piece.moved:
            return "Этот корабль уже двигался в текущем ходу."
        if end not in self.reachable(piece) or end in self.pieces:
            return "До этой клетки нельзя доплыть за одно действие."
        del self.pieces[start]
        piece.pos, piece.moved = end, True
        self.pieces[end] = piece
        self._spend()
        self._update_map()
        self._record(f"{piece.spec.name} сменил позицию.", (piece.owner,), start, end, "move")
        self._intercept(piece)
        return ""

    def _intercept(self, ship: Piece):
        opponent = 1 - ship.owner
        if not self.has_tech(opponent, "crossfire"):
            return
        towers = [tower for tower in self.pieces.values() if tower.kind == "tower" and tower.owner == opponent]
        for tower in towers:
            if not tower.intercepted and ship in self.targets(tower):
                tower.intercepted = True
                self._strike(tower, ship)
                if ship.hp <= 0:
                    return

    def targets(self, attacker: Piece) -> list[Piece]:
        return [
            piece for piece in self.pieces.values()
            if piece.owner != attacker.owner and piece.pos in self.visible[attacker.owner]
            and distance(attacker.pos, piece.pos) <= self.reach(attacker)
        ]

    def attack(self, start: Position, end: Position) -> str:
        if error := self.can_act():
            return error
        attacker = self.pieces.get(start)
        if attacker is None or attacker.owner != self.active or not attacker.spec.speed:
            return "Выберите свой боевой корабль."
        if attacker.fired:
            return "Этот корабль уже атаковал в текущем ходу."
        target = self.pieces.get(end)
        if target is None or target not in self.targets(attacker):
            return "Выберите видимого противника в радиусе атаки."
        attacker.fired = True
        self._spend()
        self._strike(attacker, target)
        return ""

    def _strike(self, attacker: Piece, target: Piece):
        fortified = not target.spec.speed and target.kind != "wall" and any(
            fort.kind == "wall" and fort.owner == target.owner and distance(fort.pos, target.pos) == 1
            for fort in self.pieces.values()
        )
        reduction = (20 if self.has_tech(target.owner, "masonry") else 12) if fortified else 0
        damage = max(1, self.firepower(attacker) - reduction)
        target.hp -= damage
        self._record(f"{attacker.spec.name} → {target.spec.name} · −{damage} ОЗ",
                     (0, 1), attacker.pos, target.pos, "hit")
        if target.hp <= 0:
            del self.pieces[target.pos]
            if target.kind == "capital":
                self.winner = attacker.owner
                self.win_reason = "capital"
                self._record(f"{FACTIONS[attacker.owner]} одерживает победу.", (0, 1), target=target.pos)
            self._update_map()

    def upgrade_cost(self, piece: Piece):
        has_lab = self.has_academy(piece.owner)
        gold = 20 if piece.level == 1 else 36
        cost = (("stone", 14 * piece.level), ("gold", gold // 2 if has_lab else gold))
        return cost + ((("platinum", 4),) if piece.level == 2 else ())

    def upgrade(self, pos: Position) -> str:
        if error := self.can_act():
            return error
        piece = self.pieces.get(pos)
        if piece is None or piece.owner != self.active:
            return "Улучшать можно только свои объекты."
        if piece.level >= 3:
            return "Достигнут максимальный уровень."
        cost = self.upgrade_cost(piece)
        if not self.afford(cost):
            return "Не хватает ресурсов для улучшения."
        old_hp = piece.max_hp
        piece.level += 1
        piece.hp += piece.max_hp - old_hp
        self._spend(cost)
        self._record(f"{piece.spec.name}: уровень {piece.level}.", (piece.owner,), target=pos, effect="build")
        return ""

    def repair(self, pos: Position) -> str:
        if error := self.can_act():
            return error
        piece = self.pieces.get(pos)
        if piece is None or piece.owner != self.active or piece.hp == piece.max_hp:
            return "Выберите свой повреждённый объект."
        if piece.repaired:
            return "Этот объект уже ремонтировали в текущем ходу."
        field_service = self.has_tech(piece.owner, "field_service")
        in_supply = field_service and self.territory.get(pos) == piece.owner
        if piece.spec.speed and not in_supply and not any(
            p.kind == "shipyard" and p.owner == piece.owner and distance(p.pos, pos) <= 2
            for p in self.pieces.values()
        ):
            return "Для ремонта подведите корабль к верфи или войдите в свои границы с полевыми мастерскими."
        if not self.afford(REPAIR_COST):
            return "Для ремонта нужны 10 дерева и 12 золота."
        repaired = min(60 if field_service else 46, piece.max_hp - piece.hp)
        piece.hp += repaired
        piece.repaired = True
        self._spend(REPAIR_COST)
        self._record(f"{piece.spec.name}: восстановлено {repaired} ОЗ.", (piece.owner,), target=pos, effect="build")
        return ""

    def dismantle(self, pos: Position) -> str:
        if error := self.can_act():
            return error
        piece = self.pieces.get(pos)
        if piece is None or piece.owner != self.active or piece.kind == "capital":
            return "Можно разобрать свой объект, кроме столицы."
        for key, value in piece.spec.cost:
            self.stock[piece.owner][key] += value // 3
        del self.pieces[pos]
        self._spend()
        self._update_map()
        self._record(f"{piece.spec.name}: разобран.", (piece.owner,), target=pos)
        return ""

    def piece_income(self, piece: Piece):
        for key, value in piece.spec.income:
            if piece.kind == "farm" and self.terrain_at(piece.pos) == "b":
                value += 6
            production = value + (piece.level - 1) * max(1, value // 4)
            if WORKSHOP_RESOURCES.get(piece.kind) == key and self.has_tech(piece.owner, "workshops"):
                production += 4
            if piece.kind == "city" and self.has_tech(piece.owner, "free_ports"):
                production += 6
            yield key, production

    def revenue(self, owner: int) -> dict[str, int]:
        income = dict.fromkeys(RESOURCES, 0)
        for piece in self.pieces.values():
            if piece.owner != owner:
                continue
            for key, value in self.piece_income(piece):
                income[key] += value
            if piece.spec.speed:
                income["food"] -= 2
        return income

    def end_turn(self):
        if self.winner is not None:
            return
        towers = [p for p in self.pieces.values() if p.owner == self.active and p.kind == "tower"]
        for tower in towers:
            targets = self.targets(tower)
            if targets:
                target = min(targets, key=lambda p: (distance(tower.pos, p.pos), p.hp, p.pos))
                self._strike(tower, target)
                if self.winner is not None:
                    return
        if len(self.owned_beacons(self.active)) == len(BEACONS):
            self.control[self.active] += 1
            self._record(
                f"{FACTIONS[self.active]} · удержание маяков: {self.control[self.active]}/{CONTROL_TURNS}.", (0, 1),
            )
            if self.control[self.active] == CONTROL_TURNS:
                self.winner = self.active
                self.win_reason = "beacons"
                self._record(f"{FACTIONS[self.active]} удерживает оба маяка и побеждает.", (0, 1))
                return
        self.active = 1 - self.active
        if self.active == 0:
            self.round += 1
        cities = sum(p.kind == "city" and p.owner == self.active for p in self.pieces.values())
        self.turn_capacity = ACTIONS + int(cities >= 2 and self.has_tech(self.active, "mobilization"))
        self.actions = self.turn_capacity
        self.science[self.active] += self.science_income(self.active)
        for resource, value in self.revenue(self.active).items():
            self.stock[self.active][resource] = max(0, self.stock[self.active][resource] + value)
        for piece in self.pieces.values():
            if piece.owner == self.active:
                piece.moved = piece.fired = piece.repaired = False
            else:
                piece.intercepted = False
