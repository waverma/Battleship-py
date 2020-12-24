from unittest import TestCase

from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.engine.field import Field
from battleship.engine.game import Game
from battleship.enums import InterfaceStage


class TestGame(TestCase):
    def test_extract_to_render(self):
        game = Game()
        game.bot_field = Field(Field.get_arrange_ships())
        game.player_field = Field(Field.get_arrange_ships())
        buffer = BufferToGameLogic()
        buffer_to_render = BufferToRender()
        game.extract_to_render(BufferToGameLogic(), buffer_to_render)

        self.assertEqual(len(buffer_to_render.player_cells), 100)
        self.assertEqual(len(buffer_to_render.bot_cells), 100)
        self.assertEqual(len(buffer_to_render.pre_show_cell), 0)

        game = Game()
        buffer.pre_show_cell_index = (1, 1)
        buffer_to_render = BufferToRender()
        game.extract_to_render(buffer, buffer_to_render)
        self.assertEqual(len(buffer_to_render.pre_show_cell), 1)

    def test_update(self):
        game = Game()
        buffer = BufferToGameLogic()
        buffer.interface_stage = InterfaceStage.PrepareToGame
        buffer.rotate_request = True
        buffer.random_field_request = True
        game.update(buffer, BufferToRender())

        self.assertEqual(len(game.player_field.ships), 10)

    def test_is_game_completed(self):
        game = Game()

        game_result = game.is_game_completed()
        game.bot_field = Field()
        self.assertFalse(game_result[0])
        self.assertFalse(game_result[1])
        game.bot_field = Field(Field.get_arrange_ships())
        game.player_field = Field(Field.get_arrange_ships())

        game_result = game.is_game_completed()
        self.assertFalse(game_result[0])
        self.assertTrue(game_result[1])

        for _ in range(100):
            game.bot_field = Field(Field.get_arrange_ships())

        game_result = game.is_game_completed()
        self.assertTrue(game_result[0])
        self.assertTrue(game_result[1])

        game.bot_field = Field(Field.get_arrange_ships())
        for _ in range(100):
            game.player_field = Field(Field.get_arrange_ships())

        game_result = game.is_game_completed()
        self.assertTrue(game_result[0])
        self.assertFalse(game_result[1])
