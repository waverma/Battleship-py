import time

import pygame

from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.buffers.drawing_buffer import DrawingBuffer
from battleship.buffers.user_event import UserEvent
from battleship.engine.game import Game
from battleship.enums import InterfaceStage
from battleship.view.graphic_utils import DEFAULT_DISPLAY_COLOR
from battleship.view.gui_elements.user_interface import UserInterface


class GameLoop:
    def __init__(self, width, height):
        # настройка PyGame
        pygame.init()
        self.display = pygame.display.set_mode(
            (width, height), pygame.DOUBLEBUF
        )
        self.is_window_closed = False
        pygame.display.set_caption("BattleShip")

        self.buffer_to_draw = DrawingBuffer()
        self.buffer_to_render = BufferToRender()
        self.buffer_to_game_logic = BufferToGameLogic()
        self.buffer_to_game_logic.interface_stage = InterfaceStage.MainMenu
        self.events = UserEvent()
        self.game = Game()
        self.user_interface = UserInterface()
        self.mouse_pos = (0, 0)

        self.clock = pygame.time.Clock()

    def run(self):
        while not self.is_window_closed:
            start_time = time.time()
            self.clock.tick(60)
            self.display.fill(DEFAULT_DISPLAY_COLOR)

            self.buffer_to_draw = DrawingBuffer()
            self.buffer_to_render = BufferToRender()
            self.buffer_to_game_logic = BufferToGameLogic()

            self.get_event()
            self.user_interface.update(
                self.events, self.game.stage, self.buffer_to_game_logic
            )
            self.game.update(self.buffer_to_game_logic, self.buffer_to_render)
            self.user_interface.render(
                self.buffer_to_render, self.buffer_to_draw
            )
            self.draw(self.buffer_to_draw)

            if self.buffer_to_game_logic.is_exit_button_pressed:
                quit()

            pygame.display.update()

            pygame.display.set_caption(str(1.0 / (time.time() - start_time)))

    def get_event(self):
        if self.events.pressed_buttons is None or \
                len(self.events.pressed_buttons) == 0:
            self.events.pressed_buttons = [0 for _ in range(513)]
        self.events.was_left_mouse_click = self.events.is_left_mouse_click
        self.events.was_right_mouse_click = self.events.is_right_mouse_click
        self.events.non_released_buttons = self.events.pressed_buttons
        self.events.events = pygame.event.get()

        self.events.entered_keys = self.events.entered_keys[-20:]
        self.events.is_left_mouse_click = False
        self.events.is_right_mouse_click = False

        for e in self.events.events:
            if e.type == pygame.QUIT:
                self.is_window_closed = True

            if e.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                self.events.pressed_buttons = keys
                self.events.entered_keys.append(e.unicode)

            if e.type == pygame.KEYUP:
                keys = pygame.key.get_pressed()
                self.events.pressed_buttons = keys

            if e.type == pygame.MOUSEMOTION:
                self.mouse_pos = e.pos

            if e.type == pygame.MOUSEBUTTONDOWN:
                self.events.is_left_mouse_click = e.button == 1
                self.events.is_right_mouse_click = e.button == 3

        self.events.absolute_mouse_location = self.mouse_pos

        self.events = self.events

    def draw(self, buffer: DrawingBuffer):
        for draw_element in buffer.store:

            x = (
                draw_element.draw_rect.x * draw_element.transform[2]
                + draw_element.transform[0]
            )
            y = (
                draw_element.draw_rect.y * draw_element.transform[3]
                + draw_element.transform[1]
            )
            width = draw_element.draw_rect.width * draw_element.transform[2]
            height = draw_element.draw_rect.height * draw_element.transform[3]

            if (
                draw_element.outline_size is not None
                and draw_element.outline_color is not None
            ):
                outline_rect = [
                    x - draw_element.outline_size,
                    y - draw_element.outline_size,
                    width + draw_element.outline_size * 2,
                    height + draw_element.outline_size * 2,
                ]
                pygame.draw.rect(
                    self.display, draw_element.outline_color, outline_rect
                )

            if draw_element.fill_color is not None:
                pygame.draw.rect(
                    self.display,
                    draw_element.fill_color,
                    [x, y, width, height],
                )

            if draw_element.text is not None:
                self.display.blit(
                    pygame.font.SysFont(
                        "arial", draw_element.text_size
                    ).render(draw_element.text, True, draw_element.text_color),
                    (x, y),
                )
