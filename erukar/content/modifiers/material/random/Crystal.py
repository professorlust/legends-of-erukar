from ..base.Mineral import Mineral
from erukar.system.engine import Observation
import erukar


class Crystal(Mineral):
    Probability = 0.05
    Desirability = 16.0

    PriceMultiplier = 50
    WeightMultiplier = 4.5
    DurabilityMultiplier = 0.5

    InventoryName = "Crystal"
    InventoryDescription = 'Delicate, clear, and the most expensive material known to man'

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor,
    ]
