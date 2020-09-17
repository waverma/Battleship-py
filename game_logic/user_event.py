from game_logic.point import Point


class UserEvent(object):
    def __init__(self):
        self.absolute_mouse_location = Point(0, 0)
        self.relatively_mouse_location = Point(0, 0)
        self.is_right_mouse_click = False
        self.is_left_mouse_click = False
        self.focus_element = None

        # self.is_enter_pressed = False
        # self.is_1_pressed = False
        # self.is_2_pressed = False
        # self.is_3_pressed = False
        # self.is_4_pressed = False
        #
        # self.was_enter_pressed_last_update = False
        # self.was_1_pressed_last_update = False
        # self.was_2_pressed_last_update = False
        # self.was_3_pressed_last_update = False
        # self.was_4_pressed_last_update = False
        # self.is_right_mouse_was_clicked_last_update = False
        # self.is_left_mouse_was_clicked_last_update = False

        self.pressed_keys_list = list()
        self.pressed_keys = dict()  # <pygame_key_enum, was pressed on last update>

