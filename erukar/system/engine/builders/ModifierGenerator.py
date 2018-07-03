from .ModuleDecorator import ModuleDecorator
from erukar.system.engine import Modifier
from erukar.ext.math import Modules


class ModifierGenerator(ModuleDecorator):
    Module = 'erukar.content.modifiers.gameplay'

    def __init__(self, item, environment, module=''):
        self.item = item
        self.Module = module or self.Module
        super().__init__(item, environment)
        self.initialize(item)

    def initialize(self, item):
        poss = list(self.get_possibilities(item))

        weights, values = zip(*[(self.calculate_probability(p), p) for p in poss])
        self.create_distribution(values, weights)

    def get_possibilities(self, item):
        for mod_name, mod_class in Modules.get_members_of(self.Module):
            if mod_class.can_apply_to(item):
                yield mod_name, mod_class
