
from game_logic.enums.cell import Cell
from game_logic.enums.ship_type import ShipType
from game_logic.point import Point


class Map(object):
    def __init__(self, width=10, height=10):
        self.width = width
        self.height = height
        self.cells = []

        self.ship_count = dict()
        self.ship_count[ShipType.FOUR_DECK] = 1
        self.ship_count[ShipType.THREE_DECK] = 2
        self.ship_count[ShipType.TWO_DECK] = 3
        self.ship_count[ShipType.SINGLE_DECK] = 4

        self.is_battle_mode = False
        self.is_ship_building = False

        for x in range(width):
            self.cells.append([])
            for y in range(height):
                self.cells[x].append(Cell.POSSIBLE_SHIP_PLACE)

    def try_set_new_peace_of_ship(self, index: Point, s_type):
        if self.cells[index.x][index.y] == Cell.POSSIBLE_SHIP_PLACE:

            if s_type == ShipType.SINGLE_DECK:
                self.cells[index.x][index.y] = Cell.SHIP_PEACE
                self.redistribute_possible_ship_places(None, None)
                return True

            cur_int_ship_value = -1
            if s_type == ShipType.TWO_DECK:
                cur_int_ship_value = 2
            if s_type == ShipType.THREE_DECK:
                cur_int_ship_value = 3
            if s_type == ShipType.FOUR_DECK:
                cur_int_ship_value = 4

            self.cells[index.x][index.y] = Cell.DEAD_SHIP_PEACE
            ship_peaces = self.get_all_snake_incident_shp_cell(index.x, index.y, Cell.DEAD_SHIP_PEACE)
            if len(ship_peaces[0]) == cur_int_ship_value:
                for cell in ship_peaces[0]:
                    self.cells[cell.x][cell.y] = Cell.SHIP_PEACE
                self.redistribute_possible_ship_places(ship_peaces[1], ship_peaces[2])
                return True
            self.redistribute_possible_ship_places(ship_peaces[1], ship_peaces[2])

        return False

    def redistribute_possible_ship_places(self, start, end):
        self.is_ship_building = True
        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y] == Cell.POSSIBLE_SHIP_PLACE:
                    self.cells[x][y] = Cell.EMPTY

        incorrect_ship = list()

        for x in range(self.width):
            for y in range(self.height):
                if self.cells[x][y] == Cell.DEAD_SHIP_PEACE:
                    incorrect_ship.append(Point(x, y))

        if len(incorrect_ship) == 0:
            self.is_ship_building = False
            for x in range(self.width):
                for y in range(self.height):
                    if not self.is_diagonal_neighbour(x, y) and not self.is_not_diagonal_neighbour(x, y) and self.cells[x][y] != Cell.SHIP_PEACE:
                        self.set_possible_cell(x, y)
        if len(incorrect_ship) == 1:

            if not self.is_not_diagonal_neighbour(incorrect_ship[0].x + 1, incorrect_ship[0].y) and \
                    not self.is_diagonal_neighbour(incorrect_ship[0].x + 1, incorrect_ship[0].y):
                self.set_possible_cell(incorrect_ship[0].x + 1, incorrect_ship[0].y)
            if not self.is_not_diagonal_neighbour(incorrect_ship[0].x, incorrect_ship[0].y + 1) and \
                    not self.is_diagonal_neighbour(incorrect_ship[0].x, incorrect_ship[0].y + 1):
                self.set_possible_cell(incorrect_ship[0].x, incorrect_ship[0].y + 1)
            if not self.is_not_diagonal_neighbour(incorrect_ship[0].x - 1, incorrect_ship[0].y) and \
                    not self.is_diagonal_neighbour(incorrect_ship[0].x - 1, incorrect_ship[0].y):
                self.set_possible_cell(incorrect_ship[0].x - 1, incorrect_ship[0].y)
            if not self.is_not_diagonal_neighbour(incorrect_ship[0].x, incorrect_ship[0].y - 1) and \
                    not self.is_diagonal_neighbour(incorrect_ship[0].x, incorrect_ship[0].y - 1):
                self.set_possible_cell(incorrect_ship[0].x, incorrect_ship[0].y - 1)

        if len(incorrect_ship) == 2 or len(incorrect_ship) == 3:
            if not self.is_not_diagonal_neighbour(start.x, start.y) and not self.is_diagonal_neighbour(start.x, start.y):
                self.set_possible_cell(start.x, start.y)
            if not self.is_not_diagonal_neighbour(end.x, end.y) and not self.is_diagonal_neighbour(end.x, end.y):
                self.set_possible_cell(end.x, end.y)

    def set_possible_cell(self, x, y):
        if (y < 0) or (x < 0) or (y >= self.height) or (x >= self.width):
            return
        self.cells[x][y] = Cell.POSSIBLE_SHIP_PLACE

    def is_diagonal_neighbour(self, x, y):
        if (y < 0) or (x < 0) or (y >= self.height) or (x >= self.width):
            return
        return (x > 0 and y > 0 and self.cells[x-1][y-1] == Cell.SHIP_PEACE) or \
               (x > 0 and y < self.height - 1 and self.cells[x-1][y+1] == Cell.SHIP_PEACE) or \
               (x < self.width - 1 and y > 0 and self.cells[x+1][y-1] == Cell.SHIP_PEACE) or \
               (x < self.width - 1 and y < self.height - 1 and self.cells[x+1][y+1] == Cell.SHIP_PEACE)

    def is_not_diagonal_neighbour(self, x, y):
        if (y < 0) or (x < 0) or (y >= self.height) or (x >= self.width):
            return
        return (x > 0 and self.cells[x-1][y] == Cell.SHIP_PEACE) or \
               (y < self.height - 1 and self.cells[x][y+1] == Cell.SHIP_PEACE) or \
               (y > 0 and self.cells[x][y-1] == Cell.SHIP_PEACE) or \
               (x < self.width - 1 and self.cells[x+1][y] == Cell.SHIP_PEACE)

    def get_all_snake_incident_shp_cell(self, x, y, s_type) -> (list, Point, Point):
        start_cell_position = None
        go_direction = None
        result = (list(), None, None)
        result_list = list()

        if x > 0 and self.cells[x - 1][y] != Cell.EMPTY:
            start_cell_position = self.get_start_snake_position(Point(x, y), Point(-1, 0), s_type)
            go_direction = Point(1, 0)
            result = (result[0],
                      Point(start_cell_position.x - 1, start_cell_position.y),
                      Point(go_direction.x + 1, go_direction.y))
        if y > 0 and self.cells[x][y - 1] != Cell.EMPTY:
            start_cell_position = self.get_start_snake_position(Point(x, y), Point(0, -1), s_type)
            go_direction = Point(0, 1)
            result = (result[0],
                      Point(start_cell_position.x, start_cell_position.y - 1),
                      Point(go_direction.x, go_direction.y + 1))
        if x < self.width - 1 and self.cells[x + 1][y] != Cell.EMPTY:
            start_cell_position = self.get_start_snake_position(Point(x, y), Point(1, 0), s_type)
            go_direction = Point(-1, 0)
            result = (result[0],
                      Point(start_cell_position.x + 1, start_cell_position.y),
                      Point(go_direction.x - 1, go_direction.y))
        if y < self.height - 1 and self.cells[x][y + 1] != Cell.EMPTY:
            start_cell_position = self.get_start_snake_position(Point(x, y), Point(0, 1), s_type)
            go_direction = Point(0, -1)
            result = (result[0],
                      Point(start_cell_position.x, start_cell_position.y + 1),
                      Point(go_direction.x, go_direction.y - 1))

        if start_cell_position is None:
            result_list.append(Point(x, y))
            return result_list, None, None

        current_cell_position = start_cell_position
        last_valid_position = current_cell_position
        while 0 <= current_cell_position.x < self.width and \
                0 <= current_cell_position.y < self.height and \
                self.cells[current_cell_position.x][current_cell_position.y] == s_type:

            result_list.append(current_cell_position)
            current_cell_position = Point(current_cell_position.x + go_direction.x,
                                          current_cell_position.y + go_direction.y)
            last_valid_position = current_cell_position

        result = (result_list, result[1], last_valid_position)
        return result

    def get_start_snake_position(self, cur: Point, direction: Point, s_type) -> Point:
        current_cell_position = cur
        last_valid_point = cur
        while 0 <= current_cell_position.x < self.width and \
                0 <= current_cell_position.y < self.height and \
                self.cells[current_cell_position.x][current_cell_position.y] == s_type:

            last_valid_point = current_cell_position
            current_cell_position = Point(current_cell_position.x + direction.x,
                                          current_cell_position.y + direction.y)
        return last_valid_point

    def try_remove_peace_of_ship(self, index: Point):
        x = index.x
        y = index.y

        if self.cells[x][y] == Cell.SHIP_PEACE:
            a = self.get_all_snake_incident_shp_cell(x, y, Cell.SHIP_PEACE)
            ship_type = None
            for point in a[0]:
                self.cells[point.x][point.y] = Cell.EMPTY
                self.redistribute_possible_ship_places(None, None)
                if len(a[0]) == 1:
                    ship_type = ShipType.SINGLE_DECK
                if len(a[0]) == 2:
                    ship_type = ShipType.TWO_DECK
                if len(a[0]) == 3:
                    ship_type = ShipType.THREE_DECK
                if len(a[0]) == 4:
                    ship_type = ShipType.FOUR_DECK
            return True, ship_type

        if self.cells[x][y] == Cell.DEAD_SHIP_PEACE:
            count = 0
            if x < self.height - 1 and self.cells[x+1][y] == Cell.DEAD_SHIP_PEACE:
                count += 1
            if y < self.height - 1 and self.cells[x][y+1] == Cell.DEAD_SHIP_PEACE:
                count += 1
            if y > 0 and self.cells[x][y-1] == Cell.DEAD_SHIP_PEACE:
                count += 1
            if x > 0 and self.cells[x-1][y] == Cell.DEAD_SHIP_PEACE:
                count += 1
            if count < 2:
                self.cells[x][y] = Cell.EMPTY
                some_point = None
                if x > 0 and self.cells[x - 1][y] == Cell.DEAD_SHIP_PEACE:
                    some_point = Point(x - 1, y)
                if y > 0 and self.cells[x][y - 1] == Cell.DEAD_SHIP_PEACE:
                    some_point = Point(x, y - 1)
                if x < self.width - 1 and self.cells[x + 1][y] == Cell.DEAD_SHIP_PEACE:
                    some_point = Point(x + 1, y)
                if y < self.height - 1 and self.cells[x][y + 1] == Cell.DEAD_SHIP_PEACE:
                    some_point = Point(x, y + 1)

                a = None
                if some_point is not None:
                    a = self.get_all_snake_incident_shp_cell(some_point.x, some_point.y, Cell.DEAD_SHIP_PEACE)
                    self.redistribute_possible_ship_places(a[1], a[2])
                else:
                    self.redistribute_possible_ship_places(None, None)
        return False, None

    def strike(self, index: Point):
        x = index.x
        y = index.y

        if self.cells[x][y] == Cell.EMPTY:
            self.cells[x][y] = Cell.SHOT
        elif self.cells[x][y] == Cell.SHIP_PEACE:
            self.cells[x][y] = Cell.DEAD_SHIP_PEACE
