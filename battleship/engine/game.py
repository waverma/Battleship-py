from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.engine.ai import AI
from battleship.engine.field import Field
from battleship.enums import Cell, InterfaceStage


class Game:
    def __init__(self):
        self.player_field = Field()
        self.player_field.reset()
        self.bot_field = None
        self.stage = InterfaceStage.MainMenu

    def is_game_completed(self):
        if self.player_field is None or self.bot_field is None:
            return False, False
        is_player_die = self.player_field.has_all_ships_die()
        is_bot_die = self.bot_field.has_all_ships_die()

        return is_player_die or is_bot_die, not is_player_die

    def update(self, buffer: BufferToGameLogic, output_buffer: BufferToRender):
        output_buffer.pre_show_cell = []

        if buffer.interface_stage == InterfaceStage.InGame:
            if self.is_game_completed()[0]:
                self.stage = InterfaceStage.PostGame
            elif buffer.is_pause_request:
                self.stage = InterfaceStage.Pause
            elif buffer.shot_request is not None:
                player_shot_result = self.bot_field.shot(buffer.shot_request)
                if player_shot_result[0]:
                    if not player_shot_result[1]:
                        while AI.generate_random_shot(self.player_field):
                            pass

        elif buffer.interface_stage == InterfaceStage.PrepareToGame:
            if buffer.start and self.player_field.get_next() is None:
                self.bot_field = Field()
                AI.arrange_ships_automatically(self.bot_field)
                self.stage = InterfaceStage.InGame
            if buffer.place_request is not None:
                self.player_field.try_place_new_ship(buffer.place_request)
            if buffer.remove_request is not None:
                self.player_field.try_remove_ship(buffer.remove_request)
            if buffer.rotate_request and \
                    self.player_field.get_next() is not None:
                self.player_field.get_next().rotate()
            if buffer.is_to_main_menu_button_pressed:
                self.stage = InterfaceStage.MainMenu
            if buffer.random_field_request:
                self.player_field = Field()
                AI.arrange_ships_automatically(self.player_field)

        elif buffer.interface_stage == InterfaceStage.MainMenu:
            if buffer.is_single_play_button_pressed:
                self.stage = InterfaceStage.PrepareToGame
            self.player_field.reset()

        elif buffer.interface_stage == InterfaceStage.PostGame:
            if buffer.restart_request:
                self.stage = InterfaceStage.PrepareToGame
                self.player_field.reset()
            if buffer.is_to_main_menu_button_pressed:
                self.stage = InterfaceStage.MainMenu

        elif buffer.interface_stage == InterfaceStage.Pause:
            if buffer.is_to_main_menu_button_pressed:
                self.stage = InterfaceStage.MainMenu
            if buffer.is_return_button_pressed:
                self.stage = InterfaceStage.InGame

        output_buffer.game_stage = self.stage
        self.extract_to_render(buffer, output_buffer)

    def extract_to_render(
            self, buffer: BufferToGameLogic, output_buffer: BufferToRender
    ):
        output_buffer.player_cells = []
        output_buffer.bot_cells = []
        output_buffer.field_size = (
            self.player_field.width, self.player_field.height
        )

        output_buffer.battle_result = (
            self.is_game_completed()[0],
            self.is_game_completed()[1],
        )

        for x in range(self.player_field.width):
            for y in range(self.player_field.height):
                output_buffer.player_cells.append((
                    x,
                    y,
                    self.player_field.get_cell_type(
                        (x, y),
                        self.stage == InterfaceStage.InGame
                    )
                ))

        if self.bot_field is not None:
            for x in range(self.bot_field.width):
                for y in range(self.bot_field.height):
                    output_buffer.bot_cells.append(
                        (x, y, self.bot_field.get_cell_type((x, y), True))
                    )

        if self.has_pre_show_requires(buffer):
            if self.player_field.can_place_ship_on(
                    self.player_field.get_next(), buffer.pre_show_cell_index
            ):

                for cell_index in self.player_field.get_next().occupied_cells:
                    output_buffer.pre_show_cell.append(
                        (buffer.pre_show_cell_index[0] + cell_index[0],
                         buffer.pre_show_cell_index[1] + cell_index[1],
                         Cell.ShipPeace)
                    )
            else:
                for cell_index in self.player_field.get_next().occupied_cells:
                    output_buffer.pre_show_cell.append(
                        (buffer.pre_show_cell_index[0] + cell_index[0],
                         buffer.pre_show_cell_index[1] + cell_index[1],
                         Cell.DeadShipPeace)
                    )

    def has_pre_show_requires(self, buffer):
        return (
            buffer.pre_show_cell_index is not None and
            self.player_field.get_next() is not None and
            0 <= buffer.pre_show_cell_index[0] < self.player_field.width and
            0 <= buffer.pre_show_cell_index[1] < self.player_field.height
        )
