from erukar.engine.model.RpgEntity import RpgEntity
from erukar.engine.conditions.Dead import Dead
from erukar.engine.conditions.Dying import Dying
from erukar.engine.model.results.DamageResult import DamageResult
import erukar, math, random

class Lifeform(RpgEntity):
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
    attack_slots = [ "left", "right" ]
    base_health = 4

    def __init__(self, name=""):
        self.uid        = ""
        self.spells     = []
        self.inventory  = []
        self.strength   = 0
        self.dexterity  = 0
        self.vitality   = 0
        self.acuity     = 0
        self.sense      = 0
        self.resolve    = 0
        self.experience = 0
        self.dual_wielding_penalty = 0.667
        self.current_room = None
        for eq_type in self.equipment_types:
            setattr(self, eq_type, None)
        self.name = name
        self.wealth = 0
        self.skill_points = 3
        self.skills = []
        self.stat_points = 15
        self.conditions = []

    def tick(self):
        '''Regular method which is performed every 5 seconds in game time'''
        results = []
        for item_slot in self.equipment_types:
            item = getattr(self, item_slot)
            if item is not None:
                results.append(item.tick())
        for condition in self.conditions:
            results.append(condition.tick())
        return results

    def initiate_aura(self, aura):
        '''Initiates an aura within the current room'''
        self.current_room.initiate_aura(aura)

    def calculate_effective_stat(self, stat_type, depth=0):
        '''Uses a decay factor based on distance'''
        score = self.calculate_stat_score(stat_type)
        decay_factor = 1.0 - 0.75*math.exp(-0.02*score)
        return math.floor(math.pow(decay_factor,depth) * score)

    def stat_random_range(self, stat_type):
        score = self.calculate_stat_score(stat_type)
        return (score, 50+score)

    def calculate_stat_score(self, stat_type):
        '''Calculates a character's stat score based on armor and status effects'''
        score = getattr(self, stat_type)
        # First up, handle equipment
        for eq_type in self.equipment_types:
            equipment = getattr(self, eq_type)
            if equipment is None:
                continue
            penalty_args = (equipment, '{}Penalty'.format(stat_type.capitalize()))
            if hasattr(*penalty_args):
                score -= getattr(*penalty_args)

            for mod in equipment.modifiers:
                if hasattr(mod, stat_type):
                    score += getattr(mod, stat_type)

        # now handle conditions
        for condition in self.conditions:
            if hasattr(condition, stat_type):
                score += getattr(condition, stat_type)
            modify_str = 'modify_{}'.format(stat_type)
            if hasattr(condition, modify_str):
                score += getattr(condition, modify_str)()
        return score

    def is_incapacitated(self):
        return any(aff for aff in self.conditions if aff.Incapacitates)

    def turn_modifier(self):
        return round(600/(0.15*self.dexterity+10)+15 )

    def define_level(self, level):
        '''Set this lifeform's level and defined the health appropriately'''
        self.level = level
        self.max_health = sum([Lifeform.base_health + self.get('vitality') for x in range(level)])
        self.health = self.max_health

    def evasion(self):
        if self.is_incapacitated():
            return RpgEntity.base_evasion / 2

        ac_mod = self.get('dexterity')
        total_ac = RpgEntity.base_evasion

        return total_ac + ac_mod

    def has_condition(self, aff_type):
        '''Alias to simplify the check to see if the lifeform has an affliction'''
        return any(x for x in self.conditions if isinstance(x, aff_type))

    def calculate_xp_worth(self):
        x = self.level
        if x >= 100:
            return 100*x
        return math.ceil((x/100)*(100*x) + ((100-x)/100) * (10+0.5*x*x + pow(2, math.exp((x-100)/x))))

    def calculate_necessary_xp(self):
        return self.calculate_xp_worth()

    def award_xp(self, xp, target=None):
        '''Award a certain amount of XP to the player and level if the threshold is met'''
        output_strings = ['{} has gained {} xp.'.format(self.alias(), xp)]
        self.experience += xp
        # Allows multiple level ups to occur
        while self.experience >= self.calculate_necessary_xp():
            self.experience -= self.calculate_necessary_xp()
            self.level += 1
            hp_proportion = self.health / self.max_health
            self.max_health += (4 + self.vitality)
            self.health = int(math.ceil(self.max_health * hp_proportion))
            self.stat_points += 1
            output_strings.append('{} has leveled up! Now Level {}.'.format(self.alias(), self.level))
        return output_strings

    def take_damage(self, damage_amount, instigator=None):
        '''Take damage and return amount of XP to award instigator'''
        if self.has_condition(erukar.engine.conditions.Dying):
            self.kill(killer=instigator)
            return
        self.health = max(0, self.health - damage_amount)
        if self.health == 0:
            self.conditions.append(Dying(self, None))
        return 

    def kill(self, killer):
        '''Mark us as dead, then return our net worth in XP'''
        self.conditions = [Dead(self, None)]

    def link_to_room(self, room):
        self.current_room = room
        for eq in self.equipment_types:
            equip = getattr(self, eq)
            if equip is not None:
                equip.on_move(room)
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

    def begin_turn(self):
        results = [aff.do_begin_of_turn_effect() for aff in self.conditions]
        return '\n'.join(r for r in results if r is not '')

    def end_turn(self):
        results = [aff.do_end_of_turn_effect() for aff in self.conditions]
        return '\n'.join(r for r in results if r is not '')

    def lifeform(self):
        return self

    def describe_as_threat(self, lifeform, acuity, sense):
        return self.on_inspect(lifeform, acuity, sense)

    def add_to_inventory(self, item):
        if item in self.inventory: return
        self.inventory.append(item)
        item.owner = self

    def possessive_pronoun(self):
        return 'his'

    def matching_deflections_and_mitigations(self, damage_type):
        # Check for Mitigation in Armor
        for x in self.equipment_types:
            armor = getattr(self, x)
            if isinstance(armor, erukar.engine.inventory.Armor):# and damage_type in armor.DamageMitigations:
                yield armor.mitigation_for(damage_type)
        # Check for Mitigation Conditions
        for condition in self.conditions:
            if damage_type in condition.DamageMitigations:
                yield condition.DamageMitigations[damage_type]
        # Check for Base Mitigations
        if damage_type in self.BaseDamageMitigations:
            yield self.BaseDamageMitigations[damage_type]
