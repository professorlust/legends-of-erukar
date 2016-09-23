from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar import Weapon

class Enhancement(WeaponMod):
    Probability = 0
    Desirability = 0
    StatType = ""
    StatEnhancement = "<bug> Enhancement"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = '{} of {}'.format(weapon.name, self.StatEnhancement)
