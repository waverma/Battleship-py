from game_logic.game import Game
from game_logic.size import Size
from view.window import Window

if __name__ == "__main__":
    window = Window(Size(Game.cell_size * 27, Game.cell_size * 14), Game())
    window.Run()
