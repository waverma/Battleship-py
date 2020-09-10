from enum import Enum
import random

from game_logic.test_map import TestMap, TestCell
from game_logic.user_control import FieldControl
from game_logic.user_event import UserEvent, Point


class Game(object):
    def __init__(self):
        self.state = GameState.PRE_GAME
        self.player_field = TestMap()
        self.bot_field = TestMap()
        self.user_controls = []

        # добавление всех контролов
        self.player_field_control = FieldControl(0, 0, 10, 10, 35, 35)
        self.player_field_control.map = self.player_field
        self.bot_field_control = FieldControl(400, 400, 10, 10, 35, 35)
        self.bot_field_control.map = self.bot_field
        self.bot_field_control.wx = 400
        self.bot_field_control.wy = 400
        self.bot_field_control.is_user_mode = False

        self.post_map = FieldControl(0, 0, 1, 1, 1000, 1000)

        self.user_controls.append(self.player_field_control)
        self.user_controls.append(self.bot_field_control)

    def update(self, e: UserEvent) -> ():
        result = list()

        if self.state == GameState.PRE_GAME:
            self.bot_field_control.enable = False
            self.player_field_control.enable = True

            if e.is_enter_pressed and not e.was_enter_pressed_last_update:
                self.begin()
                return

            if e.focus_element is self.player_field_control:
                cell_point = Point(
                    e.relatively_mouse_location.x // e.focus_element.cell_width,
                    e.relatively_mouse_location.y // e.focus_element.cell_height
                )
                if e.is_left_mouse_click and not e.is_left_mouse_was_clicked_last_update:
                    self.player_field.try_set_new_peace_of_ship(cell_point)
                elif e.is_right_mouse_click and not e.is_right_mouse_was_clicked_last_update:
                    self.player_field.try_remove_new_peace_of_ship(cell_point)

            result.append(self.player_field_control)
            return result

        elif self.state == GameState.GAME:

            if self.is_completed()[0]:
                self.end(self.is_completed()[1])
                return

            self.bot_field_control.enable = True
            self.player_field_control.enable = True

            if e.focus_element is self.bot_field_control:
                cell_point = Point(
                    e.relatively_mouse_location.x // e.focus_element.cell_width,
                    e.relatively_mouse_location.y // e.focus_element.cell_height
                )
                if e.is_left_mouse_click and not e.is_left_mouse_was_clicked_last_update:
                    self.bot_field.strike(cell_point)
                    self.player_field.strike(Point(
                        random.randint(0, self.player_field.width - 1),
                        random.randint(0, self.player_field.height - 1)
                    ))

            result.append(self.player_field_control)
            result.append(self.bot_field_control)
            return result
        elif self.state == GameState.POST_GAME:
            result.append(self.post_map)
            self.bot_field_control.enable = False
            self.player_field_control.enable = False
            return result

    def prepare_to_begin(self):
        self.user_controls = []
        self.user_controls.append(self.player_field_control)

        self.state = GameState.PRE_GAME

    def end(self, is_player_win: bool):
        self.user_controls = []
        end_image = TestMap(1, 1)

        if not is_player_win:
            end_image.try_set_new_peace_of_ship(Point(0, 0))
        end_image.strike(Point(0, 0))
        self.post_map.map = end_image
        self.user_controls.append(self.post_map)

        self.state = GameState.POST_GAME

    def is_completed(self) -> (bool, bool):
        result = False

        for cells in self.player_field.cells:
            for x in cells:
                result = result or x == TestCell.SHIP_PEACE

        if not result:
            return True, False

        result = False
        for cells in self.bot_field.cells:
            for x in cells:
                result = result or x == TestCell.SHIP_PEACE

        if not result:
            return True, True

        return False, False

    def begin(self):
        self.user_controls = []
        self.user_controls.append(self.player_field_control)
        self.user_controls.append(self.bot_field_control)

        self.bot_field = TestMap.get_random_map(self.player_field)
        self.bot_field_control.map = self.bot_field

        self.state = GameState.GAME


class GameState(Enum):
    PRE_GAME = 0
    GAME = 1
    POST_GAME = 2
