from enum import Enum


class Cell(Enum):
    EMPTY = 0,
    SHIP_PEACE = 1,
    DEAD_SHIP_PEACE = 2,
    SHOT = 3
    POSSIBLE_SHIP_PLACE = 4
