from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories import *
from erukar.engine.environment import *
import random

class Armor(RoomModifier):
    Probability = 1.0

    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.inventory.armor', None)
        armor = randomizer.create_one()
        material = ModifierGenerator('erukar.game.modifiers.inventory.material', None, armor)
        material.create_one().apply_to(armor)
        room.add(armor)
