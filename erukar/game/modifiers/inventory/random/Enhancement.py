from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.model.RpgEntity import RpgEntity
import math, random

class Enhancement(WeaponMod):
    Probability = 0
    Desirability = 0
    ShouldRandomizeOnApply = True

    StatType = ""
    StatEnhancement = "<bug> Enhancement"

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
        self.level = int(random.random() * 6)
        self.amount = int(math.pow(2, self.level))
        self.enhancement_type = random.choice(RpgEntity.AttributeTypes)
        self.InventoryName = '{} {} Enhancement'.format(self.Levels[self.level], self.enhancement_type.capitalize())
        self.InventoryDescription = 'Provides +{} bonus {}'.format(self.amount, self.enhancement_type.capitalize())

    def apply_to(self, other):
        super().apply_to(other)
        setattr(self, self.enhancement_type, self.amount)
