"""Board artwork and the small symbols reused throughout the interface."""

from random import Random

import pygame as pg

from .catalog import COLS, ROWS

FACTION_COLOURS = ((97, 201, 210), (231, 139, 105))
RESOURCE_COLOURS = {
    "wood": (203, 155, 103), "stone": (162, 179, 189), "gold": (244, 201, 111),
    "metal": (147, 193, 224), "food": (161, 204, 128), "platinum": (209, 167, 236),
}
TILE = 38
MAP_X, MAP_Y = 40, 126
MAP_SIZE = COLS * TILE, ROWS * TILE
LAND_COLOURS = {
    ".": (99, 131, 96), "f": (68, 111, 88), "h": (117, 130, 89),
    "b": (145, 134, 90), "m": (100, 115, 114), "c": (88, 108, 107),
    "r": (114, 133, 104), "p": (106, 112, 128), "v": (117, 113, 94),
}


def tint(colour, amount):
    return tuple(min(255, max(0, value + amount)) for value in colour)


def tile_at(pos):
    x, y = pos
    return pg.Rect(MAP_X + x * TILE, MAP_Y + y * TILE, TILE, TILE)


def resource_icon(surface, kind, x, y, size=16):
    colour = RESOURCE_COLOURS[kind]
    dark = tint(colour, -67)
    def point(dx, dy):
        return int(x + dx * size / 16), int(y + dy * size / 16)

    if kind == "wood":
        for offset in (0, 5):
            pg.draw.line(surface, dark, point(-5, 4 - offset), point(4, -2 - offset), 5)
            pg.draw.line(surface, colour, point(-4, 3 - offset), point(5, -3 - offset), 3)
            pg.draw.circle(surface, tint(colour, 28), point(-4, 3 - offset), max(1, size // 8))
    elif kind == "gold":
        pg.draw.circle(surface, dark, point(0, 1), size // 2)
        pg.draw.circle(surface, colour, point(0, -1), size // 2 - 1)
        pg.draw.circle(surface, tint(colour, 40), point(0, -1), max(2, size // 4), 1)
    elif kind == "food":
        pg.draw.line(surface, colour, point(-5, 6), point(5, -6), 2)
        for dx, dy in ((-2, 2), (1, -1), (4, -4)):
            pg.draw.ellipse(surface, colour, pg.Rect(point(dx - 3, dy - 5), (max(2, size // 4), max(3, size // 3))))
            pg.draw.ellipse(surface, tint(colour, 20), pg.Rect(point(dx, dy), (max(3, size // 3), max(2, size // 4))))
    else:
        pg.draw.polygon(surface, dark, [point(-7, 1), point(-3, -5), point(4, -6), point(7, 0), point(1, 7)])
        pg.draw.polygon(surface, colour, [point(-6, 0), point(-2, -5), point(4, -6), point(6, -1), point(0, 4)])
        pg.draw.line(surface, tint(colour, 35), point(-2, -4), point(4, -5), 1)


def piece_icon(kind, owner, size=32):
    """Original silhouettes, with faction pennants and a dark outline at board scale."""
    sprite = pg.Surface((36, 36), pg.SRCALPHA)
    side = FACTION_COLOURS[owner]
    ink, cream, shade = (18, 34, 41), (236, 219, 179), (158, 143, 113)
    pg.draw.ellipse(sprite, (10, 26, 35, 150), (4, 26, 28, 8))

    def poly(points, colour):
        pg.draw.polygon(sprite, colour, points)
        pg.draw.polygon(sprite, ink, points, 1)

    def block(x, y, width, height, colour):
        pg.draw.rect(sprite, ink, (x - 1, y - 1, width + 2, height + 2))
        pg.draw.rect(sprite, colour, (x, y, width, height))

    def flag(x, y):
        pg.draw.line(sprite, ink, (x, y), (x, y + 12), 2)
        poly(((x, y), (x + 9, y + 2), (x, y + 5)), side)

    if kind in ("cruiser", "explorer", "artillery"):
        poly(((4, 24), (32, 24), (27, 30), (10, 30)), (138, 88, 53))
        pg.draw.line(sprite, side, (9, 27), (27, 27), 2)
        pg.draw.line(sprite, cream, (5, 32), (26, 32), 1)
        if kind == "artillery":
            block(11, 18, 11, 6, (133, 153, 151))
            block(18, 18, 11, 3, (133, 153, 151))
            flag(11, 10)
        else:
            poly(((17, 6), (17, 22), (7, 22)), cream)
            poly(((19, 6), (28, 20), (19, 20)), side)
            if kind == "cruiser":
                poly(((25, 12), (32, 21), (25, 21)), cream)
            flag(17, 4)
    elif kind in ("capital", "tower", "wall"):
        if kind == "wall":
            block(5, 19, 26, 10, shade)
            for x in (5, 14, 24):
                block(x, 15, 7, 6, cream)
            flag(13, 8)
        else:
            if kind == "capital":
                block(4, 17, 28, 13, shade)
                for x in (5, 25):
                    block(x, 14, 6, 12, cream)
                flag(23, 8)
            block(12, 12, 12, 18, cream)
            poly(((9, 13), (18, 4), (27, 13)), side)
            block(16, 22, 4, 8, ink)
            pg.draw.line(sprite, shade, (13, 17), (22, 17), 1)
    elif kind in ("quarry", "mine", "platinum", "deep_mine"):
        gem = {"quarry": (190, 195, 185), "mine": (142, 184, 213),
               "platinum": (211, 172, 226), "deep_mine": (227, 185, 120)}[kind]
        poly(((5, 28), (11, 19), (16, 13), (24, 15), (31, 28)), shade)
        poly(((11, 27), (15, 18), (23, 18), (27, 27)), ink)
        poly(((21, 28), (25, 22), (29, 23), (32, 28)), gem)
        flag(10, 9)
    elif kind == "shipyard":
        block(4, 22, 28, 4, shade)
        block(8, 25, 3, 6, shade)
        block(26, 25, 3, 6, shade)
        block(11, 14, 14, 9, cream)
        poly(((8, 15), (17, 8), (28, 15)), side)
        pg.draw.line(sprite, (112, 174, 183), (5, 32), (31, 32), 1)
    elif kind == "fishery":
        poly(((5, 24), (29, 24), (25, 29), (9, 29)), shade)
        flag(9, 14)
        poly(((12, 20), (20, 16), (24, 19), (28, 16), (28, 23), (23, 21), (17, 23)), side)
    else:
        if kind == "farm":
            for x in (6, 11, 16, 21, 26):
                pg.draw.line(sprite, (221, 184, 105), (x, 30), (x + 3, 23), 2)
        if kind == "sawmill":
            for y in (23, 27, 30):
                pg.draw.line(sprite, (193, 135, 87), (3, y), (14, y), 3)
        if kind == "city":
            block(5, 19, 8, 11, shade)
            poly(((4, 19), (8, 13), (14, 19)), side)
        block(13, 16, 15, 13, cream)
        poly(((10, 17), (20, 8), (31, 17)), side)
        block(19, 22, 4, 7, ink)
        if kind == "lab":
            pg.draw.circle(sprite, (212, 169, 236), (20, 14), 4)
    if size == 36:
        return sprite
    return pg.transform.smoothscale(sprite, (size, size))


def make_board(terrain):
    board = pg.Surface(MAP_SIZE).convert()
    for y, row in enumerate(terrain):
        for x, kind in enumerate(row):
            render_tile(board, terrain, x, y, kind)
    return board


def render_tile(surface, terrain, x, y, kind):
    rng = Random(181 * x + 701 * y)
    xx, yy = x * TILE, y * TILE
    land = kind != "~"
    colour = tint(LAND_COLOURS[kind], rng.randrange(-7, 8)) if land else tint((40, 84, 95), rng.randrange(-5, 6))
    cell = pg.Rect(xx, yy, TILE, TILE)
    pg.draw.rect(surface, colour, cell)
    for _ in range(23 if land else 15):
        px, py = xx + rng.randrange(1, TILE - 3), yy + rng.randrange(1, TILE - 2)
        pg.draw.line(surface, tint(colour, rng.choice((-14, -8, 9, 15))), (px, py),
                     (px + rng.choice((1, 2, 3)), py))
    if not land:
        for _ in range(2):
            px, py = xx + rng.randint(4, 25), yy + rng.randint(5, 31)
            pg.draw.line(surface, tint(colour, 18), (px, py), (px + 6, py))
    if kind == "f":
        for px, py, height in ((8, 11, 10), (19, 9, 12), (28, 17, 10), (15, 23, 10)):
            px, py = xx + px, yy + py
            pg.draw.line(surface, (75, 72, 51), (px, py + 3), (px, py + height + 3), 2)
            pg.draw.polygon(surface, tint(colour, -27), ((px, py - 4), (px - 5, py + height), (px + 5, py + height)))
            pg.draw.polygon(surface, tint(colour, 12), ((px, py - 4), (px - 5, py + height), (px, py + height)))
    if kind in "hmcpv":
        dark, sun = tint(colour, -33), tint(colour, 33)
        for px, py, width, height in ((9, 27, 8, 12), (23, 25, 10, 20 if kind == "m" else 13)):
            px, py = xx + px, yy + py
            pg.draw.polygon(surface, dark, ((px - width, py), (px, py - height), (px + width, py)))
            pg.draw.polygon(surface, sun, ((px - width, py), (px, py - height), (px + 2, py)))
        if kind in "cpv":
            resource_icon(surface, {"c": "metal", "p": "platinum", "v": "gold"}[kind], xx + 26, yy + 26, 12)
    if kind == "b":
        for py in (9, 15, 21, 27):
            pg.draw.line(surface, tint(colour, -24), (xx + 9, yy + py), (xx + 27, yy + py + 2), 2)
    if kind == "r":
        for px in (9, 16, 25):
            pg.draw.rect(surface, tint(colour, 25), (xx + px, yy + 13, 4, 14 - px // 4))
        pg.draw.line(surface, tint(colour, -25), (xx + 7, yy + 27), (xx + 31, yy + 27))
    if land:
        for dx, dy, shore in (
            (-1, 0, (xx, yy, 3, TILE)), (1, 0, (xx + TILE - 3, yy, 3, TILE)),
            (0, -1, (xx, yy, TILE, 3)), (0, 1, (xx, yy + TILE - 3, TILE, 3)),
        ):
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and terrain[ny][nx] == "~":
                pg.draw.rect(surface, (168, 160, 111), shore)
    pg.draw.rect(surface, tint(colour, -11), cell, 1)
