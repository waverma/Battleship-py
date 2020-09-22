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
        self.colors[Cell.EMPTY] = (94, 242, 198)
        self.colors[Cell.POSSIBLE_SHIP_PLACE] = (255, 255, 0)
        self.colors[Cell.SHIP_PEACE] = (0, 0, 255)

        self.padding = 1

        # self.back_color = (255, 216, 214)

    def on_left_mouse(self, e):
        cell_point = Point(
            e.relatively_mouse_location.x // e.focus_element.cell_width,
            e.relatively_mouse_location.y // e.focus_element.cell_height
        )

        if self.map.is_battle_mode:
            if self.map.try_strike(cell_point):
                AI.generate_random_shot(self.game.player_field_control.map)
        else:
            if self.map.ship_count[self.game.current_ship_type] > 0 and \
                    self.map.try_set_new_peace_of_ship(cell_point, self.game.current_ship_type):
                self.map.ship_count[self.game.current_ship_type] -= 1

    def on_right_mouse(self, e):
        cell_point = Point(
            e.relatively_mouse_location.x // e.focus_element.cell_width,
            e.relatively_mouse_location.y // e.focus_element.cell_height
        )

        if not self.map.is_battle_mode:
            r = self.map.try_remove_peace_of_ship(cell_point)
            if r[0]:
                self.map.ship_count[r[1]] += 1

    def draw(self, display):
        for x in range(self.map.width):
            for y in range(self.map.height):
                rect = [self.x + x * self.cell_width + self.padding,
                        self.y + y * self.cell_height + self.padding,
                        self.cell_width - self.padding*2,
                        self.cell_height - self.padding*2]
                if Point(x, y) in self.map.last_ship_cell and not self.is_user_mode:
                    pygame.draw.rect(display, (0, 0, 0), rect)
                else:
                    pygame.draw.rect(display, self.colors[self.map.cells[x][y]], rect)
