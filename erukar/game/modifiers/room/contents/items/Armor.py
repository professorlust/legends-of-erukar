from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.environment import *
import random

class Armor(RoomModifier):
    Probability = 1.0

    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.inventory.armor', None)
        randomizer.initialize()
        material = ModuleDecorator('erukar.game.modifiers.inventory.material', None)
        material.initialize()
        created = randomizer.create_one()
        material.create_one().apply_to(created)
        room.add(created)
