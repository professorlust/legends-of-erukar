from erukar.game.modifiers.RoomDoorModifier import RoomDoorModifier
from erukar import Door, Key, Lock
import random

class LockedDoor(RoomDoorModifier):
    Probability = 0
    ProbabilityFromFabrication = 0.75

    def __init__(self):
        self.description = 'You see {describe_locked} door to the {direction}. The door is {status}. {describe_lock}'
        self.can_close = True
        self.start_state = Door.Closed
        self.lock = Lock()

    def apply_to(self, room):
        super().apply_to(room)
        k = Key(self.lock)
        possible_rooms = range(max(1, room.dungeon.rooms.index(room)))
        key_location = random.choice(list(possible_rooms))
        room.dungeon.rooms[key_location].add(k)
