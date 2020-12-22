from typing import Tuple

import pygame
from pygame.rect import Rect

from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.buffers.drawing_buffer import DrawingBuffer
from battleship.buffers.user_event import UserEvent
from battleship.enums import Cell
from battleship.view.draw_information import DrawInformation
from battleship.view.graphic_utils import (
    CELL_SIZE,
    DEAD_SHIP_PEACE,
    EMPTY,
    FULL_DEAD_PEACE,
    SHIP_PEACE,
    SHOT,
    WRONG_PEACE,
)
from battleship.view.gui_elements.user_element import UserElement


class GameFieldElement(UserElement):
    def __init__(self, rect, absolute_position):
        super().__init__(rect, absolute_position)

        self.cell_width = CELL_SIZE
        self.cell_height = CELL_SIZE

        self.map = None

        self.colors = dict()
        self.colors[Cell.DeadShipPeace] = DEAD_SHIP_PEACE
        self.colors[Cell.Shot] = SHOT
        self.colors[Cell.Empty] = EMPTY
        self.colors[Cell.WrongPeace] = WRONG_PEACE
        self.colors[Cell.ShipPeace] = SHIP_PEACE
        self.colors[Cell.FullDeadShip] = FULL_DEAD_PEACE

        self.padding = 1

    def update(self, e: UserEvent, output_buffer: BufferToGameLogic):
        output_buffer.shot_request = None
        output_buffer.place_request = None
        output_buffer.remove_request = None
        cell = (
            (e.absolute_mouse_location[0] -
             self.absolute_position[0]*2) // self.cell_width,
            (e.absolute_mouse_location[1] -
             self.absolute_position[1]*2) // self.cell_height,
        )
        output_buffer.pre_show_cell_index = cell
        if e.is_left_mouse_click and not e.was_left_mouse_click:
            output_buffer.shot_request = output_buffer.place_request = cell
        if e.is_right_mouse_click and not e.was_right_mouse_click:
            output_buffer.remove_request = cell
        if len(e.pressed_buttons) > 0 and len(e.non_released_buttons) > 0:
            output_buffer.rotate_request = (
                    e.pressed_buttons[pygame.K_SPACE] and
                    not e.non_released_buttons[pygame.K_SPACE]
            )
            output_buffer.random_field_request = (
                    e.pressed_buttons[pygame.K_r] and
                    not e.non_released_buttons[pygame.K_r]
            )

    def add_cells_to_buffer(self, cells, buffer_to_draw, new_transform):
        for cell in cells:
            buffer_to_draw.add(DrawInformation(
                transform=new_transform,
                draw_rect=Rect(
                    self.absolute_position[0] + cell[
                        0] * self.cell_width + self.padding,
                    self.absolute_position[1] + cell[
                        1] * self.cell_height + self.padding,
                    self.cell_width - self.padding * 2,
                    self.cell_height - self.padding * 2
                ),
                fill_color=self.colors[cell[2]]
            ))

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
            1, 1
        )

        if not bot_mode:
            self.add_cells_to_buffer(buffer_to_render.player_cells,
                                     buffer_to_draw, new_transform)
        else:
            self.colors[Cell.ShipPeace] = self.colors[Cell.Empty]
            self.add_cells_to_buffer(buffer_to_render.bot_cells,
                                     buffer_to_draw, new_transform)

        self.add_cells_to_buffer(buffer_to_render.pre_show_cell,
                                 buffer_to_draw, new_transform)
