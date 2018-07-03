from ..base.Wood import Wood
from erukar.system.engine import Observation
import erukar


class Iurwood(Wood):
    Probability = 0.05
    Desirability = 1.0

    PriceMultiplier = 2.3
    WeightMultiplier = 1.2
    DurabilityMultiplier = 2.4

    InventoryName = "Iurwood"
    InventoryDescription = 'Native to Iuria, this wood is durable and expensive'

    PermittedEntities = [
        erukar.system.inventory.ArcaneWeapon,
        erukar.system.inventory.BowWeapon,
        erukar.system.inventory.CrossbowWeapon,
        erukar.system.inventory.SimpleWeapon,
        erukar.system.Ammunition
    ]
