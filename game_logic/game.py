from enum import Enum

import pygame

from game_logic.ai import AI
from game_logic.controls.button import Button
from game_logic.controls.field_control import FieldControl
from game_logic.controls.text_control import TextControl
from game_logic.map import Map, Cell, ShipType
from game_logic.user_event import UserEvent, Point
from game_logic.user_interface import UserInterface


class Game(object):

    cell_size = 35
    draw_buffer = list()
    user_interface = UserInterface()

    def __init__(self):
        self.state = GameState.PRE_GAME

        # добавление всех контролов
        self.player_field_control = FieldControl(self.cell_size, self.cell_size * 3, 10, 10, self.cell_size, self.cell_size)
        self.bot_field_control = FieldControl(self.cell_size * 16, self.cell_size * 3, 10, 10, self.cell_size, self.cell_size)
        self.player_field_text_control = TextControl(self.cell_size, self.cell_size * 2, self.cell_size * 10, self.cell_size)
        self.bot_field_text_control = TextControl(self.cell_size * 16, self.cell_size * 2, self.cell_size * 10, self.cell_size)
        self.start_button = Button(self.cell_size * 18, self.cell_size * 11, self.cell_size * 8, self.cell_size * 2)
        self.post_map = FieldControl(0, 0, 1, 1, 1000, 1000)
        self.labels = dict()

        # for pre game
        self.current_ship_type = ShipType.SINGLE_DECK

    def tune_controls(self):
        self.labels[ShipType.SINGLE_DECK] = (
            TextControl(self.cell_size * 18, self.cell_size * 2, self.cell_size * 6, self.cell_size),
            TextControl(self.cell_size * 25, self.cell_size * 2, self.cell_size, self.cell_size)
        )
        self.labels[ShipType.TWO_DECK] = (
            TextControl(self.cell_size * 18, self.cell_size * 4, self.cell_size * 6, self.cell_size),
            TextControl(self.cell_size * 25, self.cell_size * 4, self.cell_size, self.cell_size)
        )
        self.labels[ShipType.THREE_DECK] = (
            TextControl(self.cell_size * 18, self.cell_size * 6, self.cell_size * 6, self.cell_size),
            TextControl(self.cell_size * 25, self.cell_size * 6, self.cell_size, self.cell_size)
        )
        self.labels[ShipType.FOUR_DECK] = (
            TextControl(self.cell_size * 18, self.cell_size * 8, self.cell_size * 6, self.cell_size),
            TextControl(self.cell_size * 25, self.cell_size * 8, self.cell_size, self.cell_size)
        )
        self.labels[ShipType.SINGLE_DECK][0].text = "одна палуба"
        self.labels[ShipType.TWO_DECK][0].text = "две палубы"
        self.labels[ShipType.THREE_DECK][0].text = "три палубы"
        self.labels[ShipType.FOUR_DECK][0].text = "четыре палубы"

        # self.player_field_control.map = Map()
        self.player_field_control.game = self

        self.bot_field_control.colors[Cell.SHIP_PEACE] = (255, 255, 255)
        self.bot_field_control.colors[Cell.POSSIBLE_SHIP_PLACE] = (255, 255, 255)
        # self.bot_field_control.map = AI.generate_random_map()
        self.bot_field_control.game = self
        # self.bot_field_control.is_user_mode = False

        self.player_field_text_control.text = 'подготовка озера'
        self.bot_field_text_control.text = 'не мое озеро'

        self.start_button.text = "В БОЙ"
        self.start_button.commands.append(lambda: self.begin())

    def update_graphic(self):
        self.draw_buffer.clear()
        self.user_interface.clear_buffer()

        if self.state == GameState.PRE_GAME:
            self.user_interface.add_control(self.player_field_control)
            self.user_interface.add_control(self.start_button)

            self.draw_buffer.append(self.player_field_control)
            self.draw_buffer.append(self.player_field_text_control)
            for c in self.labels:
                self.draw_buffer.append(self.labels[c][0])
                self.draw_buffer.append(self.labels[c][1])
            self.draw_buffer.append(self.start_button)

        if self.state == GameState.GAME:
            self.user_interface.add_control(self.player_field_control)
            self.user_interface.add_control(self.bot_field_control)

            self.draw_buffer.append(self.player_field_control)
            self.draw_buffer.append(self.bot_field_control)
            self.draw_buffer.append(self.player_field_text_control)
            self.draw_buffer.append(self.bot_field_text_control)

        if self.state == GameState.POST_GAME:
            self.draw_buffer.append(self.post_map)

    def update(self, e: UserEvent) -> ():
        if e.focus_element is not None and e.is_left_mouse_click:
            e.focus_element.on_left_mouse(e)
        elif e.focus_element is not None and e.is_right_mouse_click:
            e.focus_element.on_right_mouse(e)

        self.labels[ShipType.SINGLE_DECK][1].text = self.player_field_control.map.ship_count_limit[ShipType.SINGLE_DECK]
        self.labels[ShipType.TWO_DECK][1].text = self.player_field_control.map.ship_count_limit[ShipType.TWO_DECK]
        self.labels[ShipType.THREE_DECK][1].text = self.player_field_control.map.ship_count_limit[ShipType.THREE_DECK]
        self.labels[ShipType.FOUR_DECK][1].text = self.player_field_control.map.ship_count_limit[ShipType.FOUR_DECK]

        if self.state == GameState.PRE_GAME:

            if not self.player_field_control.map.is_ship_building:
                self.labels[self.current_ship_type][0].back_color = (255, 0, 0)
                if e.pressed_keys_list[pygame.K_1]:
                    self.current_ship_type = ShipType.SINGLE_DECK
                if e.pressed_keys_list[pygame.K_2]:
                    self.current_ship_type = ShipType.TWO_DECK
                if e.pressed_keys_list[pygame.K_3]:
                    self.current_ship_type = ShipType.THREE_DECK
                if e.pressed_keys_list[pygame.K_4]:
                    self.current_ship_type = ShipType.FOUR_DECK
                self.labels[self.current_ship_type][0].back_color = (0, 255, 0)

        elif self.state == GameState.GAME:
            if self.is_completed()[0]:
                self.end(self.is_completed()[1])
                return

        elif self.state == GameState.POST_GAME:
            pass

    def prepare_to_begin(self):
        self.bot_field_control.map = AI.generate_random_map()
        self.bot_field_control.is_user_mode = False
        self.player_field_control = Map()
        self.state = GameState.PRE_GAME

    def end(self, is_player_win: bool):
        self.user_controls = []
        end_image = Map(1, 1)

        if not is_player_win:
            end_image.try_set_new_peace_of_ship(Point(0, 0), ShipType.SINGLE_DECK)
        end_image.strike(Point(0, 0))
        self.post_map.map = end_image
        self.user_controls.append(self.post_map)

        self.state = GameState.POST_GAME

    def is_completed(self) -> (bool, bool):
        result = False

        for cells in self.player_field_control.map.cells:
            for x in cells:
                result = result or x == Cell.SHIP_PEACE

        if not result:
            return True, False

        result = False
        for cells in self.bot_field_control.map.cells:
            for x in cells:
                result = result or x == Cell.SHIP_PEACE

        if not result:
            return True, True

        return False, False

    def begin(self):
        self.user_controls = []
        self.user_controls.append(self.player_field_control)
        self.user_controls.append(self.bot_field_control)

        self.player_field_control.map.is_battle_mode = True

        for x in range(self.player_field_control.map.width):
            for y in range(self.player_field_control.map.height):
                if self.player_field_control.map.cells[x][y] == Cell.POSSIBLE_SHIP_PLACE:
                    self.player_field_control.map.cells[x][y] = Cell.EMPTY
                if self.bot_field_control.map.cells[x][y] == Cell.POSSIBLE_SHIP_PLACE:
                    self.bot_field_control.map.cells[x][y] = Cell.EMPTY

        self.player_field_text_control.text = "мое озеро"
        for c in self.labels:
            self.labels[c][0].enable = False
            self.labels[c][1].enable = False
        self.start_button.enable = False

        self.state = GameState.GAME


class GameState(Enum):
    PRE_GAME = 0
    GAME = 1
    POST_GAME = 2
