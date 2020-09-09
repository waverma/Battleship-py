import pygame

from game_logic.game import Game
from game_logic.test_map import TestMap, TestCell
from game_logic.user_control import FieldControl
from game_logic.user_event import Size, Point, UserEvent


class Window(object):
    def __init__(self, size: Size, game: Game):
        pygame.init()
        self.display = pygame.display.set_mode((size.width, size.height))
        self.game = game

        # self.display.update()
        pygame.display.set_caption("Test name")

    def Run(self):
        is_closed = False

        while not is_closed:
            user_event = UserEvent()

            # обработка событий
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    is_closed = True

                if e.type == pygame.MOUSEBUTTONDOWN:
                    for c in self.game.user_controls:
                        if c.collision.contain(Point(e.pos[0], e.pos[1])):
                            user_event.focus_element = c
                            user_event.relatively_mouse_location = Point(e.pos[0] - c.collision.location.x,
                                                                         e.pos[1] - c.collision.location.y)

                    user_event.is_left_mouse_was_clicked_last_update = user_event.is_left_mouse_click
                    user_event.is_left_mouse_click = e.button == 1

                    user_event.is_right_mouse_was_clicked_last_update = user_event.is_right_mouse_click
                    user_event.is_right_mouse_click = e.button == 3

            # обновление игры
            controls = self.game.update(user_event)

            # отрисовка
            for control in controls:
                if True:
                    self.draw_map(control, Point(0, 0))

            pygame.display.update()

    def draw_rectangle(self, rectangle, color):
        pygame.draw.rect(self.display, color, rectangle)

    def draw_map(self, map: FieldControl, position: Point):
        for x in range(map.map.width):
            for y in range(map.map.height):
                cell = map.map.cells[x][y]

                if cell == TestCell.EMPTY:
                    self.draw_rectangle(
                        [position.x + x * map.cell_width,
                         position.y + y * map.cell_height,
                         map.cell_width, map.cell_height],
                        (255, 255, 255)
                    )
                if cell == TestCell.SHOT:
                    self.draw_rectangle(
                        [position.x + x * map.cell_width,
                         position.y + y * map.cell_height,
                         map.cell_width, map.cell_height],
                        (0, 255, 0)
                    )
                if cell == TestCell.SHIP_PEACE:
                    self.draw_rectangle(
                        [position.x + x * map.cell_width,
                         position.y + y * map.cell_height,
                         map.cell_width, map.cell_height],
                        (0, 0, 255)
                    )
                if cell == TestCell.DEAD_SHIP_PEACE:
                    self.draw_rectangle(
                        [position.x + x * map.cell_width,
                         position.y + y * map.cell_height,
                         map.cell_width, map.cell_height],
                        (255, 0, 0)
                    )


