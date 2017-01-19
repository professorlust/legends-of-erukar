from erukar.engine.lifeforms.Enemy import Enemy
from erukar.game.inventory.weapons.standard.Sword import Sword
from erukar.game.inventory.armor.shields.Buckler import Buckler
import erukar

class Skeleton(Enemy):
    BaseMitigations = {
        'bludgeoning': (-0.25, 0),
        'piercing': (0.2, 0),
        'slashing': (0.15, 0)
    }
    BriefDescription = "a skeleton holding a {describe|right} and a {describe|left}."

    def __init__(self, random=True):
        super().__init__("Skeleton", random)
        self.dexterity  = -2
        self.vitality   = -1
        self.acuity     = -2
        self.sense      = -2
        # Now personality
        self.str_ratio  = 0.2
        self.dex_ratio  = 0.2
        self.vit_ratio  = 0.3
        self.acu_ratio  = 0.0
        self.sen_ratio  = 0.0
        self.res_ratio  = 0.3
        self.define_level(1)
        self.randomize_equipment()

    def randomize_equipment(self):
        s = Sword()
        b = Buckler()
        erukar.game.modifiers.material.Steel().apply_to(s)
        erukar.game.modifiers.material.Oak().apply_to(b)
        self.inventory = [s, b]
        self.left = s
        self.right = b
        self.conditions.append(erukar.game.conditions.magical.Undead(self))
