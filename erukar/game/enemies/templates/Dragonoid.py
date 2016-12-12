from erukar.engine.lifeforms.Enemy import Enemy
import random

class Dragonoid(Enemy):
    RandomizedArmor = [
        ('feet', 'erukar.game.inventory.armor.chest'),
        ('chest', 'erukar.game.inventory.armor.boots'),
        ('head', 'erukar.game.inventory.armor.helm')
    ]
    RandomizedWeapons = [ 'left', 'right' ]

    def __init__(self, name):
        super().__init__(name)
        self.strength = int(random.uniform(2, 5))
        self.dexterity = int(random.uniform(1, 4))
        self.vitality = int(random.uniform(4, 6))
        self.acuity = int(random.uniform(2, 3))
        self.sense = int(random.uniform(2, 5))
        self.resolve = int(random.uniform(1, 3))
        self.define_level(5)
        self.name = name
        self.randomize_equipment()
