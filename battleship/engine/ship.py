from typing import Tuple


class Ship:
    def __init__(self, length: int):
        self.occupied_cells = [(0, i) for i in range(length)]
        self.placed_location = None
        self.affected_cells = set()

    def on_shot(self, location: Tuple[int, int]) -> bool:
        if location in self and location not in self.affected_cells:
            self.affected_cells.add(location)
            return True
        return False

    def has_die(self) -> bool:
        return len(self.occupied_cells) == len(self.affected_cells)

    def get_affected_cells(self) -> list:
        return list(self.affected_cells)

    def get_occupied_cells(self, location=None) -> list:
        current_occupied_cells = []
        current_location = (0, 0)
        if location is not None:
            current_location = location
        if self.placed_location is not None:
            current_location = self.placed_location

        for cell in self.occupied_cells:
            current_occupied_cells.append(
                (cell[0] + current_location[0],
                 cell[1] + current_location[1])
            )

        return current_occupied_cells

    def rotate(self):
        new_occupied_cells = []
        placed_location = (0, 0)

        if self.placed_location is not None:
            placed_location = self.placed_location
        for cell in self.occupied_cells:
            new_x = 0
            new_y = 0
            if cell[0] == placed_location[0]:
                new_y = placed_location[1]
                new_x = cell[0] + cell[1] - placed_location[1]
            elif cell[1] == placed_location[1]:
                new_x = placed_location[0]
                new_y = cell[1] + cell[0] - placed_location[0]
            new_occupied_cells.append((new_x, new_y))

        self.occupied_cells = new_occupied_cells

    def __contains__(self, point: Tuple[int, int]) -> bool:
        return point in self.get_occupied_cells()
