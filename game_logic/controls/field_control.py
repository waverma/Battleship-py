import random

import pygame

from game_logic.ai import AI
from game_logic.enums.cell import Cell
from game_logic.point import Point
from game_logic.user_control import UserControl


class FieldControl(UserControl):
    def __init__(self, x: int, y: int, width: int, height: int, cell_width: int, cell_height: int):
        super().__init__(x, y, width*cell_width, height*cell_height)

        self.is_user_mode = True
        self.cell_width = cell_width
        self.cell_height = cell_height

        self.map = None

        self.colors = dict()
        self.colors[Cell.DEAD_SHIP_PEACE] = (255, 0, 0)
        self.colors[Cell.SHOT] = (0, 255, 0)
        self.colors[Cell.EMPTY] = (255, 255, 255)
        self.colors[Cell.POSSIBLE_SHIP_PLACE] = (255, 255, 0)
        self.colors[Cell.SHIP_PEACE] = (0, 0, 255)

    def on_left_mouse(self, e):
        cell_point = Point(
            e.relatively_mouse_location.x // e.focus_element.cell_width,
            e.relatively_mouse_location.y // e.focus_element.cell_height
        )

        if self.map.is_battle_mode:
            self.game.bot_field.strike(cell_point)

            AI.generate_random_shot(self.game.player_field)
        else:
            if self.game.ship_count[self.game.current_ship_type] != self.game.ship_count_limit[
                self.game.current_ship_type] and \
                    self.game.player_field.try_set_new_peace_of_ship(cell_point, self.game.current_ship_type):
                self.game.ship_count[self.game.current_ship_type] += 1

    def on_right_mouse(self, e):
        cell_point = Point(
            e.relatively_mouse_location.x // e.focus_element.cell_width,
            e.relatively_mouse_location.y // e.focus_element.cell_height
        )

        if self.map.is_battle_mode:
            pass
        else:
            r = self.game.player_field.try_remove_new_peace_of_ship(cell_point)
            if r[0]:
                self.game.ship_count[r[1]] -= 1

    def draw(self, display):
        for x in range(self.map.width):
            for y in range(self.map.height):
                pygame.draw.rect(
                    display, self.colors[self.map.cells[x][y]],
                    [self.x + x * self.cell_width, self.y + y * self.cell_height, self.cell_width, self.cell_height])
