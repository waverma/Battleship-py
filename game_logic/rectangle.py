from game_logic.point import Point
from game_logic.size import Size


class Rectangle(object):
    def __init__(self, point: Point, size: Size):
        self.location = point
        self.size = size

    def contain(self, point: Point):
        return self.location.x <= point.x <= self.size.width + self.location.x \
               and self.location.y <= point.y <= self.size.height + self.location.y
