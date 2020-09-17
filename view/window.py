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
        self.is_window_closed = False

        pygame.display.set_caption("Test name")

    def run(self):
        while not self.is_window_closed:

            self.display.fill((0, 0, 0))

            # обновление игры
            controls = self.game.update(self.event_update())

            # отрисовка
            print(self.game.current_ship_type)

            for control in self.game.draw_buffer:
                control.draw(self.display)

            pygame.display.update()

    def event_update(self) -> UserEvent:
        user_event = UserEvent()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_window_closed = True

            if e.type == pygame.KEYDOWN:
                # user_event.was_enter_pressed_last_update = user_event.is_enter_pressed
                # user_event.is_enter_pressed = pygame.key.get_pressed()[pygame.K_SPACE]
                #
                # user_event.was_1_pressed_last_update = user_event.is_1_pressed
                # user_event.is_1_pressed = pygame.key.get_pressed()[pygame.K_1]
                #
                # user_event.was_2_pressed_last_update = user_event.is_2_pressed
                # user_event.is_2_pressed = pygame.key.get_pressed()[pygame.K_2]
                #
                # user_event.was_3_pressed_last_update = user_event.is_3_pressed
                # user_event.is_3_pressed = pygame.key.get_pressed()[pygame.K_3]
                #
                # user_event.was_4_pressed_last_update = user_event.is_4_pressed
                # user_event.is_4_pressed = pygame.key.get_pressed()[pygame.K_4]
                #
                user_event.pressed_keys_list = pygame.key.get_pressed()

            if e.type == pygame.MOUSEBUTTONDOWN:
                user_event.absolute_mouse_location = Point(e.pos[0], e.pos[1])
                user_event.is_left_mouse_click = e.button == 1
                user_event.is_right_mouse_click = e.button == 3

                self.game.user_interface.update(user_event)

        return user_event
