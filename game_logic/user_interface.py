from game_logic.point import Point
from game_logic.user_control import UserControl
from game_logic.user_event import UserEvent


class UserInterface(object):
    def __init__(self):
        self.buffer = list()

    def update(self, e: UserEvent):

        for control in self.buffer:
            if control.enable and \
                    control.x <= e.absolute_mouse_location.x <= control.width + control.x and \
                    control.y <= e.absolute_mouse_location.y <= control.height + control.y:

                e.focus_element = control
                e.relatively_mouse_location = Point(
                    e.absolute_mouse_location.x - control.x,
                    e.absolute_mouse_location.y - control.y
                )

    def add_control(self, control: UserControl):
        self.buffer.append(control)

    def clear_buffer(self):
        self.buffer = list()
