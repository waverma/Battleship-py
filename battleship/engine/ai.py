import random

from battleship.engine.field import Field


class AI:
    @staticmethod
    def generate_random_shot(field: Field):
        for i in range(1000):
            point = (random.randint(0, field.width - 1),
                     random.randint(0, field.height - 1))
            if point in field.shots:
                continue
            shot = field.shot(point)
            return shot[1]

        for x in range(field.width):
            for y in range(field.height):
                if (x, y) in field.shots:
                    continue
                shot = field.shot((x, y))
                return shot[1]

        return False

    @staticmethod
    def arrange_ships_automatically(field: Field = None) -> bool:
        for i in range(1000):
            field.reset()
            if AI.try_arrange_ships(field, 1000):
                return True
        return False

    @staticmethod
    def try_arrange_ships(field: Field, step_count: int):
        for i in range(step_count):
            ship = field.get_next()
            if ship is None:
                break
            if random.randint(0, 2) == 1:
                field.get_next().rotate()

            field.try_place_new_ship((random.randint(0, field.width),
                                      random.randint(0, field.height)))

        return field.get_next() is None
