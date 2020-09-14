class UserControl(object):
    def __init__(self, x: int, y: int, width: int, height: int):
        self.enable = False
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.game = None

    def on_left_mouse(self, e):
        pass

    def on_right_mouse(self, e):
        pass

    def draw(self, display):
        pass
