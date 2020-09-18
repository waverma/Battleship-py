import unittest

from game_logic.ai import AI
from game_logic.enums.cell import Cell
from game_logic.enums.game_stage import GameStage
from game_logic.game import Game
from game_logic.point import Point


class GameTests(unittest.TestCase):
    def setUp(self) -> None:
        self.game = Game()

    def test_try_begin(self):
        assert not self.game.try_begin()
        self.game.player_field_control.map = AI.generate_random_map()

        assert self.game.try_begin()
        assert self.game.stage == GameStage.GAME

        ship_peace_count = 0
        possible_ship_peace_count = 0
        for x in range(self.game.player_field_control.map.width):
            for y in range(self.game.player_field_control.map.height):
                if self.game.player_field_control.map.cells[x][y] == Cell.SHIP_PEACE:
                    ship_peace_count += 1
                if self.game.player_field_control.map.cells[x][y] == Cell.POSSIBLE_SHIP_PLACE:
                    possible_ship_peace_count += 1

        assert ship_peace_count == 20
        assert possible_ship_peace_count == 0

    def test_is_completed(self):
        for i in range(10):
            self.game.player_field_control.map = AI.generate_random_map()
            self.game.try_begin()

            assert not self.game.is_completed()[0]
            assert not self.game.is_completed()[1]

            for x in range(self.game.bot_field_control.map.width):
                for y in range(self.game.bot_field_control.map.height):
                    self.game.bot_field_control.map.strike(Point(x, y))

            assert self.game.is_completed()[0]
            assert self.game.is_completed()[1]

            self.game.bot_field_control.map = AI.generate_random_map()
            for x in range(self.game.player_field_control.map.width):
                for y in range(self.game.player_field_control.map.height):
                    self.game.player_field_control.map.strike(Point(x, y))

            assert self.game.is_completed()[0]
            assert not self.game.is_completed()[1]

    def test_update(self):
        pass


if __name__ == '__main__':
    unittest.main()
