from erukar.system.engine import Enemy
import random

class Dragonoid(Enemy):
    def __init__(self, name, is_random=True):
        super().__init__(name, is_random)
        self.strength = int(random.uniform(2, 5))
        self.dexterity = int(random.uniform(1, 4))
        self.vitality = int(random.uniform(4, 6))
        self.acuity = int(random.uniform(2, 3))
        self.sense = int(random.uniform(2, 5))
        self.resolve = int(random.uniform(1, 3))
        self.define_level(5)
