from erukar.engine.lifeforms.Lifeform import Lifeform
from erukar.engine.model.Indexer import Indexer
from erukar.engine.model.Describable import Describable
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
import random, erukar, string

class Enemy(Lifeform, Indexer):
    RandomizedArmor = []
    RandomizedWeapons = []

    def __init__(self, name=""):
        Indexer.__init__(self)
        Lifeform.__init__(self, name)

        chars = string.ascii_uppercase + string.digits
        self.uid = ''.join(random.choice(chars) for x in range(128))

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

    def viable_targets(self, room):
        for item in room.contents:
            # A player should always be in this list
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
