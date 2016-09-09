from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar import Lifeform, Weapon
import math, random

class Enhancement(WeaponMod):
    Probability = 2
    Desirability = 4.0
    StatBonus = 2

    Types = [
        ('strength', 'red'),
        ('dexterity', 'yellow'),
        ('vitality', 'orange'),
        ('acuity', 'blue'),
        ('sense', 'purple'),
        ('resolve', 'green')]

    def __init__(self):
        super().__init__()
        self.stat_type, self.color = random.choice(self.Types)
        setattr(self, self.stat_type, self.StatBonus)
        enh_type = type(self).__name__.replace('Enhancement','')
        self.suffix = 'of {} {} Enhancement'.format(enh_type, self.stat_type.capitalize())

    def apply_to(self, weapon):
        super().apply_to(weapon)
        weapon.name = weapon.name + self.suffix
