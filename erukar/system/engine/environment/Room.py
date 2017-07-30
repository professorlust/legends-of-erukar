from erukar.system.engine import Containable, Describable, Observation, Lifeform
from erukar.system.engine.environment import Surface, Container, Door, Decoration
import random, types

class Room(Containable):
    SelfDescription = "This room is fairly large."
    DecoDescription = "You see {}."
    ContainerDescription = "In the room you see {}."
    Glances = [
        Observation(acuity=0, sense=0, result="This is a room.")
    ]

    def __init__(self, dungeon, coordinates=None):
        super().__init__([])
        self.linearity = 0
        self.dungeon = dungeon
        if isinstance(coordinates, types.GeneratorType):
            self.coordinates = list(coordinates)
        else: 
            self.coordinates = [] if not coordinates else coordinates
        self.dungeon.add_room(self, self.coordinates)
        self.floor = None
        self.ceiling = None
        self.visible_in_room_description = False

    def calculate_luminosity(self):
        return 1.0

    def calculate_danger(self):
        return 1.0

    def calculate_desirability(self):
        return 1.0

    def initiate_aura(self, aura):
        aura.location = self
        self.dungeon.active_auras.add(aura)

    def on_start(self, *_):
        '''Called when the Instance has decorated and is actually starting'''
        for content in self.contents:
            content.on_start(self)

    def get_object_by_uuid(self, uuid):
        for found in super().get_object_by_uuid(uuid):
            yield found
