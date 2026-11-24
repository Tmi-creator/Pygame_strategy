import json
import tempfile
import unittest
from pathlib import Path

from gneg import storage
from gneg.catalog import START_CAPITALS, START_SHIPS
from gneg.game import Game
from gneg.research import BEACONS, CONTROL_TURNS


class ResearchTest(unittest.TestCase):
    def test_prerequisites_cost_and_fleet_effect(self):
        game = Game("hotseat")
        scout = game._spawn("explorer", 0, (7, 5))
        before = game.reachable(scout)
        self.assertTrue(game.research("long_guns"))
        self.assertEqual((game.actions, game.science[0]), (3, 3))
        self.assertEqual(game.research("charts"), "")
        self.assertEqual((game.actions, game.science[0]), (2, 0))
        self.assertTrue(set(before) < set(game.reachable(scout)))
        self.assertTrue(game.research("charts"))
        self.assertEqual(game.actions, 2)

        game.science[0] = 5
        self.assertEqual(game.research("long_guns"), "")
        cruiser = game.pieces[START_SHIPS[0]]
        enemy = game._spawn("cruiser", 1, (13, 6))
        game._update_map()
        self.assertIn(enemy, game.targets(cruiser))
        self.assertEqual(game.attack(cruiser.pos, enemy.pos), "")
        self.assertEqual(enemy.hp, enemy.max_hp - cruiser.damage)

    def test_mobilization_needs_an_academy_and_is_exclusive(self):
        game = Game("hotseat")
        game.science[0] = 30
        game.researched[0].update(("workshops", "free_ports", "charts", "long_guns"))
        self.assertIn("академия", game.research("mobilization"))
        game._spawn("lab", 0, (3, 6))
        game._spawn("city", 0, (4, 7))
        game._spawn("city", 0, (5, 5))
        self.assertEqual(game.research("mobilization"), "")
        self.assertTrue(game.research("formation"))
        self.assertEqual((game.turn_capacity, game.actions), (3, 2))
        game.end_turn()
        game.end_turn()
        self.assertEqual((game.turn_capacity, game.actions), (4, 4))

    def test_economy_tech_changes_income_and_claims(self):
        game = Game("hotseat")
        game._spawn("sawmill", 0, (4, 5))
        city = game._spawn("city", 0, (7, 10))
        game._update_map()
        before = game.revenue(0)
        self.assertNotIn((10, 10), game.territory)
        self.assertEqual(game.research("workshops"), "")
        self.assertEqual(game.revenue(0)["wood"], before["wood"] + 4)
        game.science[0] = 5
        self.assertEqual(game.research("free_ports"), "")
        self.assertEqual(game.revenue(0)["gold"], before["gold"] + 6)
        self.assertEqual(game.territory[(10, 10)], city.owner)

    def test_squadron_and_forts_change_damage(self):
        game = Game("hotseat")
        cruiser = game.pieces[START_SHIPS[0]]
        game.researched[0].update(("charts", "long_guns", "formation"))
        game._spawn("explorer", 0, (8, 5))
        fort = game._spawn("wall", 1, (10, 8))
        city = game._spawn("city", 1, (11, 7))
        game.researched[1].add("masonry")
        game._update_map()
        self.assertEqual(game.attack(cruiser.pos, city.pos), "")
        self.assertEqual(city.max_hp - city.hp, cruiser.damage + 12 - 20)
        self.assertEqual(fort.hp, fort.max_hp)

    def test_repair_tech_and_tower_intercepts(self):
        game = Game("hotseat")
        ship = game._spawn("explorer", 0, (1, 6))
        ship.hp = 1
        self.assertTrue(game.repair(ship.pos))
        game.researched[0].update(("masonry", "field_service"))
        self.assertEqual(game.repair(ship.pos), "")
        self.assertEqual(ship.hp, 61)

        cruiser = game.pieces[START_SHIPS[0]]
        second = game._spawn("explorer", 0, (8, 5))
        tower = game._spawn("tower", 1, (9, 2))
        game.researched[1].update(("masonry", "field_service", "crossfire"))
        game._update_map()
        self.assertEqual(game.move(cruiser.pos, (9, 6)), "")
        self.assertEqual(cruiser.hp, cruiser.max_hp - tower.damage)
        self.assertEqual(game.move(second.pos, (9, 5)), "")
        self.assertEqual(second.hp, second.max_hp)

    def test_beacon_control_resets_on_loss_and_can_end_match(self):
        game = Game("hotseat")
        game._spawn("city", 0, (9, 2))
        game._spawn("city", 0, (14, 13))
        game._update_map()
        self.assertEqual(game.owned_beacons(0), BEACONS)
        self.assertEqual(game.science_income(0), 3)
        game.end_turn()
        game.end_turn()
        self.assertEqual(game.control[0], 1)
        self.assertEqual(game.science[0], 6)

        self.assertEqual(game.dismantle((9, 2)), "")
        self.assertEqual(game.control[0], 0)
        game._spawn("city", 0, (9, 2))
        game._update_map()
        for _ in range(CONTROL_TURNS):
            game.end_turn()
            game.end_turn()
        self.assertEqual((game.winner, game.win_reason), (0, "beacons"))
        self.assertTrue(all(capital in game.pieces for capital in START_CAPITALS))
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "match.json"
            storage.save(game, path)
            self.assertEqual(storage.load(path).__dict__, game.__dict__)

    def test_original_save_is_migrated(self):
        game = Game("hotseat")
        game.end_turn()
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "match.json"
            storage.save(game, path)
            payload = json.loads(path.read_text(encoding="utf-8"))
            payload["version"] = 1
            for key in ("turn_capacity", "win_reason", "science", "researched", "control"):
                del payload[key]
            for piece in payload["pieces"]:
                del piece["intercepted"]
            path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            migrated = storage.load(path)
            self.assertEqual(migrated.pieces, game.pieces)
            self.assertEqual(migrated.researched, [set(), set()])
            self.assertEqual(migrated.science, [3, 3])
            self.assertEqual(migrated.active, 1)
