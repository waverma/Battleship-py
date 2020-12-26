import _tkinter
from tkinter import Tk
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
    RIGHT_BUTTON_RECT, CELL_SIZE, INFO_TEXT,
)
from battleship.view.gui_elements.button import Button
from battleship.view.gui_elements.text import Text
from battleship.view.gui_elements.user_element import UserElement


class VkAuthorizationMenu(UserElement):
    def __init__(self, rect: Rect, absolute_position: Tuple):
        super().__init__(rect, absolute_position)
        self.buttons = list()
        self.back_color = DEFAULT_DISPLAY_COLOR

        self.to_browser_button = Button(
            LEFT_BUTTON_RECT,
            (absolute_position[0], absolute_position[1]),
            "Перейти",
        )

        self.apply_button = Button(
            RIGHT_BUTTON_RECT,
            (absolute_position[0], absolute_position[1]),
            "Подтвердить",
        )

        self.url_text = Text(
            Rect(0, CELL_SIZE * 7, CELL_SIZE * 27, CELL_SIZE),
            (0, CELL_SIZE * 7),
        )
        self.url_text.draw_info.text_size = 14

        self.text = Text(
            Rect(0, CELL_SIZE * 5, CELL_SIZE * 27, CELL_SIZE),
            (0, CELL_SIZE * 5),
            text=INFO_TEXT
        )
        self.text.draw_info.text_size = 14

        self.back_button = Button(
            Rect(CELL_SIZE * 16, CELL_SIZE * 10, CELL_SIZE * 10,
                 CELL_SIZE * 2),
            (absolute_position[0], absolute_position[1]),
            "В главное меню"
        )

        self.buttons.append(self.to_browser_button)
        self.buttons.append(self.apply_button)
        self.buttons.append(self.back_button)
        self.text_size = 36
        self.text_color = RED_BLUE_COLOR

    def update(self, e: UserEvent, output_buffer: BufferToGameLogic):
        for button in self.buttons:
            button.update(e, output_buffer)

        output_buffer.apply = self.apply_button.is_clicked
        output_buffer.to_browser_request = self.to_browser_button.is_clicked
        if (
            e.pressed_buttons[pygame.K_v]
            and len(e.non_released_buttons) > 0
            and not e.non_released_buttons[pygame.K_v]
        ):
            try:
                c = Tk()
                c.withdraw()
                output_buffer.url = c.clipboard_get()
                c.update()
                c.destroy()
            except _tkinter.TclError:
                pass
        output_buffer.is_return_button_pressed = (
            self.back_button.is_clicked
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

        self.url_text.draw_info.text = buffer_to_render.url
        text_render_info = self.url_text.get_render_info(
            new_transform, buffer_to_render
        )
        for text_render_info_parts in text_render_info:
            result.append(text_render_info_parts)

        text_render_info = self.text.get_render_info(
            new_transform, buffer_to_render
        )
        for text_render_info_parts in text_render_info:
            result.append(text_render_info_parts)

        for button in self.buttons:
            button_info = button.get_render_info(
                new_transform, buffer_to_render
            )
            for button_info_parts in button_info:
                result.append(button_info_parts)

        return result
