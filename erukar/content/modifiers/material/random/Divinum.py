from ..base.MagicOre import MagicOre
from erukar.system.engine import Observation
import erukar


class Divinum(MagicOre):
    Probability = 0.05
    Desirability = 2.0

    PriceMultiplier = 28
    WeightMultiplier = 3.2
    DurabilityMultiplier = 6.3

    InventoryName = "Divinum"
    InventoryDescription = 'A holy ore which is highly durable and is predisposed towards sanctification'

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor
    ]
