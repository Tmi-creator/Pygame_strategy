"""Authoritative match state. The AI and UI use exactly the same commands."""

from collections import deque
from dataclasses import dataclass
from typing import Literal

from .catalog import (
    ACTIONS, COLS, FACTIONS, INITIAL_STOCK, PIECES, RESOURCES, ROWS, START_CAPITALS,
    START_SHIPS, START_YARDS, TERRAIN, make_map,
)

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

    def _update_map(self):
        claims: list[dict[Position, int]] = [{}, {}]
        self.visible = [set(), set()]
        for piece in self.pieces.values():
            self.visible[piece.owner].update(area(piece.pos, piece.spec.sight))
            if piece.spec.claims:
                for pos in area(piece.pos, piece.spec.claims):
                    strength = piece.spec.claims + 1 - distance(piece.pos, pos)
                    own = claims[piece.owner]
                    own[pos] = max(own.get(pos, 0), strength)
        self.territory = {}
        for pos in claims[0].keys() | claims[1].keys():
            left, right = (side.get(pos, 0) for side in claims)
            if left != right:
                self.territory[pos] = int(right > left)
        for owner in range(2):
            self.seen[owner].update(self.visible[owner])

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
        depth = {piece.pos: 0}
        queue = deque([piece.pos])
        while queue:
            here = queue.popleft()
            steps = depth[here] + 1
            if steps > piece.spec.speed:
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
        return ""

    def targets(self, attacker: Piece) -> list[Piece]:
        return [
            piece for piece in self.pieces.values()
            if piece.owner != attacker.owner and piece.pos in self.visible[attacker.owner]
            and distance(attacker.pos, piece.pos) <= attacker.spec.reach
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
        damage = max(1, attacker.damage - (12 if fortified else 0))
        target.hp -= damage
        self._record(f"{attacker.spec.name} → {target.spec.name} · −{damage} ОЗ",
                     (0, 1), attacker.pos, target.pos, "hit")
        if target.hp <= 0:
            del self.pieces[target.pos]
            if target.kind == "capital":
                self.winner = attacker.owner
                self._record(f"{FACTIONS[attacker.owner]} одерживает победу.", (0, 1), target=target.pos)
            self._update_map()

    def upgrade_cost(self, piece: Piece):
        has_lab = any(other.kind == "lab" and other.owner == piece.owner for other in self.pieces.values())
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
        if piece.spec.speed and not any(
            p.kind == "shipyard" and p.owner == piece.owner and distance(p.pos, pos) <= 2
            for p in self.pieces.values()
        ):
            return "Корабль ремонтируется в радиусе двух клеток от своей верфи."
        if not self.afford(REPAIR_COST):
            return "Для ремонта нужны 10 дерева и 12 золота."
        repaired = min(46, piece.max_hp - piece.hp)
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
            yield key, value + (piece.level - 1) * max(1, value // 4)

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
        self.active = 1 - self.active
        if self.active == 0:
            self.round += 1
        self.actions = ACTIONS
        for resource, value in self.revenue(self.active).items():
            self.stock[self.active][resource] = max(0, self.stock[self.active][resource] + value)
        for piece in self.pieces.values():
            if piece.owner == self.active:
                piece.moved = piece.fired = piece.repaired = False
