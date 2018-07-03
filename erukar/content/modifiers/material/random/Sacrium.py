from ..base.Mineral import Mineral
from erukar.system.engine import Observation
import erukar


class Sacrium(Mineral):
    Probability = 0.05
    Desirability = 4.0

    PriceMultiplier = 36
    WeightMultiplier = 0.4
    DurabilityMultiplier = 3.8

    InventoryName = "Sacrium"
    InventoryDescription = 'A resilient and incredibly lightweight, whitish metal that has mainly divine properties'

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor
    ]
