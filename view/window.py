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

        pygame.display.set_caption("Test name")

    def Run(self):
        is_closed = False

        while not is_closed:
            user_event = UserEvent()

            # обработка событий
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    is_closed = True

                if e.type == pygame.KEYDOWN:
                    user_event.was_enter_pressed_last_update = user_event.is_enter_pressed
                    user_event.is_enter_pressed = pygame.key.get_pressed()[pygame.K_SPACE]

                if e.type == pygame.MOUSEBUTTONDOWN:

                    for c in self.game.user_controls:
                        if c.enable and c.collision.contain(Point(e.pos[0], e.pos[1])):
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
            if controls is not None:
                for control in controls:
                    if True:
                        self.draw_map(control, Point(control.wx, control.wy), control.is_user_mode)

            pygame.display.update()

    def draw_rectangle(self, rectangle, color):
        pygame.draw.rect(self.display, color, rectangle)

    def draw_map(self, map: FieldControl, position: Point, is_player_mode: bool):
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
                    color = (0, 0, 0)
                    if is_player_mode:
                        color = (0, 0, 255)
                    else:
                        color = (255, 255, 255)
                    self.draw_rectangle(
                        [position.x + x * map.cell_width,
                         position.y + y * map.cell_height,
                         map.cell_width, map.cell_height],
                        color
                    )
                if cell == TestCell.DEAD_SHIP_PEACE:
                    self.draw_rectangle(
                        [position.x + x * map.cell_width,
                         position.y + y * map.cell_height,
                         map.cell_width, map.cell_height],
                        (255, 0, 0)
                    )



