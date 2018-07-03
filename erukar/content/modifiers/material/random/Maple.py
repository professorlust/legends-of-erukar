from ..base.Wood import Wood
from erukar.system.engine import Observation
import erukar


class Maple(Wood):
    Probability = 0.05
    Desirability = 1.0

    PriceMultiplier = 0.5
    WeightMultiplier = 0.7
    DurabilityMultiplier = 0.8

    InventoryName = "Maple"
    InventoryDescription = 'Cheap wood which is used in mass-production carpentry'

    PermittedEntities = [
        erukar.system.inventory.ArcaneWeapon,
        erukar.system.inventory.BowWeapon,
        erukar.system.inventory.CrossbowWeapon,
        erukar.system.inventory.SimpleWeapon,
        erukar.system.Ammunition
    ]
