from erukar.game.modifiers.WeaponMod import WeaponMod
from erukar.game.conditions.negative.Frozen import Frozen
from erukar.engine.model.Observation import Observation
import random

class Freezing(WeaponMod):
    Probability = 1
    Desirability = 8.0

    Glances = [
    ]

    Inspects = [
    ]

    InventoryName = "Freezing"
    InventoryDescription = "Has a 5% chance to freeze target on hit"

    def on_apply_damage(self, damage_result):
        if random.random() >= 0.95:
           frozen = Frozen(damage_result.victim, damage_result.instigator) 
           damage_result.victim.conditions.append(frozen) 
