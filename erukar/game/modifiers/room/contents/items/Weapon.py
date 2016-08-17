from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.environment import *

class Weapon(RoomModifier):
    Probability = 1.0

    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.inventory.weapons', None)
        randomizer.initialize()
        modifiers = ModuleDecorator('erukar.game.modifiers.inventory.weapon', None)
        modifiers.initialize()
        material = ModuleDecorator('erukar.game.modifiers.inventory.material', None)
        material.initialize()

        created_weapon = randomizer.create_one()
        material.create_one().apply_to(created_weapon)
        modifiers.create_one().apply_to(created_weapon)
        room.add(created_weapon)
