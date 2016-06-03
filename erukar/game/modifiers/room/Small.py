from erukar.engine.model import Modifier
from erukar.engine.environment import Room
from erukar.game.modifiers.RoomModifier import RoomModifier

class Small(RoomModifier):
    def apply_to(self, room):
        room.description += ' This room is small.'
