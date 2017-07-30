from ..base.Cloth import Cloth
from erukar.system.engine import Observation

class Silk(Cloth):
    Probability = 0.05
    Desirability = 1.0

    PriceMultiplier = 0.9
    WeightMultiplier = 0.1
    DurabilityMultiplier = 0.1

    InventoryName = 'Silk'
    InventoryDescription = 'Intricate fabric used primarily by the aristocracy'
