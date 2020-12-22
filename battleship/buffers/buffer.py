class Buffer:
    def __init__(self):
        self.is_locked = False

    def lock(self):
        self.is_locked = True

    def unlock(self):
        self.is_locked = False

    def update(self, other):
        pass

    def copy(self):
        pass

    def __iter__(self):
        pass

    def __next__(self):
        pass
