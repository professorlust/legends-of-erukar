from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door

class PuzzleDoor(RoomDoorModifier):
    Probability = 0.5
    def __init__(self):
        self.description = "The door seems to have a puzzle on it, but it's not finished."
        self.can_close = True
        self.start_state = Door.Closed
