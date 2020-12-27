from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.engine.field import Field
from battleship.engine.game_constants import (
    GAME_SESSION_LENGTH,
    LOSE_TEXT_FOR_VK_POST,
    WIN_TEXT_FOR_VK_POST_PREFIX,
    WIN_TEXT_FOR_VK_POST_SUFFIX,
)
from battleship.enums import Cell, InterfaceStage
from battleship.vk_provider import VkProvider


def get_cool_down(tick_count, tick_pointer) -> int:
    return round(((tick_count * (1000 / 60)) / 1000) -
                 ((tick_pointer * (1000 / 60)) / 1000))


class Game:
    def __init__(self):
        self.player_field = Field()
        self.player_field.reset()
        self.bot_field = None
        self.current_session_tick = 0
        self.stage = InterfaceStage.MainMenu

        self.has_posted = False
        self.vk_p = VkProvider()
        self.current_url = ''

    def is_game_completed(self):
        if self.current_session_tick >= GAME_SESSION_LENGTH:
            return True, False

        if self.player_field is None or self.bot_field is None:
            return False, False
        is_player_die = self.player_field.has_all_ships_die()
        is_bot_die = self.bot_field.has_all_ships_die()

        return is_player_die or is_bot_die, not is_player_die

    def update(self, buffer: BufferToGameLogic, output_buffer: BufferToRender):
        output_buffer.pre_show_cell = []

        if buffer.interface_stage == InterfaceStage.InGame:
            self.current_session_tick += 1
            if self.is_game_completed()[0]:
                self.stage = InterfaceStage.PostGame
            elif buffer.is_pause_request:
                self.stage = InterfaceStage.Pause
            elif buffer.shot_request is not None:
                player_shot_result = self.bot_field.shot(buffer.shot_request)
                if player_shot_result[0]:
                    if not player_shot_result[1]:
                        while self.player_field.make_random_shot():
                            pass

        elif buffer.interface_stage == InterfaceStage.PrepareToGame:
            if buffer.start and \
                    self.player_field.get_next_ship_to_place() is None:
                self.has_posted = False
                self.bot_field = Field(Field.get_arrange_ships())
                self.stage = InterfaceStage.InGame
                self.current_session_tick = 0
            if buffer.place_request is not None:
                self.player_field.try_place_new_ship(buffer.place_request)
            if buffer.remove_request is not None:
                self.player_field.try_remove_ship(buffer.remove_request)
            if buffer.rotate_request and \
                    self.player_field.get_next_ship_to_place() is not None:
                self.player_field.get_next_ship_to_place().rotate()
            if buffer.is_to_main_menu_button_pressed:
                self.stage = InterfaceStage.MainMenu
            if buffer.random_field_request:
                self.player_field = Field(Field.get_arrange_ships())

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
            if not self.has_posted and buffer.vk_post_request:
                if self.vk_p.send_post_with(self.get_vk_text()):
                    self.has_posted = True
                else:
                    self.stage = InterfaceStage.VkAuthorization

        elif buffer.interface_stage == InterfaceStage.VkAuthorization:
            if buffer.url != "":
                self.current_url = buffer.url
            if buffer.to_browser_request:
                self.vk_p.try_get_access()
            if buffer.is_return_button_pressed:
                self.stage = InterfaceStage.PostGame
            if buffer.apply:
                VkProvider.save_user_id_and_access_token_by(self.current_url)
                self.vk_p = VkProvider()
                if self.vk_p.send_post_with(self.get_vk_text()):
                    self.has_posted = True
                self.stage = InterfaceStage.PostGame

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
        output_buffer.url = self.current_url
        output_buffer.posted = self.has_posted
        output_buffer.player_cells = []
        output_buffer.bot_cells = []
        output_buffer.field_size = (
            self.player_field.width, self.player_field.height
        )

        output_buffer.session_timer = get_cool_down(
            GAME_SESSION_LENGTH, self.current_session_tick
        )

        output_buffer.battle_result = (
            self.is_game_completed()[0],
            self.is_game_completed()[1],
        )
        output_buffer.is_time_up = \
            self.current_session_tick >= GAME_SESSION_LENGTH

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
                    self.player_field.get_next_ship_to_place(),
                    buffer.pre_show_cell_index
            ):

                for cell_index in self.player_field.get_next_ship_to_place()\
                        .occupied_cells:
                    output_buffer.pre_show_cell.append(
                        (buffer.pre_show_cell_index[0] + cell_index[0],
                         buffer.pre_show_cell_index[1] + cell_index[1],
                         Cell.ShipPeace)
                    )
            else:
                for cell_index in self.player_field.get_next_ship_to_place()\
                        .occupied_cells:
                    output_buffer.pre_show_cell.append(
                        (buffer.pre_show_cell_index[0] + cell_index[0],
                         buffer.pre_show_cell_index[1] + cell_index[1],
                         Cell.DeadShipPeace)
                    )

    def has_pre_show_requires(self, buffer):
        return (
                buffer.pre_show_cell_index is not None and
                self.player_field.get_next_ship_to_place() is not None and
                0 <= buffer.pre_show_cell_index[0] <
                self.player_field.width and
                0 <= buffer.pre_show_cell_index[1] < self.player_field.height
        )

    def get_vk_text(self):
        if self.is_game_completed()[1]:
            return (WIN_TEXT_FOR_VK_POST_PREFIX +
                    str(get_cool_down(
                        GAME_SESSION_LENGTH,
                        GAME_SESSION_LENGTH - self.current_session_tick)) +
                    WIN_TEXT_FOR_VK_POST_SUFFIX)
        return LOSE_TEXT_FOR_VK_POST
