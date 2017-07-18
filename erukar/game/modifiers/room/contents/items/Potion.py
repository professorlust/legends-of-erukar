from erukar.game.modifiers.RoomModifier import RoomModifier
import random, erukar

class Potion(RoomModifier):
    Probability = 5

    def apply_to(self, world, location):
        world.add_actor(erukar.game.inventory.consumables.Potion(), location)
