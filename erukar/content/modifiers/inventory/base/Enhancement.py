from ...base.WeaponMod import WeaponMod
from erukar.system.engine import ErukarActor
import math, random

class Enhancement(WeaponMod):
    Probability = 0
    Desirability = 0
    ShouldRandomizeOnApply = True

    PersistentAttributes = ['enhancement_type', 'amount', 'InventoryDescription', 'InventoryName']

    Levels = [
        'Minor',
        '',
        'Major',
        'Epic',
        'Legendary',
        'Mythical'
    ]

    def randomize(self, parameters=None):
        '''In the future we will determine level based on the generation parameters level and desirability''' 
        self.level = int(random.random() * len(self.Levels))
        self.amount = int(math.pow(2, self.level))
        self.enhancement_type = random.choice(ErukarActor.AttributeTypes)
        self.InventoryName = '{} {} Enhancement'.format(self.Levels[self.level], self.enhancement_type.capitalize())
        self.InventoryDescription = 'Provides +{} bonus {}'.format(self.amount, self.enhancement_type.capitalize())

    def apply_to(self, other):
        super().apply_to(other)
        setattr(self, self.enhancement_type, self.amount)
