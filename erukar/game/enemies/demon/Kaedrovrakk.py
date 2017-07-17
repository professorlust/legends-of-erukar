from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.standard.Halberd import Halberd
from erukar.game.modifiers.material import Abyssium
import erukar

class Kaedrovrakk(Enemy):
    Probability = 0.025

    def __init__(self):
        super().__init__("Kaedrovrakk")

        self.str_ratio = 0.1556
        self.dex_ratio = 0.1333
        self.vit_ratio = 0.2
        self.acu_ratio = 0.0778
        self.sen_ratio = 0.3889
        self.res_ratio = 0.0444

        self.randomize_equipment()
        self.define_level(26)
        self.conditions.append(erukar.engine.conditions.Dreadful(self))

    def randomize_equipment(self):
        self.right = Halberd()
        Abyssium().apply_to(self.right)
        self.left = Halberd()
        Abyssium().apply_to(self.left)

