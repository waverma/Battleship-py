from typing import Tuple

from pygame.rect import Rect

from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.buffers.user_event import UserEvent
from battleship.view.draw_information import DrawInformation
from battleship.view.graphic_utils import (
    DEFAULT_DISPLAY_COLOR,
    LEFT_BUTTON_RECT,
    RIGHT_BUTTON_RECT,
)
from battleship.view.gui_elements.button import Button
from battleship.view.gui_elements.user_element import UserElement


class MainMenu(UserElement):
    def __init__(self, rect: Rect, absolute_position: Tuple):
        super().__init__(rect, absolute_position)
        self.buttons = list()
        self.back_color = DEFAULT_DISPLAY_COLOR

        self.single_play_button = Button(
            LEFT_BUTTON_RECT,
            (absolute_position[0], absolute_position[1]),
            "Одиночная игра",
        )

        self.exit_button = Button(
            RIGHT_BUTTON_RECT,
            (absolute_position[0], absolute_position[1]),
            "Выход",
        )

        self.buttons.append(self.single_play_button)
        self.buttons.append(self.exit_button)

    def update(self, e: UserEvent, output_buffer: BufferToGameLogic):
        for button in self.buttons:
            button.update(e, output_buffer)
        output_buffer.is_single_play_button_pressed = (
            self.single_play_button.is_clicked
        )
        output_buffer.is_exit_button_pressed = self.exit_button.is_clicked

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
