from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface
import random

class CarpetFloor(RoomModifier):
    ProbabilityFromFabrication = 0.6
    colors = [
        "dark red",
        "light red",
        "dark blue",
        "dark green",
        "purple",
        "beige",
        "brown",
        "black",
        "white"
    ]
    textures = [
        "soft",
        "shaggy",
        "matted",
        "level-loop pile",
        "cut pile",
        "saxony",
        "cut loop",
        "frieze",
        "berber"
    ]
    fields = [
        "texture",
        "color"
    ]
    description = "The floor of this room is a {texture} {color} carpet"

    def apply_to(self, room):
        args = self.get_arguments()
        room.floor = Surface(self.mutate(self.description, args))
