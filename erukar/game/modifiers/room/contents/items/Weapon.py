from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories import *
from erukar.engine.environment import *

class Weapon(RoomModifier):
    Probability = 5

    def apply_to(self, room):
        randomizer = ModuleDecorator('erukar.game.inventory.weapons.standard', None)
        weapon = randomizer.create_one()

        modifiers = ModifierGenerator('erukar.game.modifiers.inventory', None, weapon)
        material = ModifierGenerator('erukar.game.modifiers.material', None, weapon)

        material.create_one().apply_to(weapon)
        modifiers.create_one().apply_to(weapon)
        room.add(weapon)
