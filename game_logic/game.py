from enum import Enum

from game_logic.test_map import TestMap
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
        # self.bot_field_control
        # self.prepare_field_control

        self.user_controls.append(self.player_field_control)

    def update(self, e: UserEvent) -> ():
        result = list()

        if self.state == GameState.PRE_GAME:

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
            return None
        elif self.state == GameState.POST_GAME:
            return None

    def begin(self):
        pass


class GameState(Enum):
    PRE_GAME = 0
    GAME = 1
    POST_GAME = 2
