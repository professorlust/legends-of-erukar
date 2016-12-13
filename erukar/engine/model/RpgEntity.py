from erukar.engine.model.Describable import Describable
import erukar, math, random, re

class RpgEntity(Describable):
    equipment_types = []
    base_armor_class = 10
    BaseDamageMitigations = {}

    def __init__(self):
        super().__init__()

    def calculate_armor_class(self):
        return RpgEntity.base_armor_class

    def roll(self, roll_range, distribution=None):
        '''Roll on a string such as '1d20' or '6d6+6' '''
        if distribution is None:
            distribution = random.uniform
        return max(1, distribution(*roll_range))

    def deflection(self, damage_type):
        deflections = [df for mit, df in self.matching_deflections_and_mitigations(damage_type)]
        return min(deflections) if len(deflections) > 0 else 0

    def mitigation(self, damage_type):
        return 1.0-sum([mit for mit, df in self.matching_deflections_and_mitigations(damage_type)])

    def matching_deflections_and_mitigations(self, damage_type):
        for x in self.equipment_types:
            armor = getattr(self, x)
            if isinstance(armor, erukar.engine.inventory.Armor):# and damage_type in armor.DamageMitigations:
                yield armor.mitigation_for(damage_type)
        if damage_type in self.BaseDamageMitigations:
            yield self.BaseDamageMitigations[damage_type]

    def damage_armor(self, damage):
        '''Damages armor durability (if applicable)'''
        for armor_type in self.equipment_types:
            armor = getattr(self, armor_type)
            if isinstance(armor, erukar.engine.inventory.Armor):
                armor.take_damage(damage)

