from unittest import TestCase

from battleship.engine.field import Field
from battleship.engine.ship import Ship
from battleship.enums import Cell


class TestField(TestCase):
    def test_has_all_ships_die(self):
        field = Field()
        field.ships.append(Ship(1))
        self.assertFalse(field.has_all_ships_die())
        field.ships[0].on_shot((0, 0))
        self.assertTrue(field.has_all_ships_die())

    def test_reset(self):
        field = Field()
        field.reset()
        self.assertEqual(len(field.ships), 0)
        self.assertEqual(len(field.shots), 0)
        self.assertEqual(len(field.ships_to_place), 10)

    def test_get_next(self):
        field = Field()
        field.reset()

        self.assertFalse(field.get_next() is None)
        field.ships_to_place = []
        self.assertTrue(field.get_next() is None)

    def test_get_cell_type(self):
        field = Field()
        point1 = (0, 0)

        point2 = (2, 0)
        ship = Ship(1)
        ship.placed_location = point2
        field.ships.append(ship)
        ship.on_shot(point2)

        point3 = (4, 0)
        ship = Ship(1)
        ship.placed_location = point3
        field.ships.append(ship)

        point4 = (6, 0)
        ship = Ship(2)
        ship.rotate()
        ship.placed_location = point4
        field.ships.append(ship)
        ship.on_shot(point4)

        point5 = (8, 0)
        field.shot(point5)

        self.assertEqual(field.get_cell_type(point1, True), Cell.Empty)
        self.assertEqual(field.get_cell_type(point2, True), Cell.FullDeadShip)
        self.assertEqual(field.get_cell_type(point3, True), Cell.ShipPeace)
        self.assertEqual(field.get_cell_type(point4, True), Cell.DeadShipPeace)
        self.assertEqual(field.get_cell_type(point5, True), Cell.Shot)
        self.assertEqual(field.get_cell_type(point5, False), Cell.Empty)
        self.assertEqual(field.get_cell_type(point2, False), Cell.ShipPeace)

    def test_can_place_ship_on(self):
        field = Field()
        field.reset()
        self.assertFalse(field.can_place_ship_on(None, (0, 0)))
        field.try_place_new_ship((0, 0))
        self.assertFalse(field.can_place_ship_on(Ship(1), (-1, 0)))
        self.assertFalse(field.can_place_ship_on(Ship(1), (0, 0)))
        self.assertFalse(field.can_place_ship_on(Ship(1), (1, 1)))
        self.assertTrue(field.can_place_ship_on(Ship(1), (1, 2)))

    def test_try_place_new_ship(self):
        field = Field()
        self.assertFalse(field.try_place_new_ship((0, 0)))
        field.reset()
        self.assertTrue(field.try_place_new_ship((0, 0)))
        self.assertFalse(field.try_place_new_ship((0, 0)))

    def test_shot(self):
        field = Field()
        field.reset()
        self.assertTrue(field.shot((0, 0))[0])
        self.assertFalse(field.shot((0, 0))[1])
        self.assertFalse(field.shot((0, 0))[0])
        self.assertFalse(field.shot((0, 0))[1])

        field.try_place_new_ship((4, 4))
        shot_result = field.shot((4, 4))
        self.assertTrue(shot_result[0])
        self.assertTrue(shot_result[1])

    def test_try_remove_ship(self):
        field = Field()
        field.reset()

        self.assertFalse(field.try_remove_ship((0, 0)))
        field.try_place_new_ship((0, 0))
        self.assertTrue(field.try_remove_ship((0, 0)))

    def test_get_ship_on(self):
        field = Field()
        field.reset()
        field.try_place_new_ship((0, 0))

        self.assertFalse(field.get_ship_on((0, 0)) is None)
        self.assertTrue(field.get_ship_on((2, 3)) is None)
