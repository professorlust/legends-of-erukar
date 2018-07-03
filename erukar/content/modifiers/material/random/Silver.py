from ..base.Metal import Metal
from erukar.system.engine import Observation
import erukar


class Silver(Metal):
    Probability = 0.25
    Desirability = 4.0

    PriceMultiplier = 27
    WeightMultiplier = 1.8
    DurabilityMultiplier = 1.9

    InventoryName = "Silver"
    InventoryDescription = 'A semi-precious metal which is capable of piercing incorporeality'

    PermittedEntities = [
        erukar.system.Weapon,
        erukar.system.Ammunition,
        erukar.system.Armor
    ]
