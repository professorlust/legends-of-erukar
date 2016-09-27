from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.Halberd import Halberd
from erukar.game.modifiers.material import Abyssium
import erukar

class Cuadrodemon(Enemy):
    Probability = 0.025

    def __init__(self):
        super().__init__("Cuadrodemon")
        self.dexterity = 12
        self.vitality = 18
        self.strength = 14
        self.resolve = 4
        self.acuity = 5
        self.sense = 30
        self.name = "Cuadrodemon"
        self.randomize_equipment()
        self.define_level(26)
        self.BriefDescription = "a Cuadrodemon holding a {describe|right} and a {describe|left}."
        self.set_vision_results('You see a {alias}.','You see a {alias}. {describe}',(0,1))
        self.set_sensory_results('You hear movement.','You hear a {alias}.',(0, 1))
        self.set_detailed_results('There is a Cuadrodemon holding a {describe_material|right}.','There is a Cuadrodemon holding {describe_material|right} in its right hand and {describe_material|left} in its left.')
        self.afflictions.append(erukar.engine.effects.Dreadful(self))

    def randomize_equipment(self):
        self.right = Halberd()
        Abyssium().apply_to(self.right)
        self.left = Halberd()
        Abyssium().apply_to(self.left)

