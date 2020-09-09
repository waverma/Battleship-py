from enum import Enum


class Map(object):
    def __init__(self, width: int, height: int):
        self.width = width  # readonly
        self.height = height  # readonly

    def set_ship(self, ship):
        pass

    def get_ship_at(self, x: int, y: int):
        pass

    def try_strike(self, x: int, y: int) -> bool:
        pass


class Cell(object):
    def __init__(self):
        self.is_ship_peace = False
        self.is_shot = False


class Ship(object):
    def __init__(self):
        self.length = 0
        self.position = (0, 0)
        self.direction = DIRECTION.LEFT
        self.status = STATUS.PREPARE_TO_SET

    def rotate(self):
        pass


class DIRECTION(Enum):
    LEFT = 0
    RIGHT = 1


class STATUS(Enum):
    ON_MAP = 0
    PREPARE_TO_SET = 1
    DESTROYED = 2
