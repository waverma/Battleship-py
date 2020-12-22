from typing import Tuple

from battleship.engine.game_constants import (
    DEFAULT_FIELD_SIZE,
    FOUR_DECK_COUNT,
    SINGLE_DECK_COUNT,
    THREE_DECK_COUNT,
    TWO_DECK_COUNT,
)
from battleship.engine.ship import Ship
from battleship.enums import Cell


class Field:
    def __init__(self):
        self.width = DEFAULT_FIELD_SIZE[0]
        self.height = DEFAULT_FIELD_SIZE[1]
        self.ships = []
        self.ships_to_place = []
        self.shots = []

    def has_all_ships_die(self) -> bool:
        for ship in self.ships:
            if not ship.has_die():
                return False
        return True

    def reset(self):
        self.ships = []
        self.ships_to_place = []
        self.shots = []

        for _ in range(SINGLE_DECK_COUNT):
            self.ships_to_place.append(Ship(1))
        for _ in range(TWO_DECK_COUNT):
            self.ships_to_place.append(Ship(2))
        for _ in range(THREE_DECK_COUNT):
            self.ships_to_place.append(Ship(3))
        for _ in range(FOUR_DECK_COUNT):
            self.ships_to_place.append(Ship(4))

    def get_next(self) -> Ship:
        if len(self.ships_to_place) != 0:
            return self.ships_to_place[0]

    def get_cell_type(
            self, location: Tuple[int, int], battle_mode: bool
    ) -> Cell:

        ship = self.get_ship_on(location)
        if battle_mode:

            if ship is not None:
                if len(ship.occupied_cells) == len(ship.affected_cells):
                    return Cell.FullDeadShip
                if location in ship.get_affected_cells():
                    return Cell.DeadShipPeace
                return Cell.ShipPeace
            if location in self.shots:
                return Cell.Shot
            return Cell.Empty

        if ship is not None:
            return Cell.ShipPeace
        return Cell.Empty

    def can_place_ship_on(self, ship: Ship, location: Tuple[int, int]) -> bool:
        if ship is None:
            return False
        cells_to_check = ship.get_occupied_cells(location)

        for cell in cells_to_check:
            if not (0 <= cell[0] < self.height and 0 <= cell[1] < self.height):
                return False
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if self.get_ship_on(
                            (cell[0] + x, cell[1] + y)
                    ) is not None:
                        return False
        return True

    def try_place_new_ship(self, location: Tuple[int, int]) -> bool:
        if len(self.ships_to_place) == 0:
            return False
        ship = self.ships_to_place[0]
        if not self.can_place_ship_on(ship, location):
            return False

        self.ships_to_place.remove(ship)
        self.ships.append(ship)
        ship.placed_location = location
        return True

    def shot(self, location: Tuple[int, int]) -> Tuple[bool, bool]:
        if location in self.shots:
            return False, False
        self.shots.append(location)
        ship = self.get_ship_on(location)
        if ship is not None:
            return ship.on_shot(location), True
        return True, False

    def try_remove_ship(self, location: Tuple[int, int]) -> bool:
        ship_to_remove = self.get_ship_on(location)
        if ship_to_remove is None:
            return False
        self.ships.remove(ship_to_remove)
        self.ships_to_place.append(Ship(len(ship_to_remove.occupied_cells)))
        return True

    def get_ship_on(self, location: Tuple[int, int]) -> Ship:
        for ship in self.ships:
            if location in ship:
                return ship
