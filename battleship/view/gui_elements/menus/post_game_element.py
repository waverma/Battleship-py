from typing import Tuple

from pygame.rect import Rect

from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.buffers.user_event import UserEvent
from battleship.view.draw_information import DrawInformation
from battleship.view.graphic_utils import (
    CELL_SIZE,
    DEFAULT_DISPLAY_COLOR,
    DEFAULT_TEXT_FILLCOLOR,
    GREEN_COLOR,
    LEFT_BUTTON_RECT,
    RED_COLOR,
    RIGHT_BUTTON_RECT,
)
from battleship.view.gui_elements.button import Button
from battleship.view.gui_elements.text import Text
from battleship.view.gui_elements.user_element import UserElement


class PostGameElement(UserElement):
    def __init__(self, rect: Rect, absolute_position: Tuple):
        super().__init__(rect, absolute_position)
        self.buttons = list()
        self.back_color = DEFAULT_DISPLAY_COLOR
        self.text = Text(
            Rect(CELL_SIZE * 6, CELL_SIZE * 5, CELL_SIZE * 15, CELL_SIZE),
            (CELL_SIZE * 11, CELL_SIZE * 5),
        )
        self.text.draw_info.text_size = 30

        self.restart_button = Button(
            LEFT_BUTTON_RECT,
            (absolute_position[0], absolute_position[1]),
            "Перезапустить",
        )

        self.exit_button = Button(
            RIGHT_BUTTON_RECT,
            (absolute_position[0], absolute_position[1]),
            "В главное меню",
        )

        self.vk_post_button = Button(
            Rect(CELL_SIZE*16, CELL_SIZE*10, CELL_SIZE*10, CELL_SIZE*2),
            (absolute_position[0], absolute_position[1]),
            "Рассказать", fill_color=RED_COLOR
        )

        self.buttons.append(self.restart_button)
        self.buttons.append(self.vk_post_button)
        self.buttons.append(self.exit_button)
        self.text_size = 10

    def update(self, e: UserEvent, output_buffer: BufferToGameLogic):
        for button in self.buttons:
            button.update(e, output_buffer)

        output_buffer.restart_request = self.restart_button.is_clicked
        output_buffer.is_to_main_menu_button_pressed = (
            self.exit_button.is_clicked
        )
        if self.vk_post_button.is_clicked:
            output_buffer.vk_post_request = self.vk_post_button.is_clicked

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

        if buffer_to_render.vk_access:
            self.vk_post_button.draw_info.fill_color = RED_COLOR
        else:
            if buffer_to_render.posted:
                self.vk_post_button.draw_info.fill_color = GREEN_COLOR
            else:
                self.vk_post_button.draw_info.fill_color = \
                    DEFAULT_TEXT_FILLCOLOR

        for button in self.buttons:
            button_info = button.get_render_info(
                new_transform, buffer_to_render
            )
            for button_info_parts in button_info:
                result.append(button_info_parts)

        if buffer_to_render.battle_result[1]:
            end_battle_message = "Победа!"
            self.text.draw_info.fill_color = GREEN_COLOR
        else:
            if buffer_to_render.is_time_up:
                end_battle_message = "Поражение! Время вышло!"
            else:
                end_battle_message = "Поражение! Все твои корабли потоплены"
            self.text.draw_info.fill_color = RED_COLOR

        self.text.draw_info.text = end_battle_message
        text_render_info = self.text.get_render_info(
            new_transform, buffer_to_render
        )
        for text_render_info_parts in text_render_info:
            result.append(text_render_info_parts)

        return result
