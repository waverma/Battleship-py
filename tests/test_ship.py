from unittest import TestCase

from battleship.engine.ship import Ship


class TestShip(TestCase):
    def test_on_shot(self):
        ship = Ship(4)
        self.assertTrue(ship.on_shot((0, 0)))
        self.assertEqual(len(ship.affected_cells), 1)
        self.assertFalse(ship.on_shot((0, 0)))
        self.assertEqual(len(ship.affected_cells), 1)

    def test_has_die(self):
        ship = Ship(1)
        self.assertFalse(ship.has_die())
        ship.on_shot((0, 0))
        self.assertTrue(ship.has_die())

    def test_get_affected_cells(self):
        ship = Ship(4)
        self.assertTrue(ship.on_shot((0, 0)))
        self.assertEqual(len(ship.get_affected_cells()), 1)

    def test_get_occupied_cells(self):
        ship = Ship(4)
        self.placed_location = (0, 0)
        cells = ship.get_occupied_cells()
        self.assertEqual(len(cells), 4)
        self.assertEqual(cells[0], (0, 0))
        self.assertEqual(cells[3], (0, 3))

        cells = ship.get_occupied_cells((1, 1))
        self.assertEqual(len(cells), 4)
        self.assertEqual(cells[0], (1, 1))
        self.assertEqual(cells[3], (1, 4))

    def test_rotate(self):
        ship = Ship(4)
        self.placed_location = (0, 0)
        ship.rotate()
        cells = ship.get_occupied_cells()
        self.assertEqual(len(cells), 4)
        self.assertEqual(cells[0], (0, 0))
        self.assertEqual(cells[3], (3, 0))

    def test___contains__(self):
        ship = Ship(4)
        self.placed_location = (0, 0)
        self.assertTrue((0, 0) in ship)
        self.assertTrue((0, 1) in ship)
        self.assertTrue((0, 2) in ship)
        self.assertTrue((0, 3) in ship)
        self.assertFalse((0, 4) in ship)
