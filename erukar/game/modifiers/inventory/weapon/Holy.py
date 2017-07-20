from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.inventory import Weapon
from erukar.engine.model.DamageBuilder import DamageBuilder
from erukar.engine.model.Observation import Observation
import numpy as np
import re

class Holy(WeaponMod):
    Probability = 1
    Desirability = 8.0
    
    Glances = [
        Observation(acuity=0, sense=10, result='which fills you with hope'),
        Observation(acuity=0, sense=20, result='with a divine {EssentialPart}'),
        Observation(acuity=0, sense=30, result='with a holy {EssentialPart} that emanates purity')
    ]

    Inspects = [
        Observation(acuity=0, sense=10, result='You feel a sense of hopeful spirituality when looking upon the {alias}'),
        Observation(acuity=0, sense=20, result='You can sense that some sort of Divine entity has created the {EssentialPart} of the {alias}.'),
        Observation(acuity=0, sense=30, result='You recognize that the divine {EssentialPart} was crafted by an archangel. The {alias} seems to purify the room of profanity through the use of some holy aura.')
    ]

    InventoryName = "Holy"
    InventoryDescription = "Adds a small amount of Divine damage that scales as a factor environmental sanctity; additionally projects a holy aura in a 1-unit radius"

    def apply_to(self, weapon):
        super().apply_to(weapon)
        self.weapon = weapon
        self.damage = DamageBuilder()\
            .with_type("Divine")\
            .with_range([1,4])\
            .with_distribution(np.random.uniform)\
            .with_properties((0,1))\
            .build()
        weapon.damages.append(self.damage)

    def remove(self):
        self.weapon.damages.remove(self.damage)
        self.weapon.modifiers.remove(self)
        self.weapon = None
