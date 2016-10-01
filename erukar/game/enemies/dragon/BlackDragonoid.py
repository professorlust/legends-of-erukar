from erukar.engine.lifeforms.Enemy import Enemy
import random

class BlackDragonoid(Enemy):
    BriefDescription = "a black dragonoid"
    RandomizedArmor = [
        ('feet', 'erukar.game.inventory.armor.chest'),
        ('chest', 'erukar.game.inventory.armor.boots'),
        ('head', 'erukar.game.inventory.armor.helm')
    ]
    RandomizedWeapons = [ 'left', 'right' ]

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

