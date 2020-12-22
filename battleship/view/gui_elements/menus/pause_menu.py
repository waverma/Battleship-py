from typing import Tuple

import pygame
from pygame.rect import Rect

from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.buffers.user_event import UserEvent
from battleship.view.draw_information import DrawInformation
from battleship.view.graphic_utils import (
    DEFAULT_DISPLAY_COLOR,
    LEFT_BUTTON_RECT,
    RED_BLUE_COLOR,
    RIGHT_BUTTON_RECT,
)
from battleship.view.gui_elements.button import Button
from battleship.view.gui_elements.user_element import UserElement


class PauseMenu(UserElement):
    def __init__(self, rect: Rect, absolute_position: Tuple):
        super().__init__(rect, absolute_position)
        self.buttons = list()
        self.back_color = DEFAULT_DISPLAY_COLOR

        self.continue_button = Button(
            LEFT_BUTTON_RECT,
            (absolute_position[0], absolute_position[1]),
            "Продолжить",
        )

        self.exit_button = Button(
            RIGHT_BUTTON_RECT,
            (absolute_position[0], absolute_position[1]),
            "В главное меню",
        )

        self.buttons.append(self.continue_button)
        self.buttons.append(self.exit_button)
        self.text_size = 36
        self.text_color = RED_BLUE_COLOR

    def update(self, e: UserEvent, output_buffer: BufferToGameLogic):
        for button in self.buttons:
            button.update(e, output_buffer)

        output_buffer.is_return_button_pressed = (
            e.pressed_buttons[pygame.K_ESCAPE]
            and len(e.non_released_buttons) > 0
            and not e.non_released_buttons[pygame.K_ESCAPE]
        ) or self.continue_button.is_clicked
        output_buffer.is_to_main_menu_button_pressed = (
            self.exit_button.is_clicked
        )

    def get_render_info(
        self, transform: Tuple, buffer_to_render: BufferToRender
    ):
        new_transform = (
            transform[0] + self.collision.x,
            transform[1] + self.collision.y,
            1,
            1,
        )
        result = list()
        result.append(
            DrawInformation(
                transform=transform,
                draw_rect=self.collision,
                fill_color=self.back_color,
            )
        )

        for button in self.buttons:
            button_info = button.get_render_info(
                new_transform, buffer_to_render
            )
            for button_info_parts in button_info:
                result.append(button_info_parts)

        return result
