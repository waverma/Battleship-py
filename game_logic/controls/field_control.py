import pygame

from game_logic.enums.cell import Cell
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

    def draw_map(self, display):
        for x in range(self.map.width):
            for y in range(self.map.height):
                pygame.draw.rect(
                    display, self.colors[self.map.cells[x][y]],
                    [self.wx + x * self.cell_width, self.wy + y * self.cell_height, self.cell_width, self.cell_height])
