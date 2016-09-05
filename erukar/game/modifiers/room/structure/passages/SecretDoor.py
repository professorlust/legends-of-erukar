from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door

class SecretDoor(RoomDoorModifier):
    Probability = 0.5
    NecessaryAcuity = 4

    def __init__(self):
        self.description = "There is a door hidden within the wall."
        self.can_close = True
        self.start_state = Door.Closed
