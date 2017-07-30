from erukar.system.engine import Enemy
from erukar.content.conditions import Undead

class Revenant(Enemy):
    RandomizedWeapons = ['right', 'left']

    def __init__(self, random=True):
        super().__init__("Revenant", random)
        self.str_ratio = 0.2
        self.dex_ratio = 0.2
        self.vit_ratio = 0.15
        self.acu_ratio = 0.15
        self.sen_ratio = 0.15
        self.res_ratio = 0.15
        self.define_level(10)
        self.randomize_equipment()
        self.conditions.append(Undead(self))
