import random

from game_logic.enums.cell import Cell
from game_logic.enums.ship_type import ShipType
from game_logic.map import Map
from game_logic.point import Point


class AI(object):
    @staticmethod
    def generate_random_map(field=None, w=10, h=10):
        if field is None:
            result_map = Map(w, h)
        else:
            result_map = field

        ships = list()
        ships.append((ShipType.FOUR_DECK, 4))
        ships.append((ShipType.THREE_DECK, 3))
        ships.append((ShipType.THREE_DECK, 3))
        ships.append((ShipType.TWO_DECK, 2))
        ships.append((ShipType.TWO_DECK, 2))
        ships.append((ShipType.TWO_DECK, 2))
        ships.append((ShipType.SINGLE_DECK, 1))
        ships.append((ShipType.SINGLE_DECK, 1))
        ships.append((ShipType.SINGLE_DECK, 1))
        ships.append((ShipType.SINGLE_DECK, 1))

        for x in range(result_map.width):
            for y in range(result_map.height):
                result_map.cells[x][y] = Cell.POSSIBLE_SHIP_PLACE

        ship_count = 0
        while ship_count != 20:
            ship_count = 0
            AI.set_ships(result_map, list(ships))
            for x in range(result_map.width):
                for y in range(result_map.height):
                    if result_map.cells[x][y] == Cell.SHIP_PEACE:
                        ship_count += 1

        for i in result_map.ship_count:
            result_map.ship_count[i] = 0

        return result_map

    @staticmethod
    def set_ships(field, ships):
        for i in range(1000):

            for x in range(field.width):
                for y in range(field.height):
                    field.cells[x][y] = Cell.POSSIBLE_SHIP_PLACE

            if AI.try_place_ships(field, ships):
                return True

        return False

    @staticmethod
    def try_place_ships(field, ships):
        for i in range(1000):
            if len(ships) == 0:
                return True
            ship = ships[random.randint(0, len(ships)) - 1]
            if AI.try_place_ship(field, ship[1], ship[0])[0]:
                ships.remove(ship)

        return len(ships) == 0

    @staticmethod
    def try_place_ship(field, peace_count, s_ship):
        possible_cells = AI.get_empty_cell(field)

        while len(possible_cells) != 0:
            point = possible_cells[random.randint(0, len(possible_cells)) - 1]
            possible_cells.remove(point)
            field.try_set_new_peace_of_ship(point, s_ship)
            if peace_count == 1:
                return True, point
            else:
                if AI.try_place_ship(field, peace_count - 1, s_ship):
                    return True, point
                else:
                    field.try_remove_peace_of_ship(point)

        return False, None

    @staticmethod
    def get_empty_cell(field):
        result = list()
        for x in range(field.width):
            for y in range(field.height):
                if field.cells[x][y] == Cell.POSSIBLE_SHIP_PLACE:
                    result.append(Point(x, y))

        return result

    @staticmethod
    def generate_random_shot(field):
        points = list()
        for x in range(field.width):
            for y in range(field.height):
                if field.cells[x][y] != Cell.SHOT and field.cells[x][y] != Cell.DEAD_SHIP_PEACE:
                    points.append(Point(x, y))

        field.try_strike(points[random.randint(0, len(points) - 1)])
