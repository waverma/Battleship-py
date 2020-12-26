from battleship.buffers.buffer import Buffer


class BufferToGameLogic(Buffer):
    def __init__(self):
        super().__init__()
        self.interface_stage = None

        self.is_cancel_button_pressed = False
        # MainMenu
        self.is_single_play_button_pressed = False
        self.is_exit_button_pressed = False

        # Одиночная игра
        self.is_new_game_button_pressed = False

        # InGame
        self.shot_request = None
        self.is_pause_request = False

        # GamePreparing
        self.place_request = None
        self.remove_request = None
        self.pre_show_cell_index = None
        self.start = False
        self.rotate_request = False
        self.random_field_request = False

        # VkAuthorization
        self.to_browser_request = False
        self.apply = False
        self.url = ""

        # Pause
        self.is_disconnect_button_pressed = False
        self.is_return_button_pressed = False

        # PostGame
        self.restart_request = False
        self.next_request = False
        self.vk_post_request = False
        self.is_to_main_menu_button_pressed = False
        self.game_info = ""

    def update(self, other: "BufferToGameLogic"):
        if other.is_locked or self.is_locked:
            return

        self.lock()
        other.lock()

        self.is_cancel_button_pressed = other.is_cancel_button_pressed
        # MainMenu
        self.is_single_play_button_pressed = (
            other.is_single_play_button_pressed
        )
        self.is_exit_button_pressed = other.is_exit_button_pressed

        # Одиночная игра
        self.is_new_game_button_pressed = other.is_new_game_button_pressed

        # InGame
        self.shot_request = other.shot_request
        self.is_pause_request = other.is_pause_request

        # GamePreparing
        self.place_request = other.place_request
        self.remove_request = other.remove_request
        self.start = other.start
        self.rotate_request = other.rotate_request
        self.random_field_request = other.random_field_request
        self.pre_show_cell_index = other.pre_show_cell_index

        # Pause
        self.is_disconnect_button_pressed = other.is_disconnect_button_pressed
        self.is_return_button_pressed = other.is_return_button_pressed

        # PostGame
        self.restart_request = other.restart_request
        self.next_request = other.next_request
        self.vk_post_request = other.vk_post_request
        self.is_to_main_menu_button_pressed = (
            other.is_to_main_menu_button_pressed
        )
        self.game_info = other.game_info

        other.unlock()
        self.unlock()

    def copy(self):
        while self.is_locked:
            pass

        other = BufferToGameLogic()
        self.lock()

        other.is_cancel_button_pressed = self.is_cancel_button_pressed
        # MainMenu
        other.is_single_play_button_pressed = (
            self.is_single_play_button_pressed
        )
        other.is_exit_button_pressed = self.is_exit_button_pressed

        # Одиночная игра
        other.is_new_game_button_pressed = self.is_new_game_button_pressed

        # InGame
        other.shot_request = self.shot_request
        other.is_pause_request = self.is_pause_request

        # GamePreparing
        other.place_request = self.place_request
        other.remove_request = self.remove_request
        other.start = self.start
        other.rotate_request = self.rotate_request
        other.random_field_request = self.random_field_request
        other.pre_show_cell_index = self.pre_show_cell_index

        # Pause
        other.is_disconnect_button_pressed = self.is_disconnect_button_pressed
        other.is_return_button_pressed = self.is_return_button_pressed

        # PostGame
        other.restart_request = self.restart_request
        other.next_request = self.next_request
        other.vk_post_request = self.vk_post_request
        other.is_to_main_menu_button_pressed = (
            self.is_to_main_menu_button_pressed
        )
        other.game_info = self.game_info

        self.unlock()

        return other

    def __iter__(self):
        pass

    def __next__(self):
        pass
