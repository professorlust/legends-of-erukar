import math

class GenerationParameter:
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def probability(self, value):
        return max(0, math.sin((self.a - value) * math.pi / self.b))
