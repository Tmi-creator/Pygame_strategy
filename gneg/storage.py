"""Versioned, atomic autosaves. A malformed file can be ignored at startup."""

import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path

from .catalog import ACTIONS, PIECES, RESOURCES
from .game import Event, Game, Piece, inside

SAVE_PATH = Path(os.environ.get("LOCALAPPDATA", Path.home() / ".local" / "share")) / "Gneg" / "match.json"


def save(game: Game, path: Path = SAVE_PATH):
    data = {
        "version": 1,
        "mode": game.mode,
        "active": game.active,
        "round": game.round,
        "actions": game.actions,
        "winner": game.winner,
        "pieces": [asdict(p) for p in game.pieces.values()],
        "stock": game.stock,
        "seen": [sorted(tiles) for tiles in game.seen],
        "events": [asdict(event) for event in game.events],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    handle = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent, delete=False)
    temp = Path(handle.name)
    try:
        with handle:
            json.dump(data, handle, ensure_ascii=False)
        temp.replace(path)
    finally:
        temp.unlink(missing_ok=True)


def _position(values):
    pos = tuple(values)
    if len(pos) != 2 or any(type(n) is not int for n in pos) or not inside(pos):
        raise ValueError("Invalid position")
    return pos


def load(path: Path = SAVE_PATH) -> Game | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        if data["version"] != 1 or data["mode"] not in ("solo", "hotseat"):
            return None
        game = Game(data["mode"])
        game.active, game.round, game.actions, game.winner = (
            data[key] for key in ("active", "round", "actions", "winner")
        )
        if (
            game.active not in (0, 1) or game.winner not in (None, 0, 1) or
            type(game.round) is not int or game.round < 1 or
            type(game.actions) is not int or not 0 <= game.actions <= ACTIONS
        ):
            return None
        game.stock = data["stock"]
        if len(game.stock) != 2 or any(
            set(stock) != set(RESOURCES) or any(type(n) is not int or n < 0 for n in stock.values())
            for stock in game.stock
        ):
            return None
        game.pieces.clear()
        for record in data["pieces"]:
            record["pos"] = _position(record["pos"])
            piece = Piece(**record)
            if (
                piece.kind not in PIECES or piece.owner not in (0, 1) or piece.pos in game.pieces or
                piece.level not in (1, 2, 3) or not 0 < piece.hp <= piece.max_hp or
                game.terrain_at(piece.pos) not in piece.spec.terrain
            ):
                return None
            game.pieces[piece.pos] = piece
        capitals = sorted(p.owner for p in game.pieces.values() if p.kind == "capital")
        if capitals != ([0, 1] if game.winner is None else [game.winner]):
            return None
        game.seen = [set(map(_position, cells)) for cells in data["seen"]]
        if len(game.seen) != 2:
            return None
        game.events = [
            Event(e["text"], tuple(e["audience"]), _position(e["origin"]) if e["origin"] else None,
                  _position(e["target"]) if e["target"] else None, e["effect"])
            for e in data["events"][-80:]
            if isinstance(e["text"], str) and isinstance(e["audience"], list)
        ]
        game._update_map()
        return game
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return None
