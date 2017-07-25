from erukar.engine.model.Tile import Tile
from erukar.engine.model.GenerationParameter import GenerationParameter
import random, operator, functools

class Snow(Tile):
    GenerationParameters = {
        'moisture':    GenerationParameter(0, 2),
        'temperature': GenerationParameter(0, 2)
    }

    def probability_distribution(self, profile):
        return functools.reduce(operator.mul, ([
            self.GenerationParameters[param_type].probability_distribution(getattr(profile, param_type, 0.0))\
            for param_type in self.GenerationParameters.keys()
        ]))

    def generate(self, *_):
        random_gray = random.uniform(225, 250)
        return [int(random_gray) for x in range(3)] + [1]

