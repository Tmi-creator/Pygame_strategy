"""The solo opponent plays the same action budget and visibility rules."""

from collections import deque

from .catalog import COLS, ROWS
from .game import Game, area, distance
from .research import BEACONS, CAPSTONES, CONTROL_TURNS


def position_scores(game, ship, objective, radius=None):
    """Distance through water to a position within firing range of the objective."""
    radius = game.reach(ship) if radius is None else radius
    goals = [
        pos for pos in area(objective, radius)
        if game.open_water(pos, ship.owner) and pos != ship.pos
    ]
    if distance(ship.pos, objective) <= radius:
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


def approach(game: Game, ship, objective, radius=None):
    if ship.moved:
        return False
    scores = position_scores(game, ship, objective, radius)
    options = [pos for pos in game.reachable(ship) if pos in scores]
    if not options:
        return False
    destination = min(options, key=lambda pos: (scores[pos], distance(pos, objective), pos))
    return scores[destination] < scores.get(ship.pos, float("inf")) and not game.move(ship.pos, destination)


def secure_beacons(game: Game, own, sites):
    side = game.active
    owned = game.owned_beacons(side)
    cities = [piece for piece in own if piece.kind == "city"]
    scouts = [piece for piece in own if piece.kind == "explorer"]
    desired = sorted(BEACONS, key=lambda pos: (pos in owned, min(
        distance(p.pos, pos) for p in own if p.kind == "capital" or p.kind == "explorer"
    )))
    for beacon in desired:
        if not any(distance(city.pos, beacon) <= 2 for city in cities):
            candidates = sorted((pos for pos in sites if distance(pos, beacon) <= 2),
                                key=lambda pos: (distance(pos, beacon), pos))
            for pos in candidates:
                if not game.build_error("city", pos):
                    return not game.build("city", pos)
    if len(owned) == len(BEACONS):
        return False
    if not scouts:
        for pos in sites:
            if not game.build_error("explorer", pos):
                return not game.build("explorer", pos)
    for beacon in desired:
        if beacon in owned:
            continue
        landings = [pos for pos in area(beacon, 2) if pos != beacon and game.terrain_at(pos) != "~"]
        for scout in scouts:
            landings.sort(key=lambda pos: (distance(pos, beacon), distance(pos, scout.pos), pos))
            for landing in landings:
                if approach(game, scout, landing, radius=1):
                    return True
    return False


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
                p.kind != "capital", p.hp > game.firepower(ship), not p.spec.speed, p.hp,
            ))
            return game.attack(ship.pos, target.pos) == ""

    if capital.hp <= 115 and not game.repair(capital.pos):
        return True

    sites = sorted(game.visible[side], key=lambda pos: (distance(pos, capital.pos), pos))
    types = {p.kind for p in own}
    if game.control[1 - side] >= CONTROL_TURNS - 1 and secure_beacons(game, own, sites):
        return True

    if game.round <= 4 and "sawmill" in types and not game.has_tech(side, "charts"):
        if not game.research("charts"):
            return True

    if game.round <= 4:
        for kind in ("sawmill", "mine", "quarry"):
            if kind not in types:
                for pos in sites:
                    if not game.build_error(kind, pos):
                        return game.build(kind, pos) == ""

    if game.stock[side]["food"] < 18 and game.revenue(side)["food"] < 10:
        for pos in sites:
            if not game.build_error("farm", pos):
                return not game.build("farm", pos)

    if game.round <= 6 and secure_beacons(game, own, sites):
        return True

    if not game.research("long_guns"):
        return True
    if game.round >= 5 and "lab" not in types and "long_guns" in game.researched[side]:
        for pos in sites:
            if not game.build_error("lab", pos):
                return not game.build("lab", pos)
    if not game.research("formation"):
        return True

    if game.round >= 6 and game.stock[side]["gold"] >= 55:
        for ship in ships:
            if ship.kind in ("cruiser", "artillery") and ship.level == 1 and not game.upgrade(ship.pos):
                return True

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
        for objective in objectives:
            if approach(game, ship, objective, radius=None if priority else 2):
                return True

    if game.round > 6 and secure_beacons(game, own, sites):
        return True
    if game.researched[side] & CAPSTONES:
        for key in ("workshops", "free_ports", "masonry", "field_service"):
            if not game.research(key):
                return True

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
