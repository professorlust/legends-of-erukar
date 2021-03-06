from erukar.system.engine import Modifier, Door
from .RoomModifier import RoomModifier
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
        rooms = [r for r in room.connections if room.connections[r].room is not None and room.connections[r].door is None]
        if len(rooms) == 0: return

        direction = random.choice(rooms)
        thisdoor = Door(self.description)
        thisdoor.acuity_needed = self.NecessaryAcuity
        thisdoor.status = self.start_state
        thisdoor.can_close = self.can_close
        room.add_door(direction, thisdoor)

        if hasattr(self, 'lock'):
            thisdoor.lock = self.lock
