from erukar.engine.model.RpgEntity import RpgEntity
from erukar.engine.effects.Dead import Dead
from erukar.engine.effects.Dying import Dying
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

    critical_health = ['The lifeform is in critical health']
    badly_wounded = ['The lifeform is badly wounded']
    wounded = ['The lifeform is wounded']
    slightly_wounded = ['The lifeform is slightly wounded']
    full_health = ['The lifeform is at full health']
    BaseDescription = "a {alias}"

    def __init__(self, name=""):
        self.uid = ""
        self.inventory = []
        self.strength   = 0
        self.dexterity  = 0
        self.vitality   = 0
        self.acuity     = 0
        self.sense      = 0
        self.resolve    = 0
        self.experience = 0
        self.current_room = None
        for eq_type in self.equipment_types:
            setattr(self, eq_type, None)
        self.name = name
        self.afflictions = []
        # Penalties define the reduction in efficacy of shields/weapons etc
        self.define_level(1)

    def tick(self):
        '''Regular method which is performed every 5 seconds in game time'''
        for item_slot in self.equipment_types:
            item = getattr(self, item_slot)
            if item is not None:
                item.tick()

    def initiate_aura(self, aura):
        self.current_room.initiate_aura(aura)

    def calculate_effective_stat(self, stat_type, depth=0):
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
        self.max_health = sum([Lifeform.base_health + self.get('vitality') for x in range(level)])
        self.health = self.max_health

    def calculate_armor_class(self):
        if self.is_incapacitated():
            return RpgEntity.base_armor_class

        ac_mod = self.get('dexterity')
        total_ac = RpgEntity.base_armor_class

        return total_ac + ac_mod

    def afflicted_with(self, aff_type):
        '''Alias to simplify the check to see if the lifeform has an affliction'''
        return any(x for x in self.afflictions if isinstance(x, aff_type))

    def calculate_xp_worth(self):
        x = self.level
        if x >= 100:
            return 100*x
        return math.ceil((x/100)*(100*x) + ((100-x)/100) * (10+0.5*x*x + pow(2, math.exp((x-100)/x))))

    def calculate_necessary_xp(self):
        return self.calculate_xp_worth()

    def award_xp(self, xp):
        '''Award a certain amount of XP to the player and level if the threshold is met'''
        output_strings = ['{} has gained {} xp.'.format(self.alias(), xp)]
        self.experience += xp
        # Allows multiple level ups to occur
        while self.experience >= self.calculate_necessary_xp():
            self.experience -= self.calculate_necessary_xp()
            self.level += 1
            self.afflictions.append(erukar.engine.effects.ReadyToLevel(self, None))
            output_strings.append('{} has leveled up! Now Level {}.'.format(self.alias(), self.level))
        return output_strings

    def deflection(self, damage_type):
        deflections = [df for dt, mit, df in self.matching_deflections_and_mitigations(damage_type)]
        return min(deflections) if len(deflections) > 0 else 0

    def mitigation(self, damage_type):
        return 1.0-sum([mit for dt, mit, df in self.matching_deflections_and_mitigations(damage_type)])

    def matching_deflections_and_mitigations(self, damage_type):
        for x in self.equipment_types:
            armor = getattr(self, x)
            if isinstance(armor, erukar.engine.inventory.Armor):
                mtg = [x for x in armor.DamageMitigations if x[0] == damage_type]
                if len(mtg) > 0:
                    yield mtg[0]

    def take_damage(self, damage, instigator=None):
        '''Take damage and return amount of XP to award instigator'''
        if self.afflicted_with(erukar.engine.effects.Dying):
            xp = self.kill(killer=instigator)
            return xp
        self.health = max(0, self.health - damage)
        if self.health == 0:
            self.afflictions.append(Dying(self, None))
        return 0

    def kill(self, killer):
        '''Mark us as dead, then return our net worth in XP'''
        self.afflictions = [Dead(self, None)]
        return self.calculate_xp_worth()

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
        results = [aff.do_begin_of_turn_effect() for aff in self.afflictions]
        return '\n'.join(r for r in results if r is not '')

    def end_turn(self):
        results = [aff.do_end_of_turn_effect() for aff in self.afflictions]
        return '\n'.join(r for r in results if r is not '')

    def lifeform(self):
        return self

    def describe_as_threat(self, lifeform, acuity, sense):
        return self.on_inspect(lifeform, acuity, sense)
