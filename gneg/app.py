"""Window, input and screen transitions for Гнег."""

import argparse
import os
from collections import namedtuple

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame as pg

from . import opponent, storage
from .art import MAP_X, MAP_Y, TILE
from .audio import Audio
from .catalog import BUILD_GROUPS, COLS, PIECES, ROWS, START_CAPITALS
from .game import Game, inside
from .interface import Interface, SIZE

Hit = namedtuple("Hit", "rect action enabled")
AI_DELAY = 460


class App:
    def __init__(self, save_path=storage.SAVE_PATH):
        pg.mixer.pre_init(22050, -16, 1, 512)
        pg.init()
        desktop_w, desktop_h = pg.display.get_desktop_sizes()[0]
        scale = min(1, (desktop_w - 44) / SIZE[0], (desktop_h - 112) / SIZE[1])
        self.window_size = tuple(int(value * max(scale, 0.45)) for value in SIZE)
        self.screen = pg.display.set_mode(self.window_size, pg.RESIZABLE)
        pg.display.set_caption("Гнег · Война за архипелаг")
        self.view = Interface(self)
        pg.display.set_icon(self.view.icons["capital", 0])
        self.audio = Audio()
        self.clock = pg.time.Clock()
        self.fullscreen = False
        self.running = True
        self.hits = []
        self.mouse = (-1, -1)
        self.page = "menu"
        self.overlay = ""
        self.save_path = save_path
        self.saved = storage.load(save_path)
        self.save_error = ""
        self.game = None
        self.selected = None
        self.build_kind = None
        self.tab = "Промыслы"
        self.notice = ""
        self.notice_until = 0
        self.next_ai = 0
        self.result_at = 0
        self.result_seen = False
        self.effect = None
        self.pending_mode = ""

    @property
    def viewer(self):
        return 0 if self.game.mode == "solo" else self.game.active

    @property
    def can_control(self):
        return self.game.winner is None and self.viewer == self.game.active

    def notify(self, message):
        self.notice = message
        self.notice_until = pg.time.get_ticks() + 5200

    def persist(self):
        try:
            storage.save(self.game, self.save_path)
            self.saved = self.game
            self.save_error = ""
        except OSError:
            self.save_error = "Автосохранение недоступно."

    def enter_game(self, game, resume=False):
        self.game = game
        self.page = "match"
        self.selected = START_CAPITALS[self.viewer]
        self.build_kind = None
        self.tab = "Промыслы"
        self.notice = ""
        self.effect = None
        self.result_at = 0
        self.result_seen = False
        self.overlay = "handoff" if game.mode == "hotseat" else ""
        self.next_ai = pg.time.get_ticks() + AI_DELAY
        if game.winner is not None:
            self.overlay = "result"
            self.result_seen = True
        if not resume:
            self.persist()
            if game.mode == "solo":
                self.notify("Постройте лесопилку или выберите фрегат, чтобы выйти в море.")

    def new_game(self, mode):
        if self.saved and self.saved.winner is None:
            self.pending_mode, self.overlay = mode, "replace"
        else:
            self.enter_game(Game(mode))

    def main_menu(self):
        if self.game is not None:
            self.persist()
        self.page, self.overlay = "menu", ""

    def select_tab(self, tab):
        self.tab, self.build_kind = tab, None

    def choose_build(self, kind):
        if not self.can_control:
            return
        self.build_kind = None if self.build_kind == kind else kind
        if self.build_kind:
            visible = self.game.visible[self.viewer]
            if not self.game.afford(PIECES[kind].cost):
                self.notify("Не хватает ресурсов для этого проекта.")
            elif not any(not self.game.build_error(kind, pos) for pos in visible):
                self.notify("Сейчас нет подходящих свободных клеток для этого проекта.")
            else:
                self.notify("Выберите подсвеченную клетку на карте.")
        else:
            self.notice = ""

    def execute(self, action, *args):
        if not self.can_control:
            return
        error = action(*args)
        if error:
            self.notify(error)
            self.audio.play("click")
            return
        self.notice = ""
        self.process_change()
        if action == self.game.dismantle:
            self.audio.play("build")

    def process_change(self):
        event = self.game.events[-1]
        if (
            event.effect and self.viewer in event.audience and
            (event.target in self.game.visible[self.viewer] or self.game.winner is not None)
        ):
            self.effect = event, pg.time.get_ticks()
            self.audio.play(event.effect)
        self.persist()
        if self.game.winner is not None:
            self.result_at = pg.time.get_ticks() + 750

    def end_turn(self):
        if not self.can_control:
            return
        previous = self.game.events[-1]
        self.game.end_turn()
        if self.game.events[-1] is not previous:
            self.process_change()
        self.build_kind = None
        self.notice = ""
        self.audio.play("turn")
        self.persist()
        if self.game.winner is not None:
            return
        if self.game.mode == "hotseat":
            self.overlay = "handoff"
            self.effect = None
            self.selected = None
        else:
            self.next_ai = pg.time.get_ticks() + AI_DELAY

    def step_ai(self, now):
        if opponent.take_action(self.game):
            self.process_change()
            self.next_ai = now + AI_DELAY
        else:
            previous = self.game.events[-1]
            self.game.end_turn()
            if self.game.events[-1] is not previous:
                self.process_change()
            self.persist()
            if self.game.winner is None:
                self.audio.play("turn")
                self.notify("Ваш ход. Доход получен.")

    def reveal_turn(self):
        self.overlay = ""
        self.selected = START_CAPITALS[self.viewer]
        if self.game.round == 1:
            self.notify("Постройте лесопилку или выберите фрегат, чтобы выйти в море.")
        self.audio.play("turn")

    def map_click(self, pos):
        game = self.game
        if self.can_control and self.build_kind:
            kind = self.build_kind
            error = game.build(kind, pos)
            if error:
                self.notify(error)
                self.audio.play("click")
            else:
                self.selected, self.build_kind, self.notice = pos, None, ""
                self.process_change()
            return
        previous = game.pieces.get(self.selected)
        target = game.pieces.get(pos) if pos in game.visible[self.viewer] else None
        if self.can_control and previous and previous.owner == game.active and previous.spec.speed and pos != self.selected:
            if target and target.owner != game.active and target in game.targets(previous):
                self.execute(game.attack, previous.pos, pos)
                return
            if target is None and not previous.moved and pos in game.reachable(previous):
                self.execute(game.move, previous.pos, pos)
                self.selected = previous.pos
                return
        self.selected, self.notice = pos, ""
        self.audio.play("click")

    def next_ship(self):
        ships = [pos for pos, piece in self.game.pieces.items() if piece.owner == self.viewer and piece.spec.speed]
        if ships:
            index = (ships.index(self.selected) + 1) % len(ships) if self.selected in ships else 0
            self.selected = ships[index]
            self.build_kind = None

    def cancel(self):
        if self.overlay == "handoff":
            self.main_menu()
        elif self.overlay == "result":
            self.overlay = ""
        elif self.overlay == "help_pause":
            self.overlay = "pause"
        elif self.overlay:
            self.overlay = ""
        elif self.build_kind:
            self.build_kind = None
            self.notice = ""
        elif self.page == "match":
            self.overlay = "pause"

    def toggle_fullscreen(self):
        if not self.fullscreen:
            self.window_size = self.screen.get_size()
        self.fullscreen = not self.fullscreen
        flags = pg.FULLSCREEN if self.fullscreen else pg.RESIZABLE
        self.screen = pg.display.set_mode((0, 0) if self.fullscreen else self.window_size, flags)

    def toggle_audio(self):
        self.audio.enabled = not self.audio.enabled
        self.audio.play("click")

    def frame_bounds(self):
        w, h = self.screen.get_size()
        scale = min(w / SIZE[0], h / SIZE[1])
        size = round(SIZE[0] * scale), round(SIZE[1] * scale)
        return ((w - size[0]) // 2, (h - size[1]) // 2), size

    def virtual_pos(self, point):
        origin, size = self.frame_bounds()
        return tuple(int((value - offset) * base / drawn) for value, offset, base, drawn in zip(point, origin, SIZE, size))

    def handle(self, event):
        if event.type == pg.QUIT:
            self.running = False
        elif event.type == pg.KEYDOWN:
            key = event.key
            if key == pg.K_F11:
                self.toggle_fullscreen()
            elif key == pg.K_m:
                self.toggle_audio()
            elif key == pg.K_ESCAPE:
                self.cancel()
            elif self.overlay == "handoff" and key in (pg.K_RETURN, pg.K_SPACE):
                self.reveal_turn()
            elif key == pg.K_F1 and self.overlay in ("", "pause"):
                self.overlay = "help_pause" if self.page == "match" else "help"
            elif self.page == "match" and not self.overlay:
                if key == pg.K_SPACE:
                    self.end_turn()
                elif key == pg.K_TAB:
                    self.next_ship()
                elif key in (pg.K_1, pg.K_2, pg.K_3):
                    self.select_tab(tuple(BUILD_GROUPS)[key - pg.K_1])
        elif event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 3 and self.build_kind:
                self.cancel()
            elif event.button == 1:
                pos = self.virtual_pos(event.pos)
                for hit in reversed(self.hits):
                    if hit.rect.collidepoint(pos):
                        if hit.enabled:
                            self.audio.play("click")
                            hit.action()
                        return
                if self.page == "match" and not self.overlay:
                    cell = (pos[0] - MAP_X) // TILE, (pos[1] - MAP_Y) // TILE
                    if inside(cell):
                        self.map_click(cell)

    def update(self, now):
        if self.page != "match" or self.overlay:
            return
        if self.game.winner is not None and not self.result_seen and now >= self.result_at:
            self.overlay = "result"
            self.result_seen = True
            self.audio.play("win")
        elif self.game.mode == "solo" and self.game.active == 1 and self.game.winner is None and now >= self.next_ai:
            self.step_ai(now)

    def hit(self, rect, action, enabled=True):
        self.hits.append(Hit(pg.Rect(rect), action, enabled))

    def draw(self):
        self.mouse = self.virtual_pos(pg.mouse.get_pos())
        self.view.draw()
        origin, size = self.frame_bounds()
        self.screen.fill((7, 15, 22))
        frame = self.view.canvas if size == SIZE else pg.transform.smoothscale(self.view.canvas, size)
        self.screen.blit(frame, origin)
        pg.display.flip()

    def run(self):
        try:
            while self.running:
                self.clock.tick(60)
                self.update(pg.time.get_ticks())
                self.draw()
                for event in pg.event.get():
                    state = self.page, self.overlay
                    self.handle(event)
                    if state != (self.page, self.overlay):
                        self.hits.clear()
        finally:
            pg.quit()


def main():
    parser = argparse.ArgumentParser(description="Гнег · Война за архипелаг")
    parser.add_argument("--smoke-test", action="store_true", help=argparse.SUPPRESS)
    args = parser.parse_args()
    app = App()
    if args.smoke_test:
        app.draw()
        pg.quit()
        return
    app.run()
