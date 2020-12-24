from battleship.buffers.buffer import Buffer
from battleship.enums import InterfaceStage


class BufferToRender(Buffer):
    def __init__(self):
        super().__init__()
        self.game_stage = InterfaceStage.MainMenu

        self.session_timer = 0
        self.points = ""
        self.battle_result = ""
        self.field_size = (0, 0)
        self.player_cells = []
        self.bot_cells = []
        self.pre_show_cell = []
        self.is_time_up = False

    def update(self, other: "BufferToRender"):
        if other.is_locked or self.is_locked:
            return

        self.lock()
        other.lock()

        self.points = other.points
        self.game_stage = other.game_stage
        self.field_size = other.field_size
        self.battle_result = other.battle_result

        other.unlock()
        self.unlock()

    def copy(self):
        while self.is_locked:
            pass

        other = BufferToRender()
        self.lock()

        other.points = self.points
        other.game_stage = self.game_stage
        other.field_size = self.field_size
        other.battle_result = self.battle_result

        self.unlock()

        return other

    def __iter__(self):
        pass

    def __next__(self):
        pass
