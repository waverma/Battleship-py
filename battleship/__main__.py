from battleship.game_loop import GameLoop
from battleship.view.graphic_utils import DEFAULT_CLIENT_SIZE

if __name__ == "__main__":

    game_loop = GameLoop(
        DEFAULT_CLIENT_SIZE[0],
        DEFAULT_CLIENT_SIZE[1],
    )

    game_loop.run()
