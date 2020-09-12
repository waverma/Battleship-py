from game_logic.point import Point
from game_logic.rectangle import Rectangle
from game_logic.size import Size


class UserControl(object):
    def __init__(self, x: int, y: int, width: int, height: int):
        self.enable = False
        self.wx = 0
        self.wy = 0

        self.collision = Rectangle(Point(x, y), Size(width, height))

    def draw(self, display):
        pass
