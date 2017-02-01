from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.model.Damage import Damage
import numpy as np
import random

class AdditionalDamage(WeaponMod):
    Probability = 1
    Desirability = 8.0

    ShouldRandomizeOnApply = True
    PersistentAttributes = ['min_damage', 'max_damage', 'damage_type', 'InventoryDescription', 'InventoryName']

    DamageRanges = [
        [1, 4],
        [4, 8],
        [8, 16],
        [16, 32],
        [32, 48],
        [48, 64]
    ]

    Damages = {
        'fire': {
            'glances': [
            ],
            'inspects': [
            ]
        },
        'ice': {
            'glances': [
            ],
            'inspects': [
            ]
        },
        'electric': {
            'glances': [
            ],
            'inspects': [
            ]
        },
        'acid': {
            'glances': [
            ],
            'inspects': [
            ]
        },
        'divine': {
            'glances': [
            ],
            'inspects': [
            ]
        },
        'demonic': {
            'glances': [
            ],
            'inspects': [
            ]
        },
    }

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
        self.min_damage, self.max_damage = self.DamageRanges[self.level]
        self.damage_type = random.choice(list(self.Damages.keys()))
        self.InventoryName = '{} {} Augmentation'.format(self.Levels[self.level], self.damage_type.capitalize()).strip()
        self.InventoryDescription = 'Deals {} to {} extra {} damage per attack'.format(self.min_damage, self.max_damage, self.damage_type)

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.damages.append(Damage(
            self.damage_type.capitalize(),
            [self.min_damage, self.max_damage],
            "",
            (np.random.uniform, (0,1))
        ))
