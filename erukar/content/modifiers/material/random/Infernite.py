from ..base.MagicOre import MagicOre
from erukar.system.engine import Observation
import erukar


class Infernite(MagicOre):
    Probability = 0.05
    Desirability = 4.0

    PriceMultiplier = 31
    WeightMultiplier = 2.2
    DurabilityMultiplier = 1.1

    InventoryName = "Infernite"
    InventoryDescription = 'Hot to the touch, has a tendency to attract fiery and infernal magics'

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor
    ]
