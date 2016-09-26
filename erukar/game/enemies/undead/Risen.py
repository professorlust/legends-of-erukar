from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.Sword import Sword
from erukar.game.inventory.armor.shields.Buckler import Buckler

class Risen(Enemy):
    BriefDescription = "a risen"
    def __init__(self):
        super().__init__("Risen")
        self.dexterity = -4
        self.vitality = -2
        self.strength = 1
        self.resolve = -2
        self.sense = -2
        self.acuity = -1
        self.define_level(1)
        self.name = "Risen"
        self.set_vision_results('You see a {alias}.','You see a {alias}. {describe}',(0,1))
        self.set_sensory_results('You hear shuffling.','You hear shuffling and smell death.',(0, 1))
        self.set_detailed_results('There is a Risen.', 'A walking corpse, a Risen, shuffles in this room')
