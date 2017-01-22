from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Indexer import Indexer
from erukar.engine.model.Describable import Describable
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.calculators import Random, Namer
import math, random, erukar, string

class Enemy(Lifeform, Indexer):
    RandomizedArmor = []
    RandomizedWeapons = []
    ElitePointClassificationMinimum = 3.0

    def __init__(self, name="", is_random=True):
        Indexer.__init__(self)
        Lifeform.__init__(self, name)
        self.stat_points = 0
        self.elite_points = 0
        self.str_ratio = 0.1667
        self.dex_ratio = 0.1667
        self.vit_ratio = 0.1667
        self.acu_ratio = 0.1667
        self.sen_ratio = 0.1667
        self.res_ratio = 0.1667
        self.history = []
        self.modifiers = []
        self.region = ''
        self.name = name

        self.is_transient = True
        self.requesting_persisted = False
        self.should_randomize = is_random

        self.elite_milestones = {
            3.0:  None,
            5.0:  erukar.game.modifiers.enemy.static.Infamous,
            10.0: erukar.game.modifiers.enemy.static.Fabled,
            15.0: erukar.game.modifiers.enemy.static.QuestTarget,
            25.0: erukar.game.modifiers.enemy.static.Legendary,
            40.0: erukar.game.modifiers.enemy.static.EpicQuestTarget,
            50.0: erukar.game.modifiers.enemy.static.Mythical,
        }

        chars = string.ascii_uppercase + string.digits
        self.uid = ''.join(random.choice(chars) for x in range(128))

    def define_level(self, level):
        self.level = level
        if self.should_randomize:
            self.stat_points = 14 + level
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
        if self.is_elite():
            return self.name
        return super().alias()

    def is_elite(self):
        return self.elite_points >= Enemy.ElitePointClassificationMinimum and not self.is_transient

    def perform_turn(self):
        targets = list(self.viable_targets(self.current_room))
        if len(targets) > 0:
            return self.do_attack(targets)
        return self.maybe_move_somewhere()

    def maybe_move_somewhere(self):
        for room_dir in list(self.current_room.adjacent_rooms()):
            room = self.current_room.get_in_direction(room_dir).room
            targets = list(self.viable_targets(room))
            if len(targets) > 0:
                return self.do_move(room_dir)

    def do_move(self, direction):
        m = erukar.engine.commands.executable.Move()
        m.sender_uid = self.uid
        m.user_specified_payload = direction.name
        return m

    def do_attack(self, targets):
        target = random.choice(targets)
        a = erukar.engine.commands.executable.Attack()
        a.sender_uid = self.uid
        a.user_specified_payload = target.alias()
        return a

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
        if isinstance(target, erukar.engine.lifeforms.Player)\
        or (isinstance(target, erukar.engine.lifeforms.Enemy) and target.is_elite()):
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
            mod = erukar.game.modifiers.enemy.Cloaked()
            mod.apply_to(self)
            # Get random inventory item (average)

        for point_threshold in self.elite_milestones:
            # Make sure we passed this threshold
            if before < point_threshold <= self.elite_points:
                mod = self.elite_milestones[point_threshold]
                if not mod:
                    # Choose randomly
                    mod = erukar.game.modifiers.enemy.Cloaked
                mod().apply_to(self)


        upgrade_increment = 25.0 if before > 50.0 else 10.0
        # The following is only possible if we pass the threshold of an upgrade
        if before % upgrade_increment > self.elite_points % upgrade_increment:
            # Add a weapon 
            # Gain a random modifier
            return 

    def viable_targets(self, room):
        acuity, sense = [math.floor(random.uniform(*self.stat_random_range(x))) for x in ('acuity', 'sense')]
        for item in room.contents:
            # A player should always be in this list
            if not item.is_detected(acuity, sense):
                continue

            if isinstance(item, erukar.engine.lifeforms.Player):
                yield item

            # If you have sense < -2, you might attack inanimate objects...
            if self.sense <= -2 or isinstance(item, erukar.engine.lifeforms.Lifeform):
                # If you have sense < -3, you might attack other enemies
                if self.sense > -3 and not isinstance(item, erukar.engine.lifeforms.Player):
                    continue
                # If you have sense < -4, you might attack yourself on accident 
                if self.sense <= -4 or item is not self:
                    yield item

    def lifeform(self):
        return self

    def kill(self, killer):
        self.history.append('Was slain by {}'.format(killer.uid))
        return super().kill(killer)

    def randomize_equipment(self):
        self.material_randomizer = ModuleDecorator('erukar.game.modifiers.material', None)
        self.left = self.create_random_weapon()
        self.right = self.create_random_weapon()

        for slot in self.RandomizedWeapons:
            setattr(self, slot, self.create_random_weapon())

        for slot,module in self.RandomizedArmor:
            setattr(self, slot, self.create_random_armor(module))

        self.inventory = [getattr(self, x) for x in [y for y,i in self.RandomizedArmor] + self.RandomizedWeapons]
        del self.material_randomizer

    def create_random_weapon(self):
        weapon_randomizer = ModuleDecorator('erukar.game.inventory.weapons', None)
        weapon_mod_randomizer = ModuleDecorator('erukar.game.modifiers.inventory.random', None)

        rand_weapon = weapon_randomizer.create_one()
        self.material_randomizer.create_one().apply_to(rand_weapon)
        weapon_mod_randomizer.create_one().apply_to(rand_weapon)
        return rand_weapon

    def create_random_armor(self, module):
        rand = ModuleDecorator(module, None)
        armor = rand.create_one()
        self.material_randomizer.create_one().apply_to(armor)
        return armor

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
