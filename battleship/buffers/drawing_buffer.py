from battleship.buffers.buffer import Buffer


class DrawingBuffer(Buffer):
    def __init__(self):
        super().__init__()
        self.store = list()

    def update(self, other):
        if other.is_locked or self.is_locked:
            return

        self.lock()
        other.lock()
        self.store = other.store  # НЕ ПОТОКОБЕЗОПАСНО!!!

        self.unlock()
        other.unlock()

    def copy(self):
        while self.is_locked:
            pass

        other = DrawingBuffer()

        self.lock()
        other.store = self.store  # НЕ ПОТОКОБЕЗОПАСНО!!!

        self.unlock()

    def add(self, item):
        self.store.append(item)

    def __iter__(self):
        return self.store.__iter__()

    def __next__(self):
        for el in self.store:
            yield el
