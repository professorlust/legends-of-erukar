from erukar.system.engine import Enemy
from erukar.content.conditions import Undead

class UndeadKnight(Enemy):
    BriefDescription = "an Undead Knight"

    def __init__(self, random=True):
        super().__init__("Undead Knight", random)
        self.str_ratio = 0.2
        self.dex_ratio = 0.2
        self.vit_ratio = 0.1
        self.acu_ratio = 0.1
        self.sen_ratio = 0.1
        self.res_ratio = 0.3
        self.define_level(14)
        self.conditions.append(Undead(self))
