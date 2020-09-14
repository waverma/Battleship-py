import pygame

from game_logic.game import Game
from game_logic.point import Point
from game_logic.size import Size
from game_logic.user_event import UserEvent


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
            self.display.fill((0, 0, 0))

            # обработка событий
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    is_closed = True

                if e.type == pygame.KEYDOWN:
                    user_event.was_enter_pressed_last_update = user_event.is_enter_pressed
                    user_event.is_enter_pressed = pygame.key.get_pressed()[pygame.K_SPACE]

                    user_event.was_1_pressed_last_update = user_event.is_1_pressed
                    user_event.is_1_pressed = pygame.key.get_pressed()[pygame.K_1]

                    user_event.was_2_pressed_last_update = user_event.is_2_pressed
                    user_event.is_2_pressed = pygame.key.get_pressed()[pygame.K_2]

                    user_event.was_3_pressed_last_update = user_event.is_3_pressed
                    user_event.is_3_pressed = pygame.key.get_pressed()[pygame.K_3]

                    user_event.was_4_pressed_last_update = user_event.is_4_pressed
                    user_event.is_4_pressed = pygame.key.get_pressed()[pygame.K_4]

                if e.type == pygame.MOUSEBUTTONDOWN:

                    for c in self.game.user_controls:
                        if c.enable and c.x <= e.pos[0] <= c.width + c.x and c.y <= e.pos[1] <= c.height + c.y:
                            user_event.focus_element = c
                            user_event.relatively_mouse_location = Point(e.pos[0] - c.x, e.pos[1] - c.y)

                    user_event.is_left_mouse_was_clicked_last_update = user_event.is_left_mouse_click
                    user_event.is_left_mouse_click = e.button == 1

                    user_event.is_right_mouse_was_clicked_last_update = user_event.is_right_mouse_click
                    user_event.is_right_mouse_click = e.button == 3

            # обновление игры
            controls = self.game.update(user_event)

            # отрисовка
            print(self.game.current_ship_type)

            if controls is not None:
                for control in controls:
                    control.draw(self.display)

            pygame.display.update()
