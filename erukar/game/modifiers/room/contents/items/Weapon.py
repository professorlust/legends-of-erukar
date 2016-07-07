from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.environment import *

class Weapon(RoomModifier):
    Probability = 10

    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.inventory.weapons', None)
        modifiers = ModuleDecorator('erukar.game.modifiers.inventory.weapon', None)
        created_weapon = randomizer.create_one()
        modifiers.create_one().apply_to(created_weapon)
        room.add(created_weapon)
