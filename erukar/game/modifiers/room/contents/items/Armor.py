from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.environment import *
import random

class Armor(RoomModifier):
    Probability = 5

    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.inventory.armor.shields', None)
        created = randomizer.create_one()
        room.add(created)
