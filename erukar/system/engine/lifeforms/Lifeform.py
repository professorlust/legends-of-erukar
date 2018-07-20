from erukar.system.engine import ErukarActor, Dead, Dying, Armor, Weapon
from erukar.ext.math import Navigator, Distance
from .Zones import Zones
import erukar
import math
import random
import re
import logging
logger = logging.getLogger('debug')


class Lifeform(ErukarActor):
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
        "blessing",
        "ammunition",
        "healing_tool",
        "maintenance_tool"
    ]
    attack_slots = ["left", "right"]
    base_health = 30
    UnknownWordEfficiency = 0.01
    BaseDualWieldingPenalty = 60
    ArcaneEnergyRegenPercentage = 0.05
    BaseSenseToDetect = 10
    BaseAcuityToDetect = 10

    def __init__(self, world=None, name=""):
        super().__init__()
        self.faction = 'unknown'
        self.name = name
        self.uid = ""
        self.inventory = []
        self.initialize_stats()
        self.coordinates = (0, 0)
        self.world = world
        self.instance = ''
        self.sector = "(0,0,0)"
        self.detected_entities = {self}
        for eq_type in self.equipment_types:
            setattr(self, eq_type, None)
        self.zones = Zones()
        self.wealth = 0
        self.initialize_effects()
        self.movement_allowed = 0

    def build_from_payloads(stats, bio):
        out = Lifeform(None)
        for stat in stats:
            setattr(out, stat, stats[stat])
        out.name = bio['name']
        out.instance = 'TutorialDungeon'
        return out

    def initialize_effects(self):
        self.skill_points = 5
        self.skills = [
            erukar.system.engine.MicroMove(),
            erukar.system.engine.Move(),
            erukar.system.engine.Attack(),
        ]
        self.conditions = []
        self.spell_words = []
        self.reserved_action_points = 0
        self.current_action_points = 0

    def initialize_stats(self):
        self.stat_points = 15
        self.strength = 0
        self.dexterity = 0
        self.vitality = 0
        self.acuity = 0
        self.sense = 0
        self.resolve = 0
        self.experience = 0
        self.arcane_energy = 0
        self.health = self.base_health
        self.level = 1

    def maximum_health(self):
        _max = self.base_health + self.level_health() + self.vitality_health()
        mod_name = 'modify_maximum_health'
        return self.modify_element(mod_name, _max)

    def modify_element(self, mod_name, _el):
        for condition in self.conditions:
            if hasattr(condition, mod_name):
                _el = getattr(condition, mod_name)(self, _el) or _el
        for item in self.equipped_items():
            _el = item.modify_element(mod_name, _el) or _el
        return _el

    def level_health(self):
        if self.level <= 25:
            return 10 * self.level
        if self.level <= 50:
            return 250 + 7*(self.level-25)
        if self.level <= 100:
            return 425 + 5*(self.level-50)
        if self.level <= 150:
            return 675 + 3*(self.level-100)
        if self.level <= 200:
            return 825 + 2*(self.level-150)
        return 725 + self.level

    def vitality_health(self):
        if self.vitality <= 25:
            return 5 * self.vitality
        if self.vitality <= 50:
            return 125 + 3*(self.vitality - 25)
        if self.vitality <= 75:
            return 200 + 2*(self.vitality - 50)
        if self.vitality <= 125:
            return 250 + self.vitality - 75
        if self.vitality <= 200:
            return 300 + int(0.5*(self.vitality - 125))
        return int(337.5 + 0.1*(self.vitality-200))

    def is_hostile_to(self, lifeform):
        return lifeform.faction != self.faction

    def subscribe(self, instance):
        self.instance = instance.identifier
        self.world = instance.dungeon
        self.sector = instance.location.sector.get_coordinates()
        for skill in self.skills:
            if hasattr(skill, 'apply_to'):
                skill.apply_to(self)
        self.arcane_energy = self.maximum_arcane_energy()
        self.check_for_detectors()

    def check_for_detectors(self):
        for lf in self.world.sentient_actors(self):
            if lf.can_detect(self):
                lf.detected_entities.add(self)

    def add_skill(self, skill):
        self.skill_points  -= 1
        self.skills.append(skill)
        if hasattr(skill, 'apply_to'):
            skill.apply_to(self)

    def overland_coordinates(self):
        matches = re.match(r'\(([-+]*\d+),([-+]*\d+),([-+]*\d+)\)', self.sector)
        if not matches: return self.sector
        return tuple(int(x) for x in matches.group()[1:-1].split(','))

    def tick(self, cmd):
        '''Regular method which is performed every 5 seconds in game time'''
        # Tick all equipped items
        for item_slot in self.equipment_types:
            item = getattr(self, item_slot)
            if item is not None:
                item.tick(cmd, self)
        # Tick all conditions
        for condition in self.conditions:
            condition.tick(cmd)
        # regenerate arcane energy
        max_arcane = self.maximum_arcane_energy()
        if not self.is_incapacitated() and self.arcane_energy < max_arcane:
            self.arcane_energy = min(max_arcane, self.arcane_energy + int(max_arcane * Lifeform.ArcaneEnergyRegenPercentage))

    def get_object_by_uuid(self, uuid):
        for item in self.inventory:
            if item.uuid and item.uuid == uuid:
                return item

    def maximum_arcane_energy(self):
        return 0

    def get_skill(self, skill_class):
        if type(skill_class) is str:
            return next((x for x in self.skills if x.__module__ == skill_class), None)
        return next((x for x in self.skills if isinstance(x, skill_class)), None)

    def has_skill(self, _type, min_level=1):
        skill = self.get_skill(_type)
        return skill and skill.level >= min_level

    def initiate_aura(self, aura):
        '''Initiates an aura within the current room'''
        room = self.world.get_room_at(self.coordinates)
        room.initiate_aura(aura)

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
        total = self.modify_element('modify_attack_roll', raw)
        return int(total * efficiency)

    def on_check_for_hit(self, attacker, weapon, attack_roll):
        return attack_roll

    def get_damage_from_attack(self, target, weapon):
        return weapon.calculate_damage(self)

    def on_successful_attack(self, target, weapon, roll):
        pass

    def on_failed_dodge(self, attacker, weapon, attack_roll):
        pass

    def on_successful_dodge(self, attacker, weapon, attack_roll):
        pass

    def on_missed_attack(self, target, weapon, attack_roll):
        pass

    def post_successful_attack(self, cmd, attacker, weapon, target):
        pass

    def post_missed_attack(self, cmd, attacker, weapon, target):
        pass

    def apply_deflection(self, attacker, weapon, damages):
        post_deflection = []
        for damage in damages:
            amount, damage_type = damage
            dfl = self.deflection(damage_type)
            reduced = max(0, amount - dfl)
            if reduced > 0:
                post_deflection.append((reduced, damage_type))
        return post_deflection

    def apply_mitigation(self, attacker, weapon, damages):
        post_mitigation = []
        for damage in damages:
            amount, damage_type = damage
            mit = self.mitigation(damage_type)
            reduced = int(amount * mit)
            if reduced > 0:
                post_mitigation.append((reduced, damage_type))
        return post_mitigation

    def apply_damage(self, attacker, weapon, damages):
        undeflected = self.apply_deflection(attacker, weapon, damages)
        unmitigated = self.apply_mitigation(attacker, weapon, undeflected)
        total_damage = sum(x[0] for x in unmitigated)
        self.take_damage(total_damage, attacker)
        return {
            'post_deflection': undeflected,
            'post_mitigation': unmitigated,
            'total': int(total_damage)
        }

    def on_process_damage(self, attack_state, command):
        '''Called after a successful attack'''
        for condition in self.conditions:
            condition.on_process_damage(attack_state, command)
        if attack_state.weapon:
            attack_state.weapon.on_process_damage(attack_state, command)

    def detect_in_area(self, area):
        for loc in area:
            self.zones.all_seen.add(loc)
            for actor in self.world.actors_at(self, loc):
                if self.can_detect(actor):
                    self.detected_entities.add(actor)

    def can_detect(self, other):
        if not isinstance(other, ErukarActor):
            return False
        sen_min = other.minimum_sense_to_detect()
        acu_min = other.minimum_acuity_to_detect()
        acu, sen = self.get_detection_pair()
        acu *= self.vision_penalty(other)
        return other in self.detected_entities\
            or acu >= acu_min\
            or sen >= sen_min\
            or (acu >= acu_min * 0.75 and sen >= sen_min * 0.75)

    def vision_penalty(self, other):
        light = self.world.lighting_at(other.coordinates)
        distance = Navigator.distance(self.coordinates, other.coordinates)
        l_penalty = self.light_penalty(light)
        d_penalty = self.distance_penalty(distance)
        return (1 - l_penalty) * (1 - d_penalty)

    def light_penalty(self, light):
        if light > 0.5:
            return 0.0
        if light > 0.25:
            return 0.5
        if light > 0.1:
            return 0.75
        return 1.0

    def distance_penalty(self, dist):
        if dist < 8:
            return 0.0
        if dist < 16:
            return 0.5
        return 1.0

    def get_detection_pair(self):
        '''Retrieve a rolled Acuity and Sense for detection'''
        return [math.floor(random.uniform(*self.stat_random_range(x))) for x in ('acuity', 'sense')]

    def minimum_sense_to_detect(self):
        s2d = self.BaseSenseToDetect
        mod_name = 'modify_sense_to_detect'
        return self.modify_element(mod_name, s2d)

    def minimum_acuity_to_detect(self):
        a2d = self.BaseAcuityToDetect
        mod_name = 'modify_acuity_to_detect'
        return self.modify_element(mod_name, a2d)

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
        return math.floor(50 - 0.5*self.dexterity)

    def define_level(self, level):
        '''Set this lifeform's level and defined the health appropriately'''
        self.level = level
        self.health = self.maximum_health()

    def dual_wielding_penalty(self):
        '''Figures out the penalty for wielding a weapon in the character's offhand'''
        return (Lifeform.BaseDualWieldingPenalty - reduction) / 100.0

    def evasion(self):
        if self.is_incapacitated():
            return ErukarActor.base_evasion / 4
        base_ac = ErukarActor.base_evasion + self.get('dexterity')
        total_ac = self.modify_element('modify_evasion', base_ac)
        return total_ac

    def has_condition(self, aff_type):
        '''Alias to simplify the check to see if the lifeform has an affliction'''
        return any(x for x in self.conditions if isinstance(x, aff_type))

    def calculate_xp_worth(self):
        x = self.level
        if x >= 100:
            return 100*x
        return math.ceil((x/100)*(100*x) + ((100-x)/100) * (10+0.5*x*x + pow(2, math.exp((x-100)/x))))

    def calculate_necessary_xp(self):
        return 22*self.calculate_xp_worth()

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
        hp_proportion = self.health / self.maximum_health()
        self.level += 1
        output_strings.append('{} has leveled up! Now Level {}.'.format(self.alias(), self.level))
        self.health = int(math.ceil(self.maximum_health() * hp_proportion))

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
        logger.info(damage_amount)
        if self.has_condition(Dying):
            self.kill(killer=instigator)
            return
        self.health = max(0, self.health - damage_amount)
        if self.health == 0:
            self.conditions.append(Dying(self, None))

    def kill(self, killer):
        '''Mark us as dead, then return our net worth in XP'''
        self.conditions = [Dead(self, None)]
        dropped = self.inventory
        self.inventory = []
        for loc in self.equipment_types:
            setattr(self, loc, None)
        for item in dropped:
            if item.CannotDrop:
                continue
            self.world.add_actor(item, self.coordinates)
        self.world.refresh_tiles()

    def on_move(self, new_coordinates):
        '''Called after Move command starts'''
        self.coordinates = new_coordinates
        self.observe()
        for eq in self.equipment_types:
            equip = getattr(self, eq)
            if equip is not None:
                equip.on_move(new_coordinates)

    def observe(self, max_range=None, loc=None, radius=None):
        visual_area = list(Distance.direct_los(
            self.coordinates,
            self.world.all_traversable_coordinates(),
            max_range or self.visual_fog_of_war(),
            loc or self.coordinates,
            radius or max_range))
        self.detect_in_area(visual_area)

    def get(self, attribute):
        '''Alias for getattr(self, ____)'''
        base = getattr(self, attribute)
        mod_name = 'modify_{}'.format(attribute)
        return self.modify_element(mod_name, base)

    def matches(self, payload):
        return payload.lower() in self.alias().lower()

    def alias(self):
        return self.name

    def gain_action_points(self):
        self.reserved_action_points = self.current_action_points
        self.current_action_points = 2

    def action_points(self):
        return self.current_action_points + self.reserved_action_points

    def consume_action_points(self, amount):
        remainder = max(0, amount - self.current_action_points)
        self.current_action_points -= amount - remainder
        self.reserved_action_points -= remainder

    def move_speed(self):
        return 4 + math.floor(self.calculate_effective_stat('dexterity')/5)

    def provision_movement_points(self):
        if self.movement_allowed <= 0 and self.action_points() > 0:
            self.movement_allowed = self.move_speed()
            self.consume_action_points(1)
            return True
        return self.movement_allowed > 0

    def should_auto_end_turn(self):
        return self.action_points() <= 0 and self.movement_allowed <= 0

    def visual_fog_of_war(self):
        return 8.0

    def begin_turn(self, cmd):
        self.movement_allowed = 0
        self.gain_action_points()
        for condition in self.conditions:
            condition.do_begin_of_turn_effect(cmd)

    def end_turn(self, cmd):
        for condition in self.conditions:
            condition.do_end_of_turn_effect(cmd)

    def lifeform(self):
        return self

    def describe_as_threat(self, lifeform, acuity, sense):
        return self.on_inspect(lifeform, acuity, sense)

    def add_to_inventory(self, item):
        if item in self.inventory:
            return
        self.inventory.append(item)
        item.owner = self

    def possessive_pronoun(self):
        return 'his'

    def protections(self, damage_type):
        # Check for Mitigation in Armor
        for x in self.equipment_types:
            armor = getattr(self, x)
            if isinstance(armor, Armor):
                yield from armor.protection(damage_type)
        # Check for Mitigation Conditions
        for condition in self.conditions:
            yield from condition.damage_mitigation(damage_type)
        # Check for Base Mitigations
        if damage_type in self.BaseDamageMitigations:
            yield self.BaseDamageMitigations[damage_type]

    def weapon_slots(self):
        return ['left', 'right']

    def build_zones(self, world):
        self.zones.rebuild_if_desynced(self, world)

    def flag_for_rebuild(self):
        self.zones.desynced = True

    def offset_scale(self, weapon):
        method_name = 'offset_scale_for_{}'.format(type(weapon).Variant)
        actual_method = getattr(self, method_name, None)
        return 0 if not actual_method else actual_method()

    def max_weapon_range(self):
        weapons = list(self.viable_weapons())
        if not weapons or len(weapons) == 0:
            return 0
        return max([weapon.attack_range(self) for weapon in weapons])

    def viable_weapons(self):
        for slot in self.weapon_slots():
            weapon = getattr(self, slot)
            if weapon and isinstance(weapon, Weapon):
                yield weapon

    def additional_commands(self):
        for skill in self.skills:
            yield from skill.commands_provided()

    def find_uid_in_inventory(self, uid):
        for item in self.inventory:
            if str(item.uuid) == str(uid):
                return item

    def find_in_inventory(self, _type):
        for item in self.find_all_in_inventory(_type):
            return item

    def find_all_in_inventory(self, _type):
        for item in self.inventory:
            if isinstance(item, _type):
                yield item

    '''Used in Skills'''
    def disposition_bonuses(self, other):
        return 0

    def haggling_buy_modifier(self):
        return 0.8

    def haggling_sell_modifier(self):
        return 1.2

    def allocated_arcane_energy(self):
        '''
        This will be a specified value in the UI, but we
        will default to 50% for now
        '''
        return int(0.5 * self.maximum_arcane_energy())

    def get_key(self, key_type):
        for key in self.find_all_in_inventory(erukar.Key):
            if issubclass(type(key.material), key_type):
                return key
