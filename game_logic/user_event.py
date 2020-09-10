class UserEvent(object):
    def __init__(self):
        self.relatively_mouse_location = Point(0, 0)
        self.is_right_mouse_click = False
        self.is_left_mouse_click = False
        self.focus_element = None

        self.is_enter_pressed = False

        self.was_enter_pressed_last_update = False
        self.is_right_mouse_was_clicked_last_update = False
        self.is_left_mouse_was_clicked_last_update = False


class Point(object):
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y


class Size(object):
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height


class Rectangle(object):
    def __init__(self, point: Point, size: Size):
        self.location = point
        self.size = size

    def contain(self, point: Point):
        return self.location.x <= point.x <= self.size.width + self.location.x \
               and self.location.y <= point.y <= self.size.height + self.location.y
