from enum import Enum

from game_logic.user_event import Point


class TestMap(object):
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.cells = []
        self.ship_peace_count = 0
        self.ship_peace_count_limit = 20

        self.one_limit = 4
        self.two_limit = 3
        self.tree_limit = 2
        self.four_limit = 1
        self.one_current = 0
        self.two_current = 0
        self.tree_current = 0
        self.four_current = 0

        for x in range(width):
            self.cells.append([])
            for y in range(height):
                self.cells[x].append(TestCell.EMPTY)

    def try_set_new_peace_of_ship(self, index: Point) -> bool:
        x = index.x
        y = index.y

        if self.ship_peace_count == self.ship_peace_count_limit:
            return False
        if self.cells[x][y] == TestCell.EMPTY:
            self.cells[x][y] = TestCell.SHIP_PEACE
            self.ship_peace_count += 1
            return True
        return False

    def place_check(self, x: int, y: int) -> bool:
        pass

    def try_remove_new_peace_of_ship(self, index: Point) -> bool:
        x = index.x
        y = index.y

        if self.cells[x][y] == TestCell.SHIP_PEACE:
            self.cells[x][y] = TestCell.EMPTY
            self.ship_peace_count -= 1
            return True
        return False

    def strike(self, index: Point):
        x = index.x
        y = index.y

        if self.cells[x][y] == TestCell.EMPTY:
            self.cells[x][y] = TestCell.SHOT
        elif self.cells[x][y] == TestCell.SHIP_PEACE:
            self.cells[x][y] = TestCell.DEAD_SHIP_PEACE
            self.ship_peace_count -= 1

    @staticmethod
    def get_random_map(map=None):
        result = TestMap()
        for x in range(map.width):
            for y in range(map.height):
                if map.cells[x][y] == TestCell.SHIP_PEACE:
                    result.try_set_new_peace_of_ship(Point(x, y))

        return result


class TestCell(Enum):
    EMPTY = 0,
    SHIP_PEACE = 1,
    DEAD_SHIP_PEACE = 2,
    SHOT = 3
