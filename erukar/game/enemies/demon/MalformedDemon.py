from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.Sword import Sword
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
        self.set_vision_results('You see a demon.', 'You see a {alias}. {describe}',(1,15))
        self.set_sensory_results('You hear the unpleasant scraping of claws against the floor.', 'You hear the sounds of demon claws scraping against the floor, but the irregularity at which they move leads you to believe that the demon is malformed in some way.', (3, 30))
        self.set_detailed_results('The demon that you see is irregularly shaped and slightly deformed.', 'The demon in this room appears to have been deformed during its creation. It slouches to one side and its extremities are warped.')
