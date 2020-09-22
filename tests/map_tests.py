import unittest

from game_logic.enums.cell import Cell
from game_logic.enums.ship_type import ShipType
from game_logic.map import Map
from game_logic.point import Point


class MapTest(unittest.TestCase):
    def setUp(self):
        self.field = Map()

    def test_try_set_new_single_deck(self):
        assert self.field.try_set_new_peace_of_ship(Point(0, 0), ShipType.SINGLE_DECK) and \
            len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 1

        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 3
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 96

        assert not self.field.try_set_new_peace_of_ship(Point(1, 0), ShipType.SINGLE_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 1
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 3
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 96

        assert not self.field.try_set_new_peace_of_ship(Point(1, 1), ShipType.SINGLE_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 1
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 3
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 96

        assert not self.field.try_set_new_peace_of_ship(Point(0, 0), ShipType.SINGLE_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 1
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 3
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 96

        assert not self.field.try_set_new_peace_of_ship(Point(0, 1), ShipType.SINGLE_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 1
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 3
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 96

        assert self.field.try_set_new_peace_of_ship(Point(9, 9), ShipType.SINGLE_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 2
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 6
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 92

    def test_try_set_new_two_deck(self):
        assert not self.field.try_set_new_peace_of_ship(Point(0, 0), ShipType.TWO_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 1
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 97
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 2

        assert not self.field.try_set_new_peace_of_ship(Point(1, 1), ShipType.TWO_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 1
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 97
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 2

        assert self.field.try_set_new_peace_of_ship(Point(1, 0), ShipType.TWO_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 2
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 4
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 94

    def test_try_set_new_three_deck(self):
        assert not self.field.try_set_new_peace_of_ship(Point(3, 3), ShipType.THREE_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 1
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 95
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 4

        assert not self.field.try_set_new_peace_of_ship(Point(3, 4), ShipType.THREE_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 2
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 96
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 2

        assert self.field.try_set_new_peace_of_ship(Point(3, 5), ShipType.THREE_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 3
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 12
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 85

    def test_try_set_new_four_deck(self):
        assert not self.field.try_set_new_peace_of_ship(Point(3, 3), ShipType.FOUR_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 1
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 95
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 4

        assert not self.field.try_set_new_peace_of_ship(Point(3, 4), ShipType.FOUR_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 2
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 96
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 2

        assert not self.field.try_set_new_peace_of_ship(Point(3, 2), ShipType.FOUR_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 3
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 95
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 2

        assert self.field.try_set_new_peace_of_ship(Point(3, 5), ShipType.FOUR_DECK)
        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 4
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 14
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 82

    def test_try_remove_peace_of_ship(self):
        self.field.try_set_new_peace_of_ship(Point(0, 0), ShipType.FOUR_DECK)
        self.field.try_set_new_peace_of_ship(Point(1, 0), ShipType.FOUR_DECK)
        self.field.try_set_new_peace_of_ship(Point(2, 0), ShipType.FOUR_DECK)

        self.field.try_remove_peace_of_ship(Point(1, 0))

        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 3
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 96
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 1

        self.field.try_remove_peace_of_ship(Point(0, 0))

        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 2
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 96
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 2

        self.field.try_remove_peace_of_ship(Point(1, 0))

        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 1
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 96
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 3

        self.field.try_remove_peace_of_ship(Point(2, 0))

        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.DEAD_SHIP_PEACE)) == 0
        assert len(get_all_cell_of(self.field, Cell.EMPTY)) == 0
        assert len(get_all_cell_of(self.field, Cell.POSSIBLE_SHIP_PLACE)) == 100

    def test_try_remove_ship(self):
        self.field.try_set_new_peace_of_ship(Point(0, 0), ShipType.SINGLE_DECK)

        self.field.try_set_new_peace_of_ship(Point(5, 5), ShipType.TWO_DECK)
        self.field.try_set_new_peace_of_ship(Point(6, 5), ShipType.TWO_DECK)

        self.field.try_set_new_peace_of_ship(Point(2, 2), ShipType.THREE_DECK)
        self.field.try_set_new_peace_of_ship(Point(2, 3), ShipType.THREE_DECK)
        self.field.try_set_new_peace_of_ship(Point(2, 4), ShipType.THREE_DECK)

        self.field.try_set_new_peace_of_ship(Point(9, 9), ShipType.FOUR_DECK)
        self.field.try_set_new_peace_of_ship(Point(9, 8), ShipType.FOUR_DECK)
        self.field.try_set_new_peace_of_ship(Point(9, 7), ShipType.FOUR_DECK)
        self.field.try_set_new_peace_of_ship(Point(9, 6), ShipType.FOUR_DECK)

        self.field.try_remove_peace_of_ship(Point(0, 0))

        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 9

        self.field.try_remove_peace_of_ship(Point(5, 5))

        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 7

        self.field.try_remove_peace_of_ship(Point(2, 2))

        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 4

        self.field.try_remove_peace_of_ship(Point(9, 9))

        assert len(get_all_cell_of(self.field, Cell.SHIP_PEACE)) == 0


def assert_two_map(first_map: Map, second_map: Map) -> bool:
    if first_map.width != second_map.width or first_map.height != second_map.height:
        return False

    for x in range(first_map.width):
        for y in range(first_map.height):
            if first_map.cells[x][y] == second_map.cells[x][y]:
                return False

    return True


def get_all_cell_of(field: Map, cell_type) -> list:
    result = list()

    for x in range(field.width):
        for y in range(field.height):
            if field.cells[x][y] == cell_type:
                result.append((x, y))

    return result


def get_message(parameter: str, mb: str, bw: str) -> str:
    return parameter + 'must be: ' + mb + 'but was: ' + bw


if __name__ == '__main__':
    unittest.main()
