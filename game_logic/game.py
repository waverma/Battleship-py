from enum import Enum

from game_logic.ai import AI
from game_logic.controls.button import Button
from game_logic.controls.field_control import FieldControl
from game_logic.controls.text_control import TextControl
from game_logic.map import Map, Cell, ShipType
from game_logic.user_event import UserEvent, Point


class Game(object):

    cell_size = 35

    def __init__(self):
        self.state = GameState.PRE_GAME
        self.player_field = Map()
        self.bot_field = AI.generate_random_map()
        self.bot_field.is_battle_mode = True
        self.user_controls = []

        # добавление всех контролов
        self.player_field_control = FieldControl(self.cell_size, self.cell_size * 3, 10, 10, self.cell_size, self.cell_size)
        self.player_field_control.map = self.player_field
        self.player_field_control.game = self
        self.bot_field_control = FieldControl(self.cell_size * 16, self.cell_size * 3, 10, 10, self.cell_size, self.cell_size)
        self.bot_field_control.colors[Cell.SHIP_PEACE] = (255, 255, 255)
        self.bot_field_control.colors[Cell.POSSIBLE_SHIP_PLACE] = (255, 255, 255)
        self.bot_field_control.map = self.bot_field
        self.bot_field_control.game = self
        self.bot_field_control.is_user_mode = False

        self.player_field_text_control = TextControl(self.cell_size, self.cell_size * 2, self.cell_size * 10, self.cell_size)
        self.player_field_text_control.text = 'подготовка озера'
        self.bot_field_text_control = TextControl(self.cell_size * 16, self.cell_size * 2, self.cell_size * 10, self.cell_size)
        self.bot_field_text_control.text = 'не мое озеро'

        self.labels = dict()
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

        self.start_button = Button(self.cell_size * 18, self.cell_size * 11, self.cell_size * 8, self.cell_size * 2)
        self.start_button.text = "В БОЙ"
        self.start_button.commands.append(lambda: self.begin())
        self.user_controls.append(self.start_button)

        self.post_map = FieldControl(0, 0, 1, 1, 1000, 1000)

        self.user_controls.append(self.player_field_control)
        self.user_controls.append(self.bot_field_control)

        # for pre game
        self.current_ship_type = ShipType.SINGLE_DECK

        self.ship_count_limit = dict()
        self.ship_count = dict()
        self.ship_count[ShipType.FOUR_DECK] = 0
        self.ship_count[ShipType.THREE_DECK] = 0
        self.ship_count[ShipType.TWO_DECK] = 0
        self.ship_count[ShipType.SINGLE_DECK] = 0

        self.ship_count_limit[ShipType.FOUR_DECK] = 1
        self.ship_count_limit[ShipType.THREE_DECK] = 2
        self.ship_count_limit[ShipType.TWO_DECK] = 3
        self.ship_count_limit[ShipType.SINGLE_DECK] = 4

        self.labels[ShipType.SINGLE_DECK][0].text = "одна палуба"
        self.labels[ShipType.TWO_DECK][0].text = "две палубы"
        self.labels[ShipType.THREE_DECK][0].text = "три палубы"
        self.labels[ShipType.FOUR_DECK][0].text = "четыре палубы"

    def update(self, e: UserEvent) -> ():

        result = list()

        if e.focus_element is not None and e.is_left_mouse_click and not e.is_left_mouse_was_clicked_last_update:
            e.focus_element.on_left_mouse(e)
        elif e.focus_element is not None and e.is_right_mouse_click and not e.is_right_mouse_was_clicked_last_update:
            e.focus_element.on_right_mouse(e)

        self.labels[ShipType.SINGLE_DECK][1].text = str(self.ship_count_limit[ShipType.SINGLE_DECK] - self.ship_count[ShipType.SINGLE_DECK])
        self.labels[ShipType.TWO_DECK][1].text = str(self.ship_count_limit[ShipType.TWO_DECK] - self.ship_count[ShipType.TWO_DECK])
        self.labels[ShipType.THREE_DECK][1].text = str(self.ship_count_limit[ShipType.THREE_DECK] - self.ship_count[ShipType.THREE_DECK])
        self.labels[ShipType.FOUR_DECK][1].text = str(self.ship_count_limit[ShipType.FOUR_DECK] - self.ship_count[ShipType.FOUR_DECK])

        if self.state == GameState.PRE_GAME:

            if not self.player_field.is_ship_building:
                self.labels[self.current_ship_type][0].back_color = (255, 0, 0)
                if e.is_1_pressed and not e.was_1_pressed_last_update:
                    self.current_ship_type = ShipType.SINGLE_DECK
                if e.is_2_pressed and not e.was_2_pressed_last_update:
                    self.current_ship_type = ShipType.TWO_DECK
                if e.is_3_pressed and not e.was_3_pressed_last_update:
                    self.current_ship_type = ShipType.THREE_DECK
                if e.is_4_pressed and not e.was_4_pressed_last_update:
                    self.current_ship_type = ShipType.FOUR_DECK
                self.labels[self.current_ship_type][0].back_color = (0, 255, 0)

            self.bot_field_control.enable = False
            self.player_field_control.enable = True
            self.start_button.enable = True

            # if e.is_enter_pressed and not e.was_enter_pressed_last_update:
            #     self.begin()

            result.append(self.player_field_control)
            result.append(self.player_field_text_control)
            for c in self.labels:
                result.append(self.labels[c][0])
                result.append(self.labels[c][1])
            result.append(self.start_button)

            return result

        elif self.state == GameState.GAME:

            if self.is_completed()[0]:
                self.end(self.is_completed()[1])
                return

            self.bot_field_control.enable = True
            self.player_field_control.enable = True
            self.start_button.enable = False

            result.append(self.player_field_control)
            result.append(self.bot_field_control)
            result.append(self.player_field_text_control)
            result.append(self.bot_field_text_control)
            return result
        elif self.state == GameState.POST_GAME:
            result.append(self.post_map)
            self.bot_field_control.enable = False
            self.player_field_control.enable = False
            self.start_button.enable = False
            return result

    def prepare_to_begin(self):
        self.user_controls = []
        self.user_controls.append(self.player_field_control)

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

        for cells in self.player_field.cells:
            for x in cells:
                result = result or x == Cell.SHIP_PEACE

        if not result:
            return True, False

        result = False
        for cells in self.bot_field.cells:
            for x in cells:
                result = result or x == Cell.SHIP_PEACE

        if not result:
            return True, True

        return False, False

    def begin(self):
        self.user_controls = []
        self.user_controls.append(self.player_field_control)
        self.user_controls.append(self.bot_field_control)

        self.player_field.is_battle_mode = True

        for x in range(self.player_field.width):
            for y in range(self.player_field.height):
                if self.player_field.cells[x][y] == Cell.POSSIBLE_SHIP_PLACE:
                    self.player_field.cells[x][y] = Cell.EMPTY
                if self.bot_field.cells[x][y] == Cell.POSSIBLE_SHIP_PLACE:
                    self.bot_field.cells[x][y] = Cell.EMPTY

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
