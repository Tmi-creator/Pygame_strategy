"""Presentation and hit targets for the game screens."""

import math
import sys
from pathlib import Path

import pygame as pg

from .art import (
    FACTION_COLOURS, MAP_SIZE, MAP_X, MAP_Y, TILE, make_board,
    piece_icon, resource_icon, tile_at,
)
from .catalog import (
    BUILD_GROUPS, COLS, FACTIONS, PIECES, RESOURCES, RESOURCE_NAMES, ROWS, TERRAIN,
    make_map,
)
from .game import Game, REPAIR_COST
from .research import BEACONS, BRANCHES, CAPSTONES, CONTROL_TURNS

SIZE = (1328, 812)
ASSETS = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parents[1])) / "assets"
BACKGROUND = (15, 28, 36)
PANEL = (23, 39, 48)
INSET = (29, 48, 58)
LINE = (57, 79, 85)
TEXT = (239, 233, 214)
MUTED = (174, 192, 190)
GOLD = (235, 188, 111)
GOLD_DARK = (87, 63, 38)
GREEN = (166, 207, 155)
RED = (239, 143, 117)

SHORT_RESOURCES = dict(zip(RESOURCES, ("Дер.", "Кам.", "Зол.", "Мет.", "Пров.", "Плат.")))
BOARD = pg.Rect((MAP_X, MAP_Y), MAP_SIZE)
SIDE_X, SIDE_W = 978, 324


class Interface:
    def __init__(self, app):
        self.app = app
        self.canvas = pg.Surface(SIZE).convert()
        self.fonts = {}
        self.text_cache = {}
        self.title_font = pg.font.match_font("georgia,cambria,dejavuserif")
        cover = pg.image.load(ASSETS / "archipelago.jpg").convert()
        scale = max(SIZE[0] / cover.get_width(), SIZE[1] / cover.get_height())
        cover = pg.transform.smoothscale_by(cover, scale)
        self.cover = pg.Surface(SIZE).convert()
        self.cover.blit(cover, ((SIZE[0] - cover.get_width()) // 2, (SIZE[1] - cover.get_height()) // 2))
        for x in range(0, 720, 3):
            shade = pg.Surface((3, SIZE[1]), pg.SRCALPHA)
            shade.fill((7, 18, 26, max(0, int(160 * (1 - x / 720) ** 1.4))))
            self.cover.blit(shade, (x, 0))

        self.icons = {(kind, owner): piece_icon(kind, owner, 36) for kind in PIECES for owner in (0, 1)}
        self.list_icons = {key: pg.transform.smoothscale(icon, (28, 28)) for key, icon in self.icons.items()}
        self.board = make_board(make_map())
        self.fog = self.swatch((12, 28, 39, 153))
        self.unseen = {}
        for y in range(ROWS):
            for x in range(COLS):
                tone = (28 + (x * 3 + y * 7) % 6, 49 + (x + y * 3) % 5, 59 + (x * 2 + y) % 5)
                block = self.swatch((*tone, 255))
                pg.draw.line(block, (45, 66, 74, 190), (0, 0), (0, TILE))
                pg.draw.line(block, (45, 66, 74, 190), (0, 0), (TILE, 0))
                pg.draw.line(block, (48, 69, 76, 165), (7 + x % 8, 13 + y % 8), (11 + x % 8, 13 + y % 8))
                self.unseen[x, y] = block
        self.ship_tile = self.swatch((101, 210, 211, 57))
        self.build_tile = self.swatch((248, 206, 125, 76))
        self.claim_tile = [self.swatch((*FACTION_COLOURS[who], 22)) for who in (0, 1)]

    @staticmethod
    def swatch(rgba):
        layer = pg.Surface((TILE, TILE), pg.SRCALPHA)
        layer.fill(rgba)
        return layer

    def font(self, size, bold=False, serif=False):
        key = size, bold, serif
        if key not in self.fonts:
            path = self.title_font if serif and self.title_font else ASSETS / "Lato-Regular.ttf"
            font = pg.font.Font(str(path), size)
            font.set_bold(bold)
            self.fonts[key] = font
        return self.fonts[key]

    def text(self, line, x, y, size=18, colour=TEXT, *, bold=False, serif=False, align="left"):
        key = line, size, colour, bold, serif
        if key not in self.text_cache:
            if len(self.text_cache) > 800:
                self.text_cache.clear()
            self.text_cache[key] = self.font(size, bold, serif).render(line, True, colour)
        image = self.text_cache[key]
        rect = image.get_rect(topleft=(x, y))
        if align == "center":
            rect.centerx = x
        elif align == "right":
            rect.right = x
        self.canvas.blit(image, rect)
        return rect

    def paragraph(self, line, x, y, width, size=17, colour=MUTED, line_height=None):
        current = ""
        font = self.font(size)
        step = line_height or size + 5
        for word in line.split():
            joined = f"{current} {word}" if current else word
            if current and font.size(joined)[0] > width:
                self.text(current, x, y, size, colour)
                y += step
                current = word
            else:
                current = joined
        if current:
            self.text(current, x, y, size, colour)
        return y + step

    def panel(self, box, fill=PANEL, border=LINE, radius=9):
        pg.draw.rect(self.canvas, fill, box, border_radius=radius)
        if border:
            pg.draw.rect(self.canvas, border, box, 1, border_radius=radius)

    def button(self, label, box, action, *, primary=False, enabled=True, active=False, size=17, left=False):
        rect = pg.Rect(box)
        hover = enabled and rect.collidepoint(self.app.mouse)
        if primary and enabled:
            fill = (250, 209, 144) if hover else GOLD
            edge, ink = GOLD, (29, 33, 34)
        elif enabled:
            fill = (51, 74, 80) if hover else INSET
            edge, ink = (178, 145, 91) if active else LINE, GOLD if active else TEXT
        else:
            fill, edge, ink = (28, 42, 49), (48, 66, 72), (125, 147, 147)
        self.panel(rect, fill, edge, 6)
        font_h = self.font(size, primary).get_height()
        self.text(label, rect.x + 16 if left else rect.centerx, rect.centery - font_h // 2,
                  size, ink, bold=primary, align="left" if left else "center")
        self.hit(rect, action, enabled)

    def hit(self, rect, action, enabled=True):
        self.app.hit(rect, action, enabled)

    def draw(self):
        self.app.hits.clear()
        page, overlay = self.app.page, self.app.overlay
        if overlay == "handoff":
            self.canvas.blit(self.cover, (0, 0))
        elif page == "menu":
            self.draw_menu()
        else:
            self.draw_match()
        if overlay:
            self.app.hits.clear()
            self.draw_overlay(overlay)

    def draw_menu(self):
        app = self.app
        self.canvas.blit(self.cover, (0, 0))
        x = 86
        self.text("ПОШАГОВАЯ МОРСКАЯ СТРАТЕГИЯ", x + 4, 107, 16, GOLD, bold=True)
        self.text("Гнег", x, 129, 102, TEXT, serif=True, bold=True)
        self.text("Война за архипелаг", x + 4, 257, 32, TEXT, serif=True)
        pg.draw.line(self.canvas, GOLD, (x + 4, 312), (x + 100, 312), 2)
        self.paragraph("Развивайте острова, собирайте флот и прорвитесь к столице соперника.",
                       x + 4, 333, 380, 19, TEXT, 26)

        saved = app.saved and app.saved.winner is None
        y = 420
        if saved:
            self.button(f"Продолжить · раунд {app.saved.round}", (x + 4, y, 316, 48),
                        lambda: app.enter_game(app.saved, resume=True), primary=True, left=True)
            y += 59
        self.button("Играть против компьютера", (x + 4, y, 316, 48),
                    lambda: app.new_game("solo"), primary=not saved, left=True)
        self.button("Двое за одним ПК", (x + 4, y + 59, 316, 48),
                    lambda: app.new_game("hotseat"), left=True)
        self.button("Как играть", (x + 4, y + 118, 150, 44), lambda: setattr(app, "overlay", "help"))
        self.button("Выйти", (x + 166, y + 118, 154, 44), lambda: setattr(app, "running", False))
        self.text("М  ·  Звук", x + 4, 750, 15, MUTED)
        self.text("F11  ·  Полный экран", x + 112, 750, 15, MUTED)
        if app.save_error:
            self.text(app.save_error, x + 4, 720, 15, RED)

    def draw_match(self):
        app, game = self.app, self.app.game
        who = app.viewer
        side = FACTION_COLOURS[who]
        self.canvas.fill(BACKGROUND)
        self.panel((20, 17, 1288, 57), PANEL, LINE, 8)
        self.text("ГНЕГ", 41, 27, 27, TEXT, bold=True, serif=True)
        income = game.revenue(who)
        for index, kind in enumerate(RESOURCES):
            x = 170 + index * 138
            pg.draw.line(self.canvas, LINE, (x - 12, 27), (x - 12, 64))
            resource_icon(self.canvas, kind, x + 8, 48, 19)
            self.text(RESOURCE_NAMES[kind], x + 26, 24, 13, MUTED)
            self.text(str(game.stock[who][kind]), x + 26, 41, 19, TEXT, bold=True)
            delta = income[kind]
            if delta:
                self.text(f"{delta:+}", x + 83, 44, 15, GREEN if delta > 0 else RED)
        self.button(f"Наука  {game.science[who]}  ·  R", (1002, 27, 155, 37), app.toggle_research, size=16)
        self.button("Меню  ≡", (1169, 27, 117, 37), lambda: setattr(app, "overlay", "pause"), size=16)
        pg.draw.circle(self.canvas, side, (45, 101), 5)
        self.text(FACTIONS[who], 58, 88, 21, side, bold=True)
        self.text(f"Раунд {game.round}", 271, 92, 17, MUTED)
        self.draw_beacon_status(who)
        status = "Партия завершена" if game.winner is not None else "Ваш ход" if app.can_control else "Ход Южной лиги…"
        self.text(status, 952, 91, 18, GOLD if app.can_control else MUTED, bold=True, align="right")

        hovered = app.mouse
        hovered_cell = (hovered[0] - MAP_X) // TILE, (hovered[1] - MAP_Y) // TILE
        self.draw_board(hovered_cell if BOARD.collidepoint(hovered) else None)
        self.draw_sidebar()
        for index in range(COLS):
            self.text(chr(65 + index), MAP_X + index * TILE + TILE // 2, 110, 10, MUTED, align="center")
        for index in range(ROWS):
            self.text(str(index + 1), 31, MAP_Y + index * TILE + TILE // 2 - 8, 12, MUTED, align="right")

        self.text("ЖУРНАЛ", 41, 752, 12, GOLD, bold=True)
        events = [event.text for event in game.events if who in event.audience]
        self.text(events[-1] if events else "", 119, 748, 16, TEXT)
        if len(events) > 1:
            self.text(events[-2], 119, 773, 14, MUTED)
        self.text("Tab · флот     F1 · справка", 952, 774, 14, MUTED, align="right")

    def draw_beacon_status(self, who):
        game = self.app.game
        for index, pos in enumerate(BEACONS):
            colour = FACTION_COLOURS[owner] if (owner := game.territory.get(pos)) is not None else MUTED
            x = 379 + index * 19
            pg.draw.polygon(self.canvas, colour, ((x, 94), (x + 6, 100), (x, 106), (x - 6, 100)), 2)
        status = f"Маяки  {len(game.owned_beacons(who))}/{len(BEACONS)}"
        if any(game.control):
            leader = 0 if game.control[0] else 1
            status += f"    ·    Удержание  {game.control[leader]}/{CONTROL_TURNS}"
            colour = FACTION_COLOURS[leader]
        else:
            colour = MUTED
        self.text(status, 412, 91, 16, colour)

    def draw_beacon(self, rect, owner, occupied=False):
        colour = GOLD if owner is None else FACTION_COLOURS[owner]
        x, y = rect.center
        pg.draw.circle(self.canvas, colour, (x, y), 16, 2)
        if occupied:
            return
        pg.draw.circle(self.canvas, (25, 43, 50), (x, y), 13)
        pg.draw.polygon(self.canvas, (222, 214, 182), ((x - 6, y + 9), (x - 3, y - 4), (x + 3, y - 4), (x + 6, y + 9)))
        pg.draw.rect(self.canvas, colour, (x - 4, y - 8, 8, 5))
        pg.draw.polygon(self.canvas, colour, ((x - 6, y - 8), (x, y - 12), (x + 6, y - 8)))
        pg.draw.line(self.canvas, colour, (x - 10, y - 6), (x - 14, y - 7))
        pg.draw.line(self.canvas, colour, (x + 10, y - 6), (x + 14, y - 7))

    def draw_board(self, hover):
        app, game = self.app, self.app.game
        who = app.viewer
        visible = game.visible[who] if game.winner is None else self.unseen.keys()
        self.canvas.blit(self.board, BOARD)
        selected = game.pieces.get(app.selected)
        moves, targets, builds = set(), set(), set()
        if app.can_control and game.actions:
            if app.build_kind:
                builds = {pos for pos in visible if not game.build_error(app.build_kind, pos)}
            elif selected and selected.owner == who and selected.spec.speed:
                if not selected.moved:
                    moves = set(game.reachable(selected))
                if not selected.fired:
                    targets = {piece.pos for piece in game.targets(selected)}

        for pos, unknown in self.unseen.items():
            rect = tile_at(pos)
            if pos not in visible:
                self.canvas.blit(self.fog if pos in game.seen[who] else unknown, rect)
                if pos in BEACONS:
                    self.draw_beacon(rect, game.territory.get(pos))
                continue
            owner = game.territory.get(pos)
            if owner is not None:
                self.canvas.blit(self.claim_tile[owner], rect)
                self.draw_border(pos, rect, owner)
            if pos in moves:
                self.canvas.blit(self.ship_tile, rect)
                pg.draw.circle(self.canvas, (132, 215, 215), rect.center, 3)
            if pos in builds:
                self.canvas.blit(self.build_tile, rect)
                pg.draw.rect(self.canvas, GOLD, rect.inflate(-5, -5), 1)
            piece = game.pieces.get(pos)
            if pos in BEACONS:
                self.draw_beacon(rect, owner, occupied=piece is not None)
            if piece:
                colour = FACTION_COLOURS[piece.owner]
                pg.draw.circle(self.canvas, (22, 42, 48), rect.center, 15)
                pg.draw.circle(self.canvas, colour, rect.center, 15, 1)
                self.canvas.blit(self.icons[piece.kind, piece.owner], (rect.x + 1, rect.y))
                if piece.hp < piece.max_hp or piece.kind == "capital":
                    bar = pg.Rect(rect.x + 5, rect.bottom - 5, 28, 3)
                    pg.draw.rect(self.canvas, (29, 35, 39), bar, border_radius=1)
                    pg.draw.rect(self.canvas, colour, (bar.x, bar.y, round(bar.w * piece.hp / piece.max_hp), bar.h), border_radius=1)
            if pos in targets:
                self.corners(rect.inflate(-2, -2), RED, 8)

        pg.draw.rect(self.canvas, LINE, BOARD.inflate(2, 2), 1)
        if app.selected is not None:
            self.corners(tile_at(app.selected), GOLD, 10)
        if hover is not None and hover != app.selected:
            pg.draw.rect(self.canvas, GOLD if hover in builds else (185, 203, 199), tile_at(hover).inflate(-3, -3), 1)
        self.draw_effect(visible)

    def draw_border(self, pos, rect, owner):
        territory = self.app.game.territory
        colour = tuple((value + 70) // 2 for value in FACTION_COLOURS[owner])
        x, y = pos
        for cell, start, end in (
            ((x - 1, y), rect.topleft, rect.bottomleft),
            ((x + 1, y), (rect.right - 1, rect.top), (rect.right - 1, rect.bottom)),
            ((x, y - 1), rect.topleft, rect.topright),
            ((x, y + 1), (rect.left, rect.bottom - 1), (rect.right, rect.bottom - 1)),
        ):
            if territory.get(cell) != owner:
                pg.draw.line(self.canvas, colour, start, end, 2)

    def corners(self, rect, colour, length):
        for x, y, dx, dy in (
            (rect.left, rect.top, 1, 1), (rect.right - 1, rect.top, -1, 1),
            (rect.left, rect.bottom - 1, 1, -1), (rect.right - 1, rect.bottom - 1, -1, -1),
        ):
            pg.draw.line(self.canvas, colour, (x, y), (x + dx * length, y), 2)
            pg.draw.line(self.canvas, colour, (x, y), (x, y + dy * length), 2)

    def draw_effect(self, visible):
        if not self.app.effect:
            return
        event, start = self.app.effect
        progress = (pg.time.get_ticks() - start) / 680
        if progress > 1 or event.target is None or event.target not in visible:
            return
        centre = tile_at(event.target).center
        colour = (249, 167, 105) if event.effect == "hit" else (249, 219, 149)
        self.canvas.set_clip(BOARD)
        pg.draw.circle(self.canvas, colour, centre, round(7 + 30 * progress), 2)
        if event.effect == "hit":
            for index in range(8):
                angle = index * math.tau / 8
                p = (round(centre[0] + math.cos(angle) * (8 + 26 * progress)),
                     round(centre[1] + math.sin(angle) * (8 + 26 * progress)))
                pg.draw.circle(self.canvas, colour, p, max(1, round(4 * (1 - progress))))
            if progress < 0.25 and event.origin in visible:
                pg.draw.line(self.canvas, colour, tile_at(event.origin).center, centre, 2)
        self.canvas.set_clip(None)

    def draw_sidebar(self):
        app, game = self.app, self.app.game
        who, x = app.viewer, SIDE_X
        self.panel((x, 90, SIDE_W, 702), PANEL, LINE, 8)
        self.draw_inspector()
        self.text("СТРОИТЕЛЬСТВО", x + 16, 277, 13, GOLD, bold=True)
        for i, tab in enumerate(BUILD_GROUPS):
            self.button(tab, (x + 14 + i * 100, 302, 96, 33), lambda name=tab: app.select_tab(name),
                        active=tab == app.tab, size=13)
        hovered = None
        for index, kind in enumerate(BUILD_GROUPS[app.tab]):
            spec = PIECES[kind]
            rect = pg.Rect(x + 14, 343 + index * 34, SIDE_W - 28, 31)
            active = app.build_kind == kind
            affordable = all(game.stock[who][key] >= value for key, value in spec.cost)
            over = rect.collidepoint(app.mouse)
            if over:
                hovered = kind
            if over or active or index % 2 == 0:
                self.panel(rect, (55, 66, 64) if active else (38, 57, 64) if over else INSET,
                           GOLD if active else None, 4)
            self.canvas.blit(self.list_icons[kind, who], (rect.x + 5, rect.y + 1))
            self.text(spec.name, rect.x + 37, rect.y + 6, 15, TEXT if affordable else MUTED, bold=active)
            self.cost(spec.cost, rect.right - 8, rect.y + 7, who)
            self.hit(rect, lambda kind=kind: app.choose_build(kind), app.can_control and game.actions > 0)

        tooltip = app.build_kind or hovered
        if tooltip:
            line = PIECES[tooltip].description
        elif app.tab == "Флот":
            line = "Для спуска корабля выберите воду рядом со своей верфью."
        else:
            line = "Выберите проект, затем подходящую клетку."
        self.paragraph(line, x + 17, 622, SIDE_W - 34, 14, MUTED, 17)
        pg.draw.line(self.canvas, LINE, (x + 15, 661), (x + SIDE_W - 15, 661))
        remaining = game.actions if app.can_control else 0
        capacity = game.turn_capacity
        self.text(f"Действия  {remaining} / {capacity}", x + 16, 673, 16, TEXT)
        for index in range(capacity):
            cx = x + SIDE_W - 23 - (capacity - 1 - index) * 20
            diamond = ((cx, 674), (cx + 6, 680), (cx, 686), (cx - 6, 680))
            pg.draw.polygon(self.canvas, GOLD if index < remaining else LINE, diamond, 0 if index < remaining else 1)
        self.button("Завершить ход   ·   Пробел", (x + 15, 703, SIDE_W - 30, 44), app.end_turn,
                    primary=True, enabled=app.can_control)
        notice = app.notice if pg.time.get_ticks() < app.notice_until else ""
        self.paragraph(notice or app.save_error or "Прогресс сохраняется автоматически.",
                       x + 16, 754, SIDE_W - 30, 13, GOLD if notice else MUTED, 15)

    def cost(self, values, right, y, who):
        app = self.app
        for key, amount in reversed(values):
            colour = MUTED if app.game.stock[who][key] >= amount else RED
            width = self.font(13).size(str(amount))[0]
            self.text(str(amount), right, y, 13, colour, align="right")
            resource_icon(self.canvas, key, right - width - 8, y + 7, 11)
            right -= width + 19

    def draw_inspector(self):
        app, game = self.app, self.app.game
        x = SIDE_X + 15
        self.panel((x, 102, SIDE_W - 30, 160), (19, 34, 43), LINE, 7)
        self.text("ВЫБРАННАЯ КЛЕТКА", x + 12, 112, 11, MUTED, bold=True)
        pos = app.selected
        if pos is None:
            self.text("Выберите клетку", x + 12, 140, 23, TEXT, bold=True)
            self.paragraph("Кликните по полю, чтобы увидеть объект и доступные действия.",
                           x + 12, 179, 265, 15)
            return
        self.text(f"{chr(65 + pos[0])}{pos[1] + 1}", x + 281, 110, 14, GOLD, align="right")
        who = app.viewer
        visible = pos in game.visible[who] or game.winner is not None
        if pos in BEACONS and (not visible or pos not in game.pieces):
            owner = game.territory.get(pos)
            self.text("Сигнальный маяк", x + 12, 136, 22, TEXT, bold=True)
            self.text("Нейтральный" if owner is None else FACTIONS[owner],
                      x + 12, 166, 15, MUTED if owner is None else FACTION_COLOURS[owner])
            self.paragraph("Приносит 1 науку за ход. Чтобы взять маяк, включите его в свою территорию.",
                           x + 12, 194, 266, 14, MUTED, 17)
            return
        if not visible:
            self.text("Туман войны", x + 12, 140, 23, TEXT, bold=True)
            hint = "Сейчас эту клетку не видно." if pos in game.seen[who] else "Отправьте флот на разведку."
            self.text(hint, x + 12, 179, 15, MUTED)
            return
        piece = game.pieces.get(pos)
        terrain = TERRAIN[game.terrain_at(pos)]
        if not piece:
            self.text(terrain, x + 12, 136, 23, TEXT, bold=True)
            owner = game.territory.get(pos)
            self.text("Нейтральная территория" if owner is None else FACTIONS[owner],
                      x + 12, 174, 16, MUTED if owner is None else FACTION_COLOURS[owner])
            return
        own = who == piece.owner
        self.canvas.blit(self.icons[piece.kind, piece.owner], (x + 8, 129))
        self.text(piece.spec.name, x + 50, 132, 20, TEXT, bold=True)
        self.text(f"Ур. {piece.level} · {piece.hp}/{piece.max_hp} ОЗ", x + 50, 157, 14, FACTION_COLOURS[piece.owner])
        if piece.spec.speed:
            damage = game.firepower(piece) if own else piece.damage
            status = f"Ход {game.speed(piece)} · Дальн. {game.reach(piece)} · Урон {damage}"
            if own and (piece.moved or piece.fired):
                spent = "ход и залп" if piece.moved and piece.fired else "ход" if piece.moved else "залп"
                status = f"Израсходован: {spent}." if not (piece.moved and piece.fired) else "Ход и залп израсходованы."
        elif piece.spec.income:
            gains = [f"+{value} {SHORT_RESOURCES[key].lower()}" for key, value in game.piece_income(piece)]
            status = "  /  ".join(gains) + " за ход"
        elif piece.kind == "tower":
            status = f"Дальн. {game.reach(piece)} · Урон {game.firepower(piece)}"
        else:
            status = FACTIONS[piece.owner] if not own else terrain
        self.text(status, x + 12, 185, 14, MUTED)
        if own and app.can_control:
            self.button("Улучшить", (x + 10, 215, 91, 32), lambda: app.execute(game.upgrade, pos),
                        enabled=piece.level < 3 and game.actions > 0, size=13)
            self.button("Починить", (x + 104, 215, 90, 32), lambda: app.execute(game.repair, pos),
                        enabled=piece.hp < piece.max_hp and not piece.repaired and game.actions > 0, size=13)
            self.button("Разобрать", (x + 197, 215, 86, 32), lambda: setattr(app, "overlay", "dismantle"),
                        enabled=piece.kind != "capital" and game.actions > 0, size=13)
            if pg.Rect(x + 10, 215, 91, 32).collidepoint(app.mouse) and piece.level < 3:
                self.cost(game.upgrade_cost(piece), x + 247, 111, who)
            elif pg.Rect(x + 104, 215, 90, 32).collidepoint(app.mouse):
                self.cost(REPAIR_COST, x + 247, 111, who)
        elif not own:
            self.text(FACTIONS[piece.owner], x + 12, 220, 14, FACTION_COLOURS[piece.owner])

    def draw_overlay(self, mode):
        app = self.app
        veil = pg.Surface(SIZE, pg.SRCALPHA)
        veil.fill((7, 16, 22, 204 if mode == "handoff" else 170))
        self.canvas.blit(veil, (0, 0))
        center = SIZE[0] // 2
        if mode in ("help", "help_pause"):
            self.draw_help()
            return
        if mode == "research":
            self.draw_research()
            return
        if mode == "pause":
            self.panel((center - 224, 180, 448, 448), PANEL, LINE, 12)
            self.text("Пауза", center, 211, 39, TEXT, serif=True, align="center")
            controls = (
                ("Вернуться к карте", app.cancel),
                ("Как играть", lambda: setattr(app, "overlay", "help_pause")),
                (f"Звук: {'включён' if app.audio.enabled else 'выключен'}", app.toggle_audio),
                ("Главное меню", app.main_menu),
                ("Выйти из игры", lambda: setattr(app, "running", False)),
            )
            for index, (label, action) in enumerate(controls):
                self.button(label, (center - 165, 279 + index * 57, 330, 45), action, primary=index == 0)
            return
        if mode == "handoff":
            who = app.viewer
            self.modal("Передача хода", FACTIONS[who], f"Раунд {app.game.round}. Передайте управление следующему игроку.",
                       "Открыть карту", app.reveal_turn, "Главное меню", app.main_menu, FACTION_COLOURS[who])
        elif mode == "result":
            who = app.game.winner
            title = "Победа!" if app.game.mode == "solo" and who == 0 else "Поражение" if app.game.mode == "solo" else "Победа"
            reason = "Оба маяка удержаны" if app.game.win_reason == "beacons" else "Столица соперника пала"
            self.modal(title, FACTIONS[who], f"{reason}. Конец партии · раунд {app.game.round}.",
                       "Новая партия", lambda: app.enter_game(Game(app.game.mode)),
                       "Посмотреть карту", app.cancel, FACTION_COLOURS[who])
            self.button("Главное меню", (center - 100, 548, 200, 38), app.main_menu, size=15)
        elif mode == "replace":
            self.modal("Новая партия", "", "Текущая партия будет заменена новой.",
                       "Начать", lambda: app.enter_game(Game(app.pending_mode)), "Отмена", app.cancel)
        elif mode == "dismantle":
            self.modal("Разобрать объект?", "", "Вернётся треть ресурсов. Это стоит одно действие.",
                       "Разобрать", self.confirm_dismantle, "Отмена", app.cancel)

    def confirm_dismantle(self):
        self.app.overlay = ""
        self.app.execute(self.app.game.dismantle, self.app.selected)

    def modal(self, title, subtitle, body, primary, confirm, secondary, cancel, colour=GOLD):
        center = SIZE[0] // 2
        self.panel((center - 298, 232, 596, 370), PANEL, LINE, 12)
        self.text(title, center, 267, 43, TEXT, serif=True, align="center")
        if subtitle:
            self.text(subtitle, center, 336, 23, colour, bold=True, align="center")
        self.text(body, center, 394, 17, MUTED, align="center")
        self.button(primary, (center - 245, 470, 236, 54), confirm, primary=True)
        self.button(secondary, (center + 9, 470, 236, 54), cancel)

    def draw_research(self):
        app, game = self.app, self.app.game
        side = app.viewer
        self.panel((77, 53, 1174, 706), PANEL, LINE, 12)
        self.text("Исследования", 108, 75, 42, TEXT, serif=True)
        self.text(f"Наука   {game.science[side]}   +{game.science_income(side)} / ход",
                  1215, 91, 24, GOLD, align="right", bold=True)
        self.text("Столица, академия и маяки дают науку. Исследование стоит одно действие.", 110, 137, 17, MUTED)
        pg.draw.line(self.canvas, LINE, (110, 169), (1217, 169))
        for column, branch in enumerate(BRANCHES):
            x = 110 + column * 377
            colour = branch.colour
            self.text(branch.name, x, 182, 25, colour, bold=True)
            for row, tech in enumerate(branch.technologies):
                y = 219 + row * 154
                known = game.has_tech(side, tech.key)
                error = game.research_error(tech.key, side)
                edge = colour if known or not error else LINE
                if row:
                    pg.draw.line(self.canvas, edge, (x + 22, y - 16), (x + 22, y), 2)
                    pg.draw.circle(self.canvas, edge, (x + 22, y - 8), 3)
                self.panel((x, y, 353, 138), INSET if known else (20, 36, 45), edge, 8)
                self.text(("I", "II", "III")[row], x + 14, y + 13, 13, colour, bold=True)
                self.text(tech.name, x + 46, y + 9, 21, TEXT, bold=True)
                self.text(f"{tech.cost} науки", x + 337, y + 15, 13, colour, align="right")
                self.paragraph(tech.effect, x + 14, y + 42, 326, 15, MUTED, 17)
                if known:
                    self.text("Изучено", x + 15, y + 108, 15, colour, bold=True)
                else:
                    self.text(error or ("Специализация" if tech.key in CAPSTONES else "Доступно"),
                              x + 15, y + 108, 13, MUTED)
                    self.button("Изучить", (x + 242, y + 99, 98, 30),
                                lambda key=tech.key: app.execute(game.research, key),
                                primary=not error, enabled=not error, size=14)
        self.text("III уровень требует академию. За партию можно выбрать одну специализацию.",
                  110, 702, 16, MUTED)
        self.button("К карте   ·   R", (1056, 691, 162, 40), app.toggle_research, size=16)

    def draw_help(self):
        x, y, w = 272, 83, 784
        self.panel((x, y, w, 646), PANEL, LINE, 12)
        self.text("Как играть", x + 38, y + 28, 43, TEXT, serif=True)
        self.text("Уничтожьте столицу или удержите оба маяка три своих хода.", x + 40, y + 95, 20, GOLD, bold=True)
        sections = (
            ("Ход", "За ход можно выполнить три действия. Доход поступает в начале вашего хода. "
                    "Разведанная местность остаётся на карте, но объекты за туманом скрыты."),
            ("Экономика", "Выберите проект справа и кликните по подсвеченной клетке. "
                         "Ставьте лесопилки в лесу, фермы на равнине, рудники в пещерах. "
                         "Города расширяют границы. Разведчики помогают занять новый берег."),
            ("Флот и бой", "Спускайте корабли рядом со своей верфью. Выберите корабль: голубые точки показывают, "
                          "куда он может доплыть, красные углы — кого можно атаковать. "
                          "Каждый корабль может один раз двигаться и один раз стрелять за ход."),
            ("Маяки и наука", "Маяк даёт науку, пока находится внутри ваших границ. Город удерживает берег, "
                               "когда разведчик уходит. Нажмите R, чтобы выбрать исследование."),
        )
        for index, (title, body) in enumerate(sections):
            py = y + 147 + index * 96
            pg.draw.line(self.canvas, LINE, (x + 38, py), (x + w - 38, py))
            self.text(title, x + 40, py + 14, 18, TEXT, bold=True)
            self.paragraph(body, x + 180, py + 13, w - 218, 17, MUTED, 21)
        self.text("Пробел · конец хода    Tab · следующий корабль    R · исследования    Esc · назад", x + 40, y + 555, 16, MUTED)
        self.button("Готово", (x + w - 184, y + 590, 145, 37), self.app.cancel, primary=True)
