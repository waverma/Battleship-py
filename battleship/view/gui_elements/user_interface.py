from battleship.buffers.buffer_to_game_logic import BufferToGameLogic
from battleship.buffers.buffer_to_render import BufferToRender
from battleship.buffers.drawing_buffer import DrawingBuffer
from battleship.buffers.user_event import UserEvent
from battleship.enums import InterfaceStage
from battleship.view.graphic_utils import DEFAULT_MENU_COLLISION
from battleship.view.gui_elements.menus.game_menu import GameMenu
from battleship.view.gui_elements.menus.game_prepare_menu import (
    GamePrepareMenu,
)
from battleship.view.gui_elements.menus.main_menu import MainMenu
from battleship.view.gui_elements.menus.pause_menu import PauseMenu
from battleship.view.gui_elements.menus.post_game_element import (
    PostGameElement,
)
from battleship.view.gui_elements.menus.vk_authorization_menu import (
    VkAuthorizationMenu,
)


def render_per_element(buffer_to_render, new_buffer_to_draw, element):
    render_info = element.get_render_info((0, 0, 1, 1), buffer_to_render)
    for render_info_parts in render_info:
        new_buffer_to_draw.add(render_info_parts)


class UserInterface:
    def __init__(self):
        self.elements = list()
        self.stage = InterfaceStage.MainMenu

        # Создание менюшек
        self.prepare_game_field_element = GamePrepareMenu(
            DEFAULT_MENU_COLLISION, (0, 0)
        )
        self.game_field_element = GameMenu(
            DEFAULT_MENU_COLLISION, (0, 0)
        )
        self.post_game_menu = PostGameElement(
            DEFAULT_MENU_COLLISION, (0, 0)
        )
        self.vk_authorization_menu = VkAuthorizationMenu(
            DEFAULT_MENU_COLLISION, (0, 0)
        )
        self.main_menu = MainMenu(DEFAULT_MENU_COLLISION, (0, 0))
        self.pause = PauseMenu(DEFAULT_MENU_COLLISION, (0, 0))

    def update(
        self,
        e: UserEvent,
        game_state: InterfaceStage,
        output_buffer: BufferToGameLogic,
    ):
        output_buffer.interface_stage = game_state
        output_buffer.is_cancel_button_pressed = False

        if game_state == InterfaceStage.MainMenu:
            self.main_menu.update(e, output_buffer)

        elif game_state == InterfaceStage.InGame:
            self.game_field_element.update(e, output_buffer)

        elif game_state == InterfaceStage.PrepareToGame:
            self.prepare_game_field_element.update(e, output_buffer)

        elif game_state == InterfaceStage.Pause:
            self.pause.update(e, output_buffer)

        elif game_state == InterfaceStage.PostGame:
            self.post_game_menu.update(e, output_buffer)

        elif game_state == InterfaceStage.VkAuthorization:
            self.vk_authorization_menu.update(e, output_buffer)

    def render(
        self, buffer_to_render: BufferToRender, buffer_to_draw: DrawingBuffer
    ):
        new_buffer_to_draw = buffer_to_draw

        self.stage = buffer_to_render.game_stage

        if self.stage == InterfaceStage.MainMenu:
            render_per_element(
                buffer_to_render, new_buffer_to_draw, self.main_menu
            )

        elif self.stage == InterfaceStage.InGame:
            self.game_field_element.get_render_info(
                (0, 0, 1, 1), buffer_to_render, new_buffer_to_draw
            )

        elif self.stage == InterfaceStage.PrepareToGame:
            self.prepare_game_field_element.get_render_info(
                (0, 0, 1, 1), buffer_to_render, new_buffer_to_draw, False
            )

        elif self.stage == InterfaceStage.VkAuthorization:
            render_per_element(
                buffer_to_render,
                new_buffer_to_draw,
                self.vk_authorization_menu
            )

        elif self.stage == InterfaceStage.PostGame:
            render_per_element(
                buffer_to_render, new_buffer_to_draw, self.post_game_menu
            )

        elif self.stage == InterfaceStage.Pause:
            render_per_element(
                buffer_to_render, new_buffer_to_draw, self.pause
            )
