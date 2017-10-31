from erukar.ext.ai.BaseAI import BaseAI
from erukar.system.engine import Indexer, Describable
from erukar.ext.math import Random, Namer
from .Lifeform import Lifeform
from .Player import Player
import math, random, string

class Enemy(Lifeform, Indexer):
    RandomizedArmor = []
    RandomizedWeapons = []
    ElitePointClassificationMinimum = 3.0

    def __init__(self, name="", world=None, is_random=True):
        Indexer.__init__(self)
        Lifeform.__init__(self, world,name)

        # Personality
        self.stat_points = 0
        self.elite_points = 0
        self.str_ratio = 0.1667
        self.dex_ratio = 0.1667
        self.vit_ratio = 0.1667
        self.acu_ratio = 0.1667
        self.sen_ratio = 0.1667
        self.res_ratio = 0.1667
        self.commander = None   # Used in conjuration or with Elites
        self.faction   = None   # Reserved
        self.spells    = []     # Enemies GENERALLY use pre-defined Spells instead of Spell words, though not necessarily 

        self.ai_module = BaseAI

        # Flavor
        self.history = []
        self.modifiers = []
        self.region = ''
        self.name = name

        # Randomized/Persistent enemy 
        self.is_transient = True
        self.requesting_persisted = False
        self.should_randomize = is_random

        chars = string.ascii_uppercase + string.digits
        self.uid = ''.join(random.choice(chars) for x in range(128))

    def is_hostile_to(self, lifeform):
        return isinstance(lifeform, Player)

    def define_level(self, level):
        self.level = level
        if self.should_randomize:
            self.perform_level_ups()
            self.redefine_personality()
        super().define_level(level)

    def redefine_personality(self):
        '''Used to give monsters a unique personality after initial levelup'''
        total = 14 + self.level
        for stat in self.AttributeTypes:
            stat_ratio = stat[:3] + '_ratio'
            new_ratio = max(getattr(self, stat) / total, 0)
            setattr(self, stat_ratio, new_ratio)
        stat_ratios = [stat[:3]+'_ratio' for stat in self.AttributeTypes]

    def alias(self):
        return self.name

    def is_elite(self):
        return self.elite_points >= Enemy.ElitePointClassificationMinimum and not self.is_transient

    def stop_execution(self):
        self.current_action_points = 0
        self.reserved_action_points = 0

    def perform_turn(self, instance):
        self.ai_module.perform_turn(self, instance)

    def perform_level_ups(self):
        while self.stat_points > 0:
            weights = [getattr(self, '{}_ratio'.format(stat[:3])) for stat in self.AttributeTypes]
            bins, values = Random.create_random_distribution(self.AttributeTypes, weights)
            chosen = Random.get_from_custom_distribution(random.random(), bins, values)
            setattr(self, chosen, getattr(self, chosen)+1)
            self.stat_points -= 1

    def award_xp(self, xp, target=None):
        super().award_xp(xp, target)
        self.perform_level_ups()

        if not target: return []
        if isinstance(target, Player)\
        or (isinstance(target, Enemy) and target.is_elite()):
            total_ep = max(0.5, 3.0 * target.level/self.level)
            self.award_elite_points(total_ep)
            self.history.append('Slew {}.'.format(target.alias()))
        return []

    def award_elite_points(self, amt):
        before = self.elite_points
        self.elite_points += amt
        self.check_for_elite_level_up(before)
        
    def check_for_elite_level_up(self, before):
        if before < 2.0 <= self.elite_points:
            self.is_transient = False

        if before < 3.0 <= self.elite_points:
            self.name = '{}, {}'.format(Namer.random(), self.name)
            mod = erukar.content.modifiers.enemy.Cloaked()
            mod.apply_to(self)
            # Get random inventory item (average)

        for point_threshold in self.elite_milestones:
            # Make sure we passed this threshold
            if before < point_threshold <= self.elite_points:
                mod = self.elite_milestones[point_threshold]
                if not mod:
                    # Choose randomly
                    mod = erukar.content.modifiers.enemy.Cloaked
                mod().apply_to(self)


        upgrade_increment = 25.0 if before > 50.0 else 10.0
        # The following is only possible if we pass the threshold of an upgrade
        if before % upgrade_increment > self.elite_points % upgrade_increment:
            # Add a weapon 
            # Gain a random modifier
            return 

    def viable_attack_targets(self, room):
        acuity, sense = [math.floor(random.uniform(*self.stat_random_range(x))) for x in ('acuity', 'sense')]
        for item in room.contents:
            # Can't be viable if it's not detected, can't be viable if is our commander
            if not item.is_detected(acuity, sense) or self.our_commander_is(item):
                continue

            # Typically, monsters are aggressive towards players so yield it if we've gotten this far
            if isinstance(item, Player):
                yield item

            # If you have sense < -2, you might attack inanimate objects...
            if self.sense <= -2 or isinstance(item, Lifeform):
                # If you have sense < -3, you might attack other enemies
                if self.sense > -3 and not isinstance(item, Player):
                    continue
                # If you have sense < -4, you might attack yourself on accident 
                if self.sense <= -4 or item is not self:
                    yield item

    def our_commander_is(self, target):
        return self.commander is not None and target is self.commander

    def lifeform(self):
        return self

    def kill(self, killer):
        self.history.append('Was slain by {}'.format(killer.uid))
        return super().kill(killer)

    def describe_armor(self):
        res = [getattr(self, x) for x in list(set(self.equipment_types) - set(self.attack_slots))]
        res = [x.brief_inspect(None, 50, 50) for x in res if x is not None]
        return Describable.erjoin(x for x in res if x is not '')

    def describe_weapon(self):
        res = [getattr(self, x) for x in self.attack_slots]
        res = [x.brief_inspect(None, 50, 50) for x in res if x is not None]
        return Describable.erjoin(x for x in res if x is not '')

    def request_persisted_enemy(self):
        self.requesting_persisted = True

    def on_inspect(self, lifeform, acu, sen):
        return 'A skeleton' 
        
