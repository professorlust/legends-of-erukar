from erukar.engine.model.RpgEntity import RpgEntity
from erukar.engine.conditions.Dead import Dead
from erukar.engine.conditions.Dying import Dying
from erukar.engine.model.Observation import Observation
from erukar.engine.environment.Corpse import Corpse
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
        "ammunition",
    ]
    attack_slots = [ "left", "right" ]
    base_health = 4
    UnknownWordEfficiency = 0.01
    BaseDualWieldingPenalty = 60
    ArcaneEnergyRegenPercentage = 0.05

    def __init__(self, name=""):
        super().__init__()
        self.name       = name
        self.uid        = ""
        self.inventory  = []
        self.initialize_stats() 
        self.room = None
        self.instance = ''
        for eq_type in self.equipment_types:
            setattr(self, eq_type, None)
        self.wealth = 0
        self.initialize_effects()

    def initialize_effects(self):
        self.skill_points   = 5
        self.skills         = []
        self.conditions     = []
        self.spell_words    = []
        self.action_points  = 2

    def initialize_stats(self):
        self.stat_points    = 15
        self.strength       = 0
        self.dexterity      = 0
        self.vitality       = 0
        self.acuity         = 0
        self.sense          = 0
        self.resolve        = 0
        self.experience     = 0
        self.arcane_energy  = 0
        self.health         = self.base_health

    def subscribe(self, instance):
        self.instance = instance.identifier
        self.arcane_energy = self.maximum_arcane_energy()

    def tick(self):
        '''Regular method which is performed every 5 seconds in game time'''
        results = []
        # Tick all equipped items
        for item_slot in self.equipment_types:
            item = getattr(self, item_slot)
            if item is not None:
                results.append(item.tick())
        # Tick all conditions
        for condition in self.conditions:
            results.append(condition.tick())
        # regenerate arcane energy
        max_arcane = self.maximum_arcane_energy()
        if not self.is_incapacitated() and self.arcane_energy < max_arcane:
            self.arcane_energy = min(max_arcane, self.arcane_energy + int(max_arcane * Lifeform.ArcaneEnergyRegenPercentage))
        return results

    def get_object_by_uuid(self, uuid):
        for item in self.inventory:
            if item.uuid and item.uuid == uuid:
                return item

    def maximum_arcane_energy(self):
        arcane_gift = self.get_skill(erukar.engine.base.skills.ArcaneGift)
        return 0 if not arcane_gift else arcane_gift.arcane_energy()

    def get_skill(self, skill_class):
        if type(skill_class) is str:
            return next((x for x in self.skills if x.__module__ == skill_class), None)
        return next((x for x in self.skills if isinstance(x, skill_class)), None)

    def initiate_aura(self, aura):
        '''Initiates an aura within the current room'''
        self.room.initiate_aura(aura)

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
        for equipment in self.equipped_items():
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

        # finally check for EL penalty if dex
        if stat_type == 'dexterity':
            score -= self.equip_load_penalty()

        return score

    def calculate_attack_roll(self, efficiency, target):
        raw = self.roll(self.stat_random_range('dexterity'))
        attack_mod = sum([x.modify_attack_roll(target) for x in self.conditions])
        return int((raw + attack_mod) * efficiency)

    def on_process_damage(self, attack_state, command):
        '''Called after a successful attack'''
        for condition in self.conditions:
            condition.on_process_damage(attack_state, command)
        if attack_state.weapon:
            attack_state.weapon.on_process_damage(attack_state, command)

    def get_detection_pair(self):
        '''Retrieve a rolled Acuity and Sense for detection'''
        return [math.floor(random.uniform(*self.stat_random_range(x))) for x in ('acuity', 'sense')]

    def minimum_sense_to_detect(self):
        condition_mod = sum([x.modify_sense_to_detect() for x in self.conditions])
        return 1 + condition_mod

    def minimum_acuity_to_detect(self):
        condition_mod = sum([x.modify_acuity_to_detect() for x in self.conditions])
        return self.calculate_effective_stat('dexterity') + condition_mod

    def get_grasp_index(self, word):
        return next((i for i,x in enumerate(self.spell_words) if x.word_class == word), None)

    def add_successful_cast(self, word):
        index = self.get_grasp_index(word)
        self.increment_grasp_scores(index, True)

    def add_failed_cast(self, word):
        index = self.get_grasp_index(word)
        self.increment_grasp_scores(index)

    def increment_grasp_scores(self, index, is_successful=False):
        if index is None: return
        self.spell_words[index].total += 1
        self.spell_words[index].successes += is_successful

    def spell_word_efficacy(self, word):
        index = self.get_grasp_index(word)
        if index is None:
            return self.UnknownWordEfficiency

        # Check for relevant skills here
        return self.spell_words[index].efficiency()

    def equip_load_penalty(self):
        return max(0, math.floor(20 * (self.equip_load() / self.max_equip_load() - 1)))

    def equip_load(self):
        return int(sum([eq.weight() for eq in self.equipped_items()]))

    def max_equip_load(self):
        effective_strength = self.calculate_stat_score('strength')
        if effective_strength > 10:
            return 70 + 2 * effective_strength
        return 10 + 5 * effective_strength

    def equipped_items(self, with_location=False):
        for eq_type in self.equipment_types:
            equipment = getattr(self, eq_type)
            if equipment is not None:
                yield (eq_type, equipment) if with_location else equipment

    def is_incapacitated(self):
        return any(aff for aff in self.conditions if aff.Incapacitates)

    def turn_modifier(self):
        return round(600/(0.15*self.dexterity+10)+15 )

    def define_level(self, level):
        '''Set this lifeform's level and defined the health appropriately'''
        self.level = level
        self.max_health = sum([Lifeform.base_health + self.get('vitality') for x in range(level)])
        self.health = self.max_health

    def dual_wielding_penalty(self):
        '''Figures out the penalty for wielding a weapon in the character's offhand'''
        dual_wielding = self.get_skill('erukar.game.skills.offensive.DualWielding')
        reduction = 0 if not dual_wielding else dual_wielding.current_penalty_reduction()
        print(reduction)
        return (Lifeform.BaseDualWieldingPenalty - reduction) / 100.0

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

    def award_xp(self, xp, cmd):
        '''Award a certain amount of XP to the player and level if the threshold is met'''
        output_strings = ['{} has gained {} xp.'.format(self.alias(), xp)]
        self.experience += xp
        necessary_xp = self.calculate_necessary_xp()

        # Allows multiple level ups to occur
        while self.experience >= necessary_xp:
            self.experience -= necessary_xp
            self.perform_level_up(output_strings)
    
        cmd.append_result(self.uid, '\n'.join(output_strings))

    def perform_level_up(self, output_strings):
        '''Level up the character once'''
        self.level += 1
        output_strings.append('{} has leveled up! Now Level {}.'.format(self.alias(), self.level))

        # Manage Health
        hp_proportion = self.health / self.max_health
        self.max_health += (4 + self.vitality)
        self.health = int(math.ceil(self.max_health * hp_proportion))

        # Manage stat and skill points
        self.stat_points += 1
        self.check_for_skill_point_award(output_strings)

    def check_for_skill_point_award(self, output_strings):
        '''
        Skill point progression (80 maximum skill points)
        Level 1         : 6 per level
        Level 2   -  30 : 1 per level
        Level 31  - 100 : 1 per 2 levels
        Level 100       : Extra point
        Level 101 - 200 : 1 per 10 levels
        '''
        eligible = 2 <= self.level < 30 \
            or (30 <= self.level < 100 and self.level % 2 == 0) \
            or (100 <= self.level < 200 and self.level % 10 == 0)

        if self.level == 100:
            self.skill_points += 1
    
        if eligible:
            self.skill_points += 1
            output_strings.append('{} now has {} skill points.'.format(self.alias(), self.skill_points))

    def take_damage(self, damage_amount, instigator=None):
        '''Take damage and return amount of XP to award instigator'''
        if self.has_condition(erukar.engine.conditions.Dying):
            self.kill(killer=instigator)
            return
        self.health = max(0, self.health - damage_amount)
        if self.health == 0:
            self.conditions.append(Dying(self, None))

    def kill(self, killer):
        '''Mark us as dead, then return our net worth in XP'''
        self.conditions = [Dead(self, None)]
        self.room.add(Corpse(self))
        self.room.remove(self)
        self.room = None

    def on_move(self, room):
        self.room = room
        for eq in self.equipment_types:
            equip = getattr(self, eq)
            if equip is not None:
                equip.on_move(room)
        room.add(self)

    def get(self, attribute):
        '''Alias for getattr(self, ____)'''
        return getattr(self, attribute)

    def matches(self, payload):
        return payload.lower() in self.alias().lower()

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
            if isinstance(armor, erukar.engine.inventory.Armor):
                yield armor.mitigation_for(damage_type)
        # Check for Mitigation Conditions
        for condition in self.conditions:
            if damage_type in condition.DamageMitigations:
                yield condition.DamageMitigations[damage_type]
        # Check for Base Mitigations
        if damage_type in self.BaseDamageMitigations:
            yield self.BaseDamageMitigations[damage_type]
