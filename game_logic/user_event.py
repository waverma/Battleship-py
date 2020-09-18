from game_logic.point import Point


class UserEvent(object):
    def __init__(self):
        self.absolute_mouse_location = Point(0, 0)
        self.relatively_mouse_location = Point(0, 0)
        self.is_right_mouse_click = False
        self.is_left_mouse_click = False
        self.was_right_mouse_click = False
        self.was_left_mouse_click = False
        self.focus_element = None

        self.pressed_keys_list = list()

