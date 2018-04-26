from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Observation, Damage, DamageScalar
import numpy as np
import random

class AdditionalDamage(WeaponMod):
    Probability = 1
    Desirability = 8.0

    ShouldRandomizeOnApply = True
    PersistentAttributes = ['rarity', 'min_damage', 'max_damage', 'damage_type', 'InventoryDescription', 'InventoryName']

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
            'inventory_name': '{} Flaming {}',
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
            'inventory_name': '{} Frosted {}',
            'glances': [
            ],
            'inspects': [
            ]
        },
        'electric': {
            'inventory_name': '{} Electric {}',
            'glances': [
            ],
            'inspects': [
            ]
        },
        'acid': {
            'inventory_name': '{} Acidic {}',
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
            'inventory_name': '{} Divine {}',
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
            'inventory_name': '{} Demonic {}',
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
        if not hasattr(self, 'level'):
            self.level = int(random.random() * len(self.Levels))
        if not hasattr(self, 'min_damage') or not hasattr(self, 'max_damage'):
            self.min_damage, self.max_damage = self.DamageRanges[self.level]
        if not hasattr(self, 'damage_type'):
            self.damage_type = random.choice(list(self.Damages.keys()))
        self.InventoryName = '{} {} Augmentation'.format(self.Levels[self.level], self.damage_type.capitalize()).strip()
        self.InventoryDescription = 'Deals {} to {} extra {} damage per attack'.format(self.min_damage, self.max_damage, self.damage_type)

    def apply_subclass(self, subclass):
        self.damage_type = subclass

    def apply_to(self, weapon):
        super().apply_to(weapon)
        extra = Damage(self.damage_type)
        weapon.damages.append(extra)

    def get_additional_damages(self, weapon):
        yield Damage(self.damage_type, DamageScalar(self.max_damage, 'acuity'))

    def on_alias(self, current):
        return self.Damages[self.damage_type]['inventory_name'].format(self.Levels[self.level], current).strip()

    def on_calculate_attack_ranged(self, attack_state):
        extra = Damage(self.damage_type)
        attack_state.add_extra_damage(extra)
