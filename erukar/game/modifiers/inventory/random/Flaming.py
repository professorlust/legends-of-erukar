from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.Damage import Damage
from erukar.engine.model.Observation import Observation
import numpy as np
import re

class Flaming(WeaponMod):
    Probability = 1
    Desirability = 8.0

    Glances = [
        Observation(acuity=0, sense=0, result='with a fiery {EssentialPart}'),
        Observation(acuity=20, sense=0, result='with flames erupting from the {EssentialPart}')
    ]

    Inspects = [
        Observation(acuity=0, sense=0, result='The {EssentialPart} is on fire.'),
        Observation(acuity=10, sense=0, result='Flames rise off of the {EssentialPart}.'),
        Observation(acuity=10, sense=10, result='Flames rise off of the {EssentialPart}, radiating a large amount of heat through the room..'),
        Observation(acuity=20, sense=0, result='A plume of flames rises from the {EssentialPart}.'),
        Observation(acuity=20, sense=10, result='A plume of flames rises from the {EssentialPart}, radiating a large amount of heat through the room.')
    ]

    InventoryName = "Fire Elemental"
    InventoryDescription = "Adds a small amount of non-scaling fire damage to physical attacks"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        self.weapon = weapon
        self.damage = Damage("Fire", [1,4], "", (np.random.uniform, (0,1)))
        weapon.damages.append(self.damage)

    def remove(self):
        self.weapon.damages.remove(self.damage)
        #self.weapon.name = re.sub(' of the Flames', '', self.weapon.name)
        self.weapon.modifiers.remove(self)
        self.weapon = None
