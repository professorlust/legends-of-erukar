from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.engine.environment.Surface import Surface
import random

class CarpetFloor(RoomModifier):
    ProbabilityFromFabrication = 1
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
    anomalys = [
        "is torn",
        "has become rotten over time",
        "has been freshly cleaned",
        "is waterlogged, making unpleasant squishing noises as you move your feet"
    ]

    fields = [
        "texture",
        "color",
        "anomaly"
    ]

    def apply_to(self, room):
        args = self.get_arguments()
        room.floor = Surface("")
        room.floor.anomaly = self.anomaly
        room.floor.texture = self.texture
        room.floor.color = self.color
        room.floor.BriefDescription = "{color} carpet"
