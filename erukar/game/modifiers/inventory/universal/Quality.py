from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.model.Damage import Damage
import random

class Quality(WeaponMod):
    Probability = 1
    Desirability = 8.0

    ShouldRandomizeOnApply = True
    PersistentAttributes = ['scaling_factor_multiplier', 'cutoff_multiplier', 'InventoryDescription', 'InventoryName']

    PriceModifier = [
        0.01,
        0.10,
        0.25,
        0.33,
        0.40,
        0.67,
        0.80,
        1.00,
        1.33,
        1.67,
        2.00,
        2.50,
        3.00,
        4.00,
        5.00,
    ]

    MultiplierRanges = [
        [0.00, 0.25],
        [0.15, 0.40],
        [0.30, 0.60],
        [0.45, 0.75],
        [0.45, 0.75],
        [0.60, 0.80],
        [0.75, 0.99],
        [0.80, 1.20],
        [0.95, 1.50],
        [1.10, 1.75],
        [1.50, 2.00],
        [1.80, 2.50],
        [1.80, 2.50],
        [2.25, 3.25],
        [3.00, 5.00],
    ]

    Levels = [
        'Grotesque',
        'Crude',
        'Shoddy',
        'Inferior',
        'Poor',
        'Low Quality',
        'Imperfect',
        'Standard',
        'Refined',
        'High Quality',
        'Masterwork',
        'Greater',
        'Superior',
        'Grand',
        'Resplendent'
    ]

    def randomize(self, parameters=None):
        '''In the future we will determine level based on the generation parameters level and desirability''' 
        self.level = int(random.random() * len(self.Levels))
        self.scaling_factor_multiplier = random.uniform(*self.MultiplierRanges[self.level])
        self.cutoff_multiplier = random.uniform(*self.MultiplierRanges[self.level])
        self.InventoryName = '{} Craftsmanship'.format(self.Levels[self.level])
        self.InventoryDescription = 'Dexterity Scaling Factor set to {}% of base; maximum Dexterity Scaling Influence set to {}% of base'.format(int(self.scaling_factor_multiplier*100), int(self.cutoff_multiplier*100))

    def on_alias(self, current_alias):
        return ' '.join([self.Levels[self.level], current_alias])

    def apply_to(self, entity):
        super().apply_to(entity)
        entity.build_quality = self
