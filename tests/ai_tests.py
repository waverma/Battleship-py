import unittest

from game_logic.ai import AI
from game_logic.enums.cell import Cell
from game_logic.point import Point


class AITest(unittest.TestCase):
    @staticmethod
    def test_generate_random_map():
        for i in range(100):
            field = AI.generate_random_map()

            l = list()
            for j in range(4):
                l.append(0)

            points = list()
            for x in range(field.width):
                for y in range(field.height):
                    if field.cells[x][y] == Cell.SHIP_PEACE:
                        points.append(Point(x, y))

            assert len(points) == 20

            while len(points) != 0:
                snake = field.get_all_snake_incident_shp_cell(points[0].x, points[0].y, Cell.SHIP_PEACE)
                l[len(snake[0]) - 1] += 1
                for p in snake[0]:
                    points.remove(p)

            assert l[0] == 4
            assert l[1] == 3
            assert l[2] == 2
            assert l[3] == 1

    def test_generate_random_shot(self):
        pass


if __name__ == '__main__':
    unittest.main()
