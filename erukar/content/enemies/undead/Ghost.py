from erukar.system.engine import Enemy
from erukar.content.conditions import Ethereal, Undead

class Ghost(Enemy):
    BriefDescription = "a ghost"

    def __init__(self, random=True):
        super().__init__("Ghost", random)
        # Base stats should start negative as the template
        self.resolve   = -2
        self.sense     = 2
        self.acuity    = -3
        # Now personality
        self.str_ratio = 0.15
        self.dex_ratio = 0.25
        self.vit_ratio = 0.15
        self.acu_ratio = 0.1
        self.sen_ratio = 0.25
        self.res_ratio = 0.1
        self.define_level(11)
        self.conditions.append(Ethereal(self))
        self.conditions.append(Undead(self))
