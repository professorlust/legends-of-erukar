from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.standard.Sword import Sword
from erukar.game.inventory.armor.shields.Buckler import Buckler

class MalformedDemon(Enemy):
    BriefDescription = "a malformed demon"
    Probability = 1

    def __init__(self):
        super().__init__("Malformed Demon")
        self.dexterity = 1
        self.vitality = 0
        self.strength = 0
        self.resolve = 2
        self.sense = 2
        self.acuity = 1
        self.define_level(2)
        self.name = "Malformed Demon"
