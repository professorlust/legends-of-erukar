from erukar.system.engine import Enemy
from erukar.content.conditions import Undead, Ethereal

class Spectre(Enemy):
    BriefDescription = "a spectre"

    def __init__(self, random=True):
        super().__init__("Spectre", random)
        # Base stats should start negative as the template
        self.resolve   = -2
        self.sense     = 2
        self.acuity    = -3
        # Now personality
        self.str_ratio = 0.2
        self.dex_ratio = 0.2
        self.vit_ratio = 0.1
        self.acu_ratio = 0.1
        self.sen_ratio = 0.1
        self.res_ratio = 0.3
        self.define_level(5)
        self.conditions.append(Ethereal(self))
        self.conditions.append(Undead(self))
