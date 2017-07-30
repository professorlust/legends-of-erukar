from ..base.Wood import Wood
from erukar.system.engine import Observation

class Ash(Wood):
    Probability = 0.05
    Desirability = 1.0

    PriceMultiplier = 0.7
    WeightMultiplier = 1.4
    DurabilityMultiplier = 1.1

    InventoryName = "Ash"
    InventoryDescription = 'A white hardwood which is fairly inexpensive and used with mass production'
