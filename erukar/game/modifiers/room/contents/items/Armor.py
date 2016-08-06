from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.environment import *
import random

class Armor(RoomModifier):
    Probability = 1

    def apply_to(self, room):
        print('Applying to Armor')
        randomizer = ModuleDecorator('erukar.game.inventory.armor', None)
        material = ModuleDecorator('erukar.game.modifiers.inventory.material', None)
        created = randomizer.create_one()
        material.create_one().apply_to(created)
        room.add(created)
