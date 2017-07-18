from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.factories import *
from erukar.engine.environment import *
import erukar

class Weapon(RoomModifier):
    Probability = 5

    def apply_to(self, world, location):
        randomizer = ModuleDecorator('erukar.game.inventory.weapons.standard', None)
        weapon = randomizer.create_one()

        modifiers = ModifierGenerator('erukar.game.modifiers.inventory', None, weapon)
        material = ModifierGenerator('erukar.game.modifiers.material', None, weapon)
        erukar.game.modifiers.universal.Size().apply_to(weapon)
        erukar.game.modifiers.universal.Quality().apply_to(weapon)

        material.create_one().apply_to(weapon)
        modifiers.create_one().apply_to(weapon)
        world.add_actor(weapon, location)
