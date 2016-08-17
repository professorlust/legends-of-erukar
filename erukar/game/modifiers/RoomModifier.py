from erukar.engine.model import Modifier
from erukar.engine.environment import Room
import random

class RoomModifier(Modifier):
    PermissionType = Modifier.ALL_PERMITTED
    PermittedEntities = [Room]
    number_of_mutations = 3
    fields = []

    def __init__(self):
        super().__init__()
        self.randomize()

    def apply_to(self, room):
        room.description += ' The air is dusty.'

    def randomize(self):
        for field in self.fields:
            choice = random.choice(getattr(self, field + 's'))
            setattr(self, field, choice)

    def get_arguments(self):
        return {f: getattr(self, f) for f in self.fields}

    def mutate(self, input_string,  arguments):
        '''Mutates strings multiple times, as specified in the parameters above'''
        result = input_string
        for num in range(self.number_of_mutations):
            result = result.format(**arguments)
        return result
