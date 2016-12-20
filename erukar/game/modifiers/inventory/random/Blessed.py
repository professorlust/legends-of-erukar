from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
from erukar.engine.model.Observation import Observation
import numpy as np
import re

class Blessed(WeaponMod):
    Probability = 1
    Desirability = 8.0

    Glances = [
        Observation(acuity=0, sense=10, result='which fills you with hope'),
        Observation(acuity=0, sense=20, result='with a blessed {EssentialPart}')
    ]

    Inspects = [
        Observation(acuity=0, sense=10, result='You feel a sense of hopeful spirituality when looking upon the {alias}'),
        Observation(acuity=0, sense=20, result='You can sense that some sort of Divine entity has blessed the {EssentialPart} of the {alias}.')
    ]

    InventoryName = "Blessing"
    InventoryDescription = "Adds a small amount of Divine damage that scales as a factor environmental sanctity"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        self.weapon = weapon
        self.damage = Damage("Divine", [1,4], "", (np.random.uniform, (0,1)))
        weapon.damages.append(self.damage)

    def remove(self):
        self.weapon.damages.remove(self.damage)
        self.weapon.modifiers.remove(self)
        self.weapon = None
