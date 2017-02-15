from erukar.engine.model.Describable import Describable
from erukar.engine.model.results import *
import erukar, math, random, re

class RpgEntity(Describable):
    equipment_types = []
    base_evasion = 10
    BaseDamageMitigations = {}
    AttributeTypes = [
        'strength',
        'dexterity',
        'vitality',
        'acuity',
        'sense',
        'resolve'
    ]

    def __init__(self):
        super().__init__()

    def evasion(self):
        return RpgEntity.base_evasion

    def roll(self, roll_range, distribution=None):
        if distribution is None:
            distribution = random.uniform
        return max(1, distribution(*roll_range))

    def deflection(self, damage_type):
        return sum( [df for mit, df in self.matching_deflections_and_mitigations(damage_type)] )

    def mitigation(self, damage_type):
        return 1.0-sum([mit for mit, df in self.matching_deflections_and_mitigations(damage_type)])

    def matching_deflections_and_mitigations(self, damage_type):
        if damage_type in self.BaseDamageMitigations:
            yield self.BaseDamageMitigations[damage_type]

    def damage_armor(self, damage):
        '''Damages armor durability (if applicable)'''
        for armor_type in self.equipment_types:
            armor = getattr(self, armor_type)
            if isinstance(armor, erukar.engine.inventory.Armor):
                armor.take_damage(damage)

    def process_damage(self, damages, instigator, efficacy=1.0):
        '''Apply a list of damages to this player and return a result'''
        damage_result = self.calculate_damage_result(damages, instigator, efficacy)
        damage_result.parse_status()
        return damage_result

    def apply_damage(self, damage_result, instigator):
        damage_sum = sum(x.amount_dealt for x in damage_result.reports)
        self.take_damage(damage_sum, instigator)  

    def calculate_damage_result(self, damages, instigator, efficacy=1.0):
        '''
        Similar to singular version but accepts a list.
        Returns a DamageResult object
        '''
        result = DamageResult(self, instigator)
        for damage in damages:
            damage_report = self.calculate_actual_damage_values(damage, instigator, efficacy)
            result.reports.append(damage_report)
        return result

    def calculate_actual_damage_values(self, damage, instigator, efficacy):
        '''Apply Deflection and Mitigation to a damage value'''
        result = DamageMitigationResult(damage)
        result.set_attacker(instigator)
        result.raw = int(damage.roll(instigator) * efficacy)

        # Check to see how much damage is mitigated
        after_deflection = result.raw - self.deflection(damage.name)
        if after_deflection <= 0:
            result.amount_deflected = result.raw - after_deflection
            result.stopped_by_deflection = True
            return result

        # Check to see how much is mitigated
        result.amount_dealt = int(after_deflection * self.mitigation(damage.name))
        if result.amount_dealt < 1:
            result.amount_mitigated = after_deflection - result.amount_dealt
            result.stopped_by_mitigation = True

        return result

    def take_damage(self, damage_amount, instigator=None):
        '''This is to be handled in subclasses'''
        pass
