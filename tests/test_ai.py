from unittest import TestCase

from battleship.engine.ai import AI
from battleship.engine.field import Field


class TestAI(TestCase):
    def test_generate_random_shot(self):
        for i in range(10000):
            field = Field()
            AI.generate_random_shot(field)
            self.assertEqual(len(field.shots), 1)
            AI.generate_random_shot(field)
            self.assertEqual(len(field.shots), 2)

    def test_arrange_ships_automatically(self):
        for i in range(10):
            field = Field()
            AI.arrange_ships_automatically(field)
            self.assertEqual(len(field.ships), 10)
