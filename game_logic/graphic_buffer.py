from game_logic.user_control import UserControl


class GraphicBuffer(object):
    def __init__(self):
        self.buffer = list()

    def add(self, control: UserControl):
        self.buffer.append(control)

    def clear(self):
        self.buffer = list()

    def __iter__(self):
        for obj in self.buffer:
            yield obj
