from typing import Tuple

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
)
from battleship.view.gui_elements.button import Button
from battleship.view.gui_elements.game_field_element import GameFieldElement
from battleship.view.gui_elements.text import Text
from battleship.view.gui_elements.user_element import UserElement


class GamePrepareMenu(UserElement):
    def __init__(self, rect: Rect, absolute_position: Tuple):
        super().__init__(rect, absolute_position)
        self.buttons = list()
        self.back_color = DEFAULT_DISPLAY_COLOR

        self.single_play_button = Button(
            Rect(CELL_SIZE * 20, CELL_SIZE * 11, CELL_SIZE * 5, CELL_SIZE * 2),
            (absolute_position[0], absolute_position[1]),
            "Начать",
        )

        self.exit_button = Button(
            Rect(CELL_SIZE * 14, CELL_SIZE * 11, CELL_SIZE * 5, CELL_SIZE * 2),
            (absolute_position[0], absolute_position[1]),
            "Назад",
        )

        self.my_field_text_marker = Text(
            LEFT_LABEL_RECT,
            (LEFT_LABEL_RECT.x, LEFT_LABEL_RECT.y),
            "МОЁ ОЗЕРО",
        )

        self.field_element = GameFieldElement(
            Rect(CELL_SIZE, CELL_SIZE,
                 CELL_SIZE*DEFAULT_FIELD_SIZE[0],
                 CELL_SIZE*DEFAULT_FIELD_SIZE[1]),
            (CELL_SIZE, CELL_SIZE)
        )

        self.buttons.append(self.single_play_button)
        self.buttons.append(self.exit_button)

    def update(self, e: UserEvent, output_buffer: BufferToGameLogic):
        self.field_element.update(e, output_buffer)

        for button in self.buttons:
            button.update(e, output_buffer)
        output_buffer.start = (
            self.single_play_button.is_clicked
        )
        output_buffer.is_to_main_menu_button_pressed = (
            self.exit_button.is_clicked
        )

    def get_render_info(
        self,
        transform: Tuple,
        buffer_to_render: BufferToRender,
        buffer_to_draw: DrawingBuffer = None,
        bot_mode: bool = None
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
        self.field_element.get_render_info(new_transform, buffer_to_render,
                                           buffer_to_draw, bot_mode)

        for text_render_info in self.my_field_text_marker.get_render_info(
                new_transform, buffer_to_render
        ):
            buffer_to_draw.add(text_render_info)

        for button in self.buttons:
            button_info = button.get_render_info(
                new_transform, buffer_to_render
            )
            for button_info_parts in button_info:
                buffer_to_draw.add(button_info_parts)

        return result
