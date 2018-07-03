from ..base.Wood import Wood
from erukar.system.engine import Observation
import erukar


class Mahogany(Wood):
    Probability = 0.05
    Desirability = 1.0

    PriceMultiplier = 3.5
    WeightMultiplier = 1.9
    DurabilityMultiplier = 2.0

    InventoryName = "Mahogany"
    InventoryDescription = 'Fine wood which is used in expensive carpentry, its durability is matched by its price'

    PermittedEntities = [
        erukar.system.inventory.ArcaneWeapon,
        erukar.system.inventory.BowWeapon,
        erukar.system.inventory.CrossbowWeapon,
        erukar.system.inventory.SimpleWeapon,
        erukar.system.Ammunition
    ]
