from enum import Enum

from game_logic.user_event import Point


class TestMap(object):
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.cells = []
        self.ship_peace_count = 0
        self.ship_peace_count_limit = 20

        self.ship_count_limit = dict()
        self.ship_count = dict()
        self.ship_count[ShipType.FOUR_DECK] = 0
        self.ship_count[ShipType.THREE_DECK] = 0
        self.ship_count[ShipType.TWO_DECK] = 0
        self.ship_count[ShipType.SINGLE_DECK] = 0

        self.ship_count_limit[ShipType.FOUR_DECK] = 1
        self.ship_count_limit[ShipType.THREE_DECK] = 2
        self.ship_count_limit[ShipType.TWO_DECK] = 3
        self.ship_count_limit[ShipType.SINGLE_DECK] = 4

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

            ship_type = self.get_new_ship_type(x, y)
            if ship_type == ShipType.INCORRECT_SHIP:
                return False
            if self.ship_count[ship_type] == self.ship_count_limit[ship_type]:
                return False
            self.ship_count[ship_type] += 1
            if ship_type == ShipType.TWO_DECK:
                self.ship_count[ShipType.SINGLE_DECK] -= 1
            if ship_type == ShipType.THREE_DECK:
                self.ship_count[ShipType.TWO_DECK] -= 1
            if ship_type == ShipType.FOUR_DECK:
                self.ship_count[ShipType.THREE_DECK] -= 1

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

    def get_new_ship_type(self, x, y):
        # check to diagonal
        if (x > 0 and y > 0 and self.cells[x-1][y-1] == TestCell.SHIP_PEACE) or \
                (x > 0 and y < self.height - 1 and self.cells[x-1][y+1] == TestCell.SHIP_PEACE) or \
                (x < self.width - 1 and y > 0 and self.cells[x+1][y-1] == TestCell.SHIP_PEACE) or \
                (x < self.width and y < self.height and self.cells[x+1][y+1] == TestCell.SHIP_PEACE):
            return ShipType.INCORRECT_SHIP

        # check to single-deck
        if (x > 0 and self.cells[x - 1][y] == TestCell.EMPTY) and \
                (y > 0 and self.cells[x][y - 1] == TestCell.EMPTY) and \
                (x < self.width - 1 and self.cells[x + 1][y] == TestCell.EMPTY) and \
                (y < self.height - 1 and self.cells[x][y + 1] == TestCell.EMPTY):
            return ShipType.SINGLE_DECK

        # check to horizontal
        current_ship_peace_count = 1
        if (x > 0 and self.cells[x - 1][y] != TestCell.EMPTY) or \
                (x < self.width - 1 and self.cells[x + 1][y] != TestCell.EMPTY):
            cx = x-1
            while cx > 0:
                if self.cells[cx][y] == TestCell.SHIP_PEACE:
                    current_ship_peace_count += 1
                else:
                    break
                cx -= 1

            cx = x+1
            while cx > 0:
                if self.cells[cx][y] == TestCell.SHIP_PEACE:
                    current_ship_peace_count += 1
                else:
                    break
                cx += 1

            if current_ship_peace_count == 2:
                return ShipType.TWO_DECK
            if current_ship_peace_count == 3:
                return ShipType.THREE_DECK
            if current_ship_peace_count == 4:
                return ShipType.FOUR_DECK
            if current_ship_peace_count > 4:
                return ShipType.INCORRECT_SHIP

        # check to vertical
        if (y > 0 and self.cells[x][y-1] != TestCell.EMPTY) or \
                (y < self.height - 1 and self.cells[x][y+1] != TestCell.EMPTY):
            cy = y - 1
            while cy > 0:
                if self.cells[x][cy] == TestCell.SHIP_PEACE:
                    current_ship_peace_count += 1
                else:
                    break
                cy -= 1

            cy = y + 1
            while cy > 0:
                if self.cells[x][cy] == TestCell.SHIP_PEACE:
                    current_ship_peace_count += 1
                else:
                    break
                cy += 1

            if current_ship_peace_count == 2:
                return ShipType.TWO_DECK
            if current_ship_peace_count == 3:
                return ShipType.THREE_DECK
            if current_ship_peace_count == 4:
                return ShipType.FOUR_DECK
            if current_ship_peace_count > 4:
                return ShipType.INCORRECT_SHIP

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


class ShipType(Enum):
    INCORRECT_SHIP = 0
    SINGLE_DECK = 1
    TWO_DECK = 2
    THREE_DECK = 3
    FOUR_DECK = 4
