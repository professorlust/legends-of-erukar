from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.model.Damage import Damage
from erukar.engine.model.Observation import Observation
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
                Observation(acuity=0, sense=0, result='with a fiery {EssentialPart}'),
                Observation(acuity=20, sense=0, result='with flames erupting from the {EssentialPart}')
            ],
            'inspects': [
                Observation(acuity=0, sense=0, result='The {EssentialPart} is on fire.'),
                Observation(acuity=10, sense=0, result='Flames rise off of the {EssentialPart}.'),
                Observation(acuity=10, sense=10, result='Flames rise off of the {EssentialPart}, radiating a large amount of heat through the room..'),
                Observation(acuity=20, sense=0, result='A plume of flames rises from the {EssentialPart}.'),
                Observation(acuity=20, sense=10, result='A plume of flames rises from the {EssentialPart}, radiating a large amount of heat through the room.')
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
                Observation(acuity=10, sense=0, result="with condensation on the {EssentialPart}"),
                Observation(acuity=25, sense=0, result="dripping with acid")
            ],
            'inspects': [
                Observation(acuity=10, sense=0, result="The {EssentialPart} has some sort of condensation on it."),
                Observation(acuity=25, sense=0, result="The {EssentialPart} is dripping with acid!")
            ]
        },
        'divine': {
            'glances': [
                Observation(acuity=0, sense=10, result='which fills you with hope'),
                Observation(acuity=0, sense=20, result='with a blessed {EssentialPart}')
            ],
            'inspects': [
                Observation(acuity=0, sense=10, result='You feel a sense of hopeful spirituality when looking upon the {alias}'),
                Observation(acuity=0, sense=20, result='You can sense that some sort of Divine entity has blessed the {EssentialPart} of the {alias}.')
            ]
        },
        'demonic': {
            'glances': [
                Observation(acuity=0, sense=10, result='which fills you with dread'),
                Observation(acuity=0, sense=20, result='with a cursed {EssentialPart}')
            ],
            'inspects': [
                Observation(acuity=0, sense=10, result='You feel a sense of dread when looking upon the {alias}'),
                Observation(acuity=0, sense=20, result='You can sense that some sort of demon has cursed the {EssentialPart} of the {alias}.')
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
