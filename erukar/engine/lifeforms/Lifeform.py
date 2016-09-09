from erukar.engine.model.RpgEntity import RpgEntity
from erukar.engine.afflictions.Dead import Dead
from erukar.engine.afflictions.Dying import Dying
import erukar, math, random

class Lifeform(RpgEntity):
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
        self.strength   = 0
        self.dexterity  = 0
        self.vitality   = 0
        self.acuity     = 0
        self.sense      = 0
        self.resolve    = 0
        self.current_xp = 0
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
            for mod in equipment.modifiers:
                if hasattr(mod, stat_type):
                    print('found one')
                    score += getattr(mod, stat_type)
        # now handle afflictions
        for aff in self.afflictions:
            if hasattr(aff, stat_type):
                score += getattr(aff, stat_type)
        return score

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

    def afflicted_with(self, aff_type):
        '''Alias to simplify the check to see if the lifeform has an affliction'''
        return any(x for x in self.afflictions if isinstance(x, aff_type))

    def calculate_xp_worth(self):
        if self.level >= 100:
            return 100*self.level
        x = self.level
        return  10+math.ceil(0.5*x*x + pow(2, math.exp((x-100)/x)))

    def calculate_necessary_xp(self):
        return self.calculate_xp_worth()*5

    def award_xp(self, xp):
        print('{} has gained {} xp.'.format(self.alias(), xp))
        self.current_xp += xp
        # Allows multiple level ups to occur
        while self.current_xp >= self.calculate_necessary_xp():
            self.current_xp -= self.calculate_necessary_xp()
            self.define_level(self.level + 1)
            print('{} has leveled up! Now Level {}.'.format(self.alias(), self.level))

    def take_damage(self, damage, instigator=None):
        if self.afflicted_with(erukar.engine.afflictions.Dying):
            self.kill(killer=instigator)
            return
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.afflictions.append(Dying(self, None))

    def kill(self, killer):
        if killer is not None:
            xp = self.calculate_xp_worth()
            killer.award_xp(xp)
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
        return random.choice(descriptions)

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
