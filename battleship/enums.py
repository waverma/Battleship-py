from enum import Enum


class InterfaceStage(Enum):
    InGame = 0
    MainMenu = 1
    Pause = 2
    PostGame = 3
    PrepareToGame = 4
    VkAuthorization = 5


class Cell(Enum):
    Empty = 0
    Shot = 3
    ShipPeace = 1
    DeadShipPeace = 2
    FullDeadShip = 4
    WrongPeace = 5
