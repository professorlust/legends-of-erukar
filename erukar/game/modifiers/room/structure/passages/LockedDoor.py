from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door, Key, Lock
import random

class LockedDoor(RoomDoorModifier):
    ProbabilityFromFabrication = 0.75
    def __init__(self):
        self.description = "This door is locked."
        self.can_close = True
        self.start_state = Door.Closed
        self.lock = Lock()

    def apply_to(self, room):
        super().apply_to(room)
        k = Key(self.lock)
        viable_rooms = [room.dungeon.rooms[r] for r in range(room.dungeon.rooms.index(room))]
        target_room = random.choice(viable_rooms)
        target_room.add(k)
