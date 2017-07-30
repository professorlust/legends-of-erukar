from erukar.system.engine import Enemy
from erukar.content.conditions import Undead

class Risen(Enemy):
    BriefDescription = "a risen"

    def __init__(self, random=True):
        super().__init__("Risen", random)
        # Base stats should start negative as the template
        self.dexterity = -4
        self.vitality  = -2
        self.strength  =  1
        self.resolve   = -2
        self.sense     = -2
        self.acuity    = -1
        # Now personality
        self.str_ratio = 0.2
        self.dex_ratio = 0.05
        self.vit_ratio = 0.15
        self.acu_ratio = 0.0
        self.sen_ratio = 0.0
        self.res_ratio = 0.6
        self.define_level(1)
        self.conditions.append(Undead(self))
