from erukar.game.modifiers.RoomModifier import RoomModifier
import random, erukar

class Potion(RoomModifier):
    Probability = 5

    def apply_to(self,room):
        room.add(erukar.game.inventory.consumables.Potion())
