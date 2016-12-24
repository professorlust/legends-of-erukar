from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
from erukar.engine.model.Observation import Observation
import numpy as np
import re

class Unholy(WeaponMod):
    Probability = 1
    Desirability = 8.0
    
    Glances = [
        Observation(acuity=0, sense=10, result='which fills you with dread'),
        Observation(acuity=0, sense=20, result='with a demonic {EssentialPart}'),
        Observation(acuity=0, sense=30, result='with an unholy {EssentialPart} that emanates purity')
    ]

    Inspects = [
        Observation(acuity=0, sense=10, result='You feel a sense of despair when looking upon the {alias}'),
        Observation(acuity=0, sense=20, result='You can sense that some sort of Demonic entity has created the {EssentialPart} of the {alias}.'),
        Observation(acuity=0, sense=30, result='You recognize that the demonic {EssentialPart} was crafted by a devil. The {alias} seems to profane the room through the use of some depraved aura.')
    ]

    InventoryName = "Unholy"
    InventoryDescription = "Adds a small amount of Demonic damage that scales as a factor environmental profanity; additionally projects an unholy aura in a 1-unit radius"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        self.weapon = weapon
        self.damage = Damage("Demonic", [1,4], "", (np.random.uniform, (0,1)))
        weapon.damages.append(self.damage)

    def remove(self):
        self.weapon.damages.remove(self.damage)
        self.weapon.modifiers.remove(self)
        self.weapon = None
