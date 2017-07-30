from ...base.WeaponMod import WeaponMod
from erukar.system.engine import Weapon

class NoModifier(WeaponMod):
    Probability = 1

    def apply_to(self, weapon):
        pass
