from typing import Tuple

from pygame.rect import Rect

from battleship.buffers.buffer_to_render import BufferToRender
from battleship.view.draw_information import DrawInformation
from battleship.view.graphic_utils import BLACK_COLOR, DEFAULT_TEXT_FILLCOLOR
from battleship.view.gui_elements.user_element import UserElement


class Text(UserElement):
    def __init__(
        self,
        rect: Rect,
        absolute_position: Tuple,
        text: str = "",
        fill_color: Tuple = DEFAULT_TEXT_FILLCOLOR
    ):
        super().__init__(rect, absolute_position)
        self.draw_info = DrawInformation(
            draw_rect=rect,
            fill_color=fill_color,
            outline_color=BLACK_COLOR,
            text_color=BLACK_COLOR,
            text=text,
            text_size=18
        )
        self.is_focused = False

    def set_text(self, text: str):
        self.draw_info.text = text

    def get_render_info(
        self, transform: Tuple, buffer_to_render: BufferToRender
    ):
        result = list()

        self.draw_info.transform = transform
        result.append(self.draw_info)

        return result
