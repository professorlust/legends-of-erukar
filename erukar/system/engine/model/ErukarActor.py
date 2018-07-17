from .Describable import Describable
from erukar.ext.math.Distance import Distance
import random
import erukar


class ErukarActor(Describable):
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

    def minimum_sense_to_detect(self):
        return 0

    def minimum_acuity_to_detect(self):
        return 0

    def evasion(self):
        return self.base_evasion

    def generate_tile(self, dimensions, tile_id):
        h, w = dimensions
        radius = int(w/3)-1
        circle = list(Distance.points_in_circle(radius, (int(h/2),int(w/2))))
        inner_circle = list(Distance.points_in_circle(int(w/4)-1, (int(h/2),int(w/2))))
        for y in range(h):
            for x in range(w):
                if (x, y) in circle:
                    if (x, y) not in inner_circle:
                        yield {'r': 0, 'g': 0, 'b': 0, 'a': 1}
                    else:
                        yield {'r': 255, 'g': 0, 'b': 0, 'a': 1}
                else:
                    yield {'r': 0, 'g': 0, 'b': 0, 'a': 0}

    def roll(self, roll_range, distribution=None):
        if distribution is None:
            distribution = random.uniform
        return max(1, distribution(*roll_range))

    def deflection(self, damage_type):
        return sum(self._deflections(damage_type))

    def mitigation(self, damage_type):
        return 1.0 - sum(self._mitigations(damage_type))

    def _deflections(self, damage_type):
        for protection in self.protections(damage_type):
            mitigation, deflection = protection
            yield deflection

    def _mitigations(self, damage_type):
        for protection in self.protections(damage_type):
            mitigation, deflection = protection
            yield mitigation

    def protections(self, damage_type):
        if damage_type in self.BaseDamageMitigations:
            yield self.BaseDamageMitigations[damage_type]

    def damage_armor(self, damage):
        '''Damages armor durability (if applicable)'''
        for armor_type in self.equipment_types:
            armor = getattr(self, armor_type)
            if isinstance(armor, erukar.engine.inventory.Armor):
                armor.take_damage(damage)

    def process_damage(self, damages, instigator, efficacy=1.0):
        pass

    def apply_damage(self, damage_result, instigator):
        damage_sum = sum(x.amount_dealt for x in damage_result.reports)
        self.take_damage(damage_sum, instigator)

    def calculate_damage_result(self, damages, instigator, efficacy=1.0):
        pass

    def calculate_actual_damage_values(self, damage, instigator, efficacy):
        pass

    def take_damage(self, damage_amount, instigator=None):
        '''This is to be handled in subclasses'''
        pass

    def modify_element(self, mod_name, element):
        return element
