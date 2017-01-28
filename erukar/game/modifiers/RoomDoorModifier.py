from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Door import Door
import random

class RoomDoorModifier(RoomModifier):
    NecessaryAcuity = 0

    def __init__(self):
        self.description = "A {status} door to the {direction} opens into another room."
        self.can_close = False
        self.start_state = Door.Open
        self.lock = None
        self.necessary_acuity = 0

    def apply_to(self, room):
        rooms = list(room.adjacent_rooms())
        if len(rooms) == 0: return

        direction = random.choice(rooms)
        thisdoor = Door(self.description)
        thisdoor.acuity_needed = self.NecessaryAcuity
        thisdoor.status = self.start_state
        thisdoor.can_close = self.can_close
        room.add_door(direction, thisdoor)

        if hasattr(self, 'lock'):
            thisdoor.lock = self.lock
