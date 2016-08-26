from erukar.engine.model.RpgEntity import RpgEntity
from erukar.engine.afflictions.Dead import Dead
from erukar.engine.afflictions.Dying import Dying
import erukar, math, random

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
        "left",
        "right",
        "chest",
        "head",
        "feet",
        "arms",
        "legs",
        "ring",
        "amulet",
        "blessing"]
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
        # Penalties define the reduction in efficacy of shields/weapons etc
        self.hand_efficacy = {
            'left': 0.0,
            'right': 0.0,
            'both': 0.0
        }
        self.define_level(1)

    def calculate_handed_penalty(self, hand):
        '''
        Calculate a penalty based on the equipped weapons' properties,
        the wielder's strength, and any afflictions which might affect
        hand usage.
        '''
        return self.hand_efficacy[hand]

    def calculate_effective_stat(self, stat_type, depth):
        score = self.calculate_stat_score(stat_type)
        decay_factor = 1.0 - 0.75*math.exp(-0.02*score)
        return math.floor(math.pow(decay_factor,depth) * score)

    def calculate_stat_score(self, stat_type):
        '''Calculates a character's stat score based on armor and status effects'''
        score = getattr(self, stat_type)
        # First up, handle equipment
        for eq_type in self.equipment_types:
            equipment = getattr(self, eq_type)
            if equipment is None:
                continue
            for mod in equipment.modifiers:
                if hasattr(mod, stat_type):
                    print('found one')
                    score += getattr(mod, stat_type)
        # now handle afflictions
        for aff in self.afflictions:
            if hasattr(aff, stat_type):
                score += getattr(aff, stat_type)
        return score

    def define_stats(self, stats):
        '''Takes a dictionary to define stats.'''
        for stat in [stat for stat in stats if hasattr(self, stat)]:
            setattr(self, stat, stats[stat])

    def is_incapacitated(self):
        return any(aff for aff in self.afflictions if aff.Incapacitates)

    def turn_modifier(self):
        return 10.0 + round(40*(1.0 - 1.0 / (1.0 + math.exp( (10.0-self.dexterity) / 5.0))))

    def define_level(self, level):
        '''Set this lifeform's level and defined the health appropriately'''
        self.level = level
        self.max_health = sum([Lifeform.base_health + self.get(Lifeform.health_attribute) for x in range(level)])
        self.health = self.max_health

    def calculate_armor_class(self):
        if self.is_incapacitated():
            return RpgEntity.base_armor_class

        ac_mod = self.get(Lifeform.armor_attribute)
        total_ac = RpgEntity.base_armor_class

        for armor_type in self.equipment_types:
            if hasattr(self, armor_type):
                armor = getattr(self, armor_type)
                # This allows us to use a shield in off/main hands
                if armor is not None and issubclass(type(armor), erukar.engine.inventory.Armor):
                    ac_mod = min(ac_mod, armor.max_dex_mod)
                    total_ac += armor.calculate_armor_class()

        return total_ac + ac_mod

    def skill_range(self, skill_type):
        skill_value = self.get(skill_type)
        return (1+skill_value, 20+(2*skill_value))

    def afflicted_with(self, aff_type):
        '''Alias to simplify the check to see if the lifeform has an affliction'''
        return any(x for x in self.afflictions if isinstance(x, aff_type))

    def take_damage(self, damage):
        if self.afflicted_with(erukar.engine.afflictions.Dying):
            self.kill()
            return

        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.afflictions.append(Dying(self, None))

    def kill(self):
        self.afflictions = [Dead(self, None)]

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
        return 'There is a {}. {}'.format(self.alias(), random.choice(descriptions))

    def alias(self):
        return self.name

    def begin_turn(self):
        results = [aff.do_begin_of_turn_effect() for aff in self.afflictions]
        return '\n'.join(r for r in results if r is not '')

    def end_turn(self):
        results = [aff.do_end_of_turn_effect() for aff in self.afflictions]
        return '\n'.join(r for r in results if r is not '')

    def lifeform(self):
        return self
