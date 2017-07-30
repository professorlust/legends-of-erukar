from erukar.system.engine import Enemy
from erukar.content.conditions import Undead

class Ghoul(Enemy):
    BriefDescription = "a ghoul"

    def __init__(self, random=True):
        super().__init__("Ghoul", random)
        # Base stats should start negative as the template
        self.resolve   = -2
        self.sense     = -2
        self.acuity    = -1
        # Now personality
        self.str_ratio = 0.25
        self.dex_ratio = 0.25
        self.vit_ratio = 0.2
        self.acu_ratio = 0.0
        self.sen_ratio = 0.0
        self.res_ratio = 0.3
        self.define_level(8)
        self.conditions.append(Undead(self))
