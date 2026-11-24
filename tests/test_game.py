import json
import tempfile
import unittest
from pathlib import Path

from gneg import opponent, storage
from gneg.catalog import ACTIONS, COLS, PIECES, ROWS, START_CAPITALS, START_SHIPS, START_YARDS
from gneg.game import Game


class GameRulesTest(unittest.TestCase):
    def setUp(self):
        self.game = Game("hotseat")

    def test_starting_layout_and_fog_are_symmetric(self):
        game = self.game
        self.assertEqual(game.map, tuple(row[::-1] for row in game.map[::-1]))
        self.assertTrue(all(len(row) == COLS for row in game.map))
        self.assertEqual(len(game.map), ROWS)
        self.assertNotIn(START_CAPITALS[1], game.visible[0])
        self.assertNotIn(START_CAPITALS[0], game.visible[1])
        self.assertEqual(game.stock[0], game.stock[1])
        self.assertEqual(game.revenue(0), game.revenue(1))

    def test_failed_build_is_free_and_valid_build_spends_resources(self):
        game = self.game
        stock = game.stock[0].copy()
        self.assertTrue(game.build("sawmill", (-1, 2)))
        self.assertTrue(game.build("sawmill", START_CAPITALS[0]))
        self.assertTrue(game.build("cruiser", (10, 6)))
        self.assertEqual(game.stock[0], stock)
        self.assertEqual(game.actions, ACTIONS)
        self.assertEqual(game.build("sawmill", (4, 5)), "")
        self.assertEqual(game.actions, ACTIONS - 1)
        self.assertEqual(game.stock[0]["wood"], stock["wood"] - dict(PIECES["sawmill"].cost)["wood"])
        gold = game.stock[0]["gold"]
        game.end_turn()
        self.assertEqual(game.stock[0]["gold"], gold)
        game.end_turn()
        self.assertEqual(game.stock[0]["gold"], gold + game.revenue(0)["gold"])

    def test_move_and_attack_are_independent_and_reset_next_turn(self):
        game = self.game
        ship = game.pieces[START_SHIPS[0]]
        destination = (9, 6)
        enemy = game._spawn("cruiser", 1, (10, 6))
        game._update_map()
        self.assertTrue(game.move(ship.pos, enemy.pos))
        self.assertEqual(game.move(ship.pos, destination), "")
        self.assertTrue(game.move(ship.pos, (9, 5)))
        self.assertEqual(game.attack(ship.pos, enemy.pos), "")
        self.assertEqual(enemy.hp, enemy.max_hp - ship.damage)
        self.assertTrue(game.attack(ship.pos, enemy.pos))
        game.end_turn()
        game.end_turn()
        self.assertFalse(ship.moved)
        self.assertFalse(ship.fired)
        self.assertEqual(game.actions, ACTIONS)

    def test_tower_fort_and_capital_victory(self):
        game = self.game
        game._spawn("tower", 0, (5, 7))
        enemy = game._spawn("cruiser", 1, (7, 8))
        game._update_map()
        game.end_turn()
        self.assertEqual(enemy.hp, enemy.max_hp - PIECES["tower"].damage)

        game = Game("hotseat")
        capital = game.pieces[START_CAPITALS[1]]
        attacker = game._spawn("artillery", 0, (15, 8))
        game._spawn("wall", 1, (18, 9))
        game._update_map()
        self.assertEqual(game.attack(attacker.pos, capital.pos), "")
        self.assertEqual(capital.hp, capital.max_hp - (attacker.damage - 12))
        capital.hp = 1
        game.end_turn()
        game.end_turn()
        self.assertEqual(game.attack(attacker.pos, capital.pos), "")
        self.assertEqual(game.winner, 0)
        self.assertNotIn(capital.pos, game.pieces)
        self.assertTrue(game.build("sawmill", (4, 5)))

    def test_upgrades_repairs_and_dismantle(self):
        game = self.game
        yard = game.pieces[START_YARDS[0]]
        yard.hp -= 50
        self.assertEqual(game.upgrade(yard.pos), "")
        self.assertEqual(yard.level, 2)
        self.assertEqual(yard.hp, yard.max_hp - 50)
        self.assertEqual(game.repair(yard.pos), "")
        self.assertEqual(yard.hp, yard.max_hp - 4)
        self.assertTrue(game.repair(yard.pos))
        self.assertTrue(game.dismantle(START_CAPITALS[0]))
        self.assertEqual(game.dismantle(yard.pos), "")
        self.assertNotIn(yard.pos, game.pieces)
        self.assertEqual(game.terrain_at(yard.pos), "~")

    def test_save_round_trip_and_corruption(self):
        game = self.game
        game.build("sawmill", (4, 5))
        game.end_turn()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "match.json"
            storage.save(game, path)
            recovered = storage.load(path)
            self.assertIsNotNone(recovered)
            self.assertEqual(recovered.__dict__, game.__dict__)
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["pieces"][0]["pos"] = [-1, 0]
            path.write_text(json.dumps(payload), encoding="utf-8")
            self.assertIsNone(storage.load(path))

    def test_solo_opponent_can_finish_a_match(self):
        game = Game("solo")
        while game.winner is None and game.round <= 20:
            if game.active == 1:
                while opponent.take_action(game):
                    pass
            game.end_turn()
        self.assertEqual(game.winner, 1)


if __name__ == "__main__":
    unittest.main()
