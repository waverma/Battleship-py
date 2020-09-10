from game_logic.game import Game
from game_logic.user_event import Size
from view.window import Window

if __name__ == "__main__":
    window = Window(Size(1000, 1000), Game())
    window.Run()
