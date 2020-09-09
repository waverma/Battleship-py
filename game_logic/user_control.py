from game_logic.user_event import Rectangle, Point, Size


class UserControl(object):
    def __init__(self, x: int, y: int, width: int, height: int):
        self.enable = False

        self.collision = Rectangle(Point(x, y), Size(width, height))

    def on_left_click(self):
        pass

    def on_right_click(self):
        pass

    def get_draw_set(self) -> list:
        pass


class FieldControl(UserControl):
    def __init__(self, x: int, y: int, width: int, height: int, cell_width: int, cell_height: int):
        super().__init__(x, y, width*cell_width, height*cell_height)

        self.cell_width = cell_width
        self.cell_height = cell_height

        self.map = None

    def get_draw_set(self) -> list:
        super(FieldControl, self).get_draw_set()
        if map is None:
            return None

        result = []
        result

