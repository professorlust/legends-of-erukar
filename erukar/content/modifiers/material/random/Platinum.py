from ..base.Metal import Metal
from erukar.system.engine import Observation
import erukar


class Platinum(Metal):
    Probability = 0.05
    Desirability = 16.0

    PriceMultiplier = 45
    WeightMultiplier = 2.7
    DurabilityMultiplier = 1.6

    InventoryName = "Platinum"
    InventoryDescription = 'An incredibly rare metal which is often mistaken for silver'

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor
    ]
