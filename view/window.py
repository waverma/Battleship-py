import pygame

from game_logic.game import Game
from game_logic.point import Point
from game_logic.user_event import UserEvent


class Window(object):
    def __init__(self, width, height, game: Game):
        pygame.init()
        self.display = pygame.display.set_mode((width, height))
        self.game = game
        self.is_window_closed = False

        pygame.display.set_caption("Test name")

    def run(self):
        while not self.is_window_closed:
            self.display.fill((30, 213, 200))

            # обновление игры
            self.game.update(self.event_update())

            # отрисовка
            for control in self.game.draw_buffer:
                control.draw(self.display)

            pygame.display.update()

    def event_update(self) -> UserEvent:
        user_event = UserEvent()
        user_event.pressed_keys_list = list()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                self.is_window_closed = True

            if e.type == pygame.KEYDOWN:
                user_event.pressed_keys_list = pygame.key.get_pressed()

            if e.type == pygame.MOUSEBUTTONDOWN:
                user_event.absolute_mouse_location = Point(e.pos[0], e.pos[1])
                user_event.is_left_mouse_click = e.button == 1
                user_event.is_right_mouse_click = e.button == 3

                self.game.user_interface.update(user_event)

        return user_event
