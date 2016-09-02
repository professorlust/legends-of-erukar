from erukar.engine.model import Modifier
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier

class WaterDrops(RoomModifier):
    Probability = 1
    def apply_to(self, room):
        deco = Decoration(aliases=['water droplets', 'drops of water', 'droplets of water'])
        deco.set_vision_results(\
            minimal='You see brief flashes of light in irregular intervals dropping from the ceiling',\
            ideal='You see droplets of water falling from somewhere in the ceiling',\
            vision_range=[2, 4])
        deco.set_sensory_results(\
            minimal='You hear an irregular, soft dropping sound from somewhere.',\
            ideal='You hear the sound of water droplets falling from the ceiling to the floor.',\
            sense_range=[1, 4])
        room.add(deco)
