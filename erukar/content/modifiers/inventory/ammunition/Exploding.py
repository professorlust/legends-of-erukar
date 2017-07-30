# Splits damage between all targets in room of impact
from erukar.content.modifiers.base import WeaponMod
from erukar.system.engine import Damage, Observation
import random

class Exploding(WeaponMod):
    Probability = 1
    Desirability = 8.0

    ShouldRandomizeOnApply = True
    PersistentAttributes = ['min_damage', 'max_damage', 'damage_type', 'InventoryDescription', 'InventoryName']
