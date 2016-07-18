from erukar.engine.model.RpgEntity import RpgEntity
import math, random

class Lifeform(RpgEntity):
    attribute_types = [
        "strength", 
        "dexterity", 
        "vitality", 
        "acuity", 
        "sense", 
        "resolve"]
    attribute_value_default = 0 
    attack_damage_attribute = "strength"
    attack_roll_attribute = "dexterity"
    armor_attribute = "dexterity"
    health_attribute = "vitality"
    equipment_types = [
        "armor",
        "helmet",
        "boots",
        "offhand",
        "weapon"]
    base_health = 4

    critical_health = ['The lifeform is in critical health']
    badly_wounded = ['The lifeform is badly wounded']
    wounded = ['The lifeform is wounded']
    slightly_wounded = ['The lifeform is slightly wounded']
    full_health = ['The lifeform is at full health']

    def __init__(self, name=""):
        for att in Lifeform.attribute_types:
            setattr(self, att, Lifeform.attribute_value_default)
        self.current_room = None
        for eq_type in self.equipment_types:
            setattr(self, eq_type, None)
        self.name = name
        self.afflictions = []
        self.define_level(1)

    def define_stats(self, stats):
        '''Takes a dictionary to define stats.'''
        for stat in [stat for stat in stats if hasattr(self, stat)]:
            setattr(self, stat, stats[stat])

    def is_incapacitated(self):
        return any(x for x in ['dead','dying','incapacitated'] if x in self.afflictions)

    def turn_modifier(self):
        if self.is_incapacitated():
            return 10000
        return 10.0 + round(40*(1.0 - 1.0 / (1.0 + math.exp( (10.0-self.dexterity) / 5.0))))

    def define_level(self, level):
        '''Set this lifeform's level and defined the health appropriately'''
        self.level = level
        self.max_health = sum([Lifeform.base_health + self.get(Lifeform.health_attribute) for x in range(level)])
        self.health = self.max_health

    def calculate_armor_class(self):
        if 'dying' in self.afflictions:
            return RpgEntity.base_armor_class

        ac_mod = self.get(Lifeform.armor_attribute)
        if self.armor is not None:
            return self.armor.calculate_armor_class(ac_mod)
        return Lifeform.base_armor_class + ac_mod

    def skill_range(self, skill_type):
        skill_value = self.get(skill_type)
        return (1+skill_value, 20+(2*skill_value))

    def take_damage(self, damage):
        if 'dying' in self.afflictions:
            self.kill()
            return

        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.afflictions.append('dying')

    def kill(self):
        self.afflictions = ['dead']

    def link_to_room(self, room):
        self.current_room = room
        room.contents.append(self)

    def get(self, attribute):
        '''Alias for getattr(self, ____)'''
        return getattr(self, attribute)

    def matches(self, payload):
        return payload.lower() in self.alias().lower()

    def describe(self):
        descriptor_index = math.floor(4.0 * self.health / self.max_health)
        description_type = [
            'critical_health',
            'badly_wounded',
            'wounded',
            'slightly_wounded',
            'full_health']
        descriptions = getattr(self, description_type[descriptor_index])
        return random.choice(descriptions)

    def alias(self):
        return self.name
