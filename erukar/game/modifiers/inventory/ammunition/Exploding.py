# Splits damage between all targets in room of impact
from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.engine.model.Damage import Damage
from erukar.engine.model.Observation import Observation
import numpy as np
import random

class Exploding(WeaponMod):
    Probability = 1
    Desirability = 8.0

    ShouldRandomizeOnApply = True
    PersistentAttributes = ['min_damage', 'max_damage', 'damage_type', 'InventoryDescription', 'InventoryName']
