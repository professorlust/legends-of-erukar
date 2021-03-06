from ..base.Cloth import Cloth
from erukar.system.engine import Observation
import erukar


class Cotton(Cloth):
    Probability = 0.05
    Desirability = 1.0

    PriceMultiplier = 0.5
    WeightMultiplier = 0.1
    DurabilityMultiplier = 0.2

    InventoryName = 'Cotton'
    InventoryDescription = 'Mass produced fabric which can be made into many different colors via the usage of dyes.'

    PermittedEntities = [
        erukar.system.Armor
    ]
