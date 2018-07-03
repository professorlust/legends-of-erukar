from .ModuleDecorator import ModuleDecorator
from erukar.ext.math import Modules
import random


class EnemyGenerator(ModuleDecorator):
    Module = 'erukar.content.enemies'

    def __init__(self, generator):
        self.world = generator.world
        self.generator = generator
        self.level = getattr(generator.location, 'level', 5)
        super().__init__(None, generator.environment_profile)
        self.initialize()

    def initialize(self, *_):
        poss = list(self.get_possibilities())

        weights, values = zip(*[(self.calculate_probability(p), p) for p in poss])
        self.create_distribution(values, weights)

    def get_possibilities(self):
        for name, cls in Modules.get_members_of(self.Module):
            if self.is_valid_class(cls):
                yield name, cls

    def is_valid_class(self, cls):
        return self.level - 5 <= cls.ClassLevel <= self.level + 5

    def add_enemies(self):
        enemies_added = 0
        while random.random() < 0.8**enemies_added:
            self.add_enemy()
            enemies_added += 1

    def add_enemy(self):
        enemy = self.create_one()
        self.world.add_actor(enemy, self.generator.random_location())
