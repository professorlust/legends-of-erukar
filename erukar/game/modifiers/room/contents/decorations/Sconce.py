from erukar.engine.model import Modifier
from erukar.game.inventory.consumables.Torch import Torch
from erukar.engine.environment import *
from erukar.game.modifiers.RoomModifier import RoomModifier
from erukar.game.modifiers.material.random.Oak import Oak
from erukar.game.modifiers.inventory import Luminous, Glowing
import random

class Sconce(RoomModifier):
    Probability = 0.2
    ProbabilityFromFabrication = 0.25
    broad_alias_base = 'sconce'

    def __init__(self):
        super().__init__()
        self.torch_possibilities = [
            ('charred torch', self.charred, 'You smell smoke that seems to linger on the air.', 10),
            ('dimly burning torch', self.dim, 'You hear the faintest crackle of flames from the tip of a {torch_type} on the {location} side of the room', 30),
            ('burning torch', self.burning, 'You feel the heat of a {torch_type}\'s flames.', 20),
            ('brightly burning torch', self.bright, 'The crackle, heat, and light emanating from the {location} by a {torch_type} are unmistakable.', 10)]

    def apply_to(self, room):
        torch, add_torch_method, sensory_result, sense_difficulty = random.choice(self.torch_possibilities)

        deco = Decoration(aliases=[self.broad_alias_base])
        deco.torch_type = torch
        deco.location = random.choice([x.name for x in room.connections])
        deco.BriefDescription = 'a sconce on the {location} wall'
        deco.set_vision_results('You see a {torch} on the {location} wall.',
                                'You see a {torch} inside of a sconce on the {location} wall.', (5, 8))
        deco.set_sensory_results('', sensory_result, (sense_difficulty, sense_difficulty))
        deco.set_detailed_results(sensory_result, sensory_result)
        add_torch_method(room)
        room.add(deco)

    def make_torch(self, room, fuel):
        '''Make a base torch and add it to the room'''
        torch = Torch()
        torch.fuel = fuel
        Oak().apply_to(torch)
        room.add(torch)
        return torch

    def charred(self, room):
        self.make_torch(room, 0)

    def dim(self, room):
        torch = self.make_torch(room, random.uniform(10, 25))

    def bright(self, room):
        torch = self.make_torch(room, random.uniform(75,100))

    def burning(self, room):
        torch = self.make_torch(room, random.uniform(25, 75))
