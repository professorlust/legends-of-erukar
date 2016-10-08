from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.environment import *

class Key(RoomModifier):
    Probability = 5

    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.inventory.consumables.keys', None)
        room.add(randomizer.create_one())

