class Rectangle(object):
    def __init__(self, x: int, y: int, width: int, height: int):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def contain(self, x, y):
        return self.x <= x <= self.width + self.x and self.y <= y <= self.height + self.y
