from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Damage
from collections import OrderedDict
import numpy as np
import random

class Size(WeaponMod):
    Probability = 1
    Desirability = 8.0

    ShouldRandomizeOnApply = True
    PersistentAttributes = ['scaling_factor_multiplier', 'cutoff_multiplier', 'InventoryDescription', 'InventoryName']

    Levels = {
        'Miniscule': {
            'WeightMultiplier': 0.1,
        },
        'Tiny': {
            'WeightMultiplier': 0.5,
        },
        'Small': {
            'WeightMultiplier': 0.75,
        },
        '': {
            'WeightMultiplier': 1,
        },
        'Large': {
            'WeightMultiplier': 1.5,
        },
        'Huge': {
            'WeightMultiplier': 3,
        },
        'Massive': {
            'WeightMultiplier': 5,
        },
    }

    def randomize(self, parameters=None):
        self.level = int(len(self.Levels.keys()) * np.random.beta(16, 16))
        ordered_levels = OrderedDict( sorted(self.Levels.items(), key=lambda y: y[1]['WeightMultiplier']) )
        base_name = list(ordered_levels.keys())[self.level]
        self.weight_multiplier = self.Levels[base_name]['WeightMultiplier']

        self.InventoryName = '{} Size'.format(base_name if base_name else 'Standard')
        self.InventoryDescription = 'Weight is {:3.1f}% of base; weight affects strength scaling'.format(self.weight_multiplier*100)

    def apply_to(self, entity):
        super().apply_to(entity)
        entity.size = self
    
