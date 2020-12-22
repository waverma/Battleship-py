from typing import Tuple

import pygame
from pygame.rect import Rect

from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.buffers.drawing_buffer import DrawingBuffer
from battleship.buffers.user_event import UserEvent
from battleship.engine.game_constants import DEFAULT_FIELD_SIZE
from battleship.view.draw_information import DrawInformation
from battleship.view.graphic_utils import (
    CELL_SIZE,
    DEFAULT_DISPLAY_COLOR,
    LEFT_LABEL_RECT,
    RIGHT_LABEL_RECT,
)
from battleship.view.gui_elements.game_field_element import GameFieldElement
from battleship.view.gui_elements.text import Text
from battleship.view.gui_elements.user_element import UserElement


class GameMenu(UserElement):
    def __init__(self, rect: Rect, absolute_position: Tuple):
        super().__init__(rect, absolute_position)
        self.buttons = list()
        self.back_color = DEFAULT_DISPLAY_COLOR

        self.player_field_element = GameFieldElement(
            Rect(CELL_SIZE, CELL_SIZE,
                 CELL_SIZE * DEFAULT_FIELD_SIZE[0],
                 CELL_SIZE * DEFAULT_FIELD_SIZE[1]),
            (CELL_SIZE, CELL_SIZE)
        )

        self.bot_field_element = GameFieldElement(
            Rect(CELL_SIZE * 8, CELL_SIZE,
                 CELL_SIZE * DEFAULT_FIELD_SIZE[0],
                 CELL_SIZE * DEFAULT_FIELD_SIZE[1]),
            (CELL_SIZE * 8, CELL_SIZE)
        )

        self.my_field_text_marker = Text(
            LEFT_LABEL_RECT,
            (LEFT_LABEL_RECT.x, LEFT_LABEL_RECT.y),
            "МОЁ ОЗЕРО",
        )

        self.bot_field_text_marker = Text(
            RIGHT_LABEL_RECT,
            (RIGHT_LABEL_RECT.x, RIGHT_LABEL_RECT.y),
            "НЕ МОЁ ОЗЕРО",
        )

    def update(self, e: UserEvent, output_buffer: BufferToGameLogic):
        self.player_field_element.update(e, output_buffer)
        self.bot_field_element.update(e, output_buffer)

        output_buffer.is_pause_request = (
                e.pressed_buttons[pygame.K_ESCAPE] and
                len(e.non_released_buttons) > 0 and
                not e.non_released_buttons[pygame.K_ESCAPE]
        )

    def get_render_info(
        self,
        transform: Tuple,
        buffer_to_render: BufferToRender,
        buffer_to_draw: DrawingBuffer = None,
    ):
        new_transform = (
            transform[0] + self.collision.x,
            transform[1] + self.collision.y,
            1,
            1,
        )
        result = list()
        buffer_to_draw.add(
            DrawInformation(
                transform=transform,
                draw_rect=self.collision,
                fill_color=self.back_color,
            )
        )

        for text_render_info in self.my_field_text_marker.get_render_info(
                new_transform, buffer_to_render
        ):
            buffer_to_draw.add(text_render_info)

        for text_render_info in self.bot_field_text_marker.get_render_info(
                new_transform, buffer_to_render
        ):
            buffer_to_draw.add(text_render_info)

        self.player_field_element.get_render_info(new_transform,
                                                  buffer_to_render,
                                                  buffer_to_draw, False)

        self.bot_field_element.get_render_info(new_transform,
                                               buffer_to_render,
                                               buffer_to_draw, True)

        return result
