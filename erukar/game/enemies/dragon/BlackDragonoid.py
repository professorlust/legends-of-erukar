from erukar.engine.lifeforms.Enemy import Enemy
from erukar.engine.factories.ModuleDecorator import ModuleDecorator
from erukar.engine.model.Describable import Describable
import random

class BlackDragonoid(Enemy):
    BriefDescription = "a black dragonoid"

    def __init__(self):
        super().__init__("Black Dragonoid")
        self.strength = int(random.uniform(2, 5))
        self.dexterity = int(random.uniform(1, 4))
        self.vitality = int(random.uniform(4, 6))
        self.acuity = int(random.uniform(2, 3))
        self.sense = int(random.uniform(2, 5))
        self.resolve = int(random.uniform(1, 3))
        self.define_level(5)
        self.name = "Black Dragonoid"
        self.randomize_equipment()
        self.set_vision_results('You see a {alias}.','You see a {alias}. {describe}',(0,1))
        self.set_sensory_results('You hear movement.','You hear a {alias}.',(0, 1))
        self.set_detailed_results('There is a black dragonoid wielding {describe_weapon}.', 'There is a black dragonoid wearing {describe_armor} and wielding {describe_weapon}')

    def randomize_equipment(self):
        self.weapon_randomizer = ModuleDecorator('erukar.game.inventory.weapons', None)
        self.material_randomizer = ModuleDecorator('erukar.game.modifiers.material', None)
        self.weapon_mod_randomizer = ModuleDecorator('erukar.game.modifiers.inventory.random', None)

        self.left = self.create_random_weapon()
        self.right = self.create_random_weapon()
        self.inventory = [self.left, self.right]
        self.chest = self.create_random_armor('erukar.game.inventory.armor.chest')
        self.feet = self.create_random_armor('erukar.game.inventory.armor.boots')
        self.head = self.create_random_armor('erukar.game.inventory.armor.helm')

        del self.weapon_randomizer, self.weapon_mod_randomizer, self.material_randomizer

    def create_random_weapon(self):
        rand_weapon = self.weapon_randomizer.create_one()
        self.material_randomizer.create_one().apply_to(rand_weapon)
        self.weapon_mod_randomizer.create_one().apply_to(rand_weapon)
        return rand_weapon

    def create_random_armor(self, module):
        rand = ModuleDecorator(module, None)
        armor = rand.create_one()
        self.material_randomizer.create_one().apply_to(armor)
        return armor

    def describe_armor(self):
        res = []
        for x in self.equipment_types:
            if x not in self.attack_slots:
                res.append(getattr(self, x))
        res = [x.brief_inspect(None, 50, 50) for x in res if x is not None]
        return Describable.erjoin(x for x in res if x is not '')

    def describe_weapon(self):
        res = []
        for x in self.attack_slots:
            res.append(getattr(self, x))
        res = [x.brief_inspect(None, 50, 50) for x in res if x is not None]
        return Describable.erjoin(x for x in res if x is not '')
