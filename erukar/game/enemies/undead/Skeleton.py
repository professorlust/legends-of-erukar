from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.Sword import Sword
from erukar.game.inventory.armor.shields.Buckler import Buckler

class Skeleton(Enemy):
    def __init__(self):
        super().__init__("Skeleton")
        self.dexterity = -2
        self.vitality = -1
        self.define_level(1)
        self.name = "Skeleton"
        self.randomize_equipment()
        self.BriefDescription = "a skeleton holding a {describe|right} and a {describe|left}."
        self.set_vision_results('You see a {alias}.','You see a {alias}. {describe}',(0,1))
        self.set_sensory_results('You hear movement.','You hear a {alias}.',(0, 1))
        self.set_detailed_results('There is a skeleton holding a {describe_material|right}.','The skeleton is holding a {describe_material|right} in its right hand and {describe_material|left} in its left. ')

    def randomize_equipment(self):
        self.right = Sword()
        self.left = Buckler()
