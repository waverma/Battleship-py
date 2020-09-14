import random

from game_logic.enums.cell import Cell
from game_logic.enums.ship_type import ShipType
from game_logic.map import Map
from game_logic.point import Point


class AI(object):
    @staticmethod
    def generate_random_map(m=None, w=10, h=10):
        if m is None:
            result_map = Map(w, h)
        else:
            result_map = m

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

        c = 0
        while c != 20:
            c = 0
            AI.set_ships(result_map, list(ships))
            for x in range(result_map.width):
                for y in range(result_map.height):
                    if result_map.cells[x][y] == Cell.SHIP_PEACE:
                        c += 1

        return result_map

    @staticmethod
    def set_ships(map, ships):
        for i in range(1000):

            for x in range(map.width):
                for y in range(map.height):
                    map.cells[x][y] = Cell.POSSIBLE_SHIP_PLACE

            if AI.try_place_ships(map, ships):
                return True

        return False

    @staticmethod
    def try_place_ships(map, ships):
        for i in range(1000):
            if len(ships) == 0:
                return True
            ship = ships[random.randint(0, len(ships)) - 1]
            if AI.try_place_ship(map, ship[1], ship[0])[0]:
                ships.remove(ship)

        return len(ships) == 0

    @staticmethod
    def try_place_ship(map, peace_count, s_ship, p=None):
        c = AI.get_empty_cell(map)

        while len(c) != 0:
            point = c[random.randint(0, len(c)) - 1]
            if p is not None:
                point = p
            c.remove(point)
            map.try_set_new_peace_of_ship(point, s_ship)
            if peace_count == 1:
                return True, point
            else:
                if AI.try_place_ship(map, peace_count - 1, s_ship):
                    return True, point
                else:
                    map.try_remove_new_peace_of_ship(point)

        return False, None

    @staticmethod
    def get_empty_cell(map):
        res = list()
        for x in range(map.width):
            for y in range(map.height):
                if map.cells[x][y] == Cell.POSSIBLE_SHIP_PLACE:
                    res.append(Point(x, y))

        return res

    @staticmethod
    def generate_random_shot(map):
        points = list()
        for x in range(map.width):
            for y in range(map.height):
                if map.cells[x][y] != Cell.SHOT and map.cells[x][y] != Cell.DEAD_SHIP_PEACE:
                    points.append(Point(x, y))

        map.strike(points[random.randint(0, len(points) - 1)])


