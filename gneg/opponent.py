"""The solo opponent plays the same action budget and visibility rules."""

from collections import deque

from .catalog import COLS, ROWS
from .game import Game, area, distance


def position_scores(game, ship, objective):
    """Distance through water to a position within firing range of the objective."""
    goals = [
        pos for pos in area(objective, ship.spec.reach)
        if game.open_water(pos, ship.owner) and pos != ship.pos
    ]
    if distance(ship.pos, objective) <= ship.spec.reach:
        goals.append(ship.pos)
    scores = dict.fromkeys(goals, 0)
    queue = deque(goals)
    while queue:
        here = queue.popleft()
        for pos in game.water_neighbors(here, ship):
            if pos in scores:
                continue
            scores[pos] = scores[here] + 1
            queue.append(pos)
    return scores


def take_action(game: Game) -> bool:
    if game.can_act():
        return False
    side = game.active
    own = [piece for piece in game.pieces.values() if piece.owner == side]
    enemies = [
        p for p in game.pieces.values() if p.owner != side and p.pos in game.visible[side]
    ]
    ships = [piece for piece in own if piece.spec.speed]
    capital = next(p for p in own if p.kind == "capital")

    for ship in ships:
        targets = game.targets(ship)
        if not ship.fired and targets:
            target = min(targets, key=lambda p: (
                p.kind != "capital", p.hp > ship.damage, not p.spec.speed, p.hp,
            ))
            return game.attack(ship.pos, target.pos) == ""

    if capital.hp <= 115 and not game.repair(capital.pos):
        return True

    sites = sorted(game.visible[side], key=lambda pos: (distance(pos, capital.pos), pos))
    types = {p.kind for p in own}
    if game.round <= 4:
        for kind in ("sawmill", "mine", "quarry"):
            if kind not in types:
                for pos in sites:
                    if not game.build_error(kind, pos):
                        return game.build(kind, pos) == ""

    if len(ships) < (2 if game.round <= 3 else 4):
        if game.round >= 4 and ships and "artillery" not in types:
            order = ("artillery", "cruiser", "explorer")
        else:
            order = ("cruiser", "explorer", "artillery")
        for kind in order:
            for pos in sites:
                if not game.build_error(kind, pos):
                    return game.build(kind, pos) == ""

    priority = sorted(enemies, key=lambda p: (p.kind != "capital", p.spec.speed == 0, p.hp))
    frontier = (COLS // 4, ROWS // 2) if side else (3 * COLS // 4, ROWS // 2)
    objectives = [p.pos for p in priority] or [frontier]
    for ship in ships:
        if ship.moved:
            continue
        reach = game.reachable(ship)
        for objective in objectives:
            if distance(ship.pos, objective) <= ship.spec.reach and priority:
                continue
            scores = position_scores(game, ship, objective)
            options = [pos for pos in reach if pos in scores and pos not in game.pieces]
            if not options:
                continue
            destination = min(options, key=lambda pos: (scores[pos], distance(pos, objective), pos))
            if scores[destination] < scores.get(ship.pos, float("inf")) or (
                not priority and distance(destination, objective) < distance(ship.pos, objective)
            ):
                return game.move(ship.pos, destination) == ""

    if "shipyard" not in types or (game.round > 5 and len(ships) < 2 and len(own) < 14):
        for pos in sites:
            if not game.build_error("shipyard", pos):
                return game.build("shipyard", pos) == ""
    for kind in ("farm", "city", "tower"):
        if kind not in types:
            for pos in sites:
                if not game.build_error(kind, pos):
                    return game.build(kind, pos) == ""
    return False
