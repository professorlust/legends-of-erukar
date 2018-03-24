from erukar.system.engine import Enemy
from ..templates.Undead import Undead
from erukar.content.inventory import Shortsword, Buckler
from erukar.content.modifiers import Steel, Oak

class Skeleton(Undead):
    BaseMitigations = {
        'bludgeoning': (-0.25, 0),
        'piercing': (0.2, 0),
        'slashing': (0.15, 0)
    }
    BriefDescription = "a skeleton holding a {describe|right} and a {describe|left}."

    def __init__(self, random=True):
        super().__init__("Skeleton", random)
        self.strength   =  5
        self.dexterity  =  4
        self.vitality   = -1
        self.acuity     = -2
        self.sense      = -2
        # Now personality
        self.str_ratio  = 0.4
        self.dex_ratio  = 0.3
        self.vit_ratio  = 0.2
        self.acu_ratio  = 0.0
        self.sen_ratio  = 0.0
        self.res_ratio  = 0.1
        self.stat_points = 8
        self.define_level(1)
        self.left = Buckler(modifiers=[Oak])
        self.right = Shortsword(modifiers=[Steel])
        self.inventory = [self.left, self.right]
