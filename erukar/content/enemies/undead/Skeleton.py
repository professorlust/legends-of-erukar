from erukar.system.engine import Enemy, BasicAI
from ..templates.Undead import Undead
from erukar.content.inventory import Shortsword, Buckler
from erukar.content.modifiers import Steel, Oak


class Skeleton(Undead):
    ClassName = 'Skeleton'
    ClassLevel = 1
    BaseMitigations = {
        'bludgeoning': (-0.25, 0),
        'piercing': (0.2, 0),
        'slashing': (0.15, 0)
    }
    BriefDescription = "a skeleton holding a {describe|right} and a {describe|left}."

    def init_stats(self):
        self.strength   =  5
        self.dexterity  =  4
        self.vitality   = -1
        self.acuity     = -2
        self.sense      = -2

    def init_personality(self):
        self.ai_module = BasicAI(self)
        self.str_ratio  = 0.4
        self.dex_ratio  = 0.3
        self.vit_ratio  = 0.2
        self.acu_ratio  = 0.0
        self.sen_ratio  = 0.0
        self.res_ratio  = 0.1
        self.stat_points = 8

    def init_inventory(self):
        self.left = Buckler(modifiers=[Oak])
        self.right = Shortsword(modifiers=[Steel])
        self.inventory = [self.left, self.right]
