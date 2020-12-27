from battleship.game_loop import GameLoop
from battleship.view.graphic_utils import DEFAULT_CLIENT_SIZE
from battleship.vk_provider import check_secret_file

if __name__ == "__main__":

    game_loop = GameLoop(
        DEFAULT_CLIENT_SIZE[0],
        DEFAULT_CLIENT_SIZE[1],
    )

    check_secret_file()

    game_loop.run()
